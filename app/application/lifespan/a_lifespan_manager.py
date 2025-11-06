import asyncio
import logging
from asyncio import Task
from multiprocessing import Process

from application.jobs.a_jobs import dummy_job
from settings.console_styles import Style


logger = logging.getLogger(__name__)


class ALifespanManager:
    def __init__(self, process: Process):
        self.process: Process = process
        self.bg_tasks: list[Task] = []

    async def start_background_tasks(self) -> None:
        logger.info(
            f"Запускаем фоновые задачи"
            f" {Style.CGREEN}{self.process.name}{Style.CEND}"
            f" [{Style.CBEIGE}{self.process.pid}{Style.CEND}]"
        )

        self.bg_tasks = [
            asyncio.create_task(dummy_job()),
        ]

        logger.info(
            f"Фоновые задачи запущены"
            f" {Style.CGREEN}{self.process.name}{Style.CEND}"
            f" [{Style.CBEIGE}{self.process.pid}{Style.CEND}]"
        )

    async def stop_background_tasks(self) -> None:
        logger.info(
            f"Останавливаем фоновые задачи"
            f" {Style.CGREEN}{self.process.name}{Style.CEND}"
            f" [{Style.CBEIGE}{self.process.pid}{Style.CEND}]"
        )

        for task in self.bg_tasks:
            task.cancel()
        await asyncio.gather(*self.bg_tasks, return_exceptions=True)

        logger.info(
            f"Фоновые задачи остановлены"
            f" {Style.CGREEN}{self.process.name}{Style.CEND}"
            f" [{Style.CBEIGE}{self.process.pid}{Style.CEND}]"
        )

    async def start(self):
        logger.info(
            f"Запускаем работу процесса"
            f" {Style.CGREEN}{self.process.name}{Style.CEND}"
            f" [{Style.CBEIGE}{self.process.pid}{Style.CEND}]"
        )

        await self.start_background_tasks()

        logger.info(
            f"Работа процесса запущена"
            f" {Style.CGREEN}{self.process.name}{Style.CEND}"
            f" [{Style.CBEIGE}{self.process.pid}{Style.CEND}]"
        )

    async def stop(self):
        logger.info(
            f"Завершение работ процесса"
            f" {Style.CGREEN}{self.process.name}{Style.CEND}"
            f" [{Style.CBEIGE}{self.process.pid}{Style.CEND}]"
        )

        await self.stop_background_tasks()

        logger.info(
            f"Работа процесса остановлена"
            f" {Style.CGREEN}{self.process.name}{Style.CEND}"
            f" [{Style.CBEIGE}{self.process.pid}{Style.CEND}]"
        )

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
