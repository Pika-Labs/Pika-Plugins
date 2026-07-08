# Render Pipeline

How to take an HTML stage and produce a 1290x2796 PNG that is deliverable to App Store Connect.

## Renderer

Use Pika MCP `html_to_png`. It runs server-side Chromium and returns a hosted PNG URL. Do not run local Chrome headless by default.

Production request shape:

```
html_to_png(
  html: screen_html,
  short_link_map: render_asset_map,  // e.g. { "s://screen01": product_screen_url }
  format: "png",
  mode: "async",
  wait_for: "domcontentloaded",
  raster_options: {
    viewport_px: { width: 1290, height: 2796 },
    device_scale: 1
  }
)
```

Use `mode:"sync"` only for quick one-page checks. Production screenshots are large; async is safer.

Example completed response:

```
{"status":"completed","file_url":"https://cdn.pika.art/v2/files/agent/4d944981-9897-40b6-9e37-533c2a90b541/5a863672-0835-4901-87a8-df8933d69cd4.png","format":"png","page_count":1,"byte_size":3806}
```

### Sparse-but-valid HTML

The renderer may receive a deliberately sparse App Store stage: a centered headline, short subhead, one real `<img>` device screenshot, and no generated background. That is valid when the HTML is a complete document, uses a real image via HTTPS or `short_link_map`, and has no placeholder tokens such as `[headline]`, `{{image}}`, or unsubstituted template variables.

If `html_to_png` returns `invalid_input` with reason `suspicious_html_body` for sparse-but-valid HTML that contains a real image and no placeholder tokens, treat it as a renderer false-positive. Do not retry the same body more than once. First confirm the image URL expands through `short_link_map` and the HTML has concrete copy; if it still fails, surface the false-positive with the render payload summary instead of burning repeated MCP calls.

## Asset Rules

Server-side Chromium cannot read local `file://` paths. Every image/font in the HTML must be one of:

- HTTPS URL returned by Pika tools
- Public HTTPS raw asset URL
- Inline `data:` URI

For local screenshots, product photos, or generated local artifacts, call `upload_asset` first and use the returned `public_url`.

For long or repeated CDN URLs, keep the HTML readable with `short_link_map`: put tokens such as `s://screen01` or `s://font0001` inside `<img src>` and CSS `url(...)`, then pass the full HTTPS URLs in the `html_to_png` request. Do not paste URLs that contain whitespace or omit `https://`; the renderer rejects those before fetch as `InvalidInput` / malformed asset URL and surfaces the exact bad URL.

`upload_asset` does not accept font files, so fonts need direct `fonts.gstatic.com` WOFF2 font-file URLs or inline `data:font/...` sources.

JavaScript is disabled by default in the renderer. Build static HTML/CSS stages; do not depend on runtime JS for layout.

## Stage Sizing

The HTML must declare an exact 1290x2796 canvas. Do not use viewport units (`vh`/`vw`) for the stage.

Top of every screen HTML:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; padding: 0; background: #000; }
    .stage {
      width: 1290px;
      height: 2796px;
      position: relative;
      overflow: hidden;
    }
  </style>
</head>
<body>
  <div class="stage">
    <!-- screen content -->
  </div>
</body>
</html>
```

The black body background is a guardrail. If the stage does not fill the render, black bleed makes the sizing bug obvious.

## Apple Safe Zones

App Store Connect overlays its own chrome on screenshots in certain views. Keep critical content inside the safe area.

```
0px        +---------------------------+
           | decoration only            | top 100px
100px      +---------------------------+
           |                           |
           | SAFE CONTENT ZONE         |
           |                           |
2696px     +---------------------------+
           | decoration only            | bottom 100px
