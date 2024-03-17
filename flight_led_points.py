import rospy
from clover import srv
from std_srvs.srv import Trigger
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

def navigate_wait(x=0, y=0, z=0, yaw=yaw_dir, speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)


#takeoff on 1 meter
navigate_wait(x = 0, y = 0, z = 1, yaw=0, speed = 0.5, frame_id = 'body', auto_arm = True)
set_effect(effect = 'blink', r = 0, g = 255, b = 0), print('Takeoff')
navigate_wait(x = 0, y = 0, z = 1, speed = 0.5, frame_id = 'aruco_map')
rospy.sleep(3)

#programm
navigate_wait(x = 0, y = 1.2, z = 1, yaw=yaw_dir, speed = 0.5, frame_id = 'aruco_map'), set_effect(effect = 'blink', r = 128, g = 0, b = 128)
#---
telemetry = get_telemetry(frame_id = 'aruco_map')
print(f'coords: x = {round(telemetry.x, 3)}, y = {round(telemetry.y, 3)}, z = {round(telemetry.z, 3)}')
print(f'cellVoltage: {telemetry.cell_voltage}')
print('coordNum: First Angle')
print('')
#---
navigate_wait(x = 1.2, y = 1.2, z = 1, yaw=yaw_dir, speed = 0.5, frame_id = 'aruco_map'), set_effect(effect = 'blink', r = 255, g = 255, b = 0)
#---
telemetry = get_telemetry(frame_id = 'aruco_map')
print(f'coords: x = {round(telemetry.x, 3)}, y = {round(telemetry.y, 3)}, z = {round(telemetry.z, 3)}')
print(f'cellVoltage: {telemetry.cell_voltage}')
print('coordNum: Second Angle')
print('')
#---
navigate_wait(x = 1.2, y = 0, z = 1, yaw=yaw_dir, speed = 0.5, frame_id = 'aruco_map'), set_effect(effect = 'blink', r = 0, g = 255, b = 255)
#---
telemetry = get_telemetry(frame_id = 'aruco_map')
print(f'coords: x = {round(telemetry.x, 3)}, y = {round(telemetry.y, 3)}, z = {round(telemetry.z, 3)}')
print(f'cellVoltage: {telemetry.cell_voltage}')
print('coordNum: Third Angle')
print('')
#---
navigate_wait(x = 0, y = 0, z = 1, speed = 0.5, yaw=yaw_dir, frame_id = 'aruco_map'), set_effect(effect = 'blink', r = 0, g = 0, b = 255)
#---
telemetry = get_telemetry(frame_id = 'aruco_map')
print(f'coords: x = {round(telemetry.x, 3)}, y = {round(telemetry.y, 3)}, z = {round(telemetry.z, 3)}')
print(f'cellVoltage: {telemetry.cell_voltage}')
print('coordNum: Fourth Angle')
print('')
#---
rospy.sleep(3)
#land
print('Landing')
set_effect(effect = 'rainbow')
land()
print('Land is complete')
