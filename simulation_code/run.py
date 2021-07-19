from asp import ASP
from const import *
from device import Device
from mpo import MPO
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
ITER = 1000

def plot_utility_device_num():
    print("device")
    num = [500, 750, 1000, 1250]
    util_proposed = []
    social_proposed = []
    asp_util_proposed = []
    util_fix_zero = []
    social_fix_zero = []
    asp_util_fix_zero = []
    util_fix_five = []
    social_fix_five = []
    asp_util_fix_five = []
    util_fix_nine = []
    social_fix_nine = []
    asp_util_fix_nine = []
    for n in num:
        u_zero = 0
        soc_zero = 0
        asp_u_zero = 0
        u_proposed = 0
        soc_proposed = 0
        asp_u_proposed = 0
        u_five = 0
        soc_five = 0
        asp_u_five = 0
        u_nine = 0
        soc_nine = 0
        asp_u_nine = 0
        for _ in tqdm(range(ITER)):
            mpo = MPO(0.1, n)
            util, max_phi, social, asp_u = mpo.optimize_phi()
            u_proposed += util
            soc_proposed += social
            asp_u_proposed += asp_u
            util, social, asp_u = mpo.optimize_phi_with_chi(0, max_phi)
            u_zero += util
            soc_zero += social
            asp_u_zero += asp_u
            util, social, asp_u = mpo.optimize_phi_with_chi(0.5, max_phi)
            u_five += util
            soc_five += social
            asp_u_five += asp_u
            util, social, asp_u = mpo.optimize_phi_with_chi(0.999, max_phi)
            u_nine += util
            soc_nine += social
            asp_u_nine += asp_u
        util_proposed.append(u_proposed / ITER)
        social_proposed.append(soc_proposed / ITER)
        asp_util_proposed.append(asp_u_proposed / ITER)
        util_fix_zero.append(u_zero / ITER)
        social_fix_zero.append(soc_zero / ITER)
        asp_util_fix_zero.append(asp_u_zero / ITER)
        util_fix_five.append(u_five / ITER)
        social_fix_five.append(soc_five / ITER)
        asp_util_fix_five.append(asp_u_five / ITER)
        util_fix_nine.append(u_nine / ITER)
        social_fix_nine.append(soc_nine / ITER)
        asp_util_fix_nine.append(asp_u_nine / ITER)
    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, util_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, util_fix_zero, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, util_fix_five, marker='s', linestyle='-.', label='50% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, util_fix_nine, marker='8', linestyle='-.', label='99.9% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_MPO_device.jpg')
    plt.savefig('./5GDDoS_Game_MPO_device.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, social_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, social_fix_zero, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, social_fix_five, marker='s', linestyle='-.', label='50% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, social_fix_nine, marker='8', linestyle='-.', label='99.9% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_social_device.jpg')
    plt.savefig('./5GDDoS_Game_social_device.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, asp_util_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, asp_util_fix_zero, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, asp_util_fix_five, marker='s', linestyle='-.', label='50% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, asp_util_fix_nine, marker='8', linestyle='-.', label='99.9% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_asp_device.jpg')
    plt.savefig('./5GDDoS_Game_asp_device.pdf')
    plt.close()

