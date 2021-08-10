from asp import ASP
from const import *
from device import Device
from mpo import *
from convex_solver import *
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import time
from device_num_sim import *
from device_num_sim_high import *
from device_num_sim_low import *
from ratio_sim import *
from same_ips_sim import *

def plot_different_step():
    print("step")
    num = [600, 800, 1000, 1200, 1400]
    phi_step_1_lst = []
    social_step_1_lst = []
    phi_step_5_lst = []
    social_step_5_lst = []
    phi_step_10_lst = []
    social_step_10_lst = []
    for n in num:
        phi_step_1 = 0
        soc_step_1 = 0
        phi_step_5 = 0
        soc_step_5 = 0
        phi_step_10 = 0
        soc_step_10 = 0
        for _ in tqdm(range(ITER)):
            mpo = MPO(0.1, n)
            _, max_phi, social, _, _ = mpo.optimize_phi_with_step(1)
            phi_step_1 += max_phi
            soc_step_1 += social
            _, max_phi, social, _, _= mpo.optimize_phi_with_step(2)
            phi_step_5 += max_phi
            soc_step_5 += social
            _, max_phi, social, _, _ = mpo.optimize_phi_with_step(0.5)
            phi_step_10 += max_phi
            soc_step_10 += social
        phi_step_1_lst.append(phi_step_1 / ITER)
        social_step_1_lst.append(soc_step_1 / ITER)
        phi_step_5_lst.append(phi_step_5 / ITER)
        social_step_5_lst.append(soc_step_5 / ITER)
        phi_step_10_lst.append(phi_step_10 / ITER)
        social_step_10_lst.append(soc_step_10 / ITER)
    X = np.arange(5)
    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, phi_step_10_lst, marker='s', linestyle='-.', label='Step = 0.5', linewidth=7, markersize=30)
    plt.plot(num, phi_step_1_lst, marker='o', linestyle='-.', label='Step = 1', linewidth=7, markersize=30)
    plt.plot(num, phi_step_5_lst, marker='^', linestyle='-.', label='Step = 2', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Optimal\ MPO\ Price}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/step_compare/5GDDoS_Game_price_device_with_step.jpg')
    plt.savefig('./image/step_compare/5GDDoS_Game_price_device_with_step.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.bar(X + 0.00, social_step_10_lst, label='Step = 0.5', width=0.25)
    plt.bar(X + 0.25, social_step_1_lst, label='Step = 1', width=0.25)
    plt.bar(X + 0.50, social_step_5_lst, label='Step = 2', width=0.25)
    plt.legend(loc="best", fontsize=100)
    plt.xticks(X + (0.375 / 2), (600, 800, 1000, 1200, 1400))
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Social\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/step_compare/5GDDoS_Game_social_device_with_step.jpg')
    plt.savefig('./image/step_compare/5GDDoS_Game_social_device_with_step.pdf')
    plt.close()

# def plot_max_vm():
#     print("max vm")
#     num = [500, 750, 1000, 1250]
#     utility_proposed_lst = []
#     social_proposed_lst = []
#     asp_utility_proposed_lst = []
#     util_max_num = []
#     social_max_num = []
#     asp_util_max_num = []
#     for n in num:
#         u_max_num = 0
#         soc_max_num = 0
#         asp_u_max_num = 0
#         utility_proposed = 0
#         social_proposed = 0
#         asp_utility_proposed = 0
#         for _ in tqdm(range(ITER)):
#             mpo = MPO(0.1, n)
#             util, _, social, asp_u = mpo.optimize_phi_with_step(0.5)
#             utility_proposed += util
#             social_proposed += social
#             asp_utility_proposed += asp_u
#             mpo.find_constraint_phi()
#             phi = mpo.constraint_phi
#             util, social, asp_u = mpo.optimize_phi_with_price(phi)
#             u_max_num += util
#             soc_max_num += social
#             asp_u_max_num += asp_u
#         utility_proposed_lst.append(utility_proposed / ITER)
#         social_proposed_lst.append(social_proposed / ITER)
#         asp_utility_proposed_lst.append(asp_utility_proposed / ITER)
#         util_max_num.append(u_max_num / ITER)
#         social_max_num.append(soc_max_num / ITER)
#         asp_util_max_num.append(asp_u_max_num / ITER)
#     plt.figure(figsize=(45, 25), dpi=400)
#     plt.plot(num, utility_proposed_lst, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
#     plt.plot(num, util_max_num, marker='^', linestyle='-.', label='Max VM', linewidth=7, markersize=30)
#     plt.legend(loc="best", fontsize=100)
#     plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
#     plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=100)
#     plt.xticks(fontsize=80)
#     plt.yticks(fontsize=80)
#     plt.savefig('./5GDDoS_Game_MPO_device_max_num.jpg')
#     plt.savefig('./5GDDoS_Game_MPO_device_max_num.pdf')
#     plt.close()

#     plt.figure(figsize=(45, 25), dpi=400)
#     plt.plot(num, social_proposed_lst, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
#     plt.plot(num, social_max_num, marker='^', linestyle='-.', label='Max VM', linewidth=7, markersize=30)
#     plt.legend(loc="best", fontsize=100)
#     plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
#     plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=100)
#     plt.xticks(fontsize=80)
#     plt.yticks(fontsize=80)
#     plt.savefig('./5GDDoS_Game_social_device_max_num.jpg')
#     plt.savefig('./5GDDoS_Game_social_device_max_num.pdf')
#     plt.close()

#     plt.figure(figsize=(45, 25), dpi=400)
#     plt.plot(num, asp_utility_proposed_lst, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
#     plt.plot(num, asp_util_max_num, marker='^', linestyle='-.', label='Max VM', linewidth=7, markersize=30)
#     plt.legend(loc="best", fontsize=100)
#     plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
#     plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
#     plt.xticks(fontsize=80)
#     plt.yticks(fontsize=80)
#     plt.savefig('./5GDDoS_Game_asp_device_max_num.jpg')
#     plt.savefig('./5GDDoS_Game_asp_device_max_num.pdf')
#     plt.close()

def plot_different_ratio():
    ratio = [0.1, 0.3, 0.5, 0.7, 0.9]
    plt.figure(figsize=(45, 25), dpi=400)
    step = 1
    for ra in ratio:
        ut = []
        pr = []
        phi = 30
        mpo = MPO(ra, 1000)
        vm_prior = float('inf')
        for _ in range(3000):
            mpo.set_and_check_required_vm(phi)
            vm_after = mpo.total_vm()
            welfare = 0
            for asp in mpo.asp_lst:
                welfare += asp.utility
            pr.append(phi)
            ut.append(phi * vm_after - MPO_cost(vm_after) + welfare)
            phi += step
            if vm_prior < vm_after:
                print('Total VM is not non-increasing')
            vm_prior = vm_after
        plt.plot(pr, ut, marker='.', linestyle='-.', label=f'ratio : {ra}', linewidth=7, markersize=30)
    plt.xlabel(r'$\bf{MPO\ Price}$', fontsize=100)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.legend(loc="best", fontsize=100)
    plt.savefig('./5GDDoS_Game_utility_ratio.pdf')
    plt.savefig('./5GDDoS_Game_utility_ratio.jpg')
    plt.close()

def plot_flat_price():
    price = [i for i in range(50, 2000, 50)]
    mpo = MPO(0.1, 1000)
    utility_proposed_lst, max_phi, _, _, _ = mpo.optimize_phi()
    ut_lst_proposed = []
    ut_lst_flat = []
    for p in price:
        mpo.set_and_check_required_vm(p)
        vm_num = mpo.total_vm()
        uti = p * vm_num - MPO_cost(vm_num)
        ut_lst_flat.append(uti)
        ut_lst_proposed.append(utility_proposed_lst)
    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(price, ut_lst_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(price, ut_lst_flat, marker='^', linestyle='-.', label='Flat Price', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Flat\ Price}$', fontsize=100)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_utility_flat.jpg')
    plt.savefig('./5GDDoS_Game_utility_flat.pdf')
    plt.close()

def plot_asp_utility():
    asp = ASP(0.1, 1000, load_type.AVERAGE)
    utility_lst = []
    purchased_vm_lst = []
    utility_lst_without_constraint = []
    purchased_vm_lst_without_constraint = []
    price = [i for i in range(20, 5000, 10)]
    print(asp.malicious_arrival_rate/(asp.chi * GLOBAL_ETA))
    for i in range(20, 5000, 10):
        asp.mpo_price = i
        asp.optimize_zv()
        utility_lst.append(asp.utility)
        purchased_vm_lst.append(asp.z_v)
        # print(asp.z_h, asp.z_v)
        asp.optimize_zv_without_constraint()
        utility_lst_without_constraint.append(asp.utility)
        purchased_vm_lst_without_constraint.append(asp.z_v)
        
    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(price, utility_lst, marker='.', linestyle='-.', label='With Constraint', linewidth=7, markersize=30)
    plt.plot(price, utility_lst_without_constraint, marker='.', linestyle='-.', label='Without Constraint', linewidth=7, markersize=30)
    plt.vlines(asp.bound, ymin=min(utility_lst_without_constraint + utility_lst), ymax=max(utility_lst_without_constraint + utility_lst), linewidth=7)
    plt.vlines(asp.qbound, ymin=min(utility_lst_without_constraint + utility_lst), ymax=max(utility_lst_without_constraint + utility_lst), linewidth=7)
    

    plt.xlabel(r'$\bf{MPO\ Price}$', fontsize=100)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
    plt.legend(loc="best", fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/asp/5GDDoS_Game_ASP_price.jpg')
    plt.savefig('./image/asp/5GDDoS_Game_ASP_price.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(price, purchased_vm_lst, marker='.', linestyle='-.', label='With Constraint', linewidth=7, markersize=30)
    plt.plot(price, purchased_vm_lst_without_constraint, marker='.', linestyle='-.', label='Without Constraint', linewidth=7, markersize=30)
    plt.vlines(asp.bound, ymin=min(purchased_vm_lst_without_constraint + purchased_vm_lst), ymax=max(purchased_vm_lst_without_constraint + purchased_vm_lst), linewidth=7)
    plt.vlines(asp.qbound, ymin=min(purchased_vm_lst_without_constraint + purchased_vm_lst), ymax=max(purchased_vm_lst_without_constraint + purchased_vm_lst), linewidth=7)
    plt.xlabel(r'$\bf{MPO\ Price}$', fontsize=100)
    plt.ylabel(r'$\bf{Purchased\ VM}$', fontsize=100)
    plt.legend(loc="best", fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/asp/5GDDoS_Game_ASP_vm.jpg')
    plt.savefig('./image/asp/5GDDoS_Game_ASP_vm.pdf')
    plt.close()



if __name__ == '__main__':
    print("\n")
    tic = time.perf_counter()
    # plot_asp_utility()
    # mpo = MPO(0.1, 1000, load_type.AVERAGE)
    # mpo.plot_MPO_utility()
    # mpo.plot_social_welfare()
    # mpo.plot_asp_utility()
    # asp = ASP(0.1, 1000, load_type.AVERAGE)
    # asp.plot_max()
    # asp.plot_max_zh()
    # plot_different_ratio()
    # plot_utility_device_num()
    plot_utility_device_num_step()
    # plot_utility_device_num_high()
    # plot_utility_device_num_step_high()
    # plot_utility_device_num_low()
    # plot_utility_device_num_step_low()
    # plot_utility_ratio()
    # plot_utility_ratio_step()
    # plot_different_step()
    # plot_ratio_with_same_IPS_ratio()
    # plot_ratio_with_same_IPS_ratio_step()
    # plot_flat_price()
    toc = time.perf_counter()
    print(f"\nTotal {toc - tic} seconds")




