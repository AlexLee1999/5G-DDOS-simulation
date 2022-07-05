from fig import *
from ratio_sim_low import *
from ratio_sim_high import *
from ratio_sim import *
from device_num_sim_low import *
from device_num_sim_high import *
from device_num_sim import *
import warnings
import datetime
import time
from asp import *
from const import *
from mpo import *
from convex_solver import *
from efficiency_sim_high import *
from efficiency_sim_low import *
from efficiency_sim import *


if __name__ == '__main__':
    print("\n")
    warnings.filterwarnings("ignore")
    tic = time.perf_counter()
    #######################################################################
    # Convex Optimizations
    #######################################################################
    # plot_utility_device_num_cvx()
    # plot_utility_device_num_high_cvx()
    # plot_utility_device_num_low_cvx()
    # plot_utility_ratio_cvx()
    plot_utility_ratio_high_cvx()
    # plot_utility_ratio_low_cvx()
    # plot_utility_efficiency_cvx()
    plot_utility_efficiency_high_cvx()
    plot_utility_efficiency_low_cvx()

    #######################################################################
    # Plot MPO Curves
    #######################################################################
    # mpo = MPO(DEFAULT_DEVICE_RATIO, DEFAULT_DEVICE_NUM, load_type.AVERAGE, MPO_NUM_OF_ASP, DEFAULT_ETA, 2, 3)
    # for asp in mpo.asp_lst:
    #     print(asp)
    # mpo.plot_MPO_utility(350)

    toc = time.perf_counter()
    print(f"\nTotal {str(datetime.timedelta(seconds=int(toc - tic)))} seconds")
