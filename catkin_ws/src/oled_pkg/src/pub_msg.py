#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32

def publish_once():
    rospy.init_node('expression_publisher', anonymous=True)
    pub = rospy.Publisher('expression_choice', Int32, queue_size=1)
    rospy.sleep(1)

    expression_value = 2
    pub.publish(expression_value)
    
    rospy.signal_shutdown("Message published") 

if __name__ == '__main__':
    try:
        publish_once()
    except rospy.ROSInterruptException:
        pass
