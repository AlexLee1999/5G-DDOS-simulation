from asp import ASP
from const import *
from device import Device
from mpo import MPO
import matplotlib.pyplot as plt
from tqdm import tqdm
ITER = 1000

def plot_utility_device_num():
    num = [i for i in range(50, 300, 50)]
    util_proposed = []
    social_proposed = []
    asp_util_proposed = []
    util_fix_zero = []
    social_fix_zero = []
    asp_util_fix_zero = []
    util_fix_three = []
    social_fix_three = []
    asp_util_fix_three = []
    for n in num:
        u_zero = 0
        soc_zero = 0
        asp_u_zero = 0
        u_proposed = 0
        soc_proposed = 0
        asp_u_proposed = 0
        u_three = 0
        soc_three = 0
        asp_u_three = 0
        for _ in tqdm(range(ITER)):
            mpo = MPO(0.5, n)
            util, max_phi, social, asp_u = mpo.optimize_phi()
            u_proposed += util
            soc_proposed += social
            asp_u_proposed += asp_u
            util, social, asp_u = mpo.optimize_phi_with_chi(0, max_phi)
            u_zero += util
            soc_zero += social
            asp_u_zero += asp_u
            util, social, asp_u = mpo.optimize_phi_with_chi(0.3, max_phi)
            u_three += util
            soc_three += social
            asp_u_three += asp_u
        util_proposed.append(u_proposed / ITER)
        social_proposed.append(soc_proposed / ITER)
        asp_util_proposed.append(asp_u_proposed / ITER)
        util_fix_zero.append(u_zero / ITER)
        social_fix_zero.append(soc_zero / ITER)
        asp_util_fix_zero.append(asp_u_zero / ITER)
        util_fix_three.append(u_three / ITER)
        social_fix_three.append(soc_three / ITER)
        asp_util_fix_three.append(asp_u_three / ITER)
    plt.figure(figsize=(42, 25), dpi=400)
    plt.plot(num, util_proposed, marker='o', linestyle='-.', label='Proposed', linewidth=7, markersize=30)
    plt.plot(num, util_fix_zero, marker='^', linestyle='-.', label='No IPS VM', linewidth=7, markersize=30)
    plt.plot(num, util_fix_three, marker='s', linestyle='-.', label='30% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_MPO_device.jpg')
    plt.savefig('./5GDDoS_Game_MPO_device.pdf')
    plt.close()

    plt.figure(figsize=(42, 25), dpi=400)
    plt.plot(num, social_proposed, marker='o', linestyle='-.', label='Proposed', linewidth=7, markersize=30)
    plt.plot(num, social_fix_zero, marker='^', linestyle='-.', label='No IPS VM', linewidth=7, markersize=30)
    plt.plot(num, social_fix_three, marker='s', linestyle='-.', label='30% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_social_device.jpg')
    plt.savefig('./5GDDoS_Game_social_device.pdf')
    plt.close()

    plt.figure(figsize=(42, 25), dpi=400)
    plt.plot(num, asp_util_proposed, marker='o', linestyle='-.', label='Proposed', linewidth=7, markersize=30)
    plt.plot(num, asp_util_fix_zero, marker='^', linestyle='-.', label='No IPS VM', linewidth=7, markersize=30)
    plt.plot(num, asp_util_fix_three, marker='s', linestyle='-.', label='30% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_asp_device.jpg')
    plt.savefig('./5GDDoS_Game_asp_device.pdf')
    plt.close()

