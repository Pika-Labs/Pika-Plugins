---
name: content-director-format-talking
description: >-
  Talking-to-camera content director. Takes an IG or TikTok handle, surfaces TTC
  trends with hard view-count proof (storytime, hot-take, "He's a 10 but…", GRWM-talk,
  confessional, "things nobody tells you", "POV explaining" — niche-fit + broad-viral),
  then for the chosen one writes a spoken script in the user's voice, an exact shot list,
  and finishes a 9:16 mp4 with trending audio mixed under the voice and word-sync
  captions burned in the IG Reels safe zone. Triggers — "be my talking-head content
  director", "find storytime trends for me", "make me a talking-to-camera trend",
  "TTC trends for {handle}", "hot-take trend for my niche", "content-director talking".
argument-hint: <instagram-or-tiktok-handle>
required-capabilities:
  - mcp__plugin_pika_pika__scrape_social
  - mcp__plugin_pika_pika__capture_website
  - mcp__plugin_pika_pika__probe_media
  - mcp__plugin_pika_pika__transcribe_audio
  - mcp__plugin_pika_pika__analyze_media
  - mcp__plugin_pika_pika__extract_audio_from_video
  - mcp__plugin_pika_pika__edit_trim
  - mcp__plugin_pika_pika__edit_reframe
  - mcp__plugin_pika_pika__edit_concat
  - mcp__plugin_pika_pika__edit_audio_stitch
  - mcp__plugin_pika_pika__edit_audio_replace
  - mcp__plugin_pika_pika__edit_audio_mix
  - mcp__plugin_pika_pika__add_captions
  - mcp__plugin_pika_pika__create_teleprompter_handoff
  - mcp__plugin_pika_pika__task_status
---

# Content Director — Talking-to-Camera

A talking-to-camera specialist content director. The user gives an IG or TikTok handle; this playbook reverse-engineers their voice, finds TTC trends that pass a hard virality gate, and produces one end-to-end: spoken script in their voice + shot list + final edited mp4 with captions + trending audio mixed under the spoken track.

Sibling routing: `formats/pov.md` (silent / situational), `formats/dance.md` (AI-generated dance from a photo), the Content Director front door (multi-format menu), `formats/duet.md` (stitch / duet reactions).

**Long-running MCP tools:** If any MCP call returns `{task_id, status}` instead of an inline URL/result, immediately call `mcp__plugin_pika_pika__task_status(task_id=<task_id>)` in a tight loop (no Bash, no sleep) until `status` is `completed`, `failed`, or `cancelled`. Continue with the returned `result` only after completion.

## Parameters

- **handle** (required) — IG or TikTok handle, in any of `@name` / `name` / full URL form. Saved as `state.handle`.
- **goal**, **camera_comfort**, **filming_constraints**, **language** — optional bias inputs collected in Stage 0. Saved as `state.brief`.

## Stage 0 — Intake (empty-args menu)

If `$ARGUMENTS` is empty or carries no handle, print this menu verbatim and stop — without a handle the rest of the pipeline can't run:

> **What's your handle?** Drop your Instagram or TikTok in any format:
> - `@yourname`
> - `yourname`
> - `https://instagram.com/yourname` or `https://tiktok.com/@yourname`
>
> Optional context that biases the menu:
> - **What's this content for?** ("grow my brand", "personal account", "promote my SaaS", "just for fun")
> - **Camera comfort?** full face / face partially obscured / voiceover-only
> - **Filming constraints?** ("only at home", "no outdoor", "phone selfie only")
> - **Language / accent?** (English / Hebrew / Spanish / etc., plus any specifics like "casual NYC", "British dry")

Once a handle arrives, save it as `state.handle` and the optional bias as `state.brief`, then continue. Niche and aesthetic are derived from the scrape — don't re-ask.

## Stage 1 — Creator profile (`state.profile`)

The goal: capture the user's *written* voice AND *spoken* voice. TTC lives on spoken delivery, so spoken voice matters more than written; but written is the fallback when no audio exists on the grid.

