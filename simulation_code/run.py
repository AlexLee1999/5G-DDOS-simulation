from asp import ASP
from const import *
from device import Device
from mpo import MPO
import matplotlib.pyplot as plt

if __name__ == '__main__':
    mpo = MPO(0.5)
    mpo.plot_phi()
    mpo.plot_social_welfare()
    asp = ASP(0.5)
    asp.plot_max()
    asp.plot_max_zh()


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
