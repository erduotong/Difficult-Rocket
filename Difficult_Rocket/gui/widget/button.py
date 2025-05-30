#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
# ruff: noqa: E241, E261

from __future__ import annotations

import math
from typing import Tuple, Sequence
from dataclasses import dataclass, field
from enum import Enum

# from libs import pyglet
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA
from pyglet.graphics.shader import ShaderProgram
from pyglet.text import Label

from pyglet.shapes import ShapeBase, _rotate_point
from pyglet.gui.widgets import WidgetBase

from pyglet.graphics import Batch, Group

# from Difficult_Rocket import DR_status

RGBA = Tuple[int, int, int, int]


@dataclass
class OreuiShapeColors:
    # 这里都是 未按下的颜色
    # 外面一圈高光
    highlight: RGBA = (255, 255, 255, 255)
    # 边框
    border: RGBA = (0, 0, 0, 255)
    # 下巴
    down_pad: RGBA = (49, 50, 51, 255)
    # 左下角和右上角的重叠点
    corner: RGBA = (124, 124, 125, 255)
    # 左上拐角
    left_up: RGBA = (109, 109, 110, 255)
    # 右下拐角
    right_down: RGBA = (90, 91, 92, 255)
    # 内部填充
    inner: RGBA = (72, 73, 74, 255)

    def __eq__(self, other: object) -> bool:
        return (
            self.__class__ == other.__class__
            and self.highlight == other.highlight # pyright: ignore reportAttributeAccessIssue
            and self.border == other.border # pyright: ignore reportAttributeAccessIssue
            and self.down_pad == other.down_pad # pyright: ignore reportAttributeAccessIssue
            and self.corner == other.corner # pyright: ignore reportAttributeAccessIssue
            and self.left_up == other.left_up # pyright: ignore reportAttributeAccessIssue
            and self.right_down == other.right_down # pyright: ignore reportAttributeAccessIssue
            and self.inner == other.inner # pyright: ignore reportAttributeAccessIssue
        )

    @property
    def base_color(self) -> tuple[int, int, int, int]:
        return self.inner

    @base_color.setter
    def base_color(self, value: tuple[int, int, int, int]) -> None:
        self.inner = value


class OreuiButtonStyles(Enum):
    wiki_normal = OreuiShapeColors()
    wiki_press = OreuiShapeColors(
        corner=(106, 107, 108, 255),
        down_pad=(35, 35, 36, 255),
        left_up=(90, 91, 92, 255),
        right_down=(70, 71, 71, 255),
        inner=(49, 50, 51, 255),
    )
    game1_normal = OreuiShapeColors(
        border=(30, 30, 31, 255),
        corner=(253, 253, 254, 255),
        down_pad=(88, 88, 90, 255),
        left_up=(251, 251, 253, 255),
        right_down=(248, 250, 251, 255),
        inner=(244, 246, 249, 255),
    )
    game1_select = OreuiShapeColors(
        border=(30, 30, 31, 255),
        corner=(244, 244, 245, 255),
        down_pad=(88, 88, 90, 255),
        left_up=(236, 237, 238, 255),
        right_down=(227, 227, 229, 255),
        inner=(208, 209, 212, 255),
    )
    game1_press = OreuiShapeColors(
        border=(30, 30, 31, 255),
        corner=(236, 236, 237, 255),
        down_pad=(110, 111, 114, 255),
        left_up=(224, 224, 225, 255),
        right_down=(208, 209, 211, 255),
        inner=(177, 178, 181, 255),
    )
    game2_normal = OreuiShapeColors(
        border=(30, 30, 31, 255),
        corner=(131, 190, 109, 255),
        down_pad=(29, 77, 19, 255),
        left_up=(1117, 183, 93, 255),
        right_down=(99, 174, 73, 255),
        inner=(82, 165, 53, 255),
    )
    game2_select = OreuiShapeColors(
        border=(30, 30, 31, 255),
        corner=(114, 167, 99, 255),
        down_pad=(29, 77, 19, 255),
        left_up=(99, 157, 82, 255),
        right_down=(79, 145, 60, 255),
        inner=(60, 133, 39, 255),
    )
    game2_press = OreuiShapeColors(
        border=(30, 30, 31, 255),
        corner=(102, 143, 91, 255),
        down_pad=(14, 77, 3, 255),
        left_up=(85, 131, 73, 255),
        right_down=(63, 115, 50, 255),
        inner=(42, 100, 28, 255),
    )


