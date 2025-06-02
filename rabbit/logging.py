import logging

logger = logging.getLogger(__name__)

# def setup_logging(debug):
#     logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
#     return logger
  
def setup_logging(level):

    # add 'levelname_c' attribute to log resords
    orig_record_factory = logging.getLogRecordFactory()
    log_colors = {
        logging.DEBUG:     "\033[1;34m",  # blue
        logging.INFO:      "\033[1;32m",  # green
        logging.WARNING:   "\033[1;35m",  # magenta
        logging.ERROR:     "\033[1;31m",  # red
        logging.CRITICAL:  "\033[1;41m",  # red reverted
    }
    logging_levels = [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    ]
    if level < 0 or level > len(logging_levels) - 1:
        raise ValueError(f"Invalid log level: {level}")

    def record_factory(*args, **kwargs):
        record = orig_record_factory(*args, **kwargs)
        record.levelname_c = "{}{}{}".format(
            log_colors[record.levelno], record.levelname, "\033[0m")
        return record

    logging.setLogRecordFactory(record_factory)

    # now each log record object would contain 'levelname_c' attribute
    # and you can use this attribute when configuring logging using your favorite
    # method.
    # for demo purposes I configure stderr log right here

    formatter_c = logging.Formatter("%(levelname_c)s: %(name)s: %(message)s")

    stderr_handler = logging.StreamHandler()
    log_level = logging_levels[level]
    stderr_handler.setLevel(log_level)
    stderr_handler.setFormatter(formatter_c)

    root_logger = logging.getLogger('')
    root_logger.setLevel(log_level)
    root_logger.addHandler(stderr_handler)