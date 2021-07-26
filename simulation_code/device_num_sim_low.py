from asp import ASP
from const import *
from device import Device
from mpo import *
from convex_solver import *
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

def plot_utility_device_num_low():
    print("device")
    num = [600, 800, 1000, 1200, 1400]
    util_proposed = []
    social_proposed = []
    asp_util_proposed = []
    vm_lst_proposed = []
    util_fix_zero = []
    social_fix_zero = []
    asp_util_fix_zero = []
    vm_lst_fix_zero = []
    util_fix_five = []
    social_fix_five = []
    asp_util_fix_five = []
    vm_lst_fix_five = []
    util_fix_nine = []
    social_fix_nine = []
    asp_util_fix_nine = []
    vm_lst_fix_nine = []
    for n in num:
        u_zero = 0
        soc_zero = 0
        asp_u_zero = 0
        vm_zero = 0
        u_proposed = 0
        soc_proposed = 0
        asp_u_proposed = 0
        vm_proposed = 0
        u_five = 0
        soc_five = 0
        asp_u_five = 0
        vm_five = 0
        u_nine = 0
        soc_nine = 0
        asp_u_nine = 0
        vm_nine = 0
        i = 0
        pbar = tqdm(total=ITER)
        while i < ITER:
            try:
                mpo = MPO_low_load(0.1, n)
                util, max_phi, social, asp_u, vm_num = mpo.optimize_phi()
                u_proposed += util
                soc_proposed += social
                asp_u_proposed += asp_u
                vm_proposed += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0, max_phi)
                u_zero += util
                soc_zero += social
                asp_u_zero += asp_u
                vm_zero += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0.5, max_phi)
                u_five += util
                soc_five += social
                asp_u_five += asp_u
                vm_five += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0.9, max_phi)
                u_nine += util
                soc_nine += social
                asp_u_nine += asp_u
                vm_nine += vm_num
                i += 1
                pbar.update(1)
            except ArithmeticError as e:
                print(e)
        pbar.close()
        util_proposed.append(u_proposed / ITER)
        social_proposed.append(soc_proposed / ITER)
        asp_util_proposed.append(asp_u_proposed / ITER)
        vm_lst_proposed.append(vm_proposed / ITER)
        util_fix_zero.append(u_zero / ITER)
        social_fix_zero.append(soc_zero / ITER)
        asp_util_fix_zero.append(asp_u_zero / ITER)
        vm_lst_fix_zero.append(vm_zero / ITER)
        util_fix_five.append(u_five / ITER)
        social_fix_five.append(soc_five / ITER)
        asp_util_fix_five.append(asp_u_five / ITER)
        vm_lst_fix_five.append(vm_five / ITER)
        util_fix_nine.append(u_nine / ITER)
        social_fix_nine.append(soc_nine / ITER)
        asp_util_fix_nine.append(asp_u_nine / ITER)
        vm_lst_fix_nine.append(vm_nine / ITER)
    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, util_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, util_fix_zero, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, util_fix_five, marker='s', linestyle='-.', label='50% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, util_fix_nine, marker='8', linestyle='-.', label='90% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_MPO_device_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_MPO_device_low.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, social_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, social_fix_zero, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, social_fix_five, marker='s', linestyle='-.', label='50% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, social_fix_nine, marker='8', linestyle='-.', label='90% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_social_device_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_social_device_low.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, asp_util_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, asp_util_fix_zero, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, asp_util_fix_five, marker='s', linestyle='-.', label='50% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, asp_util_fix_nine, marker='8', linestyle='-.', label='90% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_asp_device_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_asp_device_low.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, vm_lst_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, vm_lst_fix_zero, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, vm_lst_fix_five, marker='s', linestyle='-.', label='50% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, vm_lst_fix_nine, marker='8', linestyle='-.', label='90% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Purchased\ VM}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_total_vm_device_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_total_vm_device_low.pdf')
    plt.close()



def plot_utility_device_num_step_low():
    print("device step")
    num = [600, 800, 1000, 1200, 1400]
    util_proposed = []
    social_proposed = []
    asp_util_proposed = []
    vm_lst_proposed = []
    util_fix_zero = []
    social_fix_zero = []
    asp_util_fix_zero = []
    vm_lst_fix_zero = []
    util_fix_five = []
    social_fix_five = []
    asp_util_fix_five = []
    vm_lst_fix_five = []
    util_fix_nine = []
    social_fix_nine = []
    asp_util_fix_nine = []
    vm_lst_fix_nine = []
    for n in num:
        u_zero = 0
        soc_zero = 0
        asp_u_zero = 0
        vm_zero = 0
        u_proposed = 0
        soc_proposed = 0
        asp_u_proposed = 0
        vm_proposed = 0
        u_five = 0
        soc_five = 0
        asp_u_five = 0
        vm_five = 0
        u_nine = 0
        soc_nine = 0
        asp_u_nine = 0
        vm_nine = 0
        i = 0
        pbar = tqdm(total=ITER)
        while i < ITER:
            try:
                mpo = MPO_low_load(0.1, n)
                util, max_phi, social, asp_u, vm_num = mpo.optimize_phi_with_step(0.5)
                u_proposed += util
                soc_proposed += social
                asp_u_proposed += asp_u
                vm_proposed += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0, max_phi)
                u_zero += util
                soc_zero += social
                asp_u_zero += asp_u
                vm_zero += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0.5, max_phi)
                u_five += util
                soc_five += social
                asp_u_five += asp_u
                vm_five += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0.9, max_phi)
                u_nine += util
                soc_nine += social
                asp_u_nine += asp_u
                vm_nine += vm_num
                i += 1
                pbar.update(1)
            except ArithmeticError as e:
                print(e)
        pbar.close()
        util_proposed.append(u_proposed / ITER)
        social_proposed.append(soc_proposed / ITER)
        asp_util_proposed.append(asp_u_proposed / ITER)
        vm_lst_proposed.append(vm_proposed / ITER)
        util_fix_zero.append(u_zero / ITER)
        social_fix_zero.append(soc_zero / ITER)
        asp_util_fix_zero.append(asp_u_zero / ITER)
        vm_lst_fix_zero.append(vm_zero / ITER)
        util_fix_five.append(u_five / ITER)
        social_fix_five.append(soc_five / ITER)
        asp_util_fix_five.append(asp_u_five / ITER)
        vm_lst_fix_five.append(vm_five / ITER)
        util_fix_nine.append(u_nine / ITER)
        social_fix_nine.append(soc_nine / ITER)
        asp_util_fix_nine.append(asp_u_nine / ITER)
        vm_lst_fix_nine.append(vm_nine / ITER)
    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, util_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, util_fix_zero, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, util_fix_five, marker='s', linestyle='-.', label='50% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, util_fix_nine, marker='8', linestyle='-.', label='90% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_MPO_device_step_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_MPO_device_step_low.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, social_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, social_fix_zero, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, social_fix_five, marker='s', linestyle='-.', label='50% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, social_fix_nine, marker='8', linestyle='-.', label='90% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_social_device_step_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_social_device_step_low.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, asp_util_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, asp_util_fix_zero, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, asp_util_fix_five, marker='s', linestyle='-.', label='50% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, asp_util_fix_nine, marker='8', linestyle='-.', label='90% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_asp_device_step_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_asp_device_step_low.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, vm_lst_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, vm_lst_fix_zero, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, vm_lst_fix_five, marker='s', linestyle='-.', label='50% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, vm_lst_fix_nine, marker='8', linestyle='-.', label='90% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Purchased\ VM}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_total_vm_device_step_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_total_vm_device_step_low.pdf')
    plt.close()
