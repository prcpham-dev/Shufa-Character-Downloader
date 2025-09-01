import asyncio
from read import readFile
from download import downloadImg

async def main():
    shufas = readFile()
    author = shufas[0]
    chars = shufas[1:]

    batch_size = 4
    results = []

    # Do 4 at a time
    for i in range(0, len(chars), batch_size):
        batch = chars[i:i+batch_size]
        tasks = [downloadImg(author, w) for w in batch]
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)

    print("Finish:", results)


if __name__ == "__main__":
    asyncio.run(main())
