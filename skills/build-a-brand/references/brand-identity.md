# Brand Identity Options — Reference

Each identity option is a complete creative package. When presenting 3 options, make them
genuinely different in name personality, color mood, and voice — not just palette swaps.

## Structure for Each Option

```
### Option [1/2/3]: [Brand Name]
**Tagline:** [Short punchy line — under 8 words]

**Colors:**
- [Name]: #[hex] (role: primary/accent/background/text)
- [Name]: #[hex]
- [Name]: #[hex]
- [Name]: #[hex]

**Typography direction:** [e.g. "Serif headline with clean sans-serif body — editorial and grounded"]

**Voice & tone:** [3-4 adjectives] — [One example sentence in the brand's voice]

**Logo concept — wordmark + symbol + lockup:**

A complete brand identity has BOTH a wordmark and a symbol — they're different things doing different jobs:
- **Wordmark** = the brand name in its identifying typeface. Used wherever there's room (web header, business card, packaging).
- **Symbol** = a standalone graphic mark that lives WITHOUT the wordmark. Used for app icon, favicon, social avatar, browser tab — anywhere the wordmark is too long.
- **Lockup** = how the two combine (horizontal, stacked, symbol-only).

### Logo Pipeline — generate a high-res symbol via gpt-image-2, ship it as transparent PNG (no tracing)

**Hand-coded SVG symbols look amateur.** Do not write `<path d="M..."/>` strings to build the brand symbol. But also: **don't trace the gen'd symbol to SVG.** Keep the symbol as a high-resolution transparent PNG. Only the wordmark gets vectorized (in the brand kit). Pipeline:

1. **Generate the symbol via `generate_image` with `provider="gpt-image-2"`, `quality="high"` (or `"medium"` for first drafts), 1:1 aspect ratio, 1024×1024 minimum.** The symbol's visual style is a brand-personality decision — pick the style that fits the brand's voice and design language, not a default.
   - **Flat is correct** when the brand reads as flat — sticker-style, screen-print, comic/cartoon, vintage print, Memphis-era, modernist, anything that lives in a 2D vocabulary. Most brands land here.
   - **Dimensional / 3D / glossy / painted / photographic** is correct when the brand actually reads that way — luxury beauty, Y2K product-render, 3D-rendered toy, ceramic craft, anything where the visual world has volumetric depth as part of its character.
   - **Neither is the default.** The trace requirement is gone, but that doesn't mean dimensional is "better." Style follows brand. If you removed the trace constraint and immediately reached for dimensional, ask: would the brand prefer flat? Often the answer is yes.
   - The only style-style constraints are the ones in "Symbol output rules" below (≤3 colors, recognizable at 16×16, etc.). Within those, you're free.
2. **The prompt MUST include the no-text guardrail**: "absolutely no text, no letters, no typography, no words, no characters anywhere in the image." gpt-image-2 produces garbled fake text inside logos if you don't explicitly forbid it.
3. **Show the user the gen'd symbol(s).** Generate 2-3 variations if appropriate. Wait for user approval before committing.
4. **Once approved, save as a high-res transparent PNG.** Standard: 2048×2048 PNG with true alpha-channel transparency (verify with PIL — see `brand-guidelines.md` "gpt-image-2 transparent-background caveat"; key out the painted near-white pixels if needed, or regenerate with a solid bg matching the placement surface). Use this PNG everywhere the symbol appears — guidelines pages, brand kit, etc. **Do NOT trace to SVG.** The symbol stays raster.
5. **Wordmark = Google Font, NEVER baked into the image.** Pick a Google Font that matches the brand vibe (see `brand-guidelines.md` "Must Have Character"). The wordmark is rendered as live text in HTML/CSS for the guidelines pages, and converted to text-as-paths SVG in the brand kit (see step 7).
6. **Lockup composition is perfectly measured + permanently fixed.** Pick one horizontal lockup geometry AND one stacked lockup geometry. For each, specify: symbol size (px or em), wordmark font size (px), gap between symbol and wordmark (px), vertical baseline alignment (which point of the symbol aligns with which baseline of the wordmark). **The measurements never change across color variants or contexts.** Document the exact measurements on the Logo page so a designer or developer can rebuild the lockup without guessing.
7. **In the brand kit:** the symbol ships as `symbol-[color].png` (high-res transparent raster) at multiple sizes (16, 32, 64, 128, 256, 512, 1024, 2048). The wordmark ships as `wordmark-[color].svg` with the Google Font text converted to outlined paths (so the SVG renders identically without the font file installed). The lockup ships as `lockup-[orientation]-[color].svg` containing the symbol PNG embedded inline + the wordmark as paths, positioned at the locked measurements.

### Symbol output rules — what the gen'd symbol must satisfy

The symbol doesn't need to be flat or traceable anymore — but it does still need to function as a logo. Every gen'd symbol must satisfy ALL of:

- **Conceptually linked to the product / brand.** The mark must MEAN something about what the brand IS or DOES. Not a decorative shape, not a random pretty thing — a mark that connects to the brand's reason for existing. The koalacore heart-with-koala-ears doesn't just look cute; it says "a koala you wear like an accessory." A camera app's symbol could be a shutter aperture (product-feature), an abstract eye (sense of seeing), or a literal frame (what the app does to a photo). Whatever the concept lane (see "Symbol concepts must differ across the 3 brand options"), there has to be a real conceptual link.
- **Feels unique. Makes sense. Doesn't feel generic.** If you can describe the mark in a way that would fit 50 other unrelated brands ("a heart," "a smiling face," "an arrow"), push further — add specificity that ties it to this brand's actual personality. The uniqueness comes from the SPECIFIC interpretation, not the broad category.
- **Recognizable at small size — mandatory favicon test after every gen.** The mark must read as the brand at 16×16 (favicon size). Test procedure (run AFTER every symbol gen, before any approval ask): use PIL to resize the symbol to 16×16 with LANCZOS, then upscale that 16-px version with NEAREST to ~128×128 (pixel-doubling, so you can actually see what a viewer sees at favicon scale). Read the test image. If the dominant elements have collapsed into mush or vanished entirely, the mark fails — **regenerate**, don't ship.
  - **The fix when a mark fails the test depends on what went wrong:**
    - **All-hairline mark dissolves at small scale** (common for luxury / heritage / engraved aesthetics). Fix: give the *dominant central element* a solid filled mass while keeping the framing details (outer ring, decorative crest, laurel, ornamental flourishes) in hairline weight. The DMV exercise demonstrated this: hairline car silhouette → vanished at 16 px; same composition with the car silhouette filled solid → reads clearly at every scale. The lux feel survives because the engraved fine-line frame is still there at large sizes — at small sizes, the solid central mass carries the recognition load.
    - **Too many tiny detail elements** (e.g. many separate ornaments, fine pinstripes, small leaves). Fix: simplify — keep one or two dominant elements, remove the rest.
    - **Weak silhouette / outline blends with background.** Fix: thicken outlines OR pick colors with stronger luminance contrast against likely placement backgrounds.
    - **Light-on-light or low-contrast composition.** Fix: increase the contrast between the mark's dominant color and its background.
  - **Style is preserved, weight is adjusted.** A richly-rendered 3D mark, a painted mark, a photographic mark, a hairline engraving — all can pass the favicon test by ensuring the dominant readable element has enough mass at 16 px. The fix is compositional, not a style downgrade.
- **No more than 3 colors.** Counting the dominant color regions, not individual gradient stops. The mark can be a gradient FROM one color TO another (that counts as 2). Or a 3-tone illustration. But not a full rainbow / not a richly multicolored scene. 3 dominant colors max keeps the mark memorable and reproducible across material applications (embroidery, print, etc.).
- **High resolution.** Generate at gpt-image-2's highest available res, then upscale or regenerate larger if needed. The final shipped PNG should be at least 2048×2048 so it scales cleanly to billboard size without pixelation.
- **NO TEXT inside the symbol image.** Ever. Text goes in the wordmark only. The symbol is purely a visual mark.
- **Transparent background, verified.** True alpha=0 in the transparent region. If gpt-image-2 paints near-white pixels in the "transparent" area (it often does), key them out with PIL or regenerate with a solid bg that matches the placement surface.

If the gen'd output has text, more than 3 dominant colors, or fails the 16×16 recognizability test, **regenerate** — don't ship it.

### Symbol concepts must DIFFER across the 3 brand options

The three identity options are different brands, not the same brand in three skins. Their symbols should differ in *concept*, not only in visual style. **Do not generate three "literal brand mascot face" logos in three styles** — that's one idea repeated.

Pick a different concept lane for each option. Possible concept lanes:
- **Literal mascot / character** — the brand's animal/object rendered as the mark (most expected).
- **Product-feature reference** — symbol references what the product *does* (e.g. a camera shutter for a camera app, a needle-and-thread for a tailor, a flame for a delivery app).
- **Abstract / geometric mark** — a non-representational shape with meaning (e.g. an arrow, an arc, a spiral, a chevron).
- **Monogram** — the brand initial(s) drawn distinctively.
- **Hybrid** — two concepts fused into one shape (e.g. a heart whose top is animal ears, an arrow that's also a leaf).
- **Container / frame** — a window, badge, stamp, or seal that holds the brand's signature element.

When proposing 3 options, force the symbols across at least 2–3 different concept lanes. The brand-board comparison is more useful when the symbols argue different ideas about what the brand IS.

### Whether to generate new ones depends on what the user has

- If the user has an existing wordmark or symbol they like — USE it. Document the existing asset in the guidelines.
- If the user is asking for a new logo, or has said they don't like their current one — propose a new wordmark and/or symbol as part of the identity option.
- If the user has a wordmark but no symbol — propose just the symbol. Brands need a non-typographic mark for app icons, favicons, etc., so a symbol is worth proposing even when the wordmark is kept.
- Whatever the source, document BOTH in the guidelines. They're both part of complete brand documentation, even when only one is new.

For each identity option, fill in:
- **Wordmark:** [Which Google Font (or commercial font) is the wordmark set in? Why does it match the brand vibe? Reference existing if kept; describe new if proposed. Spec the font weight + letterspacing + baseline.]
- **Symbol / mark:** [The standalone graphic mark — shape, reference, what it evokes. Generated via gpt-image-2 (NOT hand-coded SVG). Must read at 16×16 AND 512×512. Reference existing if kept; describe new if proposed.]
- **Lockup:** [How wordmark + symbol combine — horizontal (symbol left, name right at exact x-offset), stacked (symbol above name with measured spacing), symbol-only at small sizes. Lock the placement and don't vary it across color variants.]

**Brand story:**
[2-3 sentences for the About page. Written in brand voice. Real copy, not a template.]

**Product / hero subject photography direction:**
[How the main subject of brand photography should look — for product brands: the product itself.
For service / app / community brands: the hero subject of the brand (the person using it, the
moment it serves, the artifact it produces). Be specific: surfaces, lighting, props, mood,
composition. 1-2 concrete reference descriptions (e.g. "like a Sunday farmers market table"
or "like a quiet morning before anyone else is awake").]

**Lifestyle photography direction:**
[The full visual world beyond the hero subject — what does the life around this brand look like?
Include: what environments (homes, outdoor spaces, markets, studios, offices), what kind of
people and how they're styled, what activities and moments feel on-brand, color temperature
and mood of the world, what the brand's customer looks like when they're living their life.
This should paint a complete picture someone could cast and art-direct a shoot from.]

**UI / website art direction:**
[What will the brand's digital presence actually look like? Include: layout feeling (spacious/dense,
editorial/grid), background colors, how text and images are balanced, button style (minimal/bold),
how navigation feels, any special layout details (full-bleed images, whitespace-heavy, etc.),
and overall digital mood. Reference a real website aesthetic if helpful
(e.g. "like Mejuri — very white, generous whitespace, product does the talking")]

**Example brands:**
[3-4 real existing brands that live in a similar world — not competitors, but brands that share
the same energy, customer, or aesthetic. Helps the user immediately understand the territory.
Can be fashion brands, lifestyle brands, tech brands, Instagram accounts, or cultural references.
e.g. "Entireworld, Rowing Blazers, Madhappy — brands with a strong POV and a loyal community"]
```

