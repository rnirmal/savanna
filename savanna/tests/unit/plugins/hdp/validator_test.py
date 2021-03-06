# Copyright (c) 2013 Hortonworks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from savanna.plugins.general import exceptions as ex
from savanna.plugins.hdp import validator as v
import unittest2


class ValidatorTest(unittest2.TestCase):

    def test_no_namenode(self):
        cluster = TestCluster()
        cluster.node_groups.append(TestNodeGroup(["GANGLIA_SERVER",
                                                  "AMBARI_SERVER",
                                                  "AMBARI_AGENT"]))
        cluster.node_groups.append(TestNodeGroup(["GANGLIA_MONITOR",
                                                  "AMBARI_AGENT"]))
        validator = v.Validator()
        with self.assertRaises(ex.NotSingleNameNodeException):
            validator.validate(cluster)

    def test_with_namenode(self):
        cluster = TestCluster()
        cluster.node_groups.append(TestNodeGroup(["GANGLIA_SERVER",
                                                  "AMBARI_SERVER",
                                                  "AMBARI_AGENT",
                                                  "NAMENODE"]))
        cluster.node_groups.append(TestNodeGroup(["GANGLIA_MONITOR",
                                                  "AMBARI_AGENT"]))
        validator = v.Validator()
        validator.validate(cluster)

    def test_with_multiple_namenodes(self):
        cluster = TestCluster()
        cluster.node_groups.append(TestNodeGroup(["GANGLIA_SERVER",
                                                  "AMBARI_SERVER",
                                                  "AMBARI_AGENT",
                                                  "NAMENODE"]))
        cluster.node_groups.append(TestNodeGroup(["GANGLIA_MONITOR",
                                                  "AMBARI_AGENT",
                                                  "NAMENODE"]))

        validator = v.Validator()
        with self.assertRaises(ex.NotSingleNameNodeException):
            validator.validate(cluster)

    def test_no_jobtracker(self):
        cluster = TestCluster()
        cluster.node_groups.append(TestNodeGroup(["GANGLIA_SERVER",
                                                  "AMBARI_SERVER",
                                                  "AMBARI_AGENT",
                                                  "NAMENODE"]))
        cluster.node_groups.append(TestNodeGroup(["GANGLIA_MONITOR",
                                                  "AMBARI_AGENT",
                                                  "TASKTRACKER"]))
        validator = v.Validator()
        with self.assertRaises(ex.TaskTrackersWithoutJobTracker):
            validator.validate(cluster)

    def test_with_jobtracker(self):
        cluster = TestCluster()
        cluster.node_groups.append(TestNodeGroup(["GANGLIA_SERVER",
                                                  "AMBARI_SERVER",
                                                  "AMBARI_AGENT",
                                                  "NAMENODE",
                                                  "JOBTRACKER"]))
        cluster.node_groups.append(TestNodeGroup(["GANGLIA_MONITOR",
                                                  "AMBARI_AGENT",
                                                  "TASKTRACKER"]))
        validator = v.Validator()
        validator.validate(cluster)

    def test_no_ambari_server(self):
        cluster = TestCluster()
        cluster.node_groups.append(TestNodeGroup(["GANGLIA_SERVER",
                                                  "NAMENODE",
                                                  "AMBARI_AGENT"]))
        cluster.node_groups.append(TestNodeGroup(["GANGLIA_MONITOR",
                                                  "AMBARI_AGENT"]))
        validator = v.Validator()
        with self.assertRaises(v.NotSingleAmbariServerException):
            validator.validate(cluster)

    def test_missing_ambari_agent(self):
        cluster = TestCluster()
        cluster.node_groups.append(TestNodeGroup(["GANGLIA_SERVER",
                                                  "NAMENODE",
                                                  "AMBARI_SERVER"]))
        cluster.node_groups.append(TestNodeGroup(["GANGLIA_MONITOR",
                                                  "AMBARI_AGENT"]))
        validator = v.Validator()
        with self.assertRaises(v.AmbariAgentNumberException):
            validator.validate(cluster)


class TestCluster(object):

    def __init__(self):
        self.node_groups = []


class TestNodeGroup:

    def __init__(self, processes, count=1):
        self.node_processes = processes
        self.count = count or 1
        self.name = 'TEST'
