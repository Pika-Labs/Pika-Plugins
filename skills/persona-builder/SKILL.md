---
name: persona-builder
description: >
  Whip a person into a more marketable shape online. Read their socials and the way they
  talk, then deliver real talk about where the money is, what's holding them back, and what
  to fix — then ship the designed multi-page Influencer Persona PDF + a persona.md folder kit
  that downstream skills (ugc-ads, podcast, founder-product-video, app-sizzle, app-store-screens)
  can consume. Input is the person themselves: socials, camera roll, taste URLs, a selfie
  video, or start-from-scratch answers. Visual/PDF stages still require real curated imagery:
  user-provided photos, or clean public-feed frames from a supported social handle. Output is a
  self-contained kit + a roadmap to actually become that persona online.
  Trigger phrases: "build my influencer identity", "make me a creator brand", "personal brand for
  [niche]", "build my online persona", "influencer persona.md", "I want to be an influencer",
  "make my creator identity", "persona.md for my socials", "creator identity for @[handle]",
  "persona-builder", "glow up my online presence".
argument-hint: "[social handles, camera roll, taste URLs, or 'start from scratch']"
required-capabilities:
  - mcp__plugin_pika_pika__identity_balance
  - mcp__plugin_pika_pika__scrape_social
  - mcp__plugin_pika_pika__transcribe_audio
  - mcp__plugin_pika_pika__generate_image
  - mcp__plugin_pika_pika__html_to_png
  - mcp__plugin_pika_pika__html_to_pdf
  - mcp__plugin_pika_pika__upload_asset
  - mcp__plugin_pika_pika__extract_frame
  - mcp__plugin_pika_pika__analyze_media
  - mcp__plugin_pika_pika__task_status
---

# Influencer Identity

Take a person — their socials, their camera roll, the way they talk, who they want to be online — and run them through a glow-up with real talk. The output is a `persona.md` + portable folder kit + a roadmap to close the gap between where they are now and the persona they want to project.

Sister skill to `build-a-brand`: same uncompromising standards on voice, aesthetic, and specificity — but the brand is a **human**, not a product. The output is consumed by other Pika skills (ugc-ads, podcast, founder-product-video, app-sizzle, app-store-screens) so the influencer can produce on-brand content anywhere.

## Cost transparency gate

Before any paid MCP call, call `mcp__plugin_pika_pika__identity_balance({verbose: true})` once. Surface the current balance, recent burn rate, and remaining runway, then gate the run with this exact message:

> Estimated cost: about 600-1,200 credits (~$6-$12) for scrape/transcription if needed, GPT-image-2 mood-board and voice-page atmosphere tiles, MCP HTML image renders, JPG conversion, final html_to_pdf render, and post-render analyze_media PDF QA. This exceeds $5, so Reply `proceed` to continue or `cancel` to stop.

Do not call any paid MCP tool until the user replies `proceed`. If the user replies `cancel`, stop without generating. This is the only yes/no gate; after `proceed`, run the workflow until the next explicit user approval gate for identity/mood-board/PDF content.

## Tone of the conversation

This is **not a packaging exercise**. The user came here to look more marketable. That means: be honest, be strategic, be specific. The skill should feel like a friend who books brand deals telling them what to actually fix — not a horoscope and not a Canva mood board factory.

- **Lead with what the inputs prove**, not what the user wished they'd hear. If their photos are crappy, say so and tell them how to fix it.
- **Initiate the strategic conversation**, don't wait to be asked. The user doesn't always know what's lucrative or what content mix gets paid — bring receipts.
- **Name the gap explicitly**: "to look like @[reference], you'd need to add X / drop Y / shoot in Z light." Don't soft-pedal.
- **No empty validation**. If the user's bio is generic, the answer isn't "love it!", it's a rewrite.

## Full Workflow

### Stage 0 — Intake (empty-args menu)

If invoked with no input (no handle, no URLs, no photos, and no relevant prior context), print this menu verbatim as your full response and stop. Do not call any tool. Wait for the user's next message.

> **Glow-up time.** This is going to whip you into a more marketable shape online — honest read on what's working, what's not, where the money actually is for someone with your inputs, and what to fix to get there. You'll leave with a designed Influencer Persona doc + a roadmap to actually become that persona.
>
> Light-touch from you — drop files or paste links:
>
> - **IG / TikTok / YouTube handle** — I'll pull your bio, recent posts, and captions. This is the strongest signal and the most important input.
> - **16+ individual full-res photos that feel like "you"** — drag-drop the actual files. If you gave active socials, scraped post imagery can cover some of this; if you have no socials, the full PDF needs enough real photos for the mood board and the voice-mode pages.
> - **Any URLs that show your taste** — Pinterest, Spotify, Depop, Letterboxd, etc. Drop as many or as few as you want.
> - **Describe yourself + how you want to come off on social** — a few sentences in your own words. What you're actually like, and what you want people to see when they land on your profile.
> - **No socials yet?** Say "start from scratch" and I'll ask you everything. Before the mood board / PDF stages, I'll still ask for 16+ real photos so the visuals are grounded in you.
>
> Handles + a few photos is the strongest combo. Skip what doesn't apply. **Nothing here requires screenshotting apps, drafting long paragraphs, or recording video.**

If the user already dropped one of the above, skip the menu and proceed straight to Step 1.

### Step 1 — Read the input

Before supported social scrape/transcription or any other paid MCP call in this step, ensure the Cost transparency gate above has been completed. Run that gate only if it has not already run in this invocation; do not call `mcp__plugin_pika_pika__identity_balance` again, and do not ask for a second `proceed` after the user has already approved the upfront cost gate.

Open with a brief agenda so the user knows what's coming. Set the tone — this is a glow-up, not a packaging job:

```
quick framing: this isn't a packaging exercise. i'm going to be honest with you about what's working in your current presence, what isn't, where the lucrative paths are for someone with your inputs, and exactly what to fix to get there. by the end you'll have a designed influencer persona doc + a real roadmap.

here's how this works — 5 steps:
1. **Read the input** — i scrape your socials (if you gave handles), look at your photos, ask you a few questions, play back what i'm hearing
2. **Strategic direction + lock the identity** — the real-talk step. i lay out the lucrative paths your inputs actually support (with stats), name the gaps between your current feed and where you want to go, critique your current photography honestly (lighting, framing, gear) and tell you what to buy. then we lock the persona. you approve before we move on.
3. **Mood board** — i curate from your photos (color-graded if your influencer aesthetic differs from your existing grid), then GPT fills aesthetic gaps. you approve.
4. **Influencer Persona PDF** — i draft your voice bank (bios, caption modes with visual examples, hook openers, DM voice, do/don't) and lay it into a multi-page branded PDF alongside your persona overview, content categories, mood board, and a Key Next Steps roadmap. you approve it from the PDF preview.
5. **Package the kit** — persona.md + folder kit (mood board, voice bank, PDF) saved to ./tmp/. only after you say "ship it".

let's start. [questions follow]
```

**Read inputs first:**
- If any supported social handles or supported social URLs were dropped → call `mcp__plugin_pika_pika__scrape_social` on those supported socials IN PARALLEL before asking the canonical questions, so data is back by the time the user answers. Use `rehost: true` for Instagram/TikTok feed and video actions so downstream curated tiles have durable `pika_cdn_url` / CDN media instead of ephemeral signed media. Do not send unsupported taste URLs (Spotify, Depop, Letterboxd, personal sites, mood-board links, etc.) to `mcp__plugin_pika_pika__scrape_social`; keep them as taste signals and ask what to borrow from them if the intent is not obvious. Standard call pattern per supported platform:
  - **instagram**: `instagram.profile` + `instagram.user-posts` (limit 30, `rehost: true`) + `instagram.user-reels` (limit 30, `rehost: true`)
  - **tiktok**: `tiktok.profile` + `tiktok.profile-videos` (limit 30, `rehost: true`)
  - **youtube**: `youtube.channel` + `youtube.channel-videos` (limit 30)
  - **twitter**: `twitter.profile` + `twitter.user-tweets` (limit 30)
  - **pinterest**: `pinterest.profile` (limit 50)
  Pull recent posts, captions, bios, visual style. Note dominant subjects, lighting, voice patterns, caption length, hook style. Captions, bios, metrics, and visual-style summaries are **text/strategy signal** that informs Step 2; they are not dropped raw into visual artifacts. Clean public-feed media from the `rehost: true` scrape can become curated image source material in Step 3 / Step 4 after the source-priority and no-text gates below. **Scraped captions are the PRIMARY voice signal for the voice bank in Step 4 — direct user captions beat any inference from chat answers.** Chat-voice + intake answers are the fallback only when scrape fails (private account, no posts yet, brand-new handle).
- If camera roll / photos → look at them. Note settings, lighting, what's in frame, what's NOT (no people? all flatlay? always outdoors?).
- If selfie video → transcribe via `mcp__plugin_pika_pika__transcribe_audio`, note vocabulary, energy, pacing, fillers, what they're enthusiastic about.

**Then ask these 4 FIXED canonical questions in a single message.** Same every time — do NOT improvise or substitute. Consistency matters; if the user restarts and gets different questions, they lose trust in the process.

1. **Describe yourself + how you want to come off on social** — a few sentences in your own words. What you're actually like, and what you want people to see when they land on your profile. *(This question covers the real-self / projection / authenticity dial all at once.)*
   - **Plus: name 1–3 creators or characters you want to feel like.** For each, tell me which dimension you want to borrow — their **voice**, their **content type**, or their **visual aesthetic**. You don't have to like all three things about them; specify what's in and what's out. ("I want her voice but not her content" is a totally normal answer.)
2. **Where do you live + what's your day-to-day pace?** *(Location + speed signal — affects the authenticity register and the kinds of settings the mood board renders.)*
3. **Ideal friday night?** *(Single vibe question — surfaces personality quickly. "TV and bed early" vs "out till 2am" reads instantly.)*
4. **What are you hoping to get out of this?** *(The WHY — followers, a business, dating, community, just expression, something else. This drives every strategic choice downstream.)*

That's it. 4 questions. No variations. No "pick 3 of these and skip the rest." If the user already answered some of these in their initial drop (e.g. their description-of-self answer in the intake menu covers Q1), acknowledge what you have and only ask the unanswered ones.

If the user explicitly says "start from scratch," ask these 4 questions even without socials. If the user dropped zero photos AND zero URLs AND zero description without saying start-from-scratch, fall back to asking the menu's intake items first before these 4 questions — you need at least SOMETHING to read. No-social users are supported; no-photo visual/PDF output is not. If a start-from-scratch user answers the questions but still provides no real photos, complete the strategic text work and pause before Step 3 to request 16+ individual photos: 6 mood-board curated tiles plus 10 separate PDF voice-page curated tiles.

