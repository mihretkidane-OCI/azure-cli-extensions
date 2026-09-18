# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import inspect
import unittest

from azext_oracle_database.aaz.latest.oracle_database.cloud_exadata_infrastructure._update import Update


class OracleDatabaseCloudExadataInfrastructureModelTests(unittest.TestCase):

    def test_update_uses_stable_api_version(self):
        self.assertEqual("2026-06-01", Update._aaz_info["version"])
        self.assertEqual("2026-06-01", Update._aaz_info["resources"][0][-1])

    def test_update_keeps_infrastructure_options(self):
        arguments = Update._build_arguments_schema()
        self.assertTrue(arguments.cloudexadatainfrastructurename._required)
        self.assertEqual(["--maintenance-window"], arguments.maintenance_window._options)
        self.assertEqual(["--zones"], arguments.zones._options)
        operation = Update.CloudExadataInfrastructuresCreateOrUpdate
        self.assertEqual("PUT", operation.method.fget(None))
        self.assertIn("cloudExadataInfrastructures/{cloudexadatainfrastructurename}",
                      inspect.getsource(operation.url.fget))
