# crisp-social

Public media for Crisp Advisors LLP's Instagram and LinkedIn posts. Buffer pulls each
reel/graphic from its raw GitHub URL, so everything in `media/` is public once pushed.

- `media/<yyyy-mm-topic>/` — final reels and graphics, one folder per post
- `brand/` — logo without the two dots (slate for light backgrounds, white for dark)
- `toolkit/` — the reel-making setup: GSAP HTML template, Playwright renderer
  (1080x1920, 30 fps, 2-subframe motion blur), grain texture, example MIDI music bed
  (render with FluidR3_GM via fluidsynth). Voiceover: ElevenLabs (Starter plan), voice
  "Lyan – Female Genuine Casual Ads".

Do not put client data or anything unpublished-and-sensitive here: the repo is public.
