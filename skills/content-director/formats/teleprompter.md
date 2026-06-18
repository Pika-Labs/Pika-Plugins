---
name: teleprompter-handoff
description: >-
  Browser-based camera + teleprompter that the content-director talking and duet playbooks
  can hand the user once the script is ready. Works on iOS Safari, Android Chrome, and desktop —
  HTTPS required for camera access. The user opens the link on their phone, sees the script
  scrolling in a top-anchored "read zone" right under the camera lens, hits record, gets a 3-2-1
  countdown, can re-shoot as many times as they want, then uploads the take through
  a short-token MCP handoff or falls back to Share/Save locally.
  This is an ADD-ON — format playbooks produce the
  URL; the page handles everything else.
argument-hint: "<script> [handle] [trend] [format]"
---

# Content Director — Teleprompter (browser camera + prompter add-on)

## What this does

The `formats/talking.md` and `formats/duet.md` playbooks both reach a point where
they hand the user a script and say *"now film it."* That hand-off used to be a dead-end — the
user had to copy the script into a phone teleprompter app, set up framing, fight with prompter
speed, and remember to send the result back.

The handoff replaces that step with a one-tap short link. The agent calls
`mcp__plugin_pika_pika__create_teleprompter_handoff` and sends the returned URL:

```
https://teleprompter.pika.bot/r?t=...
```

The user taps it → camera + prompter come up → they hit record → re-shoot → **Upload**.
The page uses the token to fetch `script`, `upload_url`, and `aspect_ratio` from MCP. It POSTs
`{mime_type,size_bytes}` to that browser-safe `upload_url`. The start response returns
`direct_upload_url`, `direct_upload_headers`, `attempt_id`, and `complete_url`; the page PUTs the
recorded Blob directly to the CDN URL, then POSTs the `attempt_id` to `complete_url`. The agent
polls the returned `status_url` until it sees `public_url`, then resumes its pipeline (captions,
edit, etc.). If upload fails, the page falls back to Share/Save so the user can still send the take
manually.

### Upload-return flow

The canonical playbook handoff uses `mcp__plugin_pika_pika__create_teleprompter_handoff`. **Do NOT pass raw `upload_asset` presigned URLs** to the browser:
short-lived presigned URLs can expire during a realistic recording session (open link → adjust
speed → 2-3 takes → preview → upload), and they put a storage bearer URL in front of the user before
the user is ready to upload.

So for this flow: call `create_teleprompter_handoff`, emit its short `teleprompter_url`, and keep
its `status_url` in agent state only. The MCP handoff row stores the script, `upload_url`, and
`aspect_ratio`; the browser fetches those through `/api/teleprompter-handoff?t=...`. Do not pass the
agent-pollable `status_url` to the browser. The page sends a JSON start request to `upload_url`,
receives `direct_upload_url`, `direct_upload_headers`, `attempt_id`, and `complete_url`, PUTs the
Blob to the CDN URL, then completes the session by POSTing `{attempt_id}`. The MCP upload-return
endpoint mints the short-lived CDN presign only when upload starts, so recording time no longer
races the presign TTL.

### Used by

- ✅ `formats/talking.md` (Stage 4f) — script is the spoken delivery to camera
- ✅ `formats/duet.md` (Stage 4f) — script is the user's reaction half of the stitch/duet
- ❌ `formats/pov.md` — silent acting, deliverable is on-screen captions + shot list
- ❌ `formats/dance.md` — AI-generated dance from a photo, no live filming

## The short-token contract

`create_teleprompter_handoff` returns:

| Field | Who uses it | What it does |
|---|---|---|
| `teleprompter_url` | User/browser | Short URL, normally `https://teleprompter.pika.bot/r?t=...`. This is what the agent surfaces to the user and QR generator. |
| `qr_image_url` | User/agent | Browser-viewable SVG QR image for the same `teleprompter_url`. Render this in chat so desktop users can scan with a phone. |
| `status_url` | Agent only | Poll until it returns `status="uploaded"` with `public_url`. Never show this URL to the browser. |
| `aspect_ratio` | Agent + browser | Recording ratio used by the page and shown to the user. Supported: `9:16`, `16:9`, `1:1`, `4:5`. Default: `9:16`. |
| `expires_at` | Agent | User-facing expiry if needed. |

