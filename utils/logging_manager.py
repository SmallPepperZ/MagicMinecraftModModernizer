import logging

logging.basicConfig(format="[{name}/{levelname}] {message}", style="{")
master_logger = logging.getLogger("strategies")