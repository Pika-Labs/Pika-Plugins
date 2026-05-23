# Brand Guidelines — Build Guide

The brand guidelines PDF is the primary deliverable of this skill. It is 14–16 pages depending on brand type, built locally with Chrome headless or WeasyPrint, and delivered as a local PDF path.

This guide is the technical playbook: page layouts, image generation, font rules, local rendering, QA checklist. All non-negotiable.

## Execution Model — Local First

Keep deterministic production local:
- **Local:** workspace setup, downloaded fonts, compressed image files, transparent-background cleanup, favicon tests, HTML/CSS builds, PDF rendering, PNG screenshots, crop-and-read QA, logo asset assembly, and kit packaging.
- **Cloud:** `gpt-image-2` image generation for symbols, photography, illustration, and textures; URL/source research when the brief requires it.

Do not upload PDFs by default. Save PDFs and zips to `~/Desktop` on Mac, or the project working directory if Desktop is unavailable. Only create a hosted/CDN copy when the user explicitly asks.

## Page Structure (14–16 pages depending on brand)

**Page count is conditional:**
- **14 pages** — non-digital brand (product, restaurant, fashion, service) with single-medium imagery. Icons page skipped.
- **15 pages** — digital brand (app/web/SaaS) with single-medium imagery. Icons page included.
- **15 pages** — non-digital brand with hybrid imagery. Imagery splits to 2 pages; Icons skipped.
- **16 pages** — digital brand with hybrid imagery. Both Icons + split-Imagery present.

Renumber pages contiguously based on what's included — don't leave gaps.

1. **Cover** — Full-bleed brand-specific layout. Brand name + tagline + hero mood image.
2. **Strategy & Positioning** — Direction, positioning statement, customer, 3-4 reference brands with "borrow this" notes.
3. **Brand Foundation** — Mission, values (3-5), why this exists (story in brand voice).
4. **Logo** — Primary mark + variants (horizontal, icon-only, reversed), usage rules, clear space.
5. **Logo Don'ts** — Misuse rendered in CSS with ✗ labels.
6. **Color** — Swatches with hex+RGB+CMYK, full-bleed color columns (not floating swatches).
7. **Typography** — Full hierarchy with px sizes, display/body specimens, usage rules.
8. **Icons** *(digital brands only)* — 8-12 essential UI icons in brand's geometric style + stroke/corner/grid rules + library recommendation. SKIP this page entirely for non-digital brands; renumber subsequent pages accordingly.
9. **Voice & Tone** — Adjectives + actual brand copy examples by context.
10. **Imagery Rules** — adapts to the brand's primary medium (see "Imagery Rules Page — Adapts per Brand" section below):
    - Photography-led brand → Photography Rules (subject / light / cast / treatment / forbidden) + 1 example photo
    - Illustration-led brand → Illustration Rules (style / color / line / character / composition / forbidden) + 1 example illustration
    - Hybrid brand (both matter equally) → split into two pages, pushing the total to 16 pages
