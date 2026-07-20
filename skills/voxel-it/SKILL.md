---
name: voxel-it
description: >
  Use when the user asks for voxel it or a task matching the examples below.
  Voxel-It — turn any photo into a high-quality Minecraft screenshot, keeping the
  HUMAN subject(s) fully photorealistic while the rest of the frame becomes
  detailed Minecraft block geometry, then cinematic-color-grade the whole frame to
  the photo's mood so the real person and the voxel world read as one image. A
  Step 0 router reads the photo and picks ONE of three input-driven modes:
  object-only (voxelize just the held/featured object + its tableware, keep the
  person AND background photoreal, float Minecraft loot-tag labels), background-only
  (voxelize the background/environment, keep the person and any incidental object
  photoreal, no tags), or object+background (voxelize everything except the person).
  Single still-image edit via one generate_image_edit call. This skill absorbs the old
  minecraft-food and minecraft-world trends. Triggers: "voxel it", "voxelize this",
  "minecraft world", "minecraft food", "minecraftify this", "minecraftify the
  background", "voxel food", "minecraft my photo", "put me in minecraft but keep me
  real", "loot tags on my food", "minecraft everything but the person", "/voxel-it".
required-capabilities:
  - upload_asset
  - generate_image_edit
  - remove_background
---

# voxel-it

> Tools below are **Pika MCP** tools, named bare — call each under whatever prefix your session exposes for the Pika MCP.

One skill, one engine: turn a photo into a Minecraft screenshot where the
**human stays photoreal** and the rest of the frame becomes **voxel blocks**,
unified by a cinematic color grade. A **Step 0 router** reads the photo and picks
**one of three modes** — deciding *what* gets voxelized (the featured object, the
background, or everything except the person) and whether to float **Minecraft
"loot tags"** naming the hero objects. This one skill absorbs both the old
**Minecraft-Food** trend (object-only) and the old **Minecraft-World** trend
(object+background).

