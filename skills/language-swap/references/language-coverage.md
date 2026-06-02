# Language Coverage Reference

Last verified: 2026-06-02 PST

## Purpose

Use this page only when language support is questioned, or when a language-related upstream error occurs during `/pika:language-swap`.

Do not proactively expose provider-specific language-list details in normal user replies. In ordinary success cases, keep the answer focused on the requested output video.

## Boundary

The fast-path dub accepts a target language from the user and forwards it upstream as a language code. The worker does not own a hardcoded allowlist.

The current upstream dubbing API reference documents `target_lang` and `source_lang` as valid `iso639-1` or `iso639-3` language codes, but does not publish a complete enum of accepted dubbing languages.

The language list below is a model-capability reference for speech generation / fallback behavior. It is not a guaranteed dubbing API allowlist.

The upstream dubbing product docs also advertise 90+ languages for a newer product path while noting that the newer API is not live yet. Do not use that 90+ claim as a guarantee for the current MCP worker path unless the API contract changes.

Source note: verified from upstream help center language-support docs and upstream dubbing API/product docs on the date above. Keep provider-specific names and links out of normal user-facing replies unless the user explicitly asks for the external source.

## 74-Language Model Reference

The Help Center lists 74 languages:

| Language | ISO-639 code shown by the source |
| --- | --- |
| Afrikaans | `afr` |
| Arabic | `ara` |
| Armenian | `hye` |
| Assamese | `asm` |
| Azerbaijani | `aze` |
| Belarusian | `bel` |
| Bengali | `ben` |
| Bosnian | `bos` |
| Bulgarian | `bul` |
| Catalan | `cat` |
| Cebuano | `ceb` |
| Chichewa | `nya` |
| Croatian | `hrv` |
| Czech | `ces` |
| Danish | `dan` |
| Dutch | `nld` |
| English | `eng` |
| Estonian | `est` |
| Filipino | `fil` |
| Finnish | `fin` |
| French | `fra` |
| Galician | `glg` |
| Georgian | `kat` |
| German | `deu` |
| Greek | `ell` |
| Gujarati | `guj` |
| Hausa | `hau` |
| Hebrew | `heb` |
| Hindi | `hin` |
| Hungarian | `hun` |
| Icelandic | `isl` |
| Indonesian | `ind` |
| Irish | `gle` |
| Italian | `ita` |
| Japanese | `jpn` |
| Javanese | `jav` |
| Kannada | `kan` |
| Kazakh | `kaz` |
| Kirghiz | `kir` |
| Korean | `kor` |
| Latvian | `lav` |
| Lingala | `lin` |
| Lithuanian | `lit` |
| Luxembourgish | `ltz` |
| Macedonian | `mkd` |
| Malay | `msa` |
| Malayalam | `mal` |
| Mandarin Chinese | `cmn` |
| Marathi | `mar` |
| Nepali | `nep` |
| Norwegian | `nor` |
| Pashto | `pus` |
| Persian | `fas` |
| Polish | `pol` |
| Portuguese | `por` |
| Punjabi | `pan` |
| Romanian | `ron` |
| Russian | `rus` |
| Serbian | `srp` |
| Sindhi | `snd` |
| Slovak | `slk` |
| Slovenian | `slv` |
| Somali | `som` |
| Spanish | `spa` |
| Swahili | `swa` |
| Swedish | `swe` |
| Tamil | `tam` |
| Telugu | `tel` |
| Thai | `tha` |
| Turkish | `tur` |
| Ukrainian | `ukr` |
| Urdu | `urd` |
| Vietnamese | `vie` |
| Welsh | `cym` |

## Agent Guidance

When the user asks "how many languages does Language Swap support?", answer carefully:

- For the current fast-path dub worker: upstream is the source of truth; the MCP worker accepts ISO-style `target_language` values and forwards them as `target_lang`.
- For a named reference list: cite the 74-language list above, and explicitly say it is not a published dubbing API enum.
- For the newer 90+ language product claim: mention it only with the API-not-live caveat from the upstream dubbing overview.
