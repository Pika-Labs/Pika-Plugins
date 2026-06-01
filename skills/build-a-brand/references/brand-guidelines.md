# Brand Guidelines — Build Guide

In full brand book mode, the brand guidelines PDF is the primary visual deliverable of this skill. It is 14-16 pages depending on brand type, rendered locally with Chrome headless or WeasyPrint, and delivered as a local PDF path. Quick brand mode has its own 3-page deliverable in `SKILL.md`; do not treat that quick PDF as a condensed or partial version of these full guidelines.

This guide is the technical playbook: page layouts, image generation, font rules, local render contract, QA checklist. All non-negotiable.

## Execution Model — Local First

Keep deterministic production local:
- **Local:** workspace setup, downloaded fonts, compressed image files, transparent-background cleanup, favicon tests, HTML/CSS builds, PDF rendering, preview screenshots, visual QA, logo asset assembly, and kit packaging.
- **Cloud:** `gpt-image-2` image generation for symbols, photography, illustration, and textures; URL/source research when the brief requires it.

Do not upload PDFs by default. Save PDFs and zips to `~/Desktop` on Mac, or the project working directory if Desktop is unavailable. Only create a hosted/CDN copy when the user explicitly asks.

## Page Structure (14-16 pages depending on brand)

**Page count is conditional:**
- **14 pages** — non-digital brand (product, restaurant, fashion, service) with single-medium imagery. Icons page skipped.
- **15 pages** — digital brand (app/web/SaaS) with single-medium imagery. Icons page included.
- **15 pages** — non-digital brand with hybrid imagery. Imagery splits to 2 pages; Icons skipped.
- **16 pages** — digital brand with hybrid imagery. Both Icons + split-Imagery present.

Renumber pages contiguously based on what's included. Do not leave gaps.

1. **Cover** — Full-bleed brand-specific layout. Brand name + tagline + hero mood image.
2. **Strategy & Positioning** — Direction, positioning statement, audience segments (primary segment, secondary segment(s), and anchor persona), 3-4 reference brands with "borrow this" notes.
3. **Brand Foundation** — Mission, values (3-5), why this exists (story in brand voice).
4. **Logo** — Primary mark + variants (horizontal, icon-only, reversed), usage rules, clear space.
5. **Logo Don'ts** — Misuse rendered in CSS with ✗ labels.
6. **Color** — Swatches with hex+RGB+CMYK, full-bleed color columns (not floating swatches).
7. **Typography** — Full hierarchy with px sizes, display/body specimens, usage rules.
8. **Icons** *(digital brands only)* — 8-12 essential UI icons in brand's geometric style + stroke/corner/grid rules + library recommendation. Skip this page entirely for non-digital brands and renumber subsequent pages.
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

```bash
WS="${BUILD_A_BRAND_WS:-$HOME/build-a-brand-workspace}"
mkdir -p "$WS/fonts" "$WS/images"
```

Use `$WS/images/lifestyle1.jpg` etc., and `file://$WS/images/lifestyle1.jpg` in HTML after resolving `$WS` to an absolute path. Build the final guidelines as a local HTML file or one generated HTML string; local paths are expected because rendering is local.

---

## Step 1 — Generate Imagery (in parallel batches of 4)

You need **a minimum of 10 generated images**:
- 1 hero mood image (for the cover)
- 1 example image (for the photography rules page)
- 4 lifestyle images (for the visual world grid)
- 4 touchpoints images (for the real photos page) — adapt to brand type

That's 10 images. Run in parallel batches of 4 with `&` + `wait`. Never more than 4 at once (timeouts).

Before generating or placing those images, write a short **crop plan** and **pre-generation slot plan** for the deck. This is required working context, not final user-facing copy:

