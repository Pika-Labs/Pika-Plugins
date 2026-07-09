---
name: build-a-brand
description: >
  Build a practical brand identity from any input — an idea, an existing website, a list of
  reference brands, product photos, or "I want to rebrand X". Default to a fast quick-brand
  path for founder-kit users, and offer the full 14-16-page guidelines as an opt-in upgrade. Use
  when someone wants a brand identity but does NOT need a full commerce launch (no Shopify,
  no product listings, no social posting).
  Trigger phrases: "build me a brand", "make me a brand", "design a brand identity", "brand
  guidelines for [X]", "i want a brand book", "create a brand from scratch", "brand for [idea]",
  "i want a brand that feels like [X] + [Y]", "rebrand my [thing]", "visual identity for [thing]",
  "build-a-brand".
argument-hint: <idea-or-url-or-reference-brands> [photos=<paths-or-urls>] [refresh=<existing-brand>] [--quick] [--full] [--config <path>]
required-capabilities:
  - generate_image
  - task_status
  - identity_balance
---

# Build a Brand

> Tools below are **Pika MCP** tools, named bare — call each under whatever prefix your session exposes for the Pika MCP.

Take any input — an idea, a website, a list of reference brands, product photos, or an existing brand to refresh — and produce a usable brand identity.

This is a standalone brand-building workflow focused on strategy, identity, design, and copy. The default output is a **quick brand deliverable** that can be finished in minutes. The full 14-16-page brand guidelines PDF is still available, but only when the user explicitly asks for full depth or chooses to go deeper after the quick pass.

## Reference files

Load these only when the relevant phase starts:
- `references/brand-directions.md` — strategy angle structure and differentiated positioning boards.
- `references/brand-identity.md` — logo pipeline, symbol rules, concept lanes, and board-copy budgets.
- `references/brand-guidelines.md` — full guidelines layout, render contract, page structure, and QA rules.
- `references/brand-md-template.md` — required machine-readable `brand.md` structure.

## Execution Model — Local First, Cloud Only Where Needed

This skill is local-first. Keep deterministic production work on the user's machine:
- **Local:** workspace setup, downloaded fonts, generated image files after download, image compression, transparent-background cleanup, 16x16 favicon tests, HTML/CSS page builds, PDF rendering, PNG/JPG QA screenshots, logo asset assembly, token/prompt files, and final zip packaging.
- **Cloud:** paid generation only (`gpt-image-2` for symbols, mood images, photography, illustration, and ambient textures) and URL/source research when the brief requires it.

Do not use a cloud PDF renderer or upload PDFs by default. Save quick PDFs, board PDFs, guidelines PDFs, and brand-kit zips to `~/Desktop` on Mac, or the project working directory when Desktop is unavailable. Only upload/share via CDN if the user explicitly asks for a hosted file.

**PDF asset hygiene:** never embed full-size gpt-image-2 PNGs directly in board or guidelines PDFs. This previously produced huge PDFs and `ASSET_FETCH_TIMEOUT` failures when renderers tried to fetch multi-MB CDN images. Download every generated image, down-raster/downsample it to the slot size, and save a local JPEG target of about 85-180KB before using it in render HTML. Keep transparent PNG only for logo/symbol source assets and favicon/logo export, not for photographic page imagery. **Never put a CSS `filter:`/`backdrop-filter:` (warm grade, sepia, saturate, brightness, blur) on a photo or `background-image` in the render HTML** — it forces Chromium to rasterize that element to a full-resolution *lossless* bitmap in the PDF, which cancels out the JPEG step above and re-bloats the file (a warm-graded mood-board page alone took a deck to 70 MB). Bake any color grade into the JPEG itself (in the gpt-image-2 prompt or when you `img.save(..., 'JPEG', ...)`); `drop-shadow()` on a transparent logo PNG is the only filter that's safe.

## Cost transparency gate

Before any paid MCP call, call `identity_balance({verbose: true})` once. Surface the current balance, recent burn rate, and remaining runway, then gate the selected depth with this exact message:

> Estimated cost: about 100-300 credits (~$1-$3) for quick brand, or about 900-1,500 credits (~$9-$15) for full brand book. These ranges cover gpt-image-2 symbol / mood / touchpoint generation plus one targeted regeneration for failed image QA. Quick brand is usually below $5; full brand book exceeds $5, so Reply `proceed` to continue or `cancel` to stop.

Do not call any paid MCP tool until the user replies `proceed`. If the user replies `cancel`, stop without generating. For non-interactive `--quick`, `--full`, or `--config` callers, require `cost_ack=proceed` in the config or invocation metadata; if it is absent, stop with the estimate instead of spending credits.

## Depth Modes

Choose the depth before any long-running generation or render work:

1. **Quick brand (default)** — use for first-time founder-kit runs, `--quick`, creator tutorial flows, batch/subagent calls, or any user who asks for a brand without explicitly asking for a full brand book. Target: 8-12 minutes after usable input, excluding user reply time; no more than 4 generated images unless QA fails; one quick PDF render plus one QA rerender when needed.
2. **Full brand book (opt-in)** — use only when the user asks for "full", "brand book", "brand guidelines", "14-16-page", "15-page", `--full`, or when they approve the quick path's "go deeper" upgrade. Target: 25-45 minutes after choices are locked, excluding user reply time.

The quick brand is not a partial or failed full guidelines deck. It is a deliberately smaller deliverable with its own completion criteria. If the selected mode is full, all full-guidelines completion gates still apply.

## Mode Selection

### Stage 0 — Intake (empty-args menu)

If invoked with no input (no idea, no URL, no photos, no reference brands, and no relevant prior context in the conversation), print this menu verbatim as your full response and stop. Do not call any tool. Wait for the user's next message.

> **What are we branding?** Paste any of:
>
> - **An idea / description** — e.g. "a streetwear label for cat people"
> - **A website URL** — e.g. "rebrand my existing site at example.com"
> - **Product photos** — drop them in the chat
> - **Reference brands** — e.g. "I want something that feels like Aesop + Patagonia"
> - **An existing brand to refresh** — name + what's working / what isn't
>
> I'll start with a quick brand by default. Say **full brand book** if you want the deeper 14-16-page guidelines path.

If the user already dropped one of the above, skip the menu and proceed to the selected mode: Quick Step 1 for the default quick brand path, or Step 1 below when full brand book mode is selected.

### Stage 0.5 — Quick brand and non-interactive fast lane

Use quick brand mode when the caller passes `--quick`, omits an explicit full-depth request, or states they are running from CI, a subagent, a batch job, a tutorial recording, or any other non-interactive harness.

Use full brand book mode only when the caller passes `--full`, sets `mode: "full"` in config, explicitly asks for full guidelines / brand book depth, or approves the post-quick "go deeper" upgrade.

This section has precedence over the interactive ask/wait instructions below.
When quick mode applies, use the quick brand workflow below and do not fall
through to the multi-turn full-workflow intake unless a required input is truly
missing.

