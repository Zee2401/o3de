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

# Mock tkinter modules prior to importing main to prevent loading native Cocoa _tkinter.so on headless macOS runners
mock_tk = MagicMock()
class DummyTkRoot:
    def __init__(self, *args, **kwargs):
        pass
mock_tk.Tk = DummyTkRoot
mock_tk.DISABLED = "disabled"
mock_tk.NORMAL = "normal"
mock_tk.W = "w"
mock_tk.E = "e"
mock_tk.EW = "ew"
mock_tk.NSEW = "nsew"
mock_tk.SOLID = "solid"
mock_tk.LEFT = "left"
mock_tk.RIGHT = "right"
mock_tk.WORD = "word"
mock_tk.VERTICAL = "vertical"
mock_tk.END = "end"

sys.modules['tkinter'] = mock_tk
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()

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

    @patch('tkinter.Label')
    @patch('tkinter.Entry')
    @patch('tkinter.StringVar')
    def test_add_label_entry_show_and_focus_binding(self, mock_stringvar, mock_entry_cls, mock_label_cls):
        mock_label_inst = MagicMock()
        mock_label_cls.return_value = mock_label_inst
        mock_label_inst.grid_info.return_value = {"row": 0}

        mock_entry_inst = MagicMock()
        mock_entry_cls.return_value = mock_entry_inst
        mock_entry_inst.cget.return_value = "normal"

        from main import TkApp

        parent_frame = MagicMock()
        string_var, entry, row = TkApp._add_label_entry(None, parent_frame, "Password", "secret", show="*")

        # 1. Verify Entry was called with show="*"
        mock_entry_cls.assert_called_once()
        self.assertEqual(mock_entry_cls.call_args[1].get("show"), "*")

        # 2. Verify Label was bound to <Button-1>
        mock_label_inst.bind.assert_called_once()
        self.assertEqual(mock_label_inst.bind.call_args[0][0], "<Button-1>")

        # 3. Trigger the callback and verify entry focus_set was invoked
        callback = mock_label_inst.bind.call_args[0][1]
        callback(None)
        mock_entry_inst.focus_set.assert_called_once()
