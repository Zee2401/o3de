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

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

class DummyRoot:
    def __init__(self):
        self.tk = MagicMock()
        self._last_child_ids = None
    def _root(self):
        return self

class TestClearLog(unittest.TestCase):
    @patch('tkinter.Tk.__init__', lambda self, *args, **kwargs: None)
    @patch('tkinter.Tk.title')
    @patch('tkinter.Tk.geometry')
    @patch('tkinter.Tk.columnconfigure')
    @patch('tkinter.Tk.rowconfigure')
    @patch('tkinter.Tk.bind')
    @patch('tkinter.Tk.winfo_pointerx', return_value=100)
    @patch('tkinter.Tk.winfo_pointery', return_value=100)
    @patch('tkinter.LabelFrame')
    @patch('tkinter.Text')
    @patch('tkinter.Scrollbar')
    @patch('tkinter.Button')
    @patch('config_data.ConfigData')
    def test_log_read_only_and_clear(self, mock_config, mock_btn, mock_scrollbar, mock_text, mock_labelframe, mock_px, mock_py, mock_bind, mock_row, mock_col, mock_geo, mock_title):
        # Initialize default root so StringVar doesn't fail
        tk._default_root = DummyRoot()

        # Set up mock widgets
        mock_text_inst = MagicMock()
        mock_text.return_value = mock_text_inst

        # Import TkApp
        from main import TkApp

        app = TkApp(mock_config)

        # Verify text widget was initialized as DISABLED
        mock_text.assert_called()
        self.assertEqual(mock_text.call_args[1].get("state"), "disabled")

        # Test log insertion toggles state to NORMAL and back to DISABLED
        mock_text_inst.configure.reset_mock()
        app._append_log_message("This is a test log message")

        # Check that state was set to normal, then to disabled
        configure_calls = [call[1].get("state") for call in mock_text_inst.configure.call_args_list if "state" in call[1]]
        self.assertIn("normal", configure_calls)
        self.assertIn("disabled", configure_calls)
        self.assertEqual(configure_calls[0], "normal")
        self.assertEqual(configure_calls[-1], "disabled")

        # Verify programmatic text insert occurred
        mock_text_inst.insert.assert_called()
        self.assertIn("This is a test log message", mock_text_inst.insert.call_args[0][1])

        # Test clear log button logic toggles state to NORMAL, deletes, and goes back to DISABLED
        mock_text_inst.configure.reset_mock()
        app.on_clear_log_button()

        # Check configure calls for clearing
        configure_calls_clear = [call[1].get("state") for call in mock_text_inst.configure.call_args_list if "state" in call[1]]
        self.assertEqual(configure_calls_clear[0], "normal")
        self.assertEqual(configure_calls_clear[-1], "disabled")

        # Verify text delete was called from start to end
        mock_text_inst.delete.assert_called_once_with("1.0", "end")
