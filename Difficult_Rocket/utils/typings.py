#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

from typing import get_type_hints, Type, List, Union, Dict, Any, Callable, Tuple


def get_type_hints_(cls: Type):
    try:
        return get_type_hints(cls)
    except ValueError:
        return get_type_hints(cls, globalns={})


class OptionsError(Exception):
    """ option 的错误基类"""


class OptionNameNotDefined(OptionsError):
    """ 向初始化的 option 里添加了一个不存在于选项里的选项 """


class OptionNotFound(OptionsError):
    """ 某个选项没有找到 """


class Options:
    """
    Difficult Rocket 的游戏配置的存储基类
    """
    name = 'Option Base'
    cached_options: Dict[str, Union[str, Any]] = {}

    def __init__(self, **kwargs):
        self.flush_option()
        for option, value in kwargs.items():
            if option not in self.cached_options:
                raise OptionNameNotDefined(f"option: {option} with value: {value} is not defined")
            setattr(self, option, value)
        self.flush_option()

    def option(self) -> Dict[str, Any]:
        """
        获取配置类的所有配置
        :return: 自己的所有配置
        """
        values = {}
        for ann in self.__annotations__:  # 获取类型注释
            values[ann] = getattr(self, ann, None)
            if values[ann] is None:
                values[ann] = self.__annotations__[ann]

        if not hasattr(self, 'options'):
            self.options: Dict[str, Union[Callable, object]] = {}
        for option, a_fun in self.options.items():  # 获取额外内容
            values[option] = a_fun

        for option, a_fun in values.items():  # 检查是否为 property
            if a_fun is bool and getattr(self, option, None) is not None:
                values[option] = False
            if isinstance(a_fun, property):
                try:
                    values[option] = getattr(self, option)
                except AttributeError as e:
                    raise OptionNotFound(f'Option {option} is not found in {self.name}')
        return values

    def flush_option(self) -> Dict[str, Any]:
        """
        刷新缓存 options 的内容
        :return: 刷新过的 options
        """
        self.cached_options = self.option()
        return self.cached_options

    def option_with_len(self) -> List[Union[List[Tuple[str, Any, Any]], int, Any]]:
        options = self.flush_option()
        max_len_key = 1
        max_len_value = 1
        max_len_value_t = 1
        option_list = []
        for key, value in options.items():
            value_t = type(value) if not isinstance(value, Type) else value
            max_len_key = max(max_len_key, len(key))
            max_len_value = max(max_len_value, len(str(value)))
            max_len_value_t = max(max_len_value_t, len(str(value_t)))
            option_list.append((key, value, value_t))
        return [option_list, max_len_key, max_len_value, max_len_value_t]

    @classmethod
    def add_option(cls, name: str, value: Union[Callable, object]) -> Dict:
        if not hasattr(cls, 'options'):
            cls.options: Dict[str, Union[Callable, object]] = {}
        cls.options[name] = value
        return cls.options
