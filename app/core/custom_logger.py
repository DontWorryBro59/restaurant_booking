from datetime import date

from loguru import logger

# Получаем текущую дату в строковом формате
log_filename = f"logs/{date.today().strftime('%Y-%m-%d')}.log"

logger.add(log_filename, rotation="1 day", retention="7 days")

# Логирование с использованием имени логгера
def get_logger(name: str = None):
    if name:
        return logger.bind(name=name)
    return logger