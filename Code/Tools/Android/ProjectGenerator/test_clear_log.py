#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import unittest
from unittest.mock import MagicMock, patch, call
import sys
import os

# Add current directory to path so main can be imported
sys.path.insert(0, os.path.dirname(__file__))

class DummyTk:
    def __init__(self, *args, **kwargs):
        self._last_child_ids = None
    def title(self, title):
        pass
    def geometry(self, geom):
        pass
    def winfo_pointerx(self):
        return 100
    def winfo_pointery(self):
        return 100
    def columnconfigure(self, *args, **kwargs):
        pass
    def rowconfigure(self, *args, **kwargs):
        pass
    def bind(self, *args, **kwargs):
        pass


class TestClearLog(unittest.TestCase):
    @patch('tkinter.Tk', DummyTk)
    @patch('tkinter.LabelFrame')
    @patch('tkinter.Text')
    @patch('tkinter.Scrollbar')
    @patch('tkinter.Button')
    @patch('tkinter.Checkbutton')
    @patch('tkinter.StringVar')
    @patch('tkinter.BooleanVar')
    def test_log_read_only_and_clear_functionality(
        self, mock_booleanvar, mock_stringvar, mock_checkbutton, mock_button, mock_scrollbar, mock_text, mock_labelframe
    ):
        # Set up mock instances for text widget and button
        mock_text_inst = MagicMock()
        mock_text.return_value = mock_text_inst

        mock_button_inst = MagicMock()
        mock_button.return_value = mock_button_inst

        # Import ConfigData and TkApp
        from config_data import ConfigData
        from main import TkApp

        config = ConfigData()
        app = TkApp(config)

        # 1. Verify text widget was initialized with state=tk.DISABLED
        mock_text.assert_called_with(mock_labelframe.return_value, wrap='word', borderwidth=2, relief='sunken', state='disabled')

        # 2. Verify append_log_message logic toggles state to NORMAL, inserts, and toggles back to DISABLED
        mock_text_inst.reset_mock()
        app._append_log_message("Test Message")

        # Verify calls on self._report_text_widget
        mock_text_inst.configure.assert_has_calls([
            call(state='normal'),
            call(state='disabled')
        ])
        mock_text_inst.insert.assert_called_once()
        self.assertIn("Test Message", mock_text_inst.insert.call_args[0][1])
        mock_text_inst.see.assert_called_once_with('end')

        # 3. Verify on_clear_log_button logic toggles state to NORMAL, deletes, and toggles back to DISABLED
        mock_text_inst.reset_mock()
        app.on_clear_log_button()

        # Verify calls on self._report_text_widget for clear log
        mock_text_inst.configure.assert_has_calls([
            call(state='normal'),
            call(state='disabled')
        ])
        mock_text_inst.delete.assert_called_once_with('1.0', 'end')
