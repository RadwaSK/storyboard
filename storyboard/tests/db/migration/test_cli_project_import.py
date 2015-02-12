# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import storyboard.db.api.base as api_base
from storyboard.db.models import ProjectGroup
from storyboard.db import projects_loader
from storyboard.tests.db import base


class TestProjectGroupMigration(base.BaseDbTestCase):
    """Unit tests for the load_projects commandline option, focused on
    groups only.
    """

    def setUp(self):
        super(TestProjectGroupMigration, self).setUp()

    def testSimpleGroupMigration(self):
        projects_loader.do_load_models('./etc/projects.yaml.sample')

        all_groups = api_base.entity_get_all(ProjectGroup)

        self.assertEqual(3, len(all_groups))
