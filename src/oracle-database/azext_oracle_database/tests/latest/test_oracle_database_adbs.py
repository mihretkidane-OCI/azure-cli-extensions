# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import inspect
import unittest

from azext_oracle_database.aaz.latest.oracle_database.autonomous_database._update import Update


class OracleDatabaseAdbsModelTests(unittest.TestCase):

    def test_update_uses_stable_api_version(self):
        self.assertEqual("2026-06-01", Update._aaz_info["version"])
        self.assertEqual("2026-06-01", Update._aaz_info["resources"][0][-1])

    def test_update_preserves_adbs_update_contract(self):
        arguments = Update._build_arguments_schema()
        self.assertEqual(["--retention-days", "--backup-retention-period-in-days"],
                         arguments.backup_retention_period_in_days._options)
        self.assertEqual(["--zone"], arguments.zone._options)
        operation = Update.AutonomousDatabasesCreateOrUpdate
        self.assertEqual("PUT", operation.method.fget(None))
        self.assertIn("autonomousDatabases/{autonomousdatabasename}", inspect.getsource(operation.url.fget))
        self.assertIn('"final-state-via": "azure-async-operation"', inspect.getsource(operation.__call__))
