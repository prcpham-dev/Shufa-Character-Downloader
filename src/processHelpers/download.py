import aiohttp
import asyncio

async def downloadImg(src, out_file):
    """ 
    Downloads an image from the given URL and saves it to the specified file.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(src) as resp:
            resp.raise_for_status()
            with open(out_file, "wb") as f:
                f.write(await resp.read())
    print(f"✅ Saved {out_file}")
    return out_file

if __name__ == "__main__":
    src = "https://ios.shufazidian.com/gq/1/8/43957.jpg"
    out_file = "images/example/example.jpg"
    asyncio.run(downloadImg(src, out_file))