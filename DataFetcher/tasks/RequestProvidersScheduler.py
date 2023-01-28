import time

import schedule

from DataFetcher.tasks import RequestProvider


class RequestProvidersScheduler:
    def __init__(self, providers: list[RequestProvider], debug: bool = False):
        self.providers = providers
        self._debug = debug
        self.running = True

    def stop(self):
        print("Exiting Scheduler...", end="")
        # schedule.clear()
        self.running = False

    def run(self):
        for provider in self.providers:
            print(f"Scheduling {type(provider).__name__}...", end="")
            if self._debug:
                schedule.every(provider.provider.requests_nb).seconds.do(provider.run)
            else:
                interval = 1440 / provider.provider.requests_nb
                schedule.every(interval).minutes.do(provider.run)
            print("Done")
        while self.running:
            schedule.run_pending()
            time.sleep(0.01)
        print("Done Stopped")


