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
import pprint

from Difficult_Rocket import translate


class SingleTextStyle:
    """
    单个字符的字体样式
    """

    def __init__(self,
                 font_name: str = '',
                 font_size: int = 15,
                 bold: bool = False,
                 italic: bool = False,
                 color: str = 'black',
                 text_tag: list = None,
                 show: bool = True,
                 text: str = ''):
        self.font_name = font_name
        self.font_size = font_size
        self.bold = bold
        self.italic = italic
        self.color = color
        if not text_tag:
            self._tag = []
        else:
            self._tag = text_tag
        self.show = show
        self.text = text

    @property
    def tag(self) -> list:
        return self._tag

    @tag.setter
    def tag(self, value: list):
        assert type(value) == list, 'SingleTextStyle.tag must be list'
        for tag in value:
            if tag not in self._tag:
                self._tag.append(tag)
        self._tag.sort()

    """
    对运算操作的支持
    """

    def __add__(self, other: 'SingleTextStyle') -> 'SingleTextStyle':
        """
        叠加两个字体样式 优先使用 other 的样式
        :param other: 叠加的字体样式
        :return: 叠加后的字体样式
        """
        assert type(other) == SingleTextStyle, f'SingleTextStyle + other\n other must be the same type, not a {type(other)}'
        return SingleTextStyle(
                font_name=other.font_name or self.font_name,
                font_size=other.font_size or self.font_size,
                bold=other.bold or self.bold,
                italic=other.italic or self.italic,
                color=other.color or self.color,
                text_tag=other.tag + self.tag,
                show=other.show or self.show,
                text=self.text
        )

    def __iadd__(self, other: 'SingleTextStyle') -> 'SingleTextStyle':
        """
        叠加两个字体样式 优先使用 other 的样式
        :param other: 叠加的字体样式
        :return: 叠加后的字体样式
        """
        assert type(other) == SingleTextStyle, f'SingleTextStyle += other\n other must be the same type, not a {type(other)}'
        self.font_name = other.font_name or self.font_name
        self.font_size = other.font_size or self.font_size
        self.bold = other.bold or self.bold
        self.italic = other.italic or self.italic
        self.color = other.color or self.color
        self.tag += other.tag
        self.show = other.show or self.show
        self.text = self.text
        return self

    """
    对各种判定的支持
    """

    def have_tag(self, other: 'SingleTextStyle') -> bool:
        """
        比较两个字体样式tag是否相同
        :param other: 叠加的字体样式
        :return: 是否相同
        """
        assert type(other) == SingleTextStyle
        return other.tag in self.tag

    def same_style(self, other: 'SingleTextStyle') -> bool:
        """
        比较两个字体样式是否相同
        :param other: 叠加的字体样式
        :return: 是否相同
        """
        assert type(other) == SingleTextStyle
        return (self.font_name == other.font_name and
                self.font_size == other.font_size and
                self.bold == other.bold and
                self.italic == other.italic and
                self.color == other.color and
                self.show == other.show)

    """
    自动输出一些属性的支持
    """

    def HTML_style_text(self) -> str:
        """
        输出字体样式的HTML代码
        :return: HTML代码
        """
        return f'<font name="{self.font_name}" real_size={self.font_size} bold={self.bold} italic={self.italic} color={self.color}>'


# [\u4e00-\u9fa5] 中文字符
default_fonts_config = [
    {
        'match': re.compile(r'.'),  # 匹配的字符  匹配选项是re.compile()
        'shown': re.compile(r'.'),  # 匹配到的字符中显示的部分  匹配选项是re.compile()
        'style': SingleTextStyle(font_name=translate.鸿蒙简体, font_size=15, bold=False, italic=False, show=True, color='black'),
    },
    {
        'match': re.compile(r'[a-zA-Z]'),
        'shown': re.compile(r'[a-zA-Z]'),
        'style': SingleTextStyle(font_name=translate.微软等宽)
    },
    # Markdown 语法规则匹配
    {
        # Markdown 粗体语法规则匹配
        'match': re.compile(r'\*\*(.*?(?<!\s))\*\*'),
        'shown': re.compile(r'(?<=\*\*)(.*?(?<!\s))(?=\*\*)'),
        'tag':   {
            # 为 match 匹配到的字符添加标签
            'match': re.compile(r'\*\*'),
            'style': SingleTextStyle(text_tag=['bold'])
        },
        'style': SingleTextStyle(bold=True)
    },
    {
        # Markdown 斜体语法规则匹配
        'match':  re.compile(r'\*(.*?(?<!\s))\*'),
        'shown':  re.compile(r'(?<=\*)(.*?(?<!\s))(?=\*)'),
        'ignore': {
            # 如果匹配到的字符含有 tag 就忽略本次解析
            'match': re.compile(r'\*'),
            'tag':   SingleTextStyle(text_tag=['italic'])
        },
        'style':  SingleTextStyle(italic=True)
    },
    {
        # Markdown 链接规则匹配
        # 注意：这里的匹配模式是非贪婪的，即匹配到的结果必须是完整的
        # 即：链接名称不能是空格等空白字符开头，链接名称不能是空格等空白字符结尾
        # 匹配的内容：[abc](def)
        # 显示的内容：abc
        'match': re.compile(r'\[(.*?(?<!\s))\]\((.*?(?<!\s))\)'),
        'shown': re.compile(r'(?<=\[)(.*?(?<!\s))(?=\]\((.*?(?<!\s))\))'),
        'style': SingleTextStyle(bold=True)
    }
]
font_HTML_end = '</font>'