1. **Scrape** — call `mcp__plugin_pika_pika__scrape_social` on `state.handle` (instagram profile + user-reels + user-posts, or tiktok profile + profile-videos). Prefer `digest: true` with `digest_top_n: 12` for the first profile read so large `user-posts` payloads do not flood the context; fetch raw posts only for the specific clips you need to transcribe or verify. Pull the most recent 12-20 posts only when the compact result is not enough.
2. **Fallback** — if scrape returns empty / rate-limited, run `mcp__plugin_pika_pika__capture_website` on the public profile URL for a grid screenshot, and tell the user the profile is grid-only (spoken voice will be inferred from caption style).
3. **Identity-confirmation gate before profiling** — confirm the scraped account is the intended creator before you transcribe reels or synthesize `state.profile`. Cross-check display name, verified badge, follower count, bio, platform, and whether recent posts match the user's expected creator. Try common handle variants first: with/without dots, dotless, underscores removed, and cross-platform Instagram / TikTok / YouTube checks. Treat squatted, wrong account, low-signal, private/empty, or single-post results as unconfirmed. If the default scrape returns only one stale post but the bio/follower/name signal suggests the account may be real, try `user-reels`/`user-posts` with digest and the common variants before calling the account dead. When unconfirmed, stop and ask **"Is this you?"** with the evidence you saw (`N followers`, verified badge status, display name, bio snippet, platform URL, recent-post summary) and offer the likely variant; do not synthesize the profile before identity is confirmed. When identity is confirmed, set `state.identity_confirmed = true`.
4. **Listen** — after identity is confirmed, if any scraped posts are reels with the creator talking, transcribe one or two via `mcp__plugin_pika_pika__transcribe_audio` to capture cadence, fillers, sign-offs, energy curve.
5. **Synthesize** `state.profile`:
   - **Niche** — primary topic cluster
   - **Voice (written)** — 3 adjectives (dry / earnest / chaotic / aspirational / deadpan / playful / hyped / soft / sarcastic / nerdy)
   - **Voice (spoken)** — separate from written; delivery speed, energy floor and ceiling, fillers, catchphrases, sign-offs. Note explicitly when this is unknown (no talking-head content on grid) so Stage 4 inherits written voice as a placeholder.
   - **Caption style** — short clipped vs long rambly, casing, emoji habits, punctuation. Copy this into on-screen title text so muted viewers feel the same voice as the spoken delivery.
   - **Aesthetic, recurring motifs, what works, filming environment baseline** — see the multi-option script and shot-list contract for what to capture.
6. **Present** the profile to the user in ~6 short lines (with separate "writes like" / "talks like" rows), then continue to Stage 2.

## Stage 2 — Trend research → `state.menu`

The goal: produce a menu of TTC trends that each have **3 reference clips with real view counts above the threshold**. The hardest failure mode this playbook has shipped historically is filling the menu with low-view topical content — guard against that explicitly. See the virality receipts gate.

### What counts as a trend (two-tier gate)

**Tier 1 — Fingerprinted viral trend** — a specific viral instance with all of: a named handle in ≤4 words, a fingerprint (same audio URL OR same verbatim opening sentence across replicators), 3+ reference clips each above the play threshold, 10+ replicators in past 30-60 days, same shot count / beat / duration window. Examples: "He's a 10 but…" card game (verbatim phrase + same structure + millions of plays), "I'm looking for a man in finance" (named audio).

**Tier 2 — Culturally-recognized viral TTC format** — fallback when Tier 1 yields fewer than ~5 cards. Formats that any regular TikTok viewer can name on sight (storytime, GRWM-talk, "things nobody tells you", confessional, "POV: explaining"). Tier 2 cards still need 3 reference clips at the play threshold — the format is evergreen but the example replicators must be at viral scale. Mark these cards `TIER 2 — Viral Format` so the user knows the differentiator is their voice + content angle, not a single audio.

### Play-count threshold (load-bearing)

- **Broad-viral cards:** each reference clip ≥ **500K plays**
- **Niche-fit cards:** each reference clip ≥ **50K plays**

Why: anything below these reads to viewers as "a creator doing a format," not a viral trend. See the virality receipts gate for the source incident — a prior menu padded with 200-15K-play clips broke user trust.

### Hard exclusions

- Topical clusters of low-view clips with no shared opener or structure → that's a vibe cluster, not a trend.
- Format archetypes shipped as trends without a specific viral instance (e.g. "Hot take ___" with no fingerprint) — only allowed as Tier 2 cards, with reference clips that still hit the play threshold.
- A creator's signature format that nobody else copies.
- An aesthetic / genre / hashtag without a shared structural template.

### TTC archetypes (reference, not exhaustive)

Storytime · Hot take / unpopular opinion · POV explaining (spoken, not silent) · Things nobody tells you · Confessional / "I'll be honest" · Reaction / response · Rant · GRWM-monologue · Spoken listicle · Day-in-the-life narration · "What I wish I knew" · "Answering your questions" · Lip-sync-then-talk hybrid. If a candidate doesn't fit one of these and isn't a Tier 1 fingerprinted instance, drop it — it's likely a vibe cluster.

If the trend requires silent acting and narrative-by-caption only → route to `formats/pov.md`. If it's pure lip-sync with no original spoken content → route to the Content Director front door's lip-sync path.

### Research order (don't skip — this order is the gate)

Topical keyword searches return vibe clusters of low-view content. The correct order is named-trend discovery first, virality verification second, TTC filter third.

