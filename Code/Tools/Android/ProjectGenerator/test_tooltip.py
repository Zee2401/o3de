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

    @patch('main._ToolTip')
    @patch('tkinter.LabelFrame')
    @patch('tkinter.Label')
    @patch('tkinter.Button')
    @patch('tkinter.Entry')
    @patch('tkinter.Checkbutton')
    @patch('tkinter.Text')
    @patch('tkinter.Scrollbar')
    @patch('tkinter.BooleanVar')
    @patch('tkinter.StringVar')
    def test_tkapp_tooltips_instantiation(self, mock_strvar, mock_boolvar, mock_scroll, mock_text, mock_check, mock_entry, mock_btn, mock_lbl, mock_frame, mock_tooltip):
        import tkinter as tk

        class DummyTkRoot:
            def __init__(self, *args, **kwargs):
                self._last_child_ids = {}
                self.children = {}
                self._w = '.'
                self.tk = MagicMock()
            def winfo_pointerx(self): return 100
            def winfo_pointery(self): return 100
            def geometry(self, *a): pass
            def title(self, *a): pass
            def columnconfigure(self, *a, **kw): pass
            def rowconfigure(self, *a, **kw): pass
            def bind(self, *a, **kw): pass

        from main import TkApp
        from config_data import ConfigData

        orig_bases = TkApp.__bases__
        try:
            TkApp.__bases__ = (DummyTkRoot,)
            tk._default_root = DummyTkRoot()
            config = ConfigData()
            app = TkApp(config)

            # Check tooltip calls
            tooltip_texts = [call[0][1] for call in mock_tooltip.call_args_list]

            self.assertTrue(any("Alt+L" in text for text in tooltip_texts))
            self.assertTrue(any("Alt+S" in text for text in tooltip_texts))
            self.assertTrue(any("Alt+C" in text for text in tooltip_texts))
            self.assertTrue(any("Alt+G" in text for text in tooltip_texts))
            self.assertTrue(any("Meta Quest" in text for text in tooltip_texts))
        finally:
            TkApp.__bases__ = orig_bases
