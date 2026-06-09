# Language Coverage Reference

Use this reference as the current worker-supported fast path.

## Purpose

Use this page only when language support is questioned, or when a language-related upstream error occurs during `/pika:language-swap`.

Do not proactively expose provider-specific language-list details in normal user replies. In ordinary success cases, keep the answer focused on the requested output video.

## Boundary

The `dub_video` worker owns a hardcoded, empirically verified allowlist. It is no longer a blind pass-through. Two routing paths:

- **ElevenLabs dubbing** handles **32 languages** — the codes ElevenLabs `eleven_dubbing` actually accepts through the worker path. A target outside this set (and outside the Minimax set below) is rejected **before billing** with the supported list.
- **Minimax branch (voice-cloned)** handles **8 languages ElevenLabs cannot dub**: Cantonese, Thai, Hebrew, Persian, Slovenian, Catalan, Norwegian Nynorsk, Afrikaans. For these the worker clones the source speaker's voice and synthesizes with Minimax. Trade-offs on this path: one cloned voice for the whole clip, and the original background-music bed is replaced by the dubbed speech.

**Mandarin gotcha:** ElevenLabs accepts only `zh`. The ISO-639-3 code `cmn` is rejected upstream; the worker auto-maps `cmn`/`zho`/`chi` to `zh`.

The upstream dubbing product docs also advertise 90+ languages for a newer product path while noting that the newer API is not live yet. Do not use that 90+ claim as a guarantee for the current MCP worker path unless the API contract changes.

Source note: the 32-language ElevenLabs set and the `cmn`-rejected behavior were verified empirically against the dubbing proxy. The 8-language Minimax set is Minimax Speech-02's `language_boost` coverage minus the ElevenLabs 32. Keep provider-specific names and links out of normal user-facing replies unless the user explicitly asks for the external source.

## Supported languages

### ElevenLabs dubbing — 32 languages (verified)

| Language | Code sent upstream |
| --- | --- |
| Arabic | `ara` |
| Bulgarian | `bul` |
| Croatian | `hrv` |
| Czech | `ces` |
| Danish | `dan` |
| Dutch | `nld` |
| English | `eng` |
| Filipino | `fil` |
| Finnish | `fin` |
| French | `fra` |
| German | `deu` |
| Greek | `ell` |
| Hindi | `hin` |
| Hungarian | `hun` |
| Indonesian | `ind` |
| Italian | `ita` |
| Japanese | `jpn` |
| Korean | `kor` |
| Malay | `msa` |
| Mandarin Chinese | `zh` (NOT `cmn`) |
| Norwegian (Bokmål) | `nor` |
| Polish | `pol` |
| Portuguese | `por` |
| Romanian | `ron` |
| Russian | `rus` |
| Slovak | `slk` |
| Spanish | `spa` |
| Swedish | `swe` |
| Tamil | `tam` |
| Turkish | `tur` |
| Ukrainian | `ukr` |
| Vietnamese | `vie` |

ISO-639-1 spellings (`es`, `fr`, `ja`, `pt-BR`, …) are accepted and forwarded; region subtags are tolerated and script subtags are dropped.

### Minimax voice-clone branch — 8 languages

These are NOT supported by ElevenLabs dubbing; the worker routes them to Minimax with a cloned source voice.

| Language | Accepted target codes |
| --- | --- |
| Cantonese | `yue`, `cantonese`, `zh-HK` |
| Thai | `tha`, `th` |
| Hebrew | `heb`, `he` |
| Persian (Farsi) | `fas`, `fa` |
| Slovenian | `slv`, `sl` |
| Catalan | `cat`, `ca` |
| Norwegian Nynorsk | `nno`, `nn` (Bokmål `no`/`nb` stays on ElevenLabs) |
| Afrikaans | `afr`, `af` |

## Not supported

Many languages that appear in ElevenLabs' general *speech-generation* help-center list (e.g. Welsh, Icelandic, Serbian, Swahili, Urdu, Lithuanian, Irish, and others) are **not** accepted by the dubbing API and are not in the Minimax set. A model-capability list is **not** a dubbing allowlist — passing such a code now fails fast with the supported list rather than erroring opaquely mid-pipeline.

## Agent Guidance

When the user asks "how many languages does Language Swap support?", answer carefully:

- The fast-path dub supports **40 languages total**: 32 via ElevenLabs + 8 via the Minimax voice-clone branch.
- The two paths are an implementation detail — do not surface provider names in normal replies. If a requested language is unsupported, state that plainly and, when helpful, point to the closest supported option.
- For the newer 90+ language product claim: mention it only with the API-not-live caveat from the upstream dubbing overview.
