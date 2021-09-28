#!/usr/bin/env python
 
import sys
import rospy
from turtlesim.srv import *
import numpy as np # For random numbers
from std_msgs.msg import String
from geometry_msgs.msg import Twist 
from turtlesim import msg
import time

def check_walls(msg):
    if(msg.x <= 0 or msg.x >=11 or msg.y <= 0 or msg.y >= 11):
        call_teleport_service()
        call_tray_service(np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))

#Initialize publisher
p = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=1000)

# Initialize node
rospy.init_node('idk_what_this_is')
r = rospy.Rate(2) # Set Frequency
rospy.Subscriber('turtle1/pose', msg.Pose, check_walls, queue_size=1000)

def call_tray_service(r,g,b):
    random_number = np.random.randint(1,5)
    rospy.wait_for_service('turtle1/set_pen')
    try:
        turtle1_set_pen = rospy.ServiceProxy('turtle1/set_pen',SetPen)
        turtle1_set_pen(r,g,b,random_number,False)
        return True;
    except rospy.ServiceException, e:
        print "Service tray failed: %s"%e
        return False

def call_teleport_service():
    rospy.wait_for_service('turtle1/teleport_absolute')
    try:
        turtle1_teleport_absolute = rospy.ServiceProxy('turtle1/teleport_absolute',TeleportAbsolute)
        turtle1_teleport_absolute(5.5,5.5,0)
        return True;
    except rospy.ServiceException, e:
        print "Service tp failed: %s"%e
        return False



def call_service(x, theta):
    rospy.wait_for_service('/turtle1/teleport_relative')
    try:
        teleport_relative = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
        resp1 = teleport_relative(x, theta)
        return True
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
        return False
 
 
if __name__ == "__main__":
    r = int(sys.argv[1])
    g = int(sys.argv[2])
    b = int(sys.argv[3])
    call_tray_service(r,g,b)
    i = 0
    while not rospy.is_shutdown():
        #Initiate Message with zero values
        t=Twist()

        t.angular.z = 5
        t.linear.x = 3

        
     
        #publish the message
        
        i+=1
        if(i == 5):
            t.linear.x = 40
            i = 0
        p.publish(t)
        #r.sleep()
    