The browser then reads `/api/teleprompter-handoff?t=...`, which returns only browser-safe state:
`script`, optional `handle`/`trend`/`format`, `aspect_ratio`, `upload_url`, and expiry. It does not
return `status_url`.

Legacy/manual fallback: the page still accepts `script`/`s`, `handle`, `trend`, `format`,
`aspect_ratio`/`aspect`, and `#upload=...` for local testing. Production playbooks should use the
short-token MCP tool so QR codes stay sparse.

## Wiring into the playbooks

In `formats/talking.md` or `formats/duet.md` Stage 4f (or wherever the script is finalized), add a
step:

1. Create the teleprompter handoff:
   ```python
   handoff = mcp__plugin_pika_pika__create_teleprompter_handoff(
       script=state.script_text,
       handle=state.handle,
       trend=state.pick.name,
       format=state.format,              # "talking" or "duet"
       aspect_ratio=getattr(state, "recording_aspect_ratio", "9:16"),
       filename=f"{state.handle.lstrip('@')}-{state.format}-take.webm",
       mime_type="video/webm",          # preferred; endpoint accepts browser mp4/webm variants in the same family
       max_size_bytes=350_000_000,      # enough for a short 9:16 phone take
       expires_in_s=86400,
   )
   state.teleprompter_url = handoff["teleprompter_url"]
   state.teleprompter_qr_image_url = handoff["qr_image_url"]
   state.teleprompter_status_url = handoff["status_url"]
   state.teleprompter_aspect_ratio = handoff["aspect_ratio"]
   ```
2. **Emit `state.teleprompter_url` and `state.teleprompter_qr_image_url`** to the chat — see the next section.
3. Tell the user to record, hit **Upload**, and return to chat. If upload fails, the page opens the Share/Save fallback.
4. Poll `state.teleprompter_status_url` until it returns `status="uploaded"` with `public_url`, then resume the pipeline with that uploaded take.

The page itself is stateless — no DB, no auth, no analytics. The temporary handoff state lives in
the MCP jobs registry behind the short token.

## The handoff — URL + returned QR image (canonical pattern)

Every time the agent hands off the link, show both values returned by
`create_teleprompter_handoff`:

1. **The clickable URL** — for desktop users who want to record at their workstation, or who'd
   rather paste the link into their phone manually.
2. **The `qr_image_url` SVG** — for desktop users who want to record on their phone.
   Scanning it opens the same URL with the same script preloaded. No copy-paste, no typing, and
   no local Python package dependency.

Do not invent a local helper name and do not hard-code an unapproved third-party service in the
skill:

```python
qr_image_url = state.teleprompter_qr_image_url
```

Then render it in the handoff message:

```markdown
![Scan QR]({qr_image_url})
```

Caption the QR with the same message as the URL — e.g. *"Film it on your phone — scan or click."*
If the QR image fails to render in a client, keep the clickable URL visible as the fallback.

### URL length budget

QR codes get progressively denser as URLs grow. The short-token URL is normally far below the risky
range, which is why this handoff exists. Practical thresholds:

| URL length | Result |
|---|---|
| **< 600 chars** | Sparse QR, scans instantly even in dim light |
| **600 – 1200** | Dense, still reliable |
| **1200 – 1800** | Very dense — needs a clean phone screen and steady hand. Last reasonable tier. |
| **> 1800** | Skip the QR, surface only the clickable URL with a "tap to open on this device" instruction |

If the URL is going to exceed 1500 chars, something is wrong: do not put the script or upload URL
back into the QR. Use `create_teleprompter_handoff` so the script stays server-side behind the
token.

### Example handoff message

```
🎬 Your script is ready. Film it on your phone:

📱 Scan this QR on your phone (opens teleprompter.pika.bot with the script preloaded):
   ![Scan QR]({qr_image_url})

🔗 Or open directly:
   {state.teleprompter_url}

When you're done, hit Upload. I'll watch the upload status and start the edit as soon as the take lands. If upload fails, use Share/Save and send the MP4 back here.
```

## Hosting

Two clean options:

- **`web_publish`** — push `teleprompter.html` to Pika's static host and use the returned HTTPS
  URL forever. Best for production.
