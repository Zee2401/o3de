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

from config_data import ConfigData

class DummyTk:
    """
    A dummy class to replace tk.Tk to avoid GUI initialization in headless tests.
    """
    def __init__(self, *args, **kwargs):
        self._last_child_ids = None
    def title(self, *args, **kwargs):
        pass
    def geometry(self, *args, **kwargs):
        pass
    def columnconfigure(self, *args, **kwargs):
        pass
    def rowconfigure(self, *args, **kwargs):
        pass
    def bind(self, *args, **kwargs):
        pass
    def winfo_pointerx(self, *args, **kwargs):
        return 100
    def winfo_pointery(self, *args, **kwargs):
        return 100


class TestClearLog(unittest.TestCase):
    @patch('tkinter.Tk', DummyTk)
    @patch('tkinter.LabelFrame')
    @patch('tkinter.Button')
    @patch('tkinter.Text')
    @patch('tkinter.Scrollbar')
    @patch('tkinter.Label')
    @patch('tkinter.Entry')
    @patch('tkinter.Checkbutton')
    @patch('tkinter.StringVar')
    @patch('tkinter.BooleanVar')
    def test_clear_log_and_readonly_behavior(self, mock_boolvar, mock_stringvar, mock_check, mock_entry, mock_label, mock_scrollbar, mock_text, mock_button, mock_labelframe):
        # Set up mock instances
        mock_text_inst = MagicMock()
        mock_text.return_value = mock_text_inst

        # Import main and config
        from main import TkApp
        config = ConfigData()

        # Instantiate app
        app = TkApp(config)

        # 1. Verify that the operations report text widget is initialized as read-only (DISABLED)
        # We can find the call to configure on the mock text instance.
        mock_text_inst.configure.assert_any_call(state='disabled')

        # Reset mock calls to focus on append and clear actions
        mock_text_inst.reset_mock()

        # 2. Test programmatic log append
        app._append_log_message("Hello Test Log")

        # Verify state toggling: NORMAL -> insert -> DISABLED
        mock_text_inst.configure.assert_has_calls([
            call(state='normal'),
            call(state='disabled')
        ], any_order=False)

        # Verify text was inserted and widget scrolled to end
        mock_text_inst.insert.assert_called_once()
        self.assertIn("Hello Test Log", mock_text_inst.insert.call_args[0][1])
        mock_text_inst.see.assert_called_once_with('end')

        # Reset mock calls
        mock_text_inst.reset_mock()

        # 3. Test log clearing
        app.on_clear_log_button()

        # Verify state toggling: NORMAL -> delete -> DISABLED
        mock_text_inst.configure.assert_has_calls([
            call(state='normal'),
            call(state='disabled')
        ], any_order=False)

        # Verify text delete was called with correct range
        mock_text_inst.delete.assert_called_once_with("1.0", "end")
