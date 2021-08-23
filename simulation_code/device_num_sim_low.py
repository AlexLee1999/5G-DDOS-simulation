from const import *
from mpo import *
from convex_solver import *
import matplotlib
matplotlib.use('agg') 
import matplotlib.pyplot as plt
from tqdm import tqdm


def plot_utility_device_num_low():
    print("device low")
    num = [600, 800, 1000, 1200, 1400]
    utility_proposed_lst = []
    social_proposed_lst = []
    asp_utility_proposed_lst = []
    vm_proposed_lst = []
    utility_zero_lst = []
    social_zero_lst = []
    asp_utility_zero_lst = []
    vm_zero_lst = []
    utility_five_lst = []
    social_five_lst = []
    asp_utility_five_lst = []
    vm_five_lst = []
    utility_nine_lst = []
    social_nine_lst = []
    asp_utility_nine_lst = []
    vm_nine_lst = []
    for n in num:
        utility_zero = 0
        social_zero = 0
        asp_utility_zero = 0
        vm_zero = 0
        utility_proposed = 0
        social_proposed = 0
        asp_utility_proposed = 0
        vm_proposed = 0
        utility_five = 0
        social_five = 0
        asp_utility_five = 0
        vm_five = 0
        utility_nine = 0
        social_nine = 0
        asp_utility_nine = 0
        vm_nine = 0
        i = 0
        pbar = tqdm(total=ITER)
        while i < ITER:
            try:
                mpo = MPO(DEFAULT_DEVICE_RATIO, n, load_type.LOW)
                util, max_phi, social, asp_u, vm_num = mpo.optimize_phi()
                utility_proposed += util
                social_proposed += social
                asp_utility_proposed += asp_u
                vm_proposed += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0, max_phi)
                utility_zero += util
                social_zero += social
                asp_utility_zero += asp_u
                vm_zero += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0.05, max_phi)
                utility_five += util
                social_five += social
                asp_utility_five += asp_u
                vm_five += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0.09, max_phi)
                utility_nine += util
                social_nine += social
                asp_utility_nine += asp_u
                vm_nine += vm_num
                i += 1
                pbar.update(1)
            except ArithmeticError as e:
                print(e)
        pbar.close()
        utility_proposed_lst.append(utility_proposed / ITER)
        social_proposed_lst.append(social_proposed / ITER)
        asp_utility_proposed_lst.append(asp_utility_proposed / ITER)
        vm_proposed_lst.append(vm_proposed / ITER)
        utility_zero_lst.append(utility_zero / ITER)
        social_zero_lst.append(social_zero / ITER)
        asp_utility_zero_lst.append(asp_utility_zero / ITER)
        vm_zero_lst.append(vm_zero / ITER)
        utility_five_lst.append(utility_five / ITER)
        social_five_lst.append(social_five / ITER)
        asp_utility_five_lst.append(asp_utility_five / ITER)
        vm_five_lst.append(vm_five / ITER)
        utility_nine_lst.append(utility_nine / ITER)
        social_nine_lst.append(social_nine / ITER)
        asp_utility_nine_lst.append(asp_utility_nine / ITER)
        vm_nine_lst.append(vm_nine / ITER)
    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, utility_proposed_lst, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, utility_zero_lst, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, utility_five_lst, marker='s', linestyle='-.', label='5% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, utility_nine_lst, marker='8', linestyle='-.', label='9% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_MPO_device_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_MPO_device_low.pdf')
    plt.savefig('./image/device_number_low/5GDDoS_Game_MPO_device_low.eps')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, social_proposed_lst, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, social_zero_lst, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, social_five_lst, marker='s', linestyle='-.', label='5% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, social_nine_lst, marker='8', linestyle='-.', label='9% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_social_device_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_social_device_low.pdf')
    plt.savefig('./image/device_number_low/5GDDoS_Game_social_device_low.eps')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, asp_utility_proposed_lst, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, asp_utility_zero_lst, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, asp_utility_five_lst, marker='s', linestyle='-.', label='5% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, asp_utility_nine_lst, marker='8', linestyle='-.', label='9% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_asp_device_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_asp_device_low.pdf')
    plt.savefig('./image/device_number_low/5GDDoS_Game_asp_device_low.eps')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, vm_proposed_lst, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, vm_zero_lst, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, vm_five_lst, marker='s', linestyle='-.', label='5% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, vm_nine_lst, marker='8', linestyle='-.', label='9% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Purchased\ VM}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_total_vm_device_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_total_vm_device_low.pdf')
    plt.savefig('./image/device_number_low/5GDDoS_Game_total_vm_device_low.eps')
    plt.close()



