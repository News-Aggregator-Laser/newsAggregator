from scheduled_services.services.db_cleaner import DbCleaner
from scheduled_services.services.email_service import EmailService
from scheduled_services.services.services_scheduler import ServicesScheduler

from scheduled_services.services.data_fetcher.provider_fill import fill
from scheduled_services.services.data_fetcher.request_provider import RequestProvider


class ScheduledServices:
    def __init__(self):
        self.scheduler = ServicesScheduler()
        self.db_cleaner = DbCleaner()
        self.email_service = EmailService()

        self._need_to_restart = False

    def _check_for_restart(self):
        if self._need_to_restart:
            print("========== Restarting =========")
            self._need_to_restart = False
            self.stop()
            self.run()

    def run(self):
        from news.models import Provider

        print("======== Running scheduled services ========")
        # schedule services
        self.scheduler.every_day_schedule(
            self.email_service.send_emails, hour="12", minute="00"
        )
        self.scheduler.every_week_schedule(
            self.db_cleaner.clean_db, hour="00", minute="00"
        )

        # schedule providers
        fill()
        providers = [
            RequestProvider(provider.host, provider.token, provider)
            for provider in Provider.objects.all()
            if provider.is_active
        ]
        self.scheduler.schedule_providers(providers, debug=True)

        # schedule restart checker
        self.scheduler.every_seconds_schedule(self._check_for_restart, 60)

        # ============= Just for testing =============#
        self.scheduler.every_seconds_schedule(self.email_service.send_emails)
        # self.scheduler.every_seconds_schedule(self.db_cleaner.clean_db, 25)
        # ============= Just for testing =============#

        # start scheduler
        self.scheduler.run()

    def stop(self):
        self.scheduler.stop()

    def restart(self):
        print("ScheduledServices wil be restarted in 60s")
        self._need_to_restart = True