## Visuals (Required)

After presenting all 3 identity options in text, **render a 3-page brand board PDF (one page per option, 1200×850 each)** so the user can see each identity before committing. Do not generate generic AI "mood board" images — they look stocky and bad.

### How to generate:

Build one self-contained HTML file per option, render each to PDF via Chrome headless, then merge into a single 3-page PDF. Each page MUST have a layout that physically embodies its option's design philosophy (not three template recolours — see `brand-guidelines.md` "Brand Board Layout — Differentiate per Option" for rules and examples).

```bash
WS="${BUILD_A_BRAND_WS:-$HOME/build-a-brand-workspace}"
mkdir -p "$WS/boards"

# 1. Write 3 HTML files: $WS/boards/01-<option-slug>.html ... 03-<option-slug>.html
#    (Each with @page { size: 1200px 850px; margin: 0; } in CSS, fonts via @font-face file:// — see Step 0 of brand-guidelines.md.)

# 2. Render each to PDF via Chrome headless
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"   # macOS path
# Linux: CHROME=google-chrome   |  Windows-WSL: CHROME=/mnt/c/Program\ Files/Google/Chrome/Application/chrome.exe

for i in 01 02 03; do
  "$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
    --virtual-time-budget=8000 --no-pdf-header-footer \
    --print-to-pdf="$WS/boards/$i.pdf" \
    "file://$WS/boards/$i-"*.html
done

# 3. Merge into one PDF
pdfunite "$WS/boards/01.pdf" "$WS/boards/02.pdf" "$WS/boards/03.pdf" "$WS/boards/brand-boards.pdf"

# 4. QA: screenshot each page, read every one before sending
for i in 01 02 03; do
  "$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
    --virtual-time-budget=8000 --window-size=1200,850 \
    --screenshot="$WS/boards/qa-$i.png" "file://$WS/boards/$i-"*.html
done
```

