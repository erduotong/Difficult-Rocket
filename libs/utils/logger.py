"""
@author shenjackyuanjie
@contact 3695888@qq.com
"""
#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
import os
import re
import sys
import time
import atexit
import inspect
import threading
import dataclasses

from abc import ABC
from queue import Queue
from time import strftime
from types import FrameType
from logging import NOTSET, DEBUG
from typing import NamedTuple, Optional, Type, Union, Dict, Iterable, Any, List

Version = '1.0.0'

os.system('')
# print(os.path.abspath(os.curdir))
# TODO 这个文件就是个大TODO
"""
如果想要直接使用 logger 来 logging
直接调用 logger.debug() 即可
默认配置会有
----------
配置方式一
直接使用 logger.Logger()
将会创建一个空 logger
可以自行通过
配置方式二
logger = logger.get_logger(name)
直接获取一个配置好的logger
"""

color_reset_suffix = "\033[0m"
""" 只是用来重置颜色的后缀 """

re_find_color_code = r'\033\[[^\f\n\r\t\vm]*m'
re_color_code = re.compile(re_find_color_code)

re_find_level_code = r''

"""
OFF > FATAL > ERROR > WARN > INFO > FINE > FINER > DEBUG > TRACE > ALL
logging.py
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
"""
FINE = 7
TRACE = 5
ALL = NOTSET


class LoggingLevel:
    """定义LoggingLevel属性（即是变量） """
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    FINE = 7
    TRACE = 5
    NOTSET = 0
    ALL = NOTSET
    CRITICAL_t = 'CRITICAL'
    FATAL_t = 'FATAL'
    ERROR_t = 'ERROR'
    WARNING_t = 'WARNING'
    WARN_t = 'WARN'
    INFO_t = 'INFO'
    DEBUG_t = 'DEBUG'
    FINE_t = 'FINE'
    TRACE_t = 'TRACE'
    NOTSET_t = 'NOTSET'
    ALL_t = 'ALL'

    @staticmethod
    def type() -> Type:
        return int


logging_level_type = int

level_name_map: Dict[logging_level_type, str] = {
    LoggingLevel.ALL:     'ALL',  # NOTSET
    LoggingLevel.TRACE:   'TRACE',
    LoggingLevel.FINE:    'FINE',
    LoggingLevel.DEBUG:   'DEBUG',
    LoggingLevel.INFO:    'INFO',
    LoggingLevel.WARNING: 'WARNING',  # WARN
    LoggingLevel.ERROR:   'ERROR',
    LoggingLevel.FATAL:   'FATAL'
}

name_level_map: Dict[str, logging_level_type] = {
    'NOTSET':   LoggingLevel.ALL,
    'ALL':      LoggingLevel.ALL,
    'TRACE':    LoggingLevel.TRACE,
    'FINE':     LoggingLevel.FINE,
    'DEBUG':    LoggingLevel.DEBUG,
    'INFO':     LoggingLevel.INFO,
    'WARNING':  LoggingLevel.WARNING,
    'WARN':     LoggingLevel.WARNING,
    'ERROR':    LoggingLevel.ERROR,
    'CRITICAL': LoggingLevel.FATAL,
    'FATAL':    LoggingLevel.FATAL
}


def get_level_by_name(name: str) -> logging_level_type:
    return name_level_map[name.upper()]


def get_name_by_level(level: logging_level_type) -> str:
    return level_name_map[level]


