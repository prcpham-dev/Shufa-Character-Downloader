import os
import asyncio
from src.processHelpers.scrape import searchImg
from src.processHelpers.download import downloadImg


async def search_wrapper(character, author, character_type_value, 
                         wait_time, headless, count, semaphore):
    """
    Run searchImg.
    """
    print(f"📝 Working on {character} ...")
    async with semaphore:
        return await asyncio.to_thread(
            searchImg, author, character, character_type_value, 
            wait_time, headless, count
        )

async def download_images(character_index, char_only, found):
    """
    Download all images found for a character.
    - Saves into images/{character_index}/
    - Filenames: {index:02d}_{character}_{author}_{main|other}.jpg
    """
    if not found:
        print(f"❌ No images for {character_index}")
        return

    out_dir = os.path.join("images", character_index)
    os.makedirs(out_dir, exist_ok=True)

    download_tasks = []
    for idx, (img_url, author_name, is_match) in enumerate(found, start=1):
        if not img_url:
            continue

        save_author = (author_name or "Unknown").replace("/", "_")
        tag = "main" if is_match else "other"
        out_file = os.path.join(out_dir, f"{idx:02d}_{char_only}_{save_author}_{tag}.jpg")

        download_tasks.append(downloadImg(img_url, out_file))

    if download_tasks:
        await asyncio.gather(*download_tasks)


async def process_character(character_index, author, character_type_value, 
                            semaphore, wait_time, headless, count):
    """
    Run search and download for a single character.
    """
    char_only = character_index.split("_", 1)[-1]
    found = await search_wrapper(
        char_only, author, character_type_value, wait_time, 
        headless, count, semaphore
    )
    await download_images(character_index, char_only, found)


async def run(author, character_type_value, characters, batch_size=4, 
              wait_time=15, count=5, headless=True, cancel_event=None):
    """
    Main async function to process all characters with limited concurrency.
    """
    semaphore = asyncio.Semaphore(batch_size)
    running = []
    char_iter = iter(characters)

    # Start initial batch
    for _ in range(min(batch_size, len(characters))):
        character_index = next(char_iter)
        task = asyncio.create_task(
            process_character(
                character_index, author, character_type_value, 
                semaphore, wait_time, headless, count
            )
        )
        running.append((character_index, task))

    # Handle tasks dynamically
    while running:
        if cancel_event and cancel_event.is_set():
            print("⏹️ Cancel requested. Stopping tasks...")
            break

        done, _ = await asyncio.wait([t for _, t in running], return_when=asyncio.FIRST_COMPLETED)
        finished = []

        for character_index, task in running:
            if task in done:
                finished.append((character_index, task))

        # Remove finished tasks
        for item in finished:
            running.remove(item)

        # Add next ones
        try:
            while len(running) < batch_size:
                if cancel_event and cancel_event.is_set():
                    print("⏹️ Cancel requested. Stopping batch...")
                    break
                character_index = next(char_iter)
                task = asyncio.create_task(
                    process_character(
                        character_index, author, character_type_value, 
                        semaphore, wait_time, headless, count
                    )
                )
                running.append((character_index, task))
        except StopIteration:
            pass

    print("Finish:")


def run_main(author, character_type_value, characters, wait_time=15, 
             batch_size=4, count=5, headless=True, cancel_event=None):
    asyncio.run(
        run(
            author=author,
            character_type_value=character_type_value,
            characters=characters,
            wait_time=wait_time,
            batch_size=batch_size,
            count=count,
            headless=headless,
            cancel_event=cancel_event,
        )
    )


if __name__ == "__main__":
    run_main(
        author="王羲之",
        character_type_value="8",
        batch_size=2,
        count=3,
        wait_time=15,
        characters=["01_马", "02_秋", "03_饮"],
        headless=False,
    )