- **`capture_website` (dev only)** — not useful here; this page needs real camera access from the
  user's device.

For local development: `python3 -m http.server 8443 --bind 127.0.0.1` won't work for mobile
testing because mobile browsers refuse camera on non-HTTPS, non-localhost origins. Easiest mobile
dev loop is `web_publish` to a temporary URL.

## What the page does on its own

- Asks for camera + mic on tap (iOS Safari requires a user gesture for `getUserMedia`).
- Renders the script with each line broken on natural pauses (`. , ! ? —`), then force-splits any
  chunk over 7 words at the most natural break-word (and / or / to / per / of / from / etc.) near
  the middle so 20-word run-ons don't survive. Tiny orphan fragments (under 8 chars or a leading
  conjunction/article on its own) get merged back into the previous chunk so you don't get
  "yeah," sitting alone.
- Anchors a glowing **read zone** at the very top of the prompter window — close to the front
  camera. The line crossing that zone grows + brightens; lines that have already passed fade and
  shrink. The user's eye-line stays high.
- **Lead-in:** the first line is parked ~1.5 line heights below the read zone so when scrolling
  starts after the countdown, line 1 travels visibly upward into position — giving the user a
  beat to lock onto it before they have to speak. (Without this it lands on the read zone the
  instant REC fires, which is too sudden to track.)
- **Per-line pacing:** scroll velocity is computed per line as `(distance to next line) ÷
  (this line's word count ÷ wpm × 60)`, floored at 0.55s, so a 1-word zinger like "Cents." gets
  time to breathe and a 10-word sentence scrolls past at the right reading speed. The same WPM
  setting means very different pixel speeds in different parts of the script — by design.
- Picks the best supported MIME (`video/mp4;codecs=h264,aac` first on iOS 17+, falls back to webm
  on Android/desktop).
- Shows the requested recording ratio on the start screen. Default is `9:16` (`1080×1920`), but the
  handoff can request `16:9` (`1920×1080`), `1:1` (`1080×1080`), or `4:5` (`1080×1350`). The page
  records through that target-aspect canvas with cover-crop normalization, so a mismatched physical
  camera stream still uploads the requested take shape.
- Records via `MediaRecorder`, plays back the take, and lets the user re-shoot or upload.
- If the handoff provides `upload_url`, starts the upload-return session with JSON, PUTs the Blob to
  the returned `direct_upload_url`, POSTs `attempt_id` to `complete_url`, and falls back to
  Share/Save if any step fails.

## Controls (built in)

All controls live on the main record screen — nothing important is hidden in a menu.

| Control | What |
|---|---|
| **● REC** | Big red button. Tap → 3-2-1 countdown → recording starts; prompter starts scrolling. Tap again → stop → preview screen. |
| **00:00 timer** | Sits just above the slider row when recording — never overlays the script. |
| **SPEED slider** (60–240 wpm) | Live on the main screen. Adjustable mid-take without opening any menu. |
| **SIZE slider** (22–46 px) | Live on the main screen. Adjustable mid-take. |
| **⟲ Re-shoot** | Discards take, re-parks the first line below the read zone, ready to go again. |
| **Upload / Share / Save** | Preview action. With upload-return it uploads first; without upload-return or after upload failure it uses native Share or download. |
| **Tap the prompter** | Pause / resume scroll during recording. In Manual mode (settings), tapping advances one line. |
| **⇋ Mirror** | Top-right toggle and also in settings — preview only; the recorded video is canonical. |
| **⚙ Settings sheet** | Slides up from the bottom — only contains the two toggles (Mirror, Manual). The sliders are NOT here. |
| **✕** | Top-left bail-out — confirms before discarding. |

## What this playbook is NOT

- Not a backend. No accounts, no recording-history, no streaming. One-page, stateless.
- Not a production switcher. It's a single-person front-camera setup.
- Not a beam-splitter prompter. The read zone is the best compromise — eye-line drift is minimal
  but not zero.

## Triggers (in case the user invokes it directly)

Mostly you'll never trigger this page standalone — the parent playbook calls it. But if the
user says any of:

- "give me a teleprompter for this script"
- "open the camera + prompter"
- "set up the recording page"
- "let me film this in the browser"

…produce a URL with at least `script=` and hand them the link.
