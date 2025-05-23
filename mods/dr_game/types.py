#  -------------------------------
#  Difficult Rocket
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------
from __future__ import annotations

import math
from typing import Dict, Union

# pyglet
from pyglet.image import load, AbstractImage

# Difficult Rocket
from Difficult_Rocket.api.types import Options


class SR1Textures(Options):
    """存储 sr1 的材质 img"""

    def load_file(self, **kwargs):
        for image_name in self.flush_option():
            img = load(f"assets/textures/parts/{image_name}.png")
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2
            setattr(self, image_name, img)
        self.flush_option()
        return True

    def get_texture(self, name: str) -> AbstractImage:
        """
        获取材质
        :param name:
        :return:
        """
        self.cached_options: dict[str, AbstractImage]
        if name in self.cached_options:
            return self.cached_options[name]
        elif name.split(".")[0] in self.cached_options:
            return self.cached_options[name.split(".")[0]]
        else:
            img = load(f"assets/textures/parts/{name}")
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2
            setattr(self, name, img)
            return img

    Battery: AbstractImage = None
    Beam: AbstractImage = None
    CoverBottom: AbstractImage = None
    CoverStretch: AbstractImage = None
    CoverTop: AbstractImage = None
    DetacherRadial: AbstractImage = None
    DetacherVertical: AbstractImage = None
    DockingConnector: AbstractImage = None
    DockingPort: AbstractImage = None
    EngineIon: AbstractImage = None
    EngineLarge: AbstractImage = None
    EngineMedium: AbstractImage = None
    EngineSmall: AbstractImage = None
    EngineTiny: AbstractImage = None
    Fuselage: AbstractImage = None
    LanderLegJoint: AbstractImage = None
    LanderLegLower: AbstractImage = None
    LanderLegPreview: AbstractImage = None
    LanderLegUpper: AbstractImage = None
    NoseCone: AbstractImage = None
    Parachute: AbstractImage = None
    ParachuteCanister: AbstractImage = None
    ParachuteCanisterSide: AbstractImage = None
    Pod: AbstractImage = None
    Puffy750: AbstractImage = None
    RcsBlock: AbstractImage = None
    SideTank: AbstractImage = None
    SolarPanel: AbstractImage = None
    SolarPanelBase: AbstractImage = None
    SolidRocketBooster: AbstractImage = None
    TankLarge: AbstractImage = None
    TankMedium: AbstractImage = None
    TankSmall: AbstractImage = None
    TankTiny: AbstractImage = None
    Wheel: AbstractImage = None
    Wing: AbstractImage = None


class SR1PartTexture:
    part_type_sprite: Dict[str, str] = {
        "pod-1": "Pod",
        "detacher-1": "DetacherVertical",
        "detacher-2": "DetacherRadial",
        "wheel-1": "Wheel",
        "wheel-2": "Wheel",
        "fuselage-1": "Fuselage",
        "strut-1": "Beam",
        "fueltank-0": "TankTiny",
        "fueltank-1": "TankSmall",
        "fueltank-2": "TankMedium",
        "fueltank-3": "TankLarge",
        "fueltank-4": "Puffy750",
        "fueltank-5": "SideTank",
        "engine-0": "EngineTiny",
        "engine-1": "EngineSmall",
        "engine-2": "EngineMedium",
        "engine-3": "EngineLarge",
        "engine-4": "SolidRocketBooster",
        "ion-0": "EngineIon",
        "parachute-1": "ParachuteCanister",
        "nosecone-1": "NoseCone",
        "rcs-1": "RcsBlock",
        "solar-1": "SolarPanelBase",
        "battery-0": "Battery",
        "dock-1": "DockingConnector",
        "port-1": "DockingPort",
        "lander-1": "LanderLegPreview",
    }

    @classmethod
    def get_textures_from_type(cls, name: str) -> Union[None, str]:
        return None if name not in cls.part_type_sprite else cls.part_type_sprite[name]


class SR1Rotation(Options):
    radian_angle_map: Dict[float, float] = {
        0.0: 0,
        1.570796: 270,
        3.141593: 180,
        4.712389: 90,
    }

    @classmethod
    def get_rotation(cls, radian: float) -> float:
        """
        实际上就是将弧度转换为角度 (同时自带一个映射表)
        :param radian:
        :return:
        """
        if radian in cls.radian_angle_map:
            return cls.radian_angle_map[radian]
        else:
            return (radian / math.pi) * 180