- `--config <path>` points to a JSON file that pre-bakes intake answers:
  `input`, `photos`, `reference_brands`, `audience`, `positioning`, `assets_to_keep`,
  `references`, `mode`, `chosen_direction`, `chosen_identity`, and `export_kit`.
- `--quick` means quick brand mode. Use model judgment for all confirmation gates.
  Ask only if the original input is missing entirely; otherwise infer reasonable
  defaults, choose the strongest strategy direction and identity option, and
  continue.
- `--full` means full brand book mode. Still use model judgment for confirmation
  gates in non-interactive runs, but do not cut the required 14-16-page guidelines.
- For `--quick` or `--config`, do not stop for confirmation at the deliverable
  preview, strategy-direction choice, identity-option choice, or brand-kit
  export gate. Record the assumption inline, then proceed.
- If a required asset is unavailable and cannot be inferred from the input,
  stop once with a single compact missing-fields list instead of starting a
  multi-turn Q&A loop.
- In quick mode, deliver the quick brand package defined below; do not describe
  it as a condensed full guidelines deck.
- In full mode, do not deliver a condensed or partial brand output just because
  the caller is non-interactive or the run is short on wall-clock time. A
  condensed 6-page deck is not an acceptable substitute for the required
  14-16-page guidelines. If the run is out of wall-clock budget, save a resumable
  checkpoint with the pages/assets already completed and stop; do not mark the
  workflow complete.

**Autonomous full mode:** use this only when an explicit full-depth request is present (`--full`, `mode: "full"`, or the user asks for a full brand book / full guidelines) and the run already has `cost_ack=proceed`. In that case, the brief is the spec. Do not wait for the user to pick a board and do not wait for explicit user approval before kit export. Produce all three full deliverables in one run:

1. `brand-boards.pdf` — generate all three boards and use model judgment to choose the strongest board or hybrid.
2. `brand-guidelines.pdf` — build the full 14-16-page guidelines from that chosen direction.
3. `brand-kit.zip` — export the complete kit after the guidelines pass QA.

Record the assumptions and selected direction in `brand.md` and the final response. If the brief is ambiguous enough that the board choice would be arbitrary, stop once with the missing decision instead of pretending the run is autonomous. Non-interactive clear briefs without explicit full depth stay quick; never promote a batch/tutorial/founder-kit run to full solely because the brief is clear.

## Quick Brand Workflow (Default)

Use this workflow for quick brand mode. It is the founder-kit fast lane: fewer choices, fewer generated assets, and a complete starter brand that can feed downstream skills without burning a full first-run quota.

### Quick Step 1 — One-pass intake

If there is usable input, do not start a long questionnaire. State the assumptions you are using and ask at most 3 compact questions only when the answer would materially change the brand:

- What does this sell or do?
- Who is it for?
- Should I preserve any existing name, logo, colors, fonts, photos, or references?

For `--quick`, `--config`, CI, subagent, batch, or tutorial-recording flows, do not wait for these answers unless the original input is missing entirely. Infer reasonable defaults and record them in the output.

### Quick Step 2 — Choose one strongest direction

Do not present 2-3 directions or 3 identity options in quick mode. Pick one strongest strategy and identity with model judgment. The quick strategy must still include:

- Brand name or kept name
- Tagline (8 words max)
- Audience segments: primary segment, secondary segment(s), and one anchor persona
- Positioning statement
- Assets being kept
- Reference brands / inspirations, if provided

### Quick Step 3 — Build the starter identity

Create one coherent identity system:

- Logo concept: wordmark + standalone symbol/mark + lockup plan. For a new symbol, use `generate_image` with `provider="gpt-image-2"` and ship the approved symbol as transparent PNG sizes, not SVG. Wordmark and lockup assets may be SVG because the wordmark is converted from real font text to outlined paths.
- Palette: 4 core colors with roles and hex values.
- Typography: one characterful display font plus one practical body font, with Google Fonts URLs when available.
- Voice: 3 tone principles, 3 sample lines, and 5 forbidden words/phrases.
- Imagery direction: one short photo/illustration rule set plus no-text image prompt guardrails.
- Starter applications: social avatar/app icon, simple web hero direction, and one practical touchpoint appropriate to the brand type.

Keep image generation capped: one symbol/mark image plus up to 3 mood or touchpoint images. Retry budget: each generated brand image asset gets at most 2 total generation attempts (initial attempt + one targeted regeneration). If QA fails, regenerate only the failed asset. After either cap is exhausted, stop and ask the user which failed asset or layout issue they want to relax instead of continuing to spend credits.

### Quick Step 4 — Deliver the quick brand package

The quick deliverable must be complete enough for a creator to use immediately:

```
[brand-name]-quick-brand/
├── quick-brand.pdf              # 3 pages: cover/strategy, identity system, starter applications
├── brand.md                     # compact machine-readable brand spec
├── README.md                    # how to use the quick brand and when to upgrade
├── logo/                        # symbol, wordmark, and lockup assets that were produced
├── tokens/
│   ├── tokens.css
│   ├── tokens.json
│   └── tailwind.config.snippet.js
└── prompts/
    ├── system-prompt.md
    └── imagery.md
```

The 3-page `quick-brand.pdf` page structure:

1. **Cover + Strategy** — brand name, tagline, positioning, audience segments, anchor persona, references, and hero visual.
2. **Identity System** — logo system, palette, typography, voice rules, and imagery rules.
3. **Starter Applications** — social avatar/app icon, web hero/social card direction, one real touchpoint or product-context image, plus 3 brand-specific dos and 3 don'ts.

Render `quick-brand.pdf` locally with Chrome headless (or WeasyPrint when the HTML is written for it) and inspect PNG/JPG previews before delivery. Quick visual QA must catch clipped text, missing logo/symbol, unreadable type, baked-in text inside generated images, empty placeholders, and obvious layout collisions. If the quick package or zip cannot be produced, stop with a resumable checkpoint listing completed files, missing files, asset paths/URLs, and the exact blocker.

After delivering quick brand, offer the full 14-16-page guidelines as a "go deeper" upgrade. Do not start the full workflow unless the user explicitly asks.

## Full Brand Book Workflow (Opt-in)

Use this workflow only for full brand book mode.

### Step 1 — Read the Input

Full brand book mode only.

Inputs vary. **Before asking any questions, open with a brief agenda** so the user knows what's coming:

```
here's how this works — 4 steps:
1. **Read the input** — i ask a few questions, you answer, i play back what i'm hearing
2. **3 visual brand boards** — i build a 3-page PDF with three complete brand directions, each with its own colors, fonts, photography, voice samples, and logo concept. you pick one or mix elements.
3. **Build the guidelines** — full 14-16-page brand book PDF for the chosen board
4. **Export the brand kit** — once you're happy with the guidelines, i'll bundle a `brand.md` spec + logo assets (symbol PNG sizes, wordmark SVG/PNG, lockup SVG/PNG) + fonts + tokens + AI prompts as a zip you can use anywhere

let's start. [questions follow]
```

Then ask 3-5 targeted questions in a single message. Adapt to the input type:

**If they dropped an idea / description:**
- What does this brand sell or do? (product / service / app / community / something else)
- Who is this for — describe the 2-3 audience segments this brand should serve, plus one vivid anchor persona inside the primary segment
- Why does this exist? what's broken about the alternatives, or what feeling are you trying to deliver?
- Do you have a name in mind, or is naming part of what you want help with?

**If they dropped a website / existing brand URL:**
- Are we refreshing this brand or rebuilding it from scratch?
- What's working about it today, and what isn't?
- Who's the current customer vs. who you wish were the customer?

**If they dropped product photos:**
- Ask how the product is made, who has bought or used it, price point, current sales/channel context, and any direction they already have in mind.
- Keep the output scoped to guidelines and a brand kit, not a commerce launch.

**If they dropped reference brands only ("I want a brand that feels like Aesop + Patagonia"):**
- What's the product, service, or thing this brand will be attached to?
- What about each reference brand specifically do you love? (the photography? the tone? the restraint?)
- Who buys this — describe the 2-3 audience segments this brand should serve, plus one vivid anchor persona inside the primary segment.
- Any constraints? (industry, regulation, location, price tier?)

**Always also ask (regardless of input type):**
- Do you have any existing brand assets you want to keep or incorporate? (Logo, wordmark, symbol, name, colors, fonts, photography, packaging — anything you don't want to lose.)
- Any specific references, inspirations, or moodboards you'd want this to draw from?
- **Is this a digital product** (app, website, SaaS, web tool)? This determines whether the Icons page belongs in the full guidelines — for non-digital brands (products, services, restaurants, fashion, etc.) the Icons page is skipped.

These two are essential — they prevent you from generating things the user already has, and they anchor the work in references the user actually likes. Always include them.

Keep it to a single message. Aim for 5-7 questions total (input-specific + the 2 universal), conversational not clinical. Wait for answers before proceeding.

**After answers**, analyze the input + answers together and read back:
- **Aesthetic territory**: what visual world does this live in?
- **Audience segments**: primary segment, secondary segment(s), and one vivid anchor persona inside the primary segment. Do not collapse the audience into one over-specific individual.
- **Positioning**: what's the wedge — what does this stand for that competitors don't?
- **Price tier / category fit**: where on the market shelf does this sit?
- **Story hook**: what's the emotional reason someone cares?
- **Assets being kept**: explicitly list what the user said they want to preserve (existing wordmark, name, colors, etc.)
- **References anchoring the work**: list the user-named inspirations.

**Then preview the deliverable and invite specific guidance** — before moving to brand directions, show the user what'll be in the final guidelines so they can flag anything to add, change, or call out:

```
here's what i'll build into the brand guidelines (14-16 pages depending on your brand):

1. Cover (brand name, tagline, hero mood)
2. Strategy & positioning (primary/secondary audience segments + anchor persona)
3. Brand foundation (mission, values, story)
4. Logo (wordmark + symbol + variants)
5. Logo don'ts
6. Color palette
7. Typography
8. Icons — UI icon system + library guidance, ONLY IF this is a digital product (app / web / SaaS). Skipped for non-digital brands.
9. Voice & tone
10. Imagery rules (photography and/or illustration, adapted to brand medium; splits to 2 pages if hybrid)
11. Visual world / lifestyle imagery
12. Touchpoints (real photos showing the brand in use)
13. Brand applications (mockups: business card, app icon, favicon, etc.)
14. Digital + social
15. Do & don't

plus a brand kit zip at the end with: `brand.md` spec, logo assets (symbol PNG sizes, wordmark SVG/PNG, lockup SVG/PNG), brand fonts, design tokens (CSS / JSON / Tailwind), AI prompts (system prompt + task-specific starters), and the icon SVGs if applicable.

anything you want to add, change, call out specifically, or want me to handle differently? if not, i'll move on to the 3 brand boards.
```

Wait for response. Incorporate any specific user guidance (add a page, swap something, special focus on a particular section, exclude something) before moving to Step 2. This catches scope mismatches early — much cheaper than discovering them after the PDF is built.

### Step 2 — Generate 3 Visual Brand Boards (PDF)

This step is the user's first visual touchpoint with the brand. No text-only "directions" precede it. The boards ARE the directions, made visible. Each board contains a complete visual identity at-a-glance so the user can see the difference, not just read it.

Build a single 3-page PDF (one page per board, 1200×850 each) and save it to `~/Desktop/[brand-slug]-brand-boards.pdf`. Each board is a genuinely different brand direction — not template recolors. Differentiate on WHO the brand is for and WHY it exists, while making the visual system, layout, fonts, color logic, photography style, and voice feel distinct.

**Each option must include:**
- **Wordmark** in the brand's display font — use the user's existing wordmark if they have one they like; propose a new one if they need a logo or don't like their current one. A new wordmark must have custom letter treatment: adjusted spacing, ligature, cut, terminal, case, underline, or other ownable detail. It is not just a Google Font typed in a color.
- **Symbol/mark** — a standalone graphic that lives without the wordmark. Use the user's existing symbol if they have one they like; propose a new one otherwise. Even if the user keeps their wordmark, propose a symbol if they don't have one — favicons and app icons need a non-typographic mark. For new symbols, generate a transparent PNG via `generate_image` with `provider="gpt-image-2"`. Ask for a clean isolated mark on transparent background, no baked-in letters, no watermark, no mockup, centered in a square. Do not trace the generated symbol to SVG; export PNG sizes from the approved master. Must work at 16×16 AND 512×512.
- **Seal / badge** — if the option uses a seal, stamp, badge, or monogram, it must be readable and ownable at small and medium sizes. It cannot be a generic circular font lockup, clip-art crest, or low-contrast decorative filler.
- Tagline (8 words max)
- Voice sample with visible "VOICE" label (one quoted sentence, 14 words max)
- Compact board story (~35 words max, min 2 sentences)
- Lifestyle world description with visible "WORLD" label (~22 words max, min 1 full sentence)
- Lifestyle mood image (generated via gpt-image-2)
- 4-color palette with hex + role labels
- Display + body type specimens with named fonts

Brand board pages should look different enough that the user can tell which identity they are seeing before reading the labels. Don't use the same template recolored 3 times; each board's layout should embody the option's design philosophy. A magazine-cover option should look like a magazine cover (full-bleed photo, masthead-style); a soft consumer option should look like a homepage hero (rounded shapes, soft circles for swatches); an editorial option should look like a literary spread (huge italic centered, inset photo). See `references/brand-guidelines.md` "Brand Board Layout — Differentiate per Option" for examples.

If you can't physically tell which brand you're looking at *without* reading the labels — regenerate within the visual-QA retry budget below.

**Page size:** 1200×850px. Renderer: local Chrome headless preferred; WeasyPrint is allowed only when the HTML is written for it. Render board PDFs and QA previews locally, then copy the final board PDF to `~/Desktop`.

**Board quality gate:** the 3-page preview must pass visual QA, not just render QA.

Retry budget: each brand-board or guidelines PDF visual-QA loop gets at most 2 total render/repair attempts for the same option/deck (initial render + one repair rerender). After either cap is exhausted, stop and ask the user which failed asset or layout issue they want to relax; include the failing page/asset name, the QA reason, and the best preview URL so far.

1. Inspect each PNG preview before sending the PDF. Fail ugly density, weak hierarchy, muddy one-note palette, unreadable small text, empty mockup/image slots, clipped text, and body copy or non-masthead text intersecting icons, swatches, seals, photos, phone mockups, or decorative rules. Also inspect the symbol at 16×16 and 512×512; if the small-size read is illegible, muddy, too generic, or collapses into noise, regenerate or simplify before delivery. Website/social/app mockups are optional on brand boards; do not add them unless they contain real content. If included, flat color rectangles count as empty placeholders unless the section is explicitly a palette specimen.
2. Read each board preview at full size. Fail low-contrast type, unreadable small text, text/photo collisions, missing content, weak hierarchy, and muddy one-note palettes. Masthead wordmark/tagline/issue metadata overlays on photos are allowed only when they use deliberate negative space or a contrast scrim and pass contrast QA as defined in `references/brand-guidelines.md` Rule 5. Body copy on images is still forbidden.
3. Fix every captured FAIL before delivery. If the board is technically valid but ugly, treat it as failed and simplify hierarchy, copy density, or decorative elements before rerendering.

**Font rule:** fresh fonts per brand AND fonts must have character. Never default to Inter / Karla / Outfit / DM Sans / Lato — they have no point of view as a display face. Explore the full Google Fonts library. See `references/brand-guidelines.md` "Must Have Character — Don't Default to Safe Fonts" for high-character options by vibe. Download the chosen font files locally and use absolute `file://` `@font-face` declarations in rendered HTML.

**Font fallback for non-Latin brand names:** every `font-family` chain in brand boards, quick PDFs, and full guidelines must include broad-script fallbacks. Use Chromium's per-glyph fallback so Latin stays in the chosen brand face while CJK, Arabic, Cyrillic, and other scripts resolve to Noto families instead of tofu boxes. Minimum chains: display/serif `BrandDisplay, "Noto Serif SC", "Noto Serif TC", "Noto Serif JP", "Noto Serif KR", "Noto Sans Arabic", serif`; body/sans `BrandBody, "Noto Sans SC", "Noto Sans TC", "Noto Sans JP", "Noto Sans KR", "Noto Sans Arabic", system-ui, sans-serif`.

Do not build the full 14-16-page guidelines PDF until the user picks an option — that wastes time on rejected identities. Exception: in autonomous full mode, use model judgment to pick the strongest board or hybrid and continue without waiting.

Present all 3 clearly. Ask the user to pick one, or mix elements from different options.

### Step 3 — Build the Full Brand Guidelines PDF

Once user confirms a board, build the 14-16-page brand guidelines PDF. In autonomous full mode, build from the model-selected board or hybrid recorded in the assumptions log.

**Page count is conditional:**
- **14 pages** — non-digital brands (product, restaurant, fashion, service, etc.) with single-medium imagery. Icons page is skipped.
- **15 pages** — digital brands (app / web / SaaS) with single-medium imagery. Includes Icons page.
- **15 pages** — non-digital brands with hybrid imagery (photo + illustration). Imagery splits to 2 pages; Icons skipped.
- **16 pages** — digital brands with hybrid imagery. Both Icons and split-Imagery present.

Renumber pages contiguously based on what's included. Do not leave page-number gaps.

**Page structure (full list — apply conditionally per above):**

1. **Cover** — Brand name, tagline, hero mood image. Full-bleed.
2. **Strategy & Positioning** — Direction name. Positioning statement (one punchy sentence). Target audience system: primary segment, secondary segment(s), and one vivid anchor persona inside the primary segment. Do not describe only one over-specific customer. 3-4 reference brands with "borrow this" notes.
3. **Brand Foundation** — Mission. Brand values (3-5). The "why this exists" story (2-3 paragraphs of real copy in brand voice — not a template).
4. **Logo** — Primary mark + all variants (horizontal, icon-only, reversed), usage rules (on dark / on light / on color), logo mark explanation, clear space rule.
5. **Logo Don'ts** — Explicit misuse rendered in CSS: never stretch, never rotate, never wrong background, never recolor, never use drop shadow. Show each violation visually with a ✗ label.
6. **Color** — All swatches with hex + RGB + CMYK, primary pairings, accessibility/contrast note, never-do combinations. Full-bleed color columns, not swatches floating on white.
7. **Typography** — Full hierarchy (H1 through caption with exact px sizes), display/accent/body fonts, usage rules per context, type on color backgrounds, minimum sizes.
8. **Icons** *(digital brands only — skip for product, fashion, restaurant, service brands)* — UI icon system: 8-12 essential icons (arrow-right, check, close, plus, settings, search, user, bell, menu, info, etc.) rendered in the brand's geometric style + stroke/corner/grid rules + library recommendation for icons beyond the set. See `references/brand-guidelines.md` "Icons Page — Structure & Rules" section.
9. **Voice & Tone** — Tone adjectives, copy examples by context (headline, body, button, error state, social caption), forbidden words/phrases. Show actual brand copy, not generic example copy.
10. **Imagery Rules** — adapts to the brand's medium. **Photography-led** → photography rules (subject/light/color/cast/texture/forbidden + 1 example photo). **Illustration-led** → illustration rules (style/color/line/character/composition/forbidden + 1 example illustration). **Hybrid** (both equally) → split into two pages, guidelines becomes 16 pages. See `references/brand-guidelines.md` "Imagery Rules Page — Adapts per Brand."
11. **Visual World** — Full-bleed 4-column grid of 4 images matching the brand's medium mix (all photos, all illustrations, or mixed). Cast must be racially diverse for any people-featuring images.
12. **Touchpoints — Real Photos** — A 2×2 grid of 4 REAL GENERATED PHOTOGRAPHS showing the brand in physical context. **Adapt to the brand type:**
    - **Physical product brand**: hang tag on garment, woven label macro, kraft mailer with tissue, flat lay of product + packaging
    - **Digital / app brand**: phone in hand showing the app, laptop on desk showing the site, sticker on water bottle, tote bag in a real scene
    - **Service brand**: business card in hand, branded notebook on desk, signage on a building, swag in context
    No CSS vector mockups on this page — without real generated photos the touchpoints look like a Figma exercise, not a brand. Real images prove the brand can survive contact with the physical world.
13. **Brand Applications — CSS Mockups** — CSS-rendered mockups of secondary applications, each labeled with specs: business card (with dimensions), social avatar (circle crop), sticker/app icon (rounded square), email signature, presentation cover slide. For product brands also include: hang tag spec, woven label spec, shopping bag spec.
14. **Digital / Social** — Website hero aesthetic (colors, fonts, layout feel), Instagram grid style (3×3 mockup with color palette + caption tone), story template (brand colors + logo placement), link-in-bio layout.
15. **Do & Don't** — 5 dos and 5 don'ts, brand-specific and actionable. Not generic ("do use the logo correctly") — brand-specific ("do leave a full em-dash of space around the wordmark in social posts; never crop our tagline mid-word").

Keep Page 2 (strategy) before Page 3 (foundation), and keep both before logo/color/type. Strategy frames every visual decision that follows.

Include every page in the structure. If the brand has no packaging, adapt the touchpoints page to the brand type instead of skipping it; the guidelines should still show how the identity survives in real contexts.

**Completion gate:** do not deliver a condensed or partial guidelines PDF. A
condensed 6-page deck, missing Visual World page, missing Touchpoints page, or
missing Brand Applications page is a failed checkpoint, not a final deliverable.
If time runs out, stop with a resumable checkpoint that lists completed pages,
missing pages, generated asset URLs, and the next render step. Do not present
the deck as done until all mandatory pages have rendered and passed QA.

All build rules in `references/brand-guidelines.md` apply: local rendering rules, explicit 1200×850 page dimensions, absolute local asset/font paths, no load-bearing text on generated images, no duplicate generated images across deck, text contrast thresholds on dark backgrounds, and mandatory pre-send QA previews for every page.

**Deliver as PDF.** Save to `~/Desktop/[brand-name]-brand-guidelines.pdf` and tell the user the local path. Do not upload or host the PDF unless the user explicitly asks for a hosted copy. If the user is not on a Mac, save to the project working directory and mention the path in your reply.

### Step 4 — Export the Brand Kit (HARD GATE — only after user explicitly approves the guidelines)

After delivering the 14-16-page guidelines PDF, **wait for explicit user approval** before exporting the brand kit. Don't auto-export — the kit codifies the final brand, so only build it once the brand is locked. Exception: in autonomous full mode, the single clear brief already authorizes the full deliverable set, so export `brand-kit.zip` after the guidelines pass QA.

Then build a comprehensive brand kit zip that lets the user produce on-brand work anywhere — in Claude, GPT, Figma, with a designer, with a developer.

**Kit structure:**

```
[brand-name]-brand-kit.zip
├── brand.md                       # comprehensive machine-readable spec
├── brand-guidelines.pdf           # full 14-16-page guidelines PDF (the visual deliverable)
├── README.md                      # 1-page how-to-use guide
├── logo/
│   ├── symbol/                    # standalone mark — RASTER ONLY, no SVG (symbol is generated PNG, not traced)
│   │   ├── symbol-[color]-16.png
│   │   ├── symbol-[color]-32.png
│   │   ├── symbol-[color]-64.png
│   │   ├── symbol-[color]-128.png
│   │   ├── symbol-[color]-256.png
│   │   ├── symbol-[color]-512.png
│   │   ├── symbol-[color]-1024.png
│   │   └── symbol-[color]-2048.png
│   ├── wordmark/                  # the brand name — vectorized via text-as-paths
│   │   ├── wordmark-[color].svg
│   │   └── wordmark-[color].png
│   └── lockup/                    # symbol + wordmark together at locked measurements
│       ├── horizontal/
│       │   ├── lockup-h-[color].svg
│       │   └── lockup-h-[color].png
│       └── stacked/
│           ├── lockup-s-[color].svg
│           └── lockup-s-[color].png
├── icons/                         # digital brands only — UI icons from the Icons page as SVGs
│   ├── arrow-right.svg
│   ├── check.svg
│   ├── close.svg
│   ├── plus.svg
│   ├── search.svg
│   ├── user.svg
│   ├── settings.svg
│   ├── bell.svg
│   ├── menu.svg
│   ├── info.svg
│   └── [+ any brand-specific icons]
├── fonts/                         # actual TTF font files (OFL-licensed Google Fonts)
│   ├── [display-font]-Variable.ttf
│   ├── [body-font]-Variable.ttf
│   └── README.md                  # license + install instructions
├── tokens/                        # design tokens for devs
│   ├── tokens.css                 # CSS custom properties — paste into :root
│   ├── tokens.json                # same content in JSON — for AI tools / CI
│   └── tailwind.config.snippet.js # paste into tailwind.config.js extend block
└── prompts/                       # AI prompts for downstream brand use
    ├── system-prompt.md           # paste at the top of a Claude/GPT thread for brand voice
    ├── tweet.md                   # task-specific starter: write a tweet
    ├── landing-hero.md            # task-specific starter: landing page hero copy
    ├── email.md                   # task-specific starter: marketing/transactional email
    ├── error-message.md           # task-specific starter: write a friendly error
    ├── photography.md             # task starter: generate brand-style photography (with cliché guardrails + brand-photography rules embedded)
    └── illustration.md            # task starter: generate brand-style illustration (only if the brand uses illustration as a medium)
```

**Color variants to export** (per logo): primary-on-light, primary-on-dark, neutral-on-light (ink), neutral-on-dark (cream), and one accent-on-color combination. Usually 4-5 color sets per logo type.

**brand.md** — see `references/brand-md-template.md` for the full structure. It must include:
- Quick reference block (name, tagline, primary color, fonts, voice in one scannable section)
- Positioning + audience segments
- Mission, values, story
- Voice & tone (adjectives, copy examples by context, forbidden words)
- Colors (table with hex / RGB / CMYK / Pantone / role)
- Typography (display + body + Google Fonts URLs + full hierarchy)
- Logo (wordmark description + symbol description + lockup specs + file list with paths)
- Photography rules
- Visual world description
- Touchpoint specs
- Do & don't list
- Reference brands with "borrow this" notes
- How-to-use section telling downstream tools/people how to apply the spec

**Logo asset pipeline:**
1. **Symbol assets** — the symbol is a generated raster mark, so export PNG only. Start from the approved 2048x2048 transparent master, verify true alpha, then generate `16/32/64/128/256/512/1024/2048` PNGs per needed color/background variant. Do **not** trace it to SVG and do **not** claim it is vector.
2. **Wordmark assets** — render the brand name as real font text, then convert the chosen font text to outlined paths for `wordmark-[color].svg`; also export a 1024-wide transparent PNG fallback. The wordmark is reproducible because it is typography, not an image-generation artifact.
3. **Lockup assets** — assemble the approved symbol PNG + outlined wordmark at the locked measurements. Export `lockup-[orientation]-[color].svg` with the PNG embedded inline and the wordmark as paths, plus a 1024-wide PNG fallback. Keep geometry identical across color variants.
4. **Optional print PDF** — only add PDFs if the user or printer specifically asks. A PDF may embed the raster symbol plus vector wordmark, but it is not a pure-vector logo file.
5. **Icon SVGs** — for digital brands only, write the icon set as standalone SVGs with `stroke="currentColor"`, `viewBox="0 0 24 24"`, and the brand's chosen stroke weight + corner style applied consistently. See `references/brand-guidelines.md` "Icons Page — Structure & Rules" for which icons to include.
6. **Design tokens** — generate all three files from the brand spec:
    - `tokens.css` — `:root` block with `--color-*`, `--font-*`, `--font-size-*`, `--line-height-*`, `--space-*`, `--radius-*`, `--shadow-*` custom properties
    - `tokens.json` — same content as JSON object with sections: `color`, `font`, `fontSize`, `lineHeight`, `spacing`, `radius`, `shadow`
    - `tailwind.config.snippet.js` — JavaScript snippet to paste inside `module.exports.theme.extend` covering colors, fontFamily, fontSize, borderRadius, boxShadow
7. **AI prompts** — generate each prompt file with brand specifics interpolated:
    - `system-prompt.md` — a system prompt to paste at the top of any Claude/GPT thread. Includes: brand voice adjectives, forbidden words, copy rules, photography direction, color/font specs, sample voice examples. End with "Always apply this brand voice unless explicitly instructed otherwise."
    - `tweet.md` — task starter: max 280 chars, voice constraints, sample target tweets, then "Task: [USER FILLS IN]"
    - `landing-hero.md` — task starter: hero copy structure (headline + subheadline + CTA), brand voice rules, examples from the guidelines
    - `email.md` — task starter: email tone, subject line guidance, body structure, sign-off conventions
    - `error-message.md` — task starter: how the brand handles error/empty/loading states in voice (warm not robotic, specific not vague)
    - **`photography.md`** — task starter for generating brand-style photography (gpt-image-2 etc.). Must include: master prompt template tailored to the brand's photo direction (subject, light, color grade, cast diversity, texture); explicit "what to AVOID in the prompt" list (studio strobes, stock terms, glass coworking spaces, "engineers at laptops," "professional," "premium," etc.); banned cliché concepts list (hourglasses, lightbulbs, handshakes, network nodes, glowing brains, etc.); subject substitutes for "person doing X"; quality requirements (butter accent, diversity, film grain, documentary); explicit no-text guardrail string; note about never naming real publications.
    - **`illustration.md`** — only if the brand uses illustration as a medium. Task starter for generating brand-style illustrations. Master prompt template with strict palette + style rules (flat vector / line art / etc), banned elements (gradients, drop shadows, 3D, photographic textures), when to use illustration vs photography. Skip this file entirely if the brand has no illustration in its visual world.
8. **Brand fonts** — local export step. Download the actual font files from Google Fonts (or wherever the brand fonts live) and include in `fonts/`:
    - Variable font files when available: `[FontName]-Variable.ttf` (single file, supports all weights)
    - Or static weights at the levels the brand uses
    - Use local TTFs in local render HTML via absolute `file://` paths
    - Add a `fonts/README.md` noting the license (OFL is common, allows redistribution) + Google Fonts URL for online installation
9. **Brand guidelines PDF** — copy the 14-16-page guidelines PDF produced in Step 3 into the kit as `brand-guidelines.pdf`. The kit is incomplete without it.
10. **README.md** — 1-page guide telling the user: what's in the kit, how to use brand.md with AI tools, which logo file for which context, where to install fonts (local TTFs or Google Fonts URLs), how to use the photography/illustration prompts.
11. **Zip everything**: `zip -r [brand]-brand-kit.zip brand.md brand-guidelines.pdf README.md logo/ icons/ fonts/ tokens/ prompts/`

**Brand-kit completion gate:** when the user confirms export, or when
`export_kit` is set in `--config`, the brand kit zip is a required deliverable.
Do not mark the brand kit complete until the zip exists and contains
`brand.md`, `brand-guidelines.pdf`, README, logo assets, icons, fonts, tokens,
and prompts. If any required file cannot be produced, stop with a resumable
checkpoint and list the missing files instead of shipping a partial zip.

**README.md** — 1-page guide telling the user:
- What's in the kit
- How to use `brand.md` with AI tools (paste into Claude/GPT to generate on-brand work)
- Which logo file to use for which context (web favicon → symbol PNG; print collateral → PDF; web header → wordmark SVG; etc.)
- Font installation links (Google Fonts URLs plus local TTF filenames)

**Delivery:**
- Save zip to `~/Desktop/[brand-name]-brand-kit.zip` for local Mac users.
- If the environment cannot download fonts or write a local zip, do not ship a
  partial kit. Stop with a resumable blocked checkpoint that lists the
  completed artifacts (local PDF path, `brand.md`, tokens, logo assets), the missing
  files, and the exact filesystem/network blocker.
- Host the completed zip only if the user explicitly asks.
- Tell the user what's in the completed zip and link to the `brand.md` so they can preview without unzipping.

## Post-flight quality gate

Before declaring success on either deliverable, render local preview images and perform a structured visual QA pass with a structured verdict:

- Quick mode: inspect the PNG/JPG previews or contact sheet for `quick-brand.pdf` before delivering the quick brand package.
- Full mode: inspect the final page PNG/JPG previews or contact sheet used to approve the guidelines PDF before delivering the local PDF path. Do not run analyze_media on the final PDF as the primary QA path; page previews are the QA artifact because they expose page-level layout and avoid large-PDF rasterization failures.

```
Return JSON only: {
  "verdict": "clean" | "degraded" | "catastrophic",
  "observations": string[],
  "quality_warning": string | null,
  "re_roll_suggestion": string | null
}
Check that the brand name is spelled consistently, the `quick-brand.pdf` or guidelines PDF preview shows the required pages, low-contrast text is not present, the wordmark/symbol are not garbled, and there are no blank or duplicate-looking pages.
```

- If `verdict` is `clean`, return the quick brand package or local PDF path normally.
- If `verdict` is `degraded`, return the quick brand package or local PDF path plus the `quality_warning` so the user can review before publishing.
- If `verdict` is `catastrophic`, do not call the deck complete; surface the verdict and `re_roll_suggestion` instead of declaring success.

## Key Principles

- **The input is the brief.** Don't ask for lengthy intake forms. Read what's in front of you and ask 3-5 precise questions.
- **Be specific about customers without narrowing the brand to one person.** Vague audiences = weak brands, but one hyper-specific individual can make the output unusably narrow. Define audience segments first: a primary segment, 1-2 secondary segments, and one anchor persona that makes the primary segment feel concrete.
- **3 boards at the main full-mode choice point.** Step 2 always gives three visual brand boards, not text-only directions or template recolors.
- **Opinionated but collaborative.** Present your read confidently. They can push back.
- Generate actual copy — don't give templates with [BRACKETS]. Write real words in the brand voice.
- **All images must look real and crafted.** Generated lifestyle/touchpoint images need film grain, natural light, slight imperfections, editorial composition. Banned: perfect symmetry, gradient backgrounds, studio strobes, stock-photo energy, AI-smooth surfaces, floating objects on white. If it looks fake, use the image retry budget above; do not keep regenerating after the capped retry.
- **One deliverable set per selected depth.** Quick mode delivers a quick brand package. Interactive full mode delivers one brand guidelines PDF, with the optional brand kit only after the user confirms the guidelines. Autonomous full mode ships all three full artifacts: brand boards, guidelines, and brand kit.

---

## Brand Quality Standards

Every brand produced by this skill should meet the following standards. Generic output is a failure state because the deliverable is meant to guide real design decisions, not decorate a template.

### The Anti-Generic Test

Before delivering anything, ask: *Could this be a brand for literally anything else?* If yes — it's not done.

Strong brand = specific product/service + clear audience model + specific point of view. Weak brand = vibes + aesthetic mood board + empty tagline. Never deliver the second.

### Copy Standards

**What good brand copy sounds like:**
- It makes a specific claim: "Heavy wool. Made to last a decade." / "Built for one quiet hour a day."
- It has a point of view: "Not trend-led. Not mass-made."
- It can speak concretely to a reader inside a segment: "The app you reach for before checking your phone." This is copy style, not audience strategy; do not collapse the brand's audience model to only that reader.
- It creates tension or contrast: "Handmade. Overused. On purpose."
- It trusts the reader: no over-explaining, no "perfect for any occasion", no "cozy vibes"

**What bad brand copy sounds like:**
- "Crafted with love" / "Made with care" / "Designed with passion"
- "Perfect for any occasion" / "A timeless addition"
- "Quality you can feel" / "Designed to inspire"
- Generic taglines: "Where quality meets style" / "Wear your story"
- Hollow superlatives: "premium", "luxury", "elevated", "curated", "artisanal"
- Anything that could describe 500 other brands without changing a word

**Tagline test:** A great tagline could only belong to this brand. "Handmade. Overused. On purpose." is WORN's. "Just do it." is Nike's. If your tagline could appear on any random Etsy shop or Squarespace site without anyone noticing — rewrite it.

### Design Standards

**What editorial brand design looks like:**
- Strong typographic hierarchy — one thing is clearly the most important
- Color used with conviction — large fields, not accent dots
- Photography bleeds to edges — no floating images with shadow drops
- Scale contrast — one element dominates, others recede
- Pages feel designed, not assembled
- Whitespace is intentional, not default padding

**What generic brand design looks like:**
- Equal-sized boxes arranged in a grid
- Body copy the same size as everything else
- Centered everything
- White background with a few colored boxes
- Photos floating in white space with rounded corners
- Font specimens that say "Font Name Here" or "Sample Text"
- Color swatches that look like a paint store brochure

**Layout rule:** If a page could have been made in Canva or PowerPoint in 10 minutes — it's not good enough. Every page should require design decisions only someone with taste would make.

### Photography & Diversity Standards

Generated image sets featuring people should show racial diversity. This avoids defaulting every brand world to the same narrow cast.
- Default to a mixed cast across all 4+ lifestyle images: include Black, Asian, Latina, South Asian, Middle Eastern, or mixed-race subjects
- Vary body types, not just skin tone
- If only one person is shown, make a deliberate choice about who that person is — don't default to white/light-skinned
- Diversity is not a checkbox. It's a design choice that makes the brand more resonant and more honest

**Photography must feel found, not staged:**
- Real rooms with real lives in them (papers, plants, worn furniture)
- Imperfect light (window light, overcast, early morning)
- Film grain always — even a little
- Subjects not looking at camera unless it's a strong choice

### Deck / Guidelines Design Standards

- Typography must load. Download the actual font files and use absolute `file://` paths in local render HTML. Always verify loaded fonts before signing off on a render. If fonts fall back to system defaults — the deck is broken, not deliverable.
- See `references/brand-guidelines.md` for the full local render contract and QA rules.
- Every page must have a clear visual hierarchy — one thing to look at first.
- Full-bleed photography pages should feel like magazine spreads, not slideshow slides.
- Color palette pages: full-bleed color columns, not swatches floating on white.
- Logo page: logo dramatically large, with clear variants, not timid or small.
- Voice page: show actual brand copy, not generic example copy.
- Touchpoints page: must include generated photographs of actual touchpoints — never CSS boxes.

Deliver the guidelines as one local PDF, not as individual page images. Save the PDF path and copy it into the brand-kit zip when exporting the kit.

### The Taste Check

Before delivering any brand output, ask yourself:
1. Would a 25-year-old with good taste want to buy from / use / work for this brand?
2. Does the copy sound like a real person wrote it?
3. Does the design look like a real designer made it?
4. Are the photos diverse and real-looking?
5. Is there a specific point of view — something this brand stands for that another brand doesn't?

If any answer is "not sure" — improve it before delivering. Strong and specific beats safe and generic every time.

---

## Load-bearing phrases

These are the anchors that keep this skill from drifting into generic brand-book output:

| Phrase | Where | Why load-bearing |
|---|---|---|
| `different business answer — not aesthetic variations` | Step 2 visual boards | Forces positioning variety before visual variety. |
| `fonts must have character` | Step 2 visual boards | Prevents safe-font defaults from making every brand feel interchangeable. |
| `no load-bearing text on generated images` | Guidelines build rules | Keeps brand claims editable and legible in deterministic HTML/PDF. |
| `film grain, natural light, slight imperfections` | Image quality standards | Pushes lifestyle/touchpoint images away from stock-photo smoothness. |
| `Name a specific ethnicity per prompt` | Diverse-cast recovery | Fixes the model tendency toward all-white casts more reliably than generic diversity language. |

---

## Engine choice: gpt-image-2 (with caveats)

Default to `gpt-image-2` at `quality: "medium"` for all brand imagery. Why:
- Best instruction-following for cast-diversity prompts (nano-banana-pro tends to drift toward a white default unless heavily prompted).
- Strongest no-text guardrail adherence — critical for touchpoint shots (hang tag / woven label / sticker) where any baked-in text would ruin the mockup.
- Native 3:4 / 4:3 / 9:16 ratios crop cleanly on sharp subjects without weird stretching.

Avoid `nano-banana-pro` for this skill — it bakes magazine-cover-style text into product shots when prompts mention "editorial." 1K from gpt-image-2 is plenty for a 1200×850 PDF page; bump to gpt-image-2's 2K tier (or escalate to `seedream` for higher) only if a specific touchpoint genuinely needs print-tier resolution. (4K on gpt-image-2 is 16:9 / 9:16 only — this skill's 3:4 / 4:3 ratios route to `seedream` if 4K is required.)