If `pdfunite` (from poppler-utils) isn't installed: `brew install poppler` on macOS, or fall back to Python `pypdf.PdfWriter().append()`. Chrome ships on every Mac at `/Applications/Google Chrome.app/...` — no install needed.

**Delivery:** save `$WS/boards/brand-boards.pdf` to `~/Desktop/[brand-slug]-brand-boards.pdf` and emit the local path in the chat. Do not upload or host the PDF unless the user explicitly asks for a hosted copy.

**Design rules for each board:**
- Each option panel uses its own background color from that option's palette
- Brand name displayed large in that option's display typeface (loaded via `@font-face file://` from `$WS/fonts/`)
- Color swatches shown as circles or rectangles with color names beneath
- Typography is clean and editorial — no generic fonts (no Inter / Karla / DM Sans default)
- Layout philosophy differs per board — a tabloid board looks like a newspaper, a fashion-house board looks like a lookbook spread, an archival board looks like a book frontispiece. See `brand-guidelines.md` "Brand Board Layout — Differentiate per Option" for the differentiation rule and `brand-guidelines.md` "Required content per board" for the per-page checklist.
- No generic AI mood-board collages. Each board may use one purpose-built `gpt-image-2` mood image that matches that board's photography/illustration direction.
- The whole thing should look like something a real brand studio would produce

