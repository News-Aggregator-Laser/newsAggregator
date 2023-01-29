import schedule

from .data_fetcher.request_provider import RequestProvider


class ServicesScheduler:
    def __init__(self) -> None:
        print("Initializing Scheduler...")
        self._running = False

    # ==================== Main scheduling functions ====================#
    def every_day_schedule(
        self, task: "function", hour: str = "00", minute: str = "00"
    ):
        print(f"--> Scheduling '{task.__name__}' every day at {hour}:{minute}")
        schedule.every().day.at(f"{hour}:{minute}").do(task)

    def every_week_schedule(
        self, task: "function", hour: str = "00", minute: str = "00"
    ):
        print(f"--> Scheduling '{task.__name__}' every sunday at {hour}:{minute}")
        schedule.every().sunday.at(f"{hour}:{minute}").do(task)

    # ==================== Providers scheduling functions ====================#
    def schedule_providers(
        self, providers: list["RequestProvider"], debug: bool = False
    ):
        for provider in providers:
            print(f"--> Scheduling '{provider._host}'...", end=" ")
            if debug:
                schedule.every(provider.provider.requests_nb).seconds.do(provider.run)
            else:
                interval = 1440 / provider.provider.requests_nb
                schedule.every(interval).minutes.do(provider.run)
            print("Done")

    # ==================== Testing scheduling functions ====================#
    def every_seconds_schedule(self, task: "function", seconds: int = 10):
        print(f"--> Scheduling '{task.__name__}' every {seconds} seconds...")
        schedule.every(seconds).seconds.do(task)

    # ==================== start/stop functions ====================#
    def run(self):
        self._running = True
        while self._running:
            schedule.run_pending()
        print("Scheduler stopped")

    def stop(self):
        schedule.clear()
        self._running = False
