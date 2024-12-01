from flask import Flask, jsonify, request
from playwright.async_api import async_playwright
from concurrent.futures import ThreadPoolExecutor
import asyncio

app = Flask(__name__)

executor = ThreadPoolExecutor()  # ThreadPoolExecutor for running threads

async def scrape_audio_for_pages(pages_to_scrape):
    """Scrape audio files from multiple pages using Playwright."""
    all_audio_files = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        for url in pages_to_scrape:
            await page.goto(url)
            audio_elements = await page.query_selector_all('audio.wp-audio-shortcode')

            for audio in audio_elements:
                audio_src = await audio.get_attribute('src')
                if audio_src and ".mp3" in audio_src:
                    audio_url = audio_src if audio_src.startswith('http') else f'https://carlislechurch.org{audio_src}'
                    all_audio_files.append(audio_url)

        await browser.close()

    return all_audio_files

async def scrape_audio(num_pages):
    """Scrape audio files across multiple pages."""
    urls = [f"https://carlislechurch.org/sermons/page/{i}/" for i in range(1, num_pages + 1)]

    # Divide the URLs into chunks for threading
    chunk_size = 5  # Number of URLs per thread
    chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

    loop = asyncio.get_event_loop()
    tasks = [
        loop.run_in_executor(executor, asyncio.run, scrape_audio_for_pages(chunk))
        for chunk in chunks
    ]

    results = await asyncio.gather(*tasks)
    all_audio_files = [url for result in results for url in result]  # Flatten the results
    return all_audio_files

@app.route('/scrape-audio', methods=['GET'])
async def scrape_audio_endpoint():
    """API endpoint to scrape audio files."""
    num_pages = request.args.get("pages", default=1, type=int)
    audio_files = await scrape_audio(num_pages)
    return jsonify({"audio_files": audio_files})

if __name__ == '__main__':
    app.run(debug=True)
