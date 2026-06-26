---
name: anime-match
description: >-
  Put the USER into a ~45s Japanese-anime football short as the hero — from their
  photo + their favorite team + the opponent. Anime-fies the user's face into a
  consistent character sheet, designs a dramatic 3-act match (come on → equalizer
  → winner) with the user scoring, writes three 15s cel-shaded scene prompts (CAPS
  names + Japanese dialogue), generates them on Seedance off the sheets, and stitches
  them. The "anime match" trend (Higgsfield+Claude) rebuilt on the Pika MCP, but the
  star is YOU. Triggers: "/anime-match", "put me in an anime soccer video", "make me
  the anime football hero", "anime match with my photo". Requires the Pika MCP.
argument-hint: <your photo> + <your team> vs <opponent>  (+ optional on-screen hero name)
---

> INTERNAL-RELEASING SKILL — submitted for internal testing. Loaded as `/creative-growth-internal-releasing:anime-match`.

# anime-match

Turn the **user** into the hero of a **3-scene (~45s) Japanese-anime football short** — the format @stevenwommack / @leonrdewa popularized for the 2026 World Cup, but the star is the person running it. Each scene is a 15s cel-shaded anime beat with the user (named, in CAPS) and Japanese dialogue, generated on **Seedance** off an **anime character sheet** made from the user's photo, then stitched.

**The proven pipeline (do not deviate from the order):**
`user photo → anime CHARACTER SHEET (nano-banana-pro) → DESIGN the dramatic match + WRITE 3×15s scene prompts (you, acting as Claude) → SEEDANCE each scene off the sheet → STITCH`.

The magic is in three things, in this order: (1) a **character sheet** so the user's anime likeness is consistent across every scene, (2) a **specific, dramatic match** designed for them (their team vs the opponent, real **kit colors**, a concrete goal mechanic each scene — not a generic "he scores"), (3) the **scene-prompt formula** (cel-shaded style tag + named hero in CAPS + camera/anime techniques + Japanese VO).

---

## Stage 0 — Intake

Collect, in one pass (the only things that change per user):
- **The user's photo** *(required)* — a clear face photo; this becomes the anime hero. Local path or URL. Likeness comes from this. Upload local files via `upload_asset` → use the `public_url`. (If on Claude Desktop where pasted images don't reach MCP, ask once for a URL or a `.zip`.)
- **On-screen hero name** *(optional)* — what to call them in CAPS in the prompts + Japanese VO (e.g. "MATAN"). Default to their first name, or "THE STRIKER" if they'd rather not use a name.
- **Their team** *(required)* — the hero's side. Capture the **kit colors / stripe pattern** (e.g. "sky-blue and white vertical stripes"), NOT the crest or sponsor (describe colors, not trademarks — see de-branding in failure modes).
- **The opponent** *(required)* — who they're playing against. Capture the opponent's **kit colors** too. Opponent players (keeper, a defender) are generic — described by kit color, not named.

Confirm in one line ("Putting YOU in an anime match — [TEAM] vs [OPPONENT], you score the winner…"), then run the pipeline. No further yes/no gates.

---

## Stage 1 — Anime character sheet (`generate_image`, nano-banana-pro)

Generate ONE anime **character sheet** of the user from their photo. The sheet (multiple angles + full body + close-ups) is what keeps the face consistent across all three scenes.

Call `generate_image` with:
- `provider`: **`nano-banana-pro`** (REQUIRED default). It does reference-identity → anime stylization cleanly for any real face. **Don't use `gpt-image-2`** here — OpenAI's safety system rejects anime-editing a real photo of an identifiable person (`content_policy` / `image_generation_user_error`).
- `reference_images`: `[<the user's photo url>]`
- `aspect_ratio`: `16:9` · `quality`: `high` · `output_format`: `png`
- `prompt` (verbatim template — fill `{NAME}`; put them in their team kit):
  ```
  Create a character sheet of this football player named {NAME} in a {TEAM kit colors} kit, with close-ups and full body shots from different angles in Japanese anime style.
  ```

