from DroneControl import DroneComm, PID
import sys
import time
import redis
import numpy as np

# Flight stabilization app using the DroneControl Library
# Current roll and pitch values are acquired from the flight controller
# then roll and pitch rates are set to correct the error

roll_pwm_trim = 0
pitch_pwm_trim = 0
yaw_pwm_trim = 0
drone = DroneComm(
    roll_pwm_trim = roll_pwm_trim,
    pitch_pwm_trim = pitch_pwm_trim,
    yaw_pwm_trim = yaw_pwm_trim)

# roll parameters
Kp_roll  = 0.02*0.8
Kd_roll  = 0.0001
Ki_roll  = 0.

out_roll_limit = 1.0

error_roll = 0
d_error_roll = 0


# pitch parameters
Kp_pitch  = 0.02*0.6
Kd_pitch  = 0.0001
Ki_pitch  = 0.

out_pitch_limit = 1.0

error_pitch = 0
d_error_pitch = 0


######### Start program by placing drone on a flat surface to calibrate origin

def center_error(error):
    if error > 180:
        error -= 360
    elif error < -180:
        error += 360
    return error

drone.update_imu()
drone.update_attitude()

# use calibrated roll and pitch
roll0 = 0.0
pitch0 = 0.0

roll_controller = PID(
    kp = Kp_roll, kd = Kd_roll, ki = Ki_roll,
    get_state = drone.get_roll, get_dstate = drone.get_droll,
    get_ref = lambda:roll0,
    center_error = center_error,
    out_limit=out_roll_limit)

pitch_controller = PID(
    kp = Kp_pitch, kd = Kd_pitch, ki = Ki_pitch,
    get_state = drone.get_pitch, get_dstate = drone.get_dpitch,
    get_ref = lambda:pitch0,
    center_error = center_error,
    out_limit=out_pitch_limit)

################ run the control

print(
    '   rr     r    dr     or |' +
    '    rp     p    dp     op')
try:
    while (True):
        # update telemetry data
        drone.update_imu()
        drone.update_attitude()
        #step controllers
        output_roll = roll_controller.step()
        sys.stdout.write(
            "%5.1f %5.1f %5.0f %6.3f | "%
            (roll_controller.ref, roll_controller.state,
             roll_controller.dstate, output_roll))

        output_pitch = pitch_controller.step()
        sys.stdout.write(
            "%5.1f %5.1f %5.0f %6.3f\r"%
            (pitch_controller.ref, pitch_controller.state,
             pitch_controller.dstate, output_pitch))

        sys.stdout.flush()

        # Set corrective rates
        drone.set_roll_rate(output_roll)
        drone.set_pitch_rate(output_pitch)

except (KeyboardInterrupt, SystemExit):
    # Graceful Exit
    drone.exit()
