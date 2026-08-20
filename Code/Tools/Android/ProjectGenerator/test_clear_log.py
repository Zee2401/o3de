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

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from config_data import ConfigData

class DummyTkRoot:
    def __init__(self, *args, **kwargs):
        self._last_child_ids = None
        self.children = {}
        self._w = "."
        self.tk = MagicMock()

    def title(self, t):
        pass

    def geometry(self, g):
        pass

    def winfo_pointerx(self):
        return 0

    def winfo_pointery(self):
        return 0

    def columnconfigure(self, index, weight=0):
        pass

    def rowconfigure(self, index, weight=0):
        pass

    def bind(self, sequence=None, func=None, add=None):
        pass

    def update_idletasks(self):
        pass


class TestClearLog(unittest.TestCase):
    @patch('tkinter.StringVar')
    @patch('tkinter.BooleanVar')
    @patch('tkinter.LabelFrame')
    @patch('tkinter.Label')
    @patch('tkinter.Entry')
    @patch('tkinter.Button')
    @patch('tkinter.Checkbutton')
    @patch('tkinter.Text')
    @patch('tkinter.Scrollbar')
    def test_clear_log_and_readonly_state(
        self, mock_scrollbar, mock_text, mock_checkbutton, mock_button,
        mock_entry, mock_label, mock_labelframe, mock_boolvar, mock_stringvar
    ):
        mock_text_inst = MagicMock()
        mock_text.return_value = mock_text_inst

        # Import main and patch TkApp's base class to DummyTkRoot
        import main
        original_bases = main.TkApp.__bases__
        main.TkApp.__bases__ = (DummyTkRoot,)

        try:
            config = ConfigData()
            app = main.TkApp(config, "test_config.json")

            # Verify initial state of report_text_widget is tk.DISABLED
            mock_text.assert_called_once()
            self.assertEqual(mock_text.call_args[1].get('state'), main.tk.DISABLED)

            # Test appending log message
            mock_text_inst.reset_mock()
            app._append_log_message("Test execution log message")

            # Check that state was toggled to NORMAL before insert/see, and back to DISABLED after
            config_calls = [call[1].get('state') for call in mock_text_inst.configure.call_args_list if 'state' in call[1]]
            self.assertIn(main.tk.NORMAL, config_calls)
            self.assertIn(main.tk.DISABLED, config_calls)
            mock_text_inst.insert.assert_called_once()
            mock_text_inst.see.assert_called_once_with(main.tk.END)

            # Test clearing log via on_clear_log_button
            mock_text_inst.reset_mock()
            app.on_clear_log_button()

            clear_config_calls = [call[1].get('state') for call in mock_text_inst.configure.call_args_list if 'state' in call[1]]
            self.assertIn(main.tk.NORMAL, clear_config_calls)
            self.assertIn(main.tk.DISABLED, clear_config_calls)
            mock_text_inst.delete.assert_called_once_with("1.0", main.tk.END)

        finally:
            main.TkApp.__bases__ = original_bases


if __name__ == "__main__":
    unittest.main()