@dataclass
class OreuiButtonStatus:
    popout: bool = False
    highlight: bool = False
    pad: float = 2
    down_pad: float = 5
    colors: OreuiShapeColors = field(default_factory=OreuiShapeColors)

    def __eq__(self, value: object) -> bool:
        return (
            self.__class__ == value.__class__
            and self.popout == value.popout # pyright: ignore reportAttributeAccessIssue
            and self.highlight == value.highlight # pyright: ignore reportAttributeAccessIssue
            and self.pad == value.pad # pyright: ignore reportAttributeAccessIssue
            and self.down_pad == value.down_pad # pyright: ignore reportAttributeAccessIssue
            and self.colors == value.colors # pyright: ignore reportAttributeAccessIssue
        )

    @property
    def pad2x(self) -> float:
        return self.pad * 2

    @pad2x.setter
    def pad2x(self, value: float) -> None:
        self.pad = value / 2

    def real_down_pad(self) -> float:
        return self.down_pad if self.popout else 0.0


class OreuiShape(ShapeBase):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        pad: float = 2,
        down_pad: float = 5.0,
        pop_out: bool = True,
        highlight: bool = False,
        colors: OreuiShapeColors | None = None,
        blend_src: int = GL_SRC_ALPHA,
        blend_dest: int = GL_ONE_MINUS_SRC_ALPHA,
        batch: Batch | None = None,
        group: Group | None = None,
        program: ShaderProgram | None = None,
    ):
        self._x = x
        self._y = y
        self._z = 0.0
        self._width = width
        self._height = height
        self._pad = pad
        self._down_pad = down_pad
        self._pop_out = pop_out
        self._highlight = highlight
        self._colors = colors or OreuiButtonStyles.wiki_normal.value

        vertex = 32
        if pop_out:
            vertex += 4
        super().__init__(vertex, blend_src, blend_dest, batch, group, program)

    @property
    def pop_out(self) -> bool:
        return self._pop_out

    @property
    def pad(self) -> float:
        return self._pad

    @property
    def down_pad(self) -> float:
        return self._down_pad

    @property
    def color(self) -> tuple[int, int, int, int]:
        return self._colors.base_color

    @property
    def colors(self) -> OreuiShapeColors:
        return self._colors

    @property
    def highlight(self) -> bool:
        return self._highlight

    @pop_out.setter
    def pop_out(self, value: bool) -> None:
        self._pop_out = value
        self._create_vertex_list()

    @pad.setter
    def pad(self, value: float) -> None:
        self._pad = value
        self._update_vertices()

    @down_pad.setter
    def down_pad(self, value: float) -> None:
        self._down_pad = value
        self._update_vertices()

    @color.setter
    def color(self, values: tuple[int, int, int, int] | tuple[int, int, int]) -> None:
        if len(values) == 3:
            values = values + (255,)
        self._colors.base_color = values
        self._update_color()

    @colors.setter
    def colors(self, value: OreuiShapeColors) -> None:
        self._colors = value
        self._update_color()

    @highlight.setter
    def highlight(self, value: bool) -> None:
        self._highlight = value
        self._create_vertex_list()

    def update_with_status(self, status: OreuiButtonStatus):
        assert isinstance(status, OreuiButtonStatus)
        update_vertex = False
        if status.popout != self._pop_out:
            self._pop_out = status.popout
            update_vertex = True
        if status.highlight != self._highlight:
            self._highlight = status.highlight
            update_vertex = True
        if status.pad != self._pad:
            self._pad = status.pad
            update_vertex = True
        if status.down_pad != self._down_pad:
            self._down_pad = status.down_pad
            update_vertex = True
        if status.colors != self._colors:
            self.colors = status.colors
        if update_vertex:
            self._create_vertex_list()

    def _update_color(self) -> None:
        if self._pop_out:
            colors = (
                self._colors.border * 4
                + self._colors.down_pad * 4
                + self._colors.corner * 8
                + self._colors.right_down * 6
                + self._colors.left_up * 6
                + self._colors.inner * 4
                + self._colors.highlight * 4
            )
        else:
            colors = (
                self._colors.border * 4
                + self._colors.corner * 8
                + self._colors.right_down * 6
                + self._colors.left_up * 6
                + self._colors.inner * 4
                + self._colors.highlight * 4
            )
        self._vertex_list.colors[:] = colors

    def __contains__(self, point: tuple[float, float]) -> bool:
        assert len(point) == 2
        point = _rotate_point((self._x, self._y), point, math.radians(self._rotation))
        x, y = self._x - self._anchor_x, self._y - self._anchor_y
        return x < point[0] < x + self._width and y < point[1] < y + self._height

    def _get_vertices(self) -> Sequence[float]:
        if not self._visible:
            return (0, 0) * self._num_verts

        left = -self._anchor_x
        right = left + self._width
        bottom = -self.anchor_y
        top = bottom + self._height

        pad = self._pad
        down_pad = self._down_pad

        in_left = left + pad
        i_right = right - pad
        in_bottom = bottom + pad
        inner_top = top - pad
        """
        pop out ( 默认的弹出状态 )
        20 顶点 (还有外面一圈高光)
        3                        2
            18          15   14
                 19     16   17

            11   10     13
            7    9           6
            4                5
        0                        1
        unpop
        16 顶点
        3                       2
            7          15   6
                13     12   14

            10   9     11
            4    8          5
        0                       1
        """
        # fmt: off
        out_border = [
            left,  bottom, # 0
            right, bottom, # 1
            right, top,    # 2
            left,  top,    # 3
        ]
        if self._highlight:
            highlight = [
                left - pad,  bottom - pad, # max+1
                right + pad, bottom - pad, # max+2
                right + pad, top + pad,    # max+3
                left - pad,  top + pad,    # max+4
            ]
        else:
            highlight = [0, 0, 0, 0, 0, 0, 0, 0]
        if self._pop_out:
            down_top = in_bottom + down_pad
            # 底下那个下巴
            down_part = [
                in_left, in_bottom, # 4
                i_right, in_bottom, # 5
                i_right, down_top,  # 6
                in_left, down_top,  # 7
            ]
            # 左下角的小方块
            left_down = [
                in_left,       down_top,        # 8
                in_left + pad, down_top,        # 9
                in_left + pad, down_top + pad,  # 10
                in_left,       down_top + pad,  # 11
            ]
            # 右上角的小方块
            right_up = [
                i_right - pad, inner_top - pad, # 12
                i_right,       inner_top - pad, # 13
                i_right,       inner_top,       # 14
                i_right - pad, inner_top,       # 15
            ]
            # 左上的拐弯条
            # 1   2
            #   4 3
            # 0 5
            left_up = [
                in_left,       down_top + pad,  # 16
                in_left,       inner_top,       # 17
                i_right - pad, inner_top,       # 18
                i_right - pad, inner_top - pad, # 19
                in_left + pad, inner_top - pad, # 20
                in_left + pad, down_top + pad,  # 21
            ]
            # 右下的拐弯条
            #   3 2
            # 5 4
            # 0   1
            right_down = [
                in_left + pad, down_top,        # 22
                i_right,       down_top,        # 23
                i_right,       inner_top - pad, # 24
                i_right - pad, inner_top - pad, # 25
                i_right - pad, down_top + pad,  # 26
                in_left + pad, down_top + pad,  # 27
            ]
            # 中间的方块
            inner_box = [
                in_left + pad, down_top + pad,  # 28
                i_right - pad, down_top + pad,  # 29
                i_right - pad, inner_top - pad, # 30
                in_left + pad, inner_top - pad, # 31
            ]
            return (out_border +
                    down_part +
                    left_down + right_up +
                    left_up + right_down +
                    inner_box +
                    highlight)
        else:
            # 左下角的小方块
            left_down = [
                in_left,       in_bottom,       # 4
                in_left + pad, in_bottom,       # 5
                in_left + pad, in_bottom + pad, # 6
                in_left,       in_bottom + pad, # 7
            ]
            # 右上角的小方块
            right_up = [
                i_right - pad, inner_top - pad, # 8
                i_right,       inner_top - pad, # 9
                i_right,       inner_top,       # 10
                i_right - pad, inner_top,       # 11
            ]
            # 左上的拐弯条
            # 1   2
            #   4 3
            # 0 5
            left_up = [
                in_left,       in_bottom + pad,  # 12
                in_left,       inner_top,        # 13
                i_right - pad, inner_top,        # 14
                i_right - pad, inner_top - pad,  # 15
                in_left + pad, inner_top - pad,  # 16
                in_left + pad, in_bottom + pad,  # 17
            ]
            # 右下的拐弯条
            #   3 2
            # 5 4
            # 0   1
            right_down = [
                in_left + pad, in_bottom,        # 18
                i_right,       in_bottom,        # 19
                i_right,       inner_top - pad,  # 20
                i_right - pad, inner_top - pad,  # 21
                i_right - pad, in_bottom + pad,  # 22
                in_left + pad, in_bottom + pad,  # 23
            ]
            # 中间的方块
            inner_box = [
                in_left + pad, in_bottom + pad,  # 24
                i_right - pad, in_bottom + pad,  # 25
                i_right - pad, inner_top - pad,  # 26
                in_left + pad, inner_top - pad,  # 27
            ]
            return (out_border +
                    left_down + right_up +
                    left_up + right_down +
                    inner_box +
                    highlight)
        # fmt: on

    def _create_vertex_list(self) -> None:
        if self._vertex_list:
            self._vertex_list.delete()
        colors = self._colors.border * 4
        # fmt: off
        indices = [
            0, 1, 2, # 最基本的两个三角形
            0, 2, 3, # 用来画黑色边框
        ]
        if self._pop_out:
            indices += [4, 5, 6, 4, 6, 7]  # 下巴
            indices += [8, 9, 10, 8, 10, 11]  # 左下角
            indices += [12, 13, 14, 12, 14, 15]  # 右上角
            indices += [16, 17, 20, 16, 20, 21,
                        18, 19, 20, 18, 17, 20]  # 左上拐弯
            indices += [22, 23, 26, 22, 26, 27,
                        23, 24, 26, 24, 25, 26]  # 右下拐弯
            indices += [28, 29, 30, 28, 30, 31]  # 中间的方块
            if self._highlight:
                indices = [32, 33, 34, 32, 34, 35] + indices  # 高光
            colors += (
                self._colors.down_pad * 4
                + self._colors.corner * 8
                + self._colors.right_down * 6
                + self._colors.left_up * 6
                + self._colors.inner * 4
                + self._colors.highlight * 4
            )
            self._num_verts = 36
        else:
            indices += [4, 5, 6, 4, 6, 7]  # 左下角
            indices += [8, 9, 10, 8, 10, 11]  # 右上角
            indices += [12, 16, 17, 12, 13, 16,
                        14, 15, 16, 14, 13, 16]  # 左上拐弯
            indices += [18, 22, 23, 18, 19, 22,
                        20, 21, 22, 20, 19, 22]  # 右下拐弯
            indices += [24, 25, 26, 24, 26, 27]
            if self._highlight:
                indices = [28, 29, 30, 28, 30, 31] + indices  # 高光
            colors += (
                self._colors.corner * 8
                + self._colors.right_down * 6
                + self._colors.left_up * 6
                + self._colors.inner * 4
                + self._colors.highlight * 4
            )
            self._num_verts = 32
        # fmt: on
        self._vertex_list = self._program.vertex_list_indexed(
            self._num_verts,
            self._draw_mode,
            indices,
            self._batch,
            self._group,
            position=("f", self._get_vertices()),
            colors=("Bn", colors),
            translation=("f", (self._x, self._y) * self._num_verts),
        )

    def _update_vertices(self) -> None:
        self._vertex_list.position[:] = self._get_vertices()


