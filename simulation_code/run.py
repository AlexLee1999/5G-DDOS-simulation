from asp import ASP
from const import *
from device import Device
from mpo import MPO
import matplotlib.pyplot as plt


def plot_MPO_utility_device_num():
    num = [i for i in range(50, 250, 50)]
    util_proposed = []
    util_fix_zero = []
    util_fix_three = []
    for n in num:
        mpo = MPO(0.5, n)
        util, _ = mpo.optimize_phi()
        util_proposed.append(util)
        util, _ = mpo.optimize_phi_with_chi(0)
        util_fix_zero.append(util)
        util, _ = mpo.optimize_phi_with_chi(0.3)
        util_fix_three.append(util)
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


def plot_social_device_num():
    num = [i for i in range(50, 250, 50)]
    util_proposed = []
    util_fix_zero = []
    util_fix_three = []
    for n in num:
        mpo = MPO(0.5, n)
        util, _ = mpo.optimize_phi_social()
        util_proposed.append(util)
        util, _ = mpo.optimize_phi_social_with_chi(0)
        util_fix_zero.append(util)
        util, _ = mpo.optimize_phi_social_with_chi(0.3)
        util_fix_three.append(util)
    plt.figure(figsize=(25, 16), dpi=400)
    plt.plot(num, util_proposed, marker='o', linestyle='-.', label='Proposed')
    plt.plot(num, util_fix_zero, marker='^', linestyle='-.', label='No IPS VM')
    plt.plot(num, util_fix_three, marker='s', linestyle='-.', label='30% IPS VM')
    plt.legend(loc="best", fontsize=60)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=60)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=60)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.savefig('./5GDDoS_Game_social_device.jpg')
    plt.savefig('./5GDDoS_Game_social_device.pdf')
    plt.close()


def plot_asp_device_num():
    num = [i for i in range(50, 250, 50)]
    util_proposed = []
    util_fix_zero = []
    util_fix_three = []
    for n in num:
        mpo = MPO(0.5, n)
        util, _ = mpo.optimize_phi_asp()
        util_proposed.append(util)
        util, _ = mpo.optimize_phi_asp_with_chi(0)
        util_fix_zero.append(util)
        util, _ = mpo.optimize_phi_asp_with_chi(0.3)
        util_fix_three.append(util)
    plt.figure(figsize=(25, 16), dpi=400)
    plt.plot(num, util_proposed, marker='o', linestyle='-.', label='Proposed')
    plt.plot(num, util_fix_zero, marker='^', linestyle='-.', label='No IPS VM')
    plt.plot(num, util_fix_three, marker='s', linestyle='-.', label='30% IPS VM')
    plt.legend(loc="best", fontsize=60)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=60)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=60)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    plt.savefig('./5GDDoS_Game_asp_device.jpg')
    plt.savefig('./5GDDoS_Game_asp_device.pdf')
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
    # plot_MPO_utility_device_num()
    # plot_social_device_num()
    plot_asp_device_num()
