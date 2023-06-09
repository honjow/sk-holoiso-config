#!/usr/bin/python
# coding=utf-8

import gi
import threading

gi.require_version("Gtk", "3.0")
import threading
from gi.repository import GLib, Gtk, Pango


class SwitchItem(Gtk.Box):
    def __init__(self, title, description, initial_value=False, callback=None):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.set_margin_start(2)
        self.set_margin_end(2)
        self.set_margin_top(10)
        self.set_margin_bottom(10)

        self.callback = callback
        self.last_value = initial_value

        # 左边文字部分
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.pack_start(left_box, True, True, 0)

        switch_label = Gtk.Label()
        switch_label.set_text(title)
        switch_label.set_halign(Gtk.Align.START)
        switch_label.set_valign(Gtk.Align.START)
        left_box.pack_start(switch_label, False, False, 0)

        desc_label = Gtk.Label()
        desc_label.set_text(description)
        desc_label.set_halign(Gtk.Align.START)
        desc_label.set_valign(Gtk.Align.START)
        desc_label.set_xalign(0)
        desc_label.set_yalign(0)
        desc_label.set_line_wrap(True)
        desc_label.set_line_wrap_mode(Pango.WrapMode.WORD)
        desc_label.set_ellipsize(Pango.EllipsizeMode.NONE)
        desc_label.set_markup("<small>" + desc_label.get_text() + "</small>")
        left_box.pack_start(desc_label, False, False, 0)

        # 右边开关部分
        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER
        # switch.set_size_request(80, 40)
        switch.connect("notify::active", self.on_switch_activated)
        switch.set_active(initial_value)
        switch_box = Gtk.Box()
        switch_box.set_margin_start(10)
        switch_box.set_valign(Gtk.Align.CENTER)
        switch_box.pack_start(switch, False, False, 0)
        self.pack_end(switch_box, False, False, 0)

    def on_switch_activated(self, switch, gparam):
        active = switch.get_active()
        if self.callback and active != self.last_value:
            self.callback(active)
            self.last_value = active


