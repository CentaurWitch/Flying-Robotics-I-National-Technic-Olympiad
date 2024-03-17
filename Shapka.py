#code HEAD:------------------------------------------------>
import rospy
import cv2
import numpy as np
from clover import srv
from std_srvs.srv import Trigger
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from clover.srv import SetLEDEffect
import math

rospy.init_node('flight')

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
set_effect = rospy.ServiceProxy('led/set_effect', SetLEDEffect)
yaw_dir = math.radians(90)  #yaw direct
image_pub = rospy.Publisher('~debug', Image, queue_size=1)

@long_callback
def image_callback(data):
    img = bridge.imgmsg_to_cv2(data, 'bgr8')  # OpenCV image
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    red_circle = cv2.inRange(img_hsv, (0, 158, 50), (0, 255, 255))

    image_pub.publish(bridge.cv2_to_imgmsg(red_circle, 'bgr8'))
image_sub = rospy.Subscriber('main_camera/image_raw_throtlled', Image, image_callback)
rospy.spin()

def navigate_wait(x=0, y=0, z=0, yaw=yaw_dir, speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)