logger_configs = {
    'Logger':    {
        'root':   {
            'level': DEBUG,
            'color': 'main_color',
            'file':  'main_log_file',
        },
        'client': {
            'level': TRACE,
            'color': 'main_color',
            'file':  'main_log_file',
        },
        'server': {
            'level': TRACE,
            'color': 'DiGua_color',
            'file':  'main_log_file',
        },

    },
    'Color':     {
        'main_color':       {
            # 'file_time':            '\033[38;2;201;222;56m',
            'main_time':            '\033[38;2;201;222;56m',
            'file_name':            '\033[38;2;0;255;180m',
            'code_line':            '\033[38;2;0;255;180m',
            'info':                 '\033[0m',
            'message':              '\033[0m',
            'logger':               '\033[0m',
            'marker':               '\033[0m',
            LoggingLevel.TRACE_t:   {'info': '\033[38;2;138;173;244m'},
            LoggingLevel.FINE_t:    {'info': '\033[35;48;2;44;44;54m'},
            LoggingLevel.DEBUG_t:   {'info': '\033[38;2;133;138;149m'},
            LoggingLevel.INFO_t:    {'info': '\033[0m'},
            LoggingLevel.WARNING_t: {'info': '\033[33m'},
            LoggingLevel.ERROR_t:   {'info': '\033[31m'},
            LoggingLevel.FATAL_t:   {'info': '\033[38;2;255;255;0;48;2;120;10;10m', 'logger': '\033[38;2;245;189;230m'}
        },
        'fancy_main_color': {
            # 'file_time':            '\033[38;2;201;222;56m',
            'main_time':            '\033[38;2;201;222;56m',
            'file_name':            '\033[38;2;0;255;180m',
            'code_line':            '\033[38;2;0;255;180m',
            'logger':               '\033[0m',
            'message':              '\033[0m',
            LoggingLevel.TRACE_t:   {'info': '\033[38;2;138;173;244m', 'message': '\033[38;2;138;173;244m'},
            LoggingLevel.FINE_t:    {'info': '\033[35;48;2;44;44;54m', 'message': '\033[35m'},
            LoggingLevel.DEBUG_t:   {'info': '\033[38;2;133;138;149m', 'message': '\033[38;2;133;138;149m'},
            LoggingLevel.INFO_t:    {'info': '\033[0m', 'message': '\033[0m'},
            LoggingLevel.WARNING_t: {'info': '\033[33m', 'message': '\033[33m'},
            LoggingLevel.ERROR_t:   {'info': '\033[31m', 'message': '\033[31m'},
            LoggingLevel.FATAL_t:   {'info':    '\033[38;2;255;255;0;48;2;120;10;10m',
                                     'message': '\033[38;2;255;255;0;48;2;120;10;10m', 'logger': '\033[38;2;245;189;230m'}
        },
        'DiGua_color':      {
            # catppuccin Macchiato
            # 'file_time':            '\033[38;2;238;212;159m',
            'main_time':            '\033[38;2;202;211;245m',
            'file_name':            '\033[38;2;139;213;202m',
            'code_line':            '\033[38;2;166;218;149m',
            'logger':               '\033[0m',
            'message':              '\033[0m',
            LoggingLevel.TRACE_t:   {'info': '\033[38;2;138;173;244m', 'message': '\033[38;2;138;173;244m'},
            LoggingLevel.FINE_t:    {'info': '\033[38;2;198;160;246m', 'message': '\033[38;2;198;160;246m'},
            LoggingLevel.DEBUG_t:   {'info': '\033[38;2;133;138;149m', 'message': '\033[38;2;133;138;149m'},
            LoggingLevel.INFO_t:    {'info': '\033[0m', 'message': '\033[0m'},
            LoggingLevel.WARNING_t: {'info': '\033[38;2;245;169;127m', 'message': '\033[38;2;245;169;127m'},
            LoggingLevel.ERROR_t:   {'info': '\033[38;2;237;135;150m', 'message': '\033[38;2;237;135;150m'},
            LoggingLevel.FATAL_t:   {'info':    '\033[38;2;255;255;0;48;2;120;10;10m',
                                     'message': '\033[38;2;255;255;0;48;2;120;10;10m', 'logger': '\033[38;2;245;189;230m'}
        }
    },
    'File':      {
        'main_log_file': {
            'mode':       'a',
            'encoding':   'utf-8',
            'level':      TRACE,
            'file_name':  './logs/{long_time}_logs.md',
            'cache_len':  10,
            'cache_time': 1
        },
    },
    'Formatter': {
        'MESSAGE':    {
            'format': '[{long_time}] [{logger_name}] {level} | {file_name}:{code_line} | {message}'
        },
        'file_name':  'no frame',
        'code_line':  'no frame',
        'short_time': '%Y-%m-%d %H-%M-%S',
        'long_time':  '%Y-%m-%d %H-%M-%S:%%S',
    }
}