1. **Discover named trends this week.** WebSearch for "TikTok trends {currentMonth} {currentYear}" and "Instagram Reels trends this week {currentMonth} {currentYear}" — cross-reference 3+ creator-tool blogs (Later, Hootsuite, NewEngen, Manychat, Buffer, OpusClip). Only trends named by 2+ blogs are still warm. In parallel: `mcp__plugin_pika_pika__scrape_social tiktok / trending-feed` with `params.region` set to the user's target posting region when known, or `US` when unknown, and `tiktok / popular-hashtags` to spot sounds with 5+ creators in the top 50. Show the region used on the menu; if the user says another region, re-run the trend scrape for that region before they pick.
2. **Capture the fingerprint** per candidate — exact audio name + artist + sound URL, OR the verbatim opening phrase. If creators paraphrase the opener, it's a format not a trend.
3. **Verify replicators** — for each candidate, scrape 3+ high-view clips via `mcp__plugin_pika_pika__scrape_social tiktok / hashtag` (the trend's specific tag, not generic) or `tiktok / keyword` (using the verbatim phrase). Read each clip's `play_count` field and confirm threshold. Drop candidates that don't have 3 above the line.
4. **Filter for TTC** — the format must involve audible spoken delivery from the creator. Pure lip-sync, pure POV/silent, pure dance → drop.
5. **Score for the user's voice** — last step, ranking only, NOT a filter. The trend's format is vibe-agnostic; the user's voice attaches via the script in Stage 4. See the trend-vs-voice separation rule.

If fewer than 10 trends survive, ship fewer cards. Better 4 strong cards with receipts than 10 padded ones — the user has flagged inflation as a trust break.

### Card format

```
[N] {Named trend or format (≤4 words)}  •  TIER 1 — Fingerprinted Trend  (or TIER 2 — Viral Format)
    Density: {single-selfie / walk-and-talk / +b-roll / multi-loc / lipsync-then-talk}  •  Reference duration: {Xs}
    Fingerprint: {audio name + artist (Tier 1) OR verbatim opener (Tier 1) OR format name + signature opener shape (Tier 2)}
    Template: {one sentence — the SAME structure all replicators follow}
    Requirements before picking: {none OR required disclosure/prop/location/filming constraint, stated plainly}
    Why it fits {handle}: {1 line}
    ▶ Reference clips (3, all hitting the view threshold):
       1. {URL} — {play_count} plays, {creator handle}, {date}
       2. {URL} — {play_count} plays, {creator handle}, {date}
       3. {URL} — {play_count} plays, {creator handle}, {date}
```

Save the full set as `state.menu`. Aim for the mix (when budget allows): 4 niche-fit + 4 broad-viral + 2 wildcards. When budget is thin, ship whatever passes.

## Stage 3 — Present menu, wait for pick

Print the menu cards. End with: **"Which one do we make? (pick a number)"**. Don't write the script or shot list before the pick — saves work if they want something else. Save the choice as `state.pick`.

## Stage 4 — Production package for `state.pick`

Deliver in one message:

### 4a. Spoken script + concept variations

Ship **6-10 spoken-script + concept variations**, not one option. Multi-option is mandatory — the user needs creative agency to pick the angle that hits. See the multi-option script and shot-list contract.

Per variation:
- **Opener is fixed** — the trend's verbatim opener (`storytime: that time I…`, `he's a 10 but…`, etc.) appears word-for-word. Paraphrasing breaks the algorithmic fingerprint and the viewer-recognition signal; the rest of the script is the user's voice.
- **Body** mirrors the user's *spoken* voice from `state.profile` (sentence length, fillers, pet phrases, sign-offs). When spoken voice is unknown (no talking-head content on grid), inherit the *written* voice and flag the variation as a take-1 calibration that may need retuning.
- **Length** fits the reference duration. Count words at ~2.5 spoken words/sec — going over the trend's window (15s / 30s / 45s / 60s) tanks completion rate.
- **Hook caption** (the on-screen title) lands in the first 1-2s, mirroring or paraphrasing the spoken opener so muted viewers recognize the trend instantly.

Variation template:
```
Variation {N} — {one-line concept hook}

Full spoken script (~{duration}s):
[0:00 — opener, dead at lens] {verbatim opener}
[0:03 — pivot] {body in their voice}
[~end — stinger] {payoff line}

On-screen opening title (0:00-2.0s): "{exact title text}"
Stinger title (optional, last 1-2s): "{exact text or 'none'}"
```

Save the chosen full spoken script as `state.script_text`, and save its planned spoken duration from the approved variation/shot list as `state.planned_script_duration_s`. Keep the selected variation metadata in `state.script` only if the agent needs the concept/title fields later.

### 4b. Filming breakdown

Numbered shots, each filmable on the user's phone with no crew. Per shot:

- **Shot #** and **duration**
- **Camera position** — tripod / leaned against book / handheld selfie / propped, plus height (eye level default; just-below-eye for slight up-angle)
- **Where to sit/stand** — orientation to lens
- **Framing** — chest-up selfie / medium close-up is the TTC default; head upper-third, eyes near the rule-of-thirds line
- **Action** — exact delivery direction with timing ("look dead at lens, deliver opener flat 0:00-0:02, raise brow on beat drop 0:03")
- **Energy / pacing** — TTC lives or dies on delivery energy; spell out tempo and emotional arc
- **Props, look direction, lighting, wardrobe** — every prop named and placed
- **Audio capture** — phone mic at 18-24 inches works; AirPods better. Note background noise to avoid.
- **Re-takes** — 2-3 per shot for selects. For long scripts, split at a natural beat and mark with a clap so the editor can stitch invisibly.

The validated default — **phone at eye level, 18-24 inches from face, chest-up framing, window light from camera-side** — is load-bearing for the natural selfie/FaceTime feel TTC depends on.

Be filmable, not vibey. See the multi-option script and shot-list contract for the bar — "phone on tripod at eye level, 22 inches from face, sit on the edge of the bed facing the window so the natural light hits your left cheek" beats "morning storytime energy."

For b-roll inserts in this MCP-only path: use them only when the spoken script is split at natural pauses into separate A-roll segments around the insert, e.g. `a1 -> b1 -> a2`. Do not plan one full-script A-roll plus appended B-roll; that would put the cutaway after the complete speech. Each silent B-roll replaces a pause between A-roll clips, not an overlay under continuous voice.

Do not plan lip-sync-then-talk hybrids in this MCP-only path until an envelope-capable audio workflow is validated. Pick a bed-under TTC trend instead.

### 4c. Caption layout

Two layers of on-screen text:

**Layer 1 — Opening title card** (muted-viewer hook). Top safe zone, `margin_v≈380` for 1080×1920. Text mirrors or paraphrases the spoken opener. In 0:00-2.0s. Style: `reels-clean`, bold white text, 4px black outline, no pill (Instagram-native look — see Load-bearing phrases).

**Layer 2 — Word-sync captions** for the spoken script. Bottom safe zone, `margin_v≈665` from the bottom edge. Auto-generated from `mcp__plugin_pika_pika__transcribe_audio(timestamps=true)` segment timestamps in Stage 6, then split into short phrase rows only when a segment is too dense. 2-4 word chunks when possible, ~1.5-2.5s each, no chunk crossing a sentence break.

Length guard: title cards and caption rows must be short enough to render without clipping. Keep opening titles to 1-2 lines, split any title over ~28 characters per line manually, and prefer two sequential title cards over one long line. Word-sync rows should stay near 2-4 words; if a phrase is long, split it before rendering instead of trusting automatic wrapping.

Pre-deliver the user a preview of how the word-sync captions will look for one or two variations (the punchy hook + the stinger) so they can flag rewording before filming.

### 4d. Trending audio role

The exact sound URL and how it sits in the mix:

- **MCP-supported default: Bed-under only** — trending sound at -12 to -18 dB under the spoken voice for the full clip. The vibe of the sound colors the post; the algorithm matches on audio fingerprint.
- **Unsupported in this MCP-only path until revalidated:** sting-then-duck, end-tag only, and lip-sync-then-talk. `mcp__plugin_pika_pika__edit_audio_mix` supports constant gain/offset tracks, not a timed duck/fade envelope. If a trend depends on those dynamics, pick a different TTC trend or file a follow-up rather than approximating it incorrectly.

Save `state.audio_role="bed_under"` and `state.audio_offset_s` (default `0`, adjust only when the trend's beat/stinger must land later or earlier) — Stage 6 references both.

### 4e. Filming checklist (handed to the user)

- Phone in airplane mode + Do Not Disturb
- Vertical / portrait orientation locked
- 4K 30fps or 1080p 60fps
- Clean lens (front-facing if selfie)
- One light source — window during day, ring/desk lamp at night, aimed at the face from camera-side
- Lock exposure AND focus before filming (tap-and-hold on the face in iOS camera)
- Mic distance — phone 18-24 inches from face; AirPods if available
- Background — nothing identifying you don't want public (mail, screens, kids)
- 2-3 takes per shot
- For multi-chunk scripts, mark chunk breaks with a clap or finger snap

### 4f. Teleprompter handoff (hand the script to the user's phone)

Once the user **approves** the script in Stage 4 — *don't* leave them to copy-paste it into a separate prompter app. Hand them the canonical Pika teleprompter via `formats/teleprompter.md` so they get camera + scrolling read-zone + per-line pacing in one tap.

**Create the handoff** through MCP. Do not build a long URL yourself:

```python
handoff = mcp__plugin_pika_pika__create_teleprompter_handoff(
    script=state.script_text,            # the full approved script with newlines
    handle=state.handle.lstrip("@"),     # e.g. "matancohengrumi"
    trend=state.pick.name,               # e.g. "Wow, ok challenge"
    format="talking",
    aspect_ratio=getattr(state, "recording_aspect_ratio", "9:16"),
    filename=f"{state.handle.lstrip('@')}-talking-take.webm",
    mime_type="video/webm",          # preferred; upload-return accepts browser mp4/webm variants
    max_size_bytes=350_000_000,
    expires_in_s=86400,
)
state.teleprompter_url = handoff["teleprompter_url"]
state.teleprompter_qr_image_url = handoff["qr_image_url"]
state.teleprompter_status_url = handoff["status_url"]
state.teleprompter_aspect_ratio = handoff["aspect_ratio"]
url = state.teleprompter_url
```

**Do NOT pass raw presigned media URLs** into the teleprompter. Use `create_teleprompter_handoff` only: it creates the browser-safe upload-return session behind the token, gives the agent a `status_url`, mints the CDN presign only after the user starts uploading, and avoids TTL failures from recording sessions that take more than a few minutes. The hosted page fetches `script`, `upload_url`, and `aspect_ratio` from MCP, POSTs `{mime_type,size_bytes}` to `upload_url`, receives `direct_upload_url`, `attempt_id`, and `complete_url`, PUTs the Blob to the CDN URL, then completes by POSTing `attempt_id` to `complete_url`. Keep `status_url` in agent state only; do not put it in the browser URL.

**Emit the URL and returned QR image URL** (canonical Pika-MCP handoff — see `formats/teleprompter.md`'s "The handoff" section):

```python
qr_image_url = state.teleprompter_qr_image_url
qr_block = f"![Scan QR]({qr_image_url})"
```

**Caption to surface to the user** (use this verbatim, swap the trend name):

> 📱 **Film it on your phone.** Scan the QR image or open the link below. Your script is already loaded with the read zone at the top right under the camera lens. You get 3-2-1 countdown, per-line pacing, re-shoot, and Upload when you're done.
>
> {qr_block}
>
> 🔗 Or open here: {url}
>
> When the take is ready, hit **Upload**. I'll watch the upload status and start Stage 5 as soon as it lands. If upload fails, use Share/Save and send the MP4 back here.

Do not generate a local QR PNG and do not call a third-party QR service; use the `qr_image_url`
returned by `create_teleprompter_handoff`.

After this — poll `state.teleprompter_status_url` until it returns `status="uploaded"` with `public_url`. Save it as `state.user_take_url`. If there is no B-roll plan, initialize `state.clip_manifest[]` with the uploaded A-roll entry: `{clip_id: "a1", url: public_url, role: "a_roll", planned_duration_s: state.planned_script_duration_s}`. If the shot list includes B-roll, do not treat one full-script upload as the whole edit sequence; collect separate A-roll segment uploads/attachments around each B-roll insert and build the manifest in planned order (`a1`, `b1`, `a2`, ...). If those split segment URLs are not available, omit B-roll from the edit sequence rather than appending it after the complete A-roll.

## Stage 5 — User films, uploads → `state.clip_manifest[]`

When the clips arrive:

1. **Finalize manifest** — confirm every uploaded or manually attached clip has a `state.clip_manifest[]` entry in script order with `{clip_id, url, role: "a_roll"|"b_roll", planned_duration_s}`. The teleprompter A-roll upload is normally `"a1"`; silent B-roll inserts are `"b1"`, `"b2"`, etc. If B-roll is present, the manifest must alternate around split A-roll segments (`a1 -> b1 -> a2`) rather than `full_a1 -> b1`; otherwise ask for split segment uploads or omit B-roll. Do not continue to trimming/captions until each entry has a stable `clip_id`.
2. **Probe** — `mcp__plugin_pika_pika__probe_media` per manifest entry. Confirm portrait orientation, resolution (≥1080×1920 after any server-side normalization), duration, framerate, and audio presence. Treat duration as suspect if it is shorter than the planned script duration by more than ~40%, shorter than the last transcript timestamp, or obviously contradicts the uploaded file metadata; do not cap trims to a suspect `probe_media` duration.
3. **Transcribe** — `mcp__plugin_pika_pika__transcribe_audio` (`timestamps=true`) on each A-roll clip only. Save timestamped transcript segments by `clip_id` as `state.clip_transcripts_by_id[clip_id]` for per-clip trimming and later caption-row assembly; do not store transcripts as an array aligned to `state.clips`, because B-roll clips may have no speech.
4. **Opener verbatim check** — listen to the first 2-3s of each A-roll clip; if the opener was paraphrased, ask for a reshoot of just the opener.
5. **Shot list check** — confirm each scripted shot was captured. If a single clip is unusable (wrong orientation, blown exposure, blurry, silent), reshoot only that shot.
6. **Fetch trending audio** — call `mcp__plugin_pika_pika__scrape_social` on the chosen TikTok/IG reference with `rehost: true`; use the returned durable video URL, then call `mcp__plugin_pika_pika__extract_audio_from_video`. Save the returned audio URL as `state.audio_track`.

## Stage 6 — Edit pipeline → `state.final_url`

Mechanical once `state.clip_manifest[]`, `state.clip_transcripts_by_id`, and `state.audio_track` are in hand.

1. **Trim to speech end per clip** — iterate `state.clip_manifest[]` in script order. For A-roll entries, derive `end_of_speech` from `state.clip_transcripts_by_id[clip_id].segments` as the final transcript segment's `end` timestamp, then call `mcp__plugin_pika_pika__edit_trim(video_url=entry.url, start_s=0, end_s=end_of_speech+0.1)`, using `end_s=end_of_speech+0.5` for the final A-roll entry so the last line has breathing room. Never shorten an A-roll clip just because `probe_media` reported a smaller duration than the transcript/planned speech; re-probe after normalization or trust the transcript-derived speech end instead. For B-roll/silent inserts, call `mcp__plugin_pika_pika__edit_trim(video_url=entry.url, start_s=0, end_s=planned_duration_s)` and do not expect a transcript. Save the returned URL and exact post-trim duration back onto the manifest entry as `{trimmed_url, trimmed_duration_s}`; if the trim response does not include duration, call `mcp__plugin_pika_pika__probe_media` on `trimmed_url` and store the probed duration before continuing. After all entries have `trimmed_duration_s`, set `state.total_trimmed_duration_s` to the sum of those durations in manifest order. If an A-roll transcription cannot find speech, surface that uncertainty and trim from the planned shot duration instead of guessing from silence.
2. **Normalize each clip to portrait** — call `mcp__plugin_pika_pika__edit_reframe` on each manifest entry's `trimmed_url` with `target_aspect="9:16"` and `fill_mode="crop"` for normal talking-head clips; use `fill_mode="pad"` only when preserving the full frame matters more than filling the screen. Save the returned URL as `normalized_url` on the same manifest entry.
3. **Concat in script order when needed** — collect the manifest `normalized_url` values in order. If there is only one `normalized_url`, skip `mcp__plugin_pika_pika__edit_concat` and set `state.concat_url` to that single URL because the concat tool requires at least two inputs. If there are two or more URLs, call `mcp__plugin_pika_pika__edit_concat` with them and save the returned URL as `state.concat_url`. Use clean cuts; no transitions unless the chosen trend explicitly uses them.
4. **Clean the speech track when B-roll is present** — if the manifest contains no `role: "b_roll"` entries, set `state.speech_clean_url=state.concat_url`. If any B-roll is present, do not let its camera audio survive the concat: call `mcp__plugin_pika_pika__extract_audio_from_video` on each A-roll entry's `trimmed_url`, build `state.voice_slots[]` in output timeline order as `{audio_url, start_s, end_s}` where `start_s` is the cumulative `trimmed_duration_s` of every prior manifest entry and `end_s=start_s+trimmed_duration_s`, then call `mcp__plugin_pika_pika__edit_audio_stitch(clips=state.voice_slots, total_duration_s=state.total_trimmed_duration_s, output_format="m4a")` so B-roll gaps become silence. Save the returned URL as `state.voice_track_url`, then call `mcp__plugin_pika_pika__edit_audio_replace(video_url=state.concat_url, audio_url=state.voice_track_url, duration_policy="video")` and save the returned URL as `state.speech_clean_url`. This preserves A-roll speech, mutes B-roll camera audio, and keeps the visual timeline unchanged.
5. **Mix bed-under audio** — require `state.audio_role="bed_under"` from Stage 4d, then call `mcp__plugin_pika_pika__edit_audio_mix(video_url=state.speech_clean_url, audio_url=state.audio_track, audio_gain_db=-15, audio_offset_s=state.audio_offset_s, original_gain_db=0)` and save the returned URL as `state.mixed_url`. Use -15 dB as the default bed level; adjust within -12 to -18 dB only by passing a single concrete number. The user's spoken voice is the deliverable, so the trending audio sits under it — never replace for TTC. If `state.audio_role` is anything else, stop and rescope; do not fake timed duck/fade behavior with a constant-gain mix.
6. **Burn captions with `mcp__plugin_pika_pika__add_captions` after all edit/mix steps are done** — `add_captions` has one global position per call, so treat Stage 4c's two layers as separate caption-layer passes:
   - **Opening title layer**: call `mcp__plugin_pika_pika__add_captions(video_url=state.mixed_url, caption_mode="manual", subtitles=[{start_s:0, end_s:2.0, text:<opening_title>}], style="reels-clean", position="top", margin_v=380, font_color="white", outline_color="black", outline_width=4)`; save the returned URL as `state.latest_captioned_url`. If the title is longer than the length guard, split it manually before this call; do not send a single long title and hope the renderer wraps.
   - **Word-sync layer**: after concat, build `state.caption_rows` as `[{start_s, end_s, text}]` from A-roll entries in `state.clip_manifest[]` by looking up `state.clip_transcripts_by_id[clip_id].segments`; split overly long segment text into short phrase rows only when the timing can stay monotonic. Drop any segment/phrase row whose start timestamp is at or beyond that entry's `trimmed_duration_s`, clamp each remaining row's end timestamp to `trimmed_duration_s`, and then offset rows by the cumulative `trimmed_duration_s` of all preceding clips, including B-roll inserts. Call `mcp__plugin_pika_pika__add_captions(video_url=state.latest_captioned_url, caption_mode="manual", subtitles=state.caption_rows, style="reels-clean", position="bottom", margin_v=665, font_color="white", outline_color="black", outline_width=4)` after the title pass, or the same call with `video_url=state.mixed_url` when there was no title pass. If the transcript rows are not trusted, use `caption_mode="auto"` with `hint_terms[]` for names/brands instead of passing `subtitles`. Save the returned URL as `state.latest_captioned_url`.
   - If the chosen concept has no opening title, skip the title pass and run only the word-sync pass from `state.mixed_url`. Do not run any trim/reframe/concat/mix step after captions; if timing changes, rebuild the caption rows and re-run the caption phase.
7. **Final output** — read `state.latest_captioned_url` from the last caption pass and save it as `state.final_url`. Keep version metadata in agent state (`{user_slug}_{trend_slug}_v{N}`) so a later render never overwrites the previous deliverable.

### Pre-delivery gates

- **Opener-verbatim** — the first 2-3s of the final cut delivers the trend's opener word-for-word. Paraphrasing breaks the trend fingerprint.
- **Caption legibility + sync** — every chunk readable on first pass at phone screen size, lands on the right spoken words within ±100ms. If chunks lag or lead, re-derive timings from the transcript and re-render.
- **Title/caption bounds** — no title or caption row is clipped by the left/right edge, and no caption covers the mouth/chin. If a row overflows or blocks the face, split the text, reduce font size within 50-72, or move the safe-zone margin and re-render.
- **Ending breath** — final spoken line is not cut on the last phoneme; the final A-roll keeps ~0.5s after speech unless the trend explicitly requires a hard smash cut.
- **Audio balance** — spoken voice intelligible above the bed. Lower bed by 3-6 dB if it clips the voice; normalize down if voice peaks > -3 dB.
- **Audio-sync** — trending audio's beat drop lands on the script's pivot moment, stinger lands on the closing line. Retime the audio offset if misaligned.
- **Pixel orientation** — verify with `mcp__plugin_pika_pika__probe_media` after reframe; if the result is not portrait, run `mcp__plugin_pika_pika__edit_reframe` again with `fill_mode="pad"` or ask for a corrected upload.
- **Phone-cameo** — if any clip shows a phone on screen, it must be a current-gen iPhone (15 Pro / 16 / Air). See the phone-cameo gate.

## Stage 7 — Loop

After delivering `state.final_url`, ask: **"Want to do the next one? (pick another number from the menu, or 'new trends' to re-research)"**. If they pick another, return to Stage 4 with that trend — the Stage 3 menu stays warm for the session.

## Load-bearing phrases

Each phrase below is verbatim-anchored — agents simplifying the skill should not edit these without re-validating, because empirical behavior depends on them. Source incidents linked.

### Caption render (validated `pika-trendy-reel` pattern)

- Use `mcp__plugin_pika_pika__add_captions` with `style="reels-clean"` for bold white text, no pill, black outline.
- Use one pass per caption position layer. TTC normally needs two layers: top opening title first, then bottom word-sync captions. If only bottom captions are needed, use one pass.
- Captions are the final media operation. Do not run trim/reframe/concat/mix after the caption phase, because that can drift manual timings.
- `outline_width=4` — the 4px black stroke is the Instagram-native look.
- `font_size≈57` (scale 50-72 per readability).
- Top opening title: `position="top"`, `margin_v≈380` (inside top safe zone).
- Bottom word-sync: `position="bottom"`, `margin_v≈665` (visually near y≈1255 on a 1080×1920 render).
- IG Reels safe zone (1080×1920): captions sit inside y≈270 to y≈1475, ~80px margin from left/right edges.
- Emoji warning: platform emoji glyphs can vary in burned captions. Drop decorative emoji from burned text and tell the user to put emoji in the post description at upload.

### Trim measurement

Use segment timestamps from `mcp__plugin_pika_pika__transcribe_audio(timestamps=true)`: set `end_of_speech` to the final transcript segment's `end` timestamp and trim to `(end_of_speech + 100ms)` for internal cuts, with `(end_of_speech + 500ms)` on the final A-roll tail. Eyeballed trims have shipped 1.5s of dead air per clip in production, while bad duration probes can cut off the ending — measure from transcript timestamps, don't guess, and don't cap to a suspect `probe_media` duration. This is slightly less exact than acoustic silence detection, but keeps the workflow MCP-only.

### Filming defaults

Phone at eye level, 18-24 inches from face, chest-up framing, window light from camera-side. Validated for the natural selfie/FaceTime feel TTC depends on.

### Audio mix levels

Bed-under only in this MCP path: trending audio at about -15 dB, voice at 0 dB, optional `audio_offset_s` for beat alignment. Sting-then-duck, end-tag fades, and lip-sync-then-talk need a validated envelope/segmented audio workflow before returning here.

### Play-count thresholds

≥500K plays (broad-viral) or ≥50K plays (niche-fit) per reference clip. Anything below reads as a creator doing a format, not a viral trend.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `mcp__plugin_pika_pika__scrape_social` returns empty / rate-limited | Profile blocked, region-locked, or quota exhausted | Fall back to `mcp__plugin_pika_pika__capture_website` on the public URL for grid screenshot. Tell the user the spoken voice will be inferred from caption style. |
| Whisper `mcp__plugin_pika_pika__transcribe_audio` returns 0 segments | Short clip with no detected speech, or audio track is silent / corrupted | Re-run with `provider="gemini"` via `mcp__plugin_pika_pika__analyze_media` to double-check. If both fail, ask the user to confirm the clip has audible audio. |
| Whisper mis-transcribes a phrase ("haters will say" → "hey don't") | Short clip + Israeli accent + brand-name words. Whisper degrades on <3s clips. | Use the scripted line verbatim for the caption. Don't re-transcribe — the user knows what they said. |
| User delivers a paraphrased opener | Forgot the exact wording mid-take | Reshoot only the opening 2-3s and splice in. Don't re-shoot the whole sequence. |
| iPhone clip metadata shows `1920x1080` (landscape) | iPhone stores a rotation flag separately from the pixel frame | Trust `mcp__plugin_pika_pika__probe_media` after `mcp__plugin_pika_pika__edit_reframe`, not the pre-upload filename or camera metadata. |
| Tail silence between cards in concat output | Trims eyeballed instead of measured | Re-run timestamped transcription per clip and trim to `(final transcript segment end + 100ms)`. See Load-bearing phrases. |
| Caption text overlaps the speaker's face | Top zone caption placed too low, or word-sync caption escaped the safe zone | Top title ≈380px from the top; bottom captions visually near y≈1255 for 1080×1920. Re-run `mcp__plugin_pika_pika__add_captions` with corrected `position`/`margin_v`. |
| `mcp__plugin_pika_pika__probe_media` reports a much shorter duration than the uploaded clip | Fragmented/rotated/browser-recorded MP4 metadata confused the probe | Mark the probe duration suspect, do not truncate to it, and use transcript/planned duration evidence before trimming. |
| Title card or caption runs past the frame edge | Long text sent as one caption row | Manually split the title/caption into shorter rows or sequential cards before re-running `mcp__plugin_pika_pika__add_captions`. |
| Final word cuts off abruptly | Final trim used only the speech endpoint | Re-trim the final A-roll to `final transcript segment end + 500ms` and re-run captions as the final phase. |
| Concat output has an audio glitch at a cut | Source clips have incompatible timestamps or audio layouts | Re-run `mcp__plugin_pika_pika__edit_reframe` on the affected input, then call `mcp__plugin_pika_pika__edit_concat` again so the worker normalizes the source. |
| Caption tool mis-spells a brand or slang phrase | Auto transcription drift on short TTC clips | Use `caption_mode="manual"` with transcript rows from the approved script, or pass `hint_terms[]` before re-running captions. |
| Stage 3 menu has < 10 cards | Fewer than 10 trends pass the strict virality gate this week | Ship what passed (could be 3, 5, 7). Tell the user "only N trends qualified this week" and list the formats that were popular but lacked fingerprinting. Never inflate — see the virality receipts gate. |
| Final video exceeds the trend's duration window | User's natural delivery is longer than the trend's reference clips | Trim filler / breath / dead air in the edit. If still over, trim the script before re-filming. Going over kills completion rate. |

## What NOT to do

- **Don't ship format archetypes as trends without reference receipts.** "Hot take ___" / "Storytime: that time I…" / "Things nobody tells you about ___" are evergreen FORMATS. They only earn a card slot when accompanied by 3 reference clips at the play threshold (Tier 2). Without receipts, the menu becomes a vibe cluster — the user has flagged this as the failure mode.
- **Don't pad reference URLs with creator-tool blog citations alone.** Blog citations help discover trend names. They do not stand in for the 3 viral reference URLs.
- **Don't keyword-search topical content as the primary research method.** "storytime AI artist" returns vibe clusters of low-view content. Order: blog recaps → named-audio discovery → trending-feed scan → verify each candidate has 3 high-view replicators.
- **Don't deliver 10 cards when fewer pass the gate.** Ship 3, 5, or 7 if that's what survives. Inflating burns user trust.
- **Don't paraphrase the trend's fixed opener.** The verbatim opener is the algorithmic fingerprint and the viewer-recognition signal. Paraphrasing breaks both.
- **Don't strip the user's voice from the body of the script.** Match the trend's opener and structure; write the post-opener body in the user's actual spoken voice.
- **Don't film for the user.** This playbook writes the plan and runs the edit; the user films their own talking-head footage. No AI-generated TTC footage — the authenticity of the actual delivery is the format's value.
- **Don't write vibey shot lists.** Every shot needs explicit camera position, distance, framing, energy direction, look direction.
- **Don't burn captions outside the IG Reels safe zone.** Inside `y=270 to y=1475` for 1080×1920, ~80px left/right margin. See the caption safe-zone guidance.
- **Don't chain arbitrary text overlays for captions or edit after captions.** Use `mcp__plugin_pika_pika__add_captions` with `reels-clean`, `outline_width=4`, and safe-zone placement; when TTC needs both a top title and bottom word-sync, run one caption pass per layer and keep captions as the final phase.
- **Don't put word-sync captions over the user's face.** Bottom safe zone (y=1255). Top is reserved for the opening title-card hook.
- **Don't replace the user's spoken audio with the trending sound.** Mix under with bed-under only in this MCP path. Do not choose sting-then-duck, end-tag fades, or lip-sync-then-talk until a validated envelope/segmented audio workflow exists.
- **Don't exceed the trend's duration window.** 15s / 30s / 45s / 60s. Over kills completion rate; cut tighter or trim the script.
- **Don't propose 10 of the same archetype.** Mix storytime / hot-take / POV-explaining / things-nobody-tells-you / rant / GRWM-monologue across the menu.
- **Don't show old phones.** If a clip shows a phone, it must be a current-gen iPhone (15 Pro / 16 / Air). See the phone-cameo gate.
- **Don't skip the Stage 3 menu and jump to production.** Always present cards, always wait for a pick. Producing without selection burns tokens and budget on a video the user may not want.
