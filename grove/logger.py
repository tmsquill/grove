import time

from logbook import FileHandler, Logger

log = None
log_handler = None


def init_logger(log_path=None):

    """
    Initializes the logger for various grove components.
    :param log_path: The directory that Grove will produce log files. If not specified logs will be saved to the
    """

    if log_path:

        global log_handler
        log_handler = FileHandler(log_path + '/log/grove-' + time.strftime("%I:%M-M%mD%dY%Y" + '.log'))

    else:

        global log_handler
        log_handler = FileHandler('./log/grove-' + time.strftime("%I:%M-M%mD%dY%Y" + '.log'))

    global log_handler
    log_handler.format_string = '{record.message}'

    global log
    log = Logger('Grove Logger')
