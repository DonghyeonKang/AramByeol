import schedule
import time
from datetime import datetime
import subprocess
import logging
import os

# 로그 디렉토리 생성
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'scraper.log')),
        logging.StreamHandler()
    ]
)

def run_scraper():
    try:
        logging.info("Starting menu scraping job")
        result = subprocess.run(['python', 'scraper.py'], 
                              check=True,
                              capture_output=True,
                              text=True)
        logging.info("Scraper output:")
        logging.info(result.stdout)
        if result.stderr:
            logging.warning("Scraper stderr:")
            logging.warning(result.stderr)
        logging.info("Menu scraping completed successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running scraper: {e}")
        if e.stdout:
            logging.error(f"Scraper output: {e.stdout}")
        if e.stderr:
            logging.error(f"Scraper error: {e.stderr}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def main():
    # 스케줄러 시작시 즉시 1회 실행
    current_time = datetime.now().strftime("%H:%M")
    logging.info(f"Scheduler started at {current_time}. Running initial scraping...")
    run_scraper()
    
    # 스케줄러 설정 - 매일 01:00에 실행
    schedule.every().day.at("01:00").do(run_scraper)
    logging.info("Scheduled to run scraper daily at 01:00")
    
    # 스케줄러 실행
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1분마다 체크

if __name__ == "__main__":
    main() 