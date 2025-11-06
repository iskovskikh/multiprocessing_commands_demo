import asyncio

from punq import Container

from application.lifespan.a_lifespan_manager import ALifespanManager
from application.process.base import BaseProcess, ProcessChecker
from logic.containers.a_container import get_container
from settings.console_styles import Style


class AProcess(BaseProcess):
    def run(self):
        self.start_running()

        container: Container = get_container()

        loop = asyncio.get_event_loop()
        self.logger.debug(
            f"Event loop created for"
            f" {Style.CGREEN}{self.name}{Style.CEND}"
            f" [{Style.CBEIGE}{self.pid}{Style.CEND}]"
        )
        try:
            loop.run_until_complete(self.main_loop())
        except Exception:
            import traceback

            self.logger.exception("Unhandled exception in process")
            traceback.print_exc()
        finally:
            loop.close()
            self.logger.debug(
                f"Event loop closed for"
                f" {Style.CGREEN}{self.name}{Style.CEND}"
                f" [{Style.CBEIGE}{self.pid}{Style.CEND}]"
            )

    async def main_loop(self):
        async with ALifespanManager(process=self):
            while self.is_running:
                self.logger.debug(f"A process is running (async)")
                await asyncio.sleep(0.3)


class AProcessChecker(ProcessChecker[AProcess]):
    process_type = AProcess
