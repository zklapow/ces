#!/usr/bin/env python

import roslib;roslib.load_manifest('ces')
import rospy

from kobuki_msgs.msg import Led, MotorPower, ButtonEvent
from geometry_msgs.msg import Twist


class ModeSwitcher(object):
    def __init__(self):
        rospy.init_node('ces_mode_switcher')

        self._motor_state = 1

        self._but_sub = rospy.Subscriber('/mobile_base/events/button', ButtonEvent, self._but_cb)
        self._mot_pub = rospy.Publisher('/mobile_base/commands/motor_power', MotorPower)

    def _but_cb(self, msg):
        # When button 0 is pressed
        if msg.button == 0 and msg.state == 1:
            self.toggle_motor_power()

    def toggle_motor_power(self):
        self._motor_state = not self._motor_state
        self._mot_pub.publish(self._motor_state)

if __name__ == "__main__":
    try:
        ms = ModeSwitcher()
    except rospy.ROSInterruptException:
        exit()