def plot_utility_device_num_step_low():
    print("device low step")
    num = [600, 800, 1000, 1200, 1400]
    utility_proposed_lst = []
    social_proposed_lst = []
    asp_utility_proposed_lst = []
    vm_proposed_lst = []
    utility_zero_lst = []
    social_zero_lst = []
    asp_utility_zero_lst = []
    vm_zero_lst = []
    utility_five_lst = []
    social_five_lst = []
    asp_utility_five_lst = []
    vm_five_lst = []
    utility_nine_lst = []
    social_nine_lst = []
    asp_utility_nine_lst = []
    vm_nine_lst = []
    for n in num:
        utility_zero = 0
        social_zero = 0
        asp_utility_zero = 0
        vm_zero = 0
        utility_proposed = 0
        social_proposed = 0
        asp_utility_proposed = 0
        vm_proposed = 0
        utility_five = 0
        social_five = 0
        asp_utility_five = 0
        vm_five = 0
        utility_nine = 0
        social_nine = 0
        asp_utility_nine = 0
        vm_nine = 0
        i = 0
        pbar = tqdm(total=ITER)
        while i < ITER:
            try:
                mpo = MPO(DEFAULT_DEVICE_RATIO, n, load_type.LOW)
                util, max_phi, social, asp_u, vm_num = mpo.optimize_phi_with_step(1)
                utility_proposed += util
                social_proposed += social
                asp_utility_proposed += asp_u
                vm_proposed += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0, max_phi)
                utility_zero += util
                social_zero += social
                asp_utility_zero += asp_u
                vm_zero += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0.05, max_phi)
                utility_five += util
                social_five += social
                asp_utility_five += asp_u
                vm_five += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0.09, max_phi)
                utility_nine += util
                social_nine += social
                asp_utility_nine += asp_u
                vm_nine += vm_num
                i += 1
                pbar.update(1)
            except ArithmeticError as e:
                print(e)
        pbar.close()
        utility_proposed_lst.append(utility_proposed / ITER)
        social_proposed_lst.append(social_proposed / ITER)
        asp_utility_proposed_lst.append(asp_utility_proposed / ITER)
        vm_proposed_lst.append(vm_proposed / ITER)
        utility_zero_lst.append(utility_zero / ITER)
        social_zero_lst.append(social_zero / ITER)
        asp_utility_zero_lst.append(asp_utility_zero / ITER)
        vm_zero_lst.append(vm_zero / ITER)
        utility_five_lst.append(utility_five / ITER)
        social_five_lst.append(social_five / ITER)
        asp_utility_five_lst.append(asp_utility_five / ITER)
        vm_five_lst.append(vm_five / ITER)
        utility_nine_lst.append(utility_nine / ITER)
        social_nine_lst.append(social_nine / ITER)
        asp_utility_nine_lst.append(asp_utility_nine / ITER)
        vm_nine_lst.append(vm_nine / ITER)
    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, utility_proposed_lst, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, utility_zero_lst, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, utility_five_lst, marker='s', linestyle='-.', label='5% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, utility_nine_lst, marker='8', linestyle='-.', label='9% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_MPO_device_step_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_MPO_device_step_low.pdf')
    plt.savefig('./image/device_number_low/5GDDoS_Game_MPO_device_step_low.eps')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, social_proposed_lst, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, social_zero_lst, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, social_five_lst, marker='s', linestyle='-.', label='5% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, social_nine_lst, marker='8', linestyle='-.', label='9% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_social_device_step_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_social_device_step_low.pdf')
    plt.savefig('./image/device_number_low/5GDDoS_Game_social_device_step_low.eps')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, asp_utility_proposed_lst, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, asp_utility_zero_lst, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, asp_utility_five_lst, marker='s', linestyle='-.', label='5% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, asp_utility_nine_lst, marker='8', linestyle='-.', label='9% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_asp_device_step_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_asp_device_step_low.pdf')
    plt.savefig('./image/device_number_low/5GDDoS_Game_asp_device_step_low.eps')
    plt.close()

    plt.figure(figsize=(45, 25), dpi=400)
    plt.plot(num, vm_proposed_lst, marker='o', linestyle='-.', label='Proposed Scheme', linewidth=7, markersize=30)
    plt.plot(num, vm_zero_lst, marker='^', linestyle='-.', label='No IPS', linewidth=7, markersize=30)
    plt.plot(num, vm_five_lst, marker='s', linestyle='-.', label='5% IPS VM', linewidth=7, markersize=30)
    plt.plot(num, vm_nine_lst, marker='8', linestyle='-.', label='9% IPS VM', linewidth=7, markersize=30)
    plt.legend(loc="best", fontsize=100)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=100)
    plt.ylabel(r'$\bf{Purchased\ VM}$', fontsize=100)
    plt.xticks(fontsize=80)
    plt.yticks(fontsize=80)
    plt.savefig('./image/device_number_low/5GDDoS_Game_total_vm_device_step_low.jpg')
    plt.savefig('./image/device_number_low/5GDDoS_Game_total_vm_device_step_low.pdf')
    plt.savefig('./image/device_number_low/5GDDoS_Game_total_vm_device_step_low.eps')
    plt.close()
