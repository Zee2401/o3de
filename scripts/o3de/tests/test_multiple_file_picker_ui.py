#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

from unittest.mock import MagicMock, patch
import pytest

from o3de.ui import multiple_file_picker


@pytest.fixture
def mock_tkinter():
    with patch("o3de.ui.multiple_file_picker.tk.Toplevel") as mock_toplevel, \
         patch("o3de.ui.multiple_file_picker.tk.Frame") as mock_frame, \
         patch("o3de.ui.multiple_file_picker.tk.Listbox") as mock_listbox, \
         patch("o3de.ui.multiple_file_picker.tk.Button") as mock_button, \
         patch("o3de.ui.multiple_file_picker.filedialog") as mock_filedialog:

        mock_parent = MagicMock()
        mock_parent.winfo_rootx.return_value = 100
        mock_parent.winfo_rooty.return_value = 100

        mock_top_inst = MagicMock()
        mock_toplevel.return_value = mock_top_inst

        mock_listbox_inst = MagicMock()
        mock_listbox.return_value = mock_listbox_inst

        yield {
            "parent": mock_parent,
            "toplevel": mock_toplevel,
            "toplevel_inst": mock_top_inst,
            "frame": mock_frame,
            "listbox": mock_listbox,
            "listbox_inst": mock_listbox_inst,
            "button": mock_button,
            "filedialog": mock_filedialog,
        }


def test_dialog_init(mock_tkinter):
    initial = "file1.txt; file2.txt"
    dialog = multiple_file_picker.Dialog(parent=mock_tkinter["parent"], initial_list=initial)

    assert dialog.items == {"file1.txt", "file2.txt"}

    top_inst = mock_tkinter["toplevel_inst"]
    top_inst.protocol.assert_called_with("WM_DELETE_WINDOW", dialog._on_close)
    top_inst.bind.assert_any_call("<Escape>", dialog._on_close)
    top_inst.bind.assert_any_call("<Alt-a>", dialog._choose_file)
    top_inst.bind.assert_any_call("<Alt-A>", dialog._choose_file)
    top_inst.bind.assert_any_call("<Alt-r>", dialog._remove_file)
    top_inst.bind.assert_any_call("<Alt-R>", dialog._remove_file)
    mock_tkinter["listbox_inst"].bind.assert_called_with("<Delete>", dialog._remove_file)


def test_dialog_choose_file(mock_tkinter):
    dialog = multiple_file_picker.Dialog(parent=mock_tkinter["parent"], initial_list="file1.txt")
    mock_tkinter["filedialog"].askopenfilename.return_value = "new_file.txt"

    dialog._choose_file()

    assert "new_file.txt" in dialog.items
    mock_tkinter["listbox_inst"].insert.assert_called_with(0, "new_file.txt")


def test_dialog_choose_file_cancel(mock_tkinter):
    dialog = multiple_file_picker.Dialog(parent=mock_tkinter["parent"], initial_list="file1.txt")
    mock_tkinter["filedialog"].askopenfilename.return_value = ""

    dialog._choose_file()

    assert dialog.items == {"file1.txt"}


def test_dialog_remove_file(mock_tkinter):
    dialog = multiple_file_picker.Dialog(parent=mock_tkinter["parent"], initial_list="file1.txt;file2.txt")
    mock_listbox = mock_tkinter["listbox_inst"]
    mock_listbox.curselection.return_value = (0,)
    mock_listbox.get.return_value = "file1.txt"

    dialog._remove_file()

    assert "file1.txt" not in dialog.items
    mock_listbox.delete.assert_called_with(0)


def test_dialog_on_close(mock_tkinter):
    dialog = multiple_file_picker.Dialog(parent=mock_tkinter["parent"])
    dialog._on_close()

    mock_tkinter["toplevel_inst"].destroy.assert_called_once()
