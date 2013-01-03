#!/usr/bin/env python

import roslib;roslib.load_manifest('ces')
import rospy

from kobuki_msgs.msg import Led, MotorPower, ButtonEvent
from geometry_msgs.msg import Twist


class ModeSwitcher(object):
    def __init__(self):
        rospy.init_node('ces_mode_switcher')

        self._motor_state = False

        self._but_sub = rospy.Subscriber('/mobile_base/events/button', ButtonEvent, self._but_cb)
        self._mot_pub = rospy.Publisher('/mobile_base/commands/motor_power', MotorPower)
        self._led_pub = rospy.Publisher('mobile_base/commands/led1', Led)

        # Make sure the motors are initially off
        self._mot_pub.publish(self._motor_state)
        # Set the led red
        self._led_pub.publish(3)

        rospy.spin()

    def _but_cb(self, msg):
        # When button 0 is pressed
        if msg.button == 0 and msg.state == 1:
            self.toggle_motor_power()

    def toggle_motor_power(self):
        self._motor_state = not self._motor_state
        print("Setting motor state %s" % self._motor_state)
        self._mot_pub.publish(self._motor_state)

        if self._motor_state == True:
            self._led_pub.publish(1)
        else:
            self._led_pub.publish(3)

if __name__ == "__main__":
    try:
        ms = ModeSwitcher()
    except rospy.ROSInterruptException:
        exit()
