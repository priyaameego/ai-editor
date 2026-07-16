---
name: higgsfield-prompts-only
description: |
  Write Higgsfield-ready image, video, product, and ad prompts WITHOUT generating
  media or calling the higgsfield CLI. Use when the user wants "prompts only",
  "just the prompt", "don't generate", "no API", or to draft copy before spending
  credits. Covers generic generation, Marketing Studio UGC/TV spots, product
  photoshoot modes, and marketplace cards. Delivers paste-ready prompts plus
  recommended model/mode/flags. Do NOT run Bash or higgsfield commands unless
  the user explicitly asks to generate, submit, or run the CLI.
---

# Higgsfield — Prompts Only

**Default mode: write prompts, do not generate.**

Never run `higgsfield` CLI, never submit jobs, never spend credits unless the user clearly says to **generate**, **submit**, **run**, or **create the image/video**.

## What to deliver

For each request, output:

1. **Intent summary** — one line (image / video / product photo / ad)
2. **Recommended route** — model or mode slug (e.g. `seedance_2_0`, `product_shot`, `ugc`)
3. **Final prompt(s)** — paste-ready, under ~200 tokens each
4. **Suggested flags** — `aspect_ratio`, `duration`, `resolution`, `--mode`, etc.
5. **Optional CLI** — one copy-paste command block labeled **"Only run if you want to generate"**

Use the user's language for explanations; keep technical slugs in English.

## Prompt craft (from Higgsfield prompt engineering)

- **Structure:** subject + setting + style + lighting + camera
- **Concrete & sensory:** "golden-hour rim light on wet asphalt" not "nice lighting"
- **Camera:** lens (35mm, 85mm), angle, motion (dolly in, tracking shot, slow push)
- **Length:** keep under ~200 tokens; long prompts distort
- **Positive phrasing:** "tack sharp" not "no blur"; "uninhabited landscape" not "no people"

### Image-to-image / start-frame video

- **Img2img:** describe *changes*, not the whole scene  
  Good: "transform into anime style, vibrant cel shading"  
  Bad: re-describing the uploaded photo
- **Image-to-video:** `--start-image` holds the first frame; prompt = *motion only*  
  "camera dollies in", "smoke rises slowly", "the dancer spins"

### Aspect ratios

| Ratio | Use |
|-------|-----|
| `16:9` | Landscape, cinematic |
| `9:16` | Vertical, Reels/TikTok/Shorts |
| `1:1` | Square, profile |
| `2:3` | Pinterest pins |
| `4:5` | Instagram feed |

## Route by task

| User wants | Mode / model | Prompt style |
|------------|--------------|--------------|
| General image | `gpt_image_2` | Full scene description |
| Character / stylized | `nano_banana_2` | Character + pose + style |
| Cinematic still | `text2image_soul_v2` | Film still, lens, grade |
| General video | `seedance_2_0` | Motion + camera; 4–15s |
| Cheap video | `kling3_0` | Simple single-shot motion |
| UGC / ad video | `marketing_studio_video` + `--mode ugc` | Presenter action + product beat |
| Product on white | `product_shot` (photoshoot) | Short *intent* for backend enhancer |
| Lifestyle product | `lifestyle_scene` | Environment + use context |
| Pinterest pin | `moodboard_pin` | Vertical aesthetic, mood |
| Hero banner | `hero_banner` | Wide campaign header intent |

For **product-photoshoot** and **marketplace-cards**: write a **short user-intent string** (what the backend enhancer expects), not a fully hand-built GPT Image prompt. Example: `"cold-brew bottle on sunlit kitchen counter, IG feed, cozy morning"`.

## Marketing Studio video modes

| `--mode` | Best for |
|----------|----------|
| `ugc` | Casual phone-style presenter (default) |
| `ugc_how_to` | Tutorial / explainer |
| `ugc_unboxing` | Unboxing reveal |
| `product_showcase` | Clean product highlight |
| `product_review` | Presenter opinion |
| `tv_spot` | Broadcast commercial |
| `ugc_virtual_try_on` | Try-on, organic feel |
| `virtual_try_on` | Try-on, polished |

Video prompt template:

```
[Presenter action]. [Product moment]. [Environment]. [Camera: handheld / static / slow push].
[Lighting]. [Tone: authentic UGC / polished / broadcast].
Duration: Ns. Aspect: 9:16.
```

## Product photoshoot interview (prompts-only)

If details are missing, ask up to **3 short labeled questions** (never open-ended), then write the `--prompt` string from answers:

1. Count? `[1 / 3 / 5]`
2. Style? `[Clean studio / Lifestyle / Conceptual / With model]`
3. Use? `[Shopify / Instagram / Pinterest / Paid ads / Website hero]`

## Safety (avoid rejected prompts)

No real public figures, sexual content, or trademarked characters/brands unless user owns the brand.

## References

When you need deeper mode/model tables, read sibling skills (if installed):

- `higgsfield-generate/references/prompt-engineering.md`
- `higgsfield-generate/references/marketing-modes.md`
- `higgsfield-generate/references/model-catalog.md`
- `higgsfield-product-photoshoot/SKILL.md`

## Example output

**User:** "UGC unboxing prompt for a skincare serum, vertical, 12 seconds"

**You return:**

- **Route:** `marketing_studio_video` · `--mode ugc_unboxing` · `9:16` · `12s`
- **Prompt:** "Creator lifts package toward camera, genuine surprise smile, peels outer sleeve to reveal serum bottle on bathroom counter, soft window light, handheld iPhone feel, quick rack focus to product label, warm authentic tone."
- **Optional CLI (generate only if asked):**
  ```bash
  higgsfield generate create marketing_studio_video --mode ugc_unboxing --prompt "..." --aspect_ratio 9:16 --duration 12 --wait
  ```
