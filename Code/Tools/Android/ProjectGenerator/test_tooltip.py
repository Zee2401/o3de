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

# Create dummy Tkinter mock in sys.modules to prevent loading native _tkinter.so (Cocoa AppKit) on headless macOS CI runners
class DummyTkRoot:
    def __init__(self, *args, **kwargs):
        self._last_child_ids = {}
        self.children = {}
        self._w = '.'
        self.tk = MagicMock()
    def title(self, *args, **kwargs):
        pass
    def geometry(self, *args, **kwargs):
        pass
    def columnconfigure(self, *args, **kwargs):
        pass
    def rowconfigure(self, *args, **kwargs):
        pass
    def bind(self, *args, **kwargs):
        pass
    def winfo_pointerx(self):
        return 0
    def winfo_pointery(self):
        return 0

if 'tkinter' not in sys.modules or not isinstance(sys.modules['tkinter'], MagicMock):
    mock_tk = MagicMock()
    mock_tk.Tk = DummyTkRoot
    mock_tk.DISABLED = 'disabled'
    mock_tk.NORMAL = 'normal'
    mock_tk.W = 'w'
    mock_tk.E = 'e'
    mock_tk.EW = 'ew'
    mock_tk.NSEW = 'nsew'
    mock_tk.SOLID = 'solid'
    mock_tk.SUNKEN = 'sunken'
    mock_tk.WORD = 'word'
    mock_tk.VERTICAL = 'vertical'
    mock_tk.LEFT = 'left'
    mock_tk.RIGHT = 'right'
    mock_tk.END = 'end'
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

    @patch('tkinter.StringVar')
    @patch('tkinter.Entry')
    @patch('tkinter.Label')
    def test_add_label_entry_options_and_focus_binding(self, mock_label_cls, mock_entry_cls, mock_stringvar_cls):
        from main import TkApp

        mock_parent = MagicMock()
        mock_label = MagicMock()
        mock_label.grid_info.return_value = {"row": 2}
        mock_label_cls.return_value = mock_label

        mock_entry = MagicMock()
        mock_entry_cls.return_value = mock_entry

        app = object.__new__(TkApp)

        string_var, entry, row = app._add_label_entry(
            mock_parent, "Test Label", default_value="secret", show="*"
        )

        # Verify Label creation
        mock_label_cls.assert_called_once()
        self.assertEqual(mock_label_cls.call_args[1].get("text"), "Test Label")

        # Verify Entry creation with show="*" option
        mock_entry_cls.assert_called_once()
        self.assertEqual(mock_entry_cls.call_args[1].get("show"), "*")

        # Verify label click binding for focus set
        mock_label.bind.assert_called_once()
        self.assertEqual(mock_label.bind.call_args[0][0], "<Button-1>")

        # Simulate click on label
        click_cb = mock_label.bind.call_args[0][1]
        click_cb(None)
        mock_entry.focus_set.assert_called_once()
