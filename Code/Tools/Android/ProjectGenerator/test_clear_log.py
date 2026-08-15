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

import tkinter as tk
from config_data import ConfigData

class TestClearLog(unittest.TestCase):
    @patch('tkinter.Text')
    @patch("tkinter.Tk.__init__", return_value=None)
    @patch("tkinter.Tk.title", return_value=None)
    @patch("tkinter.Tk.geometry", return_value=None)
    @patch("tkinter.Tk.winfo_pointerx", return_value=0)
    @patch("tkinter.Tk.winfo_pointery", return_value=0)
    @patch("tkinter.Tk.columnconfigure", return_value=None)
    @patch("tkinter.Tk.rowconfigure", return_value=None)
    @patch("tkinter.Tk.bind", return_value=None)
    @patch("tkinter.LabelFrame")
    @patch("tkinter.Label")
    @patch("tkinter.Entry")
    @patch("tkinter.Button")
    @patch("tkinter.Scrollbar")
    @patch("tkinter.BooleanVar")
    @patch("tkinter.StringVar")
    def test_log_read_only_and_clear_log(self, mock_string_var, mock_boolean_var, mock_scrollbar, mock_button, mock_entry, mock_label, mock_labelframe, *args):
        mock_text_inst = MagicMock()
        mock_text_inst.cget.side_effect = lambda attr: tk.DISABLED if attr == "state" else None

        # Track inserted text
        stored_text = []
        def fake_insert(pos, txt):
            stored_text.append(txt)
        def fake_delete(start, end):
            stored_text.clear()
        def fake_get(start, end):
            return "".join(stored_text)

        mock_text_inst.insert.side_effect = fake_insert
        mock_text_inst.delete.side_effect = fake_delete
        mock_text_inst.get.side_effect = fake_get

        with patch('tkinter.Text', return_value=mock_text_inst):
            import main

            config = ConfigData()
            app = main.TkApp(config, "")

            # Verify initial state of _report_text_widget is tk.DISABLED
            self.assertEqual(app._report_text_widget.cget("state"), tk.DISABLED)

            # Append log message
            app._append_log_message("Test message 1")

            # Verify text content was added
            content = app._report_text_widget.get("1.0", tk.END)
            self.assertIn("Test message 1", content)

            # Append second log message
            app._append_log_message("Test message 2")

            content = app._report_text_widget.get("1.0", tk.END)
            self.assertIn("Test message 1", content)
            self.assertIn("Test message 2", content)

            # Trigger clear log button action
            app.on_clear_log_button()

            # Verify log is empty
            cleared_content = app._report_text_widget.get("1.0", tk.END)
            self.assertEqual(cleared_content.strip(), "")

if __name__ == "__main__":
    unittest.main()
