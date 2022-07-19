#!/usr/bin/env python3

"""This module tests backing up management partner."""

import json
import yaml
import unittest

from pathlib import Path
from unittest.mock import patch
from src.IntuneCD.backup_managementPartner import savebackup
from testfixtures import TempDirectory

MANAGEMENT_PARTNER = {
    "value": [{
        "@odata.type": "#microsoft.graph.managementPartner",
        "id": "0",
        "isConfigured": True,
        "displayName": "test",
    }]}


@patch("src.IntuneCD.backup_managementPartner.savebackup")
@patch("src.IntuneCD.backup_managementPartner.makeapirequest",
       return_value=MANAGEMENT_PARTNER)
class TestBackupManagementPartner(unittest.TestCase):
    """Test class for backup_managementPartner."""

    def setUp(self):
        self.directory = TempDirectory()
        self.directory.create()
        self.token = 'token'
        self.saved_path = f"{self.directory.path}/Partner Connections/Management/test."
        self.expected_data = {
            "@odata.type": "#microsoft.graph.managementPartner",
            "isConfigured": True,
            "displayName": "test",}

    def tearDown(self):
        self.directory.cleanup()

    def test_backup_yml(self, mock_data, mock_makeapirequest):
        self.count = savebackup(self.directory.path, 'yaml', self.token)

        with open(self.saved_path + 'yaml', 'r') as f:
            data = json.dumps(yaml.safe_load(f))
            self.saved_data = json.loads(data)

        self.assertTrue(
            Path(f'{self.directory.path}/Partner Connections/Management').exists())
        self.assertEqual(self.expected_data, self.saved_data)
        self.assertEqual(1, self.count)

    def test_backup_json(self, mock_data, mock_makeapirequest):
        self.count = savebackup(self.directory.path, 'json', self.token)

        with open(self.saved_path + 'json', 'r') as f:
            self.saved_data = json.load(f)

        self.assertTrue(
            Path(f'{self.directory.path}/Partner Connections/Management').exists())
        self.assertEqual(self.expected_data, self.saved_data)
        self.assertEqual(1, self.count)

    def test_backup_with_no_return_data(self, mock_data, mock_makeapirequest):
        mock_data.return_value = {"value":[{"isConfigured": False}]}
        self.count = savebackup(self.directory.path, 'json', self.token)
        self.assertEqual(0, self.count)