class 拐角(ShapeBase):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        thick1: float = 1.0,
        thick2: float = 1.0,
        color: tuple[int, int, int, int] = (255, 255, 255, 255),
        clockwise: bool = True,
        blend_src: int = GL_SRC_ALPHA,
        blend_dest: int = GL_ONE_MINUS_SRC_ALPHA,
        batch: Batch | None = None,
        group: Group | None = None,
        program: ShaderProgram | None = None,
    ) -> None:
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._thick1 = thick1
        self._thick2 = thick2
        self._clockwise = clockwise

        self._rgba = color
        super().__init__(6, blend_src, blend_dest, batch, group, program)

    def __contains__(self, point: tuple[float, float]) -> bool:
        assert len(point) == 2
        # 先大框
        point = _rotate_point((self._x, self._y), point, math.radians(self._rotation))
        x, y = self._x - self._anchor_x, self._y - self._anchor_y
        return (x < point[0] < x + self._width and y < point[1] < y + self._height) and (
            (
                (point[1] > y + self._height - self._thick2)
                or (point[0] < x + self._thick1)
            )
            if self._clockwise
            else (
                (point[1] < y + self._thick1)
                or (point[0] > x + self._width - self._thick2)
            )
        )

    def _get_vertices(self) -> Sequence[float]:
        if not self.visible:
            return (0, 0) * self._num_verts

        t1, t2 = self._thick1, self._thick2
        left = -self._anchor_x
        bottom = -self._anchor_y
        right = left + self._width
        top = bottom + self._height

        x1 = left
        x2 = left + t1
        x3 = right - t1
        x4 = right
        y1 = bottom
        y2 = bottom + t1
        y3 = top - t2
        y4 = top

        # fmt: off
        return ([
                x1, y1,
                x1, y4,
                x4, y4,
                x4, y3,
                x2, y3,
                x2, y1
            ] if self._clockwise else [
                x1, y1,
                x4, y1,
                x4, y4,
                x3, y4,
                x3, y2,
                x1, y2
            ])
        # fmt: on

    def _update_color(self) -> None:
        self._vertex_list.colors[:] = self._rgba * self._num_verts

    def _update_vertices(self) -> None:
        self._vertex_list.position[:] = self._get_vertices()  # pyright: ignore reportAttributeAccessIssue

    def _create_vertex_list(self) -> None:
        # 1   2
        #   4 3
        # 0 5
        # or
        #   3 2
        # 5 4
        # 0   1
        # fmt: off
        groups = [
            1, 2, 3,
            1, 3, 4,
            1, 4, 5,
            1, 5, 0,
        ]
        # fmt: on
        self._vertex_list = self._program.vertex_list_indexed(
            self._num_verts,
            self._draw_mode,
            groups,
            self._batch,  # pyright: ignore reportArgumentType
            self._group,  # pyright: ignore reportArgumentType
            position=("f", self._get_vertices()),
            colors=("Bn", self._rgba * self._num_verts),
            translation=("f", (self._x, self._y) * self._num_verts),
        )

    @property
    def thick1(self) -> float:
        return self._thick1

    @property
    def thick2(self) -> float:
        return self.thick2

    @property
    def thickness(self) -> float:
        return self._thick1

    @thickness.setter
    def thickness(self, value: float):
        self._thick1 = value
        self._thick2 = value
        self._update_vertices()

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self.height

    @property
    def clockwise(self) -> bool:
        return self._clockwise

    @thick1.setter
    def thick1(self, value: float):
        self._thick1 = value
        self._update_vertices()

    @thick2.setter
    def thick2(self, value: float):
        self._thick2 = value
        self._update_vertices()

    @width.setter
    def width(self, value: float):
        self._width = value
        self._update_vertices()

    @height.setter
    def height(self, value: float):
        self._height = value
        self._update_vertices()

    @clockwise.setter
    def clockwise(self, value: bool):
        self._clockwise = bool(value)
        self._update_vertices()


