#!/usr/bin/env python3
"""Live-site smoke test for Mikan's Corner (GitHub Pages).
Run: uv run --with playwright python tests/live_smoke.py
"""
import asyncio, sys
from playwright.async_api import async_playwright

BASE = "https://maebahesioru.github.io/mikans-corner/"

async def main():
    checks = []
    def check(name, ok, detail=""):
        checks.append((name, bool(ok), detail))
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width":1100,"height":900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type=="error" else None)
        for path in ["", "gallery.html", "about.html"]:
            await page.goto(BASE + path, wait_until="networkidle")
            await page.wait_for_timeout(600)
            check(f"live {path or 'index'}: no JS errors", not errors, "; ".join(errors[:3]))
            check(f"live {path or 'index'}: theme toggle present", await page.locator(".theme-toggle").count() == 1)
        # theme toggle on live
        await page.goto(BASE, wait_until="networkidle")
        t0 = await page.evaluate("document.documentElement.dataset.theme")
        await page.click(".theme-toggle")
        t1 = await page.evaluate("document.documentElement.dataset.theme")
        check("live: theme toggle flips", t0 != t1, f"{t0}->{t1}")
        # feed button on live
        before = await page.text_content("#treats")
        await page.click("#feed")
        await page.wait_for_timeout(300)
        after = await page.text_content("#treats")
        check("live: feed works", before != after, f"{before!r}->{after!r}")
        # aria-current check
        await page.goto(BASE + "gallery.html", wait_until="networkidle")
        cur = await page.get_attribute('nav a.active', 'aria-current')
        check("live: aria-current on active nav", cur == "page", str(cur))
        await b.close()
    passed = sum(1 for _,ok,_ in checks if ok)
    for name, ok, detail in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if not ok and detail else ""))
    print(f"\n{passed}/{len(checks)} live checks passed")
    sys.exit(0 if passed == len(checks) else 1)

asyncio.run(main())
