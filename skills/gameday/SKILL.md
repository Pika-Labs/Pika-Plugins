---
name: gameday
description: >-
  Put a fan into the game. The user uploads one photo of themselves and names
  their favorite team; generate a 6-photo matchday-superfan carousel — six
  separate images of that same person at the game in their team's kit. Triggers:
  "/gameday", "make me an [team] superfan", "put me at the game", "gameday
  carousel". Requires the Pika MCP.
argument-hint: <user-photo-path-or-url> <favorite-team>
---

# gameday

The user uploads **one photo of themselves** and gives their **favorite team**. You generate **6 separate photos** of that person as a superfan at the game — a matchday carousel.

## Steps

1. **Get the two inputs.** Photo (local path or URL) and favorite team. If the photo is a local path, upload it (`upload_asset` → PUT to `presigned_url` → use `public_url`). Call the resulting URL `photo`.

2. **Fill the team.** From the team name, fill `{team}` and `{kit colors}` (two main colors + stripe pattern, e.g. Argentina → "sky-blue and white vertical stripes"). Describe colors, not crests/logos.

3. **Generate the 6 photos.** Make **6 separate `generate_image` calls**, one per prompt below, passing the same `photo` as `reference_images` on every call (this keeps the face identical). Settings each call: `provider: gpt-image-2`, `reference_images: [photo]`, `aspect_ratio: 3:4`, `quality: medium`, `output_format: png`.

4. **Deliver the 6 separate images** in order. Six files — never one image split into panels.

## The 6 prompts (substitute `{team}` / `{kit colors}`)

**p1 — Arrival at the stadium**
```
Ultra-realistic candid lifestyle sports-fan photograph, single vertical phone photo, 3:4. The
subject is the SAME person as the reference photo — preserve their exact face, hair, features,
skin tone and vibe; natural candid expression. A passionate {team} football supporter arriving on
match day, wearing an official {team} home jersey ({kit colors}) with a matching {kit colors}
{team} supporter scarf looped around the neck, effortless game-day styling. They walk confidently
toward a big modern stadium's entrance gates, golden late-afternoon sun flaring low behind the
stands, long warm shadows. Streams of other fans in the same {kit colors} flow around them,
flags and team colors everywhere, a buzzing pre-match crowd. Candid street-style framing, slight
motion in the step, shallow depth of field on the background, realistic smartphone photo look,
authentic and unposed.
```

**p2 — In the seats before kickoff**
```
Ultra-realistic candid lifestyle sports-fan photograph, single vertical phone photo, 3:4. The
subject is the SAME person as the reference photo — preserve their exact face, hair, features,
skin tone and vibe. A {team} supporter in an official {team} jersey ({kit colors}) and matching
{team} scarf, sitting in the stadium seats before kickoff, leaning casually on the armrest, looking
thoughtfully out toward the green pitch. Behind them a massive blurred crowd fills the stands,
a sea of {kit colors}, the floodlights and tiered stadium bowl rising up. Soft natural daylight,
candid quiet-before-the-storm mood, gentle bokeh on the crowd, realistic smartphone photo look,
authentic and unposed.
```

**p3 — Laughing with a friend in the stands**
```
Ultra-realistic candid lifestyle sports-fan photograph, single vertical phone photo, 3:4. The
subject is the SAME person as the reference photo — preserve their exact face, hair, features,
skin tone and vibe. A {team} supporter in an official {team} jersey ({kit colors}) and matching
{team} scarf, standing in the stands smiling and laughing mid-conversation with a friend beside
them, a joyful candid fan moment caught off-guard. A packed, colorful crowd in {kit colors} rises
behind them, banners and flags waving, lively pre-match energy. Bright stadium daylight, genuine
happy expression, slight candid blur, realistic smartphone photo look, authentic and unposed.
```

**p4 — Goal celebration (hero shot)**
```
Ultra-realistic candid lifestyle sports-fan photograph, single vertical phone photo, 3:4. The
subject is the SAME person as the reference photo — preserve their exact face, hair, features,
skin tone and vibe. A {team} supporter in an official {team} jersey ({kit colors}) caught at the
exact moment of a goal — standing in the stands cheering, both arms thrown high, the {kit colors}
{team} scarf stretched wide overhead with both hands, mouth open in an ecstatic roar of pure
euphoria. All around them the crowd erupts, fans jumping and screaming in {kit colors}, streamers
and confetti in the floodlit air, electric chaotic energy. Dynamic candid framing, slight motion
blur from the celebration, high contrast stadium lights, realistic smartphone photo look,
authentic and unposed.
```

**p5 — Crowd selfie close-up**
```
Ultra-realistic candid lifestyle sports-fan photograph, single vertical phone photo, 3:4. The
subject is the SAME person as the reference photo — preserve their exact face, hair, features,
skin tone and vibe. A close-up selfie-style portrait of a {team} supporter in the packed crowd,
wearing an official {team} jersey ({kit colors}) with the {kit colors} {team} scarf draped behind
their shoulders, giving a big genuine smile straight to camera, cheek-to-cheek with the roaring
stands behind. Bright stadium floodlight bokeh and a blurred sea of fans in {kit colors} fill the
background, evening match atmosphere. Slight selfie wide-angle look, warm skin tones, realistic
smartphone photo, authentic and unposed.
```

**p6 — Flag-draped on the concourse**
```
Ultra-realistic candid lifestyle sports-fan photograph, single vertical phone photo, 3:4. The
subject is the SAME person as the reference photo — preserve their exact face, hair, features,
skin tone and vibe. A {team} supporter walking along the open stadium concourse with a large
{kit colors} {team} flag draped over their shoulders like a cape, wearing the official {team}
jersey ({kit colors}) underneath, proud triumphant expression, chin up. Warm golden-hour light
pours through the concourse openings, lens flare, fellow fans in {kit colors} milling all around,
the stadium structure framing them. Candid editorial street-style framing, cinematic warm tones,
realistic smartphone photo look, authentic and unposed.
```