- **Crop plan**: for every generated image, name the destination page, slot aspect ratio, final pixel box, intended subject anchor (face/product/hands/object), expected `object-position`, and rounded frame risk. If rounded frame risk is high, use a softer radius, move the subject anchor lower/center, or regenerate for the actual slot ratio.
- **Pre-generation slot plan**: list every slot expected to show imagery, including destination page, slot aspect ratio, planned medium, and prompt intent. Do not invent asset URLs before generation.
- **Post-generation filled manifest / image slot manifest**: after image generation or upload, copy the final asset URLs/IDs into the same slot list and verify every planned slot is filled. The manifest must include the cover hero, imagery-rules example, visual-world grid, touchpoints grid, and the Digital / Social website hero, Instagram grid, and story template. Each required slot needs a real generated image or hosted image asset. Flat color rectangles count as empty unless the section is explicitly a palette specimen.
- The Visual World page must use real generated images that match the brand's
  medium. CSS color blocks, gradients, caption-only placeholders, and empty
  rectangles are not image assets.
- The Touchpoints page must use real generated photographs in believable
  physical or digital context. CSS color blocks, flat vector mockups, and
  captioned boxes are not substitutes for touchpoint photography.

Download generated image outputs into `$WS/images`, then compress before using in PDFs:

```python
from PIL import Image
img = Image.open(path)
img.thumbnail((1200, 1200), Image.LANCZOS)
img.save(path, 'JPEG', quality=68, optimize=True)
```

Target under 150KB per page image where practical. Keep page images reasonably sized, avoid duplicating the same source across pages, and use CSS `object-fit` / `object-position` explicitly.

This is load-bearing for reliability: full-size gpt-image-2 PNGs are often 1.5-2.5MB each. Embedding them directly can inflate a guidelines PDF into tens of MB and trigger `ASSET_FETCH_TIMEOUT` while local/remote renderers fetch page images. For photographic page imagery, down-raster/downsample to the slot size and write JPEG files targeting about 85-180KB. Keep PNG only where transparency is required for logo/symbol assets.

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

Hand-coded SVG symbols often look amateur. But also: don't trace a generated symbol to SVG. Keep the symbol as a high-resolution transparent PNG. Only the wordmark gets vectorized in the brand kit.

1. Generate the symbol via `generate_image` with `provider="gpt-image-2"`, `quality="high"` when final, 1:1 aspect ratio, 1024x1024 minimum. The symbol can be flat, dimensional, painted, photographic, gradient-rich, chrome, holographic, or hand-drawn when that style fits the brand.
2. Add the no-text guardrail: "absolutely no text, no letters, no typography, no words, no characters anywhere in the image."
3. The generated symbol must be conceptually linked to the brand, unique, recognizable at 16x16, no more than 3 dominant colors, high res for the shipped version, text-free, and true transparent background. If it fails any of these, regenerate.
4. Save as transparent PNG, verified with PIL. If gpt-image-2 paints near-white pixels in the "transparent" area, key them out or regenerate.
5. The wordmark is always real text in a Google Font or commercial font, never baked into a generated image. Convert the wordmark to text-as-paths SVG only when packaging the brand kit.
6. Lockup composition is measured and fixed: symbol size, wordmark size, gap, and alignment do not drift across color variants.

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

Before selecting final type, make a **font shortlist** for the identity:
- Include at least 2 display families and at least 2 body/accent candidates that fit the specific brand vibe.
- Do not reuse the same display/body pair from the last 3 brand briefs unless the user explicitly asks for that exact pairing.
- Pick the pair for this brief from the shortlist and state why it fits the brand's category, audience segments, and visual world.

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

**Pairing rules:**
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

### Download fonts to the local workspace

Store font files under the same local workspace as the HTML and images, then reference them with absolute `file://` URLs. Prefer direct WOFF2 font-file downloads from `fonts.gstatic.com` or other direct font-file sources.

```bash
WS="${BUILD_A_BRAND_WS:-$HOME/build-a-brand-workspace}"
mkdir -p "$WS/fonts"
curl -sL "https://fonts.gstatic.com/s/playfairdisplay/v40/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgA.woff2" -o "$WS/fonts/PlayfairDisplay.woff2"
curl -sL "https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2" -o "$WS/fonts/Inter.woff2"
```

Use `@font-face` with local file sources:

