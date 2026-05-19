from playwright.sync_api import sync_playwright
from typing import List, Dict
from datetime import datetime


def scrape_twitch_data() -> List[Dict]:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)...")
        print("Opening Twitch Page...")
        try:
            # u can change page goto depend website u wnat to scrape
            page.goto("https://www.twitch.tv/directory/category/just-chatting", timeout=60000, wait_until="domcontentloaded")
        except Exception as e:
            print(f"Failed opening page: {e}")
            browser.close()
            return []
   
        page.wait_for_selector("main")
        last_count = 0
        max_scroll = 40
        for i in range(max_scroll):
            cards = page.query_selector_all("div[data-a-target='directory-container']")
            current_count = len(cards)
            print(f"Scroll to-{i+1}, find {current_count} card")

            if current_count == last_count:
                break

            last_count = current_count
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(15000)
            
        page.wait_for_timeout(50000)

        # take asll the car viewr and global count
        cards = page.query_selector_all("a[data-a-target='preview-card-channel-link']")
        viewer_els = page.query_selector_all("div[class='ScMediaCardStatWrapper-sc-anph5i-0 kMBPhM tw-media-card-stat']")
        viewer_texts = [el.inner_text().strip() for el in viewer_els]
        
        results = []
        for i, card in enumerate(cards):
            try:
                title_el = card.query_selector("h4")
                username_el = card.query_selector("p[title]")
        
                title = title_el.inner_text().strip() if title_el else "-"
                username = username_el.inner_text().strip() if username_el else "-"
                viewers = viewer_texts[i] if i < len(viewer_texts) else "-"
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                result = {
                    "title": title,
                    "username": username,
                    "viewers": viewers,
                    "timestamp": timestamp
                }

                results.append(result)

            except Exception as e:
                print(f"Error card {i+1}: {e}")
                continue

        browser.close()
        print(f"\n Total data we get: {len(results)}")
        return results

