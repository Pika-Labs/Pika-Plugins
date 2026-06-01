# Brand Identity Options — Reference

Each identity option is a complete creative package. When presenting 3 options, make them
genuinely different in name personality, color mood, and voice — not just palette swaps.

## Structure for Each Option

```
### Option [1/2/3]: [Brand Name]
**Tagline:** [Short punchy line — 8 words max]

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

Do not write hand-coded SVG paths for a rich brand symbol, and do not trace a generated symbol to SVG. Keep the symbol as a high-resolution transparent PNG. Only the wordmark gets vectorized in the brand kit.

1. Generate the symbol via `generate_image` with `provider="gpt-image-2"`, `quality="high"` for final, 1:1 aspect ratio, 1024x1024 minimum.
2. Style follows the brand: flat, dimensional, glossy, painted, photographic, chrome, hand-drawn, etc. Neither flat nor 3D is the default.
3. The prompt must include: "absolutely no text, no letters, no typography, no words, no characters anywhere in the image."
4. Save the approved symbol as a 2048x2048 transparent PNG with true alpha verified by PIL.
5. Wordmark = real font rendering, never baked into the image. Convert the wordmark to text-as-paths SVG in the kit.
6. Lockup measurements are fixed: symbol size, wordmark size, gap, and alignment do not drift across color variants.

### Symbol output rules

Every generated symbol must satisfy all of:
- Conceptually linked to the brand/product.
- Unique enough that it would fit only this brand.
- Recognizable at 16x16 favicon size. Test by resizing to 16x16 with LANCZOS, then upscaling to 128x128 with NEAREST and reading the result.
- No more than 3 dominant colors.
- High resolution, with 2048x2048+ master when shipped.
- No text inside the image.
- True transparent background.

If the output has text, too many dominant colors, fake transparency, or fails the 16x16 test, regenerate.

**Whether to generate new ones depends on what the user has:**
- If the user has an existing wordmark or symbol they like — USE it. Document the existing asset in the guidelines.
- If the user is asking for a new logo, or has said they don't like their current one — propose a new wordmark and/or symbol as part of the identity option.
- If the user has a wordmark but no symbol — propose just the symbol. Brands need a non-typographic mark for app icons, favicons, etc., so a symbol is worth proposing even when the wordmark is kept.
- Whatever the source, document BOTH in the guidelines. They're both part of complete brand documentation, even when only one is new.

For each identity option, fill in:
- **Wordmark:** [How the brand name is typeset — typeface choice, custom letter treatment, spacing, ligature/cut/terminal detail, and lockup rhythm. Reference existing if kept; describe new if proposed. A wordmark is not just a Google Font typed in a brand color.]
- **Symbol / mark:** [The standalone graphic mark — shape, reference, what it evokes. Generated via gpt-image-2 when new, shipped as transparent PNG, NOT traced to SVG. Must read at 16x16 AND 512x512. Reference existing if kept; describe new if proposed.]
- **Lockup:** [How wordmark + symbol combine — horizontal (symbol left, name right), stacked (symbol above name), symbol-only at small sizes.]

**Brand story:**
[2-3 sentences for the About page. Written in brand voice. Real copy, not a template.]

Board-preview copy is intentionally shorter: when this story appears on the 3-option brand board, rewrite it to the board budget (~35 words max, min 2 sentences, one compact paragraph). The 2-3 sentence version belongs in the text option/About-page snippet, not the preview board. For the full guidelines foundation page, expand the story to 2-3 paragraphs of real copy in brand voice.

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

Build one self-contained HTML file per option, render each to PDF locally via Chrome headless, then merge into a single 3-page PDF. Each page MUST have a layout that physically embodies its option's design philosophy.

```bash
WS="${BUILD_A_BRAND_WS:-$HOME/build-a-brand-workspace}"
mkdir -p "$WS/boards"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

for i in 01 02 03; do
  "$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
    --virtual-time-budget=8000 --no-pdf-header-footer \
    --print-to-pdf="$WS/boards/$i.pdf" \
    "file://$WS/boards/$i-"*.html
done

pdfunite "$WS/boards/01.pdf" "$WS/boards/02.pdf" "$WS/boards/03.pdf" "$WS/boards/brand-boards.pdf"

for i in 01 02 03; do
  "$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
    --virtual-time-budget=8000 --window-size=1200,850 \
    --screenshot="$WS/boards/qa-$i.png" "file://$WS/boards/$i-"*.html
done
```

Read every PNG preview before sending the PDF path to the user. The check is not only "does it fit?" It must also look like a good brand board: one primary visual focal point with supporting required content grouped clearly, readable text, no empty placeholders, no muddy one-note palette, and no body copy intersecting decorative elements.

Each page MUST have a layout that physically embodies its option's design philosophy (not three template recolours — see `brand-guidelines.md` "Brand Board Layout — Differentiate per Option" for rules and examples).

Assets in the HTML should be local files under `$WS/images` and `$WS/fonts`, referenced via absolute `file://` paths. Download generated image outputs before rendering.

**Delivery:** save `$WS/boards/brand-boards.pdf` to `~/Desktop/[brand-slug]-brand-boards.pdf` and emit the local path. Do not upload or host the PDF unless the user explicitly asks for a hosted copy.

**Design rules for each board:**
- Each option panel uses its own background color from that option's palette
- Brand name displayed large in that option's display typeface (loaded via local `@font-face file://` from `$WS/fonts/`)
- Color swatches shown as circles or rectangles with color names beneath
- Typography is clean and editorial — no generic fonts (no Inter / Karla / DM Sans default)
- Layout philosophy differs per board — a tabloid board looks like a newspaper, a fashion-house board looks like a lookbook spread, an archival board looks like a book frontispiece. See `brand-guidelines.md` "Brand Board Layout — Differentiate per Option" for the differentiation rule and `brand-guidelines.md` "Required content per board" for the per-page checklist.
- No generic AI mood-board collages. Each board may use one purpose-built gpt-image-2 mood image and one generated PNG symbol when that is the strongest logo route. No AI app mockups, AI product mockups, or extra AI filler assets.
- The whole thing should look like something a real brand studio would produce

**Board copy budgets:**
- Tagline: 8 words max.
- Voice sample: 14 words max.
- Brand story: 35 words max, min 2 sentences.
- World description: 22 words max, min 1 full sentence.
- Body text: 18px minimum. Labels: 14px minimum unless purely decorative.
- If copy needs to be smaller than that, rewrite. Do not shrink, layer, or cram until the board technically contains everything but looks bad.

## Quality Bar

- **Names**: Should be memorable, say-able, and googleable. Avoid made-up words unless they're genuinely good.
- **Colors**: Give them real names (not "Dark Blue" — try "Ink", "Dusk", "Bone"). Specify roles.
- **Voice examples**: Write an actual sentence in the brand's voice (a headline, a button label, an error message), not a description of the voice.
- **Logo concepts**: Cover BOTH wordmark and symbol in every identity option — they're different things doing different jobs. Describe each visually — shape, reference, style. What you GENERATE depends on what the user has: use existing assets if the user wants to keep them, propose new ones if the user needs a logo or doesn't like their current one. For a new symbol, use gpt-image-2 with a transparent-background, no-text prompt and ship the symbol as PNG. If the user has a wordmark but no symbol, still propose a symbol — favicons and app icons need a non-typographic mark.
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