Keep it to one message. Wait for answers.

**After answers**, play back what you heard. Lead with the surprising or specific things, not summary boilerplate:
- **The person**: 2–3 sentence read on who they actually are
- **The voice signal**: how they talk in the inputs you read (specific phrases, energy, what they avoid)
- **The visual world**: what their feed, camera-roll photos, taste URLs, and/or reference creators suggest, AND what they're reaching for if different (this is the seed for the Step 2 visual aesthetic spec)
- **The authenticity dial**: real / amplified / different — and along which axis
- **References anchoring the work**: each creator they named + which dimension to borrow (voice / content type / visual aesthetic)

End with: "anything to add, change, or call out before I lock the identity?" Wait for response.

### Step 2 — Strategic Direction & Identity Lock (HARD GATE — approval required)

This step has four parts. The first three are **the glow-up real-talk** — the work the user came here for. The fourth is the identity lock that ends the gate. Skipping 2a–2c and going straight to identity.md is a fail state; the user explicitly wants strategic guidance, gap analysis, and critique, not just a packaging summary.

**Tone for this step:** specific, honest, and useful. Cite the inputs you read in Step 1 by name ("your trench-coat post from Nov 8" beats "your outfit content"). Bring numbers wherever you can. Don't soft-pedal — if their bio is generic, say so. If their lighting is bad, say so. The user is paying you to tell them what their friend who books brand deals would tell them.

#### 2a — Strategic direction (lucrative paths + content implications)

**Initiate the strategic conversation; don't wait to be asked.** Before locking the persona, lay out the 2–3 most lucrative directions their inputs actually support, with rough industry stats and the concrete content implications for each. The user often doesn't know what gets paid, what CPMs look like in different niches, or what posting load each path requires. Bring receipts.

For each direction:
- **Niche label** (specific, not "lifestyle" — "Boston-local lifestyle creator", "Texas barre-class founder content", "millennial dad humor for finance")
- **Why this direction fits the inputs** — point to the specific posts / photos / things they said that support it
- **Rough monetization profile** — typical CPM range, common brand-deal floor at different follower tiers (e.g. "fashion micro: $100–250/post at 5K; lifestyle micro: $150–300/post; finance: $400–800/post"), affiliate/LTK reasonableness, sponsored-post realism. Every numeric monetization claim must either cite a source verified during this run or be explicitly labeled **broad heuristic estimate**; never present unsourced CPMs, follower thresholds, or brand-deal floors as precise facts.
- **Content load this path requires** — posting cadence (e.g. "4–5 outfits/week + 1 location reel"), production tier expected (phone-shot OK vs. mirrorless needed), recurring formats audiences expect in this niche (e.g. "OOTD posts + 'GRWM for X' reels + monthly local-roundup carousel")
- **Who's already winning here at your size** — name 2–3 creators at 5K–30K who run this exact play, with one sentence each on what makes them work. Only name real creators, handles, follower tiers, or current metrics if verified during this run via `mcp__plugin_pika_pika__scrape_social` or another live supported source. If you cannot verify, use clearly labeled archetypes instead (e.g. "local style micro-creator archetype") and omit handles/counts.

End the section with a direct question: **"which of these directions are you most drawn to — or do you want to combine?"** Don't let the user pick "lifestyle" generically; force the choice to be specific.

If the user already named a direction in Step 1 ("I want to be a fashion creator"), still run this section to either validate or widen the lens — they often haven't considered the adjacent path that pays better with their existing inputs.

#### 2b — Gap analysis (current profile → target persona)

Once the direction is named (or if the user already locked it in Step 1), explicitly compare **what they're currently posting** vs. **what the target persona requires**. This is the section that tells them what's missing.

For each gap, name:
- **The missing content category** — "you have OOTD nailed but zero hosting / kitchen content; the persona you named needs that bucket"
- **The format gap** — "you have static posts but no reels; the niche pays reels at 3–5× the CPM of static"
- **The cadence gap** — "you're posting ~1×/week; this niche expects 4–5×/week to stay in the algorithm"
- **The voice gap** — if their actual captions don't match the voice they say they want, name the specific phrase patterns they need to drop and the ones they need to add
- **The aesthetic gap** — if their current visual register diverges from where they want to land (e.g. flat phone-flash shots vs. cinematic golden-hour register), say so explicitly
- **The follower-tier gap** — name where they are now (e.g. 2K), what tier the paid work starts (typically 5K+ for local brand deals, 10K+ for national), and what realistic 90-day growth looks like for someone executing the plan

Frame each gap as a **shippable action**, not a critique. "You need 1 reel/week tied to a Boston seasonal moment" lands better than "you don't post enough reels."

#### 2c — Content critique (production quality + gear)

**Be helpfully critical.** If the user's current photos are crappy, say so — and tell them how to fix it. The default failure mode is to be too polite here; correct that.

Review their existing photo / video content for:
- **Lighting** — name specific photos that are working ("the kitchen shot at 4pm — that's the window light to chase") and specific ones that aren't ("the trench post is shot into overhead-noon light, which is why your face is hard-shadowed; reshoot at 3–6pm window light")
- **Framing & composition** — phone held too low or too high, subject too centered, headroom issues, busy backgrounds, where to actually stand
- **Color & post-processing** — are they using a preset / preset pack? do their colors match the locked visual aesthetic? if not, name specific tools
- **Consistency** — does the grid feel like one person's eye? where does it break?
- **Selfie technique specifically** — phone position, mirror cleanliness, what to wear vs. avoid for OOTD selfies, how to hide face if face-shy

**Then suggest concrete gear/tools to purchase**, scaled to the user's likely budget. Don't recommend a $1500 mirrorless to someone who has 500 followers — start with what gets them 80% of the lift for under $200:
- **Starter tier (under $100)**: phone tripod (~$15), clip-on reflector or A4 white foam board (~$25), one Lightroom mobile preset pack matched to their aesthetic (~$15–40), basic ring light or LED panel if their home is dim (~$30)
- **Intermediate tier ($100–500)**: small softbox kit, gorillapod for outdoor reels, wide-angle phone clip-lens for mirror selfies in small spaces, a dedicated mic for reel voiceovers (~$80)
- **Advanced tier ($500+)**: only recommend if the user is already at 10K+ and asks — entry-level mirrorless (Sony a6400 / Fujifilm X-S20) + a 35mm-equivalent prime, color-graded preset subscription, an editor

Name brands and price points so the user can actually shop. "Buy a clip-on reflector" alone is too vague; "Lume Cube panel mini or the Pictar reflector clip, both around $25 on Amazon" gives them something to click.

#### 2d — Lock the identity.md

NOW (after 2a–2c have been delivered and the user has weighed in), draft the persona summary. This is the user's first proper artifact — it has to feel like someone gets them and like the strategic real-talk above shaped where it landed, not like generic brand copy.

**`identity.md` structure (deliver inline in the chat as a markdown block, save to disk later):**

```markdown
# [@handle or first name] — Identity

## The real you
[2–3 paragraphs in plain language. Specific. References their actual stuff — the comfort show they named, the way they describe their friends, the thing they said about their high school self. Sounds like someone who paid attention, not a horoscope.]

## Your influencer identity
[2–3 paragraphs about the online projection. Calls out the authenticity dial explicitly:
"You're not pretending to be someone else — you're you with the volume on [dimension] turned up."
OR
"This is a character. Here's where the character starts and the real you ends."
Be specific about what's amplified, what's filtered, and why.]

## Visual aesthetic
**This is the spec Step 3's mood board has to render. Be detailed enough that someone else could build the board from this section without seeing the user.**

- **Palette:** [specific colors / named tones — "warm cream, cognac brown, dusty rose, deep navy" beats "neutrals"]
- **Lighting:** [warm window / overcast / golden hour / harsh flash / candlelight — which lighting dominates]
- **Settings:** [where shots take place — specific. "Brooklyn brownstones, marble-top coffee shops, kitchen counter at 10pm" beats "city lifestyle"]
- **Photography style:** [phone-camera POV, mirror selfies (faceless or face), 3/4 candids, overhead flatlay, etc. — which framings dominate]
- **Subjects in frame:** [hands holding things, full body, faces, food, books, the dog, the bar, etc.]
- **Forbidden visual elements:** [what would never appear — e.g. "no full-glam beauty shots", "no landscape paintings", "no studio-clean white backgrounds"]
- **Relationship to existing grid:** [if their existing photos already match this aesthetic, say so. If the aesthetic is a slight evolution from their grid, name exactly what shifts — e.g. "their grid is currently warm and slightly washed; the influencer aesthetic pushes deeper shadows + cooler highlights for a more cinematic read." Step 3 uses this to decide whether to apply light color-grading to her photos for cohesion.]

## Voice principles
**Sounds like:** [3 example sentences in their voice — short, specific, real]
**Never sounds like:** [3 example sentences they would never write — the cringe versions]
**Voice adjectives (3):** [adj], [adj], [adj]
**Forbidden words/phrases:** [3–6 actual phrases they'd want to avoid]

## Reference creators (with dimension + what to borrow)
- **[@handle or name]** — borrow their **[voice / content type / visual aesthetic]**. Specifically: [the actual thing — pacing, lighting, type of self-disclosure, etc.]
- ...
```

**Anti-generic check before delivering:**
- Could this identity be re-pasted onto a different person without changing anything? If yes, push for specificity.
- Does the **Visual aesthetic** section name specific colors, lighting, and settings — or is it adjective soup? Step 3 has to render this; "warm and minimal" is not enough.
- Does each **Reference creator** entry specify the dimension (voice / content type / visual aesthetic) AND the specific thing to borrow? Vague references like "feel like @emmachamberlain" without naming WHAT are a failure state.

**Deliver the identity in chat, then explicitly ask:** "does this feel like you? anything to push harder, soften, or rewrite before I move to the mood board?"

