#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk

from o3de.ui.export_project import MainWindow


class DummyTkRoot(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._last_child_ids = {}
        self.children = {}
        self._w = '.'
        self.tk = MagicMock()

    def _get_child_mock(self, **kw):
        return MagicMock(**kw)


class TestExportProjectUI(unittest.TestCase):
    def setUp(self):
        self.orig_bases = MainWindow.__bases__
        MainWindow.__bases__ = (DummyTkRoot,)
        self.dummy_root = DummyTkRoot()
        tk._default_root = self.dummy_root

        self.mock_export_config = MagicMock()
        self.mock_export_config.is_global = False
        self.mock_export_config.project_name = "TestProject"

        mock_setting = MagicMock()
        mock_setting.description = "Test Description"
        mock_setting.is_boolean = False
        self.mock_export_config.get_settings_description.return_value = mock_setting

        def mock_get_value(key, default=''):
            if 'config' in key:
                return 'profile'
            if 'format' in key:
                return 'none'
            if 'mode' in key:
                return 'LOOSE'
            return default or ''

        self.mock_export_config.get_value.side_effect = mock_get_value

    def tearDown(self):
        MainWindow.__bases__ = self.orig_bases
        tk._default_root = None

    @patch("tkinter.Button")
    @patch("tkinter.StringVar")
    @patch("tkinter.IntVar")
    def test_window_accessibility_bindings_and_mnemonics(self, mock_intvar, mock_stringvar, mock_button):
        window = MainWindow(export_config=self.mock_export_config, is_sdk=True)

        # Check protocols and key bindings registered during init
        window.protocol.assert_called_with("WM_DELETE_WINDOW", window.on_cancel)

        bound_events = [call[0][0] for call in window.bind.call_args_list]
        self.assertIn("<Escape>", bound_events)
        self.assertIn("<Alt-s>", bound_events)
        self.assertIn("<Alt-S>", bound_events)
        self.assertIn("<Alt-c>", bound_events)
        self.assertIn("<Alt-C>", bound_events)

        # Verify button instantiation arguments for underline mnemonic
        button_calls = mock_button.call_args_list
        button_texts = {call.kwargs.get("text"): call.kwargs.get("underline") for call in button_calls if "text" in call.kwargs}

        self.assertIn("Save", button_texts)
        self.assertEqual(button_texts["Save"], 0)
        self.assertIn("Cancel", button_texts)
        self.assertEqual(button_texts["Cancel"], 0)

    @patch("tkinter.StringVar")
    @patch("tkinter.IntVar")
    def test_on_cancel_destroys_window(self, mock_intvar, mock_stringvar):
        window = MainWindow(export_config=self.mock_export_config, is_sdk=True)
        window.destroy = MagicMock()
        window.on_cancel()
        window.destroy.assert_called_once()


if __name__ == "__main__":
    unittest.main()
