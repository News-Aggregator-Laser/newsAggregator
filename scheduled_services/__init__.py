import threading

from scheduled_services.services import db_cleaner
from .services import ServicesScheduler, DbCleaner, EmailService

# init scheduler and services
scheduler = ServicesScheduler()
db_cleaner = DbCleaner()
email_service = EmailService()

# schedule services
scheduler.every_day_schedule(email_service.send_emails, hour="12", minute="00")
scheduler.every_week_schedule(db_cleaner.clean_db, hour="00", minute="00")

# ============= Just for testing =============#
scheduler.every_seconds_schedule(email_service.send_emails)
scheduler.every_seconds_schedule(db_cleaner.clean_db, 25)
# ============= Just for testing =============#

# run scheduler in a new Thread
scheduler_thread = threading.Thread(target=scheduler.run)