## Runtime expectations

Tell the user the rough total up front — long stages without status updates feel broken. Always report times in PST when giving timestamps.

### Quick brand target

| Stage | Target time | Notes |
|---|---:|---|
| Intake + assumptions | 1-2 min | Skip multi-turn Q&A unless the original input is missing |
| One strategy + identity | 2-3 min | Pick the strongest direction; no 3-option detour |
| Symbol/mood/touchpoint assets | 3-5 min | Up to 4 generated images total unless QA fails |
| Quick PDF + kit files | 2-3 min | 3-page PDF, compact `brand.md`, tokens, prompts, available logo assets |
| Quick QA + delivery | 1-2 min | PNG preview inspection; rerender only if a blocking issue appears |

Total quick target: 8-12 min after usable input, excluding user response time.

### Full brand book timing manifest

For every full run, maintain a timing manifest in working notes and include it in the final delivery or resumable checkpoint. Capture PST timestamps for:

- Input received / mode selected
- Intake complete
- Visual boards drafted
- Brand board render started / completed
- User identity choice locked
- Image generation batch 1 started / completed
- Image generation batch 2 started / completed
- Full guidelines render started / completed
- Full-deck QA started / completed
- Brand kit export started / completed, if requested

If a run takes around 2 hours again, do not guess where the time went. Use this manifest to name the actual slowest stage and carry that evidence into the next cut.

