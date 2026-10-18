#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import sys
import os
from unittest.mock import MagicMock, patch

# Mock sys.modules['tkinter'] to prevent loading native _tkinter.so (AppKit/Cocoa) on headless macOS/iOS CI runners
class DummyTkRoot:
    def __init__(self, *args, **kwargs):
        self._last_child_ids = None
        self.children = {}
        self._w = '.'
        self.tk = MagicMock()
    def winfo_pointerx(self): return 0
    def winfo_pointery(self): return 0
    def geometry(self, geom): pass
    def title(self, title): pass
    def rowconfigure(self, index, **kwargs): pass
    def columnconfigure(self, index, **kwargs): pass
    def bind(self, event, cb): pass

mock_tk = MagicMock()
mock_tk.Tk = DummyTkRoot
mock_tk.DISABLED = 'disabled'
mock_tk.NORMAL = 'normal'
mock_tk.W = 'w'
mock_tk.E = 'e'
mock_tk.EW = 'ew'
mock_tk.NSEW = 'nsew'
mock_tk.LEFT = 'left'
mock_tk.SOLID = 'solid'
mock_tk.WORD = 'word'
mock_tk.SUNKEN = 'sunken'
mock_tk.VERTICAL = 'vertical'

sys.modules['tkinter'] = mock_tk
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()

import unittest

# Add current directory to path so wait_dialog can be imported
sys.path.insert(0, os.path.dirname(__file__))

class DummyTk:
    def __init__(self):
        self._last_child_ids = None
    def winfo_x(self):
        return 100
    def winfo_y(self):
        return 100
    def winfo_width(self):
        return 800
    def winfo_height(self):
        return 600
    def focus_set(self):
        pass

class TestWaitDialog(unittest.TestCase):
    @patch('tkinter.Toplevel')
    @patch('tkinter.Label')
    @patch('tkinter.Button')
    @patch('tkinter.StringVar')
    def test_wait_dialog_initialization_and_bindings(self, mock_stringvar, mock_button, mock_label, mock_toplevel):
        # Set up mock instances
        mock_dialog_inst = MagicMock()
        mock_toplevel.return_value = mock_dialog_inst

        mock_button_inst = MagicMock()
        mock_button.return_value = mock_button_inst

        mock_stringvar_inst = MagicMock()
        mock_stringvar_inst.get.return_value = ""
        mock_stringvar.return_value = mock_stringvar_inst

        # Callback for cancel
        cancel_called = False
        def dummy_cancel_cb():
            nonlocal cancel_called
            cancel_called = True

        parent = DummyTk()

        # Import WaitDialog
        from wait_dialog import WaitDialog

        # Instantiate WaitDialog
        dialog = WaitDialog(parent, "Please wait...", dummy_cancel_cb)

        # 1. Verify Toplevel dialog was created with parent
        mock_toplevel.assert_called_once_with(parent)

        # 2. Verify window setup
        mock_dialog_inst.title.assert_called_once_with("Operation In Progress...")
        mock_dialog_inst.grab_set.assert_called_once()

        # 3. Verify Button was created with underline=0 and correct text
        mock_button.assert_called_once()
        kwargs = mock_button.call_args[1]
        self.assertEqual(kwargs.get('text'), "Cancel")
        self.assertEqual(kwargs.get('underline'), 0)

        # 4. Verify bindings were set up for Escape, Alt-c, Alt-C
        bind_calls = [call[0][0] for call in mock_dialog_inst.bind.call_args_list]
        self.assertIn("<Escape>", bind_calls)
        self.assertIn("<Alt-c>", bind_calls)
        self.assertIn("<Alt-C>", bind_calls)

        # 5. Verify protocol for WM_DELETE_WINDOW was registered
        mock_dialog_inst.protocol.assert_called_once_with("WM_DELETE_WINDOW", dialog._on_cancel_button)

        # 6. Test cancellation triggers the callback and close
        dialog._on_cancel_button()
        self.assertTrue(cancel_called)
        mock_dialog_inst.destroy.assert_called_once()

        # 7. Verify on_tick cycles progress correctly
        dialog.on_tick(0.25)
        mock_stringvar_inst.set.assert_called_with("*")


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
        mock_tip_window = MagicMock()
        mock_toplevel.return_value = mock_tip_window

        mock_label_inst = MagicMock()
        mock_label.return_value = mock_label_inst

        from main import _ToolTip

        widget = DummyWidget()
        tooltip = _ToolTip(widget, "Test ToolTip text")

        self.assertIn("<Enter>", widget.bindings)
        self.assertIn("<Leave>", widget.bindings)
        self.assertIn("<ButtonPress>", widget.bindings)

        widget.bindings["<Enter>"](None)
        self.assertIsNotNone(widget.after_id)
        self.assertIsNotNone(widget.after_func)

        widget.after_func()

        mock_toplevel.assert_called_once_with(widget)
        mock_tip_window.wm_overrideredirect.assert_called_once_with(True)
        mock_tip_window.wm_geometry.assert_called_once()

        mock_label.assert_called_once()
        self.assertEqual(mock_label.call_args[1].get("text"), "Test ToolTip text")
        mock_label_inst.pack.assert_called_once()

        widget.bindings["<Leave>"](None)
        mock_tip_window.destroy.assert_called_once()
        self.assertIsNone(tooltip.tip_window)
        self.assertIsNone(tooltip.id)

    @patch('tkinter.Label')
    @patch('tkinter.Entry')
    @patch('tkinter.StringVar')
    def test_add_label_entry_click_focus(self, mock_string_var, mock_entry_cls, mock_label_cls):
        from main import TkApp
        mock_label = MagicMock()
        mock_entry = MagicMock()
        mock_label_cls.return_value = mock_label
        mock_entry_cls.return_value = mock_entry
        mock_entry.__getitem__.side_effect = lambda key: 'normal' if key == 'state' else None

        parent_frame = MagicMock()

        TkApp._add_label_entry(None, parent_frame, "Test Label", "Default Value")

        self.assertTrue(mock_label.bind.called)
        bind_args = mock_label.bind.call_args
        self.assertEqual(bind_args[0][0], "<Button-1>")
        callback = bind_args[0][1]

        callback(None)
        mock_entry.focus_set.assert_called_once()
