# Mikan's Corner 🍊

A tiny three-page website for Mikan, a pixel cat drawn entirely with canvas
`fillRect`s. Made for [Hack Club Bento](https://bento.hackclub.com/).

## The three pages

1. **index.html — the Lid (welcome page)**: Mikan greets you; click her and she
   blushes with floating hearts.
2. **gallery.html — divider 1**: six moments from her day (morning stretch,
   zoomies, nap, star hunting, snack time, being petted) — all procedural art.
3. **about.html — divider 2**: her lore + this project's story.

The **Chopsticks** are the sticky nav bar on every page connecting all three.

## How it's built

- HTML + one shared `style.css` + one shared `cat.js` (the cat renderer)
- No images, no frameworks, no build step — open `index.html` and that's it
- The cat has poses (`sit` / `sleep` / `walk`), accessories (hearts, star,
  a mandarin), a wagging tail and a click-to-blush interaction

## Run locally

```bash
python3 -m http.server 3842
# open http://127.0.0.1:3842/
```

## Deploy

Hosted on GitHub Pages — the site IS the repo (no build step).
