# DausaXmusic — Railway Deployment Guide (हिंदी)

इस guide का उपयोग corrected project के साथ करें। इसमें कोई `.env`, bot token, session string, database password या cookie शामिल नहीं है।

## 1. जरूरी तैयारी

आपके पास ये चीजें होनी चाहिए:

1. Telegram bot और उसका token — [@BotFather](https://t.me/BotFather) से।
2. Telegram `API_ID` और `API_HASH` — https://my.telegram.org से।
3. Voice-chat assistant के लिए कम से कम एक Kurigram/Pyrogram session string।
4. MongoDB Atlas या कोई दूसरा reachable MongoDB database।
5. एक private Telegram log group/channel और उसका numeric `LOGGER_ID`।
6. Corrected source code वाला GitHub repository।

**Session string सुरक्षा:** session string assistant account का पूरा access दे सकती है। इसे केवल स्थानीय, विश्वसनीय Kurigram/Pyrogram तरीके से generate करें। किसी अज्ञात website, public paste, GitHub issue या chat में न डालें।

## 2. GitHub पर सही project root

Repository की root directory में सीधे ये files दिखनी चाहिए:

- `Dockerfile`
- `railway.json`
- `requirements.txt`
- `config.py`
- `sample.env`
- `DAUSAXMUSIC/`

`DAUSAXMUSIC/` के अंदर एक और project root nest न करें। ZIP को repository में ZIP के रूप में upload न करें; पहले extract करें और extracted project की **contents** upload करें। विस्तृत commands के लिए `GITHUB_UPLOAD.md` देखें।

## 3. Railway project बनाएं

1. Railway dashboard में **New Project → Deploy from GitHub Repo** चुनें।
2. अपना `dausaloki/DausaXmusic` repository या आपका fork चुनें।
3. अगर **Root Directory** पूछा जाए तो उसे खाली या `/` रखें—`DAUSAXMUSIC` subdirectory न चुनें।
4. Builder को Dockerfile रहने दें। Repository का `railway.json` पहले से यही configure करता है:
   - Builder: `DOCKERFILE`
   - Dockerfile: repository-root `Dockerfile`
   - Start command: `python -m DAUSAXMUSIC`
   - Restart: केवल failure पर, अधिकतम 10 retries
5. Start command को बदलने की जरूरत नहीं है। `Procfile` का `worker: bash start` भी इसी module को चलाता है।
6. यह background/worker bot है; web server, HTTP port या `PORT` variable की आवश्यकता नहीं है।

### Image में पहले से शामिल चीजें

- Python 3.12 (`python:3.12-slim`)
- FFmpeg और FFprobe
- Deno 2.9.8 और `yt-dlp-ejs` 0.8.0 — current yt-dlp YouTube extraction के लिए
- Git और required native build/media libraries
- `requirements.txt` की Python dependencies

## 4. Railway Variables — न्यूनतम आवश्यक सूची

Railway service के **Variables** section में ये values जोड़ें। नाम बिल्कुल इसी रूप में होने चाहिए:

| Variable | क्या डालना है |
|---|---|
| `API_ID` | https://my.telegram.org वाला numeric API ID |
| `API_HASH` | उसी Telegram app का API hash |
| `BOT_TOKEN` | @BotFather का bot token |
| `MONGO_DB_URI` | आपके MongoDB का full connection URI |
| `LOGGER_ID` | Log group/channel का numeric chat ID; सामान्यतः negative ID |
| `STRING_SESSION` | Primary assistant की Kurigram/Pyrogram session string |

**कम से कम एक assistant session अनिवार्य है।** `STRING_SESSION` की जगह `STRING_SESSION2`, `STRING_SESSION3`, `STRING_SESSION4` या `STRING_SESSION5` में से कोई एक भी primary valid session के रूप में इस्तेमाल हो सकता है। सामान्य single-assistant deployment के लिए `STRING_SESSION` ही रखें।

Bulk-variable template (पहले values भरें, फिर deploy करें):

```dotenv
API_ID=
API_HASH=
BOT_TOKEN=
MONGO_DB_URI=
LOGGER_ID=
STRING_SESSION=
```

## 5. Branding variables

इनके सही defaults code और `sample.env` में पहले से हैं। इन्हें Railway में explicitly रखना optional है, लेकिन values verify कर लें:

```dotenv
OWNER_NAME=𝐋𝐎𝐊𝐄𝐒𝐇 𝐃𝐀𝐔𝐒𝐀
OWNER_ID=1236703127
OWNER_USERNAME=lokesh_dausa
BOT_NAME=⏤͟͞• ˹𝚀𝚄𝙴𝙴𝙽 ✘ ᴍᴜsɪᴄ˼🫧
BOT_USERNAME=DAUSA_MUSIC1_BOT
INSTAGRAM_URL=https://instagram.com/lokesh_dausa1
SUPPORT_CHAT=https://t.me/DAUSA_123
SUPPORT_CHANNEL=https://t.me/kalam_se
```

`BOT_USERNAME` में `@` न लगाएं। Bot name और owner branding को बदलने की जरूरत नहीं है।

Optional provider, voice-play, cache, duration और tuning variables की **पूरी 86-variable table** `ENVIRONMENT_VARIABLES.md` में है। किन्हें unchanged रखना है और केवल `COOKIE_URL` का optional behavior क्या बदला है, उसकी exact सूची `RAILWAY_VARIABLES_FINAL.md` में है। केवल इस्तेमाल की जा रही optional services के credentials जोड़ें; सभी optional keys भरना आवश्यक नहीं है।

## 6. Telegram और MongoDB checks

Deploy से पहले:

- Bot को `LOGGER_ID` वाले group/channel में जोड़ें और **admin** बनाएं।
- Bot को test group में जोड़ें और voice chat के लिए आवश्यक permissions दें।
- Assistant account test group तक पहुंच सकता हो।
- MongoDB user को केवल आवश्यक database permissions दें।
- MongoDB Atlas network access में Railway से connection की अनुमति हो।
- URI, username और password को logs, screenshots या GitHub में साझा न करें।

## 7. Deploy और logs

Variables सेव करने के बाद **Deploy/Redeploy** करें। Deployments के logs देखें।

सही startup के मुख्य संकेत:

```text
MongoDB client initialized; connection is verified on first use.
Bot client initialized.
Modules loaded.
DausaXmusic started successfully.
```

Telegram log group में bot का startup message भी आना चाहिए। ध्यान दें: **Docker image build हो जाना अकेले live deployment का प्रमाण नहीं है।** Telegram login, assistant authentication, MongoDB access और voice-call playback अलग से verify करना होगा।

### सामान्य errors

- `Missing required environment variables` → बताए गए variables की value जोड़ें और redeploy करें।
- `Bot cannot access LOGGER_ID` → bot को log chat में जोड़ें और admin बनाएं।
- `No assistant started` → session string, assistant account और session validity जांचें।
- Mongo authentication/timeout → URI, database user, password escaping और network access जांचें।
- कोई optional AI/provider feature unavailable हो → उसकी credentials और third-party service status जांचें; core bot variables दोबारा न बदलें।

### YouTube song-name और URL playback

Playback source order अब **direct yt-dlp → existing optional Worker → existing optional xBit** है। Direct playback के लिए Worker या xBit API key की आवश्यकता नहीं है। ये variables blank रह सकते हैं; यदि पहले से configured हैं तो उन्हें हटाने की जरूरत नहीं है।

- `requirements.txt` से `yt-dlp==2026.10.26`, `deno==2.9.8` और `yt-dlp-ejs==0.8.0` install होते हैं।
- Dockerfile build में Deno, EJS import और FFmpeg verify किए जाते हैं।
- Direct source public YouTube videos के लिए single-file, FFmpeg-compatible stream चुनता है। कोई cookie, PO Token, proxy या paid API bundled/required नहीं है।
- Existing required variables और `MONGO_DB_URI` बदलने की जरूरत नहीं है। कोई नया required playback variable नहीं जोड़ा गया है।
- `YOUTUBE_STREAM_PREFLIGHT=1` recommended default है; यदि Railway में यह variable मौजूद नहीं है तो default पहले से enabled है।

सफल direct playback के logs इस प्रकार दिख सकते हैं:

```text
Direct yt-dlp format selected | media=audio | ... | format=18 | container=mp4
YouTube source ok | source=direct_ytdlp | media=audio | ...
```

किसी public video पर third-party extraction fail हो तो sanitized `Direct yt-dlp extraction failed` log देखें। केवल `YouTube source failed` की आखिरी line को root cause न मानें। कुछ private, age-restricted, DRM-protected या otherwise unavailable videos के लिए direct playback उपलब्ध नहीं होगा; authentication या restrictions bypass नहीं किए जाते।

**Railway IP limitation:** आपके supplied Railway screenshot में bot startup सफल था, लेकिन YouTube ने HTTP 429 और `Sign in to confirm you're not a bot` दिया। यह MongoDB, Telegram startup या FFmpeg failure नहीं है। Sandbox में direct test pass होना Railway पर guaranteed playback साबित नहीं करता, क्योंकि datacenter IP और session reputation अलग होते हैं। किसी client change या code-only setting को guaranteed anti-bot fix न मानें।

यदि आपके पास अपने authorized YouTube account का session है तो existing optional `COOKIE_URL` अब supported है:

1. अपने account का yt-dlp-compatible **Netscape `cookies.txt`** export सुरक्षित रूप से तैयार करें।
2. उसे किसी private, expiring HTTPS location पर रखें जिसे आप control करते हैं; public paste/GitHub में नहीं।
3. Railway में `COOKIE_URL=https://...` सेट करके redeploy करें। Loader public HTTPS host, 1 MiB limit और Netscape format validate करता है; file को private temporary permissions में रखता है और URL/content log नहीं करता।
4. `COOKIE_URL` blank रखने पर पुराना anonymous direct path अपरिवर्तित है। Cookies expire हो सकती हैं और यह भी playback guarantee नहीं है।

किसी और के cookies, copied Worker key, PO Token, proxy या anti-bot/DRM bypass का उपयोग न करें। Authorized session/provider उपलब्ध न हो और challenge बना रहे तो Railway IP पर legitimate code-only guarantee संभव नहीं है।

## 8. Crash/restart loop से बचाव

- `railway.json` में `ON_FAILURE` और `restartPolicyMaxRetries: 10` है, इसलिए configuration गलत होने पर अनंत restart loop configured नहीं है।
- Fatal startup errors अब nonzero exit देते हैं, जिससे Railway failure को सही पहचानता है।
- Missing variables ठीक करने के बाद manually redeploy करें।
- बार-बार failure हो तो पहले हालिया failure का **पहला root-cause log** देखें; केवल आखिरी restart message न देखें।
- अनावश्यक `ALWAYS` restart policy न लगाएं।

## 9. Live deployment verification checklist

- [ ] Railway ने repository root का `Dockerfile` इस्तेमाल किया।
- [ ] Build में Python dependencies और FFmpeg install हुए।
- [ ] Logs में `ModuleNotFoundError`, `youtubesearchpython.future` या HTTPX `proxies` error नहीं है।
- [ ] `Modules loaded.` और `DausaXmusic started successfully.` दिखाई दिया।
- [ ] Log group में startup message आया।
- [ ] `/start`, `/help` और `/ping` काम कर रहे हैं।
- [ ] Test group की active voice chat में assistant join हो रहा है।
- [ ] `/play` से audio सुनाई दे रहा है; `/queue` सही queue दिखा रहा है।
- [ ] Pause, resume, skip, stop और autoplay जांचे गए।
- [ ] `/vplay` और media controls जांचे गए।
- [ ] `/lyrics`, thumbnails और song download जांचे गए।
- [ ] Favorites, playlist और अन्य उपयोग किए जाने वाले commands जांचे गए।
- [ ] Restart के बाद MongoDB settings/data बने रहे।
- [ ] CPU, RAM, disk और restart behavior सामान्य है।
- [ ] Optional providers को अलग से जांचा गया; उनकी बाहरी availability को core startup success न माना गया।

## 10. Local/static verification commands

Python 3.12 और FFmpeg के साथ project root से:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt pytest
pip check
python -m compileall -q DAUSAXMUSIC strings scripts tests config.py
python -m pytest -q

# कोई output न आना चाहिए:
grep -RIn --include='*.py' 'youtubesearchpython\.future' DAUSAXMUSIC
```

इन checks के अलावा real bot test के लिए `.env` में अपनी private values रखकर `python -m DAUSAXMUSIC` चलाएं। `.env` को फिर Git में न डालें।

## 11. Security notes

- `.env`, `cookies.txt`, `*.session`, `*.session-journal`, real tokens और Mongo URI commit न करें।
- ZIP में जानबूझकर कोई cookie/session/secret file शामिल नहीं है।
- पुराने exposed credentials हों तो deploy से पहले rotate करें।
- Railway के cache/log files ephemeral हैं; persistent data के लिए MongoDB पर भरोसा करें, container filesystem पर नहीं।
- `COOKIE_URL` optional active consumer है, लेकिन केवल अपने authorized Netscape export के लिए उपयोग करें। किसी third-party का session कभी न लें; ZIP/repository में cookie file नहीं है।
