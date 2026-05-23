---
name: build-a-brand
description: >
  Build a complete brand identity and guidelines PDF from any input — an idea, an existing
  website, a list of reference brands, product photos, or "I want to rebrand X". Use when
  someone wants a brand identity but does NOT need a full commerce launch (no Shopify, no
  product listings, no social posting).
  Trigger phrases: "build me a brand", "make me a brand", "design a brand identity", "brand
  guidelines for [X]", "i want a brand book", "create a brand from scratch", "brand for [idea]",
  "i want a brand that feels like [X] + [Y]", "rebrand my [thing]", "visual identity for [thing]",
  "build-a-brand".
argument-hint: "[brand idea, URL, photos, or reference brands]"
---

# Build a Brand

Take any input — an idea, a website, a list of reference brands, product photos, or an existing brand to refresh — and produce a complete brand identity, ending in a 14–16-page brand guidelines PDF.

This is the brand-building engine from `business-maker` without the commerce arm. Same uncompromising standards on strategy, design, copy. Output is **one** brand guidelines PDF for the chosen identity.

## Execution Model — Local First, Cloud Only Where Needed

This skill is local-first. Keep deterministic production work on the user's machine:
- **Local:** workspace setup, downloaded fonts, generated image files after download, image compression, transparent-background cleanup, 16×16 favicon tests, HTML/CSS page builds, PDF rendering, PNG QA screenshots, crop-and-read QA files, logo asset assembly, token/prompt files, and final zip packaging.
- **Cloud:** image generation only (`gpt-image-2` for symbols, mood images, photography, illustration, and ambient textures) and URL/source research when the brief requires it.

Do not use a cloud PDF renderer or upload PDFs by default. Save board PDFs, guidelines PDFs, and brand-kit zips to `~/Desktop` on Mac, or the project working directory when Desktop is unavailable. Only upload/share via CDN if the user explicitly asks for a hosted file.

## Full Workflow

### Stage 0 — Intake (empty-args menu)

If invoked with no input (no idea, no URL, no photos, no reference brands, and no relevant prior context in the conversation), print this menu verbatim as your full response and stop. Do not call any tool. Wait for the user's next message.

> **What are we branding?** Paste any of:
>
> - **An idea / description** — e.g. "a streetwear label for cat people"
> - **A website URL** — e.g. "rebrand my existing site at example.com"
> - **Product photos** — drop them in the chat
> - **Reference brands** — e.g. "I want something that feels like Aesop + Patagonia"
> - **An existing brand to refresh** — name + what's working / what isn't

If the user already dropped one of the above, skip the menu and proceed straight to Step 1.

### Step 1 — Read the Input

Inputs vary. **Before asking any questions, open with a brief agenda** so the user knows what's coming:

```
here's how this works — 4 steps:
1. **Read the input** — i ask a few questions, you answer, i play back what i'm hearing
2. **3 visual brand boards** — i build a 3-page PDF with three complete brand directions, each with its own colors, fonts, photography, voice samples, logo concept. you pick one (or ask to mix elements).
3. **Build the guidelines** — full 14–16-page brand book PDF for the chosen board
4. **Export the brand kit** — `brand.md` spec + logo assets (symbol PNG sizes, wordmark SVG/PNG, lockup SVG/PNG) + fonts + tokens + AI prompts, zipped to your Desktop

let's start. [questions follow]
```

Then ask 3-5 targeted questions in a single message. Adapt to the input type:

**If they dropped an idea / description:**
- What does this brand sell or do? (product / service / app / community / something else)
- Who is this for — describe one specific person, not a demographic
- Why does this exist? what's broken about the alternatives, or what feeling are you trying to deliver?
- Do you have a name in mind, or is naming part of what you want help with?

**If they dropped a website / existing brand URL:**
- Are we refreshing this brand or rebuilding it from scratch?
- What's working about it today, and what isn't?
- Who's the current customer vs. who you wish were the customer?

**If they dropped product photos:**
- Use the `business-maker` Step 1 questions (how it's made, who's bought, price point, direction in mind).
- Same playbook but the output is just guidelines, not a commerce launch.

**If they dropped reference brands only ("I want a brand that feels like Aesop + Patagonia"):**
- What's the product, service, or thing this brand will be attached to?
- What about each reference brand specifically do you love? (the photography? the tone? the restraint?)
- Who buys this — describe one specific person.
- Any constraints? (industry, regulation, location, price tier?)