Save the returned URL as `state.sheets[HERO]`. Inspect: the sheet must be clearly that person, anime-styled, with usable full-body + face angles. Re-roll if it drifts. *(If the user also wants a named teammate/rival on screen with a real face, make a sheet per character the same way; otherwise opponents stay generic.)*

---

## Stage 2 — Design the match + write the 3 scene prompts (you = "Claude")

This is the step the creator did in Claude. **You do it directly.** There's no real game to research — you **design a dramatic, specific match** for the user, then WRITE it in the formula. Specificity is what sells it: pick a real goal mechanic for each scene, not "he scores."

1. **Design the match:** the user's team ([TEAM]) vs [OPPONENT] in a huge night stadium. Decide the arc — the hero comes on with the team behind, equalizes, then scores a dramatic late winner. For each goal choose a **concrete mechanic** (a volley, a header off a cross, a turn-and-finish, a solo run, a free-kick) and a **scoreline + minute**. Use the two teams' **kit colors** throughout; opponent keeper/defenders by color only.

2. **Write exactly 3 scenes, 15s each**, following the proven 3-act arc:
   - **Scene 1 — "THE CALL":** the hero comes on / kickoff for [TEAM], tension building, crowd roaring, a teammate or the bench urging them on.
   - **Scene 2 — "THE EQUALIZER":** the hero scores the equalizer vs [OPPONENT] with the chosen mechanic (real assist build-up, the strike, the keeper beaten) — e.g. 1-1.
   - **Scene 3 — "THE WINNER":** stoppage time, the hero scores the decisive goal, ending on the win + an on-screen final-score card.

