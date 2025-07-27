import logging


# Configure the root logger only once
def setup_logger():
    """
    Set up the logging configuration.
    This should be called once at the start of the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="{levelname} - {asctime} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )


# Expose a named logger
def get_logger(name: str = __name__):
    """
    Get a configured logger instance.
    :param name: Name of the logger (usually __name__)
    :return: logging.Logger
    """
    setup_logger()  # Ensure config is applied
    return logging.getLogger(name)
