from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BOT = ROOT / "DAUSAXMUSIC"


class BrandingTests(unittest.TestCase):
    def test_original_developer_identity_is_not_in_bot_sources(self):
        forbidden = (
            "Siddhartha",
            "EliteGen",
            "EliteMusic",
            "VivaanXMusic",
            "VivaanXmusic",
            "SkyBotsDeveloper",
            "VivaanUpdates",
            "VivaanSupport",
            "EliteSid",
            "Ruhu's",
        )
        sources = [ROOT / "config.py", ROOT / "app.json"]
        sources.extend(
            path
            for base in (BOT, ROOT / "strings")
            for path in base.rglob("*")
            if path.is_file() and path.suffix in {".py", ".yml", ".yaml"}
        )
        offenders = []
        for path in sources:
            text = path.read_text(encoding="utf-8")
            for marker in forbidden:
                if marker in text:
                    offenders.append(f"{path.relative_to(ROOT)}: {marker}")
        self.assertEqual([], offenders)

    def test_reference_image_uses_approved_dausa_artwork(self):
        player = BOT / "assets" / "thumb" / "player"
        self.assertEqual(
            (player / "dausaxmusic-cyan-reference.png").read_bytes(),
            (player / "design-reference.png").read_bytes(),
        )

    def test_dynamic_player_uses_neutral_runtime_template(self):
        renderer = (BOT / "utils" / "thumbnail_renderer.py").read_text(encoding="utf-8")
        self.assertIn('TEMPLATE_PATH = ASSET_DIR / "cinematic-template.png"', renderer)
        self.assertNotIn("design-reference.png", renderer)
        self.assertNotIn("dausaxmusic-cyan-reference.png", renderer)


if __name__ == "__main__":
    unittest.main()