class OreuiSlider(WidgetBase):
    """Oreui 的滑条"""


class OreuiButton(WidgetBase):
    """Oreui 的按钮!"""
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int = 30,
        text: str = "",
        normal: OreuiButtonStatus | None = None,
        select: OreuiButtonStatus | None = None,
        press: OreuiButtonStatus | None = None,
        toggle_mode: bool = True,
        auto_release: bool = True,
        batch: Batch | None = None,
        group: Group | None = None,
    ) -> None:
        """
        :param x: x 坐标
        :param y: y 坐标
        :param width: 宽度
        :param height: 高度
        :param text: 按钮上的文字
        :param normal: 正常状态
        :param select: 选中状态
        :param press: 按下状态
        :param toggle_mode: 是否为切换模式
        :param auto_release: 是否自动释放(如果你只是用来显示一个状态, 那就改成 False)
        :param batch: Batch
        :param group: Group
        """
        super().__init__(x, y, width, height)
        self._visible = True
        self._pressed = False
        self._selected = False
        self._auto_release = auto_release
        self.toggle_mode = toggle_mode
        self.main_batch = batch or Batch()
        self.main_group = group or Group()
        self._normal_status = normal or OreuiButtonStatus(popout=True)
        self._select_status = select or OreuiButtonStatus(highlight=True, popout=True)
        self._press_status = press or OreuiButtonStatus(popout=False, highlight=True)
        self._shape = OreuiShape(
            x=self._x,
            y=self._y,
            width=self._width,
            height=self._height,
            pop_out=self.current_status.popout,
            highlight=self.current_status.highlight,
            colors=self.current_status.colors,
            batch=self.main_batch,
            group=self.main_group,
        )
        self._text = text
        self._label = Label(
            text=text,
            x=round(x + self._width / 2),
            y=self._y + self.current_status.pad2x + self.current_status.real_down_pad(),
            width=width,
            height=height
            + 3
            - self.current_status.pad2x * 2
            - self.current_status.real_down_pad(), # pyright: ignore reportArgumentType
            anchor_x="center",
            anchor_y="bottom",
            font_size=12,
            batch=self.main_batch,
            group=self.main_group,
        )

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        self._visible = value
        self._shape.visible = value

    @property
    def current_status(self) -> OreuiButtonStatus:
        if self._pressed:
            return self._press_status
        if self._selected:
            return self._select_status
        return self._normal_status

    @current_status.setter
    def current_status(self, value: OreuiButtonStatus) -> None:
        self._shape.update_with_status(value)
        # 然后替换对应的状态
        if self._pressed:
            self._press_status = value
        elif self._selected:
            self._select_status = value
        else:
            self._normal_status = value

    @property
    def value(self) -> str:
        return self._text

    @value.setter
    def value(self, value: str) -> None:
        self._text = value
        self._label.text = value

    @property
    def label(self) -> Label:
        return self._label

    @property
    def shape(self) -> OreuiShape:
        return self._shape

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value
        self._shape.width = value
        self._label.width = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = value
        self._shape.height = (
            value
            + 3
            - self.current_status.pad2x * 2
            - self.current_status.real_down_pad()
        )
        self._label.height = value

    def _update_label_position(self) -> None:
        self._label.position = (
            round(self._x + self._width / 2),
            self._y + self.current_status.pad2x + self.current_status.real_down_pad(),
            0,
        )

    def _update_position(self) -> None:
        self._shape.position = (self._x, self._y)
        self._update_label_position()

    def _update_shape_status(self, status: OreuiButtonStatus) -> None:
        current_pop_out = self._shape._pop_out
        self._shape.update_with_status(status)
        if current_pop_out != self._shape._pop_out:
            self._update_label_position()

    def __contains__(self, pos: tuple[float, float]) -> bool:
        return self._check_hit(pos[0], pos[1])

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        if not self._enabled or self._pressed:
            return
        if (x, y) in self:
            if not self._selected:  # 没抬手/没选中
                self._selected = True
                self._update_shape_status(self._select_status)
                self.dispatch_event("on_select", x, y)
        elif self._selected:
            self._selected = False
            self._update_shape_status(self._normal_status)
            self.dispatch_event("on_deselect", x, y)

    def on_mouse_leave(self, x: int, y: int) -> None:
        if not self._enabled or self._pressed:
            return
        if self._selected:
            # 没抬手, 但是鼠标跑了
            self._selected = False
            if not self.toggle_mode and self._auto_release:
                self._update_shape_status(self._normal_status)
                self.dispatch_event("on_release", x, y)

    def on_mouse_press(self, x: int, y: int, buttons: int, modifiers: int) -> bool:
        """返回是否点击到了按钮"""
        if not self._enabled:
            return False
        if (x, y) in self:
            if self.toggle_mode:
                self._pressed = not self._pressed
                self._selected = True  # 顺便用来标记有没有抬手
                if self._pressed:
                    self._update_shape_status(self._press_status)
                    self.dispatch_event("on_press", x, y, buttons, modifiers)
                else:
                    self._update_shape_status(self._select_status)
                    self.dispatch_event("on_release", x, y)
                self.dispatch_event("on_toggle", x, y, buttons, modifiers)
                return True
            else:
                self._pressed = True
                self._selected = True  # 顺便用来标记有没有抬手
                self._update_shape_status(self._press_status)
                self.dispatch_event("on_press", x, y, buttons, modifiers)
                return True
        return False

    def on_mouse_release(self, x: int, y: int, buttons: int, modifiers: int) -> bool:
        """返回是否点击到了按钮"""
        if not self._enabled:
            return False
        if self._pressed:
            self._selected = False  # 抬手了
            if not self.toggle_mode and self._auto_release:
                # 非切换模式, 自动释放
                self._pressed = False
                if (x, y) in self:
                    self._update_shape_status(self._select_status)
                else:
                    self._update_shape_status(self._normal_status)
                self.dispatch_event("on_release", x, y)
            return True
        return False


OreuiButton.register_event_type("on_press")
OreuiButton.register_event_type("on_release")
OreuiButton.register_event_type("on_toggle")
OreuiButton.register_event_type("on_select")
OreuiButton.register_event_type("on_deselect")