```css
@font-face {
  font-family: 'BrandDisplay';
  src: url('file:///Users/name/build-a-brand-workspace/fonts/PlayfairDisplay.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: 'BrandBody';
  src: url('file:///Users/name/build-a-brand-workspace/fonts/Inter.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

**Font loading rules:**

- Use absolute `file://` URLs in rendered HTML so local Chrome and WeasyPrint resolve the same files.
- Keep one local `fonts/` folder per project and copy every chosen font into it before rendering.
- Do not use `@import` for render-critical type; explicit `@font-face` rules are easier to QA and reproduce.
- Do not put a Google Fonts CSS URL such as `https://fonts.googleapis.com/css2?...` inside `@font-face src`; that URL returns CSS, not a font file.

Render one page locally before the full PDF; if the type falls back to Times/Arial, fix the font source before continuing.

### Font fallback for non-Latin brand names

When rendering CSS for a brand board, quick PDF, or full guidelines deck, every `font-family` chain must include CJK and broad-script fallbacks. Chromium applies per-glyph fallback: Latin characters use the first available brand font, while CJK, Arabic, Cyrillic, and other missing glyphs resolve to the matching Noto family instead of tofu boxes.

```css
/* Body / sans-serif chains */
font-family: 'BrandBody', 'Inter', 'Noto Sans SC', 'Noto Sans TC', 'Noto Sans JP', 'Noto Sans KR', 'Noto Sans Arabic', system-ui, sans-serif;

/* Display / serif chains */
font-family: 'BrandDisplay', 'Bodoni Moda', 'Fraunces', 'Noto Serif SC', 'Noto Serif TC', 'Noto Serif JP', 'Noto Serif KR', 'Noto Sans Arabic', serif;
```

Load the Noto fallback faces with the same local strategy as brand fonts: download the relevant Noto files into `$WS/fonts`, then reference them through absolute `file://` URLs in `@font-face`. This fallback belongs in shared CSS for every page, not only the page containing the brand name.

---

## Step 3 — Build HTML

Write fresh HTML for the chosen identity. Never copy old deck HTML — always write fresh.

**Critical CSS (required in every guidelines doc):**
```css
@page { size: 1200px 850px; margin: 0; }
.page { width: 1200px; height: 850px; overflow: hidden; page-break-after: always; display: block; }
```

### Local Render Rules — Read Before Writing a Single Div

Local Chrome headless and WeasyPrint support flexbox, grid, absolute positioning, and CSS transforms well enough for these fixed-format pages. Keep page geometry explicit so QA is deterministic:

#### Rule 1: Every page is a fixed canvas
- Use `@page { size: 1200px 850px; margin: 0; }`.
- Every `.page` must be `width:1200px;height:850px;overflow:hidden;page-break-after:always;position:relative;`.
- Use explicit pixel dimensions for key regions. Flex/grid are fine, but don't let page height be content-driven.
- Avoid viewport units (`vh`, `vw`) inside pages; they couple layout to the browser window rather than the page box.

#### Rule 2: Use local assets deliberately
- Use absolute `file://` URLs for local fonts, generated images, user-provided source images, and assembled logo assets.
- Download generated image outputs into `$WS/images` before placing them in HTML.
- Small SVGs and font subsets can be inlined as `data:` URIs when it improves portability.
- Avoid hotlinking external HTTPS assets in final render HTML; download, compress, and reference the local copy.

#### Rule 3: Use layout systems intentionally
- CSS grid is preferred for swatches, icon sets, mockup grids, type specimens, and contact sheets.
- Flexbox is fine for compact rows and centered stacks.
- Use absolute positioning for full-bleed editorial pages where overlap and crop are intentional.
- Give repeated tiles fixed dimensions so badges, labels, and icons cannot resize the layout.

#### Rule 4: Text containers must wrap naturally
- Text cards, sidebars, and copy columns must have an explicit readable width. Reserve at least `320px` for body copy via `min-width:320px`, grid `minmax(320px, ...)`, or an equivalent fixed px floor. You may use `ch` only as a `max-width` line-length cap, never as the width floor. Never let a right-column card collapse until each line becomes one word.
- In flex/grid layouts, set `min-width:0` on text children so copy wraps inside its assigned track, and separately give the track/card a real width floor (`width`, `flex-basis`, or grid track minmax).
- Body-copy containers should include `box-sizing:border-box; overflow-wrap:break-word; word-break:normal; hyphens:none;`.
- Never use `word-break:break-all`, `overflow-wrap:anywhere`, or a narrow absolute-positioned card squeezed by an illustration/phone mockup for readable prose.
- If an illustration, phone, seal, swatch, or decorative element sits near a copy card, the card owns a clean rectangle above it in z-order and geometry. Do not depend on the visual QA pass to catch preventable overlap.

