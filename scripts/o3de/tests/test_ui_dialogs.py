#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import pytest
from unittest.mock import MagicMock, patch, ANY

import o3de.ui.multiple_entry as multiple_entry
import o3de.ui.multiple_file_picker as multiple_file_picker


def test_multiple_entry_dialog_initialization_and_shortcuts():
    mock_parent = MagicMock()
    mock_parent.winfo_rootx.return_value = 100
    mock_parent.winfo_rooty.return_value = 100

    with patch("tkinter.Toplevel") as mock_toplevel_cls, \
         patch("tkinter.Frame"), \
         patch("tkinter.Text") as mock_text_cls, \
         patch("tkinter.Button") as mock_button_cls:

        mock_root = MagicMock()
        mock_toplevel_cls.return_value = mock_root
        mock_text = MagicMock()
        mock_text_cls.return_value = mock_text

        dialog = multiple_entry.Dialog(mock_parent, "item1; item2")

        # Verify title update and focus
        mock_root.title.assert_called_with("Configure Entries")
        mock_text.focus_set.assert_called_once()

        # Verify protocol and key bindings registered
        mock_root.protocol.assert_called_with("WM_DELETE_WINDOW", dialog._on_cancel)
        bound_events = [call[0][0] for call in mock_root.bind.call_args_list]
        assert "<Escape>" in bound_events
        assert "<Alt-o>" in bound_events
        assert "<Alt-c>" in bound_events

        # Test _on_ok and _on_cancel
        mock_text.get.return_value = "item1\nitem2\nitem3\n"
        dialog._on_ok()
        assert set(dialog.input_value.split(";")) == {"item1", "item2", "item3"}
        mock_root.destroy.assert_called()


def test_multiple_file_picker_dialog_initialization_and_shortcuts():
    mock_parent = MagicMock()
    mock_parent.winfo_rootx.return_value = 100
    mock_parent.winfo_rooty.return_value = 100

    with patch("tkinter.Toplevel") as mock_toplevel_cls, \
         patch("tkinter.Frame"), \
         patch("tkinter.Listbox") as mock_listbox_cls, \
         patch("tkinter.Button") as mock_button_cls, \
         patch("tkinter.filedialog.askopenfilename", return_value="/path/to/file.txt"):

        mock_root = MagicMock()
        mock_toplevel_cls.return_value = mock_root
        mock_listbox = MagicMock()
        mock_listbox_cls.return_value = mock_listbox

        dialog = multiple_file_picker.Dialog(mock_parent, initial_list="file1.txt; file2.txt")

        # Verify listbox keyboard binding for Delete
        mock_listbox.bind.assert_called_with("<Delete>", ANY)

        # Verify bindings on root window
        bound_events = [call[0][0] for call in mock_root.bind.call_args_list]
        assert "<Escape>" in bound_events
        assert "<Alt-a>" in bound_events
        assert "<Alt-r>" in bound_events

        # Test adding a file
        dialog._choose_file()
        assert "/path/to/file.txt" in dialog.items

        # Test _on_close
        dialog._on_close()
        mock_root.destroy.assert_called()
