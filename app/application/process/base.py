import logging
import signal
from ctypes import c_bool
from multiprocessing import Process, Event, Value
from multiprocessing.sharedctypes import Synchronized
from multiprocessing.synchronize import Event as EventClass
from typing import Any

from settings.console_styles import Style


class BaseProcess(Process):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self._is_running: Synchronized[bool] = Value(c_bool, False, lock=True)
        self.terminate_flag: EventClass = Event()

    def _signal_handler(self, signum: int, frame: Any) -> None:
        self.logger.debug(f"Stopping process with signal {signum}")
        self.stop_running()

    def start_running(self) -> None:
        signal.signal(signal.SIGTERM, self._signal_handler)
        # init_signal_ignore_handler(SIGNALS_TO_IGNORE)
        self._is_running.value = True

    def stop_running(self) -> None:
        self._is_running.value = False
        self.terminate_flag.set()

    @property
    def is_running(self) -> bool:
        return self._is_running.value


class ProcessChecker[BaseProcessType: BaseProcess]:
    process_type: type[BaseProcessType]

    def __init__(
        self,
        *process_args,
        **process_kwargs,
    ) -> None:
        self.log = logging.getLogger(self.__class__.__name__)
        self.process_args = process_args
        self.process_kwargs = process_kwargs
        self.process_instance = self.process_type(
            *self.process_args,
            **self.process_kwargs,
        )

    def healthcheck(self) -> bool:  # True если здоров
        return self.process_instance.is_alive()

    def restart(self) -> None:
        self.log.info(
            f"Restart process"
            f" {Style.CGREEN}{self.process_instance.name}{Style.CEND}"
            f" [{Style.CBEIGE}{self.process_instance.pid}{Style.CEND}]"
        )
        self.stop()
        self.process_instance: BaseProcessType = self.process_type(
            *self.process_args,
            **self.process_kwargs,
        )
        self.start()

    def start(self) -> None:
        self.log.info(
            f"Starting process"
            f" {Style.CGREEN}{self.process_instance.name}{Style.CEND}"
        )
        try:
            self.process_instance.start()
            self.log.info(
                f"Started process"
                f" {Style.CGREEN}{self.process_instance.name}{Style.CEND}"
                f" [{Style.CBEIGE}{self.process_instance.pid}{Style.CEND}]"
            )

        except Exception as ex:
            self.log.exception(
                f"Caught exception {ex.__repr__()}"
                f" while starting"
                f" {Style.CGREEN}{self.process_instance.name}{Style.CEND}"
                f" [{Style.CBEIGE}{self.process_instance.pid}{Style.CEND}]"
            )
            self.stop()
            exit()

    def stop(self) -> None:
        self.log.warning(
            f"Stop process"
            f" {Style.CGREEN}{self.name}{Style.CEND}"
            f" [{Style.CBEIGE}{self.process_instance.pid}{Style.CEND}]"
        )
        self.process_instance.stop_running()
        self.process_instance.join(3)
        exitcode = self.process_instance.exitcode
        if exitcode is None:
            self.process_instance.kill()
            self.log.warning(
                f"Process "
                f" {Style.CGREEN}{self.name}{Style.CEND}"
                f" [{Style.CBEIGE}{self.process_instance.pid}{Style.CEND}]"
                f" forcibly killed"
            )
        else:
            self.log.info(
                f"Process "
                f" {Style.CGREEN}{self.name}{Style.CEND}"
                f" [{Style.CBEIGE}{self.process_instance.pid}{Style.CEND}]"
                f" gracefully stopped with code {exitcode}"
            )

    @property
    def pid(self) -> int | None:
        return self.process_instance.pid

    @property
    def name(self) -> str:
        return self.process_instance.name
