from asp import ASP
from const import *
from device import Device
from mpo import MPO
import matplotlib.pyplot as plt


def plot_utility_device_num():
    num = [i for i in range(50, 250, 10)]
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
        mpo = MPO(0.5, n)
        util, max_phi, social, asp_u = mpo.optimize_phi()
        util_proposed.append(util)
        social_proposed.append(social)
        asp_util_proposed.append(asp_u)
        util, social, asp_u = mpo.optimize_phi_with_chi(0, max_phi)
        util_fix_zero.append(util)
        social_fix_zero.append(social)
        asp_util_fix_zero.append(asp_u)
        util, social, asp_u = mpo.optimize_phi_with_chi(0.3, max_phi)
        util_fix_three.append(util)
        social_fix_three.append(social)
        asp_util_fix_three.append(asp_u)
    plt.figure(figsize=(25, 16), dpi=400)
    plt.plot(num, util_proposed, marker='o', linestyle='-.', label='Proposed')
    plt.plot(num, util_fix_zero, marker='^', linestyle='-.', label='No IPS VM')
    plt.plot(num, util_fix_three, marker='s', linestyle='-.', label='30% IPS VM')
    plt.legend(loc="best", fontsize=60)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=60)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=60)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.savefig('./5GDDoS_Game_MPO_device.jpg')
    plt.savefig('./5GDDoS_Game_MPO_device.pdf')
    plt.close()

    plt.figure(figsize=(25, 16), dpi=400)
    plt.plot(num, social_proposed, marker='o', linestyle='-.', label='Proposed')
    plt.plot(num, social_fix_zero, marker='^', linestyle='-.', label='50% IPS VM')
    plt.plot(num, social_fix_three, marker='s', linestyle='-.', label='30% IPS VM')
    plt.legend(loc="best", fontsize=60)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=60)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=60)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.savefig('./5GDDoS_Game_social_device.jpg')
    plt.savefig('./5GDDoS_Game_social_device.pdf')
    plt.close()

    plt.figure(figsize=(25, 16), dpi=400)
    plt.plot(num, asp_util_proposed, marker='o', linestyle='-.', label='Proposed')
    plt.plot(num, asp_util_fix_zero, marker='^', linestyle='-.', label='50% IPS VM')
    plt.plot(num, asp_util_fix_three, marker='s', linestyle='-.', label='30% IPS VM')
    plt.legend(loc="best", fontsize=60)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=60)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=60)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.savefig('./5GDDoS_Game_asp_device.jpg')
    plt.savefig('./5GDDoS_Game_asp_device.pdf')
    plt.close()

def plot_utility_ratio():
    ratio = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

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
        mpo = MPO(r, 50)
        util, max_phi, social, asp_u = mpo.optimize_phi()
        util_proposed.append(util)
        social_proposed.append(social)
        asp_util_proposed.append(asp_u)
        util, social, asp_u = mpo.optimize_phi_with_chi(0, max_phi)
        util_fix_zero.append(util)
        social_fix_zero.append(social)
        asp_util_fix_zero.append(asp_u)
        util, social, asp_u = mpo.optimize_phi_with_chi(0.3, max_phi)
        util_fix_three.append(util)
        social_fix_three.append(social)
        asp_util_fix_three.append(asp_u)
    plt.figure(figsize=(25, 16), dpi=400)
    plt.plot(ratio, util_proposed, marker='o', linestyle='-.', label='Proposed')
    plt.plot(ratio, util_fix_zero, marker='^', linestyle='-.', label='No IPS VM')
    plt.plot(ratio, util_fix_three, marker='s', linestyle='-.', label='30% IPS VM')
    plt.legend(loc="best", fontsize=60)
    plt.xlabel(r'$\bf{Ratio}$', fontsize=60)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=60)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.savefig('./5GDDoS_Game_MPO_ratio.jpg')
    plt.savefig('./5GDDoS_Game_MPO_ratio.pdf')
    plt.close()

    plt.figure(figsize=(25, 16), dpi=400)
    plt.plot(ratio, social_proposed, marker='o', linestyle='-.', label='Proposed')
    plt.plot(ratio, social_fix_zero, marker='^', linestyle='-.', label='50% IPS VM')
    plt.plot(ratio, social_fix_three, marker='s', linestyle='-.', label='30% IPS VM')
    plt.legend(loc="best", fontsize=60)
    plt.xlabel(r'$\bf{Ratio}$', fontsize=60)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=60)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.savefig('./5GDDoS_Game_social_ratio.jpg')
    plt.savefig('./5GDDoS_Game_social_ratio.pdf')
    plt.close()

    plt.figure(figsize=(25, 16), dpi=400)
    plt.plot(ratio, asp_util_proposed, marker='o', linestyle='-.', label='Proposed')
    plt.plot(ratio, asp_util_fix_zero, marker='^', linestyle='-.', label='50% IPS VM')
    plt.plot(ratio, asp_util_fix_three, marker='s', linestyle='-.', label='30% IPS VM')
    plt.legend(loc="best", fontsize=60)
    plt.xlabel(r'$\bf{Ratio}$', fontsize=60)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=60)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.savefig('./5GDDoS_Game_asp_ratio.jpg')
    plt.savefig('./5GDDoS_Game_asp_ratio.pdf')
    plt.close()



def plot_different_ratio():
    ratio = [0.1, 0.3, 0.5, 0.7, 0.9]
    plt.figure(figsize=(25, 16), dpi=400)
    step = 0.5
    for ra in ratio:
        ut = []
        pr = []
        phi = 10
        mpo = MPO(ra)
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
        plt.plot(pr, ut, marker='.', linestyle='-.', label=f'ratio : {ra}')
    plt.xlabel(r'$\bf{MPO\ Price}$', fontsize=60)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=60)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.legend(loc="best", fontsize=60)
    plt.savefig('./5GDDoS_Game_utility_ratio.pdf')
    plt.savefig('./5GDDoS_Game_utility_ratio.jpg')
    plt.close()

if __name__ == '__main__':
    # mpo = MPO(0.5, 50)
    # mpo.plot_phi()
    # mpo.plot_social_welfare()
    # asp = ASP(0.5, 50)
    # asp.plot_max()
    # asp.plot_max_zh()
    # plot_different_ratio()
    plot_utility_device_num()
    plot_utility_ratio()