#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import tkinter as tk

# Add current directory to path so main can be imported
sys.path.insert(0, os.path.dirname(__file__))

class DummyTkRoot:
    def __init__(self, *args, **kwargs):
        self._last_child_ids = {}
        self.children = {}
        self._w = "."
        self.tk = MagicMock()
        self._bindings = {}

    def winfo_pointerx(self):
        return 0

    def winfo_pointery(self):
        return 0

    def geometry(self, geom=None):
        pass

    def title(self, title=None):
        pass

    def columnconfigure(self, index, weight=0):
        pass

    def rowconfigure(self, index, weight=0):
        pass

    def bind(self, sequence=None, func=None, add=None):
        if sequence:
            self._bindings[sequence] = func


class TestClearLog(unittest.TestCase):
    @patch('tkinter.LabelFrame')
    @patch('tkinter.Label')
    @patch('tkinter.Entry')
    @patch('tkinter.Button')
    @patch('tkinter.Checkbutton')
    @patch('tkinter.Text')
    @patch('tkinter.Scrollbar')
    @patch('tkinter.StringVar')
    @patch('tkinter.BooleanVar')
    def test_tk_app_log_read_only_and_clear_log(
        self, mock_boolvar, mock_stringvar, mock_scrollbar, mock_text,
        mock_checkbutton, mock_button, mock_entry, mock_label, mock_labelframe
    ):
        mock_stringvar_inst = MagicMock()
        mock_stringvar_inst.get.return_value = ""
        mock_stringvar.return_value = mock_stringvar_inst

        mock_boolvar_inst = MagicMock()
        mock_boolvar_inst.get.return_value = False
        mock_boolvar.return_value = mock_boolvar_inst

        mock_text_inst = MagicMock()
        mock_text.return_value = mock_text_inst

        from config_data import ConfigData
        from main import TkApp

        # Patch base class to DummyTkRoot to bypass Tcl display init
        original_bases = TkApp.__bases__
        try:
            TkApp.__bases__ = (DummyTkRoot,)
            config = ConfigData()
            app = TkApp(config)

            # 1. Verify text widget was initialized with state=tk.DISABLED
            mock_text.assert_called_once()
            kwargs = mock_text.call_args[1]
            self.assertEqual(kwargs.get('state'), tk.DISABLED)

            # 2. Verify Alt-r and Alt-R shortcuts are bound
            self.assertIn("<Alt-r>", app._bindings)
            self.assertIn("<Alt-R>", app._bindings)

            # 3. Verify _append_log_message toggles state to NORMAL, inserts message, then disables
            app._append_log_message("Test message")
            mock_text_inst.configure.assert_any_call(state=tk.NORMAL)
            mock_text_inst.insert.assert_called_once()
            self.assertIn("Test message", mock_text_inst.insert.call_args[0][1])
            self.assertEqual(mock_text_inst.configure.call_args[1].get('state'), tk.DISABLED)

            # 4. Verify on_clear_log_button enables, deletes content, then disables
            mock_text_inst.reset_mock()
            app.on_clear_log_button()
            mock_text_inst.configure.assert_any_call(state=tk.NORMAL)
            mock_text_inst.delete.assert_called_once_with("1.0", tk.END)
            self.assertEqual(mock_text_inst.configure.call_args[1].get('state'), tk.DISABLED)

        finally:
            TkApp.__bases__ = original_bases