## Quality Bar

- **Names**: Should be memorable, say-able, and googleable. Avoid made-up words unless they're genuinely good.
- **Colors**: Give them real names (not "Dark Blue" — try "Ink", "Dusk", "Bone"). Specify roles.
- **Voice examples**: Write an actual sentence in the brand's voice (a headline, a button label, an error message), not a description of the voice.
- **Logo concepts**: Cover BOTH wordmark and symbol in every identity option — they're different things doing different jobs. Describe each visually — shape, reference, style. (e.g. wordmark: "a custom hand-drawn serif, slightly imperfect, like a signature"; symbol: "a thin-line greyhound silhouette, drawn mid-stride, in a single continuous line"). What you GENERATE depends on what the user has: use existing assets if the user wants to keep them, propose new ones if the user needs a logo or doesn't like their current one. If the user has a wordmark but no symbol, still propose a symbol — favicons and app icons need a non-typographic mark.
- **Fonts must have character.** Don't default to Inter / Karla / Outfit / DM Sans / Lato — they have no point of view. Explore the full Google Fonts library. See `brand-guidelines.md` "Font Selection — Must Have Character" for approved high-character options.
- **Brand story**: Should make someone feel something. Name the founder's origin if appropriate.

## Example Identity Option

### Option 1: Thread & Tide
**Tagline:** Made slowly. Worn forever.