def plot_utility_ratio():
    ratio = [0.1, 0.3, 0.5, 0.7, 0.9]
    util_proposed = []
    social_proposed = []
    asp_util_proposed = []
    util_fix_zero = []
    social_fix_zero = []
    asp_util_fix_zero = []
    util_fix_three = []
    social_fix_three = []
    asp_util_fix_three = []
    for r in ratio:
        u_zero = 0
        soc_zero = 0
        asp_u_zero = 0
        u_proposed = 0
        soc_proposed = 0
        asp_u_proposed = 0
        u_three = 0
        soc_three = 0
        asp_u_three = 0
        for _ in tqdm(range(ITER)):
            mpo = MPO(r, 100)
            util, max_phi, social, asp_u = mpo.optimize_phi()
            u_proposed += util
            soc_proposed += social
            asp_u_proposed += asp_u
            util, social, asp_u = mpo.optimize_phi_with_chi(0, max_phi)
            u_zero += util
            soc_zero += social
            asp_u_zero += asp_u
            util, social, asp_u = mpo.optimize_phi_with_chi(0.3, max_phi)
            u_three += util
            soc_three += social
            asp_u_three += asp_u
        util_proposed.append(u_proposed / ITER)
        social_proposed.append(soc_proposed / ITER)
        asp_util_proposed.append(asp_u_proposed / ITER)
        util_fix_zero.append(u_zero / ITER)
        social_fix_zero.append(soc_zero / ITER)
        asp_util_fix_zero.append(asp_u_zero / ITER)
        util_fix_three.append(u_three / ITER)
        social_fix_three.append(soc_three / ITER)
        asp_util_fix_three.append(asp_u_three / ITER)
    plt.figure(figsize=(42, 25), dpi=400)
    plt.plot(ratio, util_proposed, marker='o', linestyle='-.', label='Proposed', linewidth=7, markersize=30)
    plt.plot(ratio, util_fix_zero, marker='^', linestyle='-.', label='No IPS VM', linewidth=7, markersize=30)
    plt.plot(ratio, util_fix_three, marker='s', linestyle='-.', label='30% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Malicious\ Users\ to\ Normal\ Users\ Ratio}$', fontsize=100)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_MPO_ratio.jpg')
    plt.savefig('./5GDDoS_Game_MPO_ratio.pdf')
    plt.close()

    plt.figure(figsize=(42, 25), dpi=400)
    plt.plot(ratio, social_proposed, marker='o', linestyle='-.', label='Proposed', linewidth=7, markersize=30)
    plt.plot(ratio, social_fix_zero, marker='^', linestyle='-.', label='No IPS VM', linewidth=7, markersize=30)
    plt.plot(ratio, social_fix_three, marker='s', linestyle='-.', label='30% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Malicious\ Users\ to\ Normal\ Users\ Ratio}$', fontsize=100)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_social_ratio.jpg')
    plt.savefig('./5GDDoS_Game_social_ratio.pdf')
    plt.close()

    plt.figure(figsize=(42, 25), dpi=400)
    plt.plot(ratio, asp_util_proposed, marker='o', linestyle='-.', label='Proposed', linewidth=7, markersize=30)
    plt.plot(ratio, asp_util_fix_zero, marker='^', linestyle='-.', label='No IPS VM', linewidth=7, markersize=30)
    plt.plot(ratio, asp_util_fix_three, marker='s', linestyle='-.', label='30% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Malicious\ Users\ to\ Normal\ Users\ Ratio}$', fontsize=100)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./5GDDoS_Game_asp_ratio.jpg')
    plt.savefig('./5GDDoS_Game_asp_ratio.pdf')
    plt.close()



def plot_different_ratio():
    ratio = [0.1, 0.3, 0.5, 0.7, 0.9]
    plt.figure(figsize=(42, 25), dpi=400)
    step = 0.5
    for ra in ratio:
        ut = []
        pr = []
        phi = 10
        mpo = MPO(ra, 100)
        vm_prior = float('inf')
        for _ in range(1000):
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

if __name__ == '__main__':
    # mpo = MPO(0.5, 100)
    # mpo.plot_phi()
    # mpo.plot_social_welfare()
    # asp = ASP(0.5, 100)
    # asp.plot_max()
    # asp.plot_max_zh()
    # plot_different_ratio()
    # plot_utility_device_num()
    plot_utility_ratio()
    # lst = []
    # for _ in range(100):
    #     asp = ASP(0.5, 100)
    #     lst.append(asp.service_rate)
    # print(sum(lst)/100)
