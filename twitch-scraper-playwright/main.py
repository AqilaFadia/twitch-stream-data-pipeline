from scraper.twitch_scraper import scrape_twitch_data
from utils.save_to_sheet import save_data_to_sheet
from utils.clean_data import clean_scraped_data  

def main():
    print("Scraping data from Twitch...")
    data = scrape_twitch_data()
    print(f"count data after scraping..: {len(data)}")

    print("Membersihkan data...")
    cleaned_data = clean_scraped_data(data)
    print(f"count data after cleaning..: {len(cleaned_data)}")

    print("Saving data to google sheet...")
    save_data_to_sheet(cleaned_data)
    print("Finished")

if __name__ == "__main__":
    main()
