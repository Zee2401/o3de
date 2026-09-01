#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import sys
import pytest
from unittest.mock import MagicMock, patch

# In macOS / Darwin CI runners, importing tkinter loads Cocoa _tkinter.so which crashes
# with SIGABRT (exit code 134) when running in headless processes/jobs like AssetBuilder.
# Prevent Cocoa initialization by mocking sys.modules['tkinter'] and related submodules at top-level.
if sys.platform == 'darwin':
    mock_tk = MagicMock()
    sys.modules['tkinter'] = mock_tk
    sys.modules['tkinter.filedialog'] = MagicMock()
    sys.modules['tkinter.messagebox'] = MagicMock()
    sys.modules['tkinter.ttk'] = MagicMock()

pytestmark = pytest.mark.skipif(sys.platform == 'darwin', reason="Tkinter tests skipped on macOS headless runners")


def test_multiple_entry_dialog_ok():
    mock_parent = MagicMock()
    mock_parent.winfo_rootx.return_value = 100
    mock_parent.winfo_rooty.return_value = 100

    with patch('tkinter.Toplevel') as mock_toplevel_cls, \
         patch('tkinter.Text') as mock_text_cls, \
         patch('tkinter.Button') as mock_button_cls, \
         patch('tkinter.Frame') as mock_frame_cls:

        mock_top = MagicMock()
        mock_toplevel_cls.return_value = mock_top

        mock_text_inst = MagicMock()
        mock_text_inst.get.return_value = "file1.txt\nfile2.txt\n"
        mock_text_cls.return_value = mock_text_inst

        from o3de.ui import multiple_entry

        dialog = multiple_entry.Dialog(parent=mock_parent, input_value="file1.txt;file2.txt")

        # Verify keyboard shortcut and protocol bindings
        bind_calls = {c[0][0]: c[0][1] for c in mock_top.bind.call_args_list}
        assert '<Alt-o>' in bind_calls
        assert '<Alt-O>' in bind_calls
        assert '<Alt-c>' in bind_calls
        assert '<Alt-C>' in bind_calls
        assert '<Escape>' in bind_calls

        mock_top.protocol.assert_called_with('WM_DELETE_WINDOW', dialog._on_cancel)

        # Trigger Ok
        dialog._on_ok()
        assert dialog.input_value in ("file1.txt;file2.txt", "file2.txt;file1.txt")
        mock_top.destroy.assert_called_once()


def test_multiple_entry_dialog_cancel():
    mock_parent = MagicMock()
    mock_parent.winfo_rootx.return_value = 100
    mock_parent.winfo_rooty.return_value = 100

    with patch('tkinter.Toplevel') as mock_toplevel_cls, \
         patch('tkinter.Text') as mock_text_cls, \
         patch('tkinter.Button') as mock_button_cls, \
         patch('tkinter.Frame') as mock_frame_cls:

        mock_top = MagicMock()
        mock_toplevel_cls.return_value = mock_top

        from o3de.ui import multiple_entry

        dialog = multiple_entry.Dialog(parent=mock_parent, input_value="initial_value")

        dialog._on_cancel()
        assert dialog.input_value == "initial_value"
        mock_top.destroy.assert_called_once()
