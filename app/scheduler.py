from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from app.main import run_job
from app.utils import logger

def start_scheduler():
    scheduler = BlockingScheduler()
    
    ist = pytz.timezone('Asia/Kolkata')
    logger.info("Starting scheduler. News fetch job will run daily at 9:00 AM, 3:00 PM, and 9:00 PM IST.")
    
    # Run once immediately on startup
    try:
        logger.info("Triggering initial startup run...")
        run_job()
    except Exception as e:
        logger.error(f"Initial run failed: {e}")

    # Schedule the job
    trigger = CronTrigger(hour='9,15,21', minute='0', timezone=ist)
    scheduler.add_job(run_job, trigger)
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")

if __name__ == "__main__":
    start_scheduler()
