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

class TestToolTip(unittest.TestCase):
    @patch('tkinter.Toplevel')
    @patch('tkinter.Label')
    def test_tooltip_lifecycle(self, mock_label, mock_toplevel):
        # Setup mock widget
        mock_widget = MagicMock()
        mock_widget.winfo_rootx.return_value = 100
        mock_widget.winfo_rooty.return_value = 150
        mock_widget.winfo_height.return_value = 30
        mock_widget.after.return_value = "after_id_123"

        # Import _ToolTip from main
        from main import _ToolTip

        # 1. Test Initialization and Bindings
        tooltip = _ToolTip(mock_widget, "Helpful Tooltip")

        self.assertEqual(tooltip.widget, mock_widget)
        self.assertEqual(tooltip.text, "Helpful Tooltip")
        self.assertIsNone(tooltip.tip_window)
        self.assertIsNone(tooltip.id)

        # Check bind calls
        bind_args = [call[0][0] for call in mock_widget.bind.call_args_list]
        self.assertIn("<Enter>", bind_args)
        self.assertIn("<Leave>", bind_args)
        self.assertIn("<ButtonPress>", bind_args)

        # 2. Test Enter triggers schedule
        tooltip.enter()
        mock_widget.after.assert_called_once_with(500, tooltip.show_tip)
        self.assertEqual(tooltip.id, "after_id_123")

        # 3. Test show_tip displays window and label
        mock_top_inst = MagicMock()
        mock_toplevel.return_value = mock_top_inst

        mock_label_inst = MagicMock()
        mock_label.return_value = mock_label_inst

        tooltip.show_tip()

        # Check Toplevel was created with widget
        mock_toplevel.assert_called_once_with(mock_widget)
        mock_top_inst.wm_overrideredirect.assert_called_once_with(True)
        # Expected coordinates: x = winfo_rootx() + 20 = 120, y = winfo_rooty() + winfo_height() + 2 = 182
        mock_top_inst.wm_geometry.assert_called_once_with("+120+182")

        # Check Label setup
        mock_label.assert_called_once_with(
            mock_top_inst,
            text="Helpful Tooltip",
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("tahoma", "8", "normal")
        )
        mock_label_inst.pack.assert_called_once_with(ipadx=1)
        self.assertEqual(tooltip.tip_window, mock_top_inst)

        # 4. Test Leave triggers unschedule and hides tooltip
        tooltip.leave()
        mock_widget.after_cancel.assert_called_once_with("after_id_123")
        self.assertIsNone(tooltip.id)
        mock_top_inst.destroy.assert_called_once()
        self.assertIsNone(tooltip.tip_window)
