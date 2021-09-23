#  -------------------------------
#  Difficult Rocket
#  Copyright © 2021 by shenjackyuanjie
#  All rights reserved
#  -------------------------------

"""
writen by shenjackyuanjie
mail:   3695888@qq.com
github: @shenjackyuanjie
gitee:  @shenjackyuanjie
"""

from typing import List

from Difficult_Rocket.api import tools
from Difficult_Rocket.api.Exp import *


class Lang:
    """
    用于创建一个对应语言的翻译类
    感谢Fallen的MCDR提供idea
    https://github.com/Fallen-Breath/MCDReforged
    可以用
    lang['language'] = 'abc' 或
    lang['lang'] = 'abc'
    的方式直接更改并刷新翻译
    """

    def __init__(self, language: str = 'zh-CN'):
        self.language = language
        self.翻译结果 = tools.config(f'configs/lang/{language}.json5')
        self.默认翻译 = tools.config('configs/lang/zh-CN.json5')

    def __str__(self) -> str:
        return self.language

    def __getitem__(self, item):
        try:
            return self.翻译结果[item]
        except KeyError:
            return self.默认翻译[item]

    def __setitem__(self, key, value):
        if key == 'language' or key == 'lang':
            try:
                self.翻译结果 = tools.config(f'configs/lang/{value}.json5')
                self.language = value
            except FileNotFoundError:
                raise LanguageError(f'{value}\'s language json5 file not found')
        else:
            raise NotImplementedError

    def set_language(self, language):
        try:
            self.翻译结果 = tools.config(f'configs/lang/{language}.json5')
            self.language = language
        except FileNotFoundError:
            raise LanguageError(f'{language}\'s language json5 file not found')


try:
    tr = Lang('zh-CN')
except FileNotFoundError:
    import os

    os.chdir('..')
    os.chdir('..')
    tr = Lang('zh-CN')


def test():
    print(tr)
    assert tr.language == 'zh-CN'