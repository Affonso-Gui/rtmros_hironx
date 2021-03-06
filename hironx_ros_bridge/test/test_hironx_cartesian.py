#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Software License Agreement (BSD License)
#
# Copyright (c) 2013, Tokyo Opensource Robotics Kyokai Association
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Tokyo Opensource Robotics Kyokai Association. nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Isaac Isao Saito

# This should come earlier than later import.
# See http://code.google.com/p/rtm-ros-robotics/source/detail?r=6773
import unittest
import numpy

from hironx_ros_bridge import hironx_client as hironx
from hrpsys import rtm

_ARMGROUP_TESTED = 'larm'
_LINK_TESTED = 'LARM_JOINT5'
_GOINITIAL_TIME_MIDSPEED = 3  # second
_NUM_CARTESIAN_ITERATION = 300
_PKG = 'nextage_ros_bridge'


class TestNextageopen(unittest.TestCase):
    '''
    Test NextageClient with rostest.
    '''

    @classmethod
    def setUpClass(self):

        #modelfile = rospy.get_param("hironx/collada_model_filepath")
        #rtm.nshost = 'hiro024'
        #robotname = "RobotHardware0"

        self._robot = hironx.HIRONX()
        #self._robot.init(robotname=robotname, url=modelfile)
        self._robot.init()

        self._robot.goInitial(_GOINITIAL_TIME_MIDSPEED)

#    def test_set_relative_x(self):
    def _set_relative(self, dx=0, dy=0, dz=0):
        #print('Start moving dx={0}, dy={0}, dz={0}'.format(dx, dy, dz))
        self._robot.seq_svc.setMaxIKError(0.00001, 0.01)
        posi_prev = self._robot.getCurrentPosition(_LINK_TESTED)
        for i in range(_NUM_CARTESIAN_ITERATION):
            self._robot.setTargetPoseRelative(_ARMGROUP_TESTED,
                                            _LINK_TESTED, dx, dy, dz, tm=0.15)
            #print('   joint=', nxc.getJointAngles()[3:9])
        posi_post = self._robot.getCurrentPosition(_LINK_TESTED)

        diff_result = posi_prev
        for i in range(len(posi_prev)):
            diff_result[i] = posi_post[i] - posi_prev[i]
        diff_expected = _NUM_CARTESIAN_ITERATION*numpy.array([dx,dy,dz])
        diff_result = numpy.array(diff_result)
        print('Position diff={}, expected={}'.format(diff_result, diff_expected))
        numpy.testing.assert_array_almost_equal(diff_result, diff_expected, decimal=3)
        return True

    def test_set_targetpose_relative_dx(self):
        assert(self._set_relative(dx=0.0001))
        self._robot.goInitial(_GOINITIAL_TIME_MIDSPEED)

    def test_set_targetpose_relative_dy(self):
        assert(self._set_relative(dy=0.0001))
        self._robot.goInitial(_GOINITIAL_TIME_MIDSPEED)

    def test_set_targetpose_relative_dz(self):
        assert(self._set_relative(dz=0.0001))
        self._robot.goInitial(_GOINITIAL_TIME_MIDSPEED)

# unittest.main()
if __name__ == '__main__':
    import rostest
    rostest.rosrun(_PKG, 'test_nxopen', TestNextageopen)
