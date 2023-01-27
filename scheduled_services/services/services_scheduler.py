import schedule


class ServicesScheduler:
    def __init__(self) -> None:
        self._running = False

    # ==================== Main scheduling functions ====================#
    def every_day_schedule(
        self,
        task: "function",
        hour: str = "00",
        minute: str = "00",
    ):
        schedule.every().day.at(f"{hour}:{minute}").do(task)

    def every_week_schedule(
        self,
        task: "function",
        hour: str = "00",
        minute: str = "00",
    ):
        schedule.every().sunday.at(f"{hour}:{minute}").do(task)

    # ==================== Testing scheduling functions ====================#
    def every_seconds_schedule(self, task: "function", seconds: int = 10):
        schedule.every(seconds).seconds.do(task)

    # ==================== start/stop functions ====================#
    def run(self):
        self._running = True
        while self._running:
            schedule.run_pending()

    def stop(self):
        self._running = False
