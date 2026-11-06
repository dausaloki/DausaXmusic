import asyncio
import importlib.util
import logging
import os
import sys
import tempfile
import types
from contextlib import contextmanager
from pathlib import Path
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "DAUSAXMUSIC" / "platforms" / "Youtube.py"
SOURCE_EVENTS = []


def _module(name, **attributes):
    module = types.ModuleType(name)
    for key, value in attributes.items():
        setattr(module, key, value)
    return module


def _time_to_seconds(value):
    return sum(
        int(part) * 60**index
        for index, part in enumerate(reversed(str(value).split(":")))
    )


def _set_source_status(video_id, text):
    SOURCE_EVENTS.append((video_id, text))


def _load_youtube_module():
    dausa = _module("DAUSAXMUSIC", LOGGER=logging.getLogger)
    dausa.__path__ = []
    utils = _module("DAUSAXMUSIC.utils")
    utils.__path__ = []
    stream = _module("DAUSAXMUSIC.utils.stream")
    stream.__path__ = []
    stubs = {
        "DAUSAXMUSIC": dausa,
        "DAUSAXMUSIC.utils": utils,
        "DAUSAXMUSIC.utils.stream": stream,
        "DAUSAXMUSIC.utils.database": _module(
            "DAUSAXMUSIC.utils.database", is_on_off=AsyncMock(return_value=True)
        ),
        "DAUSAXMUSIC.utils.formatters": _module(
            "DAUSAXMUSIC.utils.formatters", time_to_seconds=_time_to_seconds
        ),
        "DAUSAXMUSIC.utils.url_guard": _module(
            "DAUSAXMUSIC.utils.url_guard",
            is_safe_media_url=lambda url: isinstance(url, str)
            and url.startswith("https://")
            and len(url) <= 4096,
        ),
        "DAUSAXMUSIC.security": _module(
            "DAUSAXMUSIC.security", build_subprocess_env=lambda: dict(os.environ)
        ),
        "DAUSAXMUSIC.utils.stream.source_status": _module(
            "DAUSAXMUSIC.utils.stream.source_status",
            set_youtube_source_status=_set_source_status,
        ),
        "DAUSAXMUSIC.utils.esse_autoplay": _module(
            "DAUSAXMUSIC.utils.esse_autoplay",
            is_playable_autoplay_metadata=lambda *args: True,
            select_or_fallback=AsyncMock(),
        ),
        "config": _module(
            "config",
            DURATION_LIMIT=18000,
            YT_API_KEY="",
            YTPROXY_URL="",
            autoclean=[],
        ),
    }
    with patch.dict(sys.modules, stubs):
        spec = importlib.util.spec_from_file_location(
            "youtube_direct_under_test", MODULE_PATH
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module


youtube = _load_youtube_module()


class FakeYoutubeDL:
    instances = []
    info = {}
    error = None

    def __init__(self, options):
        self.options = options
        type(self).instances.append(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def extract_info(self, url, download=False):
        if type(self).error:
            raise type(self).error
        return dict(type(self).info)

    def download(self, urls):
        output = self.options.get("outtmpl")
        if not output:
            raise AssertionError("Fake download requires an explicit output path")
        Path(output).write_bytes(b"\x00" * (128 * 1024))


@contextmanager
def _temporary_working_directory():
    previous = Path.cwd()
    with tempfile.TemporaryDirectory() as directory:
        os.chdir(directory)
        Path("downloads").mkdir()
        try:
            yield Path(directory)
        finally:
            os.chdir(previous)


class DirectYouTubePlaybackTest(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Executor/thread startup can exceed the debug loop's 100 ms warning
        # threshold on CI; that timing warning is unrelated to playback behavior.
        asyncio.get_running_loop().slow_callback_duration = 60

    def setUp(self):
        SOURCE_EVENTS.clear()
        FakeYoutubeDL.instances = []
        FakeYoutubeDL.error = None
        FakeYoutubeDL.info = {
            "id": "abc123",
            "url": "https://media.example.test/progressive.mp4",
            "format_id": "18",
            "ext": "mp4",
            "protocol": "https",
            "acodec": "mp4a.40.2",
            "vcodec": "avc1.42001E",
            "http_headers": {
                "User-Agent": "TestAgent/1.0",
                "Accept-Language": "en-US",
                "Cookie": "must-not-be-forwarded",
                "Range": "bytes=0-1023",
            },
        }
        self.api = youtube.YouTubeAPI()
        self.no_paid_apis = patch.multiple(
            youtube,
            WORKER_FALLBACK_API_URL="",
            WORKER_FALLBACK_API_KEY="",
            YTPROXY="",
            YT_API_KEY="",
        )
        self.fake_extractor = patch.object(
            youtube.yt_dlp, "YoutubeDL", FakeYoutubeDL
        )
        self.no_paid_apis.start()
        self.fake_extractor.start()

    def tearDown(self):
        self.fake_extractor.stop()
        self.no_paid_apis.stop()

    async def _cancel_background_cache(self):
        tasks = list(self.api._background_cache_tasks.values())
        for task in tasks:
            task.cancel()
        for task in tasks:
            try:
                await task
            except BaseException:
                pass
        self.api._background_cache_tasks.clear()

    async def test_audio_stream_uses_direct_ytdlp_before_optional_apis(self):
        preflight = AsyncMock(return_value=True)
        with _temporary_working_directory(), patch.object(
            youtube, "validate_playable_stream_url", preflight
        ):
            result = await self.api.download(
                "abc123",
                None,
                videoid=True,
                stream=True,
                title="Test Song",
            )
            await self._cancel_background_cache()

        self.assertEqual(
            result,
            ("https://media.example.test/progressive.mp4", False),
        )
        preflight.assert_awaited_once_with(
            "https://media.example.test/progressive.mp4", "audio"
        )
        options = FakeYoutubeDL.instances[0].options
        self.assertEqual(
            options["extractor_args"],
            {"youtube": {"player_client": ["android"]}},
        )
        self.assertTrue(options["format"].startswith("18/"))
        self.assertNotIn("cookiefile", options)
        self.assertNotIn("po_token", str(options).lower())
        self.assertEqual(SOURCE_EVENTS[-1], ("abc123", "direct yt-dlp ok (audio)"))

    async def test_video_stream_requires_one_combined_media_url(self):
        with _temporary_working_directory(), patch.object(
            youtube,
            "validate_playable_stream_url",
            AsyncMock(return_value=True),
        ):
            result = await self.api.download(
                "abc123",
                None,
                videoid=True,
                video=True,
                stream=True,
                title="Test Video",
            )
            await self._cancel_background_cache()

        self.assertEqual(result[1], False)
        options = FakeYoutubeDL.instances[0].options
        self.assertIn("acodec!=none", options["format"])
        self.assertIn("vcodec!=none", options["format"])
        self.assertNotIn("bestvideo+bestaudio", options["format"])
        self.assertEqual(SOURCE_EVENTS[-1], ("abc123", "direct yt-dlp ok (video)"))

    async def test_direct_local_download_preserves_cache_contract_and_filters_headers(self):
        with _temporary_working_directory():
            file_path, direct = await self.api.download(
                "abc123",
                None,
                videoid=True,
                stream=False,
                title="Test Song",
            )
            path = Path(file_path)
            self.assertTrue(direct)
            self.assertEqual(path, Path("downloads/abc123.mp3"))
            self.assertTrue(path.is_file())
            self.assertGreaterEqual(path.stat().st_size, 128 * 1024)

        self.assertEqual(len(FakeYoutubeDL.instances), 2)
        download_headers = FakeYoutubeDL.instances[1].options["http_headers"]
        self.assertEqual(download_headers["User-Agent"], "TestAgent/1.0")
        self.assertNotIn("Cookie", download_headers)
        self.assertNotIn("Range", download_headers)

    async def test_extraction_failure_is_sanitized_and_returns_no_track(self):
        FakeYoutubeDL.error = RuntimeError(
            "request failed for https://media.example.test/video?token=never-log-this"
        )
        with _temporary_working_directory(), self.assertLogs(
            youtube.logger, level=logging.WARNING
        ) as captured:
            result = await self.api.download(
                "abc123",
                None,
                videoid=True,
                stream=True,
                title="Test Song",
            )

        self.assertEqual(result, (None, True))
        logs = "\n".join(captured.output)
        self.assertIn("Direct yt-dlp extraction failed", logs)
        self.assertIn("<redacted-url>", logs)
        self.assertNotIn("never-log-this", logs)
        self.assertIn(
            "sources=direct_ytdlp,worker_fallback,xbit_fallback", logs
        )

    async def test_live_video_cli_uses_android_and_combined_format(self):
        process = types.SimpleNamespace(returncode=0)
        process.communicate = AsyncMock(
            return_value=(b"https://media.example.test/live.m3u8\n", b"")
        )
        create_process = AsyncMock(return_value=process)
        with patch.object(
            youtube.asyncio, "create_subprocess_exec", create_process
        ):
            status, url = await self.api.video(
                "https://www.youtube.com/watch?v=abc123"
            )

        self.assertEqual(status, 1)
        self.assertEqual(url, "https://media.example.test/live.m3u8")
        arguments = create_process.await_args.args
        self.assertIn("youtube:player_client=android", arguments)
        self.assertIn("--no-playlist", arguments)
        format_selector = arguments[arguments.index("-f") + 1]
        self.assertIn("acodec!=none", format_selector)
        self.assertIn("vcodec!=none", format_selector)

    def test_error_sanitizer_removes_signed_urls(self):
        sanitized = youtube.safe_yt_dlp_error(
            RuntimeError("403 at https://media.example.test/a?signature=secret")
        )
        self.assertIn("RuntimeError", sanitized)
        self.assertNotIn("signature=secret", sanitized)
        self.assertIn("<redacted-url>", sanitized)
