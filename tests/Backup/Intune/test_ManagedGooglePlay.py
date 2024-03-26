# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch

from src.IntuneCD.backup.Intune.ManagedGooglePlay import ManagedGooglePlayBackupModule


class TestManagedGooglePlayBackupModule(unittest.TestCase):
    """Tests for the ManagedGooglePlayBackupModule class."""

    def setUp(self):
        self.module = ManagedGooglePlayBackupModule()

    @patch.object(ManagedGooglePlayBackupModule, "make_graph_request")
    @patch.object(ManagedGooglePlayBackupModule, "process_data")
    def test_main(self, mock_process_data, mock_make_graph_request):
        """Test that main calls make_graph_request and process_data."""
        mock_make_graph_request.return_value = {"value": [{"id": "object"}]}

        self.module.main()

        mock_make_graph_request.assert_called_once_with(
            endpoint=self.module.endpoint + self.module.CONFIG_ENDPOINT,
        )
        mock_process_data.assert_called_once_with(
            data=mock_make_graph_request.return_value,
            filetype=None,
            path="None/Managed Google Play/",
            name_key="ownerUserPrincipalName",
            log_message="Backing up Managed Google Play: ",
            audit_compare_info={
                "type": "auditResourceType",
                "value_key": "Microsoft.Management.Services.Api.AndroidManagedStoreAccountEnterpriseSettings",
            },
        )

    @patch.object(ManagedGooglePlayBackupModule, "make_graph_request")
    @patch.object(ManagedGooglePlayBackupModule, "log")
    def test_main_logs_exception_graph_data(self, mock_log, mock_make_graph_request):
        """Test that main logs an exception if make_graph_request raises an exception."""
        mock_make_graph_request.side_effect = Exception("Test exception")

        self.module.main()

        mock_log.assert_called_with(
            tag="error",
            msg=f"Error getting Managed Google Play data from {self.module.endpoint + self.module.CONFIG_ENDPOINT}: Test exception",
        )

    @patch.object(ManagedGooglePlayBackupModule, "process_data")
    @patch.object(ManagedGooglePlayBackupModule, "make_graph_request")
    @patch.object(ManagedGooglePlayBackupModule, "log")
    def test_main_logs_exception_process_data(
        self, mock_log, mock_make_graph_request, mock_process_data
    ):
        """Test that main logs an exception if process_data raises an exception."""
        mock_make_graph_request.return_value = {"value": [{"id": "object"}]}
        mock_process_data.side_effect = Exception("Test exception")

        self.module.main()

        mock_log.assert_called_with(
            tag="error", msg="Error processing Managed Google Play data: Test exception"
        )


if __name__ == "__main__":
    unittest.main()
