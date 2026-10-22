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

# Add current directory to path so wait_dialog can be imported
sys.path.insert(0, os.path.dirname(__file__))

class DummyTk:
    def __init__(self):
        self._last_child_ids = None
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

class TestWaitDialog(unittest.TestCase):
    @patch('tkinter.Toplevel')
    @patch('tkinter.Label')
    @patch('tkinter.Button')
    @patch('tkinter.StringVar')
    def test_wait_dialog_initialization_and_bindings(self, mock_stringvar, mock_button, mock_label, mock_toplevel):
        # Set up mock instances
        mock_dialog_inst = MagicMock()
        mock_toplevel.return_value = mock_dialog_inst

        mock_button_inst = MagicMock()
        mock_button.return_value = mock_button_inst

        mock_stringvar_inst = MagicMock()
        mock_stringvar_inst.get.return_value = ""
        mock_stringvar.return_value = mock_stringvar_inst

        # Callback for cancel
        cancel_called = False
        def dummy_cancel_cb():
            nonlocal cancel_called
            cancel_called = True

        parent = DummyTk()

        # Import WaitDialog
        from wait_dialog import WaitDialog

        # Instantiate WaitDialog
        dialog = WaitDialog(parent, "Please wait...", dummy_cancel_cb)

        # 1. Verify Toplevel dialog was created with parent
        mock_toplevel.assert_called_once_with(parent)

        # 2. Verify window setup
        mock_dialog_inst.title.assert_called_once_with("Operation In Progress...")
        mock_dialog_inst.grab_set.assert_called_once()

        # 3. Verify Button was created with underline=0 and correct text
        mock_button.assert_called_once()
        kwargs = mock_button.call_args[1]
        self.assertEqual(kwargs.get('text'), "Cancel")
        self.assertEqual(kwargs.get('underline'), 0)

        # 4. Verify bindings were set up for Escape, Alt-c, Alt-C
        bind_calls = [call[0][0] for call in mock_dialog_inst.bind.call_args_list]
        self.assertIn("<Escape>", bind_calls)
        self.assertIn("<Alt-c>", bind_calls)
        self.assertIn("<Alt-C>", bind_calls)

        # 5. Verify protocol for WM_DELETE_WINDOW was registered
        mock_dialog_inst.protocol.assert_called_once_with("WM_DELETE_WINDOW", dialog._on_cancel_button)

        # 6. Test cancellation triggers the callback and close
        dialog._on_cancel_button()
        self.assertTrue(cancel_called)
        mock_dialog_inst.destroy.assert_called_once()

        # 7. Verify on_tick cycles progress correctly
        dialog.on_tick(0.25)
        mock_stringvar_inst.set.assert_called_with("*")

    @patch('tkinter.Label')
    @patch('tkinter.Entry')
    @patch('tkinter.StringVar')
    def test_label_click_focuses_entry(self, mock_stringvar, mock_entry, mock_label):
        mock_label_inst = MagicMock()
        mock_label.return_value = mock_label_inst

        mock_entry_inst = MagicMock()
        mock_entry.return_value = mock_entry_inst

        from main import TkApp, ConfigData

        # Instantiate dummy parent frame
        parent_frame = MagicMock()

        # Call _add_label_entry directly on TkApp prototype or mock instance
        app = MagicMock(spec=TkApp)
        string_var, entry, row = TkApp._add_label_entry(app, parent_frame, "Test Label", "Default", entry_read_only=False)

        # Verify <Button-1> was bound on label
        mock_label_inst.bind.assert_called_once()
        event_name, callback = mock_label_inst.bind.call_args[0]
        self.assertEqual(event_name, "<Button-1>")

        # Trigger callback and verify entry focus_set was called
        callback(MagicMock())
        mock_entry_inst.focus_set.assert_called_once()
