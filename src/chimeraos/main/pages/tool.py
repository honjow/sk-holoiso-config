#!/usr/bin/python
# coding=utf-8

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import gi
from component import ManagerItem
import installs

from utils import (
    check_decky_plugin_exists,
    check_service_exists,
)

from config import IS_HHD_SUPPORT, PRODUCT_NAME,USER,logging
from config import (
    PANED_RIGHT_MARGIN_START,
    PANED_RIGHT_MARGIN_END,
    PANED_RIGHT_MARGIN_TOP,
    PANED_RIGHT_MARGIN_BOTTOM,
)

class ToolManagerPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_margin_start(PANED_RIGHT_MARGIN_START)
        self.set_margin_end(PANED_RIGHT_MARGIN_END)
        self.set_margin_top(PANED_RIGHT_MARGIN_TOP)
        self.set_margin_bottom(PANED_RIGHT_MARGIN_BOTTOM)
        self.product_name = PRODUCT_NAME
        self.create_page()

    def create_page(self):
        item_decky = ManagerItem(
            "Decky",
            "游戏模式的插件平台",
            lambda: check_service_exists("plugin_loader.service"),
            installs.simple_decky_install,
        )
        self.pack_start(item_decky, False, False, 0)

        item_decky_cn = ManagerItem(
            "Decky(CN源)",
            "游戏模式的插件平台",
            lambda: check_service_exists("plugin_loader.service"),
            installs.simple_cn_decky_install,
        )
        self.pack_start(item_decky_cn, False, False, 0)

        item_handycon = ManagerItem(
            "HandyGCCS",
            "驱动部分掌机的手柄按钮",
            lambda: check_service_exists("handycon.service"),
            installs.handycon_install,
            installs.handycon_uninstall,
        )
        self.pack_start(item_handycon, False, False, 0)

        if IS_HHD_SUPPORT:
            item_hhd = ManagerItem(
                "HHD",
                "Handheld Daemon , 另一个手柄驱动程序",
                lambda: check_service_exists(f"hhd@{USER}.service"),
                installs.hhd_install,
                installs.hhd_install,
            )
            self.pack_start(item_hhd, False, False, 0)

            item_hhd_decky_bin = ManagerItem(
                "HHD Decky (直装)",
                "配合 HHD 使用, 直接安装版",
                lambda: check_decky_plugin_exists("hhd-decky-bin"),
                installs.power_control_bin_install,
                lambda: installs.remove_decky_plugin("hhd-decky-bin"),
            )
            self.pack_start(item_hhd_decky_bin, False, False, 0)

            item_hhd_decky = ManagerItem(
                "HHD Decky (编译版)",
                "配合 HHD 使用",
                lambda: check_decky_plugin_exists("hhd-decky"),
                installs.hhd_decky_install,
                lambda: installs.remove_decky_plugin("hhd-decky"),
            )
            self.pack_start(item_hhd_decky, False, False, 0)
        
        if self.product_name in (
            "ROG Ally RC71L_RC71L",
            "ROG Ally RC71L",
        ):
            item_spb_ally = ManagerItem(
                "SBP-ROG-Ally-Theme",
                "配合 HHD 使用的 CSS Loader 皮肤, 把模拟的 PS5 手柄按钮显示为 ROG Ally 的样式",
                installs.spb_ally_exist,
                installs.spb_ally_install,
                installs.spb_ally_uninstall,
            )
            self.pack_start(item_spb_ally, False, False, 0)

        if self.product_name in (
            "83E1",
        ):
            item_spb_lego = ManagerItem(
                "SBP-Legion-Go-Theme",
                "配合 HHD 使用的 CSS Loader 皮肤, 把模拟的 PS5 按钮显示为 Legion Go 的样式",
                installs.spb_lego_exist,
                installs.spb_lego_install,
                installs.spb_lego_uninstall,
            )
            self.pack_start(item_spb_lego, False, False, 0)

        if IS_HHD_SUPPORT:
            item_ps5_to_xbox = ManagerItem(
                "PS5-to-Xbox-glyphs",
                "配合 HHD 使用的 CSS Loader 皮肤, 把模拟的 PS5 手柄按钮显示为 Xbox 的样式",
                installs.ps5_to_xbox_exist,
                installs.ps5_to_xbox_install,
                installs.ps5_to_xbox_uninstall,
            )
            self.pack_start(item_ps5_to_xbox, False, False, 0)

        item_simple_decky_TDP = ManagerItem(
            "SimpleDeckyTDP",
            "掌机功耗性能管理 Decky插件, 只有 TDP 相关功能",
            lambda: check_decky_plugin_exists("SimpleDeckyTDP"),
            installs.simple_decky_TDP_install,
            lambda: installs.remove_decky_plugin("SimpleDeckyTDP"),
        )
        self.pack_start(item_simple_decky_TDP, False, False, 0)

        if self.product_name in (
            "AIR",
            "AIR 1S",
            "AIR Pro",
            "AYANEO 2",
            "GEEK",
            "AYANEO 2S",
            "GEEK 1S",
        ):
            item_ayaled = ManagerItem(
                "AYANEO LED",
                "AYANEO掌机LED灯控制Decky插件",
                lambda: check_decky_plugin_exists("ayaled"),
                installs.ayaled_install,
                lambda: installs.remove_decky_plugin("ayaled"),
            )
            self.pack_start(item_ayaled, False, False, 0)

        # Lenovo Legion Go
        if self.product_name == "83E1":
            item_LegionGoRemapper = ManagerItem(
                "LegionGoRemapper",
                "Lenovo Legion Go 手柄按键映射, 灯光控制 Decky 插件",
                lambda: check_decky_plugin_exists("LegionGoRemapper"),
                installs.LegionGoRemapper_install,
                lambda: installs.remove_decky_plugin("LegionGoRemapper"),
            )
            self.pack_start(item_LegionGoRemapper, False, False, 0)


        item_power_control_bin = ManagerItem(
            "PowerControl",
            "掌机功耗性能管理Decky插件, 直接安装版",
            lambda: check_decky_plugin_exists("PowerControl"),
            installs.power_control_bin_install,
            lambda: installs.remove_decky_plugin("PowerControl"),
        )
        self.pack_start(item_power_control_bin, False, False, 0)

        item_power_control = ManagerItem(
            "PowerControl (编译版)",
            "下载最新github源码编译安装",
            lambda: check_decky_plugin_exists("PowerControl"),
            installs.power_control_install,
            lambda: installs.remove_decky_plugin("PowerControl"),
        )
        self.pack_start(item_power_control, False, False, 0)

        # item_mango_peel = ManagerItem(
        #     "MangoPeel",
        #     "性能监测自定义Decky插件",
        #     lambda: check_decky_plugin_exists("MangoPeel"),
        #     installs.mango_peel_install,
        #     lambda: installs.remove_decky_plugin("MangoPeel"),
        # )
        # self.pack_start(item_mango_peel, False, False, 0)

        item_tomoon = ManagerItem(
            "ToMoon",
            "网络加速Decky插件",
            lambda: check_decky_plugin_exists("tomoon"),
            installs.tomoon_install,
            lambda: installs.remove_decky_plugin("tomoon"),
        )
        self.pack_start(item_tomoon, False, False, 0)