🛑 **Wait for explicit approval.** "yes" / "this is me" / "ship it" / "perfect, do the board". Not "ok", not silence, not "make it more X" (that's feedback — incorporate and re-ask). Approval gates are hard stops.

### Step 3 — Mood Board (HARD GATE — approval required)

Build the mood board AFTER identity is locked. **The board is built to match the `Visual aesthetic` section in the approved Step 2 identity.md — not to discover the aesthetic.** Re-read that section before sourcing or generating any tile. Every tile (curated + generated) must serve that locked spec.

**Source priority — mix is required, fully-generated is a fail state:**
1. **Individual full-resolution photos from the user** (their camera roll, photos they love, full-res files) — the strongest curated source. These go in `mood-board/curated/`.
1a. **Handle-only public-feed fallback for video-heavy / mostly Reels accounts.** If the user gave a public handle but no separate photo files, scraped feed imagery can provide curated tiles. For image posts, use the highest-quality `image_versions2.candidates[0].url`. For video posts where `media_url` is a `.mp4`, do not use the ephemeral IG `visual_media_url` / signed cover JPG as the curated tile source; do not alter any signed-cover query param because that causes `URL signature mismatch`, and mid-clip covers often include baked-in caption or title overlays. Use only the durable rehosted `.mp4` returned by the Step 1 `rehost: true` scrape (the `pika_cdn_url` / `cdn.pika.art` media; treat it as `is_durable: true`) and call `mcp__plugin_pika_pika__extract_frame(video_url: <durable_rehosted_mp4>, time_s: 0)`. Treat each extracted frame as a candidate tile, not an approved tile: immediately call `mcp__plugin_pika_pika__analyze_media` on the frame URL with an OCR / visible text / no-text prompt before placement. This sourcing-time check must happen before the frame becomes a mood-board tile, PDF content-category tile, or voice-page curated tile. If frame 0 contains text, a title card, or a burned-in caption, drop the reel or try a later keyframe (for example `time_s: 1.5` or `time_s: 3`) and run the same `mcp__plugin_pika_pika__analyze_media` no-text check before using that later keyframe. If no durable rehosted `.mp4` is present, retry the scrape with `rehost: true`; do not fall back to a signed cover URL. Final PDF QA is only a backstop after this sourcing gate, never the first text-detection step.
2. **NEVER crop from an IG grid screenshot.** Tile widths in grid screenshots aren't pixel-aligned to clean fractions; auto-crop bleeds; result is bad. Confirmed-fail approach. If a user offers a grid screenshot, **ask them for individual photos instead**.
3. **A mood board with zero curated tiles has failed.** If neither user photos nor clean public-feed curated frames are available, unblock that first — never substitute generated stand-ins. If the user intended to provide photos and they didn't reach disk, ask them to re-upload. For start-from-scratch / no-social users, pause here and request 16+ individual photos before building visual artifacts: 6 mood-board curated tiles plus 10 separate PDF voice-page curated tiles.
4. **Read the `Relationship to existing grid` field from Step 2.** If the locked aesthetic is identical to the user's existing grid, place curated tiles as-is. If Step 2 names a slight evolution (e.g. "their grid is warm + washed, the influencer aesthetic pushes deeper shadows + cooler highlights"), apply **light CSS color treatment** in the HTML composite before rendering — `filter: contrast(...) saturate(...) brightness(...)`, a subtle overlay, or a mild blend-mode treatment. **Never re-pass the user's photos through gpt-image-2** — image-model re-rendering drifts face/pet/object identity and breaks the "this is actually her" anchor. If the divergence is too large for CSS treatment alone, the answer is more generated atmosphere tiles in the new aesthetic + fewer untreated curated tiles, NOT regenerating her photos.
5. **Identify aesthetic coverage gaps** — what part of the locked Step 2 aesthetic isn't represented yet (a specific setting, framing, lighting condition)?
6. **Fill gaps with `mcp__plugin_pika_pika__generate_image` (provider="gpt-image-2")** for **social-content atmosphere only** *(load-bearing phrase — pushes gpt-image-2 away from vision-board / wallpaper energy; see Load-bearing phrases section)*, prompted in the Step 2 aesthetic (its palette, lighting, settings, photography style). See the hard rules below. Generated tiles go in `mood-board/generated/`.

🛑 **HARD RULE: Generated tiles render SOCIAL CONTENT energy, not atmospheric vision-board energy.**

A mood board for an influencer identity has to look like **a creator's actual feed**, not a vision board.

- **YES**: phone-camera framing, candid 3/4 angles, mirror selfies (faceless if generated), in-hand POV shots (coffee on a table, book in lap, drink at a bar), tablescape overheads, dressing-room outfit flatlays, golden-hour walking-from-behind shots, brunch food close-ups, candle-lit dinner tables, vintage shop browsing, looking-up POV with sky behind, behind-the-scenes hands-doing-the-thing.
- **NO**: landscape paintings, atmospheric "vibes" tiles, sunset harbors with no human signal, moss macros, pure scenery, anything that reads as desktop wallpaper or art print. If a tile looks like a Tumblr aesthetic frame from 2014 — fail. The mood board must read as a curated 2024–2026 social feed.

Prompts for generated tiles should always specify a **framing** (phone-camera POV, mirror selfie no face, 3/4 candid, overhead tablescape, etc.) AND a **moment** (the specific second of life captured), not just a "vibe."

See `references/aesthetic-prompts.md` "Social trend framings" for the prompt patterns.

🛑 **HARD RULE: Generated tiles cover ATMOSPHERE only — never the user's real subjects.**
- The user's **face, body, hair** → only their actual photos
- The user's **dog, cat, pet, horse** → only their actual photos
- Their **partner, friends, family, kids** → only their actual photos
- Their **actual car, actual home, actual recurring objects** → only their actual photos

Generated tiles render: rooms, weather, light through windows, hardwood floors, snow on cobblestones, the *type* of object they collect (vintage leather goods, brass watches), the *kind* of place they go (golden-hour skylines, woodland trails). NEVER a fake version of someone or something they actually have. **Reason:** face/animal fidelity drifts, and a fake version of someone's real dog reads as uncanny and insulting. The user will tell you "that's not my dog."

**Composite — fill the template, don't author CSS.** The board is built from a fixed template, `references/templates/mood-board.template.html`, rendered by `mcp__plugin_pika_pika__html_to_png`. Never ask gpt-image-2 to render a "mood board grid" — it hallucinates the tiles. **You only supply data:** exactly 12 `.tile` rows (each an image URL + a per-image `background-position` crop focus), the brand name, the subtitle vibe words, the font pair, and the palette tokens. The template owns the grid math, the white header band, and the dimensions once — so the cream-sliver / off-grid failures can't recur. Set `{{COLS}}` to **6** for portrait tiles (default; most camera-roll input) or **4** for landscape-heavy input. Use exactly 12 tiles so the title-banded board and the PDF full-bleed no-header variant fill the canvas with no empty cells.

**Curated:generated ratio = ~50/50.** Roughly 6 curated + 6 generated for a 12-tile board. A board that's 8+ curated tiles + 2-3 generated reads as "her camera roll dumped on a grid" — not designed. The generated tiles do the work of expanding the aesthetic into branded territory she hasn't shot yet (the brunch tablescape, the wool-coat outfit selfie, the cocktail POV). A 50/50 mix reads as a designed mood board with real-life anchoring.

**Font system — locked here, propagates to Step 4 PDF.**

Pick a typography pair (display + body) that matches the Visual aesthetic adjectives locked in Step 2. **Don't default to Didot or Helvetica reflexively** — the wrong font for the brand makes the mood board read off and undercuts the PDF. The test is whether the font's personality matches the aesthetic adjectives. Heuristic starting points:

| Aesthetic register | Display (titles) | Body (subtitles, captions) |
|---|---|---|
| quiet-luxury, classy, refined | Didot, Bodoni Moda | Inter, Helvetica Neue |
| cinematic, cozy-coastal, editorial | Cormorant Garamond, Playfair Display | Inter, Söhne |
| minimal, modern, clean | Inter Display, Helvetica Neue | Inter, Helvetica Neue |
| playful, retro, Y2K, fun | Recoleta, Bagnard, custom display | Inter, IBM Plex Sans |
| warm-feminine, romantic, soft | Italiana, Cormorant Infant | Inter, Söhne |
| editorial, magazine-style | Playfair Display, GT Sectra | Inter, Helvetica Neue |
| earthy, handmade, organic | Caudex, Recoleta Soft | Inter, IBM Plex Sans |

Save the chosen pair as `fontDisplay` + `fontBody` in the persona.md Visual aesthetic section so Step 4 PDF picks them up. When fonts aren't system-installed (most of the above except Helvetica), source them from Google Fonts by filling `{{FONT_IMPORT}}` with a full `<link rel="stylesheet" href="...">` tag.

**Render the board.** Fill the template tokens:
- `{{TILES}}` — one `<div class="tile" style="background-image:url('IMAGE_URL');background-position:POS"></div>` per tile. `POS` is the per-image crop focus: `50% 20%` upper-body OOTD, `50% 35%` top-down kitchen, `50% 50%` centered.
- `{{BRAND_NAME}}`, `{{SUBTITLE}}` (tracked vibe words, e.g. `BOSTON · WOOL COATS · COCKTAIL BARS`).
- `{{FONT_IMPORT}}` (a Google Fonts `<link>` when the pair isn't system-installed), `{{FONT_DISPLAY}}`, `{{FONT_BODY}}`, `{{BG}}` (lightest palette tone), `{{FG}}`, `{{MUTED}}`.

Then call `mcp__plugin_pika_pika__html_to_png` with `format: "png"` and `raster_options.viewport_px = { width: 1920, height: 1224 }`. If it returns `{task_id, status}`, poll `mcp__plugin_pika_pika__task_status({task_id})` until terminal and read the image URL. **For the PDF full-bleed page (Step 4 page 3)**, render the SAME tiles through `references/templates/mood-board-no-header.template.html` at `{ width: 1920, height: 1080 }` — that variant has zero gutters so the PDF page shows no cream slivers.

**Mandatory checks before delivering:**
1. **Curated tiles required.** A fully-generated mood board is a fail state. Valid curated tiles are user-supplied images or clean public-feed curated frames from a supported social handle. If you can't get either onto the board, the gate is "unblock the real curated source," not "ship without."
2. **No regenerated real subjects.** Re-read the hard rule above. The user's face, pet, partner, friends — never generated. Their atmosphere — fine.
3. **No baked-in text on any tile.** gpt-image-2 prompts must include the no-text guardrail — append `"NO text anywhere in image"` *(load-bearing — gpt-image-2 otherwise bakes faux brand labels onto bottles, scarves, books; see Load-bearing phrases section)*. For handle-only reel-derived curated tiles, use frame 0 from the durable rehosted `.mp4`; if a reel frame still shows burned-in caption/title overlays, drop it rather than shipping text on the board.
4. **Anti-stocky test.** If the board reads as stock photography (uniform polish, uniform palette, studio-perfect, no real-life imperfection) — fail. Trendy 2024–2026 aesthetic energy = real-feeling snapshots > campaign-clean glossiness. The curated user tiles anchor the "real" register; generated tiles should match that energy, not slick up.
5. **Palette variation within the identity.** A cohesive palette is fine; a single-register board ("just brown" / "just sage" / "just beige") reads dead. Even within a warm-cognac identity, you can include warm cream, dusty rose, deep navy, sage — whatever co-exists naturally in their world.
6. **Cast diversity on any generated tiles featuring people.** Name an ethnicity per prompt *(load-bearing procedural rule — gpt-image-2 defaults to lighter skin tones otherwise; see Load-bearing phrases section)*. (Note: with the hard rule above, generated tiles featuring people should be RARE — strangers in scenes only, never the user.) See `references/aesthetic-prompts.md` for the cast-diversity prompt pattern.
7. **Zoom-read the composite.** Open the PNG. Verify no overlapping tiles, no broken aspect ratios, no misaligned content. Tile borders clean.
8. **Anti-template check.** Should feel like THIS person, not a one-word aesthetic preset (NOT "clean girl beige", NOT "dark academia", NOT "cottagecore" unless the user named that aesthetic). If you can label the board with one TikTok aesthetic word — push for specificity.

**Deliver in chat:** "here's your mood board — [link to PNG]. the curated tiles are pulled from [sources]; I filled gaps in [named gaps] with generated tiles. does this feel like your visual world?"

🛑 **Wait for explicit approval** before moving on.

### Step 4 — Influencer Persona PDF (HARD GATE — approval required)

The deliverable is a **multi-page branded PDF** titled `[Name]'s Influencer Persona`, not an inline markdown block. **Never label this artifact a "media kit"** — the user came here to define their persona, not to pitch partners yet; calling it a media kit is premature and undercuts the glow-up framing. The PDF lays voice-bank content into a designed document alongside the persona overview, content categories, approved mood board, and the Key Next Steps roadmap from Step 2's strategic conversation. The user approves the voice bank by approving the PDF.

**What the PDF is for:** the personal artifact that captures who the user is online — what they post, how they sound, what their feed looks like, and the concrete next steps to actually become that persona. It has to be **well-designed** — strong typography, clear hierarchy, generous white space, on-aesthetic. A sloppy PDF undercuts the entire kit.

#### 4a — Draft the voice bank content

Generate the voice-bank text first (the same content the old skill produced inline). Save it as `./tmp/[handle]-influencer-kit/voice-bank.md` for downstream skill consumption. Content sections:

- **Bios (3 variants):** IG main (short tagline), IG alt (longer, more specific), TikTok / casual.
- **Caption modes (5):** Hook, Story, Casual selfie, Vulnerable, Promo. Each mode = a CONTEXT label ("use when…") + 2 sample captions showing range (e.g., one short + one slightly longer).
- **Hook openers (5):** opening lines for Story / Reel / TikTok intros.
- **DM + comment voice:** reply-to-compliment, decline-a-brand-pitch, reply-to-hater (or "doesn't engage"), default emoji palette.
- **Do & Don't (5 each):** person-specific, not generic ("use specific place names" beats "post consistently").

**Quality bars on the copy itself:**
- **Seed every caption from the scraped captions in Step 1** — sentence rhythm, vocabulary, emoji habits, recurring phrases, hook style. Chat-voice fallback only if scrape failed.
- Every caption passes the **anti-generic test** (could it belong to someone else? rewrite if yes).
- Every caption passes the **AI-creator-voice ban list** (no "apparently i [did thing] now", no em-dash parentheticals for wit, no "[x] + [y]" lists with plus connectors, no "fake errand", no listicle minimal poetry, no "I'm just a girl who…").
- **Forbidden words from the identity** never appear in any sample caption.
- The 2-captions-per-mode range shows genuine variation.

#### 4b — Lay it into the PDF

**PDF spec:**
- **Page size:** 16:9 landscape, 1920×1080 per page.
- **Page count:** exactly 12 pages maximum, each focused on one idea. Do not expand the kit past 12 pages: the required `mcp__plugin_pika_pika__analyze_media` PDF QA path uses `all_pages: true`, and that sync path supports at most 12 PDF pages.
- **Typography:** the `fontDisplay` + `fontBody` pair locked in Step 3. NO third font, no mixing of register.
- **Palette:** the Visual aesthetic palette from Step 2. Page backgrounds default to the lightest tone; accents from the rest of the palette.

**Page sequence (target):**
1. **Cover** — name in display font (very large, 120–180pt), tagline subtitle in tracked body-font caps, one hero image (full-bleed or large-cropped), small "Influencer Persona · [year]" label *(never "Media Kit")*
2. **About / Identity** — 1–2 paragraphs synthesized from `identity.md` (real-you + influencer-you, authenticity dial named). Side imagery: 1–3 curated photos + a small stats grid (Based / Niche / Status / Voice)
3. **Mood Board — FULL BLEED** — the approved mood board embedded edge-to-edge, no header band, no padding. Pre-render it by filling `references/templates/mood-board-no-header.template.html`; the template owns the no-header grid math: 6 cols × 320w × 2 rows × 540h = 1920×1080 exactly, no gaps. Tiles touch directly with no cream between them, otherwise the PDF page shows 2–4px cream slivers on the edges and between rows. The title-banded mood board (with gutters + header) is the standalone disk artifact at `mood-board.png`; the edge-to-edge variant is `mood-board-no-header.png` and only used in the PDF.
4. **Content Categories** — 4 cards laid out in a 2×2 grid, each card = image + category name + one-line description + 3–4 example post types. If a scrape exists, categories are derived from the user's actual scraped feed: tally the user's 30 scraped post captions, group by topic/format, pick the four highest-volume buckets. If there is no scrape/no social yet, label the page **Proposed Content Categories** and derive the four cards from the user's answers, taste URLs, reference creators, and real photos; do not claim they are existing feed frequencies. Examples: Outfits & Styling / Boston Lifestyle / Home & Recipes / Brand Partnerships for a NE-coastal lifestyle creator; Workouts / Recipes / Workouts-to-Recipes / Brand Collabs for a fitness creator; Tour & Travel / Studio / Real Life / Brand Collabs for a musician. Use the user's own specificity (e.g. "Nutcracker, holiday markets, Snowport" not "city event content"). This is more useful than a generic color-swatch page. **Do NOT use a flat color-swatch page or a textured-material-swatch page** — both variants read as boring; the texture variant specifically reads as "all cloth" and doesn't tell anyone what the creator actually MAKES.

**Content Categories layout lives in `references/templates/pdf-content-categories.template.html`** (300×400 image, `grid-template-columns: 300px 1fr` card — baked in). Fill `{{CONTENT_CATEGORIES_TITLE}}` as `Content Categories` when a scrape exists and `Proposed Content Categories` when no scrape/no social exists. Fill 4 cards' image/name/desc/post-types + a per-card `{{CARD_N_POS}}` crop focus (`50% 20%` upper-body, `50% 35%` top-down kitchen, `50% 50%` centered). Don't author the card CSS.

5–9. **Voice modes** — one page per caption mode (Hook, Story, Casual selfie, Vulnerable, Promo). Layout: text left half (mode name + "use when" context + 2 sample captions), 2×2 grid of 4 tiles right half.

   **Voice-page layout lives in `references/templates/pdf-voice-mode.template.html`** — one template reused for all 5 modes. The padded grid that prevents the off-page bleed (80px equal padding, 800/160/800 columns, 2×2 grid) is baked in. Fill `{{MODE_NAME}}` / `{{USE_WHEN}}` / 2 captions / 4 tile URLs (+ optional per-tile crop). Don't re-derive the grid CSS.

10. **Hook openers + DM voice** — numbered openers on one side, DM examples on the other
11. **Do & Don't** — two-column side-by-side
12. **Key Next Steps** — the **roadmap** page (replaces the older References + Contact page; never re-add a contact card). 4–6 cards in a 2-column grid, each card = number + section label (e.g. "01 · Lighting & Framing") + one-line headline + 2–3 sentences of concrete action. **Content comes directly from Step 2's strategic conversation** — the lucrative direction chosen in 2a, the gaps named in 2b, and the gear recommendations from 2c. Each card must be a shippable action with a specific number, brand, or behavior — not "improve your content." Example cards (from the gamar___b sample kit): "Stop shooting into harsh overhead light — buy a phone tripod ($15) + clip-on reflector ($25)", "Currently 80% OOTD; target 40/25/20/15 across the 4 content categories", "5K in 90 days: better lighting + 4–5×/week cadence + 1 reel/week tied to a seasonal moment".
   - **Next Steps layout lives in `references/templates/pdf-next-steps.template.html`** — the explicit `.next-grid { height: 720px }` that prevents BOTH the 13th-empty-page and the 300px dead-zone is baked in (Chromium collapses `1fr` rows without a definite height; >740px overflows into an extra page). Fill 4–6 cards (number / label / headline / 2–3 sentences); delete the trailing card blocks for fewer than 6. Don't re-derive this CSS.

**Voice-mode page imagery — the demonstration:**
- **Exactly 4 tiles per voice-mode page, arranged in the 2×2 grid above.** With an 800×920px grid and 16px gap, each tile cell is **392×452px** at page scale. Fill the cell with `width: 100%; height: 100%; background-size: cover;` and tune `background-position` per tile; do not force a separate 3:4 crop that would overflow the grid.
- **Split: 2 curated + 2 freshly-generated tiles per page.** Curated = scraped feed images at higher quality than what's in the mood board (different posts). For handle-only video-heavy / mostly Reels accounts, treat clean `mcp__plugin_pika_pika__extract_frame(video_url: <durable_rehosted_mp4>, time_s: 0)` outputs from `.mp4` `media_url` posts as candidate curated feed images; do not use altered `visual_media_url` signed covers. Before any reel-derived frame is placed on a voice page or content-category card, call `mcp__plugin_pika_pika__analyze_media` on the candidate frame with an OCR / visible text / no-text prompt. Reject frames with baked-in caption/title overlays; if you try a later keyframe, run the same `mcp__plugin_pika_pika__analyze_media` no-text check on that later keyframe before placement. If there is no feed/no social yet, use different user-provided camera-roll photos instead. If there are no curated user photos or clean public-feed curated frames, do not build the PDF; pause and request real photos.
- **Voice-page tiles MUST be different from the mood board.** The mood board is the visual world; voice pages demonstrate the voice with fresh imagery. Reusing mood-board tiles flattens the read.
- **Be smart per mode — match imagery to mode intent:**
  - Hook → bold scroll-stopper OOTD / cinematic outfit walks
  - Story → narrative moments (kitchen, family content, walking scenes)
  - Casual Selfie → **actually selfies** from the user's real photos, or face-free generic selfie-register generated tiles if the user did not provide selfie photos — mirror selfie with phone fully obscuring face, cropped outfit/body detail, back-of-head 3/4, hand-obscured face. No visible generated faces. NOT abstract atmosphere.
  - Vulnerable → quiet-moment imagery — unmade bed, candle, journal, wine-and-candle
  - Promo → product-on-table, brand-deal-style flat lays, the user's own brand collab posts
- **Curated photos (the user's real face / pet / partner) are placed as-is** — never AI-modified. Light CSS color treatment from Step 3 is OK; full re-rendering through gpt-image-2 is not.
- For generated selfie tiles, **never generate the user's face** — render faceless mirror-selfie POVs (`"hand obscuring face"`, `"phone obscuring face"`, `"back-of-head 3/4"`) *(load-bearing phrasings — without them gpt-image-2 invents the user's face, breaking the "this is actually her" anchor; see Load-bearing phrases section)* so the imagery reads as a selfie register without faking identity.
- **gpt-image-2 content-policy fallback:** if a generated selfie-register prompt is rejected because the words "mirror selfie", "selfie", or "phone obscuring face" trip the policy filter, retry once with reworded, policy-safe framing. Drop the word "selfie"; write a hand-held phone body-framing shot, cropped outfit/body detail, or face hidden by a hand-held phone. Do not retry the same prompt or repeat rejected wording. The fallback still requires no visible generated faces and must not invent the user's face.

#### 4c — Design principles (non-negotiable)

- **Typography hierarchy.** Display font for page titles + brand name; body font for subtitles, captions, body. Consistent type scale across pages (e.g., 120 / 64 / 32 / 18 / 13 pt). No third type family.
- **White space is a feature.** Don't fill page edges to edges. Generous margins (80–120px outer).
- **One focal element per page.** Each page has one thing to look at — title + visual, or caption + photo, not 8 things competing.
- **Palette discipline.** Use the locked Visual aesthetic palette throughout. Don't introduce new colors.
- **No baked-in fake data.** Don't invent follower counts, engagement rates, or brand partnerships that didn't happen. If a stats section is included, mark inferred items.

#### 4d — Build approach

- **Assemble from the page templates — don't author HTML/CSS.** `shared_head` = `references/templates/pdf-shared-head.template.html` (carries the palette/font vars + ALL page CSS; fill its `{{FONT_IMPORT}}` / `{{FONT_DISPLAY}}` / `{{FONT_BODY}}` / `{{BG}}` / `{{FG}}` / `{{ACCENT}}` / `{{MUTED}}` tokens). `body_pages[]` = the filled per-page templates in sequence: `pdf-cover` → `pdf-about` → `pdf-moodboard` → `pdf-content-categories` → `pdf-voice-mode` ×5 (one per mode) → `pdf-hooks-dm` → `pdf-do-dont` → `pdf-next-steps`. Each body fragment is markup-only; the worker injects `shared_head` into every page and renders them in parallel, then merges.
- Use one `@page` rule per slide (1920×1080 landscape, no margins on @page).
- Embed fonts by filling `{{FONT_IMPORT}}` with one Google Fonts `<link rel="stylesheet" href="...">` tag; that token is inserted before the shared `<style>` block.
- Reference images as HTTPS URLs — for local images, call `mcp__plugin_pika_pika__upload_asset` first to get a CDN URL, then reference that URL in the HTML.
- **🛑 LOAD-BEARING: pass `pdf_options.paper_size` explicitly to `mcp__plugin_pika_pika__html_to_pdf`.** The `@page { size: 1920px 1080px }` CSS rule alone is **not enough** — `mcp__plugin_pika_pika__html_to_pdf` defaults to US Letter (792×612 points, 1.294 aspect ratio) if `pdf_options.paper_size` is omitted, and the 1920×1080-designed HTML gets scaled/letterboxed into the letter page with giant white bars top and bottom. Always pass:
  ```json
  "pdf_options": {
    "paper_size": {"width": 1920, "height": 1080, "unit": "px"},
    "margins": {"top": 0, "right": 0, "bottom": 0, "left": 0, "unit": "px"}
  }
  ```
  `mcp__plugin_pika_pika__html_to_pdf` defaults to async mode. If the response is `{task_id, status}`, poll `mcp__plugin_pika_pika__task_status({task_id})` in a tight loop until `completed`, `failed`, or `cancelled`; on `completed`, read the PDF URL from the task result before proceeding. Keep the completed `mcp__plugin_pika_pika__html_to_pdf` / `mcp__plugin_pika_pika__task_status` result in notes; its server-side structural metadata (`page_count`, and `pages[]` when present) is the only portable page-count evidence for the timeout fallback. Verify after each render by calling `mcp__plugin_pika_pika__analyze_media` on the rendered PDF as `application/pdf` with `all_pages: true`. Ask it to inspect all pages for 16:9 landscape framing, no US Letter letterboxing, no giant white bars, no blank trailing pages, and no page that breaks the visual hierarchy. If `all_pages: true` times out on an image-dense PDF, use the Step 4e per-page QA + server-result page-count / `pdf_options.paper_size` fallback before deciding whether the render can proceed. If it reports letterboxing or white bars, rerender with the explicit `pdf_options.paper_size` above.
- Save the resulting PDF as `./tmp/[handle]-influencer-kit/influencer-persona.pdf` (never `media-kit.pdf`).

**🛑 PDF size cap: html_to_pdf rejects outputs over 50 MB.** gpt-image-2 PNG outputs are 1–3 MB each; with ~15–20 images per kit, raw PNG embeds can push past the cap on the first render. **Before final PDF render, reduce large generated images through MCP, not local image libraries:** wrap each large image URL in a one-image HTML/CSS frame and call `mcp__plugin_pika_pika__html_to_png` with `format: "jpg"`, `raster_options.viewport_px` capped so the longest side is ≤1400, and `raster_options.jpeg_quality: 85`. If the response is `{task_id, status}`, poll `mcp__plugin_pika_pika__task_status({task_id})` until terminal and use the completed JPG URL in the PDF HTML.

**Canonical generated-tile URL pipeline (MCP-only):**
1. Generate each atmosphere tile with `mcp__plugin_pika_pika__generate_image` (provider="gpt-image-2").
2. For every generated PNG that will be embedded in the PDF, transcode/downscale through `mcp__plugin_pika_pika__html_to_png` by placing the source URL as a full-bleed background image in a small HTML frame and rendering `format: "jpg"` at quality 85.
3. Build an explicit `asset_url_map` in scratch notes: raw generated URL → final JPG URL. Insert the final JPG URLs into the `body_pages` fragments.
4. Grep the final HTML/source notes for raw `gpt-image-` PNG URLs before render; the mood board full-bleed PNG may remain, but voice-page generated tiles should use the final JPG URLs.
5. Call `mcp__plugin_pika_pika__html_to_pdf` with `body_pages`, `shared_head`, and the explicit `pdf_options.paper_size` above.
6. A 12-page kit at this spec should land far below 50 MB. PDFs in the 40–55 MB range mean the MCP JPG conversion step was skipped or the HTML still references raw generated PNGs. AI tiles that still look "stocky" after this means the *composition* itself is the problem — go to Step 4d.5 for the re-generation prompt formula.

**🛑 Cloudflare R2 / `mcp__plugin_pika_pika__upload_asset` PUT gotchas:**
- **Presigned URLs expire in 300s.** A sequential `curl PUT` chain of 10+ files where each takes 8–12s can exceed the window for the last few URLs. **Always run PUTs in parallel** using `(curl ... &)` subshells + `wait`.
- **Subshell PUTs can drop the `Content-Type` header silently** — the file uploads but R2 stores it with `text/html` MIME, which then makes html_to_pdf reject the image with "MIME type 'text/html' is not in the allowlist." Mitigation: after every batch PUT, verify with `curl -s -I <url> | grep content-type` and re-PUT any wrong types.
- **Re-mint + re-PUT immediately if you see 403/ExpiredRequest.** Don't try to extend a stale URL.

#### 4d.5 — Beating the AI tell (the composition is the problem)

gpt-image-2 outputs have two recognizable AI tells:
1. **Photography style** — too-perfect lighting, pristine surfaces, no real-life imperfection. Light CSS treatment can help match the surrounding board.
2. **Composition** — perfectly arranged objects, centered subjects, magazine-product-shoot framing, no real-world clutter. **NOT fixable after generation.** It has to be solved at the prompt level.

**The AI-composition trap (especially in Promo / brand-deal tiles):**
- Three skincare bottles arranged on marble with peonies and rosemary = stock-photo flat lay. AI tell, period.
- Perfume bottle on a folded silk scarf with falling petals = product hero shot. AI tell, period.
- Cinnamon dough perfectly rolled with butter + brown sugar in matching bowls = food-blog stock. AI tell.

**The fix — prompt for *real lived-in context*, not styled arrangement:**
- Skincare: "Phone-camera mirror selfie detail of a generic person holding ONE bottle in a generic bathroom, phone fully obscuring face, toothbrush cup + towel cluttered behind. NOT a styled flat lay."
- Perfume: "Close-up of a generic wrist mid-spritz with the bottle in the other hand visible in soft focus. Background: generic cluttered vanity — hairbrushes, makeup, iced coffee. NOT a product hero shot."
- Cinnamon dough: "Generic hands rolling dough on a marble counter, dusty-rose linen towel half-falling off the side, butter and sugar in small mismatched bowls, off-center framing. NOT overhead-stock-flatlay-perfect."

**The prompt formula that beats the AI tell:**
> [hand-held / mid-action verb] + [real environment with slight clutter] + [faceless person partially in frame] + [imperfect / off-center framing] + `"NOT a [styled flat lay / product hero shot / stock food photo]"`

The trailing `"NOT a styled flat lay / product hero shot / stock food photo"` is the **load-bearing anchor** of this whole pattern — without it gpt-image-2 reverts to centered product composition that later CSS treatment cannot rescue. See Load-bearing phrases section for the full collection.

**HTML/CSS treatment (after generation, before composite/PDF):**
Use the HTML render layer to match generated tiles to the user's real-photo register:
- Slight `filter` changes only: mild contrast, saturation, brightness, or warmth.
- Optional overlay: very low-opacity noise texture or vignette via CSS pseudo-elements.
- Casual crop: `object-position` per tile so the subject is not uniformly centered.
- Never alter real user subjects through an image model. Real user photos stay source-faithful.

#### 4e — Mandatory checks before delivering

1. **Render-read every page through MCP.** Call `mcp__plugin_pika_pika__analyze_media` on the final PDF URL as `application/pdf` with `all_pages: true` and ask for a page-by-page QA pass: confirm every page renders cleanly in 16:9 landscape, no blank pages, no US Letter white-bar letterboxing, no confusing/off-aesthetic pages, no broken hierarchy, and no visible image/crop failure. If any issue is reported, fix the HTML/assets and rerender before delivering.
   - **Fallback only for image-dense PDF timeout / rasterization budget failures:** `all_pages: true` is still the mandatory first QA call. If that all-pages call times out or fails only because the multi-page PDF rasterization budget was exhausted, do not block the run solely on that aggregate failure. Verify structure from MCP/server evidence first: the completed `mcp__plugin_pika_pika__html_to_pdf` or `mcp__plugin_pika_pika__task_status` result must report `page_count: 12` (and `pages[]` length 12 when present), the render request must have exactly 12 `body_pages`, and the submitted `pdf_options.paper_size` must be `{width: 1920, height: 1080, unit: "px"}` with zero margins. Treat that server-render result + request as the MediaBox/page-size contract; do not run local PDF inspection or local PDF tools/libraries. If the server result lacks `page_count`, the fallback is not proven: rerender with smaller JPG assets or stop and report `pdf_structural_metadata_unavailable`. Once structure is proven, run per-page MCP QA with `mcp__plugin_pika_pika__analyze_media(media=<pdf_url>, application/pdf, page: <n>)` for page 1 through page 12, asking the same visual QA question for each page. Any per-page visual defect still blocks delivery and requires rerender.
2. **Anti-AI-voice on all captions** is re-checked before they go into the PDF.
3. **Real photo integrity** — the user's face / pet / partner only as curated originals (or lightly graded), never AI-rendered.
4. **Typography consistency** — same display + body pair on every page. No surprise font swaps.
5. **No baked-in text on any tile** (carried over from Step 3). Check generated, curated, public-feed, and reel-derived tiles; if a frame has burned-in caption/title overlays or any other visible text, replace it and rerender before delivery. For reel-derived tiles, verify the build notes include the sourcing-time `mcp__plugin_pika_pika__analyze_media` OCR/no-text result for each candidate frame before placement; final PDF QA is a backstop after sourcing, not the first text gate.
6. **Palette stays inside the spec** — no rogue colors.
7. **PDF size under 50 MB** — if html_to_pdf returns a "File too large" error, the MCP PNG→JPG conversion step (4d) was skipped.
8. **Voice-page imagery is mode-appropriate** — Selfie page actually shows selfies; Vulnerable page actually shows quiet-moment imagery. Not "abstract atmosphere for everything."
9. **Voice-page tiles are not mood-board tiles.** Fresh imagery only.

**Deliver in chat:** path to PDF + 1-line description. Ask: "approve this to ship the kit, or anything to swap before we lock it in?"

🛑 **Wait for explicit approval** before Step 5.

### Step 5 — Package the Kit (HARD GATE — only after explicit ship-it)

🛑 **STOP. This is a hard gate, not a soft suggestion.**

Same gate logic as `build-a-brand` Step 4. Do not begin packaging until the user says ship-it / approved / go / lock it in. "I love it" alone is ambiguous — confirm.

**Final ask format when delivering Step 4:** end with "ready to lock this in and ship the kit, or want to adjust anything first?" Then **stop and wait**. Do not stage the kit directory. Do not move files. The identity is not approved until the user says so.

**Kit structure:**

```
./tmp/[handle]-influencer-kit/
├── influencer-persona.pdf      # HEADLINE artifact — the designed Influencer Persona PDF (never named "media-kit.pdf")
├── mood-board.png              # approved composite board (~1920×1224 with title header)
├── mood-board-no-header.png    # full-bleed variant used in the PDF (1920×1080, no title band)
├── persona.md                  # comprehensive identity spec (contract for downstream skills) — formerly brand.md, do NOT recreate as brand.md
├── identity.md                 # "who you are" vs "who your influencer is" + strategic direction + gap analysis + content critique — long-form
├── voice-bank.md               # bios, captions (with context labels + 2 per mode), hooks, DMs, do/don't — what the PDF was built from
├── next-steps.md               # Key Next Steps roadmap from Step 2a strategic direction, Step 2b gap analysis, and Step 2c content critique / gear recs; mirrored as a standalone file for downstream content calendar skills
├── images/                     # 🛑 LOAD-BEARING: every image that appears in the PDF, packaged together
│   │                           #   the user receives a self-contained reference of all the visual assets without
│   │                           #   having to dig through mood-board/ and build/ subfolders. shipped at the same
│   │                           #   level as the PDF so it's obvious. populate with copies (not symlinks) of:
│   ├── tile_01.jpg … tile_06.jpg     # 6 mood-board curated tiles used in the composite
│   ├── voice_01.jpg … voice_10.jpg   # 10 voice-page curated tiles used in voice grids + categories page
│   ├── v_hook_1.jpg … v_promo_2.jpg  # generated voice-page tiles after MCP JPG conversion
│   ├── mood-board.png          # title-banded version (matches root-level file)
│   └── mood-board-no-header.png # full-bleed version embedded in PDF page 3 (matches root-level file)
├── mood-board/                 # raw source assets (kept for re-generation, not for end-user browsing)
│   ├── curated/                # individual full-res user photos
│   ├── voice-curated/          # 10 tiles pulled from feed for the voice pages (2 per mode, distinct from mood-board tiles)
│   └── generated/              # raw atmosphere tile URLs generated for mood board + voice pages
├── build/                      # build-time sources — keep for re-renders
│   ├── mood-board.html         # title-banded mood-board HTML rendered by html_to_png
│   ├── mood-board-no-header.html # full-bleed mood-board HTML rendered by html_to_png
│   ├── asset-url-map.md        # raw generated URL → MCP JPG URL map used by the final PDF
│   └── influencer-persona.html # source notes for shared_head + body_pages (never named "media-kit.html")
└── README.md                   # how to feed this kit to other skills
```

**`images/` is mandatory.** When Step 5 packages the kit, copy every image actually used in the PDF into `./images/` as the user-facing asset directory. The `mood-board/` and `build/` folders stay for re-generation/debugging — they contain raw sources, render HTML, and URL maps that are confusing to browse. The user's mental model is "I want a folder of the photos that ended up in my kit"; `images/` is that folder. Use file copies, not symlinks (zip and Google Drive both handle copies cleanly; symlinks break across both).

**Sample posts are NOT shipped.** Earlier versions of this skill included a directory of image+caption pairs. That was cut — the voice bank's caption-mode examples already demonstrate voice-in-context, and adding image+caption pairs added work without shipping a clearly-better artifact. Downstream skills that need user likeness should use the user's curated photos as their own runtime references; this skill does not generate fake versions of the user.

**`persona.md` structure** — see `references/persona-md-template.md`. Must include:
- Quick reference block (handle, niche, voice in 3 words, aesthetic in 3 words, authenticity dial, **typography pair**)
- The full identity (real you + influencer you, with the dial explicitly stated)
- **Strategic direction** — the path chosen in Step 2a (niche label, why-it-fits, monetization profile, content load, who's already winning)
- **Gap analysis** — current state → target persona, what's missing (content categories, formats, cadence, voice, aesthetic, follower-tier)
- **Content critique + gear recs** — the production-quality call-outs from Step 2c, including the specific gear/tools recommended
- Visual aesthetic (palette, lighting, settings, photography style, subjects, forbidden, relationship to existing grid, **typography: fontDisplay + fontBody**)
- Voice (sounds like / never sounds like / adjectives / forbidden)
- Bio variants
- Caption modes
- Hook openers
- DM + comment voice
- Do & Don't
- Reference creators (with dimension + what to borrow)
- **Key Next Steps** — same 4–6 cards that appear on the final PDF page; this section is the canonical source and the PDF page reads from it
- **How to use this with other skills** — section telling other Pika skills (`ugc-ads`, `podcast`, `founder-product-video`, `app-sizzle`, `app-store-screens`) how to read this kit. e.g. "ugc-ads: pull voice from voice-bank.md hook captions; pull likeness reference from one of the curated photos in mood-board/curated/; adjectives from the Visual aesthetic section drive setting/lighting; use the locked typography pair for any on-screen text."

**`README.md`** — 1-page guide:
- What's in the kit
- How to paste `persona.md` into other Pika skill prompts
- Which file feeds which skill (table)
- Note: the kit doesn't include a content calendar; it's identity + a glow-up roadmap, not a posting schedule.

**Save location:** `./tmp/[handle]-influencer-kit/`. Per the global rule, all generated deliverables go to `./tmp/`, never `~/Desktop`. Tell the user the path so they can navigate to it.

**Final delivery message:**
- Path to the kit folder
- Inline preview of the `persona.md` quick reference block
- 1-line on how to use it next: "paste `persona.md` at the top of any Pika skill prompt to get on-brand output."

## Key Principles

- **The person is the brief.** Read what's in front of you (socials, photos, the way they talk in chat) before asking anything. Don't ask things you can already answer from inputs.
- **One specific person, not a niche label.** Don't write "lifestyle creator" — describe the actual human, with their actual comfort show and their actual high-school self.
- **Authentic > polished.** When the user provided real photos, real photos always beat AI-generated. GPT-image-2 only fills atmosphere-coverage gaps in the mood board — never regenerates the user's real subjects.
- **Anti-generic at every output.** Visual aesthetic test, caption test, do/don't test: could this belong to anyone else? If yes, rewrite.
- **Authenticity dial is named explicitly.** persona.md must say what's amplified vs. true-self. Hiding the dial makes the identity feel dishonest.
- **Render-and-READ every text artifact.** Open the file. Read it as a stranger would. If the caption could appear on a random influencer page, rewrite.
- **Approval gates are hard stops.** Three gates (identity → mood board → voice → ship). Creative direction ≠ approval.
- **Output to `./tmp/`**, never `~/Desktop` (per global rule).
- **Always `provider="gpt-image-2"`** for any image generation (per global rule).

## Quality Standards — Non-Negotiable

### The Anti-Generic Test
Before delivering anything: *could this identity be repasted onto a different creator?* If yes, it's not done.

Strong creator brand = specific human + specific point of view + specific visual aesthetic Step 3 can actually render.
Weak creator brand = vibes + adjectives + "authentic + aspirational + community-driven."

### Copy Standards
**What good creator copy sounds like:**
- It has an actual opinion: "audiobooks count as reading. fight me."
- It names a real moment: "the third time I cried at the desk job"
- It trusts the reader: no over-explaining, no "as someone who has always..."
- It contradicts itself sometimes (real people do)

**What bad creator copy sounds like (never write this):**
- "Living my truth ✨"
- "On a journey to..."
- "Sharing my passion for..."
- "As a [identity], I believe..."
- Anything that could be a Canva quote-card template

### Aesthetic Standards
**Mood boards must feel like THIS person.** A board labeled "clean girl beige" or "dark academia" without the user explicitly naming that aesthetic is a failure. The board should be hard to label with a one-word TikTok aesthetic — it should feel like a specific human's visual world.

### Voice Standards
- Every sample caption must pass a read-aloud test. Read it. If it doesn't sound like a person, rewrite.
- Forbidden words from the identity must never appear in any sample.
- Vulnerability is fine; performed vulnerability is not. If the vulnerable-mode caption reads as a Notes-app screenshot draft for engagement — rewrite.

🛑 **HARD RULE: Never write in AI-creator-voice.** This is the most common failure mode. AI voice mimics "casual creator wit" by reaching for the same construction patterns every time. Banned constructions in any sample copy you write for the user:

- **"apparently i [did thing] / moved / became [thing] now"** — fake self-discovery
- **em-dash parentheticals for wit** — "i moved to boston — apparently — to wear coats"
- **"[thing] + [adjacent thing]"** lists with plus signs as connectors — "one drink + a fake errand"
- **forced quirky-specific details** that are actually generic — "fake errand", "fake date", "the third time i [thing]", "the [universe/algorithm] knew"
- **"I'm just a girl who..."** / **"I'm not [extreme] but [normal]"** structures
- **"real ones know"** / **"we don't talk about [thing]"** / **"iykyk"** / **"no thoughts just [thing]"**
- **lower-stakes self-deprecation that's actually self-promotion** — "apparently I'm a wool-coat person now"
- **listicle-style minimal poetry** — "two drinks. one walk. no thoughts."
- **observational tone with a wink at the end** that wasn't earned

**The test:** read the sample caption aloud. If you imagine ANY creator could post it without changing a word and it would still fit them — it's AI voice, not THIS user's voice. Rewrite.

**The fix:** the user's scraped captions ARE their voice. Pull phrases, sentence rhythm, and energy DIRECTLY from the posts you read in Step 1. If scrape failed or the account was caption-light, fall back to how they answered the 4 canonical questions and how they talked in chat. The "sounds like" section of persona.md should use **direct quotes from the user** wherever possible — first from their captions, then from their chat — not invented "creator-style" approximations. If their actual words are flat-declarative, the brand voice is flat-declarative; don't add "wit" they didn't ask for. If they explicitly ask for "more fun / less dry," add wit through more specific real-life observations, never through the banned constructions above.

## Engine choice: gpt-image-2

Default to `gpt-image-2` at `quality: "medium"` for all generations:
- Best instruction-following for cast-diversity prompts.
- Strongest no-text guardrail adherence (critical for mood board tiles).
- Native 9:16 portrait for the default 6×2 mood-board tile layout; 4:3 landscape if using the 4×3 alternate.

Avoid `nano-banana-pro` (bakes magazine-style text into shots). Use `seedream` only if the user explicitly asks for 2K/4K print-tier shots.

## Runtime expectations

Tell the user the rough total up front.

| Stage | Time | Notes |
|---|---|---|
| Stage 0 → Step 1 (intake + Q&A + social scrape) | 5–15 min | User-paced; one batch of questions; scrape runs in parallel |
| Step 2 (identity summary) | 2–4 min | All text; user reads + approves |
| Step 3 (mood board: font pick + curate + GPT fill + composite) | 6–10 min | gpt-image-2 generations + HTML/CSS composite rendered through `mcp__plugin_pika_pika__html_to_png` |
| Step 4 (Influencer Persona PDF: voice draft + 10 new generated tiles + 10 curated tiles + HTML layout + MCP JPG conversion + html_to_pdf render) | 12–20 min | Heaviest step. ~10 gpt-image-2 generations in parallel, curated image selection, MCP image renders, HTML + PDF render, JPG conversion pass to stay under 50 MB cap. |
| Step 5 (package kit) | 2–4 min | File assembly + README |

Total: ~30–60 min wall-clock excluding user response time.

## Load-bearing phrases

Verbatim anchors that go into gpt-image-2 prompts (or procedural rules that hold the recipe together). **Do not paraphrase or strip these when simplifying nearby prose** — they're empirical behavior dependencies, not writing style. Every entry here is referenced inline elsewhere in this file via `(load-bearing — …; see Load-bearing phrases section)`.

### Composition anchors (the AI-tell fix)

- **`"NOT a styled flat lay / product hero shot / stock food photo"`** — append to every Promo-mode tile prompt and any prompt featuring objects on a surface. Without it, gpt-image-2 reverts to centered product composition that later CSS treatment cannot rescue. Referenced in Step 4d.5 prompt formula.
- **`"generic bathroom"` / `"generic cluttered vanity"` / `"slightly cluttered nightstand"`** — environmental context anchors that move the model from studio-set composition to lived-in-context composition without inventing the user's real home or body. Pair with the negative anchor above. Referenced in Step 4d.5 worked examples.

### Identity-preservation anchors (selfie / face content)

- **`"faceless"`, `"hand obscuring face"`, `"phone obscuring face"`, `"back-of-head 3/4"`** — load-bearing for ALL selfie-mode generations. Without one of these, gpt-image-2 invents the user's face, breaking the "this is actually her" anchor (hard rule in Step 3). Referenced in Step 4b voice imagery + Step 3 hard rule. If gpt-image-2 rejects the original wording on content-policy grounds, retry once after dropping the word "selfie" and rephrasing as a hand-held phone body-framing shot with the face hidden by a hand-held phone; do not repeat the rejected prompt.

### Image-content guardrails

- **`"NO text anywhere in image"`** — every generated tile, no exceptions. Without it, gpt-image-2 bakes faux brand labels onto bottles, scarves, books, journal pages. Referenced in Step 3 mandatory check #3 + Step 4d.5 worked examples.
- **`"social-content atmosphere only"`** — mood-board generation framing. Pushes gpt-image-2 away from vision-board / wallpaper / art-print energy toward creator-feed energy. Referenced in Step 3 source priority #6.

### Procedural anchors

- **Name a specific ethnicity per face-bearing prompt** — gpt-image-2 defaults to lighter skin tones otherwise. Vary across the set. Referenced in Step 3 mandatory check #6.
- **Render generated PNGs through `mcp__plugin_pika_pika__html_to_png` before PDF embedding** — the MCP JPG conversion keeps the final PDF under the 50 MB cap and lets CSS filters/overlays match the generated tile to nearby real-photo register. This is size + presentation hygiene; it cannot rescue bad generated composition.

### Voice anchors (caption copy)

- **AI-creator-voice ban list** — "apparently i [did thing] now", em-dash parentheticals for wit, "[x] + [y]" lists with plus connectors, "fake errand", "I'm just a girl who…", "real ones know", "iykyk", "no thoughts just [thing]", listicle minimal poetry. Every sample caption is checked against this. The list lives in full under Quality Standards § Voice Standards § HARD RULE: Never write in AI-creator-voice. Treat that list as load-bearing — adding a new caption-mode example without re-checking it against this list is the #1 way the voice bank silently degrades.

### Maintenance

When editing the skill: if you touch a section that references one of these phrases inline, leave the phrase exactly as quoted. If you want to change one, change it in this section first, propagate the change to all inline references, and document why in the commit message.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Identity reads as generic / could belong to anyone | Skipped the specificity push in Step 2; defaulted to adjective soup | Rewrite with a real opinion, a real moment, the user's actual comfort show. Re-run anti-generic test. |
| Mood board feels like a one-word aesthetic preset | GPT-image-2 prompts referenced an aesthetic label ("clean girl", "dark academia") | Strip aesthetic labels from prompts. Prompt for the specific visual qualities (warm window light, papers on desk, half-drunk drink, etc.) — not the meta-label. |
| Mood board shipped fully-generated, no curated tiles | User-supplied images didn't land on disk (chat-pasted screenshots arrive without a file path); skill compromised and substituted GPT-rendered stand-ins instead of unblocking the file path | Unblock the file path first. Ask the user to save the file to `./tmp/[handle]/grid.png` (or similar) or drag-drop the actual file from Finder, not a screenshot paste. Do NOT substitute generated stand-ins for the user's real world. |
| Generated a fake version of the user's real subject (their dog, their face, their car) | Treated the user's real subjects as "fill these with GPT" gaps | Hard rule: NEVER generate the user's face, pet, partner, friends, family, or recurring specific objects. Those come from their photos only. GPT renders atmosphere — rooms, light, weather, settings, *types* of objects. The user will tell you "that's not my dog" — and they're right. |
| Mood board reads as stocky / iStockphoto density | Too many tiles (24+), uniform polish, uniform color register, studio-clean | Exactly 12 tiles at 1920×1080. Varied palette within the identity. Real-feeling snapshots > campaign-clean. The curated user tiles set the "real" register; generated tiles match that energy, never slick up. |
| Mood board palette collapses to one color (e.g. "just brown") | Every generated prompt named the same dominant color register | Cohesive palette is fine; mono-register is dead. Even a warm-cognac identity can include cream, sage, dusty rose, deep navy where those co-exist in the user's world. Vary lighting and setting, not just subjects. |
| Sample captions sound like creator-template filler | Wrote in "creator voice" instead of THIS creator's voice | Re-read the user's actual scraped captions and the personality Q&A. Pull phrases / energy / sentence rhythm from those. Rewrite from there. |
| `mcp__plugin_pika_pika__scrape_social` returns "not found" | Handle typo or wrong platform (gave you a TikTok handle thinking it was IG) | Confirm the handle with the user, retry with the correction. |
| Taste URL sent to `mcp__plugin_pika_pika__scrape_social` and fails | Spotify / Depop / Letterboxd / personal sites are taste signals, not supported `mcp__plugin_pika_pika__scrape_social` platforms | Do not call `mcp__plugin_pika_pika__scrape_social` for unsupported taste URLs. Record what the URL suggests; if unclear, ask what dimension to borrow from it. |
| `mcp__plugin_pika_pika__scrape_social` returns "private account" | Account is private | Ask the user to set it public temporarily OR paste 5–10 recent captions in chat. If they cannot, mark the voice bank as inferred from chat answers and keep caption examples conservative. |
| `mcp__plugin_pika_pika__scrape_social` throttled | Platform rate-limited the worker | Wait 60s and retry once. If still throttled, fall back to manual caption paste. |
| `mcp__plugin_pika_pika__scrape_social` returns posts but no caption text | Photos-only / reels-only account with no caption bodies | Use bio + chat-voice as voice signal. Note in `persona.md` that captions weren't available so other skills know the voice was inferred. |
| `URL signature mismatch` when trying to use a reel cover | Used or modified the ephemeral IG `visual_media_url` / signed cover URL instead of a durable video asset; signed cover query params must stay untouched and are not reliable curated-tile sources | For handle-only Reels accounts, ignore the signed cover for curated tiles. Use the durable rehosted `.mp4` `media_url` (for example `cdn.pika.art`) and call `mcp__plugin_pika_pika__extract_frame(video_url: <durable_rehosted_mp4>, time_s: 0)` to create the tile. |
| Reel-derived curated tile has baked-in caption/title overlays | Treated an extracted reel frame as already approved, skipped the sourcing-time `mcp__plugin_pika_pika__analyze_media` OCR/no-text check, or sampled a mid-clip reel frame after the creator's text appeared | Extract frame 0 / `time_s: 0` from the durable rehosted `.mp4`, then call `mcp__plugin_pika_pika__analyze_media` on that candidate frame before placement. If frame 0 contains visible text, a title card, or a burned-in caption, drop the reel or try a later keyframe and run the same `mcp__plugin_pika_pika__analyze_media` no-text check before using it. Mood-board and voice-page tiles must have no text on tiles; final PDF QA is only a backstop. |
| User says "make it more X" without approving | Treated creative direction as approval | Incorporate the direction, regenerate the relevant artifact, ask for approval again. Don't skip the gate. |
| Mood board has visible misaligned / overlapping tiles | HTML/CSS grid dimensions or `object-position` values were off | Re-check tile dimensions and grid spacing. Re-render with `mcp__plugin_pika_pika__html_to_png`. Don't ship a misaligned board. |
| Generated cast defaults to white / light-skinned | gpt-image-2 default behavior when ethnicity isn't named in the prompt | Name a specific ethnicity per face-bearing prompt, varied across the set. See `references/aesthetic-prompts.md` for the pattern. |
| Authenticity dial isn't called out in persona.md | Treated "real / amplified / different" as a private decision instead of public spec | persona.md must say it out loud. Other skills downstream read this file — they need to know what's amplified. |
| Skill skipped the strategic conversation and went straight to identity lock | Treated Step 2 as just "draft identity.md" instead of the four-part real-talk step | Step 2 has four parts (2a strategic direction, 2b gap analysis, 2c content critique + gear, 2d identity lock). Skipping 2a–2c is the most common failure mode — the user came for the real talk, not for packaging. |
| Influencer Persona PDF labeled "Media Kit" anywhere | Defaulted to the older naming when the user said remove it | The cover eyebrow reads "Influencer Persona · [year]", the PDF file is `influencer-persona.pdf`, the HTML is `influencer-persona.html`. "Media Kit" appears nowhere in the kit. If found, rename. |
| Voice page 2×2 grid bleeds off the right or bottom edge of the page | Used `position: absolute` with hand-tuned offsets, or asymmetric padding (e.g. `100px 120px`) | Equal 80px padding on all four sides; flex/grid layout with explicit 800×920px grid container and `width:100% / height:100%` on each tile. See Step 4 page-sequence load-bearing layout rule. |
| Key Next Steps page has 300+ px of dead space below the cards | Grid rows auto-sized to content; flex container had spare height that didn't propagate to rows | Set `.next-grid { height: 720px; grid-template-rows: 1fr 1fr 1fr; }` so the 3 rows distribute evenly across a definite height. See Step 4 page-sequence load-bearing rule for the final page. |
| Kit shipped a contact card / "let's work together" page | Inherited the old refs-and-contact final page | The final page is **Key Next Steps**, not a contact card. The user defines their persona, not their brand-deal contact form, in this skill. |
| Content categories card photos crop the subject's chin off or center the wrong thing | Used uniform `background-position: center` for all 4 cards | Each card declares its own per-card `background-position` (e.g. `50% 20%` for upper-body, `50% 35%` for top-down kitchen, `50% 50%` for centered subjects). Image container is 300×400, not 240×320. |
| PDF has giant white bars at the top and bottom of every page | Forgot to pass `pdf_options.paper_size` to `mcp__plugin_pika_pika__html_to_pdf` — the @page CSS rule is not enough; the tool defaults to US Letter (792×612, 1.29 aspect) and the 1920×1080 HTML letterboxes into it | Always pass `pdf_options: { paper_size: {width: 1920, height: 1080, unit: "px"}, margins: {top:0, right:0, bottom:0, left:0, unit:"px"} }`. After render, call `mcp__plugin_pika_pika__analyze_media` on the PDF as `application/pdf` with `all_pages: true` and ask it to flag white-bar letterboxing or any non-16:9 page. |
| `mcp__plugin_pika_pika__analyze_media(all_pages: true)` times out on an image-dense final PDF | Multi-page PDF rasterization budget exhausted before Gemini sees every page | Use the Step 4e fallback only with portable evidence: `mcp__plugin_pika_pika__html_to_pdf` / `mcp__plugin_pika_pika__task_status` result `page_count: 12` (and `pages[]` length 12 when present), original `body_pages.length === 12`, and explicit 1920×1080 `pdf_options.paper_size`. Then run `mcp__plugin_pika_pika__analyze_media` with `page: <n>` for page 1 through page 12. If `page_count` is missing, rerender smaller or stop with `pdf_structural_metadata_unavailable`; do not use local PDF tools/libraries. |
| Voice-page AI tiles still look stocky in the rendered PDF | The prompt composition is stocky OR the final `body_pages` still reference raw generated PNGs instead of MCP-converted JPG URLs | Re-generate with lived-in-context prompts. Then update `asset_url_map`, replace the raw generated URLs in `body_pages`, and grep the source notes for stale raw generated URLs before rerender. |
| Final kit ships without an `images/` folder | Treated the existing `mood-board/` + `build/` subfolders as sufficient | At Step 5 packaging, create `./images/` and copy every image actually used in the PDF (curated tiles, MCP-converted generated tiles, mood-board variants). The user expects a single browse-able folder of "every photo in my kit"; raw asset folders aren't a substitute. |
| Kit shipped before user explicitly approved | Misread "I love this" or "make it more X" as ship-it | Approval is explicit only. Re-ask if ambiguous. The gate exists because the kit locks every decision. |
| `mcp__plugin_pika_pika__html_to_pdf` returns "File too large" (>50 MB) | Embedded gpt-image-2 PNG outputs at full resolution. 10–20 PNGs at 1–3 MB each blow past the cap. | Mandatory: convert large PNG image inputs to JPG q85 through `mcp__plugin_pika_pika__html_to_png` before the final render. See Step 4d for the workflow. Result should land far below 50 MB for a 12-page kit. |
| Texture-swatch / color-swatch palette page reads as "all cloth" or "all boring" | Tried to make the Visual Aesthetic page interesting with material textures (cashmere, peony, silk, leather, velvet, eucalyptus) but textures end up reading as the same fabric register — they don't tell a brand partner what the creator actually MAKES. | Replace the Visual Aesthetic page with a **Content Categories** page (page 4). 4 cards in 2×2 grid, each = image + category name + 1-line description + 3–4 example post types. Categories derived from the user's actual feed. This is what brand partners want to see. |
| Voice-page imagery doesn't match mode (e.g. atmospheric scenery on a Selfie page) | Treated voice pages as "any aesthetic image" instead of mode-demonstrative imagery | When the mode is "Casual Selfie," show actual selfies (mirror, 3/4 back-of-head, phone-obscured face). When "Vulnerable," show quiet-moment imagery (unmade bed, candle, journal). Match the mode intent — that's the whole point of demonstrating voice-in-context. |
| Voice pages reuse mood-board tiles | Defaulted to mood-board imagery to save generation cost | Voice pages need FRESH imagery — different curated posts from scrape (use other `image_versions2.candidates[0].url` indices) + freshly-generated tiles. The mood board is the visual world; voice pages prove the voice in NEW contexts. |
| Mood board on PDF page 3 reads with empty cream around it | Used `mood-board.png` (with title band) and `background-size: contain` | Pre-render a `mood-board-no-header.png` variant (1920×1080, just the tile grid, no title) and embed full-bleed with `background-size: cover`. Keep the title-banded version as the standalone disk artifact. |
| Thin cream slivers visible on the left/right edges (or between rows) of the full-bleed mood board page | No-header HTML kept the standard outer padding/gutters | The no-header variant must use zero outer padding, zero gutters, and tile dimensions that exactly fill 1920×1080. The standalone disk mood-board.png keeps its gutters/header. |
| AI tiles still feel AI after CSS treatment | The AI tell is the *composition*, not just the photography style — and presentation treatment can't redo composition. Common: skincare flat lay on marble with peonies, perfume on silk scarf, perfectly arranged cinnamon dough. | Re-generate with prompts that put the item in *real lived-in context* — handheld + actual messy environment + faceless person partially in frame + "NOT a styled flat lay / product hero shot." See Step 4d.5 for the prompt formula and Promo-mode examples. |
| gpt-image-2 rejects a generated selfie-register prompt on content policy | The prompt used risky terms such as "mirror selfie", "selfie", or "phone obscuring face" | Retry once with policy-safe wording: drop the word "selfie", describe a hand-held phone body-framing shot or face hidden by a hand-held phone, and keep no visible generated faces. Do not repeat the rejected prompt. |
| html_to_pdf rejects image asset with "MIME type 'text/html' is not in the allowlist" | A parallel subshell `curl PUT` after `mcp__plugin_pika_pika__upload_asset` dropped the `Content-Type: image/jpeg` header silently; R2 stored the JPG with `text/html` MIME | After every batch PUT, verify with `curl -s -I <url> \| grep content-type` and re-PUT any with wrong types. Or use sequential PUTs (but watch the 5-min URL TTL — see next row). |
| Cloudflare R2 returns 403 ExpiredRequest on PUT | Presigned URL TTL is 300s. A sequential `curl PUT` chain of 10+ files at 8–12s each exceeds the window for the last few URLs. | Run PUTs in parallel using `(curl ... &)` subshells + `wait`. Mint + PUT within one tight cycle. Re-mint if you hit 403 — don't try to extend a stale URL. |
