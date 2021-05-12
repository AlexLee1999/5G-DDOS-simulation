from asp import ASP
from const import *
from device import Device
from mpo import MPO
import matplotlib.pyplot as plt

if __name__ == '__main__':
    mpo = MPO(0.5)
    mpo.plot_phi()
    asp = ASP(0.5)
    asp.plot_max()
    asp.plot_max_zh()


    ratio = [0.1, 0.3, 0.5, 0.7, 0.9]
    plt.figure(figsize=(20, 16), dpi=100)
    step = 5
    for ra in ratio:
        ut = []
        pr = []
        phi = 500
        mpo = MPO(ra)
        vm_prior = float('inf')
        for _ in range(1000):
            mpo.set_and_check_required_vm(phi)
            vm_after = mpo.total_vm()
            pr.append(phi)
            ut.append(phi * vm_after - MPO_cost(vm_after))
            phi += step
            if vm_prior < vm_after:
                print('Total VM is not non-increasing')
            vm_prior = vm_after
        plt.plot(pr, ut, marker='.', linestyle='-.', label=f'ratio : {ra}')
    plt.title('Utility of MPO', fontsize=30)
    plt.xlabel('MPO Price', fontsize=30)
    plt.ylabel('Utility', fontsize=30)
    plt.legend(loc="best")
    plt.savefig('./utility_ratio.jpg')
    plt.close()
