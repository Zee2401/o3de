#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Ensure the local directory is in the import path
sys.path.insert(0, os.path.dirname(__file__))

class TestWaitDialog(unittest.TestCase):
    @patch("tkinter.Toplevel")
    @patch("tkinter.Label")
    @patch("tkinter.Button")
    @patch("tkinter.StringVar")
    def test_wait_dialog_initialization(self, mock_string_var, mock_button, mock_label, mock_toplevel):
        mock_parent = MagicMock()
        mock_cancel_cb = MagicMock()
        mock_toplevel_instance = mock_toplevel.return_value

        # Import the class under test
        from wait_dialog import WaitDialog

        dialog = WaitDialog(mock_parent, "Test Work Message", mock_cancel_cb)

        # Verify grab_set was called to make it modal
        mock_toplevel_instance.grab_set.assert_called_once()

        # Verify that escape and alt-c bindings are registered
        mock_toplevel_instance.bind.assert_any_call("<Escape>", unittest.mock.ANY)
        mock_toplevel_instance.bind.assert_any_call("<Alt-c>", unittest.mock.ANY)
        mock_toplevel_instance.bind.assert_any_call("<Alt-C>", unittest.mock.ANY)

        # Verify window close protocol is registered
        mock_toplevel_instance.protocol.assert_called_once_with("WM_DELETE_WINDOW", dialog._on_cancel_button)

        # Verify the Cancel button has underline=0
        mock_button.assert_called_with(mock_toplevel_instance, text="Cancel", command=dialog._on_cancel_button, underline=0)

    @patch("tkinter.Toplevel")
    @patch("tkinter.Label")
    @patch("tkinter.Button")
    @patch("tkinter.StringVar")
    def test_wait_dialog_cancel_callback(self, mock_string_var, mock_button, mock_label, mock_toplevel):
        mock_parent = MagicMock()
        mock_cancel_cb = MagicMock()

        from wait_dialog import WaitDialog
        dialog = WaitDialog(mock_parent, "Test Work Message", mock_cancel_cb)

        # Trigger the cancel button action
        dialog._on_cancel_button()

        # Verify parent focus is reset and callback is executed
        mock_parent.focus_set.assert_called_once()
        mock_cancel_cb.assert_called_once()


class DummyTk:
    _last_child_ids = None
    def __init__(self, *args, **kwargs):
        self.bind = MagicMock()
        self.title = MagicMock()
        self.winfo_pointerx = MagicMock(return_value=100)
        self.winfo_pointery = MagicMock(return_value=100)
        self.geometry = MagicMock()
        self.columnconfigure = MagicMock()
        self.rowconfigure = MagicMock()
        self.tk = MagicMock()
        import tkinter
        tkinter._default_root = self
    def _root(self):
        return self


class TestTkApp(unittest.TestCase):
    @patch("tkinter.Tk", DummyTk)
    @patch("tkinter.LabelFrame")
    @patch("tkinter.Button")
    @patch("tkinter.Label")
    @patch("tkinter.Entry")
    @patch("tkinter.StringVar")
    @patch("tkinter.BooleanVar")
    @patch("tkinter.Checkbutton")
    @patch("tkinter.Text")
    @patch("tkinter.Scrollbar")
    @patch("config_data.ConfigData")
    def test_tk_app_mnemonics(self, mock_config, mock_scrollbar, mock_text, mock_checkbutton, mock_bool_var, mock_string_var, mock_entry, mock_label, mock_button, mock_labelframe):
        # Delete cached main module to ensure it reloads and subclass uses DummyTk correctly
        if 'main' in sys.modules:
            del sys.modules['main']
        from main import TkApp

        cfg = mock_config.return_value
        cfg.keystore_settings = MagicMock()

        app = TkApp(cfg)

        # Verify Alt bindings are registered on the main application
        app.bind.assert_any_call("<Alt-g>", unittest.mock.ANY)
        app.bind.assert_any_call("<Alt-G>", unittest.mock.ANY)
        app.bind.assert_any_call("<Alt-l>", unittest.mock.ANY)
        app.bind.assert_any_call("<Alt-L>", unittest.mock.ANY)
        app.bind.assert_any_call("<Alt-s>", unittest.mock.ANY)
        app.bind.assert_any_call("<Alt-S>", unittest.mock.ANY)
        app.bind.assert_any_call("<Alt-c>", unittest.mock.ANY)
        app.bind.assert_any_call("<Alt-C>", unittest.mock.ANY)
