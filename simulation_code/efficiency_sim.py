from fig import *
import traceback
from tqdm import tqdm
import matplotlib.pyplot as plt
from const import *
from mpo import *
from convex_solver import *


def plot_utility_efficiency_cvx():
    print("efficiency")
    eff = EFF_LST
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
    utility_ten_lst = []
    social_ten_lst = []
    asp_utility_ten_lst = []
    vm_ten_lst = []
    utility_ips_lst = []
    social_ips_lst = []
    asp_utility_ips_lst = []
    vm_ips_lst = []
    utility_eff_lst = []
    social_eff_lst = []
    asp_utility_eff_lst = []
    vm_eff_lst = []
    for ef in eff:
        print(ef, flush=True)
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
        utility_ten = 0
        social_ten = 0
        asp_utility_ten = 0
        vm_ten = 0
        utility_ips = 0
        social_ips = 0
        asp_utility_ips = 0
        vm_ips = 0
        utility_eff = 0
        social_eff = 0
        asp_utility_eff = 0
        vm_eff = 0
        i = 0
        pbar = tqdm(total=ITER)
        while i < ITER:
            try:
                mpo = MPO(DEFAULT_DEVICE_RATIO, DEFAULT_DEVICE_NUM,
                          load_type.AVERAGE, MPO_NUM_OF_ASP, ef)
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
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(
                    0.1, max_phi)
                utility_ten += util
                social_ten += social
                asp_utility_ten += asp_u
                vm_ten += vm_num
                ips = IPS_PROP_COFF * DEFAULT_DEVICE_RATIO
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(
                    ips, max_phi)
                utility_ips += util
                social_ips += social
                asp_utility_ips += asp_u
                vm_ips += vm_num
                eff_ips = ef * EFF_IPS_PROP_COFF
                util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(
                    eff_ips, max_phi)
                utility_eff += util
                social_eff += social
                asp_utility_eff += asp_u
                vm_eff += vm_num
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
        utility_ten_lst.append(utility_ten / ITER)
        social_ten_lst.append(social_ten / ITER)
        asp_utility_ten_lst.append(asp_utility_ten / ITER)
        vm_ten_lst.append(vm_ten / ITER)
        utility_ips_lst.append(utility_ips / ITER)
        social_ips_lst.append(social_ips / ITER)
        asp_utility_ips_lst.append(asp_utility_ips / ITER)
        vm_ips_lst.append(vm_ips / ITER)
        utility_eff_lst.append(utility_eff / ITER)
        social_eff_lst.append(social_eff / ITER)
        asp_utility_eff_lst.append(asp_utility_eff / ITER)
        vm_eff_lst.append(vm_eff / ITER)
    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.plot(eff, utility_proposed_lst, marker='o', markerfacecolor='none',
             label='Proposed', linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, utility_zero_lst, marker='^', markerfacecolor='none', label='No IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, utility_five_lst, marker='s', markerfacecolor='none', label='5% IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, utility_seven_lst, marker='>', markerfacecolor='none', label='7% IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, utility_ten_lst, marker='p', markerfacecolor='none', label='10% IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, utility_ips_lst, marker='*', markerfacecolor='none', label='Prop Malicious ratio',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, utility_eff_lst, marker='D', markerfacecolor='none', label='Prop IPS efficiency',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
    x_title = r'$\bf{IPS\ EFFICIENCY}$'
    y_title = r'$\bf{MPO\ Utility}$'
    plt.xlabel(x_title, fontsize=LABEL_FONT_SIZE)
    plt.ylabel(y_title, fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig(
            './image/efficiency/5GDDoS_Game_MPO_efficiency_cvx.jpg')
    plt.savefig(
        './image/efficiency/5GDDoS_Game_MPO_efficiency_cvx.pdf')
    plt.savefig(
        './image/efficiency/5GDDoS_Game_MPO_efficiency_cvx.eps')
    plt.close()

    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.plot(eff, social_proposed_lst, marker='o', markerfacecolor='none', label='Proposed',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, social_zero_lst, marker='^', markerfacecolor='none', label='No IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, social_five_lst, marker='s', markerfacecolor='none', label='5% IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, social_seven_lst, marker='>', markerfacecolor='none', label='7% IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, social_ten_lst, marker='p', markerfacecolor='none', label='10% IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, social_ips_lst, marker='*', markerfacecolor='none', label='Prop Malicious ratio',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, social_eff_lst, marker='D', markerfacecolor='none', label='Prop IPS efficiency',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
    x_title = r'$\bf{IPS\ EFFICIENCY}$'
    y_title = r'$\bf{Social\ Welfare}$'
    plt.xlabel(x_title, fontsize=LABEL_FONT_SIZE)
    plt.ylabel(y_title, fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig(
            './image/efficiency/5GDDoS_Game_social_efficiency_cvx.jpg')
    plt.savefig(
        './image/efficiency/5GDDoS_Game_social_efficiency_cvx.pdf')
    plt.savefig(
        './image/efficiency/5GDDoS_Game_social_efficiency_cvx.eps')
    plt.close()

    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.plot(eff, asp_utility_proposed_lst, marker='o', markerfacecolor='none',
             label='Proposed', linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, asp_utility_zero_lst, marker='^', markerfacecolor='none',
             label='No IPS', linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, asp_utility_five_lst, marker='s', markerfacecolor='none',
             label='5% IPS', linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, asp_utility_seven_lst, marker='>', markerfacecolor='none', label='7% IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, asp_utility_ten_lst, marker='p', markerfacecolor='none',
             label='10% IPS', linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, asp_utility_ips_lst, marker='*', markerfacecolor='none', label='Prop Malicious ratio',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, asp_utility_eff_lst, marker='D', markerfacecolor='none', label='Prop IPS efficiency',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
    x_title = r'$\bf{IPS\ EFFICIENCY}$'
    y_title = r'$\bf{ASP\ Utility}$'
    plt.xlabel(x_title, fontsize=LABEL_FONT_SIZE)
    plt.ylabel(y_title, fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig(
            './image/efficiency/5GDDoS_Game_asp_efficiency_cvx.jpg')
    plt.savefig(
        './image/efficiency/5GDDoS_Game_asp_efficiency_cvx.pdf')
    plt.savefig(
        './image/efficiency/5GDDoS_Game_asp_efficiency_cvx.eps')
    plt.close()

    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    plt.plot(eff, vm_proposed_lst, marker='o', markerfacecolor='none', label='Proposed',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, vm_zero_lst, marker='^', markerfacecolor='none', label='No IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, vm_five_lst, marker='s', markerfacecolor='none', label='5% IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, vm_seven_lst, marker='>', markerfacecolor='none', label='7% IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, vm_ten_lst, marker='p', markerfacecolor='none', label='10% IPS',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, vm_ips_lst, marker='*', markerfacecolor='none', label='Prop Malicious ratio',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.plot(eff, vm_eff_lst, marker='D', markerfacecolor='none', label='Prop IPS efficiency',
             linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
    x_title = r'$\bf{IPS\ EFFICIENCY}$'
    y_title = r'$\bf{Purchased\ VM}$'
    plt.xlabel(x_title, fontsize=LABEL_FONT_SIZE)
    plt.ylabel(y_title, fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig(
            './image/efficiency/5GDDoS_Game_total_vm_efficiency_cvx.jpg')
    plt.savefig(
        './image/efficiency/5GDDoS_Game_total_vm_efficiency_cvx.pdf')
    plt.savefig(
        './image/efficiency/5GDDoS_Game_total_vm_efficiency_cvx.eps')
    plt.close()