### Full brand book target

| Stage | Time | Notes |
|---|---|---|
| Stage 0 → Step 1 (Q&A loop) | 5–15 min | User-paced; questions in one message |
| Step 2 (3 visual brand boards PDF) | 6–10 min | Per-board symbol + one mood image + local Chrome render |
| Step 3 image gen (8 photos via gpt-image-2 in 2 parallel batches of 4) | 8–12 min | The longest stage; each batch ≈ 4–6 min |
| Step 3 page build (14-16 HTML pages + local render) | 2–5 min | Chrome headless preferred; WeasyPrint fallback |
| Step 4 brand kit zip | 3–5 min | Symbol PNG sizes + wordmark/lockup SVG+PNG + conditional icons + tokens + fonts + prompts |

Total full target: ~25–45 min wall-clock excluding user response time. Recent field feedback saw ~2 hours end to end for a paid creator tutorial recording; treat that as the baseline symptom to beat, not as an acceptable target.

---

## Failure modes

### Recovering from upstream 5xx on generate_image

If any paid generation or render MCP call returns:
- `code: "provider_5xx"` AND `retry_class: "retry_after_backoff"`
- Or HTTP 502 / 503 / 504 from an upstream image provider

Do this:
1. Wait 5 seconds.
2. Re-call the exact same MCP tool with the exact same arguments. Do not rewrite the prompt, swap fonts, change palette, change HTML, change provider, or regenerate inputs.
3. If the retry also fails with 5xx, abort and surface to the user: "Provider returned a transient upstream error twice. Try again in 1-2 minutes; this usually clears on its own."

