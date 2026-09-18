# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import inspect
import unittest

from azext_oracle_database.aaz.latest.oracle_database.cloud_vm_cluster._update import Update


class OracleDatabaseCloudVmClusterModelTests(unittest.TestCase):

    def test_update_uses_stable_api_version(self):
        self.assertEqual("2026-06-01", Update._aaz_info["version"])
        self.assertEqual("2026-06-01", Update._aaz_info["resources"][0][-1])

    def test_update_keeps_storage_and_compute_options(self):
        arguments = Update._build_arguments_schema()
        self.assertTrue(arguments.cloudvmclustername._required)
        self.assertEqual(["--cpu-core-count"], arguments.cpu_core_count._options)
        self.assertEqual(["--storage-tbs", "--data-storage-size-in-tbs"],
                         arguments.data_storage_size_in_tbs._options)
        operation = Update.CloudVmClustersCreateOrUpdate
        self.assertEqual("PUT", operation.method.fget(None))
        self.assertIn("cloudVmClusters/{cloudvmclustername}", inspect.getsource(operation.url.fget))