def decode_text2HTML(text: str,
                     configs=None) -> str:
    if configs is None:
        configs = default_fonts_config
    style_list = [SingleTextStyle(text=text[x]) for x in range(0, len(text))]

    # 根据输入的配置对每一个字符进行样式设定
    for config in configs:
        # 根据 配置"文件"
        match_texts = config['match'].finditer(text)  # 使用config.match匹配
        for match_text in match_texts:  # 每一个匹配到的匹配项
            text_match = match_text.group()  # 缓存一下匹配到的字符，用于匹配显示的字符
            shown_texts = config['shown'].finditer(text_match)  # 使用config.shown匹配
            match_start = match_text.span()[0]
            match_end = match_text.span()[1]

            if 'ignore' in config:  # 如果样式选项包含忽略某些字符的tag
                ignore_texts = config['ignore']['match'].finditer(text_match)  # 根据选项匹配可能忽略的字符
                ignore = False  # 忽略先为False
                for ignore_text in ignore_texts:  # 每一个可能忽略的字符
                    if ignore:  # 为了方便退出
                        break
                    for ignore_index in range(match_start + ignore_text.span()[0], match_start + ignore_text.span()[1]):  # 对每一个可能的字符进行检测
                        if style_list[ignore_index].have_tag(config['ignore']['tag']):  # 如果确实包含要忽略的
                            ignore = True  # 忽略为True
                            break
                if ignore:
                    continue  # 跳过本次匹配

            if 'tag' in config:  # 如果样式选项包含对部分字符添加tag
                tag_texts = config['tag']['match'].finditer(text_match)  # 根据配置的正则表达式匹配要添加tag的字符
                for tag_text in tag_texts:  # 对每一个匹配到的~~~~~~
                    for tag_index in range(match_start + tag_text.span()[0], match_start + tag_text.span()[1]):  # 用于遍历匹配到的字符
                        style_list[tag_index] += config['tag']['style']

            # 为匹配到的字符添加样式
            for match_index in range(match_start, match_end):  # 用于遍历匹配到的字符
                # 这里用match index来精确读写列表里的元素，毕竟re.Match返回的span是两个标点，得遍历
                style_list[match_index] += config['style']  # 字体样式列表的[match_index] += config['style']的样式
                style_list[match_index].show = False  # 设置显示属性变为False


            # 为每一个显示的字符设置显示属性
            for shown_text in shown_texts:  # 每一个显示的匹配项
                for shown_index in range(match_start + shown_text.span()[0], match_start + shown_text.span()[1]):
                    style_list[shown_index].show = True
                    # 字体样式列表的[shown_index]设置显示属性变为True

    # 开始根据配置好的样式输出HTML文本
    style_list[0].text = style_list[0].HTML_style_text() + style_list[0].text if style_list[0].show else style_list[0].text
    # 样式列表里的第一个.text
    # 如果 (这个字符显示) = 第一个的HTML样式+第一个样式.text
    # 否则 = 第一个样式.text(其实pass最好)
    for style_index in range(1, len(style_list)):  # 从第二个开始的每一个样式
        if not style_list[style_index].same_style(style_list[style_index-1]):  # 如果这个字符的样式跟前一个不一样
            style_list[style_index-1].text += font_HTML_end  # 在前一个样式.text 的后面附加一个 </font>
            style_list[style_index].text = style_list[style_index].HTML_style_text() + style_list[style_index].text  # 在这个样式.text 的前面放一个HTML样式
    style_list[-1].text += font_HTML_end  # 样式表的最后一个样式后面附加一个 </font>

    # 输出最终的HTML文本
    formatted_HTML_text = ''  # 初始化一下
    for style in style_list:  # 每一个样式
        if style.show:  # 如果这个字符显示
            formatted_HTML_text += style.text  # 文本的后面附加一下
    return formatted_HTML_text  # 返回，DONE！
