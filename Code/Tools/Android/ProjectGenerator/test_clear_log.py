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
    def __init__(self):
        self._last_child_ids = None
    def winfo_pointerx(self):
        return 0
    def winfo_pointery(self):
        return 0
    def winfo_x(self):
        return 100
    def winfo_y(self):
        return 100
    def winfo_width(self):
        return 800
    def winfo_height(self):
        return 600
    def focus_set(self):
        pass


class TestClearLog(unittest.TestCase):
    @patch('tkinter.Tk.__init__')
    @patch('tkinter.LabelFrame')
    @patch('tkinter.Label')
    @patch('tkinter.Entry')
    @patch('tkinter.Button')
    @patch('tkinter.Checkbutton')
    @patch('tkinter.Text')
    @patch('tkinter.Scrollbar')
    @patch('tkinter.StringVar')
    @patch('tkinter.BooleanVar')
    def test_clear_log_and_read_only_behavior(self, mock_boolvar, mock_stringvar, mock_scrollbar, mock_text, mock_checkbutton, mock_button, mock_entry, mock_label, mock_labelframe, mock_tk_init):
        # Set up a mock text widget
        mock_text_inst = MagicMock()
        mock_text.return_value = mock_text_inst

        # MockStringVar setup
        mock_stringvar_inst = MagicMock()
        mock_stringvar_inst.get.return_value = ""
        mock_stringvar.return_value = mock_stringvar_inst

        from config_data import ConfigData
        config = ConfigData()

        # Import TkApp
        from main import TkApp

        # We need a dummy root to satisfy tk.StringVar and other Tkinter lookups when Tk is not fully initialized.
        import tkinter
        dummy_root = DummyTk()
        tkinter._default_root = dummy_root

        # Patch winfo methods on TkApp to avoid accessing actual display
        with patch.object(TkApp, 'winfo_pointerx', return_value=100), \
             patch.object(TkApp, 'winfo_pointery', return_value=100), \
             patch.object(TkApp, 'columnconfigure'), \
             patch.object(TkApp, 'rowconfigure'), \
             patch.object(TkApp, 'bind'), \
             patch.object(TkApp, 'title'), \
             patch.object(TkApp, 'geometry'):

            app = TkApp(config)

            # Assert Text widget initialized with state=tk.DISABLED
            mock_text.assert_called_once()
            kwargs = mock_text.call_args[1]
            self.assertEqual(kwargs.get('state'), 'disabled')

            # Test appending log message (should change state to NORMAL, insert/see, then change back to DISABLED)
            app._append_log_message("My Test Log Message")

            # Verify text configure calls
            configure_calls = [c[1].get('state') for c in mock_text_inst.configure.call_args_list if 'state' in c[1]]
            self.assertIn('normal', configure_calls)
            self.assertIn('disabled', configure_calls)
            mock_text_inst.insert.assert_called_once()
            self.assertIn("My Test Log Message", mock_text_inst.insert.call_args[0][1])
            mock_text_inst.see.assert_called_once()

            # Reset call states on text widget mock
            mock_text_inst.configure.reset_mock()
            mock_text_inst.delete.reset_mock()

            # Test on_clear_log_button (should change state to NORMAL, delete content, then change back to DISABLED)
            app.on_clear_log_button()

            configure_calls_clear = [c[1].get('state') for c in mock_text_inst.configure.call_args_list if 'state' in c[1]]
            self.assertIn('normal', configure_calls_clear)
            self.assertIn('disabled', configure_calls_clear)
            mock_text_inst.delete.assert_called_once_with("1.0", "end")

        # Clean up default root
        tkinter._default_root = None
