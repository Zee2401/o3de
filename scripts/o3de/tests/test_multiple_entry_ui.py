#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#

import unittest.mock as mock
from unittest.mock import MagicMock, patch
import pytest

from o3de.ui import multiple_entry


class DummyParent:
    def winfo_rootx(self):
        return 100

    def winfo_rooty(self):
        return 100


@patch('tkinter.Toplevel')
@patch('tkinter.Frame')
@patch('tkinter.Text')
@patch('tkinter.Button')
def test_dialog_init(mock_button, mock_text, mock_frame, mock_toplevel):
    mock_dialog_inst = MagicMock()
    mock_toplevel.return_value = mock_dialog_inst

    parent = DummyParent()
    dialog = multiple_entry.Dialog(parent=parent, input_value="entry1;entry2")

    assert dialog.input_value == "entry1;entry2"
    mock_toplevel.assert_called_once_with(parent)
    mock_dialog_inst.title.assert_called_once_with('Configure Files')


@patch('tkinter.Toplevel')
@patch('tkinter.Frame')
@patch('tkinter.Text')
@patch('tkinter.Button')
def test_dialog_ok_cancel_shortcuts(mock_button, mock_text, mock_frame, mock_toplevel):
    mock_dialog_inst = MagicMock()
    mock_toplevel.return_value = mock_dialog_inst

    parent = DummyParent()
    dialog = multiple_entry.Dialog(parent=parent, input_value="item1")

    # Verify button creation with underline=0
    button_texts = [call[1].get('text') for call in mock_button.call_args_list]
    button_underlines = [call[1].get('underline') for call in mock_button.call_args_list]

    assert "Ok" in button_texts
    assert "Cancel" in button_texts
    assert button_underlines == [0, 0]

    # Verify shortcut bindings
    bind_calls = [call[0][0] for call in mock_dialog_inst.bind.call_args_list]
    assert "<Escape>" in bind_calls
    assert "<Alt-c>" in bind_calls
    assert "<Alt-C>" in bind_calls
    assert "<Alt-o>" in bind_calls
    assert "<Alt-O>" in bind_calls

    with patch.object(dialog, "_on_cancel") as mock_cancel:
        # Trigger Escape shortcut callback
        escape_call = [call for call in mock_dialog_inst.bind.call_args_list if call[0][0] == "<Escape>"][0]
        escape_call[0][1](None)
        mock_cancel.assert_called_once()

    with patch.object(dialog, "_on_ok") as mock_ok:
        # Trigger Alt-o shortcut callback
        alt_o_call = [call for call in mock_dialog_inst.bind.call_args_list if call[0][0] == "<Alt-o>"][0]
        alt_o_call[0][1](None)
        mock_ok.assert_called_once()


@patch('tkinter.Toplevel')
@patch('tkinter.Frame')
@patch('tkinter.Text')
@patch('tkinter.Button')
def test_dialog_wm_delete_window(mock_button, mock_text, mock_frame, mock_toplevel):
    mock_dialog_inst = MagicMock()
    mock_toplevel.return_value = mock_dialog_inst

    parent = DummyParent()
    dialog = multiple_entry.Dialog(parent=parent, input_value="item1")

    protocol_calls = mock_dialog_inst.protocol.call_args_list
    wm_delete_call = [call for call in protocol_calls if call[0][0] == "WM_DELETE_WINDOW"]
    assert len(wm_delete_call) == 1
    assert wm_delete_call[0][0][1] == dialog._on_cancel
