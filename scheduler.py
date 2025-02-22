from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from main import lead_management_crew
import time

# ------------------- Schedule Workflow Using APScheduler -------------------

def run_workflow():
    print("\n🚀 Running scheduled AI-Powered Lead Management Workflow...\n")
    lead_management_crew.kickoff()
    print("\n✅ Scheduled workflow completed successfully!\n")

if __name__ == "__main__":
    # Initialize the scheduler
    scheduler = BackgroundScheduler()

    # ✅ Schedule the workflow to run every 30 minutes (adjustable)
    scheduler.add_job(run_workflow, IntervalTrigger(minutes=30))

    # ✅ Start the scheduler
    print("\n⏰ Scheduler started. The workflow will run every 30 minutes.\n")
    scheduler.start()

    # ✅ Keep the script running
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("\n⏹️ Scheduler stopped.")
