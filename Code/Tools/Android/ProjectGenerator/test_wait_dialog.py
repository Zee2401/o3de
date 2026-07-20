#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import sys
import os
from unittest.mock import MagicMock, patch
import pytest

# Add the directory to path so wait_dialog can be imported
sys.path.append(os.path.dirname(__file__))

from wait_dialog import WaitDialog


def test_wait_dialog_escape_binding():
    # Setup mocks
    mock_parent = MagicMock()
    mock_parent.winfo_x.return_value = 100
    mock_parent.winfo_y.return_value = 100
    mock_parent.winfo_width.return_value = 500
    mock_parent.winfo_height.return_value = 500

    mock_cancel_cb = MagicMock()

    # We will mock tk.Toplevel, tk.Label, tk.StringVar, tk.Button
    # so we don't need a real Tcl/Tk graphics environment in headless CI.
    with patch('tkinter.Toplevel') as mock_toplevel_cls, \
         patch('tkinter.Label') as mock_label_cls, \
         patch('tkinter.StringVar') as mock_stringvar_cls, \
         patch('tkinter.Button') as mock_button_cls:

        mock_dialog_instance = MagicMock()
        mock_toplevel_cls.return_value = mock_dialog_instance

        # Create WaitDialog instance
        wait_dialog = WaitDialog(mock_parent, "Test Work Message", mock_cancel_cb)

        # 1. Assert Toplevel was instantiated correctly
        mock_toplevel_cls.assert_called_once_with(mock_parent)

        # 2. Assert escape key was bound
        escape_bind_call = None
        for call in mock_dialog_instance.bind.call_args_list:
            args, kwargs = call
            if args[0] == "<Escape>":
                escape_bind_call = call
                break

        assert escape_bind_call is not None, "Escape key was not bound to the dialog"

        # 3. Verify that calling the bound lambda triggers the cancellation callback
        bound_func = escape_bind_call[0][1]

        # Reset any call history on mock_cancel_cb
        mock_cancel_cb.reset_mock()
        mock_dialog_instance.destroy.reset_mock()

        # Trigger the bound function (simulating pressing Escape key)
        dummy_event = MagicMock()
        bound_func(dummy_event)

        # Verify that the cancel callback was invoked
        mock_cancel_cb.assert_called_once()
        # Verify that the dialog was destroyed/closed
        mock_dialog_instance.destroy.assert_called_once()


def test_wait_dialog_on_tick():
    mock_parent = MagicMock()
    mock_parent.winfo_x.return_value = 100
    mock_parent.winfo_y.return_value = 100
    mock_parent.winfo_width.return_value = 500
    mock_parent.winfo_height.return_value = 500

    mock_cancel_cb = MagicMock()

    with patch('tkinter.Toplevel'), \
         patch('tkinter.Label'), \
         patch('tkinter.StringVar') as mock_stringvar_cls, \
         patch('tkinter.Button'):

        # Mock the StringVar behavior so get/set work normally
        mock_stringvar_inst = MagicMock()
        current_val = [""]
        def mock_set(val):
            current_val[0] = val
        def mock_get():
            return current_val[0]
        mock_stringvar_inst.set.side_effect = mock_set
        mock_stringvar_inst.get.side_effect = mock_get
        mock_stringvar_cls.return_value = mock_stringvar_inst

        wait_dialog = WaitDialog(mock_parent, "Test", mock_cancel_cb)

        # On tick starts with sign 1 and ""
        assert wait_dialog._progress_string_var.get() == ""

        # Tick 1 -> "*"
        wait_dialog.on_tick(0.25)
        assert wait_dialog._progress_string_var.get() == "*"
        assert wait_dialog._progress_sign == 1

        # Tick 2 -> "**"
        wait_dialog.on_tick(0.25)
        assert wait_dialog._progress_string_var.get() == "**"
        assert wait_dialog._progress_sign == 1

        # Tick 3 -> "***"
        wait_dialog.on_tick(0.25)
        assert wait_dialog._progress_string_var.get() == "***"
        assert wait_dialog._progress_sign == 1

        # Tick 4 -> "****" -> and sign becomes -1 because len(progress) >= MAX_DOTS
        wait_dialog.on_tick(0.25)
        assert wait_dialog._progress_string_var.get() == "****"
        assert wait_dialog._progress_sign == -1

        # Tick 5 -> progress becomes "***" (len of "****" - 1)
        wait_dialog.on_tick(0.25)
        assert wait_dialog._progress_string_var.get() == "***"
