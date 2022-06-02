import traceback
from tqdm import tqdm
import matplotlib.pyplot as plt
from const import *
from mpo import MPO
from convex_solver import *



def plot_utility_device_num_cvx():
    print("device")
    num = NUM_LST
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
    utility_seven_lst = []
    social_seven_lst = []
    asp_utility_seven_lst = []
    vm_seven_lst = []
    for n in num:
        print(n, flush=True)
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
        utility_seven = 0
        social_seven = 0
        asp_utility_seven = 0
        vm_seven = 0
        i = 0
        pbar = tqdm(total=ITER)
        while i < ITER:
            try:
                mpo = MPO(DEFAULT_DEVICE_RATIO, n,
                          load_type.AVERAGE, MPO_NUM_OF_ASP, DEFAULT_ETA)
                util, max_phi, social, asp_u, vm_num = mpo.optimize_phi()
                utility_proposed += util
                social_proposed += social
                asp_utility_proposed += asp_u
                vm_proposed += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(
                    0, max_phi)
                utility_zero += util
                social_zero += social
                asp_utility_zero += asp_u
                vm_zero += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(
                    0.05, max_phi)
                utility_five += util
                social_five += social
                asp_utility_five += asp_u
                vm_five += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(
                    0.07, max_phi)
                utility_seven += util
                social_seven += social
                asp_utility_seven += asp_u
                vm_seven += vm_num
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
        utility_seven_lst.append(utility_seven / ITER)
        social_seven_lst.append(social_seven / ITER)
        asp_utility_seven_lst.append(asp_utility_seven / ITER)
        vm_seven_lst.append(vm_seven / ITER)
    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.plot(num, utility_proposed_lst, marker='o', markerfacecolor='none',
             label='Proposed Scheme', linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, utility_zero_lst, marker='^', markerfacecolor='none', label='No IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, utility_five_lst, marker='s', markerfacecolor='none', label='5% IPS VM',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, utility_seven_lst, marker='p', markerfacecolor='none', label='7% IPS VM',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=LABEL_FONT_SIZE)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig('./image/device_number/5GDDoS_Game_MPO_device_cvx.jpg')
    plt.savefig('./image/device_number/5GDDoS_Game_MPO_device_cvx.pdf')
    plt.savefig('./image/device_number/5GDDoS_Game_MPO_device_cvx.eps')
    plt.close()

    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.plot(num, social_proposed_lst, marker='o', markerfacecolor='none',
             label='Proposed Scheme', linewidth=LINE_WIDTH, markersize=MARKER_SIZE)
    plt.plot(num, social_zero_lst, marker='^', markerfacecolor='none',
             label='No IPS', linewidth=LINE_WIDTH, markersize=MARKER_SIZE)
    plt.plot(num, social_five_lst, marker='s', markerfacecolor='none',
             label='5% IPS VM', linewidth=LINE_WIDTH, markersize=MARKER_SIZE)
    plt.plot(num, social_seven_lst, marker='p', markerfacecolor='none',
             label='7% IPS VM', linewidth=LINE_WIDTH, markersize=MARKER_SIZE)
    plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=LABEL_FONT_SIZE)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig('./image/device_number/5GDDoS_Game_social_device_cvx.jpg')
    plt.savefig('./image/device_number/5GDDoS_Game_social_device_cvx.pdf')
    plt.savefig('./image/device_number/5GDDoS_Game_social_device_cvx.eps')
    plt.close()

    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.plot(num, asp_utility_proposed_lst, marker='o', markerfacecolor='none',
             label='Proposed Scheme', linewidth=LINE_WIDTH, markersize=MARKER_SIZE)
    plt.plot(num, asp_utility_zero_lst, marker='^', markerfacecolor='none',
             label='No IPS', linewidth=LINE_WIDTH, markersize=MARKER_SIZE)
    plt.plot(num, asp_utility_five_lst, marker='s', markerfacecolor='none',
             label='5% IPS VM', linewidth=LINE_WIDTH, markersize=MARKER_SIZE)
    plt.plot(num, asp_utility_seven_lst, marker='p', markerfacecolor='none',
             label='7% IPS VM', linewidth=LINE_WIDTH, markersize=MARKER_SIZE)
    plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=LABEL_FONT_SIZE)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig('./image/device_number/5GDDoS_Game_asp_device_cvx.jpg')
    plt.savefig('./image/device_number/5GDDoS_Game_asp_device_cvx.pdf')
    plt.savefig('./image/device_number/5GDDoS_Game_asp_device_cvx.eps')
    plt.close()

    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.plot(num, vm_proposed_lst, marker='o', markerfacecolor='none',
             label='Proposed Scheme', linewidth=LINE_WIDTH, markersize=MARKER_SIZE)
    plt.plot(num, vm_zero_lst, marker='^', markerfacecolor='none',
             label='No IPS', linewidth=LINE_WIDTH, markersize=MARKER_SIZE)
    plt.plot(num, vm_five_lst, marker='s', markerfacecolor='none',
             label='5% IPS VM', linewidth=LINE_WIDTH, markersize=MARKER_SIZE)
    plt.plot(num, vm_seven_lst, marker='p', markerfacecolor='none',
             label='7% IPS VM', linewidth=LINE_WIDTH, markersize=MARKER_SIZE)
    plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=LABEL_FONT_SIZE)
    plt.ylabel(r'$\bf{Purchased\ VM}$', fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig('./image/device_number/5GDDoS_Game_total_vm_device_cvx.jpg')
    plt.savefig('./image/device_number/5GDDoS_Game_total_vm_device_cvx.pdf')
    plt.savefig('./image/device_number/5GDDoS_Game_total_vm_device_cvx.eps')
    plt.close()


def plot_utility_device_num_step():
    print("device step")
    num = NUM_LST
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
    utility_seven_lst = []
    social_seven_lst = []
    asp_utility_seven_lst = []
    vm_seven_lst = []
    for n in num:
        print(n, flush=True)
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
        utility_seven = 0
        social_seven = 0
        asp_utility_seven = 0
        vm_seven = 0
        i = 0
        pbar = tqdm(total=ITER)
        while i < ITER:
            try:
                mpo = MPO(DEFAULT_DEVICE_RATIO, n,
                          load_type.AVERAGE, MPO_NUM_OF_ASP, DEFAULT_ETA)
                util, max_phi, social, asp_u, vm_num = mpo.optimize_phi_with_step(
                    STEP)
                utility_proposed += util
                social_proposed += social
                asp_utility_proposed += asp_u
                vm_proposed += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(
                    0, max_phi)
                # util, social, asp_u, vm_num = mpo.optimize_phi_with_step_chi(1, 0)
                utility_zero += util
                social_zero += social
                asp_utility_zero += asp_u
                vm_zero += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(
                    0.05, max_phi)
                # util, social, asp_u, vm_num = mpo.optimize_phi_with_step_chi(1, 0.05)

                utility_five += util
                social_five += social
                asp_utility_five += asp_u
                vm_five += vm_num
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(
                    0.07, max_phi)
                # util, social, asp_u, vm_num = mpo.optimize_phi_with_step_chi(1, 0.07)
                utility_seven += util
                social_seven += social
                asp_utility_seven += asp_u
                vm_seven += vm_num

                i += 1
                pbar.update(1)
            except ArithmeticError as e:
                print(e)
                traceback.print_exc()
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
        utility_seven_lst.append(utility_seven / ITER)
        social_seven_lst.append(social_seven / ITER)
        asp_utility_seven_lst.append(asp_utility_seven / ITER)
        vm_seven_lst.append(vm_seven / ITER)
    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.plot(num, utility_proposed_lst, marker='o', markerfacecolor='none',
             label='Proposed Scheme', linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, utility_zero_lst, marker='^', markerfacecolor='none', label='No IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, utility_five_lst, marker='s', markerfacecolor='none', label='5% IPS VM',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, utility_seven_lst, marker='p', markerfacecolor='none', label='7% IPS VM',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=LABEL_FONT_SIZE)
    plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig('./image/device_number/5GDDoS_Game_MPO_device_step.jpg')
    plt.savefig('./image/device_number/5GDDoS_Game_MPO_device_step.pdf')
    plt.savefig('./image/device_number/5GDDoS_Game_MPO_device_step.eps')
    plt.close()

    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.plot(num, social_proposed_lst, marker='o', markerfacecolor='none', label='Proposed Scheme',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, social_zero_lst, marker='^', markerfacecolor='none', label='No IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, social_five_lst, marker='s', markerfacecolor='none', label='5% IPS VM',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, social_seven_lst, marker='p', markerfacecolor='none', label='7% IPS VM',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=LABEL_FONT_SIZE)
    plt.ylabel(r'$\bf{Social\ Welfare}$', fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig('./image/device_number/5GDDoS_Game_social_device_step.jpg')
    plt.savefig('./image/device_number/5GDDoS_Game_social_device_step.pdf')
    plt.savefig('./image/device_number/5GDDoS_Game_social_device_step.eps')
    plt.close()

    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.plot(num, asp_utility_proposed_lst, marker='o', markerfacecolor='none',
             label='Proposed Scheme', linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, asp_utility_zero_lst, marker='^', markerfacecolor='none',
             label='No IPS', linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, asp_utility_five_lst, marker='s', markerfacecolor='none',
             label='5% IPS VM', linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, asp_utility_seven_lst, marker='p', markerfacecolor='none',
             label='7% IPS VM', linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=LABEL_FONT_SIZE)
    plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig('./image/device_number/5GDDoS_Game_asp_device_step.jpg')
    plt.savefig('./image/device_number/5GDDoS_Game_asp_device_step.pdf')
    plt.savefig('./image/device_number/5GDDoS_Game_asp_device_step.eps')
    plt.close()

    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.plot(num, vm_proposed_lst, marker='o', markerfacecolor='none', label='Proposed Scheme',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, vm_zero_lst, marker='^', markerfacecolor='none', label='No IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, vm_five_lst, marker='s', markerfacecolor='none', label='5% IPS VM',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(num, vm_seven_lst, marker='p', markerfacecolor='none', label='7% IPS VM',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
    plt.xlabel(r'$\bf{Device\ Number}$', fontsize=LABEL_FONT_SIZE)
    plt.ylabel(r'$\bf{Purchased\ VM}$', fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig('./image/device_number/5GDDoS_Game_total_vm_device_step.jpg')
    plt.savefig('./image/device_number/5GDDoS_Game_total_vm_device_step.pdf')
    plt.savefig('./image/device_number/5GDDoS_Game_total_vm_device_step.eps')
    plt.close()
