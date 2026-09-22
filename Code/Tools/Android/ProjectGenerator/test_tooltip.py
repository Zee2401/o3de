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

# Prevent native Cocoa/AppKit _tkinter.so load on headless macOS CI runners during pytest collection
class DummyTkRoot:
    def __init__(self, *args, **kwargs):
        pass

mock_tk = MagicMock()
mock_tk.Tk = DummyTkRoot
mock_tk.DISABLED = 'disabled'
mock_tk.NORMAL = 'normal'
mock_tk.SOLID = 'solid'
mock_tk.LEFT = 'left'
mock_tk.W = 'w'
mock_tk.E = 'e'
mock_tk.EW = 'ew'
mock_tk.NSEW = 'nsew'
mock_tk.WORD = 'word'
mock_tk.SUNKEN = 'sunken'
mock_tk.VERTICAL = 'vertical'
mock_tk.END = 'end'

sys.modules['tkinter'] = mock_tk
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()

# Add current directory to path so main can be imported
sys.path.insert(0, os.path.dirname(__file__))

class DummyWidget:
    def __init__(self):
        self.bindings = {}
        self.after_id = None
        self.after_func = None
        self._exists = True

    def bind(self, event, callback):
        self.bindings[event] = callback

    def after(self, ms, func):
        self.after_id = "after_id_123"
        self.after_func = func
        return self.after_id

    def after_cancel(self, after_id):
        if self.after_id == after_id:
            self.after_id = None
            self.after_func = None

    def winfo_exists(self):
        return self._exists

    def winfo_rootx(self):
        return 100

    def winfo_rooty(self):
        return 100


class TestToolTip(unittest.TestCase):
    @patch('tkinter.Toplevel')
    @patch('tkinter.Label')
    def test_tooltip_creation_and_lifecycle(self, mock_label, mock_toplevel):
        # Set up mock instances
        mock_tip_window = MagicMock()
        mock_toplevel.return_value = mock_tip_window

        mock_label_inst = MagicMock()
        mock_label.return_value = mock_label_inst

        # Import _ToolTip
        from main import _ToolTip

        widget = DummyWidget()
        tooltip = _ToolTip(widget, "Test ToolTip text")

        # 1. Verify bindings were established on initialization
        self.assertIn("<Enter>", widget.bindings)
        self.assertIn("<Leave>", widget.bindings)
        self.assertIn("<ButtonPress>", widget.bindings)

        # 2. Simulate <Enter> event to trigger the timer
        widget.bindings["<Enter>"](None)
        self.assertIsNotNone(widget.after_id)
        self.assertIsNotNone(widget.after_func)

        # 3. Execute the timer's callback
        widget.after_func()

        # 4. Verify Toplevel (the tip window) was created
        mock_toplevel.assert_called_once_with(widget)
        mock_tip_window.wm_overrideredirect.assert_called_once_with(True)
        mock_tip_window.wm_geometry.assert_called_once()

        # 5. Verify Label with the text was packed inside
        mock_label.assert_called_once()
        self.assertEqual(mock_label.call_args[1].get("text"), "Test ToolTip text")
        mock_label_inst.pack.assert_called_once()

        # 6. Simulate <Leave> event to hide and destroy the tooltip
        widget.bindings["<Leave>"](None)
        mock_tip_window.destroy.assert_called_once()
        self.assertIsNone(tooltip.tip_window)
        self.assertIsNone(tooltip.id)

    def test_add_label_entry_masking_and_focus_binding(self):
        mock_label = MagicMock()
        mock_label.grid_info.return_value = {"row": 2}

        mock_entry = MagicMock()

        mock_parent = MagicMock()

        import main
        main.tk.Label = MagicMock(return_value=mock_label)
        main.tk.Entry = MagicMock(return_value=mock_entry)
        main.tk.StringVar = MagicMock()

        app = object.__new__(main.TkApp)

        string_var, entry, row = app._add_label_entry(
            parent_frame=mock_parent,
            lbl_name="Password Field",
            default_value="secret",
            entry_colspan=3,
            label_width=20,
            entry_read_only=False,
            show="*"
        )

        # 1. Verify Entry was initialized with show="*"
        main.tk.Entry.assert_called_once()
        self.assertEqual(main.tk.Entry.call_args[1].get("show"), "*")

        # 2. Verify Label was bound to <Button-1> for click focus
        mock_label.bind.assert_called_once()
        event_name, callback = mock_label.bind.call_args[0]
        self.assertEqual(event_name, "<Button-1>")

        # 3. Simulate clicking label and verify focus_set was called on Entry
        callback(None)
        mock_entry.focus_set.assert_called_once()
