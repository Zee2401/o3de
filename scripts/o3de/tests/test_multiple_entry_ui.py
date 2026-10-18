#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import unittest
from unittest.mock import MagicMock, patch
import sys
import pathlib

# Add o3de python package to path
O3DE_PATH = pathlib.Path(__file__).parent.parent
if str(O3DE_PATH) not in sys.path:
    sys.path.insert(0, str(O3DE_PATH))


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
        mock_toplevel_inst = MagicMock()
        mock_toplevel.return_value = mock_toplevel_inst

        mock_text_inst = MagicMock()
        mock_text.return_value = mock_text_inst
        mock_text_inst.get.return_value = "item1\nitem2\n"

        parent = DummyTk()

        from o3de.ui.multiple_entry import Dialog

        dialog = Dialog(parent, "item1;item2")

        # 1. Verify Toplevel dialog was created
        mock_toplevel.assert_called_once_with(parent)
        mock_toplevel_inst.title.assert_called_once_with('Configure Files')

        # 2. Verify Buttons were created with mnemonics (underline=0)
        self.assertEqual(mock_button.call_count, 2)
        button_args = [call[1] for call in mock_button.call_args_list]
        self.assertEqual(button_args[0].get('text'), "Ok")
        self.assertEqual(button_args[0].get('underline'), 0)
        self.assertEqual(button_args[1].get('text'), "Cancel")
        self.assertEqual(button_args[1].get('underline'), 0)

        # 3. Verify window protocol and key bindings were configured
        mock_toplevel_inst.protocol.assert_called_once_with("WM_DELETE_WINDOW", dialog._on_cancel)
        bind_calls = [call[0][0] for call in mock_toplevel_inst.bind.call_args_list]
        self.assertIn("<Escape>", bind_calls)
        self.assertIn("<Alt-o>", bind_calls)
        self.assertIn("<Alt-O>", bind_calls)
        self.assertIn("<Alt-c>", bind_calls)
        self.assertIn("<Alt-C>", bind_calls)

        # 4. Verify _on_ok logic updates input_value and destroys window
        dialog._on_ok()
        self.assertIn("item1", dialog.input_value.split(";"))
        self.assertIn("item2", dialog.input_value.split(";"))
        mock_toplevel_inst.destroy.assert_called_once()

    @patch('tkinter.Toplevel')
    @patch('tkinter.Frame')
    @patch('tkinter.Text')
    @patch('tkinter.Button')
    def test_dialog_on_cancel(self, mock_button, mock_text, mock_frame, mock_toplevel):
        mock_toplevel_inst = MagicMock()
        mock_toplevel.return_value = mock_toplevel_inst

        parent = DummyTk()

        from o3de.ui.multiple_entry import Dialog

        dialog = Dialog(parent, "item1;item2")
        dialog._on_cancel()

        mock_toplevel_inst.destroy.assert_called_once()
