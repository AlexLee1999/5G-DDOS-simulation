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
from asp import *
from const import *
from mpo import *
from convex_solver import *


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
    plot_utility_ratio_cvx()
    plot_utility_ratio_high_cvx()
    plot_utility_ratio_low_cvx()
    #######################################################################
    # Step Optimizations
    #######################################################################
    # plot_utility_device_num_step()
    # plot_utility_device_num_high_step()
    # plot_utility_device_num_low_step()
    # plot_utility_ratio_step()
    # plot_utility_ratio_high_step()
    # plot_utility_ratio_low_step()

    #######################################################################
    # Plot MPO Curves
    #######################################################################
    # mpo = MPO(0.9, 1000, load_type.RATIO, MPO_NUM_OF_ASP, 5, 0)
    # for asp in mpo.asp_lst:
    #     print(asp.case)
    # print(mpo.bd)
    # print(mpo.qbd)
    # print(mpo.cp)
    # mpo_utility, max_phi, social_welfare, asp_utility, vm_number = mpo.optimize_phi()
    # print(mpo_utility, max_phi, social_welfare, asp_utility, vm_number)
    # print(mpo.optimize_phi_with_chi(0, max_phi))
    # print(mpo.optimize_phi_with_price(max_phi))
    # mpo_utility, max_phi, social_welfare, asp_utility, vm_number = mpo.optimize_phi_with_step(STEP)
    # print(mpo_utility, max_phi, social_welfare, asp_utility, vm_number)
    # print(mpo.optimize_phi_with_chi(0, max_phi))
    # print(mpo.optimize_phi_with_price(max_phi))
    # mpo.plot_MPO_utility(1000)
    # mpo.plot_social_welfare()
    # mpo.plot_asp_utility()

    #######################################################################
    # Plot ASP Curves
    #######################################################################
    # asp = ASP(DEFAULT_DEVICE_RATIO, DEFAULT_DEVICE_NUM, load_type.HIGH)
    # asp.plot_max_zh()
    # asp.plot_max()
    # plot_asp_utility()

    #######################################################################
    # Misc.
    #######################################################################    
    # plot_utility_device_num_high_new_step()
    # plot_utility_device_num_low_new_step()
    # plot_utility_ratio_high_new_step()
    # plot_utility_ratio_low_new_step()
    # plot_utility_high_low_ratio_step()
    # plot_ratio_with_same_IPS_ratio_step()
    # plot_flat_price()

    toc = time.perf_counter()
    print(f"\nTotal {str(datetime.timedelta(seconds=int(toc - tic)))} seconds")
