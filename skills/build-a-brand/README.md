# build-a-brand · Claude Code Skill

A skill that takes any input — an idea, a website URL, a list of reference brands, product photos, or a request to refresh an existing brand — and produces a complete brand identity, ending in a 14–16-page brand guidelines PDF + a portable brand kit.

## What this skill does

Walks the user through a 4-step workflow:

1. **Read the input** — adaptive intake questions per input type + universal asks about existing brand assets, references, and whether the brand is a digital product. Finishes with a deliverable preview to invite specific guidance.
2. **Generate 3 visual brand boards (PDF)** — three complete brand directions, each with its own colors, fonts, photography style, voice samples, and logo concept. Boards diverge across at least 4 structural dimensions (density, saturation, layout philosophy, type energy, voice register). User picks one or mixes elements before guidelines build. **Hard stop until user picks.**
3. **Build the full brand guidelines PDF** — render the 14–16-page guidelines PDF for the chosen board (page count depends on whether the brand is digital and whether imagery is single-medium or hybrid). Includes: cover, strategy, foundation, logo, logo don'ts, color, typography, voice, photography, visual world, icons (conditional), touchpoints, application, digital/social, do & don't. **Hard stop until user explicitly approves the guidelines.**
4. **Export the brand kit** — after user confirms the guidelines PDF, bundle a zip with: `brand.md` (machine-readable spec), `brand-guidelines.pdf` (the visual deliverable), logo assets (symbol as transparent PNG at 8 sizes; wordmark + lockup as SVG/PNG with text-as-paths), conditional UI icon SVGs for digital brands, brand fonts (TTF), design tokens (CSS/JSON/Tailwind), and AI prompts (system prompt + copy + image starters).

**Autonomous full exception:** when a non-interactive run supplies an explicit full request (`--full`, `mode: "full"`, or asks for full guidelines / full brand book) and `cost_ack=proceed`, the brief is the spec. The skill ships all three artifacts — brand boards, guidelines, and brand kit — without waiting at the board-pick or guidelines-approval gates. If the brief is not clear enough to pick a direction responsibly, it stops once with the missing decision. Non-interactive clear briefs without explicit full depth still use quick mode.

## Install

```bash
# Extract the zip to your user-level Claude Code skills directory:
unzip build-a-brand-skill.zip -d ~/.claude/skills/

# Confirm the folder lives at:
ls ~/.claude/skills/build-a-brand/
# Should show: README.md  SKILL.md  references/
```

The skill is now available in any Claude Code session.

## Invoke

The user can trigger this skill by saying any of:
- "build me a brand"
- "make me a brand"
- "design a brand identity"
- "brand guidelines for [X]"
- "i want a brand book"
- "create a brand from scratch"
- "brand for [idea]"
- "i want a brand that feels like [X] + [Y]"
- "rebrand my [thing]"
- "visual identity for [thing]"
- `/build-a-brand`

## Folder structure

```
build-a-brand/
├── README.md                       # this file
├── SKILL.md                        # main skill instructions (4-step workflow)
└── references/
    ├── brand-directions.md         # how to structure positioning angles (WHO + WHY differentiation rule)
    ├── brand-identity.md           # logo pipeline + symbol output rules + concept lanes
    ├── brand-guidelines.md         # 14-16 page build mechanics, font rules, image rules, three-pass QA
    └── brand-md-template.md        # template for the Step 4 brand kit `brand.md` file
```

## Dependencies

- **Image generation:** Skill defaults to `gpt-image-2` for all `generate_image` calls (logos, mood photos, textures).
- **PDF rendering:** Built for Chrome headless (`--print-to-pdf`) or WeasyPrint.
- **Python + PIL:** for image transparency keying, favicon-test renders, and lockup composition.
- **Fonts:** Pulled from Google Fonts as TTF for self-hosting.

## Local vs Cloud

- **Local by default:** font downloads, image cleanup/compression, favicon tests, HTML/PDF rendering, QA screenshots/crops, logo asset assembly, tokens/prompts, and final zip packaging.
- **Cloud only where needed:** `gpt-image-2` image generation and URL/source research when required by the brief.
- PDFs and zips are saved locally by default. Hosting/upload is only used when explicitly requested.

## What the skill enforces

Embedded in the reference files as non-negotiable rules (all auto-applied during build):

### Brand strategy & options
- 3 boards must be genuinely different brands, not template recolors — diverge across at least 4 structural dimensions (density, saturation, layout, type energy, composition, photography mood, voice register, era specificity)
- Adjective audit before delivery — top-3 adjectives per board; if any 2 share 2+ adjectives, push apart
- Divergence ≠ subtraction — every board delivers the brief at 100%, never strip back to differentiate
- Era palettes are specific (Y2K = chrome/gel/holo/candy, NOT muted cottage cream; same for any named era)

### Logo
- Symbol generated via gpt-image-2, shipped as high-res transparent PNG (NOT traced to SVG)
- Symbol style is a brand-personality choice — flat, dimensional, painted, photographic, hand-drawn — whatever fits
- Mandatory checks: conceptually linked to brand, unique, recognizable at 16×16 (favicon test via PIL), ≤3 dominant colors, no text in image, true alpha=0 transparency
- 3 symbols across 3 boards must differ in concept lane (mascot / product-feature / abstract / monogram / hybrid / container)
- Wordmark is always Google Font; in the brand kit it's converted to text-as-paths SVG so it renders without the font file
- Lockup measurements perfectly measured and permanently fixed across all color variants

### Fonts
- No favorite fonts and no banned fonts — every font in Google Fonts is in the running. Diversity is enforced through process (brainstorm fresh every brand + cross-brand variety check), not gatekeeping
- Display fonts with built-in shadow/3D detail (BungeeShade, Honk, etc.) only at hero scale (40px+) and only on cream/black backgrounds

### Photography
- Hero photography shows the product IN USE (for digital products = phone/device with the actual result, or person using it). Never a representational stand-in object (the "keychain test")
- Photography occupies distinct visual territories per direction; vary medium and subject scale across the 3 boards

### Texture (for retro/era briefs)
- Textures must be AMBIENT (subtle grain, VHS noise, paper grain, grainy gradient) — not literal patterns (halftone dots, glitter flakes, scanline rows)
- Always generated via gpt-image-2 (never CSS gradients — those read as theme-applied)
- Applied full-board with mix-blend-mode + opacity 0.12–0.30

### Product clarity & layout
- Page 1 cover + Page 2 strategy must make the product unambiguous in the brand's voice (clarity through content, not robotic templates)
- Contrast gate — every text/background pair audited; pink-on-pink, lime-on-cream, dark-on-dark photos are auto-fail
- Complex fills (chrome / holographic / multi-stop gradients) only at hero scale (60px+); switch to solid + stroke at small scale
- `.content` element must have `overflow: hidden` + explicit max-height as a safety net against footer overlap

### QA & approval gates
- Three-pass QA: render every page individually → thumbnail pass → mandatory crop-and-read (PIL crops into 800×800 regions, Read each crop file — glancing at the full PNG is NOT zoom-reading)
- Approval gates are HARD stops:
  - Step 2 → Step 3: user must explicitly pick a board before guidelines build
  - Step 3 → Step 4: user must explicitly approve the guidelines PDF before kit export
  - Creative direction ("make it cuter") is feedback, not approval — explicit "yes / ship it / go" only
- In autonomous full mode, the explicit full request plus `cost_ack=proceed` is the approval source; the run records its assumptions and continues through all three artifacts instead of stopping at those gates.

*User-level Claude Code skill at `~/.claude/skills/build-a-brand/`.*
