# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import inspect
import unittest

from azext_oracle_database.aaz.latest.oracle_database.resource_anchor._update import Update


class OracleDatabaseResourceAnchorModelTests(unittest.TestCase):

    def test_update_uses_stable_api_version(self):
        self.assertEqual("2026-06-01", Update._aaz_info["version"])
        self.assertEqual("2026-06-01", Update._aaz_info["resources"][0][-1])

    def test_update_keeps_required_name_and_tags(self):
        arguments = Update._build_arguments_schema()
        self.assertTrue(arguments.resource_anchor_name._required)
        self.assertEqual(["-n", "--name", "--resource-anchor-name"], arguments.resource_anchor_name._options)
        self.assertEqual(["--tags"], arguments.tags._options)
        operation = Update.ResourceAnchorsCreateOrUpdate
        self.assertEqual("PUT", operation.method.fget(None))
        self.assertIn("resourceAnchors/{resourceAnchorName}", inspect.getsource(operation.url.fget))
