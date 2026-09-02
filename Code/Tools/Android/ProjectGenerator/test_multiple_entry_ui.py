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

class DummyTk:
    def __init__(self):
        self._last_child_ids = None
    def winfo_rootx(self):
        return 100
    def winfo_rooty(self):
        return 100


class TestMultipleEntryUI(unittest.TestCase):
    @patch('tkinter.Toplevel')
    @patch('tkinter.Text')
    @patch('tkinter.Button')
    def test_multiple_entry_dialog_initialization_and_bindings(self, mock_button, mock_text, mock_toplevel):
        mock_toplevel_inst = MagicMock()
        mock_toplevel.return_value = mock_toplevel_inst

        mock_text_inst = MagicMock()
        mock_text.return_value = mock_text_inst

        button_calls = []
        def mock_button_factory(*args, **kwargs):
            m = MagicMock()
            m.kwargs = kwargs
            button_calls.append(kwargs)
            return m
        mock_button.side_effect = mock_button_factory

        from o3de.ui.multiple_entry import Dialog

        parent = DummyTk()
        dialog = Dialog(parent, "item1;item2")

        # 1. Verify Toplevel setup
        mock_toplevel.assert_called_once_with(parent)
        mock_toplevel_inst.title.assert_called_once_with('Configure Files')

        # 2. Verify Text widget populated and focus set
        mock_text_inst.insert.assert_called_once()
        mock_text_inst.focus_set.assert_called_once()

        # 3. Verify Buttons created with underline=0 and correct text
        self.assertEqual(len(button_calls), 2)
        self.assertEqual(button_calls[0].get('text'), "OK")
        self.assertEqual(button_calls[0].get('underline'), 0)
        self.assertEqual(button_calls[1].get('text'), "Cancel")
        self.assertEqual(button_calls[1].get('underline'), 0)

        # 4. Verify keyboard shortcut bindings
        bind_calls = [call[0][0] for call in mock_toplevel_inst.bind.call_args_list]
        self.assertIn("<Escape>", bind_calls)
        self.assertIn("<Alt-o>", bind_calls)
        self.assertIn("<Alt-O>", bind_calls)
        self.assertIn("<Alt-c>", bind_calls)
        self.assertIn("<Alt-C>", bind_calls)

        # 5. Verify WM_DELETE_WINDOW protocol registered
        mock_toplevel_inst.protocol.assert_called_once_with("WM_DELETE_WINDOW", dialog._on_cancel)
