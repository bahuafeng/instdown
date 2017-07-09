#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
A smart logger with multi-processing-rotating handler and smart and beautiful
Exception logging function.

                        NOTICE

1.  You should configure the `RELATIVE_PATH` of your logging files,
    the `RELATIVE_PATH` is relate to the `log.py` file location
2.  Although you could change the `CODE`, we recommand you do NOT change it,
    since UTF-8 works well in most of our programs.
"""
import os
import time
import logging
import traceback
from sys import exc_info
from logging.handlers import TimedRotatingFileHandler


__inited_handlers, __inited_loggers = {}, {}
__level_map = {
    'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING,
    'error': logging.ERROR, 'critical': logging.CRITICAL,
}

__all__ = ['get_logger']

# the code of output strings. Default is UTF-8
CODE = 'utf-8'
assert(CODE)
# the path of log dir relative to the path of this file
RELATIVE_PATH = '../../log'
assert(RELATIVE_PATH)


class Logger(logging.Logger):
    """A smart logger with many useful functions
    """

    def __init__(self, name, level=logging.NOTSET):
        super(Logger, self).__init__(name, level)

    def _compose_msg(self, *args, **kwargs):
        """Compose pairs in arguments to format as key=value

        Args:
            args: the string log message.
            kwargs: the log messages. it must follow {key: value} format.

        Returns:
            return the msg_list joint by '\t'.
        """
        global CODE

        msg_list = []
        if len(args) > 0:  # some string should log directly.
            msg_list.extend(map(lambda x: str(x), args))

        if len(kwargs) > 0:  # some pairs should log with compose
            for k, v in kwargs.items():
                # encode to code
                k = k.encode(CODE) if isinstance(k, unicode) else str(k)
                v = v.encode(CODE) if isinstance(v, unicode) else str(v)
                msg_list.append('{0}={1}'.format(k, v))

        return '\t'.join(msg_list)

    def debug(self, *args, **kwargs):
        """Log messages in DEBUG level.
        """
        if self.isEnabledFor(logging.DEBUG):
            msg = self._compose_msg(*args, **kwargs)
            self._log(logging.DEBUG, msg, [])

    def info(self, *args, **kwargs):
        """Log messages in INFO level.
        """
        if self.isEnabledFor(logging.INFO):
            msg = self._compose_msg(*args, **kwargs)
            self._log(logging.INFO, msg, [])

    def warning(self, *args, **kwargs):
        """Log messages in WARNING level.
        """
        if self.isEnabledFor(logging.WARNING):
            msg = self._compose_msg(*args, **kwargs)
            self._log(logging.WARNING, msg, [])

    def error(self, *args, **kwargs):
        """Log messages in ERROR level.
        """
        if self.isEnabledFor(logging.ERROR):
            msg = self._compose_msg(*args, **kwargs)
            self._log(logging.ERROR, msg, [])

    def critical(self, *args, **kwargs):
        """Log messages in CRITICAL level.
        """
        if self.isEnabledFor(logging.CRITICAL):
            msg = self._compose_msg(*args, **kwargs)
            self._log(logging.CRITICAL, msg, [])

    def exc_log(self, *args, **kwargs):
        """Get exception information and log them
        ONLY ERROR LEVEL
        """
        if not self.isEnabledFor(logging.ERROR):
            return

        # get exception
        exc = traceback.format_exc().rstrip()
        exc_index = exc.rfind('\n')
        exc = exc[exc_index + 1:]
        log_contents = ['EXC_LOG', exc]

        # get exception stack
        exc_list = list(traceback.extract_tb(exc_info()[2]))
        for i, (file, lineno, func, msg) in enumerate(exc_list):
            # get exception
            stack_info = {
                'file': file,
                'lineno': lineno,
                'func': func,
                'msg': msg,
                'i': i,
            }
            log_contents.append(
                '{i}|{file}|{lineno}|{func} {msg}'.format(**stack_info)
            )

        # dump them
        msg = self._compose_msg(*log_contents)
        self._log(logging.ERROR, msg, [])


class MultiProcessingTimedRotatingFileHandler(TimedRotatingFileHandler):
    """Logger handler suit for multi processing with time rotate
    """

    def doRollover(self):
        """Overwrite doRollover
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        if not os.path.exists(dfn):
            os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            # find the oldest log file and delete it
            for s in self.getFilesToDelete():
                os.remove(s)
        self.mode = 'a'
        self.stream = self._open()
        currentTime = int(time.time())
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and \
                not self.utc:
            dstNow = time.localtime(currentTime)[-1]
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                # DST kicks in before next rollover,
                # so we need to deduct an hour
                if not dstNow:
                    newRolloverAt = newRolloverAt - 3600
                # DST bows out before next rollover, so we need to add an hour
                else:
                    newRolloverAt = newRolloverAt + 3600
        self.rolloverAt = newRolloverAt


def __init_handler(name, level):
    """Initialize a handler. The handler splits at EVERY MIDNIGHT,
    and it won't delete any past logging files

    Args:
        name: the name of handler
        level: the level of handler

    Returns:
        return the handler object
    """
    # the root path for storing log files
    log_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        RELATIVE_PATH,
    )
    # is the path exists? or create it
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    # path of log file
    file_path = os.path.join(
        log_dir,
        '{0}_log'.format(name),
    )

    fmt = '%(levelname)s %(asctime)s %(filename)s|%(lineno)d\t%(message)s'
    formatter = logging.Formatter(fmt)

    # init a handler
    handler = MultiProcessingTimedRotatingFileHandler(
        file_path,
        when='MIDNIGHT',
        interval=1,
        backupCount=0,
    )

    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def __get_handler(name, level):
    """Get a handler of given name and level. It's a factory of handlers, the
    same object will return if you pass the same name without initialize a new
    handler object

    Args:
        name: the name of handler
        level: the level of handler

    Returns:
        return the handler object
    """
    global __inited_handlers

    if name not in __inited_handlers:
        __inited_handlers[name] = __init_handler(name, level)

    return __inited_handlers[name]


def __init_logger(name, level):
    """Initialize logger

    Args:
        name: logger name
        level: level for logging action.

    Returns:
        return the logger with 2 handlers at least.
    """
    global __inited_loggers

    handler = __get_handler(name, level)
    root_handler = __get_handler('root', logging.ERROR)
    logger = Logger(name, level)

    logger.addHandler(handler)
    logger.addHandler(root_handler)
    logger.setLevel(level)
    return logger


def get_logger(name, **kwargs):
    """To get a logger

    Args:
        name: logger name
        level: the level for logging, DEFAULT is `INFO`

    Returns:
        return the initialized logger
    """
    global __inited_loggers, RELATIVE_PATH, __level_map

    # not exists, initialize one
    if name not in __inited_loggers:
        level = kwargs.get('level', 'info')
        level.lower()
        level = __level_map.get(level, logging.INFO)
        __inited_loggers[name] = __init_logger(name, level)

    return __inited_loggers[name]

