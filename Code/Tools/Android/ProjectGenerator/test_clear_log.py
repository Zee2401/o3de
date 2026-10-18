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

class DummyTk:
    def __init__(self, *args, **kwargs):
        pass
    def title(self, *args):
        pass
    def geometry(self, *args):
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
    @patch('tkinter.Entry')
    @patch('tkinter.Label')
    @patch('tkinter.Checkbutton')
    def test_clear_log_behavior(self, mock_check, mock_label, mock_entry, mock_button, mock_scrollbar, mock_text, mock_labelframe):
        # Force reload main module so that patches to tkinter are in effect
        if 'main' in sys.modules:
            del sys.modules['main']

        # Set up default root for tk variables
        tk._default_root = MagicMock()

        # Prevent actually calling Tk/Text methods, mock them all
        mock_text_inst = MagicMock()
        mock_text.return_value = mock_text_inst

        # We need a ConfigData mock
        from config_data import ConfigData
        config = MagicMock(spec=ConfigData)
        config.keystore_settings = MagicMock()
        config.android_ndk_version = "25.2.9519653"
        config.android_sdk_api_level = "33"
        config.android_sdk_path = "/path/to/sdk"
        config.is_meta_quest_project = False
        config.extra_cmake_args = ""
        config_file_path = "apg_config.json"

        from main import TkApp

        # Instantiate TkApp (all sub-widgets will be mock instances)
        app = TkApp(config, config_file_path)

        print(f"mock_text.call_args_list: {mock_text.call_args_list}")

        # Verify Text widget was initialized as disabled
        mock_text.assert_called()
        init_kwargs = mock_text.call_args[1]
        self.assertEqual(init_kwargs.get('state'), tk.DISABLED)

        # Reset mock_text_inst to track new calls clearly
        mock_text_inst.reset_mock()

        # Test appending a message
        # _append_log_message should:
        # 1. set state to NORMAL
        # 2. insert the message
        # 3. set state to DISABLED
        # 4. scroll to the end (see)
        app._append_log_message("Hello World")

        # Verify the sequence of configure and insert calls
        expected_calls = [
            unittest.mock.call.configure(state=tk.NORMAL),
            unittest.mock.call.insert(tk.END, unittest.mock.ANY),
            unittest.mock.call.configure(state=tk.DISABLED),
            unittest.mock.call.see(tk.END)
        ]
        mock_text_inst.assert_has_calls(expected_calls, any_order=False)

        # Reset mock_text_inst again
        mock_text_inst.reset_mock()

        # Test clearing the log
        # on_clear_log_button should:
        # 1. set state to NORMAL
        # 2. delete everything
        # 3. set state to DISABLED
        app.on_clear_log_button()

        expected_clear_calls = [
            unittest.mock.call.configure(state=tk.NORMAL),
            unittest.mock.call.delete("1.0", tk.END),
            unittest.mock.call.configure(state=tk.DISABLED)
        ]
        mock_text_inst.assert_has_calls(expected_clear_calls, any_order=False)
