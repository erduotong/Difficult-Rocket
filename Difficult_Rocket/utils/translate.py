#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021-2022 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie <3695888@qq.com>
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

import inspect
# import dataclasses

from typing import Union, Tuple, Any, Type, List, Dict, Hashable

from Difficult_Rocket import DR_runtime, DR_option
from Difficult_Rocket.utils import tools
from Difficult_Rocket.exception.language import *


class Translates:
    def __init__(self,
                 value: Union[Dict[str, Any], list, tuple, str],
                 raise_error: bool = False,
                 get_list: List[str] = None,
                 error_get_list: List[str] = None,
                 final: bool = False):
        """
        一个用于翻译的东西
        :param value: 翻译键节点
        :param raise_error: 是否抛出错误
        :param get_list: 尝试获取的列表
        :param final: 是否为翻译结果 (偷懒用的)
        """
        self.value: Union[Dict[str, Any], list, tuple] = value
        self.raise_error = raise_error
        self.get_list = get_list or []
        self.error_get_list = error_get_list or []
        self.final = final

    def __getitem__(self, item: Union[str, int, Hashable]) -> Union["Translates", str, int]:
        """
        一坨答辩
        :param item: 取用的内容/小天才
        :return:
        """
        cache_get_list = self.get_list.copy()
        cache_error_get_list = self.error_get_list.copy()
        cache_get_list.append(item)
        try:
            cache = self.value[item]
            cache_get_list.append(item)
        except (KeyError, TypeError):
            # 出现问题
            if DR_option.report_translate_no_found:
                frame = inspect.currentframe()
                last_frame = frame.f_back
                if last_frame.f_code == self.__getattr__.__code__:
                    last_frame = last_frame.f_back
                call_info = f'Translate Not Found at {last_frame.f_code.co_name} by {".".join(cache_get_list)} at:' \
                            f'{last_frame.f_code.co_filename}:{last_frame.f_lineno}'
                print(call_info)
            # 如果不抛出错误
            if self.raise_error:
                raise TranslateKeyNotFound(item_names=cache_get_list) from None
            cache_error_get_list.append(item)
            if self.final:  # 如果已经是翻译结果
                return Translates(value='.'.join(cache_get_list), raise_error=False, final=True, error_get_list=cache_error_get_list)
        else:
            if self.final:
                return self
            else:
                return Translates(value=cache, raise_error=self.raise_error, get_list=cache_get_list)

    def __getattr__(self, item: Union[str, Hashable]) -> Union["Translates"]:
        if hasattr(object, item):
            return getattr(object, item)
        return self.__getitem__(item)

    def __str__(self):
        if self.final:  # 如果是字符串
            return f'{self.value}.{".".join(self.get_list)}'
        return str(self.value)


class Tr:
    """
    我不装了，我就抄了tr
    GOOD
    """
    def __init__(self, language: str = None, raise_error: bool = False):
        """
        诶嘿，我抄的MCDR
        :param language: Tr 所使用的的语言
        :param raise_error: 解析失败的时候是否报错
        """
        self.language_name = language or DR_runtime.language
        self.translates: Dict = tools.load_file(f'configs/lang/{self.language_name}.toml')
        self.default_translate: Dict = tools.load_file(f'configs/lang/{DR_runtime.default_language}.toml')
        self.不抛出异常 = raise_error

    def __call__(self, ):
        ...


class Lang:
    """
    用于创建一个对应语言的翻译类
    感谢Fallen的MCDR提供idea
    https://github.com/Fallen-Breath/MCDReforged
    可以用
    lang['language'] = 'abc' 或
    lang['lang'] = 'abc'
    的方式直接更改并刷新翻译
    用
    lang.lang(xxx, xxx)来获取翻译过的值
    """

    def __init__(self) -> None:
        self.translates = tools.load_file(f'configs/lang/{DR_runtime.language}.toml')
        self.default_translates = tools.load_file('configs/lang/zh-CN.toml')
        self.直接返回原始数据 = True

    def __str__(self) -> str:
        return DR_option.language

    def __getitem__(self, item) -> Union[int, str, list, dict]:
        try:
            return self.translates[item]
        except KeyError:
            try:
                return self.default_translates[item]
            except KeyError:
                raise TranslateKeyNotFound(f'there\'s no key {item} in both {DR_option.language} and zh-CN')

    def lang(self, *args) -> Union[int, str, list, dict, tuple]:
        # frame = inspect.currentframe()
        # # print("调用当前log的文件名:", frame.f_back.f_code.co_filename)
        # objprint.objprint(frame.f_back.f_code,
        #                   honor_existing=False,
        #                   depth=2)
        try:
            result = self.translates
            for option in args:
                result = result[option]
            return result
        except KeyError:
            try:
                result = self.default_translates
                for option in args:
                    result = result[option]
                return result
            except KeyError as e:
                if self.直接返回原始数据:
                    return args
                raise TranslateKeyNotFound(f'there\'s no key {args} in both {DR_option.language} and zh-CN') from e

    def 翻译(self, *args) -> Union[int, str, list, dict]:
        return self.lang(args)

    def _update_lang(self) -> str:
        """
        用于更新语言(内部调用)
        :return: 设置完成后的语言
        """
        self.translates = tools.load_file(f'configs/lang/{DR_option.language}.toml')
        return DR_option.language


if not __name__ == '__main__':
    tr = Lang()
else:
    tr_ = Tr()