3. **Scene-prompt formula (match this structure exactly — it's what makes it work):**
   - **Open with the style tag:** `Japanese anime action style, cel-shaded, high contrast, [color grade e.g. cold desaturated → blazing gold], [intensity], [setting: packed night stadium, the minute + scoreline].`
   - **Beat-by-beat action** naming the **hero in CAPS** with their **kit colors**, the exact goal mechanic, and anime camera/FX language: *extreme close-up on the eyes, low heroic angle pushing up, slow dolly-in, anime smear frames, bullet-time on the strike, impact frame flashes pure white then SNAPS to full speed, net ripples, golden particle burst, motion-blur trail, frozen goalkeeper mid-dive.*
   - **Mood line:** e.g. `brooding/determined → electric/triumphant → euphoric/explosive`.
   - **End with Japanese VO/subtitle lines**, one per speaker, prefixed by the character's name, plus a commentator — short dialogue + the hero's inner monologue. Format:
     ```
     VO/subtitle (JP): {NAME}「…」 / {NAME} (inner)「…」 / commentator「…」
     ```
   - Scene 3 also gets a **final on-screen card**: `Final on-screen card: {TEAM} {SCORE}.`

   *(Proven structural reference — the Undav/Germany edit this format is modeled on; **mirror its SHAPE exactly, swapping in YOUR hero name + YOUR team + the opponent**: Scene 1 cold-graded close-up → strides on under floodlights, a teammate shouts, hero inner-monologue. Scene 2 a cross comes in → the HERO volleys it in, bullet-time + white impact flash, 1-1, keeper frozen. Scene 3 stoppage time, the HERO turn-and-spin finish past the defender, knee-slide, gold confetti, "[TEAM] 2-1" card. Each opens with the cel-shaded style tag and closes on JP dialogue + monologue + commentator. Reuse this shape; swap in your hero + teams + the goal mechanics you designed.)*

---

## Stage 3 — Generate each scene (`generate_reference_video`, seedance)

One call per scene. Use the **character sheet as reference** and map the hero name to the image (the Higgsfield "@image" trick → Seedance `@Image1` token).

Call `generate_reference_video` with:
- `provider`: **`seedance`** · `seedance_backend`: **`ark`**
- `reference_images`: the hero sheet (plus any extra character sheets used in THAT scene) — e.g. `[sheets[HERO]]`
- `aspect_ratio`: **`16:9`** · `resolution`: **`1080p`** · `duration`: **`15`** · `sound`: **`true`** (the JP dialogue + dramatic SFX are the point here — this format KEEPS generated voice/audio)
- `prompt`: a **name→image mapping line, then the scene prompt**. Example:
  ```
  {HERO} is @Image1. <full Scene 1 prompt from Stage 2>
  ```
  Reference the hero via its `@ImageN` token where it first appears so Seedance binds the likeness.

Fire all three in parallel (`background: true`) and poll. Re-roll a scene if: the goal mechanic is wrong, the face drifts off the sheet, or the title/score card text garbles. If a scene trips `OutputAudioSensitiveContentDetected`, re-roll with a new seed (or, as a last resort, `sound: false` for that scene only and add the dialogue as an overlay).

---

## Stage 4 — Stitch

Concatenate Scene 1 → 2 → 3 in order into the final ~45s, 16:9 1080p cut (`edit_concat`, or ffmpeg concat of normalized clips). Keep each scene's generated audio. Optionally lay a subtle epic-anime music bed under it (post-only) if the user wants one. Deliver the stitched MP4 + the 3 scene clips.

---

## Settings quick-reference

| Step | Tool | Key settings |
|---|---|---|
| Character sheet | `generate_image` | **`nano-banana-pro`** (gpt-image-2 rejects real-person photos), ref = user's photo, hero in team kit, `16:9` |
| Design + prompts | you (acting as Claude) | a specific dramatic match → 3×15s scenes in the formula above |
| Scene video | `generate_reference_video` | `seedance`/`ark`, sheet as ref, name→`@ImageN` map, `16:9`, `1080p`, `15s`, `sound:true` |
| Stitch | `edit_concat` / ffmpeg | scenes in order, keep audio, ~45s |

Optional: `seedance-anime` (style help for the prompt voice) and `seedance-director` can assist with shot phrasing — but the formula above already reproduces the target look.

## Failure modes

| Symptom | Fix |
|---|---|
| Face changes between scenes | Always pass the **character sheet** (not the raw photo) as the reference on every scene; re-roll drifters; map the hero to its `@ImageN`. |
| Goal looks generic / weak | You skipped the design step — pick a **specific mechanic** (volley / header / turn-and-finish), a scoreline, kit colors, and write the strike beat-by-beat. |
| Hero unnamed / no Japanese dialogue | The formula is mandatory: name the hero in CAPS, end every scene with the `VO/subtitle (JP): …` block. |
| Score / title card text garbled | Keep card text short ("[TEAM] 2-1"); re-roll; or burn it as a clean overlay in post. |
| Audio sensitive-content trip (`OutputAudioSensitiveContentDetected`) | Re-roll seed; last resort `sound:false` for that scene + overlay the JP lines. |
| **Copyright/sensitive-content trip on the VIDEO (`OutputVideoSensitiveContentDetected`)** | A new seed alone won't clear it — it's the *content*. Walkout / ceremony / broadcast-style scenes trip it most. **De-brand the prompt:** no named tournament ("World Cup" → "a huge night stadium"), no real club crests/sponsor logos, no on-screen scoreboard / lower-thirds / broadcast graphics, no captain's armband. Describe **kit COLORS only**, keep it **pure on-pitch action** (open-play goal scenes pass first try). |
| Transient `invalid_input` / "Unknown provider: seedance-assets" / `skill_crashed` mid-job | Pika-side backend hiccup, not your input. Re-fire the same call with a new seed. If it ran past ~4 min before failing, the content already cleared the safety pass. |
| `content_policy` / `image_generation_user_error` on the character sheet | gpt-image-2 (OpenAI) blocks anime-editing a real person's photo. Use **`nano-banana-pro`** for the sheet (the default); don't retry gpt-image-2 with the same photo. |

## Notes
- Provenance: recreates the workflow shown by @stevenwommack (tutorial reel) / inspired by @leonrdewa — image-sheet → Claude prompts → Seedance 15s scenes → stitch — rebuilt entirely on the Pika MCP, generalized so the **user** is the hero (their photo + team + opponent).
- Default output: 3 scenes × 15s = ~45s, 16:9, 1080p, anime cel-shaded, Japanese VO. Aspect/length configurable if the user asks (e.g. 9:16 for reels).
