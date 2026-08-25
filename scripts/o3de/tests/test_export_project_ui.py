#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

from unittest.mock import MagicMock, patch
import pytest


class DummyTk:
    def __init__(self, *args, **kwargs):
        self._last_child_ids = None
        self.children = {}
        self._w = "."
        self.tk = MagicMock()

    def title(self, *args, **kwargs):
        pass

    def columnconfigure(self, *args, **kwargs):
        pass

    def rowconfigure(self, *args, **kwargs):
        pass

    def grid_rowconfigure(self, *args, **kwargs):
        pass

    def grid_columnconfigure(self, *args, **kwargs):
        pass

    def eval(self, *args, **kwargs):
        pass

    def bind(self, *args, **kwargs):
        pass

    def protocol(self, *args, **kwargs):
        pass

    def destroy(self):
        pass

    def __getattr__(self, name):
        return MagicMock()


@patch("tkinter.Frame")
@patch("tkinter.LabelFrame")
@patch("tkinter.Label")
@patch("tkinter.Button")
@patch("tkinter.Entry")
@patch("tkinter.Checkbutton")
@patch("tkinter.OptionMenu")
@patch("tkinter.StringVar")
@patch("tkinter.IntVar")
@patch("tkinter.ttk.Notebook")
@patch("tkinter.ttk.Frame")
def test_main_window_keyboard_and_protocol_bindings(
    mock_ttk_frame,
    mock_notebook,
    mock_int_var,
    mock_string_var,
    mock_option_menu,
    mock_checkbutton,
    mock_entry,
    mock_button,
    mock_label,
    mock_labelframe,
    mock_frame,
):
    from o3de.ui.export_project import MainWindow

    orig_bases = MainWindow.__bases__
    try:
        MainWindow.__bases__ = (DummyTk,)

        mock_export_config = MagicMock()
        mock_export_config.is_global = False
        mock_export_config.project_name = "TestProject"

        def mock_get_value(key, default=""):
            if "archive" in key or "assets.mode" in key:
                return ""
            if "config" in key:
                return "profile"
            return "false"

        mock_export_config.get_value.side_effect = mock_get_value
        mock_export_config.get_settings_description.return_value.description = "Test description"

        with patch.object(DummyTk, "bind") as mock_bind, patch.object(
            DummyTk, "protocol"
        ) as mock_protocol:

            window = MainWindow(export_config=mock_export_config, is_sdk=True)

            bound_events = [call[0][0] for call in mock_bind.call_args_list]
            assert "<Alt-s>" in bound_events
            assert "<Alt-S>" in bound_events
            assert "<Alt-c>" in bound_events
            assert "<Alt-C>" in bound_events
            assert "<Escape>" in bound_events

            mock_protocol.assert_called_once_with("WM_DELETE_WINDOW", window.on_cancel)
    finally:
        MainWindow.__bases__ = orig_bases
