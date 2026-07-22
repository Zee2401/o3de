#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Ensure directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestWaitDialog(unittest.TestCase):
    def setUp(self):
        # We will mock the entire tkinter library to be safe in headless environments
        self.patcher_tk = patch("wait_dialog.tk")
        self.mock_tk = self.patcher_tk.start()

        # Set up a mock parent
        self.mock_parent = MagicMock()
        self.mock_parent.winfo_x.return_value = 100
        self.mock_parent.winfo_y.return_value = 100
        self.mock_parent.winfo_width.return_value = 800
        self.mock_parent.winfo_height.return_value = 600

        # Mock Toplevel
        self.mock_dialog = MagicMock()
        self.mock_tk.Toplevel.return_value = self.mock_dialog

        # Mock StringVar
        self.mock_string_var = MagicMock()
        self.mock_string_var.get.return_value = ""
        self.mock_tk.StringVar.return_value = self.mock_string_var

        # Cancel callback
        self.cancel_called = False
        def cancel_cb():
            self.cancel_called = True
        self.cancel_cb = cancel_cb

    def tearDown(self):
        self.patcher_tk.stop()

    def test_init_and_bindings(self):
        from wait_dialog import WaitDialog
        wd = WaitDialog(self.mock_parent, "Testing...", self.cancel_cb)

        # Assert correct title, geometry, modality, etc.
        self.mock_tk.Toplevel.assert_called_once_with(self.mock_parent)
        self.mock_dialog.wait_visibility.assert_called_once()
        self.mock_dialog.title.assert_called_with("Operation In Progress...")
        self.mock_dialog.grab_set.assert_called_once()

        # Check button creation
        self.mock_tk.Button.assert_called_once()

        # Verify keyboard and protocol bindings
        bind_calls = {call[0][0]: call[0][1] for call in self.mock_dialog.bind.call_args_list}
        self.assertIn("<Escape>", bind_calls)
        self.assertIn("<Alt-c>", bind_calls)
        self.assertIn("<Alt-C>", bind_calls)

        self.mock_dialog.protocol.assert_called_with("WM_DELETE_WINDOW", wd._on_cancel_button)

    def test_cancellation(self):
        from wait_dialog import WaitDialog
        wd = WaitDialog(self.mock_parent, "Testing...", self.cancel_cb)

        # Trigger cancel button or Escape/Alt-C action
        wd._on_cancel_button()

        # Assert dialog destroy was called
        self.mock_dialog.destroy.assert_called_once()
        self.mock_parent.focus_set.assert_called_once()
        self.assertTrue(self.cancel_called)

    def test_on_tick(self):
        from wait_dialog import WaitDialog
        wd = WaitDialog(self.mock_parent, "Testing...", self.cancel_cb)

        # Test progress string ticking positive then negative
        # 1. First tick (* added)
        self.mock_string_var.get.return_value = ""
        wd.on_tick(1.0)
        self.mock_string_var.set.assert_called_with("*")

        # 2. Second tick
        self.mock_string_var.get.return_value = "*"
        wd.on_tick(1.0)
        self.mock_string_var.set.assert_called_with("**")

        # 3. Third tick
        self.mock_string_var.get.return_value = "**"
        wd.on_tick(1.0)
        self.mock_string_var.set.assert_called_with("***")

        # 4. Limit hit -> reverse direction
        self.mock_string_var.get.return_value = "***"
        wd.on_tick(1.0)
        self.mock_string_var.set.assert_called_with("****")

        self.mock_string_var.get.return_value = "****"
        wd.on_tick(1.0)
        self.mock_string_var.set.assert_called_with("***")
