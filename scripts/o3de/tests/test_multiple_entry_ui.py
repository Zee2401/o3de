#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import unittest
from unittest.mock import MagicMock, patch


class DummyTk:
    def winfo_rootx(self):
        return 100

    def winfo_rooty(self):
        return 100


class TestMultipleEntryDialog(unittest.TestCase):
    @patch('tkinter.Toplevel')
    @patch('tkinter.Text')
    @patch('tkinter.Button')
    @patch('tkinter.Frame')
    def test_dialog_initialization_and_accessibility(self, mock_frame, mock_button, mock_text, mock_toplevel):
        mock_root = MagicMock()
        mock_toplevel.return_value = mock_root

        mock_text_inst = MagicMock()
        mock_text.return_value = mock_text_inst

        mock_button_inst = MagicMock()
        mock_button.return_value = mock_button_inst

        parent = DummyTk()

        from o3de.ui.multiple_entry import Dialog

        dialog = Dialog(parent, input_value="foo; bar")

        # 1. Verify Toplevel setup
        mock_toplevel.assert_called_once_with(parent)
        mock_root.title.assert_called_once_with('Configure Files')

        # 2. Verify text entry initialization and focus
        mock_text_inst.insert.assert_called_once()
        mock_text_inst.focus_set.assert_called_once()

        # 3. Verify buttons have underline=0 mnemonics
        self.assertEqual(mock_button.call_count, 2)
        ok_kwargs = mock_button.call_args_list[0][1]
        cancel_kwargs = mock_button.call_args_list[1][1]

        self.assertEqual(ok_kwargs.get('text'), "Ok")
        self.assertEqual(ok_kwargs.get('underline'), 0)
        self.assertEqual(cancel_kwargs.get('text'), "Cancel")
        self.assertEqual(cancel_kwargs.get('underline'), 0)

        # 4. Verify keyboard shortcuts were bound
        bound_events = [call[0][0] for call in mock_root.bind.call_args_list]
        self.assertIn("<Escape>", bound_events)
        self.assertIn("<Alt-o>", bound_events)
        self.assertIn("<Alt-O>", bound_events)
        self.assertIn("<Alt-c>", bound_events)
        self.assertIn("<Alt-C>", bound_events)

        # 5. Verify WM_DELETE_WINDOW window protocol registration
        mock_root.protocol.assert_called_once_with("WM_DELETE_WINDOW", dialog._on_cancel)

    @patch('tkinter.Toplevel')
    @patch('tkinter.Text')
    @patch('tkinter.Button')
    @patch('tkinter.Frame')
    def test_on_ok_and_on_cancel(self, mock_frame, mock_button, mock_text, mock_toplevel):
        mock_root = MagicMock()
        mock_toplevel.return_value = mock_root

        mock_text_inst = MagicMock()
        mock_text_inst.get.return_value = "item1\nitem2\n"
        mock_text.return_value = mock_text_inst

        parent = DummyTk()

        from o3de.ui.multiple_entry import Dialog

        dialog = Dialog(parent, input_value="")
        dialog._on_ok()

        self.assertIn("item1", dialog.input_value)
        self.assertIn("item2", dialog.input_value)
        mock_root.destroy.assert_called_once()

        mock_root.reset_mock()
        dialog._on_cancel()
        mock_root.destroy.assert_called_once()


if __name__ == '__main__':
    unittest.main()
