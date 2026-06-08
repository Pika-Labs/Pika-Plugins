# Aesthetic prompts — influencer-identity

Patterns for `generate_image` calls (provider="gpt-image-2") used in:
- Step 3 mood-board gap-fill tiles
- Step 4b voice-page atmosphere tiles

Generated imagery in this skill is atmosphere and scene context only. It must never invent a fake version of the user, their body, their pet, their partner, their family, their home, or any recurring object that belongs to them.

All prompts assume `provider="gpt-image-2"`, `quality="medium"` unless otherwise noted.

---

## Universal guardrails

Append this to every generated tile prompt:

```text
NO text anywhere in image, no captions, no watermarks, no logos, no signage with readable copy,
no UI chrome, no graphic-design overlays, iPhone snapshot, no filter, no color grade,
casual composition, slight real-life imperfection.
```

These guardrails exist because gpt-image-2 otherwise bakes pretend text onto signs, posters, packaging, journals, scarves, and bottles.

---

## Cast-diversity pattern

Use this only when a generated atmosphere tile includes strangers or background people. Generated people should be rare, faceless, partial, or from behind.

**Rule:** gpt-image-2 defaults to lighter skin tones when ethnicity is not named explicitly. Name an ethnicity per face-bearing or body-bearing prompt and vary across the set.

**Pattern:**

```text
[faceless / from-behind / partial subject description], [age range], [specific ethnicity — e.g.
Black, mixed-race East-Asian-and-white, South Asian, Latina, East Asian, Middle Eastern,
mixed-race Black-and-Latina].
```

Do not apply this to the user. The user's likeness comes only from their actual photos.

---

## Social trend framings

A mood board for an influencer identity should look like a creator's actual feed, not an atmospheric vision board. Generated tiles must use social-content framings: specific compositions trending in 2024-2026 creator content.

Every generated tile prompt must specify a framing and a moment, not just a vibe.

### Match the user's photographic register

The biggest tell that an atmosphere tile is generated is the look. AI defaults to cinematic-magazine rendering: heavy warmth, perfect composition, no real-life imperfection. Real iPhone snapshots have mixed lighting, slight exposure weirdness, casual framing, and clutter.

**Avoid by default:**
- "shot on 35mm film"
- "golden hour" as a default lighting condition
- "warm glow" / "candle warm glow"
- "shallow depth of field"
- pure scenery or art-print language

**Require:**
- "iPhone snapshot" or "iPhone HDR snapshot"
- "natural [time-of-day] lighting"
- "slightly underexposed" or "slightly overexposed" when useful
- "no filter, no color grade"
- "casual composition", "slight hand-tilt", or "slightly off-center"
- a concrete real-life imperfection: clutter, smudges, wrinkles, papers in frame, water ring, dust, half-finished drink

Match time of day to nearby curated tiles. If the user's photos are mostly daytime, do not generate everything at sunset. If their photos are dim warm interiors, do not generate harsh outdoor sunlight.

### Framings

