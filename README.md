# Mikan's Corner 🍊

A tiny three-page website for Mikan, a pixel cat drawn entirely with canvas
`fillRect`s. Made for [Hack Club Bento](https://bento.hackclub.com/).

Live: https://maebahesioru.github.io/mikans-corner/

## The three pages

1. **index.html — the Lid (welcome page)**: Mikan greets you; click her (or
   press Enter) and she blushes with floating hearts. You can also give her a
   mikan — the snack counter is remembered in localStorage.
2. **gallery.html — divider 1**: six moments from her day (morning stretch,
   zoomies, nap, star hunting, snack time, being petted) — all procedural art.
   Every card is interactive: tap one and she reacts.
3. **about.html — divider 2**: her lore, a timeline, and a small FAQ.

The **Chopsticks** are the sticky nav bar on every page connecting all three.

## How it's built

- HTML + one shared `style.css` + two shared scripts (`cat.js` = the cat
  renderer, `theme.js` = theme + animation helpers)
- No images, no frameworks, no build step — open `index.html` and that's it
- The cat has poses (`sit` / `sleep` / `walk`), accessories (hearts, star,
  a mandarin), a wagging tail and click-to-blush interactions
- **Theme toggle**: ☀️/🌙 button, remembers your choice, follows your system
  preference on first visit
- **A11y**: skip link, keyboard-operable cat and cards, `prefers-reduced-motion`
  support, focus rings
- **Battery friendly**: the idle animation pauses while the tab is hidden

## Run locally

```bash
python3 -m http.server 3842
# open http://127.0.0.1:3842/
```

## Deploy

Hosted on GitHub Pages — the site IS the repo (no build step).
