# Content Director — Bundle

A complete trend-research -> script -> camera -> edit pipeline for short-form video, packaged as
one registered Content Director skill with nested format playbooks. The user gives you their IG
or TikTok handle. You discover real, currently-viral trends across four formats, hand them the
production package, route them into the recording flow, and ship the final edited mp4.

## What's in the bundle

```
content-director/             ← top-level routing skill (this is where it starts)
├── SKILL.md                  ← registered `/pika:content-director` router
├── formats/
│   ├── talking.md            ← talking-to-camera (spoken to lens)
│   ├── pov.md                ← silent POV (acting + on-screen captions)
│   ├── duet.md               ← stitch / duet (react to a viral original)
│   ├── dance.md              ← AI-generated dance from one photo
│   ├── teleprompter.md       ← teleprompter handoff contract
│   └── teleprompter.html     ← browser camera + scrolling prompter source
└── README.md                 ← this file
```

Only `content-director/SKILL.md` is registered as a user-invoked skill. The format files under
`formats/` are playbooks the router loads after Stage 0 locks the format. The teleprompter HTML
source is the same static page deployed to `https://teleprompter.pika.bot/`.

## How the user reaches each skill

| User intent | Entry point | Trigger phrases |
|---|---|---|
| "Be my content director" / "what kind of trend should I make" | `content-director` | The orchestrator; Stage 0 figures out which of the four formats fits, then routes. |
| Already knows they want a spoken hot-take / storytime / hook | `content-director talking` | Loads `formats/talking.md`. |
| Wants silent POV acting | `content-director pov` | Loads `formats/pov.md`. |
| Wants to react to a specific viral video | `content-director duet` | Loads `formats/duet.md`. |
| Wants AI dance from one photo | `content-director dance` | Loads `formats/dance.md`. |

The teleprompter is **not user-invokable**. It's a sub-tool the talking and duet skills hand off
into during Stage 4f (after script approval). Its contract is documented in
`formats/teleprompter.md`; the deployed page source is `formats/teleprompter.html`.

## End-to-end flow

```
                                  ┌───────────────────────────────────────┐
                                  │   content-director (Stage 0-1) │
                                  │   - intake handle                     │
                                  │   - recommend OR show cross-format    │
                                  │     sampler                           │
                                  │   - route                             │
                                  └──────────────┬────────────────────────┘
                                                 │
            ┌───────────────────┬────────────────┴───────────────┬────────────────────┐
            ▼                   ▼                                ▼                    ▼
       talking              pov                               duet                  dance
   Stages 0-7:        Stages 0-7:                       Stages 0-7:           Stages 0-7:
   profile,           profile,                          profile,              profile,
   trend research,    POV trend research,               find viral original,  dance trend research,
   menu, script       menu, captions+shot list,         menu, reaction        menu, motion-control,
                                                       script,
            │                   │                                │                    │
            ▼                   ▼                                ▼                    ▼
      [Stage 4f]          (no prompter —              [Stage 4f]              (no prompter —
   TELEPROMPTER          shot list                  TELEPROMPTER             AI-generated,
      HANDOFF             handed directly)             HANDOFF                no filming)
            │                                                │
            ▼                                                ▼
      user records on phone (teleprompter.pika.bot/r?t=...)
      hits Upload → MCP upload-return → agent polls status_url
            │                                                │
            └─────────────────┬──────────────────────────────┘
                              ▼
                       Stage 5: receive take
                       Stage 6: edit + captions + audio mix
                       Stage 7: deliver + loop
```

## The teleprompter — what makes it special

A single static HTML page at `teleprompter.pika.bot`, backed by a short-token MCP handoff. The
agent stores the approved script, browser `upload_url`, and `aspect_ratio` in the MCP jobs registry,
then gives the user a sparse QR-friendly URL like `https://teleprompter.pika.bot/r?t=...` plus a
returned `qr_image_url` for phone scanning.

Key behaviors:

- **Top-anchored read zone** — the line you're reading sits at the very top of the screen, right
  under the front-facing camera lens. The line crossing the read zone grows + brightens; lines
  above fade and shrink. The user's eye-line stays high, not down at their lap.
- **Per-line pacing** — scroll velocity is computed per chunk as `(distance to next line) ÷
  (this line's word count ÷ wpm × 60)`. A 1-word zinger like "Cents." dwells 0.55s; a 10-word
  sentence dwells ~4.3s at 140 wpm. Same WPM, very different pixel speeds — by design.
- **1.5-line lead-in** — the first line parks below the read zone so when scrolling starts after
  the 3-2-1 countdown, line 1 visibly travels upward into position. No "blink and miss" start.
- **Smart line breaking** — splits on `. , ! ? —` and force-breaks chunks over 7 words at the
  most natural break word (`and`, `or`, `to`, `per`, `of`, etc.) near the middle. Orphans
  (`yeah,` alone) get merged back.
- **Mirrored output** — when the mirror toggle is on, recording is routed through a hidden
  `<canvas>` with `ctx.scale(-1, 1)`, so the recorded MP4 matches what the user saw in preview.
- **Upload-return first, Share fallback** — the page uploads the take through the browser-safe
  `upload_url`; if that fails, `navigator.share({ files: [...] })` opens the iOS share sheet
  (AirDrop, Save Video to Photos, Messages, Mail) on iOS Safari 14+ and falls back to a download
  on desktop browsers.
- **Protocol-selected recording ratio** — the handoff can request `9:16`, `16:9`, `1:1`, or `4:5`.
  The page shows that ratio before recording and records through a matching canvas.
- **Live controls** — SPEED and SIZE sliders always visible above the record button (stacked on
  phone, side-by-side on tablet+). No hunting in menus mid-take.

The deployed URL is **production-stable**. Each session changes only the token; the underlying app
is the same. The token expires with the MCP handoff/upload-return session.

## Updating the teleprompter

Source lives in `formats/teleprompter.html`. To redeploy:

1. `mcp__plugin_pika_pika__upload_asset` with `filename: teleprompter.pdf`,
   `mime_type: application/pdf` (HTML isn't allow-listed by upload_asset; PDF mime is accepted
   and the bytes are served as text/html when web_publish republishes them at `index.html`).
2. PUT the HTML bytes to the returned `presigned_url`.
3. `mcp__plugin_pika_pika__web_publish` with `slug: pika-teleprompter`,
   `files: [{path: "index.html", source_url: <public_url from step 1>}]`.
4. Verify with `curl -sI https://teleprompter.pika.bot/` — content-type should be
   `text/html`.

If you're picking this up as a maintainer, start with `content-director/SKILL.md` to
understand the routing model. The two heaviest playbooks are `formats/talking.md` and
`formats/duet.md`; they're each self-contained pipelines with stage-by-stage guidance.
