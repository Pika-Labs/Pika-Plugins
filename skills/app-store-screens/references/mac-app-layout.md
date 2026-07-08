# Mac app layout

Use this template when App Store listing fetch returns landscape Mac screenshots instead of iPhone portrait screenshots. Common source dimensions include **1290×806** for Mac screenshots; the final App Store Connect deliverable remains the standard **1290×2796** portrait PNG.

This is the Mac-only / hybrid-app counterpart to `default-layout.md`. The goal is to preserve the landscape UI composition and make it feel intentional inside a portrait campaign.

## Detection

After `fetch_appstore_screens`, branch to this layout when `mac_shots` is non-empty. In other words, use this layout if any returned screenshot is landscape; it is safer to preserve the landscape UI as an embedded card than to force a mixed hybrid listing through the iPhone full-frame default.

```
mac_shots = [s for s in screenshots if s.aspect_ratio_w > s.aspect_ratio_h]
# or, when only dimensions are present:
mac_shots = [s for s in screenshots if s.width > s.height]
```

Use this for hybrid apps such as Things 3, Drafts, Numbers, Day One, OmniFocus, and BBEdit when the returned screenshots are Mac UI rather than iPhone UI.

## Composition

```
1290 × 2796 canvas
┌────────────────────────────────┐
│                                │
│   Headline in brand voice      │
│   Short subhead if needed      │
│                                │
│      ┌──────────────────┐      │
│      │ landscape Mac UI │      │  ← embedded UI cards
│      └──────────────────┘      │
│                                │
│      ┌──────────────────┐      │
│      │ optional detail  │      │
│      └──────────────────┘      │
│                                │
│   Brand mark / close cue       │
└────────────────────────────────┘
```

## Layout rules

- Treat landscape screenshots as **embedded UI cards**, not phone devices.
- Place them as rounded-corner rectangles with a soft shadow inside the portrait canvas.
- Do not crop the Mac UI to portrait.
- Do not letterbox with black bars.
- Do not stretch the screenshot vertically.
- Prefer one large hero card per screen. Use a second smaller detail card only when it adds a clear feature proof.
- Keep load-bearing text and the full readable UI card inside the App Store safe zone from `render-pipeline.md`.
- Source screenshot prep still applies: inspect each landscape Mac screenshot for footer watermark bleed or listing-brand footer clutter before placing it in the card.
- Do not use the phone portrait crop on Mac screenshots. Preserve the landscape ratio in a `source-screen-crop--mac` card; if a footer must be hidden, prefer a narrow bottom fade/mask or a small landscape-preserving bottom crop inside the card.

## Card specs

- Canvas: `1290×2796`, solid or brand-gradient background.
- Hero landscape card: 1080-1160px wide, centered, `border-radius: 44-56px`, soft shadow.
- For a 1290×806 source, 1120px wide renders about 700px tall. This leaves room for a strong headline and a secondary proof/detail card without crushing the UI.
- Optional detail card: 760-900px wide, cropped only if the crop is a deliberate zoom into a readable feature region. Do not crop the main hero card.

## Things 3 benchmark pattern

The Things 3 round-2 benchmark returned six landscape Mac screenshots. The successful adaptation embedded each Mac screenshot as a clean UI card within the 1290×2796 portrait canvas, matching the app's minimal aesthetic and avoiding both destructive portrait crops and giant black letterbox bars.

Use that pattern for hybrid Mac/iOS listings: keep the Mac UI intact, make the surrounding portrait shell carry the App Store story, and use the headline to explain why the feature matters.