Do not retry more than once. This is a transient outage, not a brand-direction problem; changing the creative brief wastes credits and makes the retry harder to compare.

### Recovering from upstream 4xx / moderation_blocked

If `generate_image` with `provider="gpt-image-2"` returns an upstream 4xx or `moderation_blocked`:
1. Do NOT retry the same prompt; moderation and most 4xx validation failures are deterministic.
2. If the failed asset is a generated symbol or lifestyle image, try a fallback provider once only when the brief can survive it: `seedream` for high-resolution brand imagery, or an inline SVG mark for simple geometric symbols.
3. If the fallback provider also fails or would materially change the brand direction, surface to the user: "Image provider declined this brand-image prompt. Try a less recognizable reference, remove real publication/celebrity cues, or approve an SVG/simple-mark alternative."

### Recovering from upstream 429 (rate limit)

If any upstream returns HTTP 429 with a backoff hint:
1. Wait the hinted backoff, or 30 seconds if no hint is provided.
2. Re-call the exact same MCP tool with the exact same arguments.
3. Do not retry more than once. If it still returns 429, abort and surface the rate-limit message instead of spending more calls.

### `capture_website` returning empty / page-not-loaded

This skill normally builds from user answers and provided assets, but URL-sourced references or future intake helpers may call `capture_website`. If `capture_website` returns 200 but `action_bboxes` is empty or `recording_viewport` is 0x0:
1. Do NOT retry; the page failed to render in the capture environment.
2. Surface: "Could not capture <url>. The page may be blocked / paywalled / require auth. Please provide screenshots, logos, or hosted assets instead."

