from apscheduler.schedulers.blocking import BlockingScheduler


def job_function():
    print("Hello World")

sched = BlockingScheduler()

# Runs from Monday to Friday at 5:30 (am) until
sched.add_job(job_function, 'cron', day_of_week='mon-fri', hour=5, minute=30)
sched.start()