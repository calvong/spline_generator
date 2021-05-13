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


    def interpolate_traj(self, traj, traj_time):
        """
        :param traj:
        :param traj_time:
        :return:
        """

        joint = 5

        traj_cs = CubicSpline(traj_time, traj[joint, :], bc_type="natural")

        xs = np.arange(0, 1, 0.01)

        abc = traj_cs.c.transpose()

        c = abc[0, :]

        xx = np.arange(0, 0.6, 0.1, dtype=float)
        f = c[0]*np.float_power(xx, 3) + c[1]*np.float_power(xx, 2) + c[2]*xx + c[3]

        c = abc[1, :]

        xx2 = np.arange(0.3, 0.6, 0.1, dtype=float)
        f2 = c[0]*np.float_power(xx2-traj_cs.x[1], 3) + c[1]*np.float_power(xx2-traj_cs.x[1], 2) + c[2]*(xx2-traj_cs.x[1]) + c[3]

        c_reshape = np.reshape(traj_cs.c.transpose(), (traj_cs.c.shape[0]*traj_cs.c.shape[1]))

        traj_cs.d

        # plt.plot(traj_time, traj[1,:])
        #plt.plot(xs, traj_cs(xs), '.')
        plt.plot(traj_time, traj[joint, :], 'o')
        plt.plot(xx, f ,'x')
        plt.plot(xx2, f2, 'x')
        plt.grid()
        plt.show()

def run():
    print "hello world"

    p = PlanReader()

    pos, vel, accel, traj_time = p.read_plan_file("plan_joint6.txt")

    p.interpolate_traj(pos, traj_time)



    # r = R.from_euler('z', 45, degrees=True)
    # r2 = R.from_euler('z', 0, degrees=True)
    #
    # a = r * r2
    #
    # print r.as_quat()
    # print a.as_quat()
    #
    # print r2.as_quat()
    #
    #
    # print a
    # print r.as_dcm()
    # print r.as_rotvec()
    #
    # r2 = R.from_euler('z', 45, degrees=True)
    # r2_vec = [r2.as_rotvec(), r2.as_rotvec()]
    #
    # a = r.apply(r2_vec)




if __name__ == '__main__':
    run()

