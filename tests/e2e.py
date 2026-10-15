#!/usr/bin/env python3
"""Mikan's Corner v2 — E2E test (Playwright, headless Chromium).

Run:
  uv run --with playwright python tests/e2e.py

Covers all three pages: zero JS errors, cat renders (non-blank canvas),
click-to-pet, feed counter + localStorage persistence, theme toggle +
persistence, gallery card reactions, FAQ toggle, skip link, PNG pose
export (home / gallery / about).
Also writes a fresh screenshot to screenshot.png.
"""
import asyncio
import pathlib
import sys

from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["index.html", "gallery.html", "about.html"]

checks = []


def check(name, ok, detail=""):
    checks.append((name, bool(ok), detail))


async def canvas_nonblank(page, selector):
    return await page.evaluate(
        """(sel) => {
        const c = document.querySelector(sel);
        if (!c) return false;
        const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
        for (let i = 3; i < d.length; i += 4) if (d[i] > 0) return true;
        return false;
    }""",
        selector,
    )


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1100, "height": 900})
        page = await ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on(
            "console",
            lambda m: errors.append(f"console.{m.type}: {m.text}")
            if m.type == "error"
            else None,
        )

        base = (HERE / "index.html").as_uri()

        # --- all pages load with zero errors ---
        for name in PAGES:
            url = (HERE / name).as_uri()
            await page.goto(url)
            await page.wait_for_timeout(500)
            check(f"{name}: loads, no JS errors", not errors, "; ".join(errors[:3]))
            check(
                f"{name}: has theme toggle",
                await page.locator(".theme-toggle").count() == 1,
            )
            check(f"{name}: has skip link", await page.locator(".skip-link").count() == 1)

        # --- home page ---
        await page.goto(base)
        await page.wait_for_timeout(500)
        check("home: cat canvas drawn", await canvas_nonblank(page, "#cat"))

        # pet: click canvas -> busy reaction, then returns
        await page.click("#cat")
        await page.wait_for_timeout(150)
        check("home: canvas still drawn after pet", await canvas_nonblank(page, "#cat"))
        await page.wait_for_timeout(1100)

        # keyboard pet
        await page.focus("#cat")
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(200)
        check("home: keyboard pet works (no error)", not errors, "; ".join(errors[:3]))
        await page.wait_for_timeout(1000)

        # export the current pose as a PNG download
        async with page.expect_download() as dl_info:
            await page.click("#export")
        dl = await dl_info.value
        check(
            "home: PNG pose export downloads",
            (dl.suggested_filename or "").endswith(".png"),
            str(dl.suggested_filename),
        )

        # feed counter
        treats0 = await page.text_content("#treats")
        await page.click("#feed")
        await page.wait_for_timeout(200)
        treats1 = await page.text_content("#treats")
        check("home: feed increments", treats0 != treats1, f"{treats0!r} -> {treats1!r}")
        await page.wait_for_timeout(1400)
        stored = await page.evaluate("localStorage.getItem('mikan-treats')")
        check("home: treats stored", stored is not None, str(stored))

        # persistence across reload
        await page.reload()
        await page.wait_for_timeout(500)
        treats2 = await page.text_content("#treats")
        check("home: treats persist after reload", "1" in (treats2 or ""), str(treats2))

        # welcome-back counter (2nd visit in this context)
        wb = await page.text_content("#welcome-back")
        check("home: welcome-back appears on revisit", "visit #" in (wb or ""), str(wb))

        # theme toggle
        theme0 = await page.evaluate("document.documentElement.dataset.theme")
        await page.click(".theme-toggle")
        theme1 = await page.evaluate("document.documentElement.dataset.theme")
        check("theme: toggle flips", theme0 != theme1, f"{theme0} -> {theme1}")
        await page.reload()
        await page.wait_for_timeout(400)
        theme2 = await page.evaluate("document.documentElement.dataset.theme")
        check("theme: persists after reload", theme2 == theme1, f"{theme2} (want {theme1})")
        # toggle back to default for the screenshot
        await page.click(".theme-toggle")
        await page.wait_for_timeout(300)

        # --- gallery ---
        await page.goto((HERE / "gallery.html").as_uri())
        await page.wait_for_timeout(600)
        n_canv = await page.locator(".card canvas").count()
        check("gallery: 6 cards", n_canv == 6, str(n_canv))
        drawn = 0
        for i in range(n_canv):
            if await canvas_nonblank(page, f".card:nth-child({i+1}) canvas"):
                drawn += 1
        check("gallery: all canvases drawn", drawn == 6, f"{drawn}/6")
        # click a card -> reaction
        await page.click(".card:nth-child(2)")
        await page.wait_for_timeout(200)
        check("gallery: card reacts (no error)", not errors, "; ".join(errors[:3]))
        await page.wait_for_timeout(1300)

        # save a card pose as PNG (must not trigger the card reaction)
        async with page.expect_download() as dl_info:
            await page.click(".card:nth-child(3) .save-img")
        dl = await dl_info.value
        check(
            "gallery: card pose export downloads",
            (dl.suggested_filename or "").startswith("mikan-"),
            str(dl.suggested_filename),
        )

        # --- about ---
        await page.goto((HERE / "about.html").as_uri())
        await page.wait_for_timeout(500)
        check("about: cat drawn", await canvas_nonblank(page, "#cat"))
        n_faq = await page.locator(".faq details").count()
        check("about: FAQ present", n_faq >= 4, str(n_faq))
        await page.click(".faq details:first-of-type summary")
        await page.wait_for_timeout(200)
        open_state = await page.evaluate(
            "document.querySelector('.faq details').open"
        )
        check("about: FAQ toggles open", open_state is True, str(open_state))
        check("about: timeline present", await page.locator(".timeline li").count() >= 4)

        # export from the about page
        async with page.expect_download() as dl_info:
            await page.click("#export-about")
        dl = await dl_info.value
        check(
            "about: PNG export downloads",
            (dl.suggested_filename or "").endswith(".png"),
            str(dl.suggested_filename),
        )

        # --- screenshot (dark theme, home) ---
        await page.goto(base)
        await page.wait_for_timeout(700)
        await page.screenshot(path=str(HERE / "screenshot.png"), full_page=False)
        check("screenshot written", (HERE / "screenshot.png").exists())

        check("zero JS errors overall", not errors, "; ".join(errors[:5]))
        await browser.close()

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    for name, ok, detail in checks:
        mark = "PASS" if ok else "FAIL"
        line = f"[{mark}] {name}"
        if not ok and detail:
            line += f"  -- {detail}"
        print(line)
    print(f"\n{passed}/{total} checks passed")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    asyncio.run(main())
