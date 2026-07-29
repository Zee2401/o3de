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

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

class TestTooltip(unittest.TestCase):
    @patch('tkinter.Toplevel')
    @patch('tkinter.Label')
    def test_tooltip_lifecycle(self, mock_label, mock_toplevel):
        # Import _ToolTip from main
        from main import _ToolTip

        mock_master = MagicMock()
        mock_widget = MagicMock()
        mock_widget.winfo_rootx.return_value = 100
        mock_widget.winfo_rooty.return_value = 200
        mock_widget.winfo_height.return_value = 25

        tooltip = _ToolTip(mock_master, delay_ms=100)

        # 1. Test bind_widget sets up bindings
        tooltip.bind_widget(mock_widget, "Test Message")
        self.assertEqual(mock_widget.bind.call_count, 3)

        bind_args = [call[0][0] for call in mock_widget.bind.call_args_list]
        self.assertIn('<Enter>', bind_args)
        self.assertIn('<Leave>', bind_args)
        self.assertIn('<ButtonPress>', bind_args)

        # 2. Test scheduling
        tooltip._schedule(mock_widget, "Test Message")
        mock_master.after.assert_called_once()
        after_args = mock_master.after.call_args[0]
        self.assertEqual(after_args[0], 100) # delay_ms is 100

        # Simulate the timer firing to call show
        after_callback = after_args[1]

        mock_toplevel_inst = MagicMock()
        mock_toplevel.return_value = mock_toplevel_inst

        after_callback()

        # Verify show was called, which creates Toplevel and Label
        mock_toplevel.assert_called_once_with(mock_widget)
        mock_toplevel_inst.wm_overrideredirect.assert_called_once_with(True)
        mock_toplevel_inst.wm_geometry.assert_called_once_with('+120+227') # x + 20, y + height + 2
        mock_label.assert_called_once()
        mock_label_inst = mock_label.return_value
        mock_label_inst.pack.assert_called_once()

        # 3. Test hiding and unscheduling
        tooltip._hide()
        mock_toplevel_inst.destroy.assert_called_once()
        self.assertIsNone(tooltip._tip_window)
