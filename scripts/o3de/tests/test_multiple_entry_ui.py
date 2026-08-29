#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import unittest
from unittest.mock import MagicMock, patch
class DummyTk:
    def __init__(self):
        self._last_child_ids = None
    def winfo_rootx(self):
        return 100
    def winfo_rooty(self):
        return 100


class TestMultipleEntryDialog(unittest.TestCase):
    @patch('tkinter.Toplevel')
    @patch('tkinter.Frame')
    @patch('tkinter.Text')
    @patch('tkinter.Button')
    def test_dialog_initialization_and_bindings(self, mock_button, mock_text, mock_frame, mock_toplevel):
        mock_root = MagicMock()
        mock_toplevel.return_value = mock_root

        mock_text_inst = MagicMock()
        mock_text_inst.get.return_value = "item1\nitem2"
        mock_text.return_value = mock_text_inst

        parent = DummyTk()

        from o3de.ui.multiple_entry import Dialog

        dialog = Dialog(parent, "item1;item2")

        # Verify buttons created with underline=0
        button_calls = mock_button.call_args_list
        self.assertEqual(len(button_calls), 2)
        ok_kwargs = button_calls[0][1]
        cancel_kwargs = button_calls[1][1]

        self.assertEqual(ok_kwargs.get('text'), "Ok")
        self.assertEqual(ok_kwargs.get('underline'), 0)
        self.assertEqual(cancel_kwargs.get('text'), "Cancel")
        self.assertEqual(cancel_kwargs.get('underline'), 0)

        # Verify keyboard shortcuts binding
        bind_calls = [call[0][0] for call in mock_root.bind.call_args_list]
        self.assertIn("<Escape>", bind_calls)
        self.assertIn("<Alt-o>", bind_calls)
        self.assertIn("<Alt-O>", bind_calls)
        self.assertIn("<Alt-c>", bind_calls)
        self.assertIn("<Alt-C>", bind_calls)

        # Verify WM_DELETE_WINDOW protocol registration
        mock_root.protocol.assert_called_once_with("WM_DELETE_WINDOW", dialog._on_cancel)

        # Verify Ok action
        dialog._on_ok()
        self.assertTrue("item1" in dialog.input_value)
        self.assertTrue("item2" in dialog.input_value)
        mock_root.destroy.assert_called()

        # Verify Cancel action
        dialog._on_cancel()
        mock_root.destroy.assert_called()
