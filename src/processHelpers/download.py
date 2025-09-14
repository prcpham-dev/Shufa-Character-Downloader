import aiohttp
import asyncio

async def fetchImg(session, src, out_file):
    async with session.get(src) as resp:
        resp.raise_for_status()
        with open(out_file, "wb") as f:
            f.write(await resp.read())
    print(f"✅ Saved {out_file}")

async def downloadImg(src, out_file):
    async with aiohttp.ClientSession() as session:
        await fetchImg(session, src, out_file)
    return out_file

if __name__ == "__main__":
    # Example usage
    src = "https://ios.shufazidian.com/gq/1/8/43957.jpg"
    out_file = "images/example/example.jpg"
    asyncio.run(downloadImg(src, out_file))