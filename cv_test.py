import rospy
import cv2
import numpy as np
from clover import srv
from std_srvs.srv import Trigger
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
#from clover import long_callback

rospy.init_node('cv')
bridge = CvBridge()

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_altitude = rospy.ServiceProxy('set_altitude', srv.SetAltitude)
set_yaw = rospy.ServiceProxy('set_yaw', srv.SetYaw)
set_yaw_rate = rospy.ServiceProxy('set_yaw_rate', srv.SetYawRate)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
image_pub = rospy.Publisher('~debug', Image, queue_size=1)

#@long_callback
def image_callback(data):
    img = bridge.imgmsg_to_cv2(data, 'bgr8')  # OpenCV image
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    red_circle = cv2.inRange(img_hsv, (0, 158, 50), (0, 255, 255))

    image_pub.publish(bridge.cv2_to_imgmsg(red_circle, 'bgr8'))
image_sub = rospy.Subscriber('main_camera/image_raw_throtlled', Image, image_callback)
rospy.spin()