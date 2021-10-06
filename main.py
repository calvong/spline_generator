from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation as R

class PlanReader():
    def __init__(self):
        1+1

    def read_plan_file(self, filename):
        fd = open(filename, "r")

        #
        n_pt = int(fd.readline())

        # initialise empty arrays
        pos = np.empty((7, n_pt), dtype=float)
        vel = np.empty((7, n_pt), dtype=float)
        accel = np.empty((7, n_pt), dtype=float)
        traj_time = np.empty(n_pt, dtype=float)

        for n in range(n_pt):
            foo = fd.readline()
            for j in range(7):
                pos[j, n] = float(fd.readline())
                vel[j, n] = float(fd.readline())
                accel[j, n] = float(fd.readline())

            traj_time[n] = float(fd.readline())

        fd.close()

        # normalising time
        traj_time = traj_time/max(traj_time)
        return pos, vel, accel, traj_time


    def interpolate_traj(self, traj, vel, traj_time):
        """
        :param traj:
        :param traj_time:
        :return:
        """

        joint = 5
        break_pt = 2

        pos_cs = CubicSpline(traj_time, traj[joint, :], bc_type="natural")
        vel_cs = pos_cs.derivative()
    
        print "pos coeff:"
        print pos_cs.c
        
        print "vel coeff:"
        print vel_cs.c

        print "break"
        print vel_cs.x

        xs = np.arange(0, 1, 0.01)

        pos_c = pos_cs.c.transpose()
        c = pos_c[break_pt, :]

        xp = np.arange(pos_cs.x[break_pt], pos_cs.x[break_pt+1], 0.02, dtype=float)
        fp = c[0]*np.float_power(xp-vel_cs.x[break_pt], 3) + c[1]*np.float_power(xp-vel_cs.x[break_pt], 2) \
            + c[2]*(xp-vel_cs.x[break_pt]) + c[3]

        vel_c = vel_cs.c.transpose()
        cv = vel_c[break_pt, :]

        xv = np.arange(vel_cs.x[break_pt], vel_cs.x[break_pt+1], 0.02, dtype=float)
        fv = cv[0]*np.float_power(xv-vel_cs.x[break_pt], 2) + cv[1]*np.float_power(xv-vel_cs.x[break_pt], 1) + cv[2] - vel_c[0, 2]

        # c_reshape = np.reshape(pos_cs.c.transpose(), (pos_cs.c.shape[0]*pos_cs.c.shape[1]))

        plt.figure(1)
        plt.plot(xs, pos_cs(xs), '.r')
        plt.plot(traj_time, traj[joint, :], '*k')
        plt.plot(xp, fp, 'og')
        plt.grid()
        plt.title("position")

        plt.figure(2)
        plt.plot(xs, vel_cs(xs), '.r')
        plt.plot(traj_time, vel[joint, :], '*k')
        plt.plot(xv, fv, 'og')
        plt.grid()
        plt.title("velocity")

        plt.show()


def run():
    print "hello world"

    p = PlanReader()

    pos, vel, accel, traj_time = p.read_plan_file("plan_joint6.txt")

    p.interpolate_traj(pos, vel, traj_time)

    # r = R.from_quat([0, 0, 0, 1])
    # rxyz = R.from_euler('xyz', [0, 270, 0], degrees=True)
    # rx = R.from_euler('xyz', [0, 0, 45], degrees=True)
    # new_r = R.from_dcm(np.matmul(rxyz.as_dcm(), rx.as_dcm()))

    # print rxyz.as_quat()

    # print new_r.as_quat()

    # print new_r.as_dcm()

if __name__ == '__main__':
    run()


