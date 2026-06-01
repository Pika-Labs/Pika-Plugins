# Renderer-Safe Google Fonts

Use these snippets when `html_to_png` or `html_to_pdf` needs deterministic font loading. The URLs point directly at `fonts.gstatic.com` WOFF2 font files, so the renderer receives a font MIME type instead of a CSS or HTML page.

## Font URL gotchas

- Use direct `https://fonts.gstatic.com/s/<family>/v<version>/<hash>.woff2` font-file URLs in `@font-face src`.
- Do not use GitHub raw Google Fonts links in renderer HTML. They can resolve as `text/html` or redirect pages, which the font MIME allowlist rejects.
- Do not put `https://fonts.googleapis.com/css2?...` in `@font-face src`; it returns CSS, not a font. Use it in `<link rel="stylesheet">`, or open the CSS and copy the direct `fonts.gstatic.com` WOFF2 URL from the `/* latin */` block.
- Render one proof PNG and inspect it before generating the full set. If text falls back to Times, Arial, or a system face, fix the font source first.

## CJK / non-Latin font-family fallback

When App Store screenshots include user-supplied non-Latin text, include broad-script fallbacks in every CSS `font-family` chain. Use direct `fonts.gstatic.com` WOFF2 URLs or inline data fonts for any Noto faces you explicitly load.

```css
/* Sans / UI text */
font-family: 'BrandBody', 'Inter', 'Noto Sans SC', 'Noto Sans TC', 'Noto Sans JP', 'Noto Sans KR', 'Noto Sans Arabic', system-ui, sans-serif;

/* Display text when the brand uses a serif/display face */
font-family: 'BrandDisplay', 'Noto Serif SC', 'Noto Serif TC', 'Noto Serif JP', 'Noto Serif KR', 'Noto Sans Arabic', serif;
```

## Inter

```css
@font-face {
  font-family: 'Inter';
  src: url('https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2') format('woff2');
  font-weight: 400 700;
  font-style: normal;
  font-display: swap;
}
```

## Roboto

```css
@font-face {
  font-family: 'Roboto';
  src: url('https://fonts.gstatic.com/s/roboto/v51/KFO7CnqEu92Fr1ME7kSn66aGLdTylUAMa3yUBA.woff2') format('woff2');
  font-weight: 400 700;
  font-style: normal;
  font-display: swap;
}
```

## Open Sans

```css
@font-face {
  font-family: 'Open Sans';
  src: url('https://fonts.gstatic.com/s/opensans/v44/memvYaGs126MiZpBA-UvWbX2vVnXBbObj2OVTS-muw.woff2') format('woff2');
  font-weight: 400 700;
  font-style: normal;
  font-display: swap;
}
```

## Lato

```css
@font-face {
  font-family: 'Lato';
  src: url('https://fonts.gstatic.com/s/lato/v25/S6uyw4BMUTPHjx4wXg.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Lato';
  src: url('https://fonts.gstatic.com/s/lato/v25/S6u9w4BMUTPHh6UVSwiPGQ.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}
```

## Montserrat

```css
@font-face {
  font-family: 'Montserrat';
  src: url('https://fonts.gstatic.com/s/montserrat/v31/JTUSjIg1_i6t8kCHKm459Wlhyw.woff2') format('woff2');
  font-weight: 400 700;
  font-style: normal;
  font-display: swap;
}
```

## Poppins

```css
@font-face {
  font-family: 'Poppins';
  src: url('https://fonts.gstatic.com/s/poppins/v24/pxiEyp8kv8JHgFVrJJfecg.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Poppins';
  src: url('https://fonts.gstatic.com/s/poppins/v24/pxiByp8kv8JHgFVrLCz7Z1xlFQ.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}
```

## Playfair Display

```css
@font-face {
  font-family: 'Playfair Display';
  src: url('https://fonts.gstatic.com/s/playfairdisplay/v40/nuFiD-vYSZviVYUb_rj3ij__anPXDTzYgA.woff2') format('woff2');
  font-weight: 400 700;
  font-style: normal;
  font-display: swap;
}
```

## Merriweather

```css
@font-face {
  font-family: 'Merriweather';
  src: url('https://fonts.gstatic.com/s/merriweather/v33/u-4e0qyriQwlOrhSvowK_l5UcA6zuSYEqOzpPe3HOZJ5eX1WtLaQwmYiSeqqJ-k.woff2') format('woff2');
  font-weight: 400 700;
  font-style: normal;
  font-display: swap;
}
```

## Source Sans 3

```css
@font-face {
  font-family: 'Source Sans 3';
  src: url('https://fonts.gstatic.com/s/sourcesans3/v19/nwpStKy2OAdR1K-IwhWudF-R3w8aZQ.woff2') format('woff2');
  font-weight: 400 700;
  font-style: normal;
  font-display: swap;
}
```

## DM Sans

```css
@font-face {
  font-family: 'DM Sans';
  src: url('https://fonts.gstatic.com/s/dmsans/v17/rP2Yp2ywxg089UriI5-g4vlH9VoD8Cmcqbu0-K4.woff2') format('woff2');
  font-weight: 400 700;
  font-style: normal;
  font-display: swap;
}
```