The conversion engine is the **@rohxit7 viral recipe**, verbatim (Instagram, 194K
likes, #minecraft #prompt #chatgpt). The object-only prompt and loot-tag clause
are salvaged from the retired **Minecraft-Food** trend (@aibyjoe "Minecraft
Food").

**The effect, precisely:**

1. **Keep photorealistic & untouched — the PERSON** (face, skin, hair, clothing,
   pose, proportions). No stylization, no blockifying — in every mode.
2. **Convert to Minecraft — the parts the chosen mode targets** (some subset of:
   terrain, structures, plants, objects, furniture, vehicles, food, drinks, sky,
   background): clean cubic/voxel geometry, crisp 16×16-style textures,
   modern-Minecraft-screenshot quality (premium SEUS/BSL shaders — realistic
   light, soft shadows, AO, volumetric light, sharp edges).
3. **Spatial fidelity (strict):** exact camera, framing, composition; every
   element in its original position and size; nothing added/removed/rearranged.
4. **Cinematic color grade (the unifier):** analyze the source mood and grade the
   whole frame to match, cohesive across real human + voxel world so it's one
   image, not a pasted cutout.
5. **(Conditional) Loot tags** — object-only mode only; see Step 0.

> **Identity note:** maskless single full-canvas edit (per the recipe), so the
> face is *regenerated* and can drift slightly. Accepted for color cohesion. For
> a byte-perfect face, see the advanced mask note at the bottom.

## Step 0 — Router: pick the MODE

Read the photo and commit to exactly ONE mode. **State the decision as a single
line — `MODE: object-only` / `MODE: background-only` / `MODE: object+background`
— then apply the matching prompt block in Step 3.** The engine, color grade, and
quality bar are identical across modes; the only delta is *what* voxelizes and
whether loot tags float.

The three modes:

- **object-only** — voxelize ONLY the held/featured object (food / drink /
  product) **and its own tableware**. Keep the **PERSON** and the **BACKGROUND**
  fully photorealistic. Float a Minecraft loot-tag label above each hero object.
  *(This is the old Minecraft-Food look.)*
- **background-only** — voxelize the **BACKGROUND / environment** into Minecraft
  blocks. Keep the **PERSON** photorealistic; if an incidental object is present,
  keep it photoreal too. **No loot tags.** *(A person standing in a place, now in
  a voxel world — but anything they're holding stays real.)*
- **object+background** — voxelize **EVERYTHING except the person** (the object
  AND the background). Loot tags optional. *(The old full-voxelize Minecraft-World
  default.)*

**Decision tree (default detection):**

```
Does the user EXPLICITLY ask to voxelize everything?
  ("voxelize everything" / "object and background" / "full voxel world")
    → MODE: object+background
Else, is a human FACE or BODY present?
    ├─ Person present + a held/featured object (food/product) is the subject?
    │     → MODE: object-only        (float loot tags on the object)
    └─ Person present, NO featured object (people-in-a-place shot)?
          → MODE: background-only     (the default for face-in-a-scene shots)
No person present?
    ├─ Pure object shot (a meal, a product, a flat-lay, a desk of gear)?
    │     → MODE: object-only
    └─ Landscape / scene with no featured object?
          → MODE: background-only
Genuinely ambiguous (can't tell if the object or the scene is the point)?
    → ask the user ONE line: "voxelize just the object, just the background,
      or everything but you?"
```

The routing intent: a **face with no featured object defaults to
background-only** (put the person in a voxel world, keep them and anything
incidental real). A **featured object → object-only** (voxelize the hero item,
tag it, keep person + scene real). **object+background only on an explicit
request.**

## Inputs

- `<source>` — any photo (path, URL, or chat-pasted image). Works on object
  shots, person+object shots, and wide scenes alike.

## Empty-args menu

1. "Drop the photo (path, URL, or paste it). I'll auto-pick the mode — object-only
   (voxelize just the food/product you're featuring, with Minecraft loot tags),
   background-only (voxelize the scene around you, keep you and anything you're
   holding real), or object+background (voxelize everything but you). Tell me if
   you want to force a specific mode."

(No provider question — always gpt-image-2; see Engine.)

## Engine — always `gpt-image-2`

`gpt-image-2`, `quality="high"`, `output_format="png"`. It's the strong editor the
recipe needs and commits the world to blocks. **Do not use nano-banana-pro** — it
*under-voxelizes* (preserves subjects as photoreal even when told to block-ify),
so the world barely changes (audited over a 6-scene batch).

**Timeout gotcha:** at `quality="high"` a synchronous call often exceeds the
~260s tool budget and the client times out. Always call with `background:true`
and poll `task_status(task_id)` in a tight loop until `completed`.

## Workflow

Working dir: `<project>/voxel-it/<run-id>/` — each run its own folder.

### Step 1 — Get the source as a Pika-CDN URL

- **HTTPS URL?** Use it directly.
- **Local file?** Upload (Step 2). Convert HEIC: `sips -s format jpeg in.HEIC
  --out out.jpg` — this strips the EXIF orientation flag, so the JPEG can land
  on its side. **View it**; only if it's sideways, rotate upright with `sips -r
  90` or `sips -r 270` (whichever way it's tilted), then view again to confirm.
  The model bakes the reference pixels as-is, so it must be upright before upload.
- **Chat-pasted image?** Not reliably on disk. If the user names a file (e.g. a
  Desktop screenshot — macOS uses a narrow no-break space U+202F before AM/PM, so
  match via a glob), copy it. Otherwise extract from the session transcript:

  ```bash
  cd ~/.claude/projects/<project-slug>/
  SRC=$(ls -t *.jsonl | head -1)   # newest = current session
  python3 - "$SRC" "<run-dir>" <<'PY'
  import json, base64, sys, os, hashlib
  src, out = sys.argv[1], sys.argv[2]; imgs=[]
  for line in open(src):
      try: o=json.loads(line)
      except: continue
      m=o.get("message") if isinstance(o,dict) else None
      role=(m or {}).get("role") if isinstance(m,dict) else o.get("role")
      if role!="user": continue
      c=(m or o).get("content")
      if not isinstance(c,list): continue
      for p in c:
          if isinstance(p,dict) and p.get("type")=="image" and isinstance(p.get("source"),dict):
              s=p["source"]
              if s.get("data") and s.get("media_type","").startswith("image/"):
                  imgs.append((s["media_type"], s["data"]))
  # save the last N pasted images (newest turn). Adjust [-1:] to [-N:] for batches.
  for i,(mt,data) in enumerate(imgs[-1:], 1):
      b=base64.b64decode(data); ext={"image/webp":"webp","image/jpeg":"jpg","image/png":"png"}.get(mt,"jpg")
      p=os.path.join(out,f"source_{i}.{ext}"); open(p,"wb").write(b)
      print(p, len(b), "sha256", hashlib.sha256(b).hexdigest())
  PY
  ```

  Always **read the saved file back** (view it) before spending a generation.

### Step 2 — Upload to Pika CDN

`upload_asset({filename, mime_type, size_bytes, sha256})`
→ PUT the bytes to `presigned_url` with the **exact** `content_type` from the
response (`curl -X PUT -H "content-type: <type>" --upload-file <file>
"<presigned_url>"`, expect `HTTP 200`) → use the returned `public_url`.

### Step 3 — Run the edit (branch on the Step 0 mode)

`generate_image_edit` with `provider="gpt-image-2"`,
`quality="high"`, `output_format="png"`, `background=true` (poll), the CDN URL in
`images`, and `aspect_ratio: "auto"` — the worker measures the
reference and matches its orientation, so you never hand-pick or recompute the
ratio. Fill the COLOR GRADING mood line from your read of the photo.

**Pick the prompt block for the mode you committed to in Step 0.**

---

#### MODE: object+background (voxelize everything except the person)

Use the @rohxit7 recipe verbatim:

> ROLE: You are an expert image-transformation artist specializing in stylized
> photo-to-game-world conversions and cinematic color grading.
>
> TASK: Transform the attached reference photo into a high-quality Minecraft
> screenshot in which the human subject(s) remain fully photorealistic and
> untouched, while everything else in the scene is converted into detailed
> Minecraft block geometry — then apply cinematic color grading derived from the
> original photo's mood.
>
> CORE CONCEPT (the hero idea — do not deviate): A real, photorealistic human
> standing inside a fully voxel/blocky Minecraft world. The contrast between the
> realistic person and the blocky environment is the entire point of this image.
>
> CONVERSION RULES:
> 1. KEEP PHOTOREALISTIC (do NOT alter): the human subject(s) from the reference
> photo; their face, skin, hair, clothing, pose, and proportions; render them
> exactly as they appear — no stylization, no blockifying.
> 2. CONVERT TO MINECRAFT (high-quality block model): all non-human elements —
> terrain, ground, plants, objects, structures, furniture, vehicles, sky, and
> background. Use clean cubic/voxel geometry with crisp 16x16-style block
> textures. Quality reference: a modern Minecraft screenshot rendered with
> premium shaders (e.g., SEUS / BSL style) — realistic lighting, soft shadows,
> ambient occlusion, volumetric light, sharp block edges.
> 3. SPATIAL FIDELITY (strict — this is a conversion, not a reimagining):
> preserve the EXACT camera angle, framing, and composition; keep every element
> in its ORIGINAL position; keep every element at its ORIGINAL relative size and
> scale; the human must occupy the same place and proportion as in the source; do
> NOT add, remove, or rearrange objects.
>
> COLOR GRADING (apply AFTER the Minecraft conversion):
> Step 1 — ANALYZE the original photo first: identify its time of day, lighting
> direction, dominant color palette, warmth/coolness, and overall mood ([fill in
> the mood you read, e.g. "moody night street, cool blue sky with warm street-lamp
> glow" / "golden-hour warm" / "overcast neutral"]).
> Step 2 — APPLY cinematic color grading that matches that analyzed mood: filmic
> contrast curve, balanced highlights and shadows; color tone consistent with the
> original photo's atmosphere; subtle vignette and depth, cohesive across both the
> realistic human and the blocky environment so they feel like one unified image.
>
> OUTPUT SPECIFICATIONS: single high-resolution image; sharp, detailed,
> professional Minecraft-screenshot quality; photorealistic human + voxel world,
> seamlessly color-graded.
>
> SELF-CHECK BEFORE FINALIZING: Is the human still 100% photorealistic and
> unchanged? Is everything else clearly Minecraft block geometry? Are positions,
> sizes, and composition identical to the source? Does the color grade match the
> original photo's analyzed mood? Does the realistic human and blocky world feel
> unified, not pasted?

**Loot tags in object+background are OPTIONAL.** If the user wants them (or there's
a clear namable hero object), insert the LOOT TAGS block below between CONVERSION
RULES and COLOR GRADING, and add its tag line to TASK + SELF-CHECK:

> LOOT TAGS: above or near EACH hero voxelized object, float a Minecraft
> inventory-style name tag — clean white pixel/bitmap font on a dark
> semi-transparent rounded rectangle (a Minecraft item-tooltip / named-entity
> tag) — naming that item: [list each hero object → its short name, e.g. "Mojito",
> "Sesame Latte", "Apple Cake", "Air Jordan 1", "Leica M6"]. Keep tags tidy,
> crisp, readable, non-overlapping, floating just above each item, and NEVER
> covering a person's face. (add to SELF-CHECK: "Does each hero object have a
> clean, readable Minecraft name tag that doesn't cover a face?")

---

#### MODE: background-only (voxelize the scene, keep the person AND any incidental object real)

Same @rohxit7 recipe as object+background, with **CONVERSION RULE 1 widened** so
the person is not the ONLY thing kept real: also keep any incidental held/foreground
object photorealistic. Concretely, replace RULE 1 and RULE 2 with:

> 1. KEEP PHOTOREALISTIC (do NOT alter): the human subject(s) — face, skin, hair,
> clothing, pose, proportions — AND any object the person is holding or that sits
> in the immediate foreground (a phone, a drink, a bag, a prop). Render all of
> these exactly as they appear — no stylization, no blockifying.
> 2. CONVERT TO MINECRAFT (high-quality block model): the BACKGROUND and
> ENVIRONMENT only — terrain, ground, plants, structures, furniture, vehicles,
> sky, and scenery behind and around the subject. Use clean cubic/voxel geometry
> with crisp 16x16-style block textures. Quality reference: a modern Minecraft
> screenshot with premium shaders (SEUS / BSL) — realistic lighting, soft
> shadows, ambient occlusion, volumetric light, sharp block edges. Do NOT
> voxelize the person or anything they are holding.

Keep CORE CONCEPT, SPATIAL FIDELITY (RULE 3), COLOR GRADING, OUTPUT
SPECIFICATIONS, and SELF-CHECK from the object+background block verbatim (they
apply unchanged). **No loot tags in background-only.**

---

#### MODE: object-only (voxelize just the featured object + its tableware; keep the person AND background real; float loot tags)

This is the retired Minecraft-Food recipe. Fill the bracketed list per item and
keep the KEEP and label clauses verbatim:

> Edit this exact photo. KEEP [the person + their face, hair, hands, clothing,
> accessories /OR for a flat-lay: the table, containers, plates, cups, tray,
> utensils] and the background/scene and lighting 100% PHOTOREALISTIC and
> unchanged — do not stylize [the person] at all.
>
> ONLY transform the FOOD, DRINK and the food's TABLEWARE into 3D Minecraft
> voxel blocks — chunky, low-resolution cube-pixel geometry with flat blocky
> textures, exactly like Minecraft items, each sitting naturally where the real
> item was: [per-item mapping — e.g. "the ramen bowl → a blocky voxel bowl of
> yellow cube-noodles"; "the pepperoni slice → cube crust + voxel cheese + cube
> pepperoni discs"; "the steamed rice → a mound of white voxel rice cubes"].
>
> Above or near EACH transformed item, add a Minecraft inventory-style text
> label: clean white pixel/bitmap font on a dark semi-transparent rounded
> rectangle, naming the item (e.g. [item labels]). Keep labels tidy and
> readable, non-overlapping, and never over [the person's face].
>
> Final look: a real photorealistic [person / scene], but every piece of food,
> drink and tableware is a Minecraft voxel object with floating Minecraft
> inventory labels.

Then apply the **COLOR GRADING** step from the object+background block (analyze
the source mood, grade the whole frame to match) so the voxel object and the real
person/scene read as one image.

**Enumerate before you generate:** the single biggest lever on object-only
quality is naming each food/product item AND the voxel object it should become,
item by item, in the prompt. Read the source and list every dish / drink / utensil
first; generic "turn the food into blocks" is mushy, per-item mapping lands.

---

**Groups:** in any mode, name *every* person in the KEEP clause so none gets
blockified. **Contact objects** (held mug, drink, plate) voxelize with the object
in object-only / object+background, but stay real in background-only.

### Step 4 — Download, show, open (+ rotation check)

Download to `<run-dir>/voxel-it-<subject>.png`, show it, `open` in Finder
(no analyze_media re-check — just look). PNG only unless asked. **Rotation check:**
gpt-image-2 occasionally returns an edit rotated 90° — if sky/ceiling isn't up,
rotate it back with `sips -r 90` or `sips -r 270` (whichever lands it upright,
free, no regen) and re-view. Stills only.

## Tips & failure modes

| Symptom | Fix |
|---|---|
| Output rotated 90° | Rotate back `sips -r 90` / `sips -r 270` — whichever lands upright (free, no regen). |
| Person got blockified | Re-assert the KEEP clause; for groups name every person. |
| World barely voxelized | You're on nano-banana-pro — switch to gpt-image-2. |
| Person looks pasted | Make sure the COLOR GRADING block + mood line are present — that's the unifier. |
| Wrong things voxelized | Re-check Step 0 — you picked the wrong mode. object-only = just the featured object; background-only = just the scene; object+background = everything but the person. |
| Object voxelized in background-only | Widen the KEEP clause to name the held/foreground object explicitly. |
| Tags missing / wrong items (object-only) | You forgot the label clause, or didn't list the hero items by name. List each one. |
| Tags messy / overlapping / on the face | "keep labels non-overlapping, just above each item, never over a face"; re-roll. |
| Tags appeared but shouldn't have | You're in background-only (no tags) — drop the label clause. |
| Day-for-night flip | Name the night mood explicitly in COLOR GRADING. |
| Cropped vs source | Pass `aspect_ratio: "auto"` — the worker matches the reference's orientation. |
| Face drifted | Expected (maskless recipe). Advanced fix below. |

**Advanced — guaranteed identity (off-recipe).** `remove_background` (`mode="portrait"`)
on the source → use the alpha as the gpt-image-2 `mask` (transparent=repaint,
opaque=keep) so only the targeted region converts and the person's pixels are
never touched. Off the @rohxit7 path; use only when a face must be byte-perfect.

## Reference

- **Engine:** @rohxit7 viral recipe, verbatim. **object-only prompt + loot tags:**
  salvaged from @aibyjoe "Minecraft Food". This skill **absorbs and retires both
  minecraft-food (object-only) and minecraft-world (object+background)**.
- Verdict: gpt-image-2 always; one recipe, three input-driven modes.