def plot_utility_ratio():
    print("ratio")
    ratio = [0.1, 0.3, 0.5, 0.7, 0.9]
    util_proposed = []
    social_proposed = []
    asp_util_proposed = []
    util_fix_zero = []
    social_fix_zero = []
    asp_util_fix_zero = []
    util_fix_five = []
    social_fix_five = []
    asp_util_fix_five = []
    util_fix_nine = []
    social_fix_nine = []
    asp_util_fix_nine = []
    for r in ratio:
        u_zero = 0
        soc_zero = 0
        asp_u_zero = 0
        u_proposed = 0
        soc_proposed = 0
        asp_u_proposed = 0
        u_five = 0
        soc_five = 0
        asp_u_five = 0
        u_nine = 0
        soc_nine = 0
        asp_u_nine = 0
        for _ in tqdm(range(ITER)):
            mpo = MPO(r, 1000)
            util, max_phi, social, asp_u = mpo.optimize_phi()
            u_proposed += util
            soc_proposed += social
            asp_u_proposed += asp_u
            util, social, asp_u = mpo.optimize_phi_with_chi(0, max_phi)
            u_zero += util
            soc_zero += social
            asp_u_zero += asp_u
            util, social, asp_u = mpo.optimize_phi_with_chi(0.5, max_phi)
            u_five += util
            soc_five += social
            asp_u_five += asp_u
            util, social, asp_u = mpo.optimize_phi_with_chi(0.999, max_phi)
            u_nine += util
            soc_nine += social
            asp_u_nine += asp_u
        util_proposed.append(u_proposed / ITER)
        social_proposed.append(soc_proposed / ITER)
        asp_util_proposed.append(asp_u_proposed / ITER)
        util_fix_zero.append(u_zero / ITER)
        social_fix_zero.append(soc_zero / ITER)
        asp_util_fix_zero.append(asp_u_zero / ITER)
        util_fix_five.append(u_five / ITER)
        social_fix_five.append(soc_five / ITER)
        asp_util_fix_five.append(asp_u_five / ITER)
        util_fix_nine.append(u_nine / ITER)
        social_fix_nine.append(soc_nine / ITER)
        asp_util_fix_nine.append(asp_u_nine / ITER)
    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(ratio, util_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(ratio, util_fix_zero, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(ratio, util_fix_five, marker='s', linestyle='-.', label='50% IPS VM', linewidth=7, markersize=30)
    plt.plot(ratio, util_fix_nine, marker='8', linestyle='-.', label='99.9% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Malicious\ Users\ to\ Normal\ Users\ Ratio}$', fontsize=100)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_MPO_ratio.jpg')
    plt.savefig('./5GDDoS_Game_MPO_ratio.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(ratio, social_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(ratio, social_fix_zero, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(ratio, social_fix_five, marker='s', linestyle='-.', label='50% IPS VM', linewidth=7, markersize=30)
    plt.plot(ratio, social_fix_nine, marker='8', linestyle='-.', label='99.9% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Malicious\ Users\ to\ Normal\ Users\ Ratio}$', fontsize=100)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_social_ratio.jpg')
    plt.savefig('./5GDDoS_Game_social_ratio.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(ratio, asp_util_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(ratio, asp_util_fix_zero, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(ratio, asp_util_fix_five, marker='s', linestyle='-.', label='50% IPS VM', linewidth=7, markersize=30)
    plt.plot(ratio, asp_util_fix_nine, marker='8', linestyle='-.', label='99.9% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Malicious\ Users\ to\ Normal\ Users\ Ratio}$', fontsize=100)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_asp_ratio.jpg')
    plt.savefig('./5GDDoS_Game_asp_ratio.pdf')
    plt.close()

def plot_ratio_with_same_IPS_ratio():
    print("same ratio")
    ratio = [0.1, 0.3, 0.5, 0.7, 0.9]
    util_proposed = []
    social_proposed = []
    asp_util_proposed = []
    util_fix = []
    social_fix = []
    asp_util_fix = []
    for r in ratio:
        u_fix = 0
        soc_fix = 0
        asp_u_fix = 0
        u_proposed = 0
        soc_proposed = 0
        asp_u_proposed = 0
        for _ in tqdm(range(ITER)):
            mpo = MPO(r, 1000)
            if r > 0.999:
                r = 0.999
            util, max_phi, social, asp_u = mpo.optimize_phi()
            u_proposed += util
            soc_proposed += social
            asp_u_proposed += asp_u
            util, social, asp_u = mpo.optimize_phi_with_chi(r, max_phi)
            u_fix += util
            soc_fix += social
            asp_u_fix += asp_u
        util_proposed.append(u_proposed / ITER)
        social_proposed.append(soc_proposed / ITER)
        asp_util_proposed.append(asp_u_proposed / ITER)
        util_fix.append(u_fix / ITER)
        social_fix.append(soc_fix / ITER)
        asp_util_fix.append(asp_u_fix / ITER)
    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(ratio, util_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(ratio, util_fix, marker='^', linestyle='-.', label='IPS ratio', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Malicious\ Users\ to\ Normal\ Users\ Ratio}$', fontsize=100)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_MPO_ratio_with_same_IPS_ratio.jpg')
    plt.savefig('./5GDDoS_Game_MPO_ratio_with_same_IPS_ratio.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(ratio, social_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(ratio, social_fix, marker='^', linestyle='-.', label='IPS ratio', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Malicious\ Users\ to\ Normal\ Users\ Ratio}$', fontsize=100)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_social_ratio_with_same_IPS_ratio.jpg')
    plt.savefig('./5GDDoS_Game_social_ratio_with_same_IPS_ratio.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(ratio, asp_util_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(ratio, asp_util_fix, marker='^', linestyle='-.', label='IPS ratio', linewidth=7, markersize=30)
    plt.xlabel(r'$\bf{Malicious\ Users\ to\ Normal\ Users\ Ratio}$', fontsize=100)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_asp_ratio_with_same_IPS_ratio.jpg')
    plt.savefig('./5GDDoS_Game_asp_ratio_with_same_IPS_ratio.pdf')
    plt.close()

def plot_different_step():
    print("step")
    num = [500, 750, 1000, 1250]
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
            _, max_phi, social, _ = mpo.optimize_phi_with_step(1)
            phi_step_1 += max_phi
            soc_step_1 += social
            _, max_phi, social, _ = mpo.optimize_phi_with_step(2)
            phi_step_5 += max_phi
            soc_step_5 += social
            _, max_phi, social, _ = mpo.optimize_phi_with_step(0.5)
            phi_step_10 += max_phi
            soc_step_10 += social
        phi_step_1_lst.append(phi_step_1 / ITER)
        social_step_1_lst.append(soc_step_1 / ITER)
        phi_step_5_lst.append(phi_step_5 / ITER)
        social_step_5_lst.append(soc_step_5 / ITER)
        phi_step_10_lst.append(phi_step_10 / ITER)
        social_step_10_lst.append(soc_step_10 / ITER)
    X = np.arange(4)
    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, phi_step_10_lst, marker='s', linestyle='-.', label='Step = 0.5', linewidth=7, markersize=30)
    plt.plot(num, phi_step_1_lst, marker='o', linestyle='-.', label='Step = 1', linewidth=7, markersize=30)
    plt.plot(num, phi_step_5_lst, marker='^', linestyle='-.', label='Step = 2', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Optimal\ MPO\ Price}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_price_device_with_step.jpg')
    plt.savefig('./5GDDoS_Game_price_device_with_step.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.bar(X + 0.00, social_step_10_lst, label='Step = 10', width=0.25)
    plt.bar(X + 0.25, social_step_1_lst, label='Step = 1', width=0.25)
    plt.bar(X + 0.50, social_step_5_lst, label='Step = 2', width=0.25)
    plt.legend(loc="best", fontsize=100)
    plt.xticks(X + (0.375 / 2), (500, 750, 1000, 1250))
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Social\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_social_device_with_step.jpg')
    plt.savefig('./5GDDoS_Game_social_device_with_step.pdf')
    plt.close()

def plot_max_vm():
    print("max vm")
    num = [500, 750, 1000, 1250]
    util_proposed = []
    social_proposed = []
    asp_util_proposed = []
    util_max_num = []
    social_max_num = []
    asp_util_max_num = []
    for n in num:
        u_max_num = 0
        soc_max_num = 0
        asp_u_max_num = 0
        u_proposed = 0
        soc_proposed = 0
        asp_u_proposed = 0
        for _ in tqdm(range(ITER)):
            mpo = MPO(0.1, n)
            util, max_phi, social, asp_u = mpo.optimize_phi()
            u_proposed += util
            soc_proposed += social
            asp_u_proposed += asp_u
            mpo.find_constraint_phi()
            phi = mpo.constraint_phi
            util, social, asp_u = mpo.optimize_phi_with_price(phi)
            u_max_num += util
            soc_max_num += social
            asp_u_max_num += asp_u
        util_proposed.append(u_proposed / ITER)
        social_proposed.append(soc_proposed / ITER)
        asp_util_proposed.append(asp_u_proposed / ITER)
        util_max_num.append(u_max_num / ITER)
        social_max_num.append(soc_max_num / ITER)
        asp_util_max_num.append(asp_u_max_num / ITER)
    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, util_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, util_max_num, marker='^', linestyle='-.', label='Max VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_MPO_device_max_num.jpg')
    plt.savefig('./5GDDoS_Game_MPO_device_max_num.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, social_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, social_max_num, marker='^', linestyle='-.', label='Max VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_social_device_max_num.jpg')
    plt.savefig('./5GDDoS_Game_social_device_max_num.pdf')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, asp_util_proposed, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, asp_util_max_num, marker='^', linestyle='-.', label='Max VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_asp_device_max_num.jpg')
    plt.savefig('./5GDDoS_Game_asp_device_max_num.pdf')
    plt.close()

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
    util_proposed, max_phi, _, _ = mpo.optimize_phi()
    print(util_proposed, max_phi)
    ut_lst_proposed = []
    ut_lst_flat = []
    for p in price:
        mpo.set_and_check_required_vm(p)
        vm_num = mpo.total_vm()
        uti = p * vm_num - MPO_cost(vm_num)
        ut_lst_flat.append(uti)
        ut_lst_proposed.append(util_proposed)
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



if __name__ == '__main__':
    #mpo = MPO(0.1, 1000)
    #mpo.plot_MPO_utility()
    #mpo.plot_social_welfare()
    #mpo.plot_asp_utility()
    #asp = ASP(0.1, 1000)
    #asp.plot_max()
    #asp.plot_max_zh()
    #plot_different_ratio()
    plot_utility_device_num()
    plot_utility_ratio()
    plot_different_step()
    plot_max_vm()
    plot_ratio_with_same_IPS_ratio()
    #plot_flat_price()