11. **Visual World** — Full-bleed 4-column grid of 4 images (photos and/or illustrations matching the brand's medium choice).
12. **Touchpoints — Real Photos** — 2×2 grid of generated photos showing the brand in physical/digital context. Real images, never CSS boxes.
13. **Brand Applications — CSS Mockups** — Business card, social avatar, sticker, hang tag, woven label, etc. CSS-rendered. Each labeled with specs.
14. **Digital / Social** — Web hero, IG grid (3×3), story template, link-in-bio.
15. **Do & Don't** — 5 dos + 5 don'ts. Brand-specific, actionable.

---

## Step 0 — Workspace Setup

Images and fonts live in a persistent workspace path. `/tmp` is wiped between sessions on many systems, so don't put assets there.

Pick any writable directory. The default below works on Mac, Linux, and inside containers (it resolves `$HOME`, so no hardcoded paths). Override by exporting `BUILD_A_BRAND_WS=/some/other/path` before running, if you have a preferred location (e.g. `~/Downloads/...` or a project-relative `./tmp/build-a-brand`).

```bash
WS="${BUILD_A_BRAND_WS:-$HOME/build-a-brand-workspace}"
mkdir -p "$WS/fonts" "$WS/images"
```

In Python, expand the same way:

```python
import os
WS = os.environ.get('BUILD_A_BRAND_WS') or os.path.expanduser('~/build-a-brand-workspace')
```

Use `$WS/images/lifestyle1.jpg` etc., and `file://$WS/images/lifestyle1.jpg` in HTML (resolve `$WS` to an absolute path before baking into HTML — `file://` URLs don't do shell expansion).
Build the HTML as a separate `.py` script file (e.g., `$WS/build_guidelines.py`) — avoids f-string parsing errors with inline Python heredocs.

---

## Step 1 — Generate Imagery (in parallel batches of 4)

You need **a minimum of 5 generated images**:
- 1 hero mood image (for the cover)
- 1 example image (for the photography rules page)
- 4 lifestyle images (for the visual world grid)
- 4 touchpoints images (for the real photos page) — adapt to brand type

That's 10 images. Run in parallel batches of 4 with `&` + `wait`. Never more than 4 at once (timeouts).

**After every generation, compress before using in PDFs:**
```python
from PIL import Image
img = Image.open(path)
img.thumbnail((1200, 1200), Image.LANCZOS)
img.save(path, 'JPEG', quality=68, optimize=True)
```
Target: under 150KB per image. WeasyPrint silently drops images that are too large — most common cause of missing images.

**Photography prompt template (lifestyle):**
```
[Brand lifestyle direction — who, where, what they're doing, mood]. [Specific moment or activity]. [Environmental details — what's in the room, on the desk, in the background]. [Color temperature]. Film grain, natural light, slight imperfections, editorial composition. No studio strobes, no gradient backgrounds, no perfect symmetry.
```

**Touchpoint prompt template (physical brand):**
```
[Type of touchpoint — hang tag / woven label / kraft mailer / business card / signage]. [Brand visual cues — logo style, color]. [Real-world context — on a garment, on a desk, in a hand]. [Surface, light, color temp]. Editorial photography, film grain, natural light.
```

**Touchpoint prompt template (digital brand):**
```
[Type of touchpoint — phone screen / laptop / tote / sticker]. [Real-world context — in a hand, on a desk, on a water bottle, on a coffee shop table]. [Brand visual cues showing through]. Editorial photography, film grain, natural light.
```

**Diversity rule:** All lifestyle images with people must show a mixed cast across the 4-image grid: Black, Asian, Latina, South Asian, Middle Eastern, or mixed-race subjects. Vary body types. Never default to white/light-skinned subjects.

---

## Image Generation — Hard Rules (Read Before Every Prompt)

These are the failure modes that have burned us before. Apply EVERY prompt.

### 0. Default provider: gpt-image-2

**Every `generate_image` call must pass `provider="gpt-image-2"` unless the user explicitly names a different model.** This is a global preference, not a per-skill rule. Don't default to `nano-banana-pro` (Gemini) — it has worse instruction-following for our brand work and bakes in text more aggressively. Use gpt-image-2 with `quality="medium"` for the default balance of speed and fidelity.

### 1. Never let text bake into the image

Every image model — gpt-image-2 included — WILL render text into generated images when you give them a reason to. Risk is highest when prompts mention "magazine cover," "editorial," "Bloomberg Businessweek," "Vogue," "TIME," "billboard," "poster," "book cover," any real publication name, or any framing that implies typography on the surface.

**Every prompt must end with this guardrail (copy verbatim):**
```
ABSOLUTELY NO TEXT of any kind in the image — no magazine titles, no logos, no watermarks, no captions, no typography, no brand names, no headers. Pure photograph only. No graphic design overlays whatsoever.
```

**Never name real publications or brands directly in a prompt** ("Bloomberg Businessweek cover," "looks like Vogue," "Anthropic launch film"). The model treats these as instructions to reproduce the publication's design — including its name. Instead, describe the *visual qualities* the brand evokes: "editorial close-up portrait with dramatic side light and quiet authority" rather than "Bloomberg Businessweek cover portrait."

### 2. Photo composition must survive the crop you'll use

Before writing the prompt, decide WHERE this photo will appear in the layout and what shape it will be cropped to. Generate a composition that survives that crop:

- **Full-bleed landscape from 3:4 portrait source** → subject must be in the vertical center 60% of the source. The top and bottom 20% will be cropped off.
- **Arched / dome rounded frame (border-radius ≥ ½ of width)** → DON'T use this shape unless the subject is in the LOWER center of the source. The dome will eat the entire top including any head. Default to soft 24-60px corner radius instead.
- **Small landscape inset from 3:4 portrait source** → subject must be in the horizontal center 70%. Sides will crop.
- **Centered portrait subject** → safest. Most layouts can preserve a centered head-and-shoulders composition.

Specify the subject's position in the prompt explicitly: "subject centered in frame, face occupying middle 50% of the image vertically."

### 3. Logos: generate a high-res symbol via gpt-image-2, ship as transparent PNG (no tracing)

Hand-coded SVG symbols look amateur. But also: **don't trace the gen'd symbol to SVG.** Keep the symbol as a high-resolution transparent PNG. Only the wordmark gets vectorized in the brand kit. The pipeline:

1. **Generate the symbol via `generate_image` with `provider="gpt-image-2"`, `quality="high"` (or `"medium"` for first drafts), 1:1 aspect ratio, 1024×1024 minimum.** The symbol can be any style that fits the brand — flat illustration, 3D-rendered, painted, photographic, gradient-rich, chrome, holographic, hand-drawn. No flat-vector requirement. The only constraints are in "Symbol output rules" in `brand-identity.md`. **Always append the no-text guardrail**: "absolutely no text, no letters, no typography, no words, no characters anywhere in the image." gpt-image-2 produces garbled fake text inside logos if you don't explicitly forbid it.
2. **The gen'd symbol must satisfy ALL of:** conceptually linked to the brand (means something about what the brand IS/DOES), feels unique (not generic), recognizable at 16×16, no more than 3 dominant colors, high res (2048×2048+ for the shipped version), no text inside the image, true transparent background. If it fails any of these — regenerate. See `brand-identity.md` "Symbol output rules" for the full list.
3. **Generate 2-3 variations** if appropriate. Show them to the user. Wait for approval before committing. **When generating across the 3 brand-board options, symbols must DIFFER IN CONCEPT, not just style.** Don't ship three "literal mascot face" logos in three styles. See `brand-identity.md` "Symbol concepts must DIFFER across the 3 brand options" for concept lanes (mascot / product-feature reference / abstract / monogram / hybrid / container).
4. **Save as transparent PNG, verified.** True alpha=0 in transparent regions. gpt-image-2 frequently paints near-white pixels in the "transparent" area — verify by sampling corner pixels with PIL (`alpha == 0`). If not, key them out with PIL, or regenerate with a solid background matching the placement surface. See "gpt-image-2 transparent-background caveat" in the QA section. **Do NOT trace to SVG.** The symbol stays as a high-res PNG.
5. **The wordmark is ALWAYS rendered as real text in a Google Font, never baked into a generated image.** Pick the font in the typography step. Render the wordmark via live HTML/CSS for the guidelines pages, and convert to text-as-paths SVG only when packaging the brand kit.
6. **Lockup composition is perfectly measured and permanently fixed.** Pick one horizontal lockup geometry AND one stacked lockup geometry. For each, specify: symbol size (px or em), wordmark font size (px), gap between symbol and wordmark (px), vertical baseline alignment (which point of the symbol aligns with which baseline of the wordmark). **The measurements never change across color variants or contexts** — cream / pink / lime / on-photo / on-dark variants all use the IDENTICAL geometry. Document the exact measurements on the Logo page so a designer or developer can rebuild the lockup without guessing.

**In the brand kit:**
- `symbol-[color].png` — high-res transparent raster at multiple sizes (16, 32, 64, 128, 256, 512, 1024, 2048). NOT vectorized.
- `wordmark-[color].svg` — Google Font text converted to outlined paths (text-as-paths), so the SVG renders identically without the font file installed. PNG version at 1024 wide also included.
- `lockup-[orientation]-[color].svg` — contains the symbol PNG embedded inline + the wordmark as paths, positioned at the locked measurements. PNG version of the assembled lockup at 1024 wide also included.

This rule applies to brand boards (Step 2), the guidelines logo page (Step 3), and the kit's exported logo files (Step 4). Always.

### 4. Verify by screenshot BEFORE delivering

After rendering ANY PDF or board, screenshot every page and read every screenshot. The QA checklist at the bottom of this doc is mandatory. Never deliver based on assumption that the layout worked. Specifically check:

- Are subjects visible (not cropped to forehead, hand-only, etc.)?
- Did baked-in text from the image generator appear anywhere?
- Are rounded shapes / arches cutting off content they shouldn't?
- Did `object-position` show the right portion of the image?

If anything looks wrong, fix it before delivering. Never ask the user to spot problems the agent should have caught.

---

## Step 2 — Choose Fonts (Based on Brand Vibe)

**Fonts are NOT hardcoded.** Select fonts that match the identity built in Step 3 of the main skill. If the fonts could work for a competitor, pick different ones.

### Must Have Character — Don't Default to Safe Fonts

If the brand's display font could appear on any random SaaS site without anyone noticing, it's wrong. Push for fonts with recognizable personality.

**Avoid as display defaults:** Inter, DM Sans, Lato, Karla, Manrope, Outfit, Roboto, Open Sans, Source Sans, Helvetica, Arial. These can be fine as utility body fonts but have no point of view as a display face — they make every brand feel the same.

**Explore the full Google Fonts library with intentionality.** High-character options by vibe:

- **Editorial / archival / literary** → Fraunces (variable serif, sloped descenders), Instrument Serif (literary italic), Newsreader (newspaper character), Spectral, Cardo, Crimson Pro, Bodoni Moda (high contrast modern), EB Garamond
- **Magazine / cover energy / bold display** → Bricolage Grotesque (chunky variable), Big Shoulders Display, Familjen Grotesk, Karantina, Anton (when condensed is core), Funnel Display
- **Friendly / soft / consumer-feeling** → Funnel Display, Funnel Sans, Hanken Grotesk, Schibsted Grotesk, Geist, Hahmlet
- **Tech / mono / digital-native** → Reddit Mono, Geist Mono, JetBrains Mono, IBM Plex Mono, DM Mono, Space Mono, Fragment Mono
- **Playful / loud / personality-forward** → Honk (chubby 3D), Tilt Warp, Tilt Neon, Bagel Fat One, Caveat (handwritten)
- **Quiet / minimal-with-soul** → Public Sans, Hahmlet, Newsreader (light weights), Spectral (light weights)

### No favorite fonts — every brand starts the search fresh

There is no "house font" for this skill. No font is a default. No font is banned either — every font on Google Fonts is still in the running for the right brand, including ones used on previous brands. What's forbidden is the *pattern*: reaching for the same fonts across unrelated brands because they worked last time.

Run the selection from scratch every brand. The fact that Sansita, Fraunces, Funnel Display, Bagel Fat One, etc. fit a past brand doesn't make them the right pick for this one — and it doesn't disqualify them either. The question is always "what UNIQUELY fits this brand's vibe?", run fresh.

### The mandatory research step — do this every brand, every time

Google Fonts hosts ~1500 families. The failure mode is selecting from a tiny mental shortlist of ~20 fonts that worked before. Force a real search:

1. **Name the brand's vibe in 3-5 specific adjectives** ("warm, archival, slightly weird, with restraint"). The adjectives are the brief; the font search runs against them.
2. **Brainstorm 5+ candidates from at least 3 different categories** — serif / sans / mono / display / script / slab / stencil. Don't pre-filter to fonts you remember liking; widen the net first, narrow after.
3. **Pull at least 2 less-obvious options into the shortlist** — Eczar, Workbench, Bungee Shade, Climate Crisis, IM Fell DW Pica, Krona One, Suez One, Yeseva One, Tilt Prism, Italiana, Stardos Stencil, Inria Serif, Ribeye Marrow, etc. These don't get picked because they're weird; they get picked when the brand is the one that wants them.
4. **Cross-brand variety check.** Before locking the choice, ask: "Have I reached for this font on a recent brand?" If yes, you need a real reason this brand specifically wants the same font — not just "it worked before." If you can't articulate why this brand uniquely wants it, pick a different fresh option that fits as well.
5. **Sanity check:** would 5 brands in unrelated industries reach for this font? If yes, it's too generic — keep looking.
6. **Pick** the one that UNIQUELY fits this brand's vibe.

### Wider library by vibe — go beyond the top tier

Use these as starting points only, not automatic defaults. The point is to widen your candidate pool every brand.

- **Editorial / archival / literary** → Vollkorn, EB Garamond, Crimson Pro, Newsreader, Spectral, Cardo, Eczar, Inria Serif, Petrona, Faustina, Libre Caslon Text, Libre Baskerville, IM Fell DW Pica, Old Standard TT, PT Serif
- **Magazine / cover energy / bold display** → Bricolage Grotesque, Big Shoulders Display, Familjen Grotesk, Karantina, Yeseva One, Suez One, Krona One, Italiana, Workbench
- **Heavy display / chunky / 3D** → Honk, Bungee, Bungee Shade, Bungee Inline, Climate Crisis, Lilita One, Bowlby One, Modak, Alfa Slab One, Workbench, Ribeye, Ribeye Marrow
- **Slab / vintage / sturdy** → Aleo, Bitter, Arvo, Rokkitt, Zilla Slab, Roboto Slab, Saira Stencil One, Stardos Stencil, Sancreek (western), Rye, Smokum
- **Friendly / soft / consumer** → Lilita One, Albert Sans, Plus Jakarta Sans, Onest, Quicksand, Comfortaa, Nunito Sans, Mulish, Mona Sans
- **Tech / mono / digital-native** → Reddit Mono, Geist Mono, IBM Plex Mono, Space Mono, DM Mono, Fragment Mono, Anonymous Pro, B612 Mono, Major Mono Display, Cutive Mono, Inconsolata, Fira Code, Cousine
- **Playful / weird / personality-forward** → Honk, Tilt Warp, Tilt Neon, Tilt Prism, Workbench, Iceland, Limelight, Knewave, Climate Crisis, Permanent Marker, Caveat, Indie Flower, Cinzel Decorative
- **Old style / classical / serious** → IM Fell DW Pica, Cinzel, Cardo, Old Standard TT, Vollkorn, Italiana, EB Garamond, Inria Serif, Stardos Stencil
- **Script / handwriting** → Lobster, Lobster Two, Pacifico, Sacramento, Caveat, Indie Flower, Permanent Marker, Allura, Great Vibes, Berkshire Swash, Yellowtail
- **Quiet / minimal-with-soul** → Public Sans, Hahmlet, Newsreader light, Spectral light, Inria Sans, Albert Sans, Onest

### Pairing rules

- Display font must have character. Body font can be quieter but should still feel intentional.
- Never pair two characterless fonts (Inter + DM Sans = no point of view).
- Display + body should feel related but distinct.
- Test: if you swapped this brand's display font with another brand's display font from your last 3 projects, would anyone notice? If no — pick a more characterful one.

### Decision Framework

**Headline font feeling:**
- Striking / loud / high-energy → bold condensed (Bebas Neue, Druk, Anton, Oswald, Archivo Black)
- Precious / archival / collected → elegant serif (Cormorant Garamond, Playfair Display, EB Garamond)
- Tech / app / digital-native → geometric sans (Space Grotesk, DM Mono, Syne, Monument Grotesk)
- Handmade / artisan / craft → warm serif (Libre Baskerville, Lora, Bitter)
- Clean / editorial / grown-up minimal → geometric humanist (Jost, Raleway, Josefin Sans)
- Playful / cute / youth → friendly rounded (Nunito, Poppins, Quicksand)

**Body font must contrast with headline:**
- Serif headline → clean sans body (Lato Light, DM Sans, Inter)
- Bold condensed headline → lightweight sans (DM Sans, Lato Light, Inter)
- Geometric sans headline → same family lighter weight, or Inter

### Download fonts to workspace

```bash
WS="${BUILD_A_BRAND_WS:-$HOME/build-a-brand-workspace}"
mkdir -p "$WS/fonts"
# example — download the fonts you've selected:
curl -sL "https://github.com/google/fonts/raw/main/ofl/syne/Syne%5Bwght%5D.ttf" -o "$WS/fonts/Syne.ttf" &
curl -sL "https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf" -o "$WS/fonts/PlayfairDisplay.ttf" &
curl -sL "https://github.com/google/fonts/raw/main/ofl/karla/Karla%5Bwght%5D.ttf" -o "$WS/fonts/Karla.ttf" &
wait
```

Declare in CSS via `@font-face` only (`@import` or `<link>` cause 30s+ render timeouts in WeasyPrint and unreliable loading in Chrome headless). Resolve `$WS` to an absolute path in your HTML-generator script, then bake it in via f-string:

```python
# In your HTML-builder script:
css = f"""
@font-face {{ font-family: 'Syne'; src: url('file://{WS}/fonts/Syne.ttf'); }}
@font-face {{ font-family: 'Karla'; src: url('file://{WS}/fonts/Karla.ttf'); }}
"""
```

Always use **absolute file:// paths**. Never relative. Never `@import url(...)` from Google Fonts.

---

## Step 3 — Build HTML

Write a fresh Python script (e.g., `$WS/build_guidelines.py`) that emits the HTML to `$WS/guidelines.html`. Never copy old deck HTML — always write fresh.

**Critical CSS (required in every guidelines doc):**
```css
@page { size: 1200px 850px; margin: 0; }
.page { width: 1200px; height: 850px; overflow: hidden; page-break-after: always; display: block; }
```

### WeasyPrint Hard Rules — Read Before Writing a Single Div

WeasyPrint's flexbox engine is severely broken. `display:flex` fails silently — columns collapse to zero width and content disappears with no error message. This is the #1 cause of blank pages.

#### Rule 1: No flex anywhere
- **NEVER** `display:flex` on `.page`, on header bars, on two-column rows. Nowhere.
- **For all multi-column layouts: use `<table>` elements** with explicit `width` and `height` on every `<td>`.
- **For `.page`: use `display:block`**.
- **Header bar template**: `<table style="width:1200px;height:68px;border-collapse:collapse;">` with two `<td>` cells.
- **Two-column content template**: `<table style="width:1200px;height:782px;border-collapse:collapse;table-layout:fixed;">`.
- **Column widths must add up to 1200px exactly.** Always verify.
- **CSS `display:grid` is acceptable** for internal item arrangements (swatches, mockup grids, type specimens). NOT for page structure.

#### Rule 2: `vertical-align:middle` is unreliable
Even with real `<table>` elements + explicit heights, `vertical-align:middle` often renders content at the top.

**For full-page content centering**: nested table pattern — outer table 782px, inner table auto-height, `vertical-align:middle` on outer td. Works when inner content has NO explicit height.

**For shapes (logo mockups, hang tags, circles, labels)**: never use `vertical-align:middle`. Always use explicit `padding-top`:
```
padding-top = (shape_height - estimated_content_height) / 2
```

#### Rule 3: `position:absolute` is unreliable
Inside fixed-height shapes, `position:absolute` does not render reliably — elements appear in document flow. Replace with table rows or `padding-top`.

#### Rule 4: Image rules
- Always explicit px dimensions: `style="width:300px;height:400px;object-fit:cover;display:block;"`
- Never `height:100%` or `width:100%` — WeasyPrint cannot resolve percentage heights
- Never `opacity:` on any `<img>` — images always at full opacity
- Never text/overlay on images — put captions in an adjacent column or block
- Never duplicate an image src across the deck — each file appears at most once
- Compress to under 150KB before render

#### Rule 5: Text contrast thresholds on dark backgrounds
On graphite (#2E2E2E) or any dark background:
- Body text minimum: `rgba(248,243,236,.7)`
- Sub-descriptions minimum: `rgba(248,243,236,.55)`
- Decorative / ghost text minimum: `rgba(248,243,236,.45)` — below this, remove the element entirely
- `.3` opacity on dark = invisible. Never use for any visible text.

#### Rule 6: Page overflow prevention
- Every page is 850px tall. All content MUST fit.
- If a page has a headline >60px AND more than 3 body paragraphs, it will overflow. Cut or split.
- Never more than ~220 words of body text on a single page.
- Padding: 64px top/bottom max on content pages. Don't stack multiple padded sections.

#### Rule 6b: Content must not bleed into the footer (Chrome --print-to-pdf path)
When the brand guidelines deck is rendered via Chrome `--print-to-pdf` (not WeasyPrint), the footer is typically `position: absolute; bottom: 18px` and the main content is in normal flow. If main content extends past the available content height, it visually overlaps the footer text — Monica caught this on the koalacore Voice page (2026-05-22).

**Mandate for Chrome `--print-to-pdf` page builds:**
- `.content` (the main page area between header and footer) MUST have an explicit `height: calc(850px - HEADER_HEIGHT - FOOTER_HEIGHT)` (or a similar max-height) AND `overflow: hidden` as a safety net.
- This way, even if a content block grows unexpectedly, the layout clips at the content boundary instead of bleeding into the footer.
- Treat it as a guardrail, not a target — the goal is still to fit content within the available height. But the overflow:hidden prevents accidental overlap when content density is hard to predict.

#### Rule 7: Vertical centering critical gotcha
When using `<table><tr><td style="vertical-align:middle;">` to center, the inner content div **must NOT have explicit height**. If the inner div has `height:782px` (same as td), the td has nothing to center → appears top-aligned. Set `height` only on the outer `<td>`, never on the inner content div.

### Reusable Templates

**Two-column content page:**
```html
<div style="width:1200px;height:850px;overflow:hidden;page-break-after:always;display:block;background:#F8F3EC;">
  <!-- Header bar -->
  <table style="width:1200px;height:68px;border-collapse:collapse;border-bottom:1px solid rgba(0,0,0,.07);">
    <tr>
      <td style="padding:0 52px;vertical-align:middle;"><span style="font-size:9px;letter-spacing:.42em;text-transform:uppercase;color:#C4B49A;">01 — Section Label</span></td>
      <td style="padding:0 52px;vertical-align:middle;text-align:right;"><span style="font-style:italic;color:#C4B49A;">optional quote</span></td>
    </tr>
  </table>
  <!-- Two-column body -->
  <table style="width:1200px;height:782px;border-collapse:collapse;table-layout:fixed;">
    <tr>
      <td style="width:480px;height:782px;vertical-align:top;padding:0;overflow:hidden;">
        <img src="file:///..." style="width:480px;height:782px;object-fit:cover;display:block;">
      </td>
      <td style="width:720px;height:782px;vertical-align:middle;padding:52px;background:#2E2E2E;">
        <!-- right column text content -->
      </td>
    </tr>
  </table>
</div>
```

**Full-bleed lifestyle grid (page 10):**
```html
<table style="width:1200px;height:782px;border-collapse:collapse;table-layout:fixed;">
  <tr>
    <td style="width:300px;height:782px;padding:0;overflow:hidden;"><img src="file:///..." style="width:300px;height:782px;object-fit:cover;display:block;"></td>
    <td style="width:300px;height:782px;padding:0;overflow:hidden;"><img src="file:///..." style="width:300px;height:782px;object-fit:cover;display:block;"></td>
    <td style="width:300px;height:782px;padding:0;overflow:hidden;"><img src="file:///..." style="width:300px;height:782px;object-fit:cover;display:block;"></td>
    <td style="width:300px;height:782px;padding:0;overflow:hidden;"><img src="file:///..." style="width:300px;height:782px;object-fit:cover;display:block;"></td>
  </tr>
</table>
```

**Touchpoints 2×2 grid (page 11):**
```html
<table style="width:1200px;height:782px;border-collapse:collapse;table-layout:fixed;">
  <tr>
    <td style="width:599px;height:390px;padding:0;overflow:hidden;"><img src="file:///..." style="width:599px;height:390px;object-fit:cover;display:block;"></td>
    <td style="width:1px;background:#fff;"></td>
    <td style="width:600px;height:390px;padding:0;overflow:hidden;"><img src="file:///..." style="width:600px;height:390px;object-fit:cover;display:block;"></td>
  </tr>
  <tr><td colspan="3" style="height:2px;background:#fff;padding:0;"></td></tr>
  <tr>
    <td style="width:599px;height:390px;padding:0;overflow:hidden;"><img src="file:///..." style="width:599px;height:390px;object-fit:cover;display:block;"></td>
    <td style="width:1px;background:#fff;"></td>
    <td style="width:600px;height:390px;padding:0;overflow:hidden;"><img src="file:///..." style="width:600px;height:390px;object-fit:cover;display:block;"></td>
  </tr>
</table>
```

### Page-Specific Notes

**Page 1 (Cover) — must make the product unambiguous.** The cover hero photo + subtitle together must answer "what is this?" with zero ambiguity. For digital products (apps, services, software): the hero photo must show the product IN USE — a phone or device displaying the actual result of using the product, OR a person in the moment of using it. NEVER use a representational object (a charm, a token, a packaging mockup, a logo-shaped artifact) as the cover hero — it makes the brand look like it sells that object instead of the actual product. The cover subtitle should communicate what the thing IS in the brand's voice — clarity through content, never robotic templates.

**Page 2 (Strategy) — product clarity sentence required, in brand voice.** Within the first 80 words of the Strategy page, the reader must understand what the product literally IS. Communicated in the brand's tone, not a robotic format. "Koalacore is an app that…" is robotic; "It's an app. You pick a photo. We drop a koala in. The end." is on-brand. Either form works — what's required is that a reader who lands on this page knows what the product is by the end of the opening paragraph. NEVER substitute "what we believe" or "what we stand for" for "what we are."

**Page 4 — Logo applications:** Left half (~420px) = large logo mark centered with generous whitespace. Right half (~780px) = 5 CSS mockups in a 2-row grid (3 top, 2 bottom), `gap:32px`, each cell min 160×180px. Don't flex-wrap — use proper grid.

**Page 5 — Logo Don'ts:** 5 violation tiles in a row, each with the wrong-usage logo + a small ✗ label + a one-line caption explaining the violation.

**Page 9 — Photography Rules:** Left 2/3 (~780px) = 3 example images in a grid with explicit pixel dimensions. Right 1/3 (~420px) = sidebar of 4-5 specific rules (surface, light, propping, editing, mood). Small label caps + body text.

**Page 11 — Touchpoints:** The page **must show real generated photos** of the brand in context. Never substitute CSS vector mockups. Generate the 4 images before building HTML. For physical product brands: hang tag, woven label macro, kraft mailer, flat lay. For digital brands: phone showing app, laptop showing site, sticker, tote bag. For service brands: business card in hand, signage, branded notebook, swag.

**Page 12 — Brand Applications (CSS mockups):** Each mockup is a small physical-object representation rendered in CSS. Use explicit `padding-top` centering — never `vertical-align:middle` inside fixed-height shapes.

| Shape | Dimensions | Suggested padding-top |
|---|---|---|
| Hang tag | 120×168px | ~31px in body row |
| Woven label | 200×80px | ~13px |
| Avatar circle | 100×100px | ~22px |
| Sticker rounded square | 100×100px | ~18px |
| Business card | 200×120px | ~35px |

### Image hard constraints

- **No opacity on images.** Never `opacity:` on any `<img>` — full brightness always.
- **No text on images.** No `position:absolute` to overlay text/elements on images. Captions go in an adjacent column.
- **No gradient overlays.** No `background:linear-gradient(...)` divs positioned over images.
- **No duplicate images.** Each image file appears at most once across the deck. If you run out, replace with typographic or color design elements (large CG italic quote, big page number, color field) — never reuse.
- **Remove all price stickers / shelf labels / tags** from products before use. If source has a Goodwill sticker or similar, regenerate clean.
- **Header logo on every page uses the brand's actual logo font/style** — never a generic fallback.
- **Generated lifestyle images must match the brand's specific aesthetic** — not just "editorial." Define surface/light/color-temp/prop-types per brand before generating. A warm cozy apartment is wrong for a gritty brand; harsh concrete is wrong for a quiet-luxury brand. Regenerate if it doesn't match.

---

## Step 4 — Render PDF Locally

**Preferred: Chrome headless.** Chrome handles modern CSS, flexbox, grid, and `@font-face file://` font declarations reliably when run locally. Use it when available:

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WS="${BUILD_A_BRAND_WS:-$HOME/build-a-brand-workspace}"
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --virtual-time-budget=8000 --no-pdf-header-footer \
  --print-to-pdf="$WS/guidelines.pdf" \
  "file://$WS/guidelines.html"
```

**Fallback: WeasyPrint.** Use this only when Chrome is unavailable or the HTML was written to the table-only constraints above:

```python
import weasyprint, warnings, os
warnings.filterwarnings('ignore')

WS = os.environ.get('BUILD_A_BRAND_WS') or os.path.expanduser('~/build-a-brand-workspace')
pdf = weasyprint.HTML(filename=f'{WS}/guidelines.html',
                       base_url=f'file://{WS}/').write_pdf()
open(f'{WS}/guidelines.pdf', 'wb').write(pdf)
print(f'guidelines: {os.path.getsize(f"{WS}/guidelines.pdf")//1024}KB')
```

Use the Python API, not the CLI — CLI has font resolution issues.
Pick one engine and stick with it for the whole 14–16-page build.

---

## Verify Every Page (Mandatory — sub-step within Step 3 guidelines build)

Before delivery, screenshot every page and verify against the QA checklist.

```python
# Screenshot every page — run this after every render
import fitz, os
WS = os.environ.get('BUILD_A_BRAND_WS') or os.path.expanduser('~/build-a-brand-workspace')
doc = fitz.open(f'{WS}/guidelines.pdf')
for i in range(len(doc)):
    doc[i].get_pixmap(matrix=fitz.Matrix(1.8,1.8)).save(f'{WS}/qa_p{i+1}.png')
print(f'{len(doc)} pages — now read each one')
```

```python
# Corner-sample verification — catches blank columns
import fitz, os
WS = os.environ.get('BUILD_A_BRAND_WS') or os.path.expanduser('~/build-a-brand-workspace')
doc = fitz.open(f'{WS}/guidelines.pdf')
for i, page in enumerate(doc):
    pix = page.get_pixmap(matrix=fitz.Matrix(1,1))
    w, h = pix.width, pix.height
    s = pix.samples
    def px(x,y): return (s[(y*w+x)*3], s[(y*w+x)*3+1], s[(y*w+x)*3+2])
    corners = [px(10,10), px(w-10,10), px(10,h-10), px(w-10,h-10)]
    print(f'P{i+1}: {corners}')
    # white (255,255,255) corner on a dark page = blank column bug
```

### Pre-Send QA Checklist

Read every screenshot. Verify every item. If any check fails, fix it. No exceptions. Never ask the user to spot problems the agent should have caught.

**Three-pass QA is mandatory for multi-page brand guidelines (Step 3). Glancing at the full-page PNG is NOT zoom-reading — it's pass 1.**
1. **Render-every-page pass** — render EVERY page in the 14–16-page deck to PNG individually (not just one or two). Open and READ each PNG full-size. If ANY page is blank, has overlapping text, missing content, or wrong rendering, fix and re-render that page before continuing. A blank page in the deliverable is a hard ship-block. **Each page is verified individually before the merge.**
2. **Thumbnail pass** — full-page screenshots to catch layout-level issues (blank columns, missing content, wrong colors). The 1200×850 PNG read at standard screen size is the thumbnail pass. Do NOT confuse this with zoom-reading.
3. **Zoom pass — MANDATORY CROP-AND-READ, NOT GLANCE.** Use PIL to crop the rendered PNG into 800×800 regions around every text-bearing area: page title, subtitle, every section header, every body block, every card pull-quote, every label, every hex code, every footer. **Read each crop individually.** This is the only way to catch borderline contrast, shade/3D font issues, footer overlap with content, and text-wrap failures — those issues all compress out of view at thumbnail scale. If you find yourself ready to ship without having opened named `zoom-{page}-{region}.png` files, you HAVEN'T done the zoom pass. Go back. (The agent has shipped twice claiming to have zoom-read when really it only glanced at the full PNG. The rule is now: zoom-read = generate crops + Read each crop file. No shortcut.)

**Specifically zoom-read (crop into 800×800 and Read each):**
- Cover hero copy + subtitle
- Every page's top breadcrumb header (the brand wordmark at small scale)
- Every page's footer band (look for footer-text overlapping page content)
- Every "pull" or display-pull-quote block on every page
- Every card title + body on cards with saturated backgrounds (pink cards especially)
- Every text-on-photo region
- Every swatch label + hex code
- Every IG grid quote tile
- Every small mockup label (app icon caption, splash subtitle, etc.)

**Contrast gate — every text/background pair must be verifiably legible.** Before delivery, audit every text-on-color combination across all pages. Auto-fails: pink text on pink background, lime text on cream background, dark text on dark photo, any small text whose color is within 25% luminance of its container background. When in doubt, run the pair through a contrast checker (4.5:1 minimum for body text, 3:1 for large display type). If even one text block fails contrast — fix it. Pink-on-pink is the most common failure; resolve by either (a) darkening the text to a deep accent, (b) lightening the background to cream, or (c) putting a contrasting card behind the text.

**Complex fills (chrome / holographic / multi-stop gradients) only at hero scale.** Multi-stop chrome / holographic / iridescent gradients on display type read clean at hero scale (60px+) but **muddy at small scale** (under ~24px) — the gradient stops compress into smudge and the type becomes hard to read. When a type style appears at multiple scales in the system (e.g. the brand wordmark on the cover hero AND in the small page-header breadcrumb), use the complex fill ONLY at hero scale, and switch to a solid color (with optional stroke) at small scale. Document both versions on the Logo page so the system has the right tool at every size.

**Same rule for shaded / 3D / decorative display fonts** — `BungeeShade`, `Honk`, `Bungee Inline`, `Bungee Outline`, `Workbench`, `Tilt Prism`, any font with built-in shadow / 3D / chrome / outline detail baked into the glyph design. These fonts have visible "shade" or "3D depth" portions inside each letter; at small/medium scale (under ~40px) those portions compress into mud, AND when used on a saturated background, the shade portion can render as a color that blends INTO the background — creating an apparent contrast failure where parts of letters disappear (pink BungeeShade on pink reads as pink-on-pink even when the letter face is cream). **Use shaded display fonts ONLY at hero scale (40px+) AND prefer cream/black backgrounds at any scale.** At smaller scales OR on saturated brand backgrounds, switch to the brand's flat sans (Onest Black, Plus Jakarta 900, etc.) for the same visual hierarchy with clean contrast.

**Test before shipping:** if the brand has a chunky display font (BungeeShade, Honk, etc.) and you're using it under 40px or on a hot-color background, render the page and zoom in on the letterforms. If you can see the shade/3D detail picking up the background color in any portion of any letter — switch to flat sans.

**Zoom-read every text-containing region, not just logos.** Specifically: numbered/lettered pill markers, button states, favicon-size logo renderings, color-swatch hex labels, type specimens, business card layouts, single-character badges, **hero taglines, decorative strips, callout banners, brand-name headers, voice-sample blocks, and any badge/sticker with text.** Anywhere text sits in a fixed-width container is a wrap risk — verify it stayed on the line you intended. A trailing word, comma, or star alone on its own line is a layout failure.

**Logo lockup centering check.** When a generated logo sits inside a circular or rounded frame: confirm the symbol is visually centered, not pushed to a corner by `object-fit: cover` revealing an off-center source comp. If the source image has a strong asymmetric mass (e.g. ears on top, body below), `object-fit: cover` will cut it badly. Use `object-fit: contain` on a transparent PNG, or remove the frame and let the source image's own composition speak.

**gpt-image-2 transparent-background caveat.** When generating logos with "transparent background" in the prompt, gpt-image-2 frequently outputs a literal painted checker pattern or near-white pixels in the "transparent" areas — NOT true alpha=0 transparency. Before placing on a colored card, **verify true transparency**: sample corner pixels with PIL and confirm `alpha == 0`. If not, either (a) key out the near-white pixels with PIL to true transparent, or (b) regenerate with a solid color background that matches the surface you'll place the logo on.

| Check | What to look for |
|---|---|
| Fonts loaded | Headlines render in the chosen font, not a system fallback (Times, Arial) |
| No blank columns | Every column has content — no white/solid blocks where text should be |
| No text on images | No overlaid headlines, labels, or divs sitting on top of any image |
| **No baked-in text in generated images** | **Open each generated image and look for ANY text — magazine titles, watermarks, brand names, captions, headers. If you see any, regenerate with stronger no-text guardrails.** |
| **Subjects survive their crop** | **For every generated image used in a layout: is the intended subject visible after the CSS crop? No forehead-only portraits, no hand-only kitchen scenes. If the subject got cut off by `object-fit:cover`, `object-position`, or a rounded/arched frame, fix the layout or regenerate the image.** |
| **Rounded shapes don't eat content** | **Any `border-radius` ≥ ½ the element width creates a dome that crops content underneath. If the photo's subject sits in the top portion of the source, a dome top will hide it. Soften the radius or reposition the subject.** |
| No duplicate images | Each image file used at most once across the deck |
| No opacity on images | No `opacity:` on any `<img>` — images always full brightness |
| Logo shapes centered | Content visually centered in hang tags, circles, labels — not top-aligned |
| Text contrast | All text on dark (#2E2E2E) backgrounds at sufficient opacity |
| Decorative text legible | Ghost / watermark text at ≥ .45 opacity — if lower, remove entirely |
| Images load | No broken images — every img has explicit px width+height |
| Page count = 14–16, conditionally correct | Non-digital/single-medium = 14; digital/single-medium = 15; non-digital/hybrid = 15; digital/hybrid = 16; no blank extras |
| Touchpoints are real photos | Page 12 shows generated photographs, not CSS vector boxes |
| Diverse cast | Lifestyle grid (page 11) shows racial diversity across subjects |
| Icons consistent | Page 8 icons all use the same stroke weight + corner style + line caps |
| Imagery medium matches brand | Page 10 reflects the brand's medium (photo / illustration / hybrid) — don't ship Photography Rules for an illustration brand |
| No concept clichés | No hourglass-for-time / lightbulb-for-ideas / handshake-for-trust etc. — apply the three cheesiness tests |

Only deliver after all checks pass.

---

## Step 6 — Deliver

Save the final PDF to `~/Desktop/[brand-slug]-brand-guidelines.pdf` and send the local path in a single message. Do not upload or host the PDF unless the user explicitly asks for a hosted copy.

```bash
cp "$WS/guidelines.pdf" "$HOME/Desktop/[brand-slug]-brand-guidelines.pdf"
```

Reply shape:

```
**[BRAND NAME] — brand guidelines**
Saved to: ~/Desktop/[brand-slug]-brand-guidelines.pdf ([actual page count] pages · 1200×850 · ~5MB)
```

If the user is not on a Mac, save to the project working directory and emit that path instead. Never attach the PDF as a file in the chat — link by path only.

Done.

---

## Image Concept Must Connect to the Brand Metaphor (Don't Default to "Person Doing X")

Before generating any image, identify the brand's central metaphor — the verb or noun the brand keeps returning to. For DeltaStream → "stream" (water, motion, flow, time). For a coffee brand → "ritual" (steam, pour, slow). For a sleep app → "rest" (stillness, breath, dark warmth).

Then, for each direction, propose a visual concept that USES that metaphor in a FRESH way. The most common failure mode is defaulting to "person at desk" or "person using product" three times in a row. That looks stocky and unbranded — three engineers at three desks, even with different palettes, reads as three variations of the same image.

### Steps to follow every time

1. **Name the brand metaphor.** Write it down (e.g. "stream = flow / motion / time / water").
2. **For each of the 3 directions, brainstorm 3 different image concepts that use the metaphor** through a different medium or subject. Pick the most ownable.
3. **Vary the medium across the 3 boards.** Mix:
   - Photographs (documentary / editorial / macro / long-exposure / portrait / still life)
   - Illustrations (flat vector, line art, gradient, isometric, geometric)
   - Abstract compositions (typographic posters, color fields, motion studies)
   - Architectural / environmental shots
4. **Specify the medium AND the concept in the prompt.** "Flat vector illustration of..." vs. "Editorial macro photograph of..." vs. "Long-exposure photograph of...".

### Examples (for a "stream" brand)

- **Cover Story (bold manifesto)** → Editorial macro photograph of glowing amber liquid frozen mid-pour, single dramatic light. Stream metaphor = literal liquid stream, captured in a moment.
- **First Light (soft consumer)** → Flat vector illustration of a stylized sunrise over geometric waves in butter yellow and cream. Stream metaphor = waves of light + flow.
- **Slow Burn (quiet editorial)** → Long-exposure photograph of city traffic light trails on a wet dark street at night, rust tail lights as the only accent. Stream metaphor = streams of light through time.

Three different MEDIUMS (macro photo / vector illustration / long-exposure photo). Three different SUBJECTS. All rooted in "stream" but used distinctly. None of them are "person doing X."

### When illustration beats photography

Default to illustration (over photography) when:
- The brand is consumer-feeling, app-like, or has Bumble/Notion/Pika DNA → flat illustration reads warmer and more ownable than stock-photo people
- The concept is abstract or symbolic (a feeling, a state, a moment) — illustration can render concepts photography cannot
- The brand has a strong color palette and you want it to dominate the image — illustration controls color absolutely
- The aesthetic is playful, soft, or geometric — photography would feel like a mismatch

Default to photography when:
- The brand is editorial, archival, premium, or grown-up
- The concept is tactile (an object, a material, a texture)
- The mood is documentary or quiet (Frank Ocean / Anthropic territory)

### What NOT to do

- Three "person at desk" with different palettes
- Three "person using product" with different lighting
- Three "engineer at laptop" — the stock photo zone
- Defaulting to portraits when an object, illustration, or abstract composition would say more
- Generating photography when illustration would serve the brand better

---

## Icons Page — Structure & Rules

**⚠️ Conditional page — only build this for DIGITAL brands.** Skip entirely if the brand is a physical product, restaurant, fashion line, service business, or any non-software brand. For those, a UI icon system is irrelevant noise — the page would feel forced.

**Include the Icons page if the brand is:** an app, a web tool, a SaaS product, a software platform, a digital community, a website-as-product, or anything where users interact via UI.

**Skip the Icons page if the brand is:** a physical product, fashion, food/beverage, restaurant, hospitality, service business, consultancy, agency, or any brand whose surfaces are mostly physical / printed / packaging-driven.

If you're not sure, ask the user in Step 1: "Is this a digital product?" (this question should already be in your intake).

When included, page 8 defines the brand's UI icon system.

### Page layout

- **Header bar** (standard section label + page num + brand symbol)
- **Headline** (top): a 38-44px brand-styled headline like "Icons" or "A consistent UI language"
- **Rules block** (left third, ~380px):
  - **Stroke weight** — e.g. `1.5px` / `2px` / `3px` based on brand character (thinner = editorial / refined; thicker = friendly / consumer)
  - **Corner radius** — sharp / soft 2px / round 4px / fully rounded
  - **Line caps** — round / butt / square (round for friendly brands; butt for technical/precise)
  - **Style** — outline / filled / two-tone / mixed
  - **Grid** — 24×24 base / 32×32 base (24 is standard; 32 for larger UI)
  - **Stroke ends / corners consistency** — same treatment across all icons
- **Icon grid** (right two-thirds): 4×3 grid of 12 icons, each in a `~120×120px` tile
- **Bottom note**: library recommendation for icons beyond the set — e.g. "Use Phosphor Light for any icon not in this set" or "Use Lucide at 1.5px stroke."

### The 12 essential UI icons

Every brand's icon set should include at minimum:

| Icon | Use |
|---|---|
| arrow-right | navigation, "see more" |
| arrow-down | dropdown, expand |
| check | confirmation, success |
| close (×) | dismiss, close |
| plus | add, new |
| minus | remove |
| search | search/find |
| user | profile, account |
| settings (gear) | settings, preferences |
| bell | notifications |
| menu (hamburger) | mobile nav |
| info (circle-i) | helper tooltip |

These cover 80% of UI needs. Brands with specific product features can add 2-4 product-specific icons (e.g. a streaming brand might add a "live" indicator; a finance brand might add "card" / "wallet").

### Stroke style choice by brand vibe

- **Bold editorial / display-heavy brand** → 2-2.5px stroke, sharp corners, butt line caps. Looks intentional and precise.
- **Friendly / consumer / Bumble-Pika DNA brand** → 2px stroke, soft 2-3px corner radius, ROUND line caps. Looks warm and approachable.
- **Technical / dev-tool brand** → 1.5px stroke, sharp corners, butt caps. Looks precise like the rest of the brand.
- **Editorial / quiet / Anthropic-Modal brand** → 1.5px stroke, sharp corners, butt caps. Reads as refined.
- **Playful / heavy display brand** → 2.5-3px stroke, round corners, round caps. Echoes the chunky type.

Pick the stroke style at the same time as the brand's identity, and apply it consistently across all 12 icons.

### Rendering each icon

Each icon is a 24×24 viewBox SVG with the brand's chosen stroke weight and corner style. Example structure (for arrow-right at 1.5px stroke, sharp corners, butt caps):

```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="butt" stroke-linejoin="miter">
  <path d="M5 12 L19 12"/>
  <path d="M13 6 L19 12 L13 18"/>
</svg>
```

Use `currentColor` for the stroke so the icon adopts the surrounding text color (essential for color-flexible UI usage).

### What goes in the brand kit

A `/icons/` folder containing all 12 (or more) icons as SVG files:
- `icons/arrow-right.svg`
- `icons/check.svg`
- `icons/close.svg`
- `icons/plus.svg`
- `icons/search.svg`
- `icons/user.svg`
- `icons/settings.svg`
- `icons/bell.svg`
- `icons/menu.svg`
- `icons/info.svg`
- (etc — full set used on page 8)

Each SVG with `stroke="currentColor"` so it inherits color from the application context.

---

## Imagery Rules Page — Adapts per Brand

Page 9 of the guidelines defines the brand's imagery rules. **Its title and content adapt to whatever medium the brand actually uses** — don't ship a "Photography Rules" page for an illustration-led brand and don't ship "Illustration Rules" for a brand that lives in photos.

### How to decide which page(s) to build

Look at the chosen identity option's specs (set in Step 3) and the lifestyle world you've defined:

| Brand visual medium | Page 9 setup |
|---|---|
| All photography (no illustration anywhere) | Page 9 = Photography Rules (single page) |
| All illustration (no photography anywhere) | Page 9 = Illustration Rules (single page) |
| Hybrid — both matter equally in the brand world | Page 9a = Photography Rules, Page 9b = Illustration Rules (two pages → guidelines totals 15) |
| Hybrid — one medium dominates but the other appears occasionally | Page 9 = the dominant medium's rules, with a short "minor medium" callout block at the bottom |

### Photography Rules page structure

If the brand uses photography:
- **Subject** — who/what is in the frame (real engineers / hands at work / still life / etc.)
- **Light** — direction, quality, time of day
- **Color** — grade, palette tones preserved, anything muted
- **Cast / diversity** — explicit rule that lifestyle images with people show racial diversity across the set
- **Texture** — film grain, composition style, off-center editorial framing
- **Forbidden** — stock-photo energy, studio strobes, perfect symmetry, AI-smooth surfaces, gradient backgrounds
- **One example image** filling 2/3 of the page (real generated photo in the brand's photo style)

### Illustration Rules page structure

If the brand uses illustration:
- **Style** — flat vector / line art / geometric / hand-drawn / 3D render / collage / mixed. Be specific (e.g. "flat vector with no realistic detail" not just "illustrated").
- **Color** — how brand colors apply to illustrations (large fields vs accent dots; how many colors per illustration; palette restraint)
- **Line / stroke** — stroke weight rules (uniform 4px / varied / no strokes); corner radius (rounded / sharp); line caps (round / butt / square)
- **Character** — what the illustrations feel like (friendly / precise / playful / archival / geometric / organic). Match the brand's overall voice.
- **Composition** — asymmetric / centered, generous negative space / dense, rule-of-thirds / centered subject
- **Subject matter** — what the illustrations DEPICT (scenes / objects / abstract patterns / characters / metaphors). Tied to the brand metaphor.
- **Forbidden** — what kills the style (realistic detail in a flat-vector brand, gradients in a flat-color brand, drop shadows, photo textures, generic stock-illustration style, AI-uncanny features)
- **One example illustration** filling 2/3 of the page (real generated illustration in the brand's style)
- **Reference brands' illustration** — 2-3 brands whose illustration style is close (e.g. "like Notion's homepage illustrations but a notch more grown-up")

### Visual World page (page 10) also adapts

The 4-image lifestyle grid on page 10 should match the brand's medium mix:
- All-photo brand → 4 photos
- All-illustration brand → 4 illustrations (varied scenes, not 4 of the same composition)
- Hybrid → mix of photos and illustrations in the proportions that match the brand world (e.g. 3 photos + 1 illustration if photography dominates)

---

## Avoid Concept Clichés — The First Metaphor Is Always Wrong

The strongest image concepts come from the SECOND or THIRD thing you think of, not the first. The first metaphor is what every stock photography library has been selling for 20 years. If a concept makes you go "yeah, that captures the idea" — pause. Did you actually invent it, or are you reaching for a familiar trope?

### Banned cliché concepts

Never use any of these. They read as stock and weaken every brand they appear in:

- **Hourglass / sand falling** for time, urgency, deadlines
- **Lightbulb glowing** for ideas, innovation
- **Chess pieces** for strategy, decisions
- **Jigsaw puzzle pieces** for fit, integration
- **Climbers reaching the summit / mountain peak silhouette** for ambition, success, leadership
- **Runner crossing a finish line** for achievement
- **Handshake** for trust, partnership, deals
- **Sunrise / sunset** for new beginnings (used to be fresh, now stock — though abstract sunrise illustrations can still work in consumer brands)
- **Compass or map alone** for direction, navigation
- **Rising graph line / arrow going up** for growth
- **Open road / horizon stretching into distance** for vision
- **Ocean waves / endless vastness** for scale
- **Tangled vs. straight cables** for organized vs. chaotic
- **Glowing network nodes connecting** for connection (especially in AI/tech)
- **Magnifying glass over numbers/charts** for analysis
- **Brain made of circuit board / glowing brain** for AI / intelligence
- **Domino chain falling** for cascading effect
- **Tree growing from a coin** for investment growth

If you find yourself reaching for any of these — STOP. Brainstorm three more concepts. The third one is usually right.

### Three tests for whether a concept is cheesy

1. **The Wikipedia test** — could this concept be the lead image on Wikipedia's article for the abstract noun your brand cares about? "Hourglass" is literally Wikipedia's image for "Time." That's why it's cliché.
2. **The Shutterstock test** — search Shutterstock for the keyword. If the top 20 results all look like your concept, you've picked the trope, not a fresh image.
3. **The 4-other-brands test** — could 4 brands in unrelated industries use this exact image and have it mean something to each of them? (Hourglass: works for time-tracking software, project management, dating apps, history museums, fitness apps — that's the giveaway.)

If a concept fails any of these three tests, regenerate.

### Substitutes that work

Trade the obvious metaphor for something **specific, indirect, or documentary**:

| Cheesy first instinct | Sharper substitute |
|---|---|
| Hourglass (time) | Analog watch dial macro with second-hand mid-tick / polaroid mid-development / a long-exposure trace of motion |
| Rising graph (growth) | Two real photos of the same space weeks apart / a plant in a real apartment / handwritten progress note |
| Lightbulb (ideas) | A worn notebook with marginalia in warm desk light / a paper cup of cold coffee at 2am |
| Handshake (trust) | Two people working side-by-side in a real space / a sticky note left for a teammate |
| Chess pieces (strategy) | Hand pausing mid-move on a real board / whiteboard with one diagram half-erased |
| Compass (direction) | Real map being read in a real environment / a fork in a real road |
| Network nodes (connection) | People in a room talking / a real meeting / a shared screen between two people |
| Glowing brain (AI) | Real engineers using real software / hands typing on a real interface |

**Pattern: trade the SYMBOL for the SCENE. Trade the OBJECT for the MOMENT. Trade the METAPHOR for the DOCUMENTARY.**

### The cringe test (run before delivering)

After generating, ask: *"If I saw this image without knowing the brand, would I cringe slightly?"* Stock-photo cringe is subtle — it doesn't scream "BAD IMAGE." It quietly says "this brand reached for the obvious symbol." If even slightly cringe — regenerate.

---

## Photography Must Show the Product IN USE — never a representational object

**For the full guidelines PDF (Step 3), the hero photography on the Cover, Photography Direction, Touchpoints, and Application pages must show the product being USED, not a representational object that stands in for the product.** This is the single most common reason a brand reads as "selling a thing it doesn't actually sell." A keychain charm shown on the cover of an app brand makes the brand look like it sells keychains. A coffee bag mockup for a streaming service makes it look like the brand sells coffee. A bottle photo for a software brand makes it look like the brand sells bottles.

**For digital products (apps, web services, SaaS):** hero photography must show the actual experience of using the product — selfies/photos taken with the app, screen captures of the result, people in the moment of using it (phone in hand showing the actual UI/result, video calls showing the feature in action, etc.). The brand's *symbol* can be a stylized heart-with-ears or any abstract mark — that's logo language. But brand *photography* must show the product itself, not the symbol.

**For physical products:** the product itself in real use — being worn, eaten, used, lived with. Not just unboxing or packshot.

**For services:** the moment of being served, the artifact produced, or the relationship in action.

**The keychain test:** ask yourself, "if a stranger saw this cover photo with no other context, would they correctly guess what we sell?" If the photo is of a physical-looking representational object that ISN'T the product, the answer is no — they'd guess the brand sells that object. Re-shoot.

## Photography Must Occupy Distinct Visual Territories

Each of the 3 mood images on the brand board must show a **genuinely different visual territory** — not three variations on the same subject. If all 3 images are "engineer at desk with laptop" with slightly different color grading, the photography has failed. The user reads three identical concepts and concludes the directions aren't really different.

Think of each option as a different MOVIE GENRE, each with its own:
- **Subject matter** — what's actually in the frame (portrait? still life? interior? hands at work? landscape?)
- **Setting** — where the brand lives (office? home? kitchen? after-hours desk? outdoors? abstract space?)
- **Scale** — close-up portrait vs. wide environment vs. tight still life vs. mid-shot
- **Time of day** — morning sun vs. midday vs. golden hour vs. midnight
- **Human presence** — is a person the subject, an element in the composition, or absent entirely?

### Examples of structurally distinct territories

For a brand with 3 directions (magazine-cover / consumer-warmth / editorial-quiet):
- **Magazine-cover** → close-up editorial PORTRAIT, single subject lit dramatically with one strong directional source, Bloomberg Businessweek cover energy
- **Consumer-warmth** → domestic STILL LIFE or hands in a real environment, no laptops or screens, golden hour, the LIFE around the work (kitchen, couch, sketchbook, market)
- **Editorial-quiet** → atmospheric STILL LIFE on a dark surface, single objects in moody pool of warm light, often no person visible, Frank Ocean Blonde sparseness

For a different set of directions, the territories would be entirely different — the rule isn't "always do portrait + kitchen + still life," it's "find three structurally distinct territories that match each direction."

### What NOT to do

- Three engineers at three desks with three different color casts
- Three close-ups of hands on three different keyboards
- Three "person at laptop in coffee shop" with different lighting
- Any variation where you swap one word in the prompt and re-run with a different palette

Each prompt should be **structurally different**: different subject, different setting, different scale, different mood. Color grading is the LAST differentiator, not the first.

---

## Brand Board Layout — Differentiate per Option (Step 2 of main skill)

**Critical rule for the 3-page brand board PDF built in Step 2:** do NOT use the same template for all 3 boards recolored. Each board's layout must physically embody its option's design philosophy. If you can swap colors and fonts and the layouts feel identical, the board has failed — viewers read the differences as cosmetic, not structural.

### Mandatory layout discipline — what makes a board NOT sloppy

The boards have repeatedly come back with overlapping type, mis-aligned elements, and broken hierarchy. The fixes below are non-negotiable.

1. **Plan the grid before writing CSS.** Sketch a 12-column × 12-row grid mentally for each board. Place each piece of content (wordmark, palette, type specimen, mood image, voice quote, brand story, references) into specific grid cells. Two pieces of content can NEVER occupy the same cell.

2. **Build a content inventory per board, with measured space allocations.** Example: "Wordmark = top-left 6 cols × 3 rows. Palette = top-right 6 cols × 2 rows. Mood image = middle 12 cols × 5 rows. Type specimen = bottom-left 6 cols × 2 rows. Voice quote + brand story = bottom-right 6 cols × 2 rows." If the sum of allocations exceeds 144 cells, cut content — don't squeeze.

3. **No text on top of text. Ever.** A headline overlapping a swatch label, a wordmark drifting into a voice quote, a tagline crashing into the brand story — all forbidden. Reserve a buffer (min 32px) around every text block.

4. **No text on top of busy parts of images.** Text overlaid on a mood image is allowed ONLY if the image area under the text is a flat color (e.g., a sky, a fade gradient zone). If text sits on a textured/detailed photo area, it becomes illegible. Either move the text into a flat zone, add a solid color band behind it, or lift the text out of the photo entirely.

5. **Render and READ each board PNG before delivering.** This is mandatory, not optional. Pipeline:
   ```bash
   for i in 01 02 03; do
     "$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
       --window-size=1200,850 \
       --screenshot="$WS/boards/qa-$i.png" "file://$WS/boards/$i-"*.html
   done
   ```
   Then open each PNG and check: (a) no overlapping text, (b) no text on busy image regions, (c) every required content block visible, (d) layout matches the brand's design philosophy, not a template. If any check fails — fix the HTML and re-render, don't ship.

6. **One element per board has visual priority.** Decide before building which element is the loudest: usually the wordmark, sometimes the mood image, occasionally a giant pull quote. Everything else sizes down from that. If two elements are competing visually, the board reads as cluttered.

7. **Whitespace is content.** A board with 30% empty space, intentionally placed, reads as confident. A board with content crammed into every corner reads as sloppy.

### The differentiation rule

Each brand board must answer: *what would this brand's actual hero page look like?* Build the answer.

### Unified aesthetic briefs STILL require structural divergence

When the user gives a unified aesthetic brief — one era ("Y2K"), one mood ("nostalgic"), one set of references ("Tamagotchi + PowerPuff + Bratz") — the easy failure mode is to deliver 3 variations of the same energy: all bright, all maximalist, all cartoon-y. **This is wrong.** A unified brief doesn't mean a unified output. The references the user lists are usually pointing at *sub-territories within the era*, not at a single shared visual. Pull them apart.

**Test before building:** when you read the brief, ask "are these references actually the same thing?" Tamagotchi is sparse 90s LCD mono. PowerPuff is loud 2001 cartoon outline. Bratz is glossy 2003 fashion editorial. These are three different visual languages from the same decade — each board should live in ONE of them, not blend all three into a single bright stew.

**The 3 boards must diverge across at least 4 of these dimensions** (not just color palette):

- **Density** — sparse breathing room / medium / dense maximalist
- **Color saturation** — muted/desaturated / mid / neon-bright
- **Color temperature** — warm cream-and-pink / cool blue-and-mint / monochrome / high-contrast neutrals
- **Layout philosophy** — centered symmetric / asymmetric editorial / grid-based / full-bleed image
- **Type energy** — quiet restrained / loud heavy display / technical mono / handwritten/script
- **Composition focal point** — wordmark-dominant / image-dominant / quote-dominant / palette-dominant
- **Photography subject scale** — macro detail / full scene / portrait / still life / abstract texture
- **Photography mood** — quiet documentary / saturated cartoon / glossy editorial / lo-fi grainy
- **Voice register** — deadpan / hype/loud / warm-poetic / technical
- **Era within the era** — pick a specific year and pin the board to it (1998 LCD vs 2001 cartoon vs 2003 magazine)

**Adjective audit before delivering:** write the top-3 primary adjectives for each of the 3 boards. If 2 boards share 2+ primary adjectives (e.g. board 1: bright/maximalist/cartoon, board 2: bright/maximalist/sticker-y), they're too similar — push at least one of them further. The point of 3 options is to give the user genuinely different takes on what their brand could be, not three saturations of the same take.

### Divergence ≠ subtraction. Every board delivers on the brief.

**The brief is non-negotiable.** Whatever character the user named — Y2K, kawaii, brutalist, art-deco, cottage-core, cyberpunk — every single one of the 3 boards must deliver on it at full intensity. Variety comes from sub-territories within the brief, not from departing from the brief. Never strip a board back to differentiate it from another; never make a board boring or generic to make it "different."

When pushing the 3 boards into different sub-territories, the failure mode is interpreting "different from loud" as "quiet / muted / stripped back." Don't. Each board should MAXIMALLY express its own sub-territory's character — AND each board must deliver the brief's core aesthetic. If one territory is "minimal editorial within Y2K," it's still minimal-editorial-WITH-Y2K-character (chrome, holographic foil, glitter accents); it is NOT minimal-editorial-stripped-of-Y2K. If another is "lo-fi digital nostalgia within Y2K," it's still saturated-Tamagotchi-candy-and-LCD-greens; it is NOT dusty-cottage-cream.

**The 3 boards should feel like 3 fun things, each delivering the brief**, not "one loud + two stripped." Differentiation is on STRUCTURE (density, layout, type energy, voice register, composition), and on SUB-TERRITORY (different reference points within the same era/mood) — not on amount-of-character. Three boards, each at 100% of its own thing AND 100% of the brief.

**The trap to avoid:** "Board 2 is loud and saturated, so I'll make Board 1 muted and Board 3 minimal to differentiate." This sacrifices the brief for the sake of variety. The right pattern: "Board 2 is loud-PowerPuff-saturated, Board 1 is loud-Tamagotchi-candy-LCD, Board 3 is loud-Bratz-glossy-glittered-editorial." All three are still loud Y2K — they differ in *which Y2K* they live in.

### Era palettes are specific — don't substitute "muted" for "era-appropriate"

When the user names an era (Y2K, 90s, 80s, 60s, mid-century, art deco, etc.), the palette signatures of that era are non-negotiable. "Muted" is rarely the right answer; era-specific saturation profiles are. Research the era's actual palette before picking colors.

**Y2K palette signatures** (early 2000s, 1998–2004):
- iMac G3 gel colors: Bondi blue, tangerine, grape, lime, strawberry, blueberry — translucent saturated
- Tamagotchi: candy pink, mint, lavender, butter yellow, pastel egg colors
- Bratz / mall culture: hot magenta #FF2BB8, chrome silver, lime #C8FF32, butter yellow, baby blue
- Holographic / iridescent: shifting rainbow on chrome base
- Cyber: lime green on black, hot pink + cyan, chrome metallic
- Frosted: white-on-cream with chrome accents
- NOT Y2K: dusty mauve, muted putty, cottage cream, faded sage — those are 2010s rustic/cottage-core, NOT Y2K

**90s grunge / 90s alt**: washed-out, desaturated, photocopied texture, off-register print
**80s Memphis**: primary colors + black + cyan, geometric shapes, pastel accents
**70s**: harvest gold, avocado, burnt orange, brown, mustard, warm earth tones
**60s mod**: bold flat color blocks, op-art black/white, saturated psych
**50s**: pastel mint, pink, baby blue, chrome + cream

If you've shifted a palette to "muted" or "dusty" to differentiate it from a brighter board, you've likely left the era. The era is non-negotiable; the energy varies through density, composition, and texture instead.

### Texture is era signal — but it must be AMBIENT, not a pattern

A flat-vector board with no texture reads as generic 2020s vector, not as a specific era. But the opposite failure is just as bad: a board with a recognizable repeating motif (literal halftone dots, scattered glitter flakes, visible scanline rows) reads as a graphic element stamped onto the layout, not as authentic era-character. Both fail. The right answer is **ambient atmospheric texture**: subtle grain, soft noise, grainy gradient, faded VHS shimmer — texture that the user *feels* without recognizing it as a graphic motif.

**Reference frame: VHS noise / film grain / paper grain / grainy gradient.** Not patterns. The user should look at the board, feel the era, and not be able to point at "the texture." If they can name what the texture is (halftone! glitter! scanlines!) it's too literal.

**Always generate textures via `generate_image` with `provider="gpt-image-2"`, never via CSS gradients.** CSS halftone dot patterns, conic-gradient chrome, and repeating-linear-gradient scanlines are too clean — they read as a stylesheet, not as material. Generated textures have the small imperfections (real grain, soft gradient drift, atmospheric noise) that make a board read as authentic-retro. The only acceptable CSS-rendered "texture" is something that's also a UI element (e.g. a thin holographic strip used as a divider).

**Pipeline for generating a texture:**
1. `generate_image` with `provider="gpt-image-2"`, `quality="medium"`, aspect ratio 4:3 or 16:9 to cover full-canvas (not 1:1 — tileable patterns will repeat visibly).
2. Prompt for **ambient grain / atmospheric noise**, NOT a pattern. Required prompt language: "subtle ambient grain," "atmospheric noise field," "grainy gradient," "soft film grain," "barely visible," "smooth not patterned," "NO recognizable motifs," "NO repeating elements," "NO visible patterns." Add the era's specific texture vocabulary as ATMOSPHERE not as object (e.g. "subtle VHS noise atmosphere" not "scanline pattern"; "ambient holographic shimmer" not "glitter flakes"; "soft newsprint paper grain" not "halftone dots").
3. Download and place in `images/textures/`.
4. Apply via CSS `background-image` on the **body** (full-board coverage), with `mix-blend-mode: overlay` or `multiply` or `screen`, at **low opacity (0.12–0.30 max)**. The texture should be felt across the whole board ambient-style, not stuck onto one card as a focal element.

**Era-texture prompts as ATMOSPHERE, not pattern:**
- **Y2K LCD/handheld** → "subtle VHS noise atmosphere with very faint horizontal screen-line drift, low-contrast warm vintage screen feel, NOT a scanline pattern"
- **Y2K cartoon/comic** → "soft newsprint paper grain, ambient print noise, barely-visible warm-cream paper roughness, NOT halftone dots"
- **Y2K glam/Bratz** → "subtle iridescent grainy gradient, ambient holographic shimmer atmosphere, soft pink/lime color drift, NOT glitter flakes or stars"
- **Mid-century print** → "fine paper grain atmosphere, soft warm tonal noise"
- **80s digital** → "subtle CRT phosphor glow atmosphere, faint color drift, NOT pixel grid"
- **90s grunge** → "ambient Xerox roughness, soft photocopy grain drift, NOT visible dust spots"
- **70s organic** → "warm paper grain, soft fiber atmosphere"
- **Film/photography** → "fine silver-halide grain, atmospheric noise, NOT visible particles"

**Application rule of thumb:** if a viewer can describe the texture as a noun ("halftone dots", "glitter flakes", "scanlines"), it's too literal. If they describe it as an atmosphere ("kind of grainy", "feels VHS-y", "soft retro feel"), it's right. The goal is era-character through ambience, not graphic elements through stamping.

Don't ship a "retro" board with zero texture. And don't ship a "retro" board with literal pattern overlays — generate ambient grain, apply widely, keep subtle.

### Examples of differentiated layouts

**Magazine-cover brand** — Full-bleed photo as background covering the entire page. Massive wordmark overlaid in display type. Tagline overlaid in small text. Issue/edition tag in corner ("Vol. 01 / Cover Story"). Bottom-margin strip showing color swatches and typography credit, like a magazine masthead. Whole page should look like a Bloomberg Businessweek or NYT Magazine cover.

**Soft consumer-brand homepage hero** — Asymmetric split with a curved or rounded shape break between colored side and cream side. Big rounded type on one half, photo with rounded corners on the other. Color swatches presented as soft circles, not squares. Lots of breathing room. Should feel like the hero of bumble.com or pika.me.

**Editorial / literary essay** — Bone or cream full-bleed background. Massive italic display type centered with extreme whitespace. Photo as a small inset rectangle, not full-bleed. Pull-quote on the margin. Color swatches as a tiny ribbon at the bottom. Should feel like the opening page of a Frank Ocean visual essay or an Anthropic announcement.

**Tech-doc / dev-tool aesthetic** — Monochrome grid. Tight type. Code-like layout with bracket marks or syntax highlighting. Mono font everywhere. Color swatches as inline `code` blocks with hex strings. Should feel like Linear's changelog or Stripe's docs.

### Required content per board (regardless of layout)

Every brand board page must include ALL of the following. The layout differentiation rule above does NOT mean cutting content — visually distinct layouts must still fit ALL the text. If a layout doesn't have room for the content, redesign the layout, don't drop content.

- Brand wordmark (set in the brand's display font)
- **A standalone logo symbol/mark — rendered inline as SVG (preferred) or generated PNG. NOT just typography.** The symbol must work as a favicon, app icon, social avatar.
- Tagline
- Voice sample (one sentence in brand voice, quoted, with a "VOICE" label)
- Brand story (2-3 sentences in brand voice)
- **Lifestyle world description (1-2 sentences describing the brand's visual territory — where it visually lives, who's in the frame, time of day, color temperature)** — labeled "WORLD" or similar
- Lifestyle mood image (generated via gpt-image-2 — see "Photography Must Occupy Distinct Visual Territories" rule below)
- 4-color palette with hex codes + role labels
- Display + body type specimens with named fonts

### What NOT to do

- Same left-column-color-block-right-column-photo template recolored 3 times
- Same swatch grid in the same position on every page
- Same type specimen "Aa" treatment on every page
- Three different colors and three different fonts laid onto identical layouts
- Wordmark with no separate symbol — the logo isn't complete without a mark
- **Asymmetric rounded corners on color blocks** (e.g. only `border-top-left-radius` on a big shape) — these read as a clipping bug, not a design choice. If you want softness, use **symmetric** rounded corners (whole left edge rounded, or all four corners rounded), a **clean rectangular split**, or a deliberately organic shape via SVG/clip-path. Half-rounding a single corner of a big block looks like a mistake every time.
- **Inline pill backgrounds on display text (40px+)** — they overlap into adjacent lines because line-height is usually tighter than the rendered character box. A `background: var(--color); padding: 0 12px; border-radius: 12px;` on big headline text WILL bleed into the line above or below. Two safer options:
  1. **Highlighter-underline gradient** (recommended): `background: linear-gradient(to bottom, transparent 0%, transparent 58%, var(--accent) 58%, var(--accent) 92%, transparent 92%); padding: 0 6px; -webkit-box-decoration-break: clone; box-decoration-break: clone;` — creates a marker-highlight band that only occupies the bottom of the line, never extends beyond.
  2. **Just change the text color** (color: var(--accent)) — simplest, no overlap risk.
  Never use solid pill backgrounds on display text unless you've also set generous line-height (1.4+) AND tested the actual render.
- **Pill/badge containers with text inside** (numerals like 01, 02, markers like + or ×, single letters) — never style them with `padding + text-align: center` and expect the text to look vertically centered. Font glyphs sit on a baseline with empty space above and below, so padding alone leaves the character looking top-shifted with empty space underneath. **Always use `display: inline-flex; align-items: center; justify-content: center;` with EXPLICIT `width` and `height`** — let the flex container center the text. Skip padding. Skip `text-align: center` (it only handles horizontal). The text will sit visually centered regardless of font metrics.

If you can't physically tell which brand you're looking at *without* reading the labels, regenerate.

---

## Quality Bar

- Feels like a $5,000 brand studio deliverable — not a template, not a Canva export
- Every page should feel like a deliberate design decision was made
- **Typography used boldly**: headlines at 80–160px as graphic elements, not just labels
- **Color used intentionally**: full-bleed color blocks, not just colored text
- **Negative space is a design tool** — don't crowd every page
- **Hierarchy must be obvious**: display → subhead → body at dramatically different sizes
- **Voice page shows actual brand copy**, not generic example text
- **Touchpoints page shows real generated photos** — never CSS vector boxes
- **No placeholder text, no [BRACKETS], no repeated images anywhere**
