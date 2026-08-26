#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import pytest
from unittest.mock import MagicMock, patch
from o3de.ui import multiple_file_picker


class DummyParent(object):
    def winfo_rootx(self):
        return 100

    def winfo_rooty(self):
        return 100


def test_multiple_file_picker_init():
    parent = DummyParent()
    with patch('tkinter.Toplevel') as mock_toplevel:
        mock_root = MagicMock()
        mock_toplevel.return_value = mock_root

        dialog = multiple_file_picker.Dialog(parent, initial_list="file1.txt;file2.txt")

        assert "file1.txt" in dialog.items
        assert "file2.txt" in dialog.items
        assert mock_root.bind.called
        assert mock_root.protocol.called


def test_multiple_file_picker_choose_file():
    parent = DummyParent()
    with patch('tkinter.Toplevel') as mock_toplevel, \
         patch('tkinter.filedialog.askopenfilename', return_value="/path/to/new_file.txt"):
        mock_root = MagicMock()
        mock_toplevel.return_value = mock_root

        dialog = multiple_file_picker.Dialog(parent, initial_list="")
        dialog._choose_file()

        assert "/path/to/new_file.txt" in dialog.items


def test_multiple_file_picker_remove_file():
    parent = DummyParent()
    with patch('tkinter.Toplevel') as mock_toplevel:
        mock_root = MagicMock()
        mock_toplevel.return_value = mock_root

        dialog = multiple_file_picker.Dialog(parent, initial_list="file1.txt;file2.txt")

        # Mock listbox curselection and get
        dialog.file_list_box.curselection = MagicMock(return_value=(0,))
        dialog.file_list_box.get = MagicMock(return_value="file1.txt")

        dialog._remove_file()

        assert "file1.txt" not in dialog.items
        assert "file2.txt" in dialog.items
