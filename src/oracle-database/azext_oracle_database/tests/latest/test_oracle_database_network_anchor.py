# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import inspect
import unittest

from azext_oracle_database.aaz.latest.oracle_database.network_anchor._update import Update


class OracleDatabaseNetworkAnchorModelTests(unittest.TestCase):

    def test_update_uses_stable_api_version(self):
        self.assertEqual("2026-06-01", Update._aaz_info["version"])
        self.assertEqual("2026-06-01", Update._aaz_info["resources"][0][-1])

    def test_update_keeps_dns_and_zone_options(self):
        arguments = Update._build_arguments_schema()
        self.assertTrue(arguments.network_anchor_name._required)
        self.assertEqual(["--is-oracle-to-azure-dns-zone-sync-enabled"],
                         arguments.is_oracle_to_azure_dns_zone_sync_enabled._options)
        self.assertEqual(["--zones"], arguments.zones._options)
        operation = Update.NetworkAnchorsCreateOrUpdate
        self.assertEqual("PUT", operation.method.fget(None))
        self.assertIn("networkAnchors/{networkAnchorName}", inspect.getsource(operation.url.fget))