**Colors:**
- Bone: #F5F0E8 (background)
- Sienna: #C2714F (primary)
- Bark: #6B4F3A (text/accent)
- Sage: #8A9E85 (secondary accent)

**Typography direction:** Soft serif headlines (elegant, unhurried) with minimal sans-serif body text.

**Voice & tone:** Warm, specific, unhurried, honest — "Each clasp is set by hand, so yours might be slightly different from the photo. That's the point."

**Logo concept — wordmark + symbol:**
- **Wordmark:** The brand name in a loose, hand-drawn serif. All-caps with light tracking. Slightly imperfect, like a signature.
- **Symbol / mark:** A small monogram T&T inside a hand-drawn circle, like a maker's hallmark stamped into clay. Used as the standalone identity at app-icon size.
- **Lockup:** Wordmark above symbol-circle for primary lockup; symbol-only at small sizes (favicon, avatar).

**Brand story:**
Thread & Tide started on a kitchen table in 2021, when beads that were supposed to be a birthday gift turned into a small obsession. Every piece is made in small batches — no two exactly alike. We make jewelry for people who want something that feels like it was made for them. Because it basically was.

**Product / hero subject photography direction:**
Natural light only — shoot near a window, never flash. Backgrounds: raw linen, unfinished wood, or stone. Props kept to a minimum — maybe a dried flower or two, never cluttered. Mood is quiet and a little intimate, like something found at a market stall you almost walked past. Close-up shots showing texture and knot detail are essential. Avoid white seamless — it reads too commercial for this brand.

**Lifestyle photography direction:**
The world of Thread & Tide is weekend mornings and slow afternoons. Worn while making coffee in a light-filled kitchen, sitting cross-legged on a rumpled bed, at a farmers market with a canvas tote. The person in the photos is unhurried — no poses, caught mid-moment. Warm skin tones, natural hair, wearing pieces with a simple outfit (linen, denim, nothing loud). Color temperature is warm throughout — golden morning light, never cool or blue. Nothing aspirational in a luxury sense — aspirational in a "I want that quiet Saturday" sense.

**UI / website art direction:**
Cream background (#F5F0E8), not white — warmer and more handmade-feeling. Generous whitespace. Full-bleed photography as hero, minimal text overlaid. Body font is a quiet serif. Navigation is simple — 3-4 items max, no mega-menus. Buttons are outlined, not filled — refined and light. Product grid is 2 columns on mobile, 3 on desktop with breathing room between items. No pop-ups or aggressive CTAs. Overall feel: like a well-made independent magazine. Reference: Aesop's website energy but warmer and more accessible.