#### Rule 5: Image rules
- Always explicit px dimensions: `style="width:300px;height:400px;object-fit:cover;display:block;"`
- Avoid percentage heights unless the parent has an explicit pixel height
- Never `opacity:` on any `<img>` — images always at full opacity
- Never body text/labels/rules on images — put captions in an adjacent column or block. Masthead brand boards may overlay wordmark/tagline/issue metadata on a full-bleed photo only when the type sits on intentional negative space or a contrast scrim and passes contrast QA.
- Contrast QA for masthead overlays means the masthead text remains readable in the full-page PNG preview. If uncertain, render a local crop or full-page screenshot and judge the masthead wordmark/tagline/issue metadata at actual preview size before continuing.
- Never duplicate an image src across the deck — each file appears at most once
- Use `object-position` deliberately and verify the crop in PNG previews

#### Rule 6: Text contrast thresholds on dark backgrounds
On graphite (#2E2E2E) or any dark background:
- Body text minimum: `rgba(248,243,236,.7)`
- Sub-descriptions minimum: `rgba(248,243,236,.55)`
- Decorative / ghost text minimum: `rgba(248,243,236,.45)` — below this, remove the element entirely
- `.3` opacity on dark = invisible. Never use for any visible text.

#### Rule 7: Page overflow prevention
- Every page is 850px tall. All content MUST fit.
- If a page has a headline >60px AND more than 3 body paragraphs, it will overflow. Cut or split.
- Never more than ~220 words of body text on a single page.
- Padding: 64px top/bottom max on content pages. Don't stack multiple padded sections.

#### Rule 8: Good-looking layout prevention
- Passing render QA is not enough. A page can have no clipped text and still be bad if it looks crowded, muddy, or amateur.
- Body copy, labels, and load-bearing informational text must never collide with swatches, icons, photos, decorative rules, grain, seals, or background imagery. If an element sits on top of body copy, the page fails even when the text technically remains inside its box. Masthead boards may overlay wordmark/tagline/issue metadata on a full-bleed photo only when the type sits on intentional negative space or a contrast scrim and passes contrast QA; body copy still gets its own clean reading area.
- Body copy on brand boards and guidelines must be readable at the full-page screenshot size. Use 18px minimum for body copy, 14px minimum for labels, and 10px minimum only for decorative metadata that is not load-bearing.
- Decorative microtype is optional. If small labels, faux archival notations, issue numbers, or specimen marks make the page noisy, remove them before reducing the real content.
- Keep one primary visual focal point per page while required board content stays secondary and grouped. If the viewer's eye has to choose between a huge wordmark, a dense paragraph block, six swatches, a seal, a photo, and a pull quote at once, simplify hierarchy and grouping; do not drop required content.
- Do not use a one-note dark brown/green/slate page unless the brief specifically demands it. Add contrast through scale, image light, accent color, or negative space; do not let the whole page collapse into one muddy value range.
- Empty placeholders are a hard fail. Website/social/app mockups are optional on brand boards; do not add them unless they contain real content. If a website hero, grid, story template, image slot, or app mockup is included, either render the real content or remove/redesign the slot. Flat color rectangles in a Digital/Social mockup count as empty placeholders unless the section is explicitly a palette specimen.

#### Rule 9: Vertical centering critical gotcha
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
        <img src="https://..." style="width:480px;height:782px;object-fit:cover;display:block;">
      </td>
      <td style="width:720px;height:782px;vertical-align:middle;padding:52px;background:#2E2E2E;box-sizing:border-box;min-width:0;overflow-wrap:break-word;word-break:normal;hyphens:none;">
        <!-- right column text content -->
        <div style="max-width:560px;min-width:320px;box-sizing:border-box;overflow-wrap:break-word;word-break:normal;hyphens:none;">
          <!-- body copy goes here -->
        </div>
      </td>
    </tr>
  </table>
</div>
```

**Full-bleed lifestyle grid (page 11):**
```html
<table style="width:1200px;height:782px;border-collapse:collapse;table-layout:fixed;">
  <tr>
    <td style="width:300px;height:782px;padding:0;overflow:hidden;"><img src="https://..." style="width:300px;height:782px;object-fit:cover;display:block;"></td>
    <td style="width:300px;height:782px;padding:0;overflow:hidden;"><img src="https://..." style="width:300px;height:782px;object-fit:cover;display:block;"></td>
    <td style="width:300px;height:782px;padding:0;overflow:hidden;"><img src="https://..." style="width:300px;height:782px;object-fit:cover;display:block;"></td>
    <td style="width:300px;height:782px;padding:0;overflow:hidden;"><img src="https://..." style="width:300px;height:782px;object-fit:cover;display:block;"></td>
  </tr>
</table>
```

This grid is image-only. If captions or labels are needed, put them in adjacent Rule-4 text containers; do not overlay body copy on the photos.

**Touchpoints 2×2 grid (page 12):**
```html
<table style="width:1200px;height:782px;border-collapse:collapse;table-layout:fixed;">
  <tr>
    <td style="width:599px;height:390px;padding:0;overflow:hidden;"><img src="https://..." style="width:599px;height:390px;object-fit:cover;display:block;"></td>
    <td style="width:1px;background:#fff;"></td>
    <td style="width:600px;height:390px;padding:0;overflow:hidden;"><img src="https://..." style="width:600px;height:390px;object-fit:cover;display:block;"></td>
  </tr>
  <tr><td colspan="3" style="height:2px;background:#fff;padding:0;"></td></tr>
  <tr>
    <td style="width:599px;height:390px;padding:0;overflow:hidden;"><img src="https://..." style="width:599px;height:390px;object-fit:cover;display:block;"></td>
    <td style="width:1px;background:#fff;"></td>
    <td style="width:600px;height:390px;padding:0;overflow:hidden;"><img src="https://..." style="width:600px;height:390px;object-fit:cover;display:block;"></td>
  </tr>
</table>
```

This touchpoints grid is image-only. If a label is required, use a separate caption strip or adjacent Rule-4 text container; do not place readable prose inside the image cells.

### Page-Specific Notes

**Page 4 — Logo applications:** Left half (~420px) = large logo mark centered with generous whitespace. Right half (~780px) = 5 CSS mockups in a 2-row grid (3 top, 2 bottom), `gap:32px`, each cell min 160×180px. Don't flex-wrap — use proper grid.

**Page 5 — Logo Don'ts:** 5 violation tiles in a row, each with the wrong-usage logo + a small ✗ label + a one-line caption explaining the violation.

**Page 10 — Photography Rules:** Left 2/3 (~780px) = 3 example images in a grid with explicit pixel dimensions. Right 1/3 (~420px) = sidebar of 4-5 specific rules (surface, light, propping, editing, mood). Small label caps + body text.

**Page 12 — Touchpoints:** The page **must show real generated photos** of the brand in context. Never substitute CSS vector mockups. Generate the 4 images before building HTML. For physical product brands: hang tag, woven label macro, kraft mailer, flat lay. For digital brands: phone in hand showing app, laptop on desk showing site, sticker on water bottle, tote bag in a real scene. For service brands: business card in hand, signage, branded notebook, swag.

**Page 13 — Brand Applications (CSS mockups):** Each mockup is a small physical-object representation rendered in CSS. Use fixed dimensions and verify the visual center in PNG previews.

| Shape | Dimensions | Suggested centering |
|---|---|---|
| Hang tag | 120×168px | CSS grid/flex center, then visual QA |
| Woven label | 200×80px | CSS grid/flex center, then visual QA |
| Avatar circle | 100×100px | CSS grid/flex center, then visual QA |
| Sticker rounded square | 100×100px | CSS grid/flex center, then visual QA |
| Business card | 200×120px | CSS grid/flex center, then visual QA |

### Image hard constraints

- **No opacity on images.** Never `opacity:` on any `<img>` — full brightness always.
- **No body text on images.** Body copy, captions, labels, and rules never overlay images. Captions go in an adjacent column. Masthead brand boards may overlay the wordmark/tagline/issue metadata on a full-bleed photo only when the type sits on intentional negative space or a contrast scrim and passes contrast QA.
- **No gradient overlays on ordinary content images.** Do not use decorative gradient overlays on photos. Masthead covers may use one controlled linear scrim/gradient mask behind wordmark/tagline/issue metadata text to preserve contrast: strongest stop <= 50% opacity, one edge direction only, max scrim height <= 40% of image height, and no product/detail/focal subject hidden under the scrim.
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

**Fallback: WeasyPrint.** Use this only when Chrome is unavailable or the HTML was written to the table-safe constraints:

```python
import weasyprint, warnings, os
warnings.filterwarnings('ignore')
WS = os.environ.get('BUILD_A_BRAND_WS') or os.path.expanduser('~/build-a-brand-workspace')
pdf = weasyprint.HTML(filename=f'{WS}/guidelines.html', base_url=f'file://{WS}/').write_pdf()
open(f'{WS}/guidelines.pdf', 'wb').write(pdf)
```

Pick one engine and stick with it for the whole 14-16-page build.

---

## Step 5 — Verify Every Page (Mandatory)

Before delivery, render one full-page preview per page and verify against the QA checklist. JPG previews are fine for layout/contrast QA; PNG is required only for logo/symbol asset export.

For PDF-to-preview QA, use PyMuPDF:

```python
import fitz, os
WS = os.environ.get('BUILD_A_BRAND_WS') or os.path.expanduser('~/build-a-brand-workspace')
doc = fitz.open(f'{WS}/guidelines.pdf')
for i in range(len(doc)):
    doc[i].get_pixmap(matrix=fitz.Matrix(1.8, 1.8)).save(f'{WS}/qa_p{i+1}.png')
print(f'{len(doc)} pages — now read each one')
```

### Pre-Send QA Checklist

Read every screenshot. Verify every item. If any check fails, fix it. No exceptions. Never ask the user to spot problems the agent should have caught.

**Cost rule — QA must scale with page count, not element count.** Read ONE full-page preview per page (14-16 reads). Do NOT crop-and-read every small element on every page by default. The full-page read is the default; targeted zoom is the exception, not the rule.

**Full-deck visual QA:** every final guidelines page must receive a local full-page preview read before delivery. Record PASS or FAIL per page, fix every captured fail, and do not deliver the PDF until all included pages are clean or the user explicitly accepts a documented `degraded` quality warning.

**Per-page QA (mandatory — one full-page read per page):**
1. **Full-page pass** — read the full-page PNG for each page and verify it against the checklist below (blank columns, missing content, wrong colors, font fallback, text/image collisions, clipped text, weak hierarchy).
2. **Target detail-level QA only where needed** — use local crops for flagged defects or the few highest-risk elements. Fix every captured FAIL.

**Targeted zoom — only when triggered.** Crop and read an 800×800px region ONLY for:
- a specific element the full-page read flagged as suspect, OR
- the few genuinely highest-risk spots, when the page contains them: a single-character pill/badge marker, a favicon-size (≤32px) logo rendering, or a business-card layout.

Do not zoom every element on every page. Zoom the flagged ones. A clean full-page read with no blocking defects is sufficient to clear a page.

| Check | What to look for |
|---|---|
| Fonts loaded | Headlines render in the chosen font, not a system fallback (Times, Arial) |
| No blank columns | Every column has content — no white/solid blocks where text should be |
| No empty placeholders | Optional website heroes, grids, story templates, app mockups, image slots, and cards contain real content or are redesigned away. Flat color blocks in Digital/Social mockups count as empty unless they are explicitly palette specimens |
| No text/image collisions | Body copy, captions, labels, and rules do not sit on top of images. Masthead wordmark/tagline/issue metadata overlays are allowed only with deliberate negative space or a contrast scrim and must pass contrast QA |
| No text collisions | Text does not overlap or sit underneath icons, swatches, seals, decorative lines, photos, phone mockups, or other graphic elements |
| No clipped or occluded text | Text is not cut off by its own container, page edge, rounded shape, sibling graphic, or z-index layer |
| Board looks good, not just valid | Full-page read has one focal point, clear hierarchy, enough negative space, and no muddy one-note palette |
| Load-bearing copy is readable | Body copy is readable in the full-page PNG; do not hide key content in 10px decorative microtype |
| **No baked-in text in generated images** | **Open each generated image and look for ANY text — magazine titles, watermarks, brand names, captions, headers. If you see any, regenerate with stronger no-text guardrails.** |
| **Subjects survive their crop** | **For every generated image used in a layout: is the intended subject visible after the CSS crop? No forehead-only portraits, no hand-only kitchen scenes. If the subject got cut off by `object-fit:cover`, `object-position`, or a rounded/arched frame, fix the layout or regenerate the image.** |
| **Rounded shapes don't eat content** | **Any `border-radius` ≥ ½ the element width creates a dome that crops content underneath. If the photo's subject sits in the top portion of the source, a dome top will hide it. Soften the radius or reposition the subject.** |
| No duplicate images | Each image file used at most once across the deck |
| No opacity on images | No `opacity:` on any `<img>` — images always full brightness |
| Logo shapes centered | Content visually centered in hang tags, circles, labels — not top-aligned |
| Text contrast | All text on dark (#2E2E2E) backgrounds at sufficient opacity |
| Decorative text legible | Ghost / watermark text at ≥ .45 opacity — if lower, remove entirely |
| Images load | No broken images — every img has explicit px width+height |
| Page count = 14-16, conditionally correct | Non-digital/single-medium = 14; digital/single-medium = 15; non-digital/hybrid = 15; digital/hybrid = 16; no blank extras |
| Touchpoints are real photos | Page 12 shows generated photographs, not CSS vector boxes |
| Diverse cast | Lifestyle grid (page 11) shows racial diversity across subjects |
| Icons consistent | Page 8 icons all use the same stroke weight + corner style + line caps |
| Imagery medium matches brand | Imagery Rules page (page 10) reflects the brand's medium (photo / illustration / hybrid) — don't ship Photography Rules for an illustration brand |
| No concept clichés | No hourglass-for-time / lightbulb-for-ideas / handshake-for-trust etc. — apply the three cheesiness tests |

Only deliver after all checks pass.

---

## Step 6 — Deliver

Save the final PDF to `~/Desktop/[brand-slug]-brand-guidelines.pdf` and send the local path in a single message. Do not upload or host the PDF unless the user explicitly asks for a hosted copy.

Reply shape:

```
**[BRAND NAME] — brand guidelines**
Saved to: ~/Desktop/[brand-slug]-brand-guidelines.pdf ([actual page count] pages · 1200×850)
```

If the user is not on a Mac, save to the project working directory and emit that path instead. Never attach the PDF as a file in the chat; link by path.

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

Page 8 defines the brand's UI icon system. Every digital brand needs one — even non-tech brands benefit from consistent icons for navigation, social, and product surfaces.

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

Page 10 of the guidelines defines the brand's imagery rules. **Its title and content adapt to whatever medium the brand actually uses** — don't ship a "Photography Rules" page for an illustration-led brand and don't ship "Illustration Rules" for a brand that lives in photos.

### How to decide which page(s) to build

Look at the chosen identity option's specs (set in Step 3) and the lifestyle world you've defined:

| Brand visual medium | Page 10 setup |
|---|---|
| All photography (no illustration anywhere) | Page 10 = Photography Rules (single page) |
| All illustration (no photography anywhere) | Page 10 = Illustration Rules (single page) |
| Hybrid — both matter equally in the brand world | Page 10a = Photography Rules, Page 10b = Illustration Rules (two pages → guidelines totals 16) |
| Hybrid — one medium dominates but the other appears occasionally | Page 10 = the dominant medium's rules, with a short "minor medium" callout block at the bottom |

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

### Visual World page (page 11) also adapts

The 4-image lifestyle grid on page 11 should match the brand's medium mix:
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

## Brand Board Layout — Differentiate per Option (Step 3 Preview)

**Critical rule for the 3-page brand board preview built in Step 3 of the main skill:** do NOT use the same template for all 3 boards recolored. Each board's layout must physically embody its option's design philosophy. If you can swap colors and fonts and the layouts feel identical, the board has failed — viewers read the differences as cosmetic, not structural.

Each brand board must answer: *what would this brand's actual hero page look like?* Build the answer.

### Examples of differentiated layouts

**Magazine-cover brand** — Full-bleed photo as background covering the entire page. Massive wordmark overlaid in display type. Tagline overlaid in small text. Issue/edition tag in corner ("Vol. 01 / Cover Story"). Bottom-margin strip showing color swatches and typography credit, like a magazine masthead. Whole page should look like a Bloomberg Businessweek or NYT Magazine cover.

**Soft consumer-brand homepage hero** — Asymmetric split with a curved or rounded shape break between colored side and cream side. Big rounded type on one half, photo with rounded corners on the other. Color swatches presented as soft circles, not squares. Lots of breathing room. Should feel like the hero of bumble.com or pika.me.

**Editorial / literary essay** — Bone or cream full-bleed background. Massive italic display type centered with extreme whitespace. Photo as a small inset rectangle, not full-bleed. Pull-quote on the margin. Color swatches as a tiny ribbon at the bottom. Should feel like the opening page of a Frank Ocean visual essay or an Anthropic announcement.

**Tech-doc / dev-tool aesthetic** — Monochrome grid. Tight type. Code-like layout with bracket marks or syntax highlighting. Mono font everywhere. Color swatches as inline `code` blocks with hex strings. Should feel like Stripe's docs or GitHub's changelog.

### Required content per board (regardless of layout)

Every brand board page must include ALL of the following. The layout differentiation rule above does NOT mean cutting content — visually distinct layouts must still fit ALL the text. If a layout doesn't have room for the content, redesign the layout, don't drop content.

- Brand wordmark (set in the brand's display font)
- **A standalone logo symbol/mark — generated as a transparent PNG via `mcp__claude_ai_pika__generate_image` with `provider="gpt-image-2"` when new. Do not trace the generated symbol to SVG and do not claim it is vector. NOT just typography.** The symbol must work as a favicon, app icon, social avatar, and exported asset on transparent background at 1024×1024+.
- **A distinctive wordmark and any seal/badge treatment — custom letter spacing, ligature/cut/terminal detail, stamp geometry, or other ownable touch. Not just a Google Font in a circle, not a generic monogram seal, and not decorative filler.**
- Tagline
- Voice sample (one sentence in brand voice, quoted, with a "VOICE" label)
- Brand story (~35 words max, min 2 sentences, one compact paragraph in brand voice)
- **Lifestyle world description (~22 words max, min 1 full sentence describing the brand's visual territory — where it visually lives, who's in the frame, time of day, color temperature)** — labeled "WORLD" or similar
- Lifestyle mood image (generated via gpt-image-2 — see "Photography Must Occupy Distinct Visual Territories" rule below)
- 4-color palette with hex codes + role labels
- Display + body type specimens with named fonts

### Content budgets per board

The board is a visual decision aid, not the final brand book. Keep each board sharp enough to sell the direction at a glance:

- Tagline: 8 words max.
- Voice sample: 14 words max.
- Brand story: 35 words max, min 2 sentences. Use one compact paragraph, not 2-3 full paragraphs.
- World description: 22 words max, min 1 full sentence.
- Palette: 4 colors max on the board. Full extended palettes belong in the final guidelines.
- Type specimen: one display sample and one body sample. Do not add full hierarchy tables to boards.
- Essential body copy: 18px minimum. If it needs to be smaller to fit, rewrite the copy.

If all required content cannot fit within those budgets, the content is too verbose for a board. Rewrite it; do not shrink, stack, or layer it until it becomes technically present but visually bad.

### What NOT to do

- Same left-column-color-block-right-column-photo template recolored 3 times
- Same swatch grid in the same position on every page
- Same type specimen "Aa" treatment on every page
- Three different colors and three different fonts laid onto identical layouts
- Wordmark with no separate symbol — the logo isn't complete without a mark
- Dense archival/specimen styling where decorative rules, labels, swatches, and paragraphs intersect. If it looks like a broken certificate rather than a brand board, simplify.
- Body copy crossing through color swatches, icons, seals, or decorative overlays. Text must own a clean reading area.
- Empty mockup boxes or blank social grids. A placeholder reads as missing output, not restraint.
- Full boards that are almost entirely one muddy value range. Use image light, accent color, or negative space to create hierarchy.
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
