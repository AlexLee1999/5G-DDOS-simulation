from asp import ASP
from const import *
from mpo import *
from convex_solver import *
import matplotlib
matplotlib.use('agg') 
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import time
import datetime
import warnings
from device_num_sim import *
from device_num_sim_high import *
from device_num_sim_low import *
from ratio_sim import *
from ratio_sim_high import *
from ratio_sim_low import *
from same_ips_sim import *
from high_low_ratio_sim import *
from device_num_sim_high_new import *
from misc import *
from device_num_sim_low_new import *
from ratio_sim_high_new import *
from ratio_sim_low_new import *
from fig import *

if __name__ == '__main__':
    print("\n")
    warnings.filterwarnings("ignore")
    tic = time.perf_counter()
    # plot_asp_utility()
    # mpo = MPO(DEFAULT_DEVICE_RATIO, DEFAULT_DEVICE_NUM, load_type.RATIO, MPO_NUM_OF_ASP, 3, 2)
    # mpo.plot_MPO_utility(3000)
    
    # mpo.plot_social_welfare()
    # mpo.plot_asp_utility()
    # asp = ASP(DEFAULT_DEVICE_RATIO, DEFAULT_DEVICE_NUM, load_type.LOW)
    # asp.plot_max_zh()
    # asp.plot_max()
    # plot_utility_device_num_step()
    # plot_utility_device_num_high_step()
    # plot_utility_device_num_low_step()
    # plot_utility_ratio_step()
    # plot_utility_ratio_high_step()
    # plot_utility_ratio_low_step()
    # plot_utility_high_low_ratio_step()
    # plot_utility_device_num_high_new_step()
    # plot_utility_device_num_low_new_step()
    # plot_utility_ratio_high_new_step()
    # plot_utility_ratio_low_new_step()
    # plot_ratio_with_same_IPS_ratio_step()
    # plot_flat_price()
    toc = time.perf_counter()
    print(f"\nTotal {str(datetime.timedelta(seconds=int(toc - tic)))} seconds")




