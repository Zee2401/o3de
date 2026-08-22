#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#

import unittest
from unittest.mock import MagicMock, patch

class DummyTkRoot:
    def __init__(self, *args, **kwargs):
        self._last_child_ids = None
        self.children = {}
        self._w = "."
        self.tk = MagicMock()
    def columnconfigure(self, *args, **kwargs):
        pass
    def title(self, *args, **kwargs):
        pass
    def eval(self, *args, **kwargs):
        pass
    def bind(self, *args, **kwargs):
        pass
    def protocol(self, *args, **kwargs):
        pass

class TestExportProjectUI(unittest.TestCase):
    @patch('o3de.ui.export_project.MainWindow.init_source_engine_build_options')
    @patch('o3de.ui.export_project.MainWindow.init_project_build_options')
    @patch('o3de.ui.export_project.MainWindow.init_asset_bundling_options')
    @patch('o3de.ui.export_project.MainWindow.init_platform_tabs')
    @patch('o3de.ui.export_project._ToolTip.bind_widget')
    def test_main_window_okay_cancel_buttons_and_bindings(
        self,
        mock_tooltip_bind,
        mock_platform_tabs,
        mock_asset_bundling,
        mock_project_build,
        mock_source_build
    ):
        mock_config = MagicMock()
        mock_config.is_global = False
        mock_config.project_name = "TestProject"

        from o3de.ui.export_project import MainWindow

        original_bases = MainWindow.__bases__
        MainWindow.__bases__ = (DummyTkRoot,)

        try:
            with patch.object(MainWindow, 'bind') as mock_bind, \
                 patch.object(MainWindow, 'protocol') as mock_protocol:

                window = MainWindow(export_config=mock_config, is_sdk=True)

                # Verify keyboard shortcut bindings
                bound_events = [call[0][0] for call in mock_bind.call_args_list]
                self.assertIn("<Alt-s>", bound_events)
                self.assertIn("<Alt-S>", bound_events)
                self.assertIn("<Alt-c>", bound_events)
                self.assertIn("<Alt-C>", bound_events)
                self.assertIn("<Escape>", bound_events)

                # Verify WM_DELETE_WINDOW protocol registration
                mock_protocol.assert_called_once_with("WM_DELETE_WINDOW", window.on_cancel)

                # Verify tooltip calls for Save and Cancel buttons
                tooltip_messages = [call[1].get('balloonmsg', '') for call in mock_tooltip_bind.call_args_list]
                self.assertTrue(any("Save settings and close" in msg for msg in tooltip_messages))
                self.assertTrue(any("Cancel and close without saving" in msg for msg in tooltip_messages))
        finally:
            MainWindow.__bases__ = original_bases
