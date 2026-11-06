# Security Policy

## Reporting a vulnerability

Please report suspected vulnerabilities privately through the DausaXmusic support group:
https://t.me/DAUSA_123

Do not post access tokens, session strings, API keys, database URIs, or exploit details in public chats. Include the affected version, a concise impact description, and safe reproduction steps. Do not include real user data.

## Supported deployment practices

- Keep `.env`, Telegram sessions, cookies and API keys private.
- `COOKIE_URL` is optional and intended only for your own authorized Netscape cookie export over HTTPS. Never use a public paste or another person's session; no cookie file is bundled.
- Rotate credentials that may have been exposed.
- Use least-privilege Telegram permissions and private logging groups.
- Keep MongoDB private and restrict network access.