2796px     +---------------------------+
```

Visuals can live in the top/bottom 100px bands. Load-bearing headlines and product UI cannot.

Strict text margin: text block bounding boxes for headlines, eyebrows, subheads,
CTA text, labels, and any product UI must be fully inside y=180..2616. The top
and bottom 100px bands are hard no-go zones; the extra 80px gives breathing room
for status-bar chrome, App Store search-result cropping, and text ascenders. If
a safe-zone audit finds load-bearing text with y < 180, or a block bottom past
y=2616, reject and rerender.

## Device Compositing

Preferred source:

- Transparent PNG export from Figma/simulator
- Individual phone screenshots, not a strip
- High enough resolution that scaling to 1000px width does not blur text

### Source screenshot prep

Classify each fetched App Store screenshot before applying a device layout:

- `clean_ui_capture`: raw app UI suitable for a device mockup.
- `composed_marketing`: a pre-composed marketing screen, not a clean in-app screenshot.
- `legacy_footer_cleanup`: clean UI that needs only footer cleanup before device embedding.

Composed-marketing source signals include a baked headline or subhead already above the phone, a phone that bleeds or clips against the source edge, campaign-color background art, and a source that already reads as a finished marketing screen rather than clean product UI. The 2025 Notion screenshots use this shape.

For `composed_marketing`, first try to replace it with a clean UI source by using `mcp__claude_ai_pika__capture_website` on a real product surface or by asking for simulator/Figma/raw UI exports. If no clean source exists, set `source_treatment=composed_passthrough` and present the composed screen as-is. Do not reframe it in another device mockup, do not add or generate a second headline/subhead, and do not rely on the legacy bottom crop to fix it. A bottom footer crop removes the wrong area and still leaves a double-headline result.

Fetched App Store screenshots sometimes include listing footers or watermark bleed that should not appear inside the device mockup. This legacy footer cleanup applies only after a source is classified as otherwise clean UI. Example: older Notion screenshots may include `NOTION · NOTES, TASKS, AI` at the bottom, which can overlap list content after compositing. Before embedding the source screenshot in the device mockup, crop or mask the bottom 6-8% when that footer is visible.

Use a top-anchored phone crop so the product UI remains stable. The wrapper must define its own aspect ratio; relying on `height:100%` without a definite parent height can make the crop a no-op.

```html
<div class="source-screen-crop source-screen-crop--phone" style="
  width:100%;
  aspect-ratio:1290 / 2796;
  overflow:hidden;
  position:relative;
">
  <img src="s://screen01" style="
    width:100%;
    height:calc(100% / 0.92);   /* shows the top 92% while cropping the bottom 8% */
    object-fit:cover;
    object-position:top center;
    display:block;
  ">
</div>
```

If the footer overlaps real UI and a crop would cut off important content, place a brand-color fade over only the footer area. Either path must remove the footer watermark before delivery.

For Mac or hybrid-app landscape screenshots (`mac_shots`), do not route the image through the phone portrait crop. Preserve the landscape aspect ratio inside an embedded UI card and apply footer cleanup inside that card:

```html
<div class="source-screen-crop source-screen-crop--mac" style="
  width:100%;
  aspect-ratio:1290 / 806;
  overflow:hidden;
  position:relative;
