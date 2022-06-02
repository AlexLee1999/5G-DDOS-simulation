from fig import *
import traceback
from tqdm import tqdm
import matplotlib.pyplot as plt
from const import *
from mpo import *
from convex_solver import *



def plot_utility_device_num_low_new_step():
    print("device low new step")
    marker_dic = dict()
    marker_dic["Proposed Scheme"] = 'o'
    marker_dic["No IPS"] = '^'
    marker_dic["5% IPS VM"] = 's'
    marker_dic["7% IPS VM"] = 'p'
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
                          load_type.LOW, MPO_NUM_OF_ASP)
                util, max_phi, social, asp_u, vm_num = mpo.optimize_phi_with_step(
                    1)
                utility_proposed += util
                social_proposed += social
                asp_utility_proposed += asp_u
                vm_proposed += vm_num
                # util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0, max_phi)
                util, social, asp_u, vm_num = mpo.optimize_phi_with_step_chi(
                    STEP, 0)
                utility_zero += util
                social_zero += social
                asp_utility_zero += asp_u
                vm_zero += vm_num
                # util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0.05, max_phi)
                util, social, asp_u, vm_num = mpo.optimize_phi_with_step_chi(
                    STEP, 0.05)
                utility_five += util
                social_five += social
                asp_utility_five += asp_u
                vm_five += vm_num
                # util, social, asp_u, vm_num = mpo.optimize_phi_with_chi(0.07, max_phi)
                util, social, asp_u, vm_num = mpo.optimize_phi_with_step_chi(
                    STEP, 0.07)
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
        utility_proposed_lst.append(utility_proposed / utility_zero)
        social_proposed_lst.append(social_proposed / social_zero)
        asp_utility_proposed_lst.append(
            asp_utility_proposed / asp_utility_zero)
        vm_proposed_lst.append(vm_proposed / vm_zero)
        utility_zero_lst.append(utility_zero / utility_zero)
        social_zero_lst.append(social_zero / social_zero)
        asp_utility_zero_lst.append(asp_utility_zero / asp_utility_zero)
        vm_zero_lst.append(vm_zero / vm_zero)
        utility_five_lst.append(utility_five / utility_zero)
        social_five_lst.append(social_five / social_zero)
        asp_utility_five_lst.append(asp_utility_five / asp_utility_zero)
        vm_five_lst.append(vm_five / vm_zero)
        utility_seven_lst.append(utility_seven / utility_zero)
        social_seven_lst.append(social_seven / social_zero)
        asp_utility_seven_lst.append(asp_utility_seven / asp_utility_zero)
        vm_seven_lst.append(vm_seven / vm_zero)
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
    x_title = r'$\bf{Device\ Number}$'
    y_title = r'$\bf{MPO\ Utility}$'
    plt.xlabel(x_title, fontsize=LABEL_FONT_SIZE)
    plt.ylabel(y_title, fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig(
            './image/device_number_low_new/5GDDoS_Game_MPO_device_low_new_step.jpg')
    plt.savefig(
        './image/device_number_low_new/5GDDoS_Game_MPO_device_low_new_step.pdf')
    plt.savefig(
        './image/device_number_low_new/5GDDoS_Game_MPO_device_low_new_step.eps')
    data_dic = dict()
    data_dic["Proposed Scheme"] = utility_proposed_lst
    data_dic["No IPS"] = utility_zero_lst
    data_dic["5% IPS VM"] = utility_five_lst
    data_dic["7% IPS VM"] = utility_seven_lst
    fig_name = "device_number_low_new/5GDDoS_Game_MPO_device_low_new_step"
    fig = Fig(num, data_dic, x_title, y_title, fig_name, marker_dic)
    write_fig(fig, fig_name)
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
    x_title = r'$\bf{Device\ Number}$'
    y_title = r'$\bf{Social\ Welfare}$'
    plt.xlabel(x_title, fontsize=LABEL_FONT_SIZE)
    plt.ylabel(y_title, fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig(
            './image/device_number_low_new/5GDDoS_Game_social_device_low_new_step.jpg')
    plt.savefig(
        './image/device_number_low_new/5GDDoS_Game_social_device_low_new_step.pdf')
    plt.savefig(
        './image/device_number_low_new/5GDDoS_Game_social_device_low_new_step.eps')
    data_dic = dict()
    data_dic["Proposed Scheme"] = social_proposed_lst
    data_dic["No IPS"] = social_zero_lst
    data_dic["5% IPS VM"] = social_five_lst
    data_dic["7% IPS VM"] = social_seven_lst
    fig_name = "device_number_low_new/5GDDoS_Game_social_device_low_new_step"
    fig = Fig(num, data_dic, x_title, y_title, fig_name, marker_dic)
    write_fig(fig, fig_name)
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
    x_title = r'$\bf{Device\ Number}$'
    y_title = r'$\bf{ASP\ Utility}$'
    plt.xlabel(x_title, fontsize=LABEL_FONT_SIZE)
    plt.ylabel(y_title, fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig(
            './image/device_number_low_new/5GDDoS_Game_asp_device_low_new_step.jpg')
    plt.savefig(
        './image/device_number_low_new/5GDDoS_Game_asp_device_low_new_step.pdf')
    plt.savefig(
        './image/device_number_low_new/5GDDoS_Game_asp_device_low_new_step.eps')
    data_dic = dict()
    data_dic["Proposed Scheme"] = asp_utility_proposed_lst
    data_dic["No IPS"] = asp_utility_zero_lst
    data_dic["5% IPS VM"] = asp_utility_five_lst
    data_dic["7% IPS VM"] = asp_utility_seven_lst
    fig_name = "device_number_low_new/5GDDoS_Game_asp_device_low_new_step"
    fig = Fig(num, data_dic, x_title, y_title, fig_name, marker_dic)
    write_fig(fig, fig_name)
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
    x_title = r'$\bf{Device\ Number}$'
    y_title = r'$\bf{Purchased\ VM}$'
    plt.xlabel(x_title, fontsize=LABEL_FONT_SIZE)
    plt.ylabel(y_title, fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    if JPG_ENABLE:
        plt.savefig(
            './image/device_number_low_new/5GDDoS_Game_total_vm_device_low_new_step.jpg')
    plt.savefig(
        './image/device_number_low_new/5GDDoS_Game_total_vm_device_low_new_step.pdf')
    plt.savefig(
        './image/device_number_low_new/5GDDoS_Game_total_vm_device_low_new_step.eps')
    data_dic = dict()
    data_dic["Proposed Scheme"] = vm_proposed_lst
    data_dic["No IPS"] = vm_zero_lst
    data_dic["5% IPS VM"] = vm_five_lst
    data_dic["7% IPS VM"] = vm_seven_lst
    fig_name = "device_number_low_new/5GDDoS_Game_total_vm_device_low_new_step"
    fig = Fig(num, data_dic, x_title, y_title, fig_name, marker_dic)
    write_fig(fig, fig_name)
    plt.close()
