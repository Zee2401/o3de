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

# Add current directory to path so main can be imported
sys.path.insert(0, os.path.dirname(__file__))

class DummyTk:
    def __init__(self, *args, **kwargs):
        self._last_child_ids = None
        self.bindings = {}
    def winfo_x(self):
        return 100
    def winfo_y(self):
        return 100
    def winfo_width(self):
        return 800
    def winfo_height(self):
        return 600
    def winfo_pointerx(self):
        return 150
    def winfo_pointery(self):
        return 150
    def focus_set(self):
        pass
    def columnconfigure(self, *args, **kwargs):
        pass
    def rowconfigure(self, *args, **kwargs):
        pass
    def geometry(self, *args):
        pass
    def title(self, *args):
        pass
    def bind(self, event, callback):
        self.bindings[event] = callback


class TestClearLog(unittest.TestCase):
    @patch('tkinter.Tk', DummyTk)
    @patch('tkinter.LabelFrame')
    @patch('tkinter.Label')
    @patch('tkinter.Button')
    @patch('tkinter.Entry')
    @patch('tkinter.Text')
    @patch('tkinter.Scrollbar')
    @patch('tkinter.StringVar')
    @patch('tkinter.Checkbutton')
    @patch('tkinter.BooleanVar')
    def test_read_only_and_clear_log(self, mock_boolvar, mock_checkbutton, mock_stringvar,
                                      mock_scrollbar, mock_text, mock_entry, mock_button,
                                      mock_label, mock_labelframe):
        # Setup mocks
        mock_text_inst = MagicMock()
        mock_text.return_value = mock_text_inst

        # Import modules
        from main import TkApp
        from config_data import ConfigData

        config = ConfigData()
        # Initialize app
        app = TkApp(config, "dummy_path.json")

        # 1. Verify report text widget was instantiated with state=tk.DISABLED
        mock_text.assert_called_once()
        kwargs = mock_text.call_args[1]
        self.assertEqual(kwargs.get('state'), 'disabled')

        # Reset mocks before append testing to clear init configure calls
        mock_text_inst.configure.reset_mock()

        # 2. Verify _append_log_message toggles state to NORMAL and back to DISABLED
        app._get_time_now_str = MagicMock(return_value="12:00:00.123")
        app._append_log_message("Hello Test Log")

        # Check call order of configure and insert
        configure_calls = mock_text_inst.configure.call_args_list
        self.assertEqual(len(configure_calls), 2)
        self.assertEqual(configure_calls[0][1].get('state'), 'normal')
        mock_text_inst.insert.assert_called_with('end', ">>12:00:00.123>>\nHello Test Log\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        self.assertEqual(configure_calls[1][1].get('state'), 'disabled')
        mock_text_inst.see.assert_called_with('end')

        # 3. Verify clear_log clears text and handles read-only state toggling
        mock_text_inst.configure.reset_mock()
        app.clear_log()

        clear_configure_calls = mock_text_inst.configure.call_args_list
        self.assertEqual(len(clear_configure_calls), 2)
        self.assertEqual(clear_configure_calls[0][1].get('state'), 'normal')
        mock_text_inst.delete.assert_called_with("1.0", "end")
        self.assertEqual(clear_configure_calls[1][1].get('state'), 'disabled')

        # 4. Verify Alt-R bindings exist on the root window
        self.assertIn("<Alt-r>", app.bindings)
        self.assertIn("<Alt-R>", app.bindings)
