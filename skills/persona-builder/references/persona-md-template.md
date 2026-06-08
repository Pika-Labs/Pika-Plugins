# persona.md template — influencer-identity

This is the canonical structure for the `persona.md` file the skill ships. It's the contract that downstream Pika skills (ugc-ads, podcast, founder-product-video, app-sizzle, app-store-screens) read.

**Naming:** this file is `persona.md`, not `brand.md`. The earlier version of this skill called it brand.md; that name has been retired because "brand" implied a product and the file is about a person. Do not regenerate as brand.md.

Fill every section with real content. No `[BRACKETS]` placeholders in the shipped file.

---

```markdown
# [@handle or display name] — Influencer Persona

## Quick reference
- **Handle:** [@[verified handle] OR "No public handle yet"]
- **Niche / lane:** [3–6 words — what they're known for]
- **Voice in 3 words:** [adj], [adj], [adj]
- **Aesthetic in 3 words:** [adj], [adj], [adj]
- **Typography:** [fontDisplay] + [fontBody] — e.g. "Cormorant Garamond + Inter"
- **Authenticity dial:** [real self / lightly amplified / different persona]
  - **What's amplified or different:** [one sentence — e.g. "real me with the volume on directness turned up" or "a calmer, more curated version of how I actually live"]
- **Current follower tier:** [scraped or user-provided value OR "unknown / pre-launch"] — never invent counts
- **90-day growth target:** [user-provided or explicitly heuristic target OR "not set"] — never invent counts

---

## The real you
[2–3 paragraphs. Specific. References actual stuff the user shared — their comfort show, their high-school self, the way they describe their friends, the thing they got excited about in the questions. Sounds like someone who paid attention.]

## Your influencer persona
[2–3 paragraphs about the online projection. States the authenticity dial out loud:
"You're not pretending to be someone else — you're you with the volume on [dimension] turned up,"
or "This is a character. Here's where the character starts and the real you ends."
Be specific about what's amplified, what's filtered, and why.]

---

## Strategic direction
**Chosen path:** [niche label — specific, e.g. "Boston-local lifestyle creator" not "lifestyle"]

**Why this fits the inputs:** [point to the specific posts / photos / things the user said that support this direction]

**Monetization profile:**
- Typical CPM range: [source-verified value OR broad heuristic estimate, labeled as such]
- Brand-deal floor by tier: [source-verified value OR broad heuristic estimate, labeled as such]
- Affiliate/LTK realism: [e.g. "LTK works at 5K+ in fashion; below that the click-through rates don't justify the time"]
- Sponsored-post realism: [e.g. "expect 2–4 paid collabs per quarter at 5K, scaling to monthly at 15K"]

**Monetization source note:** [list sources checked during this run OR state "broad heuristic estimate; no live monetization source verified"]

**Content load this path requires:**
- Posting cadence: [e.g. "4–5 posts/week, 1 reel/week"]
- Production tier: [phone-OK / mirrorless-needed / pro editing required]
- Recurring formats audiences expect: [e.g. "OOTD posts + GRWM reels + monthly local-roundup carousel"]

**Who's already winning at your size:**

Use the verified-live path only if each handle/count was checked during this run via `mcp__plugin_pika_pika__scrape_social` or another live supported source:
- **@[verified handle]** ([verified follower tier/count]) — [one sentence on what makes them work]
- **@[verified handle]** ([verified follower tier/count]) — [one sentence]
- **@[verified handle]** ([verified follower tier/count]) — [one sentence]

If live verification is unavailable, use clearly labeled archetypes instead and omit handles/counts:
- **[Archetype label]** — [one sentence on what makes this archetype work]
- **[Archetype label]** — [one sentence]
- **[Archetype label]** — [one sentence]

---

## Gap analysis (current → target)

**Content categories missing:** [name the buckets they don't currently post in that the chosen niche requires]
**Format gap:** [e.g. "you post static only; the niche expects reels at 3–5× the CPM of static"]
**Cadence gap:** [current posts/week → required posts/week]
**Voice gap:** [specific phrases to drop + phrases to add]
**Aesthetic gap:** [what visual register shift the persona requires]
**Follower-tier gap:** [where they are now → where paid work starts → realistic 90-day target]

---

## Content critique + gear recs

**Lighting:** [specific photos that work + specific ones that don't, with WHY]
**Framing & composition:** [phone position, common framing mistakes, what to actually do]
**Color & post-processing:** [presets they should use, color register issues]
**Consistency:** [where the grid feels like one person + where it breaks]
**Selfie technique:** [phone position, mirror cleanliness, OOTD selfie best practices]

**Gear recommendations (scaled to current tier):**
- Starter tier: [specific items with brand + price + where to buy]
- Intermediate tier: [if and when they should upgrade]
- Advanced tier: [only if relevant — e.g. for 10K+]

---

## Voice
**Sounds like:**
> [example sentence 1]
> [example sentence 2]
> [example sentence 3]

**Never sounds like:**
> [cringe sentence 1]
> [cringe sentence 2]
> [cringe sentence 3]

**Voice adjectives:** [adj], [adj], [adj]
**Forbidden words/phrases:** [list 3–6 actual phrases]

## Bios
1. **IG bio:** [bio v1]
2. **TikTok bio:** [bio v2]
3. **Long-form / serious platform bio:** [bio v3]

## Caption modes
**Hook:**
- **Use when:** [context label — e.g. scroll-stopper outfit / quick opinion / cold open]
- **Sample 1:** [3–4 lines]
- **Sample 2:** [shorter or longer contrast sample]

**Story:**
- **Use when:** [context label — e.g. day-in-life / recap / lesson learned]
- **Sample 1:** [5–8 lines]
- **Sample 2:** [shorter or longer contrast sample]

**Casual selfie:**
- **Use when:** [context label — e.g. mirror selfie / low-stakes update / outfit check]
- **Sample 1:** [1–2 lines]
- **Sample 2:** [shorter or longer contrast sample]

**Vulnerable:**
- **Use when:** [context label — e.g. honest reset / transition / quiet moment]
- **Sample 1:** [4–6 lines]
- **Sample 2:** [shorter or longer contrast sample]

**Promo:**
- **Use when:** [context label — e.g. brand fit / affiliate / product mention]
- **Sample 1:** [3–5 lines]
- **Sample 2:** [shorter or longer contrast sample]

## Hook openers (Story / Reel / TikTok)
1.
2.
3.
4.
5.

## DM + comment voice
- **Reply to a compliment:** [example]
- **Decline a brand pitch:** [example]
- **Reply to a hater (or "I don't reply" with reason):** [example]
- **Default emoji palette:** [emojis they actually use, or "no emojis"]

---

## Visual aesthetic
**Mood board:** see `mood-board.png`
**Palette:** [specific colors / named tones — e.g. "warm cream, cognac brown, dusty rose, deep navy"]
**Lighting:** [warm window / overcast / golden hour / harsh flash / candlelight — which dominates]
**Settings:** [where shots take place — be specific. "Brooklyn brownstones, marble-top coffee shops, kitchen counter at 10pm"]
**Photography style:** [phone-camera POV / mirror selfies (faceless or face) / 3/4 candids / overhead flatlay / etc. — which framings dominate]
**Subjects in frame:** [hands holding things / full body / faces / food / books / the dog / the bar / etc.]
**Forbidden visual elements:** [what would never appear in this feed]
**Typography — `fontDisplay`:** [e.g. "Cormorant Garamond"] — used on the mood board title and PDF page headings.
**Typography — `fontBody`:** [e.g. "Inter"] — used for subtitles, body, captions across the kit.
**Relationship to existing grid:** [whether the aesthetic matches their current grid or evolves it, and along which axis. Downstream skills use this to know whether to color-grade source photos.]

---

## Content categories (4)

For each category include image filename + headline + 1-line description + 3–4 example post types. These render as the 4-card grid on PDF page 4.

1. **[Category name]** — [image file] — [one-line description] — [3–4 example post types]
2. **[Category name]** — [image file] — [one-line description] — [3–4 example post types]
3. **[Category name]** — [image file] — [one-line description] — [3–4 example post types]
4. **[Category name]** — [image file] — [one-line description] — [3–4 example post types]

---

## Do & Don't (person-specific, not generic)
**DO:**
1.
2.
3.
4.
5.

**DON'T:**
1.
2.
3.
4.
5.

## Reference creators (with dimension + what to borrow)
- **[@handle or name]** — borrow their **[voice / content type / visual aesthetic]**. Specifically: [the actual thing — pacing, lighting, self-disclosure style, etc.]
- **[@handle or name]** — borrow their **[voice / content type / visual aesthetic]**. Specifically: [the actual thing]
- **[@handle or name]** — borrow their **[voice / content type / visual aesthetic]**. Specifically: [the actual thing]

---

## Key Next Steps (roadmap)

4–6 cards. Each is a shippable action with a specific number, brand, or behavior. This section is the canonical source — the same content renders on the final PDF page.

1. **[Section label, e.g. Lighting & Framing]** — [one-line headline] — [2–3 sentences of concrete action, with specific gear or behavior]
2. **[Section label, e.g. Content Mix]** — [one-line headline] — [concrete percentages or cadence target]
3. **[Section label, e.g. Voice Consistency]** — [one-line headline] — [specific phrases to use / drop]
4. **[Section label, e.g. Brand Pitches]** — [one-line headline] — [number of pitches by when, to whom]
5. **[Section label, e.g. Growth Goal]** — [one-line headline] — [specific follower target + horizon + the path]
6. **[Section label, e.g. The 30-Day Test]** — [one-line headline] — [the explicit re-audit trigger]

---

## How to use this kit with other Pika skills

| Skill | What to pull from this kit |
|---|---|
| **ugc-ads** | Voice: `voice-bank.md` hook captions + DO/DON'T. Likeness: pick one of the curated photos in `mood-board/curated/` as the lipsync reference. Aesthetic: mood adjectives + settings. |
| **podcast** | Voice principles + sample story captions for the spoken script. If generating an avatar for Host A, use a user-provided curated photo as that skill's runtime reference. |
| **founder-product-video** | Voice: vulnerable + promo caption modes for founder dialogue. Aesthetic: settings + lighting for the talking-head shots. Use a curated user photo only if that skill needs a founder likeness reference. |
| **app-sizzle** | Aesthetic adjectives + settings to guide product-demo backgrounds, title-card tone, and on-screen text register. |
| **app-store-screens** | Typography pair, palette, and visual aesthetic notes to keep screenshot campaigns aligned with the human creator identity. |
| **build-a-brand** | If the user also has a product brand, this file describes the human; build-a-brand's `brand.md` describes the product. The two should be cross-referenced but kept separate. |

**General usage:** paste this entire `persona.md` at the top of any Pika skill prompt to get on-brand output. The Quick reference block is the bare-minimum context; the full file is the rich context.

---

## File index (this kit)
- `persona.md` — this file
- `identity.md` — long-form "who you are" vs "who your influencer is" + strategic direction notes
- `voice-bank.md` — bios, captions, hooks, DMs, do/don't
- `next-steps.md` — Key Next Steps roadmap (standalone)
- `influencer-persona.pdf` — designed Influencer Persona PDF
- `mood-board.png` — composite visual board
- `mood-board/curated/` — tiles from your actual photos (color-graded for aesthetic cohesion if Step 2 named a shift from your existing grid)
- `mood-board/generated/` — tiles generated in the Step 2 aesthetic to fill coverage gaps
- `README.md` — kit usage guide
```