@dataclasses.dataclass
class LogFileConf:
    file_name: str = 'logs/log.txt'
    file_mode: str = 'a'
    file_encoding: str = 'utf-8'
    file_level: logging_level_type = LoggingLevel.DEBUG
    file_cache_len: int = 20
    file_cache_time: Union[int, float] = 1


class Message_content(NamedTuple):
    """用于存储 log 信息的不可变元组"""
    log_time: float
    text: str
    level: int
    marker: Optional[str] = None
    end: Optional[str] = '\n'
    flush: Optional[bool] = False
    frame: Optional[FrameType] = None


class ThreadLock:
    """一个用来 with 的线程锁"""

    def __init__(self, the_lock: threading.Lock, time_out: Union[float, int] = 1 / 60) -> None:
        """
        :param the_lock: 用于 with 的线程锁
        :param time_out: with 的超时时间
        """
        self.lock = the_lock
        self.time_out = time_out

    def __enter__(self):
        self.lock.acquire(timeout=self.time_out)
        if not self.lock.locked():
            raise RuntimeError(f'Lock time Out with {self.time_out}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.lock.locked():
            self.lock.release()


class ListCache:
    """一个线程安全的列表缓存"""

    def __init__(self, lock: ThreadLock):
        self._cache = []
        self.with_thread_lock = lock

    def append(self, value: Union[str, Iterable[str]]):
        with self.with_thread_lock:
            if isinstance(value, str):
                self._cache.append(value)
            elif isinstance(value, Iterable):
                self._cache.append(*value)
            else:
                raise TypeError(
                    f"cache must be string or Iterable. not a {type(value)}")

    def __getitem__(self, item) -> str:
        assert isinstance(item, int)
        with self.with_thread_lock:
            try:
                return self._cache[item]
            except IndexError as exp:
                print(f'cache:{self.cache}')
                raise IndexError(
                    f'there is no cache at {item}!\ncache:{self.cache}\n{exp}')

    def __call__(self, *args, **kwargs) -> List[str]:
        return self.cache

    def __iter__(self):
        self._iter_len = len(self.cache)
        return self

    def __next__(self):
        if self._iter_len == -1:
            del self._iter_len
            raise StopIteration('there is no more cache')
        returns = self.cache[-self._iter_len]
        self._iter_len -= 1
        return returns

    def __bool__(self):
        return True if len(self.cache) > 0 else False

    @property
    def cache(self):
        return self._cache

    def clear(self):
        with self.with_thread_lock:
            self.cache.clear()


class FormatterTemplate(ABC):
    """用于格式化 log 信息的模板类"""

    def __init__(self, formats: str):
        self.formats = formats

    def format(self, message: str) -> str:
        raise NotImplementedError('There is a formatter that not implemented')


class StdFormatter(FormatterTemplate):
    """ 一个标准的格式化类 """

    def __init__(self, formats: str):
        super().__init__(formats=formats)
        ...

    def format(self, message: Message_content) -> Message_content:
        ...


"""
logger a 
.enable = True
.level = 0
handler b -> shell
    .enable = True
    .level = 30
handler c -> file
    .enable = True
    .level = 0 
    
a.info('abc')

b -> none
c -> [info]'abc'

"""


class StreamHandlerTemplate:
    """ 一个一个一个 stream template 啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊 """
    name = "handler temple"

    def __init__(self, level: int, formatter: Optional[FormatterTemplate] = None):
        """
        :param level: 处理器输出等级
        :param formatter: 格式化处理器
        """
        self.enable = True
        self.level = level
        self.formatter = formatter

    def write(self, message: Message_content) -> bool:
        """
        向 输出 文件/stdio 写入信息
        :param message: 要写入的信息包
        :return: 是否写入成功
        """
        raise NotImplementedError("You Need to Implement the 'write' method")

    def flush(self) -> bool:
        """
        刷新缓冲区
        :return: 是否刷新成功
        """
        return True

    def close(self) -> bool:
        """
        :return: stream 是否关闭成功
        """
        raise NotImplementedError("You Need to Implement the 'close' method")

    def setFormatter(self, fmt: FormatterTemplate) -> None:
        """
        用于与 logging 兼容
        :param fmt: 要设置的格式化处理器
        :return: None
        """
        self.formatter = fmt

    def __str__(self):
        """
        :return: 自己的名字 等级
        """
        return f"{self.name}{{level={self.level}}}"


class StdHandler(StreamHandlerTemplate):
    """ 向标准输入输出流输出信息 """
    name = "std handler"

    def __init__(self, level: int, formatter: Optional[FormatterTemplate] = None):
        """
        :param level: 级别
        :param formatter: 格式器
        """
        super().__init__(level=level, formatter=formatter)

    def write(self, message: Message_content) -> bool:
        print(self.formatter.format(message.text), end=message.end, flush=message.flush)
        return True

    def close(self) -> bool:
        return True

    def flush(self) -> bool:
        print('', end='', flush=True)
        return True


class CachedFileHandler(StreamHandlerTemplate):
    """ 缓存文件的处理器 """
    name = 'cached file handler'

    def __init__(self, level: int, formatter: Optional[FormatterTemplate] = None, file_conf: Union[dict, LogFileConf, None] = None):
        """
        :param level:
        :param formatter:
        :param file_conf: 文件配置
        """
        super().__init__(level=level, formatter=formatter)
        if file_conf is not None:
            if isinstance(file_conf, dict):
                self.file_conf = LogFileConf(**file_conf)
            elif isinstance(file_conf, LogFileConf):
                self.file_conf = file_conf
        else:
            self.file_conf = LogFileConf()
        # 缓存
        self.string_queue = Queue(maxsize=self.file_conf.file_cache_len)
        # 状态
        self.started = True
        self.thread_started = False
        self.running = False
        # 同步锁
        self.cache_lock = threading.Lock()  # 主锁
        self.time_limit_lock = ThreadLock(self.cache_lock, time_out=1 / 60)  # 直接用于 with 的主锁
        self.threaded_write = threading.Timer(1, self._thread_write, kwargs={'by_thread': True})  # 基于 timer 的多线程

    def _start_thread(self) -> bool:
        """
        如果成功启动 返回 True
        已经启动则返回 False
        :return: 是否启动
        """
        if self.thread_started:
            return False
        self.threaded_write = threading.Timer(1, self._thread_write, kwargs={'by_thread': True})
        self.threaded_write.start()
        self.thread_started = True
        return True

    def _stop_thread(self) -> bool:
        """
        成功关闭 返回 True
        未开启/关闭失败 返回 False
        :return: 是否成功关闭
        """
        if not self.threaded_write.is_alive():
            self.thread_started = False
            return False
        self.threaded_write.cancel()

    def _thread_write(self, by_thread: bool) -> None:
        if not self.string_queue.empty():  # 队列非空
            with self.time_limit_lock and open(file=self.file_conf.file_name, mode=self.file_conf.file_mode,
                                               encoding=self.file_conf.file_encoding) as log_file:
                while not self.string_queue.empty():
                    log_file.write(self.string_queue.get())

    def write(self, message: Message_content) -> bool:
        if not message.flush:
            if self.string_queue.qsize() + 1 <= self.file_conf.file_cache_len:
                self.string_queue.put_nowait(message)
            else:
                if not self.thread_started:
                    self.threaded_write.start()
        else:
            ...
        return True

    def close(self) -> bool:
        ...

    def flush(self) -> bool:
        ...


class LogFileCache:
    """日志文件缓存"""

    def __init__(self, file_conf: dict):
        """
        :param file_conf: 日志文件配置
        """
        # 配置相关
        self._logfile_name = os.path.abspath(format_str(file_conf['file_name']))  # log 文件名称
        self.level: logging_level_type = get_key_from_dict(file_conf, 'level', DEBUG)
        self.file_conf = file_conf
        self.flush_time = file_conf['cache_time']  # 缓存刷新时长
        self.cache_entries_num = file_conf['cache_len']
        self.started = True
        self.running = False
        # 同步锁
        self.cache_lock = threading.Lock()  # 主锁
        self.time_limit_lock = ThreadLock(self.cache_lock, time_out=1 / 60)  # 直接用于 with 的主锁
        self.threaded_write = threading.Timer(1, self._log_file_time_write, kwargs={'thread': True})  # 基于 timer 的多线程
        # 日志缓存表
        self.log_cache = ListCache(self.time_limit_lock)
        self.file_setup()

    def file_setup(self):
        cache_time = 0
        file_type = self.logfile_name[self.logfile_name.rfind('.'):]
        file_pure_name = self.logfile_name[:self.logfile_name.rfind('.')]
        while os.path.isfile(self.logfile_name):
            cache_time += 1
            self.logfile_name = f'{file_pure_name}-{cache_time}{file_type}'

    def end_thread(self) -> None:
        """结束日志写入进程，顺手把目前的缓存写入"""
        self.cache_lock.acquire(blocking=True)
        if self.running:
            self.threaded_write.cancel()
            self.running = False
        self.started = False
        self._log_file_time_write()
        atexit.unregister(self.end_thread)

    def start_thread(self) -> None:
        self.threaded_write.start()
        self.started = True
        self.running = True
        atexit.register(self.end_thread)

    @property
    def logfile_name(self) -> str:
        self._logfile_name: str
        return self._logfile_name

    @logfile_name.setter
    def logfile_name(self, value: str) -> None:
        with self.time_limit_lock:
            self._logfile_name = value

    def _log_file_time_write(self, thread: bool = False) -> None:
        """使用 threading.Timer 调用的定时写入日志文件的函数"""
        if self.log_cache:
            with self.time_limit_lock:
                if self.log_cache:
                    with open(file=self.logfile_name,
                              encoding=get_key_from_dict(
                                  self.file_conf, 'encoding', 'utf-8'),
                              mode=get_key_from_dict(self.file_conf, 'mode', 'a')) as log_file:
                        log_file.writelines(self.log_cache.cache.copy())
                    self.log_cache.clear()
                    if thread:
                        self.running = False

    def write_logs(self, string: str, flush: bool = False) -> None:
        self.log_cache.append(string)
        if len(self.log_cache.cache) >= 10:
            self._log_file_time_write()
            return None
        if flush:
            self._log_file_time_write()
        if self.started and not self.running:
            self.threaded_write = threading.Timer(1, self._log_file_time_write, kwargs={
                'thread': True})  # 基于 timer 的多线程
            self.threaded_write.start()
            self.running = True


class Logger:
    """shenjackのlogger"""

    def __init__(self,
                 name: str = 'root',
                 level: int = DEBUG,
                 file_conf: Optional[List[LogFileCache]] = None,
                 colors: Optional[Dict[Union[int, str],
                                       Dict[str, str]]] = None,
                 formats=None) -> None:
        """
        配置模式: 使用 kwargs 配置
        :param name: logger 名称 默认为 root
        :param level: logging 输出等级 默认为 DEBUG(10)
        :param file_conf: logger 的文件处理配置
        :param colors: dict 颜色配置
        :param formats: 格式化配置
        """
        self.enable = True
        self.name = name
        self.level = level
        self.low_level = level
        self.colors = colors or logger_configs['Color']['main_color']
        self.formats = formats or logger_configs['Formatter'].copy()
        self.streams = []  # type: List[StreamHandlerTemplate]
        self.min_level = self.level
        self.handler = []
        if file_conf:
            self.file_cache = file_conf
            self.min_level = min(
                *[file.level for file in file_conf], self.level)
        else:
            self.file_cache = []
        self.warn = self.warning

    def format_formats(self) -> None:
        if 'long_time' not in self.formats:
            self.formats['long_time'] = '%Y-%m-%d %H-%M-%S:%%S'
        if 'short_time' not in self.formats:
            self.formats['short_time'] = '%Y-%m-%d %H-%M-%S'

    def add_stream(self, stream: StreamHandlerTemplate) -> bool:
        """
        向 logger 添加一个输出方法 (stream handler)
        :param stream: 将要添加的 stream handler
        :return: 是否添加成功 如果 stream 已经存在则返回 False
        """
        if stream in self.streams:
            return False
        self.streams.append(stream)
        return True

    def enabled_for(self, level: logging_level_type) -> bool:
        if not self.enable:
            return False
        return True

    def format_time(self, input_time: Optional[float] = None) -> Dict[str, str]:
        # 毫秒
        get_time: float = input_time or time.time()
        millisecond = str((get_time - int(get_time)) * 1000)
        long_time = time.strftime(
            self.formats['long_time'].replace('%%S', millisecond))
        short_time = time.strftime(
            self.formats['short_time'].replace('%%S', millisecond))
        return {'long_time': long_time, 'short_time': short_time}

    # def filter_and_make_log(): make_log(formatted_string)
    def make_log(self, *values: object,
                 level: int,
                 marker: Optional[str] = None,
                 sep: Optional[str] = ' ',
                 end: Optional[str] = '\n',
                 flush: Optional[bool] = False,
                 frame: Optional[FrameType] = None) -> Optional[str]:
        if frame is None:
            if (frame := inspect.currentframe()) is not None:
                frame = frame if frame.f_back is None else frame.f_back if frame.f_back.f_back is None else frame.f_back.f_back
        message = Message_content(log_time=time.time(),
                                  text=sep.join(i if type(i) is str else str(i) for i in values),
                                  level=level, marker=marker, end=end, flush=flush, frame=frame)
        message_color = self.colors[get_name_by_level(
            level)]['message'] if 'message' in self.colors[get_name_by_level(level)] else self.colors['message']
        text = f"{message_color}{sep.join(i if type(i) is str else str(i) for i in values)}{color_reset_suffix}"
        # print('abc', 'abc', marker='123')
        print_text = self.format_text(level=level, text=text, frame=frame)
        if level >= self.level:
            print(print_text, end=end)
        for file in self.file_cache:
            file: LogFileCache
            if level < file.level:
                continue
            file.write_logs(
                f"{re.sub(re_find_color_code, '', print_text)}{end}", flush=flush)
        return print_text

    def format_text(self, level: int, text: str, frame: Optional[FrameType]) -> str:
        level_with_color = f"[{get_key_from_dict(self.colors[get_name_by_level(level)], 'info')}{get_name_by_level(level)}{color_reset_suffix}]"
        level_with_color = f"{level_with_color}{' ' * (9 - len_without_color_maker(level_with_color))}"
        formats = self.formats.copy()
        if frame is not None:
            formats['file_name'] = f"{get_key_from_dict(self.colors[get_name_by_level(level)], 'file_name', self.colors['file_name'])}{os.path.split(frame.f_code.co_filename)[-1]}{color_reset_suffix}"
            formats['code_line'] = f"{get_key_from_dict(self.colors[get_name_by_level(level)], 'code_line', self.colors['code_line'])}{frame.f_lineno}{color_reset_suffix}"
        formats['logger_name'] = f'{get_key_from_dict(self.colors[get_name_by_level(level)], "logger", self.colors["logger"])}{self.name}{color_reset_suffix}'
        now_time = str(time.time())
        for key, value in formats.items():
            if isinstance(value, dict):
                if 'strftime' in value:
                    value['strftime']: str
                    formats[key] = f"{get_key_from_dict(self.colors[get_name_by_level(level)], key, self.colors[key])}{strftime(value['strftime'].replace('%%S', now_time[now_time.find('.') + 1:now_time.find('.') + 5]))}{color_reset_suffix}"
        print_text = self.formats['MESSAGE']['format'].format(level_with_color=level_with_color,
                                                              level=level_with_color, message=text,
                                                              **formats)
        return print_text

    def trace(self, *values: object,
              marker: Optional[str] = None,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False,
              frame: Optional[FrameType] = None) -> Optional[str]:
        return self.make_log(*values, level=LoggingLevel.TRACE, marker=marker, sep=sep, end=end, flush=flush, frame=frame)

    def fine(self, *values: object,
             marker: Optional[str] = None,
             sep: Optional[str] = ' ',
             end: Optional[str] = '\n',
             flush: Optional[bool] = False,
             frame: Optional[FrameType] = None) -> Optional[str]:
        return self.make_log(*values, level=LoggingLevel.FINE, marker=marker, sep=sep, end=end, flush=flush, frame=frame)

    def debug(self, *values: object,
              marker: Optional[str] = None,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False,
              frame: Optional[FrameType] = None) -> Optional[str]:
        return self.make_log(*values, level=LoggingLevel.DEBUG, marker=marker, sep=sep, end=end, flush=flush, frame=frame)

    def info(self, *values: object,
             marker: Optional[str] = None,
             sep: Optional[str] = ' ',
             end: Optional[str] = '\n',
             flush: Optional[bool] = False,
             frame: Optional[FrameType] = None) -> Optional[str]:
        return self.make_log(*values, level=LoggingLevel.INFO, marker=marker, sep=sep, end=end, flush=flush, frame=frame)

    def warning(self, *values: object,
                marker: Optional[str] = None,
                sep: Optional[str] = ' ',
                end: Optional[str] = '\n',
                flush: Optional[bool] = False,
                frame: Optional[FrameType] = None) -> Optional[str]:
        return self.make_log(*values, level=LoggingLevel.WARNING, marker=marker, sep=sep, end=end, flush=flush, frame=frame)

    def error(self, *values: object,
              marker: Optional[str] = None,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False,
              frame: Optional[FrameType] = None) -> Optional[str]:
        return self.make_log(*values, level=LoggingLevel.ERROR, marker=marker, sep=sep, end=end, flush=flush, frame=frame)

    def fatal(self, *values: object,
              marker: Optional[str] = None,
              sep: Optional[str] = ' ',
              end: Optional[str] = '\n',
              flush: Optional[bool] = False,
              frame: Optional[FrameType] = None) -> Optional[str]:
        return self.make_log(*values, level=LoggingLevel.FATAL, marker=marker, sep=sep, end=end, flush=flush, frame=frame)


_logger_class = Logger


class RootLogger(Logger):
    """ 默认的 logger """

    def __init__(self, level: int = LoggingLevel.WARNING, *args, **kwargs):
        super().__init__(level=level, *args, **kwargs)


root_logger = RootLogger()


def basic_config() -> None:
    ...


def trace(*values: object,
          marker: Optional[str] = None,
          sep: Optional[str] = ' ',
          end: Optional[str] = '\n',
          flush: Optional[bool] = False,
          frame: Optional[FrameType] = None) -> Optional[str]:
    ...


def fine(*values: object,
         marker: Optional[str] = None,
         sep: Optional[str] = ' ',
         end: Optional[str] = '\n',
         flush: Optional[bool] = False,
         frame: Optional[FrameType] = None) -> Optional[str]:
    ...


def debug(*values: object,
          marker: Optional[str] = None,
          sep: Optional[str] = ' ',
          end: Optional[str] = '\n',
          flush: Optional[bool] = False,
          frame: Optional[FrameType] = None) -> Optional[str]:
    ...


def info(*values: object,
         marker: Optional[str] = None,
         sep: Optional[str] = ' ',
         end: Optional[str] = '\n',
         flush: Optional[bool] = False,
         frame: Optional[FrameType] = None) -> Optional[str]:
    ...


def warning(*values: object,
            marker: Optional[str] = None,
            sep: Optional[str] = ' ',
            end: Optional[str] = '\n',
            flush: Optional[bool] = False,
            frame: Optional[FrameType] = None) -> Optional[str]:
    ...


def error(*values: object,
          marker: Optional[str] = None,
          sep: Optional[str] = ' ',
          end: Optional[str] = '\n',
          flush: Optional[bool] = False,
          frame: Optional[FrameType] = None) -> Optional[str]:
    ...


def fatal(*values: object,
          marker: Optional[str] = None,
          sep: Optional[str] = ' ',
          end: Optional[str] = '\n',
          flush: Optional[bool] = False,
          frame: Optional[FrameType] = None) -> Optional[str]:
    ...


def get_key_from_dict(a_dict: Dict, key: Any, default: Any = None) -> Optional[Any]:
    if default is None:
        return a_dict[key]
    try:
        return a_dict[key]
    except KeyError:
        return default


def format_str(text: str) -> str:
    formats = logger_configs['Formatter'].copy()
    now_time = str(time.time())
    for key, value in formats.items():
        if isinstance(value, dict):
            if 'strftime' in value:
                value['strftime']: str
                formats[key] = strftime(value['strftime'].replace(
                    '%%S', now_time[now_time.find('.') + 1:now_time.find('.') + 5]))
    return text.format(**formats)


def len_without_color_maker(text: str) -> int:
    with_out_text = re.sub(re_find_color_code, '', text)
    return len(with_out_text)


def gen_file_conf(file_name: str,
                  file_level: int = DEBUG,
                  file_mode: str = 'a',
                  file_encoding: str = 'utf-8',
                  file_cache_len: int = 10,
                  file_cache_time: Union[int, float] = 1) -> dict:
    """
    生成一个文件配置
    :param file_name: 日志文件名
    :param file_level: 日志文件记录级别
    :param file_mode: 文件模式
    :param file_encoding: 文件编码
    :param file_cache_len: 文件缓存长度
    :param file_cache_time: 文件缓存时间
    :return: 生成的配置
    """
    return {'file_name':  file_name,
            'level':      file_level,
            'mode':       file_mode,
            'encoding':   file_encoding,
            'cache_len':  file_cache_len,
            'cache_time': file_cache_time}


def gen_color_conf(color_name: Optional[str] = None, **colors) -> dict:
    default_color = logger_configs['Color']['main_color' if color_name is None else color_name].copy(
    )
    default_color.update(colors)
    return default_color


def logger_with_default_settings(name: str,
                                 level: int = DEBUG,
                                 file_conf: Optional[dict] = None,
                                 colors: Optional[dict] = None,
                                 formats: Optional[dict] = None) -> Logger:
    return Logger(name=name,
                  level=level,
                  file_conf=[LogFileCache(gen_file_conf(**file_conf))],
                  colors=gen_color_conf(**colors),
                  formats=logger_configs['Formatter'].copy().update(formats))


def add_file_config(conf_name: str,
                    file_name: str,
                    file_level: int = DEBUG,
                    file_mode: str = 'a',
                    file_encoding: str = 'utf-8',
                    file_cache_len: int = 10,
                    file_cache_time: Union[int, float] = 1) -> None:
    """
    向 logger config 里添加一个文件配置
    :param conf_name: 文件配置名称
    :param file_name: 日志文件名
    :param file_level: 日志文件记录级别
    :param file_mode: 文件模式
    :param file_encoding: 文件编码
    :param file_cache_len: 文件缓存长度
    :param file_cache_time: 文件缓存时间
    :return: None
    """
    logger_configs['File'][conf_name] = {'file_name':  file_name,
                                         'level':      file_level,
                                         'mode':       file_mode,
                                         'encoding':   file_encoding,
                                         'cache_len':  file_cache_len,
                                         'cache_time': file_cache_time}


def get_logger(name: str = 'root') -> Logger:
    """
    此函数用于从 global_config 中取出对应的配置建立一个相应的 logger
    :param name: logger的名称 默认为 root
    :return: 创建好的 logger
    """
    if name in logger_configs['Logger']:
        the_config = logger_configs['Logger'][name]
    else:
        the_config = logger_configs['Logger']['root']
    file_handler = None
    if 'file' in the_config:
        file_handler = [LogFileCache(
            logger_configs['File'][the_config['file']])]
    color = the_config['color'] if 'color' in the_config else 'main_color'
    return Logger(name=name,
                  level=the_config['level'],
                  file_conf=file_handler,
                  colors=logger_configs['Color'][color],
                  formats=logger_configs['Formatter'].copy())


def test_logger(the_logger: Logger):
    the_logger.trace('tracing')
    the_logger.fine('some fine!')
    the_logger.debug('debugging')
    the_logger.info("Hello World!!")
    the_logger.warn('warning')
    the_logger.error('error haaaa')
    the_logger.fatal('oh no')


if __name__ == "__main__":
    os.chdir('../../')
    logger = get_logger('server')

    logger.info('my name is:', logger.name)
    a_logger = get_logger('client')

    a_logger.trace('tracing')
    a_logger.fine('some fine!')
    a_logger.debug('debugging')
    a_logger.info("Hello World!!")
    a_logger.warn('warning')
    a_logger.error('error haaaa')
    a_logger.fatal('oh no')
    logger.info('my name is:', logger.name)
    for x in range(5):
        test_logger(logger)
        test_logger(a_logger)
    import rtoml

    parse_config = rtoml.dumps(logger_configs, pretty=True)
    import pprint

    sys.stdout.write(rtoml.dumps(logger_configs, pretty=True))
    print('-----------------')
    sys.stdout.write(rtoml.dumps(logger_configs, pretty=False))
    print('-----------------')
    pprint.pprint(rtoml.loads(parse_config))
