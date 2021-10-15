from fig import *
from ratio_sim_low_new import *
from ratio_sim_high_new import *
from device_num_sim_low_new import *
from misc import *
from device_num_sim_high_new import *
from high_low_ratio_sim import *
from same_ips_sim import *
from ratio_sim_low import *
from ratio_sim_high import *
from ratio_sim import *
from device_num_sim_low import *
from device_num_sim_high import *
from device_num_sim import *
import warnings
import datetime
import time
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from asp import ASP
from const import *
from mpo import *
from convex_solver import *


if __name__ == '__main__':
    print("\n")
    warnings.filterwarnings("ignore")
    tic = time.perf_counter()
    # plot_asp_utility()
    # mpo = MPO(DEFAULT_DEVICE_RATIO, DEFAULT_DEVICE_NUM, load_type.RATIO, MPO_NUM_OF_ASP, 1, 0)
    
    # mpo.plot_MPO_utility(1000)
    # for asp in mpo.asp_lst:
    #     print(asp)
    

    # mpo.plot_social_welfare()
    # mpo.plot_asp_utility()
    # asp = ASP(DEFAULT_DEVICE_RATIO, DEFAULT_DEVICE_NUM, load_type.HIGH)
    # X = (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
    # B = ((1-asp.chi)*asp.service_rate*asp.chi*GLOBAL_ETA)
    # C = asp.arrival_rate / B
    # D = (asp.malicious_arrival_rate / (GLOBAL_ETA * asp.chi))
    # asp.mpo_price = asp.total_payment / (X * B * (D-C)**2)
    # print(asp.mpo_price)
    # asp.optimize_zv()
    # print(asp)
    # asp.plot_max_zh()
    # asp.plot_max()
    # plot_utility_device_num_step()
    plot_utility_device_num_high_step()
    plot_utility_device_num_low_step()
    # plot_utility_ratio_step()
    plot_utility_ratio_high_step()
    plot_utility_ratio_low_step()
    # plot_utility_high_low_ratio_step()
    # plot_utility_device_num_high_new_step()
    # plot_utility_device_num_low_new_step()
    # plot_utility_ratio_high_new_step()
    # plot_utility_ratio_low_new_step()
    # plot_ratio_with_same_IPS_ratio_step()
    # plot_flat_price()
    toc = time.perf_counter()
    print(f"\nTotal {str(datetime.timedelta(seconds=int(toc - tic)))} seconds")
