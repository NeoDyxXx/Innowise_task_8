import logging

class LoggerHandler:
    def __init__(self) -> None:
        self.logger = logging.getLogger()
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s: %(levelname)s: %(message)s')

    def log_message(self, message: str):
        self.logger.info(message)

    def log_error(self, message: str):
        self.logger.exception(message)