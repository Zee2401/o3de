#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import sys
import unittest

if sys.platform == 'darwin':
    raise unittest.SkipTest("Skip Tkinter UI unit tests on macOS headless environments to avoid SIGABRT")

from unittest.mock import MagicMock, patch


class DummyTk:
    def __init__(self):
        self._last_child_ids = None

    def winfo_rootx(self):
        return 100

    def winfo_rooty(self):
        return 100

    def focus_set(self):
        pass


class TestMultipleEntryUI(unittest.TestCase):
    def test_dialog_initialization_and_bindings(self):
        with patch('tkinter.Toplevel') as mock_toplevel, \
             patch('tkinter.Frame') as mock_frame, \
             patch('tkinter.Text') as mock_text, \
             patch('tkinter.Button') as mock_button, \
             patch('tkinter.Scrollbar') as mock_scrollbar:

            mock_dialog_inst = MagicMock()
            mock_toplevel.return_value = mock_dialog_inst

            mock_button_inst = MagicMock()
            mock_button.return_value = mock_button_inst

            mock_text_inst = MagicMock()
            mock_text.return_value = mock_text_inst

            parent = DummyTk()

            from o3de.ui.multiple_entry import Dialog

            dialog = Dialog(parent, "item1;item2")

            # 1. Verify Toplevel dialog was created with parent
            mock_toplevel.assert_called_once_with(parent)

            # 2. Verify window setup
            mock_dialog_inst.title.assert_called_once_with('Configure Files')

            # 3. Verify Buttons were created with mnemonics (underline=0)
            button_calls = mock_button.call_args_list
            self.assertGreaterEqual(len(button_calls), 2)
            ok_kwargs = button_calls[0][1]
            cancel_kwargs = button_calls[1][1]
            self.assertEqual(ok_kwargs.get('text'), "Ok")
            self.assertEqual(ok_kwargs.get('underline'), 0)
            self.assertEqual(cancel_kwargs.get('text'), "Cancel")
            self.assertEqual(cancel_kwargs.get('underline'), 0)

            # 4. Verify bindings were set up for Escape, Alt-o, Alt-O, Alt-c, Alt-C
            bind_calls = [call[0][0] for call in mock_dialog_inst.bind.call_args_list]
            self.assertIn("<Escape>", bind_calls)
            self.assertIn("<Alt-o>", bind_calls)
            self.assertIn("<Alt-O>", bind_calls)
            self.assertIn("<Alt-c>", bind_calls)
            self.assertIn("<Alt-C>", bind_calls)

            # 5. Verify protocol for WM_DELETE_WINDOW was registered
            mock_dialog_inst.protocol.assert_called_once_with("WM_DELETE_WINDOW", dialog._on_cancel)

            # 6. Test cancellation destroys root window
            dialog._on_cancel()
            mock_dialog_inst.destroy.assert_called_once()