### Long-running `task_status` exceeding ceiling

Each async MCP call returns either an inline result or `{task_id, status}` for polling. Use these ceilings before deciding a task is stuck:
- gpt-image-2 high quality: 3 min per call
- Seedream image generation: 3 min per call

Use whichever is earlier: the provider's ceiling x 1.5 or any skill-specific hard polling cap. If `task_status` returns `status: "processing"` or `status: "queued"` past that earlier limit, call `task_cancel({task_id})` and surface: "Provider taking unusually long; aborting. Try again."

| Symptom | Cause | Fix |
|---|---|---|
| Fonts render as Times / Arial in the PDF | `@font-face` points to a missing or relative local path | Download TTFs to the local workspace, declare them with absolute `file://` paths, and render a one-page local preview before the full PDF |
| Generated image has baked-in magazine title or watermark | Prompt mentioned "magazine cover," "Vogue," "TIME," "Bloomberg," or any real publication | Strip publication names from prompt; append the verbatim no-text guardrail; regenerate once within the image retry budget. Describe visual qualities, not publications |
| Touchpoint / lifestyle photo shows only forehead / hand-only crop | 9:16 portrait source got cropped to a landscape cell | Regen with `aspect_ratio: "4:3"` or `"16:9"` to match the cell aspect, OR change the layout to a portrait cell |
| Page overflows the 850px ceiling | Headline > 60px combined with > 3 body paragraphs on the same page | Cut content, drop headline to 48px, or split across two pages. Re-render and verify with a screenshot |
| Board technically fits but looks ugly | Too much decorative styling, tiny text, muddy one-note palette, empty mockups, or weak hierarchy | Rewrite board copy to fit the budgets in `brand-identity.md`, remove decorative microtype, increase body text to 18px+, add negative space/contrast, and rerun PNG + visual QA |
| Text overlaps icons/swatches/seals/mockups | Decorative or absolute-positioned elements share the same reading area as copy | Give text a clean reading column/card, move graphics behind non-text areas only, and rerender. Passing `scrollHeight` is not enough if a sibling graphic occludes text |
| Brand board pages feel like recolored templates | Same template reused with palette swaps | Rebuild from `references/brand-guidelines.md` "Brand Board Layout — Differentiate per Option" — each board's layout must physically embody its design philosophy |
| Multi-page merge fails | `pdfunite` or local merge tooling is missing | Use Chrome `--print-to-pdf` on one full HTML document, or fall back to Python `pypdf.PdfWriter().append()` |
| User picks a hybrid identity ("02's palette + 01's voice") | Skill assumes single-option pick | Build a hybrid spec brief before Step 3, confirm with user before rendering 14-16 pages |
| User asks for hosted PDF and upload fails | PDF upload paths often reject `application/pdf` | Keep the local PDF as canonical; if hosting is required, use a user-approved file host or deployment path |
| Lifestyle grid all-white-cast despite diverse-cast rule | gpt-image-2 defaults to lighter skin tone when ethnicity isn't named explicitly per prompt | Name a specific ethnicity per prompt (Black, mixed-race East-Asian-and-white, East Asian, Latina, South Asian, Middle Eastern) — vary across the 4 grid prompts |
