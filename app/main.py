import asyncio
import logging
import signal
import time
from typing import Any

from application.process.dummy_process import DummyProcessChecker

logger = logging.getLogger(__name__)

shutdown_event = asyncio.Event()


def handle_signal(signum: int, frame: Any):
    logger.info(f"Получен сигнал {signum}, завершаем работу...")
    if not shutdown_event.is_set():
        logger.info("Signal received, shutting down...")
        shutdown_event.set()


def run():
    checkers = [
        DummyProcessChecker(),
    ]

    for checker in checkers:
        checker.start()


    logger.info("Все процессы запущены. Ожидание сигнала завершения...")

    # блокируемся, пока не будет сигнала завершения
    while not shutdown_event.is_set():
        time.sleep(0.5)

    # --- останавливаем процессы ---
    logger.info("Остановка процессов...")
    for checker in checkers:
        checker.stop()

    logger.info("Все процессы остановлены.")


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # Регистрируем обработчики сигналов
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, handle_signal)

    logger.info("Запуск основной программы.")
    run()
    logger.info("Выход из программы.")


if __name__ == '__main__':
    main()