---

## Quality bars for the shipped persona.md

- **Every section filled with real content.** No `[BRACKETS]` left in.
- **Authenticity dial called out explicitly** in the quick reference + the "Your influencer persona" section. Hiding the dial breaks the contract for downstream skills.
- **Strategic direction has real numbers** — CPM ranges, brand-deal floors, posting cadence. Not adjective claims like "monetizable" without bones.
- **Gap analysis is specific** — name the missing content category, the missing format, the cadence delta. Vague gaps like "post more" are failures.
- **Content critique + gear recs name specific brands and price points.** "Buy a clip-on reflector" alone is too vague; "Lume Cube panel mini or the Pictar reflector clip, both ~$25 on Amazon" gives them something to click.
- **"Sounds like" and "Never sounds like"** are real sentences a real person would or wouldn't say, not adjective soup.
- **Forbidden words are actual phrases**, not categories. E.g. "elevated", "curated", "journey", "passion" — not "any corporate-sounding words."
- **Reference creators include BOTH the dimension AND the specific thing** — e.g. "borrow her *voice*: short declarative sentences, no qualifiers." Vague references like "feel like Emma Chamberlain" without naming the dimension (voice / content type / visual aesthetic) AND what specifically to borrow are a failure state.
- **Visual aesthetic section is renderable.** Step 3 has to build a mood board from it. Specific colors, lighting types, named settings, photography style — not adjective soup. "Warm and minimal" is not enough.
- **Content categories use the user's actual feed.** Derived from the scrape, not generic ("Outfits / Lifestyle / Food / Brand Partnerships"). Specific buckets like "Boston Lifestyle" or "Tour & Travel."
- **Key Next Steps cards are shippable actions** with specific numbers, brands, or behaviors. "Improve your content" is a failure; "Post 1 reel/week tied to a Boston seasonal moment" passes.
- **Do / Don't are person-specific.** "Do post the unflattering version too" beats "Do post consistently."
