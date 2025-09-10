import os,asyncio
from src.scrape import searchImg
from src.download import downloadImg

async def run(author, character_type_value, characters, batch_size=4, wait_time=15, count=5, headless=True):
    """
    Search and download images for each character.
    - Saves into images/{character}/
    - Filenames: {character}_{author}_{main|other}_{index:03d}.jpg
    """
    for i in range(0, len(characters), batch_size):
        batch = characters[i:i + batch_size]

        search_tasks = []
        for character in batch:
            print(f"📝 Working on {character} ...")
            search_tasks.append(
                asyncio.to_thread(
                    searchImg, author, character, character_type_value, wait_time, headless, count
                )
            )

        search_results = await asyncio.gather(*search_tasks)

        download_tasks = []
        for character, found in zip(batch, search_results):
            if not found:
                print(f"❌ No images for {character}")
                continue

            out_dir = os.path.join("images", character)
            os.makedirs(out_dir, exist_ok=True)

            for idx, (img_url, author_name, is_match) in enumerate(found, start=1):
                if not img_url:
                    continue
                save_author = (author_name or "Unknown").replace("/", "_")
                tag = "main" if is_match else "other"
                out_file = os.path.join(out_dir, f"{idx:02d}:{character}_{save_author}_{tag}.jpg")
                download_tasks.append(downloadImg(img_url, out_file))

        if download_tasks:
            await asyncio.gather(*download_tasks)

    print("Finish:")

def run_main(author, character_type_value, characters, wait_time=15, batch_size=4, count=5, headless=True):
    asyncio.run(
        run(
            author=author, character_type_value=character_type_value,
            characters=characters, wait_time=wait_time,
            batch_size=batch_size, count=count, headless=headless
        )
    )

if __name__ == "__main__":
    run_main(
        author="王羲之", character_type_value="1",
        characters=["饮", "马", "渡", "秋", "水"],
        headless=False
    )
