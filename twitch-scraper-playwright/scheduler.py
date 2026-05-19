import schedule
import time
from main import main


def run_scheduler():
    # Schedule scraping every 15 minutes
    schedule.every(15).minutes.do(main)
    
    print("Scheduler is active. Scraping runs every 15 minutes.")
    
    while True:
        schedule.run_pending()
        time.sleep(1)
        
if __name__ == "__main__":
    run_scheduler()