">
  <img src="s://mac-screen01" style="
    width:100%;
    height:100%;
    object-fit:cover;
    object-position:top center;
    display:block;
  ">
  <div style="
    position:absolute;
    left:0;
    right:0;
    bottom:0;
    height:6%;
    background:linear-gradient(to bottom, rgba(245,240,230,0), #F5F0E6);
    pointer-events:none;
  "></div>
</div>
```

Use the Mac mask only when footer watermark bleed is visible; otherwise keep the Mac screenshot untouched. If a crop is necessary, crop a small bottom band while preserving the landscape card ratio rather than using the phone portrait crop.

Default CSS:

```html
<div class="device" style="
  position: absolute;
  top: 580px;
  left: 50%;
  transform: translateX(-50%);
  width: 1000px;
  border-radius: 96px;
  overflow: hidden;
  filter: drop-shadow(0 80px 100px rgba(28,26,24,0.22));
">
  <img src="https://cdn.pika.art/..." style="
    width: 100%;
    display: block;
  ">
</div>
```

If the source PNG already has transparent rounded corners, remove `border-radius` and `overflow:hidden` and let the alpha channel define the shape.

Current MCP gap: there is no server-side uniform rounded-corner cleaner equivalent to the old local `clean_phone_uniform()` PIL recipe. If Figma source PNGs contain gray/colored corner triangles, ask for transparent exports or use a real phone mockup cutout. CSS masking is acceptable for iteration, but visually QA every corner because it can reveal source-background artifacts.

Position rule:

- Full-frame default: `top:580px`, `width:1000px`, bottom lands at about y=2748 with breathing room.
- Bleed variant: `top >= 819`, so the rounded bottom curve is fully past y=2796.
- Avoid any value between 581 and 818 for bleed layouts; it slices through the bottom corner mid-curve.

For tilt, wrap the device in `transform: translateX(-50%) rotate(-3deg)`. Stay under 5 degrees unless the brand is deliberately playful.

## Font Loading

Fonts that do not load make the campaign look broken. Use explicit `@font-face` declarations:

```css
@font-face {
  font-family: 'BrandDisplay';
  src: url('https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2') format('woff2');
  font-weight: 400 700;
  font-style: normal;
  font-display: swap;
}
```

**Font URL gotchas:**

- Use direct `https://fonts.gstatic.com/s/<family>/v<version>/<hash>.woff2` font-file URLs. These serve `font/woff2` with open CORS and pass the renderer MIME allowlist.
- Do not use GitHub raw Google Fonts links in MCP-rendered HTML. They can resolve as `text/html` or redirect pages, which the font allowlist rejects.
- Do not put a Google Fonts CSS URL such as `https://fonts.googleapis.com/css2?...` inside `@font-face src`; that URL returns CSS, not a font file. Use the CSS URL in a `<link rel="stylesheet">` tag, or open the CSS and copy the direct `fonts.gstatic.com` WOFF2 URL from the `/* latin */` block.

Inline data URI fonts are also acceptable:

```css
@font-face {
  font-family: 'BrandDisplay';
  src: url('data:font/ttf;base64,...') format('truetype');
}
```

Avoid Google Fonts `@import` chains; direct font-file URLs are easier for the server renderer to prefetch and inline. After the first render, inspect the screenshot before generating the rest. If type falls back to a system face, fix the font source first.

### CJK / non-Latin fallback

App Store screenshots often include user-supplied app names, testimonials, or product UI labels. Every `font-family` chain in rendered HTML should include broad-script fallbacks so non-Latin glyphs do not become tofu boxes:

```css
font-family: 'BrandDisplay', 'BrandBody', 'Noto Sans SC', 'Noto Sans TC', 'Noto Sans JP', 'Noto Sans KR', 'Noto Sans Arabic', system-ui, sans-serif;
```

Chromium uses per-glyph fallback: Latin glyphs stay in the brand face when available, while CJK, Arabic, Cyrillic, and other missing glyphs resolve to Noto/system fallbacks. Load Noto fallback faces with direct `fonts.gstatic.com` WOFF2 URLs or inline `data:font/...`, following the same MIME-safe rules as brand fonts.

## Retina Sharpness

Text in App Store screenshots needs to look crisp on a 6.9-inch device. `viewport_px:1290x2796` and `device_scale:1` produce the exact final pixel size.

If text looks fuzzy:

- Check `.stage` is exactly 1290x2796.
- Check `raster_options.viewport_px` is exactly 1290x2796.
- Check `device_scale` is 1.
- Check no CSS `transform: scale()` is shrinking text and then scaling it back up.

## Image Asset Prep

When `generate_image` returns a hosted URL, use it directly in HTML. When the user provides local files, upload them first:

```
upload_asset(filename:"screen.png", mime_type:"image/png", size_bytes:<size>)
# PUT bytes to presigned_url
# Use public_url in <img src="...">
```

Remote assets sometimes fail if they block server requests. In that case, upload the file through Pika and use the returned CDN URL.

## Contact Sheet

After all six individual PNGs render, build a `_preview.png` contact sheet with one more `html_to_png` call. Use the six returned PNG URLs in a 3x2 grid.
If the six URLs make the contact-sheet HTML noisy, use `short_link_map` again and place `s://shot0001`, `s://shot0002`, etc. in the `<img src>` values.

```html
<div style="
  width: 2400px;
  min-height: 1800px;
  background: #f5f0e6;
  padding: 80px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
">
  <div>
    <img src="https://cdn.pika.art/.../01_hook.png" style="width: 100%; border-radius: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
    <p style="font-family: sans-serif; font-size: 18px; margin-top: 12px; opacity: 0.6;">1 - Hook</p>
  </div>
  <!-- repeat for 02-06 -->
</div>
```

Render with a contact-sheet viewport large enough for the grid, usually `2400x1900` or taller if labels wrap.

## Pre-delivery Checklist

Before handing files to the user, verify:

- [ ] Every individual PNG is exactly 1290x2796.
- [ ] Brand fonts loaded, not system fallbacks.
- [ ] No black bleed at edges.
- [ ] Safe-zone audit passes: no load-bearing text block bounding boxes at y < 180 or past y=2616; reject and rerender failures.
- [ ] Source screenshot prep applied: no footer watermark bleed such as `NOTION · NOTES, TASKS, AI` remains inside device mockups.
- [ ] Composed-marketing sources use `clean_ui_capture` or `composed_passthrough`; no baked headline is stacked under a generated headline and no composed source is embedded inside an extra device mockup.
- [ ] Dark-mode subheads use a light token such as `--subhead-on-dark: #B5B4B0`, not medium gray on near-black.
- [ ] Proof screen includes a visible proof artifact; text-only proof claims are rejected.
- [ ] Device corners look consistent across all six.
- [ ] First two screens are legible when viewed at 25%.
- [ ] Contact sheet shows visual variety across the six.
- [ ] All six use colors from `brand.md`'s palette.
- [ ] Real app UI appears in the device area; no hallucinated placeholder UI.
