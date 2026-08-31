#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import importlib
import sys
import unittest
from unittest.mock import MagicMock, patch


class TestMultipleEntryDialog(unittest.TestCase):
    def _get_mock_tk(self):
        mock_tk = MagicMock()
        mock_tk.END = "end"
        mock_tk.SOLID = "solid"
        mock_tk.NSEW = "nsew"
        mock_tk.N = "n"
        mock_tk.E = "e"
        return mock_tk

    def test_dialog_initialization_and_accessibility(self):
        mock_tk = self._get_mock_tk()
        mock_root = MagicMock()
        mock_tk.Toplevel.return_value = mock_root

        mock_text_inst = MagicMock()
        mock_tk.Text.return_value = mock_text_inst

        mock_button_inst = MagicMock()
        mock_tk.Button.return_value = mock_button_inst

        with patch.dict('sys.modules', {'tkinter': mock_tk, 'tkinter.filedialog': MagicMock()}):
            import o3de.ui.multiple_entry
            importlib.reload(o3de.ui.multiple_entry)
            from o3de.ui.multiple_entry import Dialog

            parent = MagicMock()
            parent.winfo_rootx.return_value = 100
            parent.winfo_rooty.return_value = 100

            dialog = Dialog(parent, input_value="foo; bar")

            # 1. Verify Toplevel setup
            mock_tk.Toplevel.assert_called_once_with(parent)
            mock_root.title.assert_called_once_with('Configure Files')

            # 2. Verify text entry initialization and focus
            mock_text_inst.insert.assert_called_once()
            mock_text_inst.focus_set.assert_called_once()

            # 3. Verify buttons have underline=0 mnemonics
            self.assertEqual(mock_tk.Button.call_count, 2)
            ok_kwargs = mock_tk.Button.call_args_list[0][1]
            cancel_kwargs = mock_tk.Button.call_args_list[1][1]

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

    def test_on_ok_and_on_cancel(self):
        mock_tk = self._get_mock_tk()
        mock_root = MagicMock()
        mock_tk.Toplevel.return_value = mock_root

        mock_text_inst = MagicMock()
        mock_text_inst.get.return_value = "item1\nitem2\n"
        mock_tk.Text.return_value = mock_text_inst

        with patch.dict('sys.modules', {'tkinter': mock_tk, 'tkinter.filedialog': MagicMock()}):
            import o3de.ui.multiple_entry
            importlib.reload(o3de.ui.multiple_entry)
            from o3de.ui.multiple_entry import Dialog

            parent = MagicMock()
            parent.winfo_rootx.return_value = 100
            parent.winfo_rooty.return_value = 100

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
