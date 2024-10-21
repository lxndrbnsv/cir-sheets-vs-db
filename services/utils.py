import json
import logging


class Phone:
    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number

    def transform_phone(self) -> str:
        """Приводим номер телефона к стандарту (10 последних цифр)"""
        digits = "".join(filter(str.isdigit, self.phone_number))
        return f"+7{digits[-10:]}"


class BasicLogger:
    def __init__(self, msg):
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            level=logging.INFO,
        )
        logging.info(msg)
