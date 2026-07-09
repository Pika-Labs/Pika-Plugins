---
name: podcast
description: >-
  Two-host podcast video for any URL or free-form topic — 1 minute, 4 acts × ~15s,
  native multi-shot dialogue, optional voice cloning for Host A. Use when the user
  asks to "make a podcast", "podcast about [thing]", "podcast review of [url]",
  "two-host explainer", "interview-style clip", "two people talking on camera",
  "I/me and X talk about Y", or "interview with [persona] about [topic]". Native
  audio is the deliverable; captions are skipped by default because podcast dialogue
  mistranscribes domain terms.
argument-hint: <url-or-topic> [bg_img=] [host_a_img=] [host_b_img=] [voice_a=] [voice_b=] [aspect_ratio=16:9]
---

# /pika:podcast

4 acts × 15s each = 60s. Host A always LEFT, Host B always RIGHT. Accepts a URL **or** a free-form topic / brief.

## Parameters

| Param | Default | Notes |
|---|---|---|
| `input` | required | URL to review **or** free-form topic / brief (e.g. "I and Elon Musk talk about Mars") |
| `bg_img` | auto-generated | Podcast studio background |
| `host_a_img` | auto-generated | Host A portrait — see Real-person handling below |
| `host_b_img` | auto-generated | Host B portrait — see Real-person handling below |
| `voice_a` | `876341503281471517` | Kling preset or cloned voice ID for Host A |
| `voice_b` | `829837252279803904` | Kling preset or cloned voice ID for Host B |
| `aspect_ratio` | `16:9` | Output aspect ratio |

## Cost transparency gate

Before any paid MCP call, call `identity_balance({verbose: true})` once. Surface the current balance, recent burn rate, and remaining runway, then gate the run with this exact message:

> Estimated cost: about 6,000-9,000 credits (~$60-$90) for four Kling v3-omni pro 15s acts, optional missing-asset image generation, one act corrective retry, concat, and post-flight analyze_media QA. This exceeds $5, so Reply `proceed` to continue or `cancel` to stop.

Do not call any paid MCP tool until the user replies `proceed`. If the user replies `cancel`, stop without generating. This is the only yes/no gate; after `proceed`, render the four acts and return the URL.

## Defaults — fire fast, no mid-flow confirmation

