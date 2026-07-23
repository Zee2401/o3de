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

# Ensure the parent directory is in sys.path so we can import wait_dialog
sys.path.append(os.path.dirname(__file__))

from wait_dialog import WaitDialog


class TestWaitDialog(unittest.TestCase):
    @patch('tkinter.Toplevel')
    @patch('tkinter.Label')
    @patch('tkinter.Button')
    @patch('tkinter.StringVar')
    def test_wait_dialog_initialization(self, mock_string_var, mock_button, mock_label, mock_toplevel):
        # Configure mocked StringVar
        stored_string = [""]
        mock_string_var_instance = MagicMock()
        mock_string_var_instance.get.side_effect = lambda: stored_string[0]
        def set_val(val):
            stored_string[0] = val
        mock_string_var_instance.set.side_effect = set_val
        mock_string_var.return_value = mock_string_var_instance

        # Mock tk_parent
        mock_parent = MagicMock()
        mock_parent.winfo_x.return_value = 100
        mock_parent.winfo_y.return_value = 100
        mock_parent.winfo_width.return_value = 500
        mock_parent.winfo_height.return_value = 400

        cancel_called = False
        def cancel_cb():
            nonlocal cancel_called
            cancel_called = True

        # Initialize WaitDialog
        dialog = WaitDialog(mock_parent, "Testing message", cancel_cb)

        # Assertions
        mock_toplevel.assert_called_once_with(mock_parent)
        dialog._dialog.wait_visibility.assert_called_once()
        dialog._dialog.geometry.assert_called_once()
        dialog._dialog.title.assert_called_once_with("Operation In Progress...")
        dialog._dialog.grab_set.assert_called_once()

        # Check bindings
        dialog._dialog.bind.assert_any_call("<Escape>", unittest.mock.ANY)
        dialog._dialog.bind.assert_any_call("<Alt-c>", unittest.mock.ANY)
        dialog._dialog.bind.assert_any_call("<Alt-C>", unittest.mock.ANY)
        dialog._dialog.protocol.assert_called_once_with("WM_DELETE_WINDOW", dialog._on_cancel_button)

        # Verify on_tick behavior
        stored_string[0] = ""
        dialog.on_tick(0.25)
        self.assertEqual(stored_string[0], "*")

        dialog.on_tick(0.25)
        self.assertEqual(stored_string[0], "**")

        dialog.on_tick(0.25)
        self.assertEqual(stored_string[0], "***")

        dialog.on_tick(0.25)
        self.assertEqual(stored_string[0], "****")

        dialog.on_tick(0.25)
        self.assertEqual(stored_string[0], "***")

        # Verify cancel action triggers callback
        self.assertFalse(cancel_called)
        dialog._on_cancel_button()
        self.assertTrue(cancel_called)
        dialog._dialog.destroy.assert_called_once()
        mock_parent.focus_set.assert_called_once()
