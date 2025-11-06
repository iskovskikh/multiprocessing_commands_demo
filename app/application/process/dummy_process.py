from application.process.base import BaseProcess, ProcessChecker
from settings.console_styles import Style


class DummyProcess(BaseProcess):
    def run(self):
        self.start_running()

        while self.is_running:
            self.logger.debug(
                f"Running process {self.name} [{Style.CBEIGE}{self.pid}{Style.CEND}]"
            )
            self.terminate_flag.wait(timeout=1)


class DummyProcessChecker(ProcessChecker[DummyProcess]):
    process_type = DummyProcess
