# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import inspect
import unittest

from azext_oracle_database.aaz.latest.oracle_database.autonomous_database.backup._list import List
from azext_oracle_database.aaz.latest.oracle_database.autonomous_database.backup._show import Show
from azext_oracle_database.aaz.latest.oracle_database.autonomous_database.backup._update import Update


class OracleDatabaseAdbsBackupModelTests(unittest.TestCase):

    def test_update_uses_stable_api_version(self):
        self.assertEqual("2026-06-01", Update._aaz_info["version"])
        self.assertEqual("2026-06-01", Update._aaz_info["resources"][0][-1])

    def test_update_keeps_backup_retention_and_lro_contract(self):
        arguments = Update._build_arguments_schema()
        self.assertTrue(arguments.adbbackupid._required)
        self.assertTrue(arguments.retention_period_in_days._required)
        self.assertEqual(["--retention-days", "--retention-period-in-days"],
                         arguments.retention_period_in_days._options)
        self.assertNotIn("AZ_SUPPORT_GENERIC_UPDATE", inspect.getsource(Update))
        operation = Update.AutonomousDatabaseBackupsUpdate
        self.assertEqual("PATCH", operation.method.fget(None))
        self.assertIn("autonomousDatabaseBackups/{adbbackupid}", inspect.getsource(operation.url.fget))
        self.assertIn('"final-state-via": "location"', inspect.getsource(operation.__call__))
        self.assertNotIn("AutonomousDatabaseBackupsGet", inspect.getsource(Update._execute_operations))
        self.assertNotIn("InstanceUpdateByGeneric", inspect.getsource(Update._execute_operations))
        self.assertFalse(hasattr(Update, "AutonomousDatabaseBackupsGet"))
        self.assertFalse(hasattr(Update, "InstanceUpdateByJson"))
        self.assertFalse(hasattr(Update, "InstanceUpdateByGeneric"))
        self.assertIn("retentionPeriodInDays", inspect.getsource(operation.content.fget))
        self.assertNotIn("new_content_builder", inspect.getsource(operation.content.fget))

    def test_show_uses_paginated_list_and_filters_backup_identifiers(self):
        self.assertIn("AutonomousDatabaseBackupsListByParent", inspect.getsource(Show._output))
        self.assertIn("next_link", inspect.getsource(Show._output))
        self.assertNotIn("AutonomousDatabaseBackupsGet", inspect.getsource(Show._execute_operations))
        self.assertIs(Show.AutonomousDatabaseBackupsListByParent.__bases__[0],
                      List.AutonomousDatabaseBackupsListByParent)
        self.assertFalse(hasattr(Show, "AutonomousDatabaseBackupsGet"))

        backup = {
            "id": "/subscriptions/sub/resourceGroups/rg/providers/Oracle.Database/"
                  "autonomousDatabases/adb/autonomousDatabaseBackups/backup-id",
            "name": "backup-display-name",
            "properties": {"ocid": "ocid1.autonomousdatabasebackup.oc1..example"},
        }
        self.assertEqual(backup, Show._find_backup([backup], "BACKUP-ID"))
        self.assertEqual(backup, Show._find_backup([backup], backup["id"].upper()))
        self.assertEqual(backup, Show._find_backup([backup], backup["name"].upper()))
        self.assertEqual(backup, Show._find_backup([backup], backup["properties"]["ocid"].upper()))
        self.assertIsNone(Show._find_backup([backup], "missing-backup"))
