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

class DummyTk:
    def __init__(self):
        self._last_child_ids = None
        self.title_val = ""
        self.geometry_val = ""
        self.bindings = {}
        self._row_count = 0
        self._column_count = 0

    def _root(self):
        return self

    def title(self, val):
        self.title_val = val

    def geometry(self, val):
        self.geometry_val = val

    def winfo_pointerx(self):
        return 0

    def winfo_pointery(self):
        return 0

    def columnconfigure(self, col, weight=0):
        pass

    def rowconfigure(self, row, weight=0):
        pass

    def bind(self, event, callback):
        self.bindings[event] = callback

    def after(self, ms, func):
        pass


class TestClearLog(unittest.TestCase):
    @patch('tkinter.Tk.__init__', lambda self, *args, **kwargs: None)
    @patch('tkinter.LabelFrame')
    @patch('tkinter.Label')
    @patch('tkinter.Entry')
    @patch('tkinter.Button')
    @patch('tkinter.Checkbutton')
    @patch('tkinter.Text')
    @patch('tkinter.Scrollbar')
    @patch('tkinter.StringVar')
    @patch('tkinter.BooleanVar')
    def test_tk_app_clear_log(self, mock_booleanvar, mock_stringvar, mock_scrollbar, mock_text, mock_checkbutton, mock_button, mock_entry, mock_label, mock_labelframe):
        # Set up a mock text widget instance
        mock_text_inst = MagicMock()
        mock_text.return_value = mock_text_inst

        # Mock stringvar get/set
        mock_stringvar_inst = MagicMock()
        mock_stringvar_inst.get.return_value = ""
        mock_stringvar.return_value = mock_stringvar_inst

        # Mock booleanvar get/set
        mock_booleanvar_inst = MagicMock()
        mock_booleanvar_inst.get.return_value = False
        mock_booleanvar.return_value = mock_booleanvar_inst

        # Track configure calls for state
        config_states = []
        def mock_configure(**kwargs):
            if 'state' in kwargs:
                config_states.append(kwargs['state'])
        mock_text_inst.configure.side_effect = mock_configure

        # Mock the default root for Tkinter widgets
        dummy_tk = DummyTk()
        tk._default_root = dummy_tk

        # Import ConfigData and TkApp
        from config_data import ConfigData
        from main import TkApp

        config = ConfigData()

        # Instantiate TkApp
        # Since we patched tkinter.Tk.__init__ to do nothing, we can safely initialize TkApp
        # and manually assign dummy methods/attributes if needed.
        with patch.object(TkApp, 'winfo_pointerx', return_value=100), \
             patch.object(TkApp, 'winfo_pointery', return_value=200), \
             patch.object(TkApp, 'geometry'), \
             patch.object(TkApp, 'title'), \
             patch.object(TkApp, 'columnconfigure'), \
             patch.object(TkApp, 'rowconfigure'), \
             patch.object(TkApp, 'bind') as mock_bind:

            app = TkApp(config, "dummy_config.json")

            # 1. Verify text widget starts as disabled
            # When Text is instantiated, it gets state=tk.DISABLED
            mock_text.assert_called_once()
            self.assertEqual(mock_text.call_args[1].get('state'), tk.DISABLED)

            # 2. Verify clear button was created inside the operations report frame
            # Let's check Button calls to see if "Clear Log" button is created
            clear_btn_calls = [call for call in mock_button.call_args_list if call[1].get('text') == "Clear Log"]
            self.assertEqual(len(clear_btn_calls), 1)
            self.assertEqual(clear_btn_calls[0][1].get('underline'), 4)

            # 3. Verify keyboard bindings for Alt-r and Alt-R were established
            bind_calls = [call[0][0] for call in mock_bind.call_args_list]
            self.assertIn("<Alt-r>", bind_calls)
            self.assertIn("<Alt-R>", bind_calls)

            # 4. Test _append_log_message
            config_states.clear()
            app._append_log_message("Test Message")
            # Should configure to NORMAL, insert, and then configure back to DISABLED
            mock_text_inst.insert.assert_called_with(tk.END, unittest.mock.ANY)
            self.assertIn(tk.NORMAL, config_states)
            self.assertIn(tk.DISABLED, config_states)
            # Ensure it ends in DISABLED state
            self.assertEqual(config_states[-1], tk.DISABLED)

            # 5. Test on_clear_log_button
            config_states.clear()
            mock_text_inst.delete.reset_mock()
            app.on_clear_log_button()
            # Should configure to NORMAL, delete, and configure to DISABLED
            mock_text_inst.delete.assert_called_once_with("1.0", tk.END)
            self.assertIn(tk.NORMAL, config_states)
            self.assertIn(tk.DISABLED, config_states)
            # Ensure it ends in DISABLED state
            self.assertEqual(config_states[-1], tk.DISABLED)
