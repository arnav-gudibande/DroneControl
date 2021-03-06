"""Yaw controllers"""
from dronestorm.control.pd import PDController
from dronestorm.control.utils import find_min_angle

class YawPD(object):
    """PID controller for quadcopter Attitude (roll, pitch)

    Parameters
    ----------
    drone_comm: DroneComm instance
        communication object with drone
    yaw_gains: {'kp': kp, 'ki': ki, 'kd': kd}
    """
    def __init__(
            self, drone_comm, yaw_gains, out_yaw_limit=1.0,
            ):
        self.yaw_controller = PID(
            yaw_gains['kp'], yaw_gains['ki'], yaw_gains['kd'],
            lambda:yaw0, drone.get_yaw, drone.get_dyaw,
            _min_angle, out_yaw_limit)

    def step(self):
        output_yaw = self.yaw_controller.step()
        self.drone_comm.set_yaw_rate(output_yaw)