**Always also ask (regardless of input type):**
- Do you have any existing brand assets you want to keep or incorporate? (Logo, wordmark, symbol, name, colors, fonts, photography, packaging — anything you don't want to lose.)
- Any specific references, inspirations, or moodboards you'd want this to draw from?
- **Is this a digital product** (app, website, SaaS, web tool)? This determines whether the Icons page belongs in the guidelines — for non-digital brands (products, services, restaurants, fashion, etc.) the Icons page is skipped.

These two are essential — they prevent you from generating things the user already has, and they anchor the work in references the user actually likes. Always include them.

Keep it to a single message. Aim for 5-7 questions total (input-specific + the 2 universal), conversational not clinical. Wait for answers before proceeding.

**After answers**, analyze the input + answers together and read back:
- **Aesthetic territory**: what visual world does this live in?
- **Customer**: specific and vivid, not demographic
- **Positioning**: what's the wedge — what does this stand for that competitors don't?
- **Price tier / category fit**: where on the market shelf does this sit?
- **Story hook**: what's the emotional reason someone cares?
- **Assets being kept**: explicitly list what the user said they want to preserve (existing wordmark, name, colors, etc.)
- **References anchoring the work**: list the user-named inspirations.

**Then preview the deliverable and invite specific guidance** — before moving to brand directions, show the user what'll be in the final guidelines so they can flag anything to add, change, or call out:

```
here's what i'll build into the brand guidelines (14–16 pages depending on your brand):

1. Cover (brand name, tagline, hero mood)
2. Strategy & positioning
3. Brand foundation (mission, values, story)
4. Logo (wordmark + symbol + variants)
5. Logo don'ts
6. Color palette
7. Typography
8. Icons — UI icon system + library guidance · ONLY IF this is a digital product (app / web / SaaS). Skipped for non-digital brands.
9. Voice & tone
10. Imagery rules (photography and/or illustration, adapted to brand medium · splits to 2 pages if hybrid)
11. Visual world / lifestyle imagery
12. Touchpoints (real photos showing the brand in use)
13. Brand applications (mockups: business card, app icon, favicon, etc.)
14. Digital + social
15. Do & don't

plus a brand kit zip at the end with: `brand.md` spec, logo assets (symbol PNG sizes, wordmark SVG/PNG, lockup SVG/PNG), brand fonts (TTF), design tokens (CSS / JSON / Tailwind), AI prompts (system prompt + task-specific starters), and the icon SVGs (if applicable).

anything you want to add, change, call out specifically, or want me to handle differently? if not, i'll move on to the 3 brand boards.
```

Wait for response. Incorporate any specific user guidance (add a page, swap something, special focus on a particular section, exclude something) before moving to Step 2. This catches scope mismatches early — much cheaper than discovering them after the PDF is built.

### Step 2 — Generate 3 Visual Brand Boards (PDF)

**This step is the user's first visual touchpoint with the brand.** No text-only "directions" precede it. The boards ARE the directions, made visible. Each board contains a complete visual identity at-a-glance so the user can SEE the difference, not just read it.

Build a single 3-page PDF (one page per board, 1200×850 each) and save it to `~/Desktop/[brand-slug]-brand-boards.pdf`.

**Each board must contain ALL of:**
- Brand name + tagline (rendered in that board's display font)
- 4-color palette with hex codes + role labels
- Display + body font specimens with the actual font names labeled
- A logo concept (see "Logo Pipeline" below — generate the symbol via gpt-image-2, NEVER hand-code an SVG)
- One mood image (real photograph or illustration, generated via gpt-image-2 to match the brand's photography/illustration direction)
- A voice sample (one quoted sentence in brand voice)
- A 1-2 sentence brand story
- 3-4 reference brand names

**The 3 boards must be genuinely different brand directions** — not template recolors. Differentiate on WHO the brand is for and WHY it exists (see `references/brand-directions.md` for the differentiation rule and examples). Each board's layout, fonts, color logic, photography style, and voice must feel like 3 distinct brands.

**Each board's LAYOUT must embody its design philosophy.** A magazine-cover board looks like a magazine cover (full-bleed photo, masthead-style). A soft consumer board looks like a homepage hero (rounded shapes, soft circles for swatches). An editorial board looks like a literary spread (huge italic centered, inset photo). See `references/brand-guidelines.md` "Brand Board Layout — Differentiate per Option" for rules.

**Mandatory before delivering:**
1. **Render each board to PNG via Chrome headless** and READ each PNG. Verify no overlapping type, no broken layouts, no missing content. If anything looks sloppy — fix and re-render.
2. **Verify the fonts feel chosen for THIS brand, not pulled from a mental shortlist.** No font is banned — but no font is a favorite either. If you reached for a font you used on a recent brand, you need a real reason this brand uniquely wants it. Otherwise pick a fresh option that fits as well. See `references/brand-guidelines.md` "No favorite fonts — every brand starts the search fresh" + "The mandatory research step" for the process.
3. **Verify each board's mood image was generated with `provider="gpt-image-2"`** and contains no baked-in text.
4. **Verify the 3 symbols differ in CONCEPT, not just style.** Don't ship three "literal mascot face" marks in three styles — that's one idea repeated. Push the symbols across different concept lanes (mascot / product-feature reference / abstract / monogram / hybrid / container). See `references/brand-identity.md` "Symbol concepts must DIFFER across the 3 brand options."
5. **Verify each symbol passes the "Symbol output rules" check.** Symbols can be any style (flat / 3D / painted / chrome / photographic — no flat-vector requirement). But every gen'd symbol MUST satisfy ALL of: (a) conceptually linked to the brand (means something about what the brand IS/DOES, not just decorative), (b) feels unique (not generic — would fit ONLY this brand), (c) recognizable at 16×16 favicon size — mandatory test: PIL resize to 16×16 with LANCZOS, then upscale that 16-px image with NEAREST to 128×128 to see what a viewer sees at favicon scale, Read the test image. If the mark dissolves to mush, regenerate with stronger compositional weight (for hairline/lux marks: give the dominant element a solid filled mass while keeping framing details fine-lined — see DMV exercise pattern). Style is preserved, weight is adjusted. Details in `references/brand-identity.md` "Recognizable at small size," (d) no more than 3 dominant colors, (e) high res (2048×2048+ when shipped), (f) no text inside the image, (g) true transparent background (verified alpha=0 in PIL, key out near-white pixels if gpt-image-2 painted them). The symbol is shipped as a high-res transparent PNG — **NOT traced to SVG**. Only the wordmark gets vectorized in the brand kit. See `references/brand-identity.md` "Symbol output rules" + "Logo Pipeline."
6. **Adjective audit — verify the 3 boards diverge across multiple dimensions, not just palette.** Even when the user's brief is unified (one era / one mood / one set of references), the 3 boards must feel like 3 different brands. Write the top-3 primary adjectives for each board. If 2 boards share 2+ primary adjectives ("both bright, both maximalist, both cartoon-y"), they're collapsing — push apart on density / saturation / layout philosophy / type energy / voice register. See `references/brand-guidelines.md` "Unified aesthetic briefs STILL require structural divergence" for dimensions. The user gave you 3 references for a reason — interpret each as a SUB-territory, not as overlapping inputs into one mood.
7. **Brief delivery check: every board delivers on the brief at full intensity.** Whatever character the brief named (Y2K, kawaii, brutalist, etc.), every board delivers it 100%. Variety comes from sub-territories within the brief, not from stripping the brief. NEVER make a board muted/dusty/generic to differentiate — that breaks the brief in service of variety. Restraint is allowed (sparse editorial layouts are valid), but stripping character is forbidden. See `references/brand-guidelines.md` "Divergence ≠ subtraction. Every board delivers on the brief."
8. **Era palette check.** If the brief names an era (Y2K, 90s, 80s, mid-century, etc.), all 3 boards must use era-appropriate palette signatures. "Muted dusty cream" is rarely an era's actual signature — Y2K = iMac gel / Tamagotchi candy / chrome / holographic / cyber, NOT cottage-core. See `references/brand-guidelines.md` "Era palettes are specific."
9. **Texture check — generated, ambient, NOT a pattern.** Retro/era briefs need era-appropriate texture, but it must be ATMOSPHERIC (subtle grain / VHS noise / grainy gradient / soft film grain), NEVER a recognizable pattern (literal halftone dots, scattered glitter, visible scanlines). If a viewer can name the texture as a noun ("halftone dots! glitter!") it's too literal — they should describe it as atmosphere ("kind of grainy", "feels VHS-y"). **Generate via `generate_image` with `provider="gpt-image-2"`** — CSS gradients read as stylesheet. Prompt for "ambient grain / atmospheric noise / grainy gradient," NEVER for "pattern / dots / flakes." Apply on the BODY (full board), `mix-blend-mode: overlay/multiply/screen`, `opacity: 0.12–0.30`. See `references/brand-guidelines.md` "Texture is era signal — but it must be AMBIENT, not a pattern."

If you can't tell which brand is which without reading the labels — the boards have failed. Regenerate.

For board PDF assembly via Chrome + `pdfunite`, see `references/brand-identity.md` "Visuals (Required)".

**Do not build the full guidelines PDF until the user picks an option.** Present the 3-board PDF and ask: "Which one feels right? Pick one, mix elements from two, or tell me to swing further in a direction."

### Step 3 — Build the Full Brand Guidelines PDF

Once user confirms a board, build the brand guidelines PDF for that direction.

**Page count is conditional:**
- **14 pages** — non-digital brands (product, restaurant, fashion, service, etc.) with single-medium imagery. Icons page is skipped.
- **15 pages** — digital brands (app / web / SaaS) with single-medium imagery. Includes Icons page.
- **15 pages** — non-digital brands with hybrid imagery (photo + illustration). Imagery splits to 2 pages; Icons skipped.
- **16 pages** — digital brands with hybrid imagery. Both Icons and split-Imagery present.

**Page structure (full list — apply conditionally per above):**

1. **Cover** — Brand name, tagline, hero mood image. Full-bleed.
2. **Strategy & Positioning** — Direction name. Positioning statement (one punchy sentence). Target customer described vividly (one specific person, not a demographic). 3-4 reference brands with "borrow this" notes.
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

**ORDER IS MANDATORY:** Page 2 (strategy) comes before page 3 (foundation) which comes before logo/color/type. Strategy frames everything else.

**ALL PAGES MUST APPEAR.** Never skip a page just because the brand "doesn't have packaging" — adapt the touchpoints page to the brand type instead.

All build rules in `references/brand-guidelines.md` apply: local rendering rules (Chrome headless preferred; WeasyPrint allowed when following its table-only constraints), explicit pixel dimensions, no opacity on images, no text on images, font `@font-face` with absolute `file://` paths, image compression, no duplicate generated images across deck, text contrast thresholds, and mandatory pre-send QA.

**Mandatory pre-delivery checks for the full guidelines PDF (Step 3):**

1. **Product clarity gate — Page 1 (Cover) + Page 2 (Strategy) must make the product unambiguous.** A reader landing on either page must be able to answer "what does this brand sell?" without ambiguity. Cover hero photo must show the product IN USE (for digital products = phone/device showing the actual result, or person using it). Cover subtitle + Page 2 opening paragraph must communicate what the product literally IS, in the brand's voice (clarity through content — not robotic templates). See `references/brand-guidelines.md` Page-Specific Notes for Page 1 + Page 2.

2. **Photography-in-use gate — hero photos show the product, not a representational object.** The cover, photography direction page, touchpoints page, and application page hero photos must show the actual product being used. The brand's *symbol* can be a stylized abstract mark (a heart, a charm shape, etc.) — that's logo language. But brand *photography* must show the actual product. Apply "the keychain test": if a stranger saw the cover with no other context, would they correctly guess what the brand sells? If they'd guess the brand sells the object shown — re-shoot. See `references/brand-guidelines.md` "Photography Must Show the Product IN USE."

3. **Contrast gate — every text/background pair must be verifiably legible.** Audit every text-on-color combination. Auto-fails: pink-on-pink, lime-on-cream, dark-on-dark photo, any small text within 25% luminance of its container. 4.5:1 minimum for body, 3:1 for large display. Fix any failure before delivery — pink display text on a pink background block is a hard ship-block.

4. **Complex-fill scale gate — chrome / holographic / multi-stop gradients ONLY at hero scale.** When the brand wordmark appears at multiple sizes (e.g. cover hero AND small page-header breadcrumb), the cover uses the complex chrome fill BUT the small-scale instances use a solid color with optional stroke. Multi-stop gradients muddy at small sizes. Document both versions on the Logo page.

5. **Render-and-READ every single page individually before merge, including ACTUAL zoom crops.** Render every page in the 14–16-page deck to PNG. Open and READ each PNG full-size (thumbnail pass). Then, for each page, use PIL to crop into 800×800 regions around every text-bearing area (title, subtitle, every section header, every body block, every card pull-quote, every label, every hex code, every footer band). **Read each crop file.** Glancing at the full-page PNG is NOT zoom-reading — it's the thumbnail pass. Without the actual crop-and-read, contrast failures, shaded-font issues, footer overlaps, and text-wrap flaws all hide in plain sight. If you find yourself about to ship without having opened named `zoom-{page}-{region}.png` files — you haven't done the zoom pass. Go back. See `references/brand-guidelines.md` "Three-pass QA" for the full list of regions to crop.

**Deliver as PDF.** Save to `~/Desktop/[brand-name]-brand-guidelines.pdf` and tell the user the local path. Do not upload or host the PDF unless the user explicitly asks for a hosted copy. If the user is not on a Mac, save to the project working directory and mention the path in your reply. Either way: emit the file path so the user can open it — never attach the PDF as a file in the chat.

### Step 4 — Export the Brand Kit (HARD GATE — only after user explicitly approves the guidelines)

🛑 **STOP. This is a hard gate, not a soft suggestion.**

After delivering the 14–16-page guidelines PDF, you MUST wait for **explicit user approval** before exporting the brand kit. The kit codifies the final brand, so only build it once the brand is locked.

**Explicit approval looks like:**
- "yes" / "approved" / "ship it" / "go" / "looks good, export the kit"
- "this is great, do the kit"
- Specific changes followed by approval after those changes are made

**Explicit approval does NOT look like:**
- "just make it cute" (this is creative direction, not approval)
- "ok" alone (ambiguous — could be acknowledging a previous message)
- "i like it" without referring to the guidelines specifically
- The user simply not objecting

**When you deliver the guidelines PDF, your message must end with an explicit ask** like: "ready to lock this in and export the brand kit, or want to adjust anything first?" Then **stop and wait**. Do not call any tool that begins the kit export. Do not stage the kit directory. Do not even copy files into a `kit/` folder. The brand is not approved until the user says so.

**Why this gate matters:** the kit zip locks in every decision — color tokens, voice prompts, logo variants, brand.md — into a portable artifact people will share and reference. Exporting before approval means we ship a kit that might need to change, which defeats the whole point of a kit. Worse, the user feels skipped.

If the user gives feedback on the guidelines (any feedback), iterate on the guidelines PDF first, then ask for approval again. Do not export the kit until they explicitly say go.

Then build a comprehensive brand kit zip that lets the user produce on-brand work anywhere — in Claude, GPT, Figma, with a designer, with a developer.

**Kit structure:**

```
[brand-name]-brand-kit.zip
├── brand.md                       # comprehensive machine-readable spec
├── brand-guidelines.pdf           # full 14–16-page guidelines PDF (the visual deliverable)
├── README.md                      # 1-page how-to-use guide
├── logo/
│   ├── symbol/                    # standalone mark — RASTER ONLY, no SVG (symbol is gen'd PNG, not traced)
│   │   ├── symbol-[color]-16.png      # favicon size
│   │   ├── symbol-[color]-32.png
│   │   ├── symbol-[color]-64.png
│   │   ├── symbol-[color]-128.png
│   │   ├── symbol-[color]-256.png
│   │   ├── symbol-[color]-512.png
│   │   ├── symbol-[color]-1024.png
│   │   └── symbol-[color]-2048.png    # high-res master, transparent background
│   ├── wordmark/                  # the brand name — vectorized via text-as-paths
│   │   ├── wordmark-[color].svg       # Google Font converted to outlined paths (renders without font file)
│   │   └── wordmark-[color].png       # 1024-wide raster fallback
│   └── lockup/                    # symbol + wordmark together at locked measurements
│       ├── horizontal/
│       │   ├── lockup-h-[color].svg   # symbol PNG embedded inline + wordmark as paths
│       │   └── lockup-h-[color].png   # assembled lockup as raster, 1024-wide
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
- Positioning + customer
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
1. **Symbol assets** — the symbol is a generated raster mark, so export PNG only. Start from the approved 2048×2048 transparent master, verify true alpha, then generate `16/32/64/128/256/512/1024/2048` PNGs per needed color/background variant. Do **not** trace it to SVG and do **not** claim it is vector.
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
8. **Brand fonts** — download the actual font files from Google Fonts (or wherever the brand fonts live) and include in `fonts/`:
    - Variable font files when available: `[FontName]-Variable.ttf` (single file, supports all weights)
    - Or static weights at the levels the brand uses
    - GitHub mirror pattern: `https://github.com/google/fonts/raw/main/ofl/[fontname]/[FontName][wght].ttf`
    - Add a `fonts/README.md` noting the license (OFL is common, allows redistribution) + Google Fonts URL for online installation
9. **Brand guidelines PDF** — copy the 14–16-page guidelines PDF (the visual deliverable produced in Step 3) into the kit as `brand-guidelines.pdf`. The kit is incomplete without it.
10. **README.md** — 1-page guide telling the user: what's in the kit, how to use brand.md with AI tools, which logo file for which context, where to install fonts (local TTFs or Google Fonts URLs), how to use the photography/illustration prompts.
11. **Zip everything**: `zip -r [brand]-brand-kit.zip brand.md brand-guidelines.pdf README.md logo/ icons/ fonts/ tokens/ prompts/`

**README.md** — 1-page guide telling the user:
- What's in the kit
- How to use `brand.md` with AI tools (paste into Claude/GPT to generate on-brand work)
- Which logo file to use for which context (web favicon → symbol PNG; print collateral → high-res lockup PNG or optional PDF; web header → wordmark SVG; etc.)
- Font installation links (Google Fonts URLs)

**Delivery:**
- Save zip to `~/Desktop/[brand-name]-brand-kit.zip` for local Mac users.
- Save to the project working directory if Desktop is unavailable.
- Tell the user what's in it and link to the `brand.md` so they can preview without unzipping.

## Key Principles

- **The input is the brief.** Don't ask for lengthy intake forms. Read what's in front of you and ask 3-5 precise questions.
- **Be specific about customers.** Vague audiences = weak brands. Push for vivid specificity — one person, not a demographic.
- **3 boards at the main choice point.** Step 2 always gives the user three visual brand boards, not text-only directions or template recolors.
- **Opinionated but collaborative.** Present your read confidently. They can push back.
- Generate actual copy — don't give templates with [BRACKETS]. Write real words in the brand voice.
- **All images must look real and crafted.** Generated lifestyle/touchpoint images need film grain, natural light, slight imperfections, editorial composition. Banned: perfect symmetry, gradient backgrounds, studio strobes, stock-photo energy, AI-smooth surfaces, floating objects on white. If it looks fake — regenerate.
- **Primary deliverable is the guidelines PDF.** The brand kit is exported only after explicit approval. Not a press kit. Not a launch package. Not a social calendar.

---

## Brand Quality Standards — Non-Negotiable

Every brand produced by this skill must meet the following standards without exception. Generic is a failure state.

### The Anti-Generic Test

Before delivering anything, ask: *Could this be a brand for literally anything else?* If yes — it's not done.

Strong brand = specific product/service + specific person + specific point of view. Weak brand = vibes + aesthetic mood board + empty tagline. Never deliver the second.

### Copy Standards

**What good brand copy sounds like:**
- It makes a specific claim: "Heavy wool. Made to last a decade." / "Built for one quiet hour a day."
- It has a point of view: "Not trend-led. Not mass-made."
- It talks to one person, not a demographic: "The app you reach for before checking your phone."
- It creates tension or contrast: "Handmade. Overused. On purpose."
- It trusts the reader: no over-explaining, no "perfect for any occasion", no "cozy vibes"

**What bad brand copy sounds like (NEVER write this):**
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

**What generic brand design looks like (NEVER produce this):**
- Equal-sized boxes arranged in a grid
- Body copy the same size as everything else
- Centered everything
- White background with a few colored boxes
- Photos floating in white space with rounded corners
- Font specimens that say "Font Name Here" or "Sample Text"
- Color swatches that look like a paint store brochure

**Layout rule:** If a page could have been made in Canva or PowerPoint in 10 minutes — it's not good enough. Every page should require design decisions only someone with taste would make.

### Photography & Diversity Standards

**All generated images featuring people must show racial diversity.** No exceptions.
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

- Typography must load. Always use absolute paths for fonts in WeasyPrint. Always verify loaded fonts before signing off on a render. If fonts fall back to system defaults — the deck is broken, not deliverable.
- See `references/brand-guidelines.md` for the full set of WeasyPrint technical rules.
- Every page must have a clear visual hierarchy — one thing to look at first.
- Full-bleed photography pages should feel like magazine spreads, not slideshow slides.
- Color palette pages: full-bleed color columns, not swatches floating on white.
- Logo page: logo dramatically large, with clear variants, not timid or small.
- Voice page: show actual brand copy, not generic example copy.
- Touchpoints page: must include generated photographs of actual touchpoints — never CSS boxes.

**Deliver as PDF always.** Never as individual page images. Save the PDF locally and share the path.

### The Taste Check

Before delivering any brand output, ask yourself:
1. Would a 25-year-old with good taste want to buy from / use / work for this brand?
2. Does the copy sound like a real person wrote it?
3. Does the design look like a real designer made it?
4. Are the photos diverse and real-looking?
5. Is there a specific point of view — something this brand stands for that another brand doesn't?

If any answer is "not sure" — improve it before delivering. Strong and specific beats safe and generic every time.

---

## Engine choice: gpt-image-2 (with caveats)

Default to `gpt-image-2` at `quality: "medium"` for all brand imagery. Why:
- Best instruction-following for cast-diversity prompts (nano-banana-pro tends to drift toward a white default unless heavily prompted).
- Strongest no-text guardrail adherence — critical for touchpoint shots (hang tag / woven label / sticker) where any baked-in text would ruin the mockup.
- Native 3:4 / 4:3 / 9:16 ratios crop cleanly on sharp subjects without weird stretching.

Avoid `nano-banana-pro` for this skill — it bakes magazine-cover-style text into product shots when prompts mention "editorial." Use `seedream` only when the brand needs 2K/4K print-tier touchpoint photos; otherwise the 1K from gpt-image-2 is plenty for a 1200×850 PDF page.

## Runtime expectations

Tell the user the rough total up front — long stages without status updates feel broken.

| Stage | Time | Notes |
|---|---|---|
| Stage 0 → Step 1 (Q&A loop) | 5–15 min | User-paced; questions in one message |
| Step 2 (3 visual brand boards PDF) | 6–10 min | Per-board: gpt-image-2 symbol + 1 mood image + Chrome render. Then pdfunite all 3. |
| Step 3 image gen (8 photos via gpt-image-2 in 2 parallel batches of 4) | 8–12 min | The longest stage; each batch ≈ 4–6 min |
| Step 3 page build (14–16 HTMLs + Chrome render + pdfunite) | 2–3 min | Sequential render per page |
| Step 4 brand kit zip | 3–5 min | Symbol PNG sizes + wordmark/lockup SVG+PNG + conditional icons + tokens + fonts + prompts |

Total: ~25–45 min wall-clock excluding user response time.

---

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Fonts render as Times / Arial in the PDF | `@import` from Google Fonts races in Chrome headless; WeasyPrint can't resolve relative font paths | Download TTFs to a local `fonts/` dir, declare via `@font-face` with `file://` absolute paths |
| Generated image has baked-in magazine title or watermark | Prompt mentioned "magazine cover," "Vogue," "TIME," "Bloomberg," or any real publication | Strip publication names from prompt; append the verbatim no-text guardrail; regenerate. Describe visual qualities, not publications |
| Touchpoint / lifestyle photo shows only forehead / hand-only crop | 9:16 portrait source got cropped to a landscape cell | Regen with `aspect_ratio: "4:3"` or `"16:9"` to match the cell aspect, OR change the layout to a portrait cell |
| Page overflows the 850px ceiling | Headline > 60px combined with > 3 body paragraphs on the same page | Cut content, drop headline to 48px, or split across two pages. Re-render and verify with a screenshot |
| Brand board pages feel like recolored templates | Same template reused with palette swaps | Rebuild from `references/brand-guidelines.md` "Brand Board Layout — Differentiate per Option" — each board's layout must physically embody its design philosophy |
| `pdfunite` is not on user's machine | Linux user without poppler-utils, or container env | Fall back to `qpdf --empty --pages file1.pdf file2.pdf -- out.pdf` or Python `pypdf.PdfWriter().append()` |
| User picks a hybrid identity ("02's palette + 01's voice") | Skill assumes single-option pick | Build a hybrid spec brief before Step 3, confirm with user before rendering the guidelines |
| User asks for a hosted PDF and upload fails | PDF upload paths often reject `application/pdf` | Keep the local PDF as canonical; if hosting is required, use a user-approved file host or deployment path |
| Lifestyle grid all-white-cast despite diverse-cast rule | gpt-image-2 defaults to lighter skin tone when ethnicity isn't named explicitly per prompt | Name a specific ethnicity per prompt (Black, mixed-race East-Asian-and-white, East Asian, Latina, South Asian, Middle Eastern) — vary across the 4 grid prompts |