class ManagerItem(Gtk.Box):
    def __init__(self, title, description, installed_cb, install_callback=None, uninstall_callback=None):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.set_margin_start(2)
        self.set_margin_end(2)
        self.set_margin_top(10)
        self.set_margin_bottom(10)

        self.title = title
        self.install_callback = install_callback
        self.uninstall_callback = uninstall_callback
        self.install_button = None
        self.uninstall_button = None
        
        self.installed_cb = installed_cb

        if callable(self.installed_cb):
            self.current_installed = self.installed_cb()
        else:
            self.current_installed = self.installed_cb

        # print ("{} current_installed: {}".format(self.title, self.current_installed))

        # 左边文字部分
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.pack_start(left_box, True, True, 0)

        switch_label = Gtk.Label()
        switch_label.set_text(title)
        switch_label.set_halign(Gtk.Align.START)
        switch_label.set_valign(Gtk.Align.START)
        left_box.pack_start(switch_label, False, False, 0)

        desc_label = Gtk.Label()
        desc_label.set_text(description)
        desc_label.set_halign(Gtk.Align.START)
        desc_label.set_valign(Gtk.Align.START)
        desc_label.set_xalign(0)
        desc_label.set_yalign(0)
        desc_label.set_line_wrap(True)
        desc_label.set_line_wrap_mode(Pango.WrapMode.WORD)
        desc_label.set_ellipsize(Pango.EllipsizeMode.NONE)
        desc_label.set_markup("<small>" + desc_label.get_text() + "</small>")
        left_box.pack_start(desc_label, False, False, 0)

        self.spinner = Gtk.Spinner()
        self.spinner.set_valign(Gtk.Align.CENTER)
        self.spinner.set_margin_end(10)
        self.pack_start(self.spinner, False, False, 0)

        # 右边按钮部分
        if self.uninstall_callback is not None:
            self.uninstall_button = Gtk.Button()
            self.uninstall_button.set_margin_end(10)
            self.uninstall_button.set_label("卸载")
            self.uninstall_button.set_valign(Gtk.Align.CENTER)
            self.uninstall_button.connect("clicked", self.on_uninstall_clicked)
            self.pack_start(self.uninstall_button, False, False, 0)
            if not self.current_installed:
                # self.uninstall_button.hide()
                GLib.idle_add(self.uninstall_button.hide)

        if self.install_callback is not None:
            self.install_button = Gtk.Button()
            self.install_button.set_label("更新" if self.current_installed else "安装")
            self.install_button.set_valign(Gtk.Align.CENTER)
            self.install_button.connect("clicked", self.on_install_clicked)
            self.pack_start(self.install_button, False, False, 0)

    def disable_buttons(self):
        if self.install_button is not None:
            self.install_button.set_sensitive(False)
        if self.uninstall_button is not None:
            self.uninstall_button.set_sensitive(False)
        self.spinner.start()

    def enable_buttons(self):
        if self.install_button is not None:
            self.install_button.set_sensitive(True)
        if self.uninstall_button is not None:
            self.uninstall_button.set_sensitive(True)
        self.spinner.stop()

    def reload_installed(self):
        if callable(self.installed_cb):
            self.current_installed = self.installed_cb()
        else:
            self.current_installed = self.installed_cb
    
        if self.current_installed:
            if self.install_button is not None:
                self.install_button.set_label("更新")
            if self.uninstall_button is not None:
                self.uninstall_button.show()
        else:
            if self.install_button is not None:
                self.install_button.set_label("安装")
            if self.uninstall_button is not None:
                self.uninstall_button.hide()

    def completed(self, success, install=True, msg=None):
        self.reload_installed()
        self.enable_buttons()
        print ("Completed: success: {}, install: {}, msg: {}".format(success, install, msg))
        # 根据回调函数的运行结果显示对话框内容
        if success:
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                modal=True,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=msg if msg else "{} {}成功".format(self.title, "安装" if install else "卸载"),
            )
        else:
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text=msg,
            )

        dialog.run()
        dialog.destroy()


    def execute_callback(self, callback, install):
        success, ret_msg = callback()
        GLib.idle_add(self.completed, success, install, ret_msg)

    def on_install_clicked(self, button):
        print("Installing...")
        self.disable_buttons()
        threading.Thread(target=self.execute_callback, args=(self.install_callback, True)).start()

    def on_uninstall_clicked(self, button):
        print("Uninstalling...")
        self.disable_buttons()
        threading.Thread(target=self.execute_callback, args=(self.uninstall_callback, False)).start()

class AsyncActionFullButton(Gtk.Button):
    def __init__(self, title, callback=None):
        Gtk.Button.__init__(self, label=title)

        self.set_margin_start(5)
        self.set_margin_end(5)
        self.set_margin_top(5)
        self.set_margin_bottom(5)

        self.set_sensitive(True)

        self.function_name = title
        self.callback = callback

        self.connect("clicked", self.on_clicked)

    def on_clicked(self, button):
        self.set_sensitive(False)
        self.set_label("处理中...")

        # 在一个新线程中执行回调函数
        threading.Thread(target=self.execute_callback).start()

    def execute_callback(self):
        # 执行回调函数，例如模拟耗时操作
        if self.callback:
            result, ret_msg = self.callback()

        # 在主循环中使用 GLib.idle_add() 调用回调函数
        GLib.idle_add(self.update_complete, result, ret_msg)

    def update_complete(self, result, ret_msg=None):
        # 更新完成后恢复按钮状态和文本
        self.set_sensitive(True)
        self.set_label(self.function_name)

        # 根据回调函数的运行结果显示对话框内容
        if result:
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                modal=True,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=ret_msg if ret_msg else "处理成功",
            )
        else:
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                modal=True,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text=ret_msg,
            )

        dialog.run()
        dialog.destroy()

        return False