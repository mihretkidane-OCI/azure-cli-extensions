# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import inspect
import unittest

from azext_oracle_database.aaz.latest.oracle_database.db_system._update import Update


class OracleDatabaseDbSystemModelTests(unittest.TestCase):

    def test_update_uses_stable_api_version(self):
        self.assertEqual("2026-06-01", Update._aaz_info["version"])
        self.assertEqual("2026-06-01", Update._aaz_info["resources"][0][-1])

    def test_update_keeps_name_zones_and_lro_contract(self):
        arguments = Update._build_arguments_schema()
        self.assertTrue(arguments.db_system_name._required)
        self.assertEqual(["-n", "--name", "--db-system-name"], arguments.db_system_name._options)
        self.assertEqual(["--zones"], arguments.zones._options)
        operation = Update.DbSystemsCreateOrUpdate
        self.assertEqual("PUT", operation.method.fget(None))
        self.assertIn("dbSystems/{dbSystemName}", inspect.getsource(operation.url.fget))
        self.assertIn('"final-state-via": "azure-async-operation"', inspect.getsource(operation.__call__))
