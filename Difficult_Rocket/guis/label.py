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

import re
from typing import Dict, List

from Difficult_Rocket import translate

from libs.pyglet.text import DocumentLabel


class FontsLabel(DocumentLabel):
    """
    一个基于HTMLLabel的 可以同时在一行字里面显示多种字体的 Label
    """

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self._text = 'a'
        self.formatted_text = 'a'