- **phone POV in-hand** — `iPhone POV shot of [object] held in hand, [setting visible behind]`
- **mirror selfie, no face** — `mirror selfie in [setting], phone covering face or held at chest, outfit visible`
- **3/4 candid from friend's angle** — `candid 3/4 shot from a friend's POV at [scene], subject looking off-camera or cropped faceless`
- **overhead tablescape** — `overhead phone shot of a table set with [items], natural window light`
- **from-behind walking shot** — `from-behind shot of a person walking through [setting], environment leading the frame`
- **looking-up POV** — `POV looking up at [trees / arch / sky / chandelier], partial non-identifying foreground`
- **dressing-room outfit flatlay** — `outfit laid out on bed or floor: [garment list], slight clutter around it`
- **hands-doing-the-thing** — `close-up of hands [writing, holding mug, flipping pages, pouring wine] in [setting]`
- **low-light dinner / cocktails** — `low-light dinner table with [items], slight hand or glass in frame`
- **window-seat moment** — `subject reading by window or curtain, faceless or partial, soft window light`

### Moments

- the second before someone takes a sip
- the second after closing a book
- mid-laugh in a group photo with faces cropped out
- catching light through a window
- the table after the meal, glasses half-empty
- the outfit laid out the night before
- the boutique you wandered into
- the cocktail just placed on the bar
- the new book plus the coffee on Saturday morning

### Template

```text
[FRAMING with specific composition language] + [MOMENT — what's happening in this second] +
[SETTING — specific to the locked aesthetic] + [LIGHTING — overcast / window light / tungsten / harsh midday / etc.]

iPhone snapshot, natural [time-of-day] lighting, casual composition, slight hand-tilt,
slightly off-center, real-life [specific imperfection].

NO text anywhere in image, no captions, no watermarks, no logos, no readable signage.
```

---

## Voice-page atmosphere tiles

Voice-page tiles demonstrate caption modes with fresh imagery. They should be different from mood-board tiles and mode-specific:

- **Hook:** bold scroll-stopper outfit, walk, object-in-hand, or sharp location moment.
- **Story:** narrative scene, kitchen, commute, friend-angle, or day-in-the-life moment.
- **Casual selfie:** mirror, phone-obscured, back-of-head, or cropped face-free framing.
- **Vulnerable:** quiet room, unmade bed, journal, candle, late-night counter, window seat.
- **Promo:** product in lived-in context, never a styled product hero shot.

**gpt-image-2 content-policy fallback for generated selfie-register tiles:** if the model rejects "mirror selfie", "selfie", or "phone obscuring face" wording, retry once with safer language. Drop the word "selfie"; describe a hand-held phone body-framing shot, cropped outfit/body detail, or face hidden by a hand-held phone. Do not retry the same prompt or repeat rejected wording. No visible generated faces remains mandatory.

Promo-mode formula:

```text
[hand-held / mid-action verb] + [real environment with slight clutter] +
[faceless person partially in frame] + [imperfect / off-center framing] +
"NOT a styled flat lay / product hero shot / stock food photo"
```

Worked examples:

- Skincare: `Phone-camera mirror selfie of a generic person holding ONE bottle in a generic bathroom, phone fully obscuring face, toothbrush cup and towel clutter behind. NOT a styled flat lay / product hero shot / stock food photo.`
- Perfume: `Close-up of a generic wrist mid-spritz with the bottle in the other hand visible in soft focus, generic cluttered vanity behind: hairbrush, makeup, iced coffee. NOT a styled flat lay / product hero shot / stock food photo.`
- Food: `Hands rolling dough on a marble counter, towel half-falling off the side, butter and sugar in small mismatched bowls, off-center framing. NOT a styled flat lay / product hero shot / stock food photo.`

---

## What not to generate

- The user's face, body, hair, pet, partner, friends, family, kids, actual car, actual home, or recurring specific objects.
- Anything with text on it.
- Aesthetic-preset tiles: "clean girl beige", "dark academia", "Y2K", "cottagecore", unless the user explicitly named the aesthetic.
- Stock-photo people doing stock-photo things.
- Generic flat lays on white backgrounds.
- Studio-polished product shots.
- Pure scenery, landscape paintings, texture macros, or desktop-wallpaper tiles.

GPT renders atmosphere: rooms, weather, light, settings, types of objects, public places, and faceless social-content moments. The user's real world comes from their actual photos.

---

## HTML/CSS composite assembly

Build mood-board composites as deterministic HTML/CSS and render with `mcp__plugin_pika_pika__html_to_png`; do not ask gpt-image-2 to render a mood-board grid.

**Title-banded board:**
- Canvas: about 1920×1224 PNG (1920×1080 tile area + 120-144px header band).
- Tile count: exactly 12, roughly 50/50 curated + generated.
- Default layout: 6 cols × 2 rows for portrait-heavy inputs; 4 cols × 3 rows for landscape-heavy inputs.
- Header band: brand name in display font, tracked-caps vibe subtitle, generous vertical spacing.
- Use CSS `object-fit: cover`, per-tile `object-position`, and mild filters/overlays only when Step 2 names a visual shift.

**No-header PDF variant:**
- Canvas: exactly 1920×1080.
- No outer padding, no gutters, no row gaps.
- A 6×2 grid uses 320×540 tiles and fills the page exactly.
- Save/render as `mood-board-no-header.png` for PDF page 3.

**MCP render pattern:**

```json
{
  "html": "<!doctype html>...",
  "format": "png",
  "raster_options": {
    "viewport_px": {"width": 1920, "height": 1224}
  }
}
```

If `html_to_png` returns `{task_id, status}`, poll `task_status({task_id})` until `completed`, `failed`, or `cancelled`.
