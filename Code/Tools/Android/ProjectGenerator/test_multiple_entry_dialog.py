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

# Prevent SIGABRT crashes on macOS CI runners when importing native tkinter (_tkinter.so)
if sys.platform == 'darwin':
    sys.modules['tkinter'] = MagicMock()
    sys.modules['tkinter.filedialog'] = MagicMock()
    sys.modules['tkinter.messagebox'] = MagicMock()

# Add scripts/o3de path so multiple_entry can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../scripts/o3de")))

class DummyTk:
    def __init__(self):
        self._last_child_ids = None
    def winfo_rootx(self):
        return 100
    def winfo_rooty(self):
        return 100

@unittest.skipIf(sys.platform == 'darwin', "Skip Tkinter GUI tests on macOS runners to prevent native _tkinter SIGABRT crashes")
class TestMultipleEntryDialog(unittest.TestCase):
    @patch('tkinter.Toplevel')
    @patch('tkinter.Frame')
    @patch('tkinter.Text')
    @patch('tkinter.Button')
    def test_multiple_entry_dialog_initialization_and_bindings(self, mock_button, mock_text, mock_frame, mock_toplevel):
        mock_toplevel_inst = MagicMock()
        mock_toplevel.return_value = mock_toplevel_inst

        mock_button_inst = MagicMock()
        mock_button.return_value = mock_button_inst

        mock_text_inst = MagicMock()
        mock_text.return_value = mock_text_inst

        parent = DummyTk()

        from o3de.ui.multiple_entry import Dialog

        dialog = Dialog(parent, "entry1;entry2")

        # 1. Verify Toplevel was initialized with parent
        mock_toplevel.assert_called_once_with(parent)

        # 2. Verify window title and geometry
        mock_toplevel_inst.title.assert_called_once_with("Configure Files")

        # 3. Verify Ok and Cancel buttons created with underline=0 mnemonics
        self.assertEqual(mock_button.call_count, 2)
        btn_calls = mock_button.call_args_list
        btn_ok_kwargs = btn_calls[0][1]
        btn_cancel_kwargs = btn_calls[1][1]

        self.assertEqual(btn_ok_kwargs.get('text'), "Ok")
        self.assertEqual(btn_ok_kwargs.get('underline'), 0)
        self.assertEqual(btn_cancel_kwargs.get('text'), "Cancel")
        self.assertEqual(btn_cancel_kwargs.get('underline'), 0)

        # 4. Verify WM_DELETE_WINDOW protocol was set to _on_cancel
        mock_toplevel_inst.protocol.assert_called_once_with("WM_DELETE_WINDOW", dialog._on_cancel)

        # 5. Verify keyboard bindings for Escape, Alt-o, Alt-O, Alt-c, Alt-C
        bind_calls = [call[0][0] for call in mock_toplevel_inst.bind.call_args_list]
        self.assertIn("<Escape>", bind_calls)
        self.assertIn("<Alt-o>", bind_calls)
        self.assertIn("<Alt-O>", bind_calls)
        self.assertIn("<Alt-c>", bind_calls)
        self.assertIn("<Alt-C>", bind_calls)

        # 6. Verify _on_cancel destroys window
        dialog._on_cancel()
        mock_toplevel_inst.destroy.assert_called_once()
