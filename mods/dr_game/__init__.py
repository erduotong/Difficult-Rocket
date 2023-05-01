#  -------------------------------
#  Difficult Rocket Mod
#  Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
#  All rights reserved
#  -------------------------------

import warnings
import traceback

from typing import Optional


from libs.MCDR.version import Version
from Difficult_Rocket.main import Game
from Difficult_Rocket.api.mod import ModInfo
from Difficult_Rocket.api.types import Options
from Difficult_Rocket.client import ClientWindow

DR_rust_version = Version("0.2.6.2")  # DR_mod 的 Rust 编写部分的兼容版本


class _DR_mod_runtime(Options):

    use_DR_rust: bool = True
    DR_rust_available: bool = False
    DR_rust_version: Version = DR_rust_version
    DR_rust_get_version: Optional[Version] = None

    def init(self, **kwargs) -> None:
        try:
            from libs.Difficult_Rocket_rs import get_version_str
            self.DR_rust_get_version = Version(get_version_str())
            self.DR_rust_available = True
            if self.DR_rust_get_version != self.DR_rust_version:
                relationship = 'larger' if self.DR_rust_version > self.DR_rust_version else 'smaller'
                warnings.warn(f'DR_rust builtin version is {self.DR_rust_version} but true version is {get_version_str()}.\n'
                              f'Builtin version {relationship} than true version')
            self.use_DR_rust = self.use_DR_rust and self.DR_rust_available
        except ImportError as e:
            traceback.print_exc()
            self.DR_rust_available = False
            self.use_DR_rust = False
        self.flush_option()


DR_mod_runtime = _DR_mod_runtime()


class DR_mod(ModInfo):

    mod_id = "difficult_rocket_mod"
    name = "Difficult Rocket mod"
    version = Version("0.7.2.2")

    writer = "shenjackyuanjie"
    link = "shenjack.top"
    description = "Difficult Rocket mod (where the game implement)"
    info = "Difficult Rocket mod (where the game implement)"

    config = DR_mod_runtime

    # DR_version =  # DR SDK 兼容版本
    # 反正是内置 mod 跟着最新版本的 DR 走就行了
    # DR_Api_version =   # DR Api版本
    # 同理 不管 API 版本   这东西要是不兼容了才是大问题

    def on_load(self, game: Game, old_self: Optional["DR_mod"] = None):
        if old_self:
            game.client.window.add_sub_screen("SR1_ship", old_self.screen)
        else:
            self.config.flush_option()

    def on_client_start(self, game: Game, client: ClientWindow):
        from .sr1_ship import SR1ShipRender
        self.screen = SR1ShipRender
        print('DR_mod: on_client_start')
        client.add_sub_screen("SR1_ship", SR1ShipRender)


mod_class = DR_mod
