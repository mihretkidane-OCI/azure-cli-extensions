# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import inspect
import unittest

from azext_oracle_database.aaz.latest.oracle_database.database_system_shape._list import List
from azext_oracle_database.aaz.latest.oracle_database.database_system_shape._show import Show


class OracleDatabaseSystemShapeModelTests(unittest.TestCase):

    def test_list_and_show_use_stable_api_version(self):
        for command in (List, Show):
            with self.subTest(command=command.__module__):
                self.assertEqual("2026-06-01", command._aaz_info["version"])
                self.assertEqual("2026-06-01", command._aaz_info["resources"][0][-1])

    def test_list_keeps_filter_arguments(self):
        arguments = List._build_arguments_schema()
        self.assertEqual(["--shape-attribute"], arguments.shape_attribute._options)
        self.assertEqual(["--zone"], arguments.zone._options)

    def test_list_and_show_keep_location_scoped_get_contracts(self):
        self.assertTrue(List._build_arguments_schema().location._required)
        self.assertTrue(Show._build_arguments_schema().dbsystemshapename._required)
        self.assertEqual("GET", List.DbSystemShapesListByLocation.method.fget(None))
        self.assertEqual("GET", Show.DbSystemShapesGet.method.fget(None))
        self.assertIn("locations/{location}/dbSystemShapes", inspect.getsource(List.DbSystemShapesListByLocation.url.fget))
        self.assertIn("dbSystemShapes/{dbsystemshapename}", inspect.getsource(Show.DbSystemShapesGet.url.fget))
