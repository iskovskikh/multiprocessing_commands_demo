from dataclasses import dataclass

from app.domain.exceptions import ApplicationException


@dataclass(eq=False)
class LogicException(ApplicationException):
	@property
	def message(self):
		return 'В обработке запроса возникла ошибка'