import asyncio, pathlib
from playwright.async_api import async_playwright
HERE = pathlib.Path("/home/maebahesioru/ダウンロード/sushi_money_research/実行/240_hackclub/bento/mikans-corner")
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":375,"height":812}, device_scale_factor=2)
        for name in ["index.html","gallery.html","about.html"]:
            await pg.goto((HERE/name).as_uri())
            await pg.wait_for_timeout(600)
            overflow = await pg.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
            sw = await pg.evaluate("document.documentElement.scrollWidth")
            print(name, "h-overflow:", overflow, "scrollWidth:", sw)
            await pg.screenshot(path=f"/tmp/mobile_{name.replace('.html','')}.png")
        await b.close()
asyncio.run(main())