- **Use the param-table defaults silently for voices.** `voice_a` defaults to the Kling preset `876341503281471517` and `voice_b` to `829837252279803904`. Do **not** ask "which voice?" before firing — only honor explicit overrides (`voice_a=`, `voice_b=`).
- **Auto-generate any missing host portraits silently** (Step 1's archetype prompts). Do **not** ask "should I generate a host image?" — just generate.
- **Only the cost transparency gate asks for `proceed`.** After `proceed`, submit → render the 4 acts → return URL. Account credit balance + provider failover are the canonical guardrails. The `--yes` flag is accepted as a no-op for backward compatibility.
- **Topic-mode personas (Step 3)** — when the user names a real public figure, follow Step 4 (Real-person handling) silently: archetype portrait by default, no auto-generated photographic likeness, no question to the user about likeness rights.

## Pre-generation wall-clock guard

Start a timer at skill start once the podcast input is resolved and the cost gate has passed. The first paid generation call is `generate_image` for missing background/host assets. If all assets are already provided, the first paid generation call is `generate_reference_video`. The first paid generation call must be invoked within 5 minutes of skill start. If you have not invoked the first paid generation call within 5 minutes of skill start, stop before any paid generation call and report `failed_pre_generation_timeout` with what you have so far: input mode, asset status, voice status, URL capture/WebFetch status, script draft status, and the exact blocker. Do not keep refining host archetypes, factual grounding, jokes, or act wording.

Print a single-line progress checkpoint after each prep stage and right before the paid generation call:
- `Stage 1/4 done — input resolved and cost gate passed, locking missing-asset image prompts.`
- `Stage 2/4 done — missing asset prompts ready, calling image generation now.` Use this right before the first paid `generate_image` call when any background or host image is missing. If all images are already provided, emit `Stage 2/4 done — assets and voices ready, collecting URL/topic facts.` instead and continue without image generation.
- `Stage 3/4 done — script draft locked, preparing first act.`
- `Stage 4/4 done — first act prompt ready, calling Kling now.`

Missing-asset image prompt iteration is maximum 2 passes before the first `generate_image` call. After the max 2 passes, ship what you have to `generate_image`; do not continue polishing host archetypes, studio background details, or persona styling. Script and act-prompt iteration is maximum 2 passes before Kling. After the max 2 passes, ship what you have to `generate_reference_video`; do not continue polishing jokes, interruptions, persona framing, or camera wording.

## Local images on Claude Desktop

Claude Desktop can't pass inline-pasted images to MCP tools yet (Anthropic-side limitation). If the user pastes a photo inline, or mentions a local file they want as `host_a_img` / `host_b_img`, pause Step 1 and kindly send them this — something like:

> Heads up — pasted images don't reach MCP tools on Claude Desktop yet (Anthropic limitation). Two easy options for your photo:
>
> - **Paste a URL** if it's already hosted (Imgur, S3, your site) — fastest
> - **Attach the image file** so I can upload it before generation.

When a local file arrives, convert it to a public URL with `upload_asset` and use the returned `public_url` as the parameter before Step 1. Already-hosted `https://...` URLs work as-is and skip this entirely.

If the user names a real public figure without attaching anything, do NOT auto-generate their likeness — Step 4 (Real-person handling) uses an archetype portrait instead.

## Long-running task_status polling

When any long-running generation or edit call returns a `task_id` with or without an initial status, including `{task_id}`, `{task_id, status: "queued"}`, or an initial `queued`, `running`, or `processing` status, record the task id and start time immediately.

- Call `task_status({task_id})` in a tight loop until terminal (`completed | failed | cancelled`). No manual sleep and no Bash polling; the worker holds each status call open.
- Emit ONE visible progress line every 60s while status is `queued`, `running`, or `processing`: `Seedance i2v queued for {N}m {S}s... still processing`. Replace the provider/stage label when polling Kling, image generation, clone voice, or concat tasks.
- On `completed`, unwrap the returned result URL and continue.
- On `failed` or `cancelled`, surface failure to the user with `task_id`, status, and the last status message.
- After 15 min total from the original submit, call `task_cancel({task_id})` if the task is still non-terminal, then surface failure to the user. If cancel reports the task is already terminal, call status once more and report that terminal result.
- Do not submit a duplicate request while the original task is still `queued`, `running`, or `processing`.

## Steps

### 0. Resolve input (empty-args menu)

Strip flags (`--yes`, `--no-captions`, etc.) and `key=value` parameters from `$ARGUMENTS`. **If what remains is empty or whitespace-only**, print this menu **verbatim** as your full response, then **stop and wait for the user's next message** — do NOT call any tool, do NOT proceed to Step 1, do NOT invent a topic or URL. If the stripped input is non-empty (a URL or any prose), skip this step silently and proceed to Step 1.

> **What would you like a podcast about?** I can take any of:
>
> - **A website URL** (product page, docs site, launch page) — e.g. `https://pika.art`
> - **A GitHub repo** — e.g. `https://github.com/anthropics/claude-code`
> - **A blog post / article URL** — e.g. a recent piece you'd like discussed
> - **A free-form topic or brief** — e.g. *"I and Elon Musk talk about Mars"* or *"two scientists debate AGI"*
>
> Reply with your choice and I'll generate a 1-minute two-host podcast video (4 acts × ~15s).
>
> *Tip: you don't need to type `/pika:podcast` — just say things like "make a podcast about <topic>", "podcast review of <url>", or "I and <persona> talk about <topic>" and I'll fire this skill automatically.*

When the user replies, treat their reply as the resolved input (URL or topic) and proceed to Step 1. Do not re-prompt.

### 1. Generate missing assets (parallel)

Generate only what's not provided. Default archetype prompts:
- `bg_img` — modern podcast studio, two chairs, warm lighting, no people, 16:9
- `host_a_img` — enthusiastic host, studio portrait, left-side framing, 1:1
- `host_b_img` — pragmatic skeptic host, studio portrait, right-side framing, 1:1

If the input mentions specific personas (Step 3), tune the archetype to match the persona vibe — see Real-person handling below.

### 2. Resolve voice IDs

Use `voice_a` / `voice_b` as given; otherwise fall back to the default Kling presets (`876341503281471517` / `829837252279803904`). If the user supplied a cloned voice ID via `voice_a=` / `voice_b=`, use it directly.

### 3. Parse input mode — URL vs topic

Strip flags (`--yes`, `--no-captions`, etc.) and key=value parameters from `$ARGUMENTS`. Inspect what remains.

**URL mode** — input contains a `https?://` URL:
- Call `capture_website` on the URL for visual grounding only: product/page name, visible layout, screenshots, b-roll cues, and one jokeable visual detail.
- Call `WebFetch` on the same URL and use its full-page text as the script source of truth. Do not rely on the screenshot alone for facts.
- Extract from the combined inputs: product name, value prop, 2–3 specific features or facts, pricing, one jokeable detail, and any concrete quotes or claims.
- For long-form pages (Wikipedia, docs, blog posts, or articles), scan the WebFetch full-page text for deep sections beyond the lede. When at least 3 substantive deep sections are present, the script must mention at least 3 distinct sections beyond the lede (for example architecture, training, hallucinations, limitations, deployment, or safety), not just the opening summary.
- Use WebFetch text for factual anchors and `capture_website` for visuals. If they conflict, prefer WebFetch for factual claims and treat the screenshot as a visual reference.

**Topic mode** — input is free-form prose (no URL):
- Treat the whole input as the brief. Parse for:
  - **Subject** — what the conversation is about
  - **Hosts** — explicit if mentioned ("I and Elon Musk", "two scientists", "Joe and Sarah"); otherwise use defaults (enthusiastic host + skeptic host)
  - **Angle** — debate / interview / explainer / casual
  - **Concrete facts** — any specific claims, numbers, dates, quotes the user gave
- If no concrete facts are given, use **2–3 clearly framed observations or hypotheses** to anchor jokes and the "wait, actually..." pivot. Do not present invented claims as facts; if factual accuracy matters for the topic, ask for a source or URL.
- If the user says "I and X" or "me and X", Host A = the user (represented by `host_a_img=` if supplied, else a generated host portrait) and Host B = X.

### 4. Real-person handling (topic mode only)

If the parsed input names a specific real public figure as a host (e.g. "Elon Musk", "Taylor Swift", "Joe Rogan"):

- **Default behavior**: do NOT auto-generate that person's photographic likeness. Generate an **archetype portrait** matching the persona vibe — e.g. "tech-billionaire-energy CEO at a podcast desk" for an Elon-style host, "pop-star aesthetic" for a Taylor-style host. Clearly inspired-by, not impersonation.
- **Override**: if the user explicitly provides `host_a_img=<url>` or `host_b_img=<url>`, use the provided image as-is. The user takes responsibility for likeness rights.
- **Voices**: same logic — default to a generic Kling preset; only use a cloned voice when the user provides one (`voice_a=` / `voice_b=`).
- **Script tone**: the dialogue can riff on the named persona's known public positions or vibe (e.g. Mars enthusiasm for Elon-style) — public-record opinions are fair game. Do NOT put specific defamatory, off-character, or fabricated-private-life statements in their mouth.

This guardrail keeps the skill creative ("I want a podcast where I argue with a tech CEO about Mars") without auto-generating deepfakes of named real people.

### CJK / non-Latin handling

Use this section when the URL, topic, product name, host name, quote, or required script detail includes Chinese, Japanese, Korean, Arabic, Devanagari, Cyrillic, accented Latin, emoji, or any other non-Latin text.

- **Script preservation**: preserve user-supplied non-Latin characters exactly in the script state and in any factual recap. Do not romanize, transliterate, or translate product names, person names, slogans, or quoted phrases unless the user explicitly asks. If a pronunciation aid is useful, put it in nearby English prose, not as a replacement for the original characters.
- **Kling voice IDs**: `voice_a=` and `voice_b=` must still be valid Kling voice IDs. For Chinese / Japanese / Korean dialogue, prefer a Kling voice ID or cloned voice sample known to speak that language; if no language-matched Kling voice is available, keep the original characters in the dialogue and surface that pronunciation may be accented instead of silently swapping to an unrelated TTS provider.
- **Mixed-language dialogue**: keep each host's line short and unambiguous. Avoid asking Kling to pronounce long mixed-language paragraphs; split complex names or quotes across acts and keep surrounding English simple.
- **Captions / font fallback**: this skill skips `add_captions` by default because podcast dialogue mistranscribes jargon. If the user explicitly asks for captions anyway, pass manual `subtitles[]` from the authored script rather than auto-transcribing, set `font: "noto-cjk"` for Chinese / Japanese / Korean, and preserve the original non-Latin text exactly.
- **QA**: before delivery, include a one-line note in the final verdict when non-Latin text was present: whether original characters were preserved in the script and whether the selected voices were language-matched or best-effort.

### Jargon-heavy native audio handling

Use this section when the URL, topic, product name, quote, or required script detail is domain-heavy or jargon-heavy, especially finance, law, medicine, AI/crypto, acronyms, coined terms, unusual product names, long numbers, or multi-word compounds. Kling-omni native TTS can garble coined terms in the spoken native audio, not just in auto-captions, so reduce the risk before the paid Kling calls.

- **Risk scan**: mark the run jargon-heavy when a line would contain several domain-specific terms, acronyms, long numbers, or nested / multi-clause economist-style phrasing. Treat examples like stablecoins, unbundle, and reassure as load-bearing terms that must remain intelligible.
- **Script rewrite**: preserve the canonical term in the script state and final recap, but shorten the spoken line around it. Use short lines, split long clauses, keep at most one or two high-risk terms per host line, and avoid nested clauses that make Kling infer similar-sounding filler words.
- **Pronunciation aid**: create a small per-act pronunciation aid for high-risk terms, for example `stablecoins = STAY-bul coins`, `unbundle = un-BUN-dul`, `reassure = ree-uh-SHOOR`. The pronunciation aid is prompt metadata only; do not replace the canonical term in the dialogue, captions, facts, or final recap.
- **Known-hard-term correction**: if a term is known to drift, or post-flight localizes a near-neighbor mishearing, do not retry the same standalone hard word. Keep the canonical term in act metadata (`canonical_terms: ["unbundle"]`), then make the corrected voice-token line a short context phrase with a speakable cue / micro-pause, for example `we un-bundle payments`. Add the observed wrong form as a negative pronunciation guard in metadata, for example `unbundle = un-BUN-dul, not un-bumble`.
- **Known-hard publishable fallback**: before the paid Kling calls, mark observed hard terms such as `unbundle` as known-hard when prior E2E or the current post-flight findings show drift like `unbundle` -> `unbubble`, `un-bumble`, or `unbundable`. Record `canonical_terms` and `observed_wrong_forms`. Do not render known-hard spoken terms with Kling native audio. Instead, generate the affected visual act or final video with no spoken known-hard term in the native voice-token lines, then generate controlled narration with `generate_speech(text=<spoken-only script>, provider: "minimax-tts", minimax_model: "speech-2.8-hd", language: "en")` using the canonical spelling (`unbundle`, not the hyphen cue). The spoken-only script must preserve the authored host-turn order but contain no HOST_A/HOST_B labels, no metadata, no pronunciation aids, and no observed wrong-form spellings. Run pre-replacement QA on the TTS audio with both `transcribe_audio(audio=<tts_audio_url>)` and `analyze_media(media=<tts_audio_url>)`; every required `canonical_terms` entry must appear in the `transcribe_audio` text and must appear in the `analyze_media` observed transcript. Reject the TTS if a canonical term is missing, replaced by any observed wrong form, or replaced by a new near-neighbor. Then call `edit_audio_replace(video_url=<final_mp4>, audio_url=<tts_audio_url>, duration_policy: "video")` to discard the native audio and replace it with the controlled TTS track. Run post-replacement QA on the replaced MP4 with both `transcribe_audio(audio=<replaced_mp4_url>)` and `analyze_media(media=<replaced_mp4_url>)`; every required `canonical_terms` entry must appear in both final checks, and `analyze_media` must also verify host-turn order and acceptable audio/video sync. If any final check hears a wrong form, misses a canonical term, or says the fallback collapses the podcast turn structure, return `not publish-ready`; if both checks pass, the fallback output is publish-ready even though it uses controlled TTS instead of Kling native speech.
- **Numbers and acronyms**: write spoken-friendly forms when they matter: `$175B` becomes `one hundred seventy-five billion dollars`; `API` becomes `A P I` unless the brand normally says it as a word.
- **Act prompt**: include the per-act pronunciation aid near the voice-token lines with an instruction that it is not dialogue and should not be spoken verbatim. Ask for clear pronunciation of the canonical terms and no improvising similar words.

### 5. Write script

Write 4 acts × 2 lines (HOST_A / HOST_B). Each line ~10–12s of spoken dialogue.

**Required (apply to both URL and topic modes):**
- One specific joke tied to a concrete detail (scraped fact in URL mode; topic-derived claim in topic mode)
- One "wait, actually..." skeptic-flip moment
- At least one mid-sentence interruption
- Natural filler: "okay so", "wait", "right?", "i mean", "honestly"
- Real reactions, not generic praise
- Reference at least one actual feature name, price, claim, or quote
- Natural ending — no forced "bye!"
- Apply Jargon-heavy native audio handling before finalizing the act lines when the topic is domain-heavy, jargon-heavy, or uses coined terms.

Acts: Hook → Feature deep-dive → The Turn → Verdict
(In topic mode the analogue: Hook → Substance → The Pivot → Verdict.)

### 6. Generate video acts (subagent, sequential)

Delegate to a subagent with all resolved assets and the script. The subagent runs acts 1→2→3→4 sequentially — do NOT parallelize. The subagent must follow the Long-running task_status polling contract above and relay every 60s progress line back to the parent while it is waiting on Kling, image generation, voice clone, or concat tasks.

Each normal act: one `generate_reference_video` call (`kling-v3-omni`, `duration=15`, `sound=true`, `quality_mode: "pro"`). Pass `reference_images=[bg_img, host_a_img, host_b_img]`, `voice_ids=[voice_a, voice_b]`, and `quality_mode: "pro"` on every normal act; this must pass `quality_mode: "pro"` because the cost gate quotes the pro-tier 15s act cost. Optional knob: `kling_model` to pin a specific kling family member if you need reproducibility across runs. Three shots:

- **Known-hard fallback exception**: for acts containing known-hard spoken terms, render the affected visual act with `sound=false` and no voice tokens for the affected lines. Do not include canonical known-hard terms in any `<<<voice_*>>>` native voice-token line; the controlled TTS replacement supplies those words later. For jargon-heavy but not known-hard acts, include the per-act pronunciation aid from Step 5 in the act prompt as non-dialogue metadata and preserve canonical terms in the quoted `<<<voice_*>>>` lines.
- Wide 5s: both hosts, no voice token
- MCU-A 5s: `<<<voice_1>>> '<HOST_A line>'`
- MCU-B 5s: `<<<voice_2>>> '<HOST_B line>'`

Emotional beats per act:
- Act 1: A excited, B skeptical
- Act 2: A gesturing/explaining, B questioning
- Act 3: A firm, B surprised and reconsidering
- Act 4: A satisfied, B conceding

After act 4, subagent calls `edit_concat([act1, act2, act3, act4])`, relays any async polling progress to the parent, and returns the final video URL. Keep the four act URLs in state so the post-flight quality gate can spend at most one targeted act correction without regenerating clean acts.

### 7. Output

Return the final video URL and a one-sentence verdict. **Do not call `add_captions` by default** — Whisper auto-transcription is unreliable on the domain-specific terms typical of podcast dialogue (product names, persona names, technical jargon). If the user explicitly asks for captions, pass manual `subtitles[]` from the authored script rather than auto-transcribing; for CJK / non-Latin text, follow the font and preservation guidance above. Native Kling Omni audio is the default deliverable.

## Post-flight quality gate

Before declaring success, call `analyze_media` on the final video URL and ask for a structured verdict:

```
Return JSON only: {
  "verdict": "clean" | "degraded" | "catastrophic",
  "observations": string[],
  "quality_warning": string | null,
  "re_roll_suggestion": string | null
}
Check that Host A remains on the left, Host B remains on the right, product names / persona names / topic-specific terms are not visibly garbled, the four-act podcast structure is present, and there are no black frames or wrong-host shots.
Also check the spoken audio, not only captions or visible text: product names, persona names, topic-specific terms, coined terms, and jargon must be intelligible. Flag garbled or mispronounced native audio such as "stablecoins" sounding like "stable kinds", "unbundle" sounding like "un-bumble" or "unbundable", or "reassure" losing syllables.
```

- If `verdict` is `clean`, first check whether the script state contains a known-hard spoken term. For known-hard terms, before accepting a clean verdict, run the Known-hard publishable fallback and its pre-replacement plus post-replacement `transcribe_audio` / `analyze_media` checks. Only return success after the replaced MP4 checks pass. If there are no known-hard spoken terms, return the final URL and one-sentence verdict normally.
- If `verdict` is `degraded` for ordinary non-blocking visual issues, return the final URL plus the `quality_warning` so the user can review before publishing.
- If `verdict` is `degraded` because spoken audio garbles jargon, coined terms, or other domain-specific terms, treat it as not publish-ready instead of silent success. For a known-hard term or observed hard-term drift, skip the native-audio act correction; do not spend the targeted act correction budget on another Kling native-audio prompt. Use the Known-hard publishable fallback directly: call `generate_speech(text=<spoken-only script>, provider: "minimax-tts", minimax_model: "speech-2.8-hd")`, run pre-replacement `transcribe_audio` and `analyze_media` on the TTS audio, then call `edit_audio_replace(video_url=<final_mp4>, audio_url=<tts_audio_url>, duration_policy: "video")` to discard the native audio and replace the final MP4 audio. Run post-replacement `transcribe_audio` and `analyze_media` on the replaced MP4. If those checks pass, return the replaced URL; if the fallback checks still report spoken jargon garble, or if the garble is not localized enough to correct or replace, do not call the podcast complete; return the URL with `not publish-ready`, affected terms, and the `quality_warning`. For non-known-hard garble only, if the observations or `re_roll_suggestion` localize the problem to one act, spend the one targeted act correction budget: materially change that act payload by shortening the affected line, splitting multi-clause wording, adding or refining the phonetic pronunciation aid, changing the shot prompt, reference image, voice ID, or other stage-specific input that caused the failure. Submit one corrected act with `quality_mode: "pro"`, re-concat the four acts, and run this analyze_media check one more time. If the second verdict still reports spoken jargon garble, do not call the podcast complete; return `not publish-ready`.
- If `verdict` is `catastrophic`, spend the one targeted act correction budget only when the observations or `re_roll_suggestion` identifies a single bad act, wrong-host shot, black frame, or localized visual/audio failure. kling-v3-omni has no seed, and identical act payloads can resolve to the same job/asset. Do not submit an identical Kling payload. Before retrying, materially change the bad act payload by adjusting the script line, shot prompt, reference image, voice ID, pronunciation aid, or other stage-specific input that caused the failure. Submit one corrected act with `quality_mode: "pro"`, re-concat the four acts, and run this analyze_media check one more time. Do not exceed the cost-gate range: if the second verdict is still `catastrophic`, or if the failure is not attributable to one act, do not call the podcast complete; surface the verdict and `re_roll_suggestion` instead of declaring success.

---

**Rules:**
- `voice_ids` must be valid Kling voice IDs — never use name-style strings like `Calm_Man`
- Host A always LEFT (`<<<image_2>>>`), Host B always RIGHT (`<<<image_3>>>`) — never swapped

## Load-bearing phrases

These anchors keep the podcast output coherent across URL and topic modes:

| Phrase | Where | Why load-bearing |
|---|---|---|
| `Host A always LEFT, Host B always RIGHT` | Layout and shot prompts | Prevents host identity swapping across the four separate act renders. |
| `4 acts × 15s each` | Overall structure | Keeps the concat predictable and avoids uneven act pacing. |
| `Hook → Feature deep-dive → The Turn → Verdict` | Script structure | Gives the episode a conversational arc instead of four disconnected reactions. |
| `wait, actually...` skeptic-flip moment | Script requirements | Creates the pivot that makes the podcast feel like a real exchange. |
| `Do not call add_captions` | Output rule | Avoids low-quality burned captions by default; explicit caption requests use manual `subtitles[]` and font fallback instead of auto-transcription. |

## Engine choice: Kling v3-omni for native two-host dialogue

Use Kling v3-omni for the four acts because it supports native dialogue with two reference hosts and voice tokens in a single shot plan. The tradeoff is that acts run sequentially for consistency and can take longer than pure edit/composite flows. Do not add a separate caption or music layer by default; the value of this skill is the native spoken exchange.

## Runtime expectations

Typical wall-clock is 24-32 minutes for the full 4-act render: ~25 min realistic, ~32 min P95.
The 4 acts run sequentially through Kling Omni; this is the dominant runtime and should not be described as parallel work.
If the user or execution harness has a tight budget below 32 min, warn upfront that the full render may not finish and offer a 2-act / 30s fallback. Otherwise keep the normal no-confirmation flow.

| Step | Wall clock | Notes |
|---|---:|---|
| Missing asset generation | 30-90s | Skipped for provided background/host refs |
| URL/topic parse + script | 1-3 min | URL mode depends on page fetch quality |
| Four Kling acts | 24-32 min | 4 × ~8 min sequential Kling Omni calls; dominant cost |
| Concat + return | 30-90s | Final URL only; captions skipped by default |

## Failure modes

### Recovering from upstream 5xx on capture_website / clone_voice / generate_video / edit_concat

If any MCP call returns:
- `code: "provider_5xx"` AND `retry_class: "retry_after_backoff"`
- Or HTTP 502 / 503 / 504 from any upstream provider (Kling, voice clone, capture, storage)

Do this:
1. Wait 5 seconds.
2. Re-call the exact same MCP tool with the exact same arguments. Do not rewrite the script, change voices, change host refs, change act order, or resubmit a different prompt.
3. If the retry also fails with 5xx, abort and surface to the user: "Provider returned a transient upstream error twice. Try again in 1-2 minutes; this usually clears on its own."

Do not retry more than once. A 5xx is a transient outage, not evidence that the podcast topic, voices, or script are wrong.

### Recovering from upstream 4xx / moderation_blocked

If an upstream 4xx or `moderation_blocked` occurs on an optional `generate_image` helper, host asset, or Kling act:
1. Do NOT retry the same input; moderation and most 4xx validation failures are deterministic.
2. Use a fallback provider only if one is explicitly available for that stage. For the default Kling v3-omni two-host act path, no equivalent fallback provider exists; do not fake the podcast with unrelated captions or single-voice TTS.
3. Surface to the user: "Provider declined this podcast input. Try a different host reference, less recognizable public figure/brand wording, or a safer topic angle."

### Recovering from upstream 429 (rate limit)

If any upstream returns HTTP 429 with a backoff hint:
1. Wait the hinted backoff, or 30 seconds if no hint is provided.
2. Re-call the exact same MCP tool with the exact same arguments.
3. Do not retry more than once. If it still returns 429, abort and surface the rate-limit message.

### `capture_website` returning empty / page-not-loaded

If URL mode calls `capture_website` and it returns 200 but `action_bboxes` is empty or `recording_viewport` is 0x0:
1. Do NOT retry `capture_website`; the page failed to render in the capture environment.
2. If `WebFetch` returned usable full-page text, continue without retrying `capture_website`: use WebFetch for factual anchors and use a generic visual or generated visual instead of pretending the broken capture contains page details.
3. If both capture and WebFetch fail to expose usable source material, surface: "Could not capture <url>. The page may be blocked / paywalled / require auth. Please provide a text brief or paste the source material instead."

If the captured page is visibly only above-the-fold navigation with no article/content body, continue only if `WebFetch` returned enough full-page text to ground the script; in that case use the capture for visuals and WebFetch for facts. If both capture and WebFetch fail to expose usable source material, ask for pasted source material rather than hallucinating deep-page details.

### `upload_asset` network / auth failure

If `upload_asset` fails while converting local host refs, voice samples, or source media to hosted URLs, do not continue with local filesystem paths. Retry once only for the 5xx or 429 classes above. For `auth_error`, unsupported MIME, network failure, or repeated upload failure, ask for a hosted URL or a supported replacement file.

### Long-running `task_status` exceeding ceiling

Each async MCP call returns either an inline result or `{task_id, status}` for polling. Use these ceilings before deciding a task is stuck:
- Kling Omni act: 15 min per call
- Voice clone: 5 min per call
- Edit/concat: 5 min per call

Use whichever is earlier: the provider's ceiling x 1.5 or any skill-specific hard polling cap, including the 15 min total cap in the Long-running task_status polling contract above. If `task_status` returns `status: "processing"` or `status: "queued"` past that earlier limit, call `task_cancel({task_id})` and surface: "Provider taking unusually long; aborting. Try again."

## Examples

URL mode (review a website / repo / blog):

```
/pika:podcast https://pika.art
/pika:podcast https://github.com/anthropics/claude-code
/pika:podcast https://cursor.com voice_a=876341503281471517
```

Topic mode (free-form brief):

```
/pika:podcast Two AI researchers debate whether AGI arrives before 2030
/pika:podcast I and a Mars-obsessed tech CEO talk about colonization timelines
/pika:podcast interview with a seed-stage VC about what kills most startups
/pika:podcast podcast about quantum computing breakthroughs in 2026
```

Mixed (URL inside a topic prompt — agent prefers URL mode if a valid URL is found):

```
/pika:podcast podcast about https://pika.art with skeptical investor energy
```
