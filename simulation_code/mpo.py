import matplotlib.pyplot as plt
from random import uniform
from const import *
from asp import *
from convex_solver import convex_solve


class MPO():
    def __init__(self, ratio, num, mpo_type, asp_num, eff, high_num=0, low_num=0):
        self.price_per_vm = None
        self.type = mpo_type
        self.high_num = high_num
        self.low_num = low_num
        self.asp_lst = []
        self.asp_case_lst = []
        self.asp_response = []
        self.num_of_asp = asp_num
        self.eff = eff
        self.num_of_vm = uniform(MPO_NUM_OF_VM_LOWER, MPO_NUM_OF_VM_UPPER)
        self.ratio = ratio
        self.num = num
        self.set_asp()
        self.set_bd()
        self.set_change_point()
        self.set_queue_bound()
        self.bound = self.bd + self.qbd + self.cp
        self.bound.sort()
        self.find_constraint_phi()
        self.bound = [b for b in self.bound if b > self.constraint_phi]
        self.bound.append(self.constraint_phi)
        self.bound.sort()
        self.check_asp_response()
    """
    set_asp : initial asp
    """

    def set_asp(self):
        if self.type == load_type.RATIO:
            for _ in range(self.high_num):
                asp = ASP(self.ratio, self.num, load_type.HIGH, self.eff)
                self.asp_lst.append(asp)
            for _ in range(self.low_num):
                asp = ASP(self.ratio, self.num, load_type.LOW, self.eff)
                self.asp_lst.append(asp)
        else:
            for _ in range(self.num_of_asp):
                asp = ASP(self.ratio, self.num, self.type, self.eff)
                self.asp_lst.append(asp)
    """
    set_price_per_vm : initial mpo price
    """

    def set_price_per_vm(self, price):
        self.price_per_vm = price
        for asp in self.asp_lst:
            asp.set_mpo_price(price)
    """
    total_vm : calculate and return total vm
    """

    def total_vm(self):
        tot = 0
        for asp in self.asp_lst:
            tot += asp.z_v
        return tot
    """
    set_bd : add boundary points to the list
    """

    def set_bd(self):
        self.bd = []
        for asp in self.asp_lst:
            self.bd.append(asp.bound)
        self.bd.sort()
        return
    """
    set_queue_bound : add queuing boundary points to the list
    """

    def set_queue_bound(self):
        self.qbd = []
        for asp in self.asp_lst:
            if asp.qbound is not None:
                self.qbd.append(asp.qbound)
        self.qbd.sort()
        return

    def set_change_point(self):
        self.cp = []
        for asp in self.asp_lst:
            if asp.change_point is not None:
                self.cp.append(asp.change_point)
        self.cp.sort()
        return
    """
    set_and_check_required_vm : set price and optimize the asp
    """

    def set_and_check_required_vm(self, price):
        self.set_price_per_vm(price)
        for asp in self.asp_lst:
            asp.optimize_zv()
            # if asp.z_h != 0 and isinstance(price, int):
            #     print(f"price : {price}, pruchased_vm : {asp.z_v}, IPS VM : {asp.z_h}, Intercepted : {ASP_H(asp.z_h, asp.malicious_arrival_rate, asp.malicious_ratio)}, Mal request : {asp.malicious_arrival_rate}, Utility : {asp.utility}")
        return
    """
    set_and_check_required_vm_with_chi : set price and IPS ratio and optimize the asp
    """

    def set_and_check_required_vm_with_chi(self, price, chi):
        self.set_price_per_vm(price)
        for asp in self.asp_lst:
            asp.set_zv_zh(chi)
        return

    def check_asp_response(self):
        for i in range(len(self.bound) - 1):
            mid = (self.bound[i] + self.bound[i + 1]) / 2.0
            res = []
            for asp in self.asp_lst:
                res.append(asp.res(mid))
            self.asp_response.append(res)
    """
    optimize_phi : find the optimize phi
    """

    def optimize_phi(self):
        max, max_phi = convex_solve(self)
        self.set_and_check_required_vm(max_phi)
        asp_util = 0
        asp_vm = 0
        for asp in self.asp_lst:
            asp_util += asp.utility
            asp_vm += asp.z_v
        return max, max_phi, asp_util + max, asp_util, asp_vm
    """
    optimize_phi_with_step : find the optimize phi with different step
    """

    def optimize_phi_with_step(self, step):
        # self.find_constraint_phi()
        phi = (self.constraint_phi)
        max = 0
        max_phi = 0
        iter = int(25000 / step)
        for _ in range(iter):
            self.set_and_check_required_vm(phi)
            vm_num = self.total_vm()
            uti = phi * vm_num - MPO_cost(vm_num)
            if uti > max:
                max = uti
                max_phi = phi
            phi += step
            if uti == 0:
                break
        self.set_and_check_required_vm(max_phi)
        asp_util = 0
        asp_vm = 0
        for asp in self.asp_lst:
            asp_util += asp.utility
            asp_vm += asp.z_v
        return max, max_phi, asp_util + max, asp_util, asp_vm
    """
    optimize_phi_with_chi : calculate the overall utility with input (MPO price, IPS ratio)
    """

    def optimize_phi_with_chi(self, chi, phi):
        self.set_and_check_required_vm_with_chi(phi, chi)
        vm = self.total_vm()
        util = phi * vm - MPO_cost(vm)
        asp_util = 0
        asp_vm = 0
        for asp in self.asp_lst:
            asp_util += asp.utility
            asp_vm += asp.z_v
        return util, util + asp_util, asp_util, asp_vm

    def optimize_phi_with_step_chi(self, step, chi):
        self.find_constraint_phi()
        phi = self.constraint_phi
        max = 0
        max_phi = 0
        iter = int(25000 / step)
        for _ in range(iter):
            self.set_and_check_required_vm_with_chi(phi, chi)
            vm_num = self.total_vm()
            uti = phi * vm_num - MPO_cost(vm_num)
            if uti > max:
                max = uti
                max_phi = phi
            phi += step
            if uti == 0:
                break
        self.set_and_check_required_vm_with_chi(max_phi, chi)
        asp_util = 0
        asp_vm = 0
        for asp in self.asp_lst:
            asp_util += asp.utility
            asp_vm += asp.z_v
        return max, asp_util + max, asp_util, asp_vm
    """
    optimize_phi_with_price : calculate the overall utility with input (MPO price)
    """

    def optimize_phi_with_price(self, price):
        self.set_and_check_required_vm(price)
        vm = self.total_vm()
        util = price * vm - MPO_cost(vm)
        asp_util = 0
        for asp in self.asp_lst:
            asp_util += asp.utility
        return util, util + asp_util, asp_util
    """
    plot the MPO utility
    """

    def plot_MPO_utility(self, plot_range):
        self.find_constraint_phi()
        phi = 1
        step = 1
        pr = []
        ut = []
        num = []
        asp_ut = []
        vm_prior = float('inf')
        for _ in range(plot_range):
            self.set_and_check_required_vm(phi)
            vm_after = self.total_vm()
            pr.append(phi)
            ut.append(phi * vm_after - MPO_cost(vm_after))
            num.append(vm_after)
            asp_u = 0
            for asp in self.asp_lst:
                asp_u += asp.utility
            asp_ut.append(asp_u)
            phi += step
            if vm_prior < vm_after:
                print(
                    f'Total VM is not non-increasing {vm_prior} -> {vm_after}')
            vm_prior = vm_after

        plt.figure(figsize=FIG_SIZE, dpi=DPI)
        plt.plot(pr, ut, marker='.', linestyle='-',
                 label='Utility', linewidth=LINE_WIDTH)
        plt.xlabel(r'$\bf{MPO\ Price}$', fontsize=LABEL_FONT_SIZE)
        plt.ylabel(r'$\bf{MPO\ Utility}$', fontsize=LABEL_FONT_SIZE)
        plt.vlines(self.bd + self.qbd + self.cp, ymin=min(ut), ymax=max(ut),
                   linestyle='dashed', color='gray', label='Boundary', linewidth=LINE_WIDTH)
        plt.vlines(self.constraint_phi, ymin=min(ut), ymax=max(ut), linestyle=(
            0, (3, 5, 1, 5, 1, 5)), color='red', label='Constraint', linewidth=LINE_WIDTH)
        plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
        plt.xticks(fontsize=TICKS_FONT_SIZE)
        plt.yticks(fontsize=TICKS_FONT_SIZE)
        plt.savefig('./image/optimize_mpo/5GDDoS_Game_plot_MPO_utility.pdf')
        if JPG_ENABLE:
            plt.savefig('./image/optimize_mpo/5GDDoS_Game_plot_MPO_utility.jpg')
        plt.savefig('./image/optimize_mpo/5GDDoS_Game_plot_MPO_utility.eps')
        plt.close()

        plt.figure(figsize=FIG_SIZE, dpi=DPI)
        plt.plot(pr, num, marker='.', linestyle='-',
                 label='Purchased VM', linewidth=LINE_WIDTH)
        plt.vlines(self.bd + self.qbd + self.cp, ymin=min(num), ymax=max(num),
                   linestyle='dashed', color='gray', label='Boundary', linewidth=LINE_WIDTH)
        plt.vlines(self.constraint_phi, ymin=min(num), ymax=max(num), linestyle=(
            0, (3, 5, 1, 5, 1, 5)), color='red', label='Constraint', linewidth=LINE_WIDTH)
        plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
        plt.xlabel(r'$\bf{MPO\ Price}$', fontsize=LABEL_FONT_SIZE)
        plt.ylabel(r'$\bf{Total\ Purchased\ VM}$', fontsize=LABEL_FONT_SIZE)
        plt.xticks(fontsize=TICKS_FONT_SIZE)
        plt.yticks(fontsize=TICKS_FONT_SIZE)
        plt.savefig(
            './image/optimize_mpo/5GDDoS_Game_plot_purchased_vm_number.pdf')
        if JPG_ENABLE:
            plt.savefig(
                './image/optimize_mpo/5GDDoS_Game_plot_purchased_vm_number.jpg')
        plt.savefig(
            './image/optimize_mpo/5GDDoS_Game_plot_purchased_vm_number.eps')
        plt.close()

        plt.figure(figsize=FIG_SIZE, dpi=DPI)
        plt.plot(pr, asp_ut, marker='.', linestyle='-',
                 label='Purchased VM', linewidth=LINE_WIDTH)
        plt.vlines(self.bd + self.qbd + self.cp, ymin=min(asp_ut), ymax=max(asp_ut),
                   linestyle='dashed', color='gray', label='Boundary', linewidth=LINE_WIDTH)
        plt.vlines(self.constraint_phi, ymin=min(asp_ut), ymax=max(asp_ut), linestyle=(
            0, (3, 5, 1, 5, 1, 5)), color='red', label='Constraint', linewidth=LINE_WIDTH)
        plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
        plt.xlabel(r'$\bf{MPO\ Price}$', fontsize=LABEL_FONT_SIZE)
        plt.ylabel(r'$\bf{ASP\ Utility}$', fontsize=LABEL_FONT_SIZE)
        plt.xticks(fontsize=TICKS_FONT_SIZE)
        plt.yticks(fontsize=TICKS_FONT_SIZE)
        plt.savefig('./image/optimize_mpo/5GDDoS_Game_plot_asp_utility.pdf')
        if JPG_ENABLE:
            plt.savefig('./image/optimize_mpo/5GDDoS_Game_plot_asp_utility.jpg')
        plt.savefig('./image/optimize_mpo/5GDDoS_Game_plot_asp_utility.eps')
        plt.close()

    """
    find_constraint_phi : find the lowest price that satisfy the total vm constraint
    """

    def find_constraint_phi(self):
        vm_prior = float('inf')
        phi_prior = 0.00000000001
        for bd in self.bd:
            self.set_and_check_required_vm(bd)
            vm_after = self.total_vm()
            phi_after = bd
            if vm_after < self.num_of_vm and vm_prior > self.num_of_vm:
                break
            vm_prior = vm_after
            phi_prior = phi_after
        if phi_prior > min(self.bd):
            self.constraint_phi = phi_after
        else:
            upper = phi_after
            lower = phi_prior
            mid = (upper + lower) / 2
            self.set_and_check_required_vm(lower)
            vm_num = self.total_vm()
            while abs(vm_num - self.num_of_vm) > 0.001 and abs(upper - lower) > 1E-8:
                mid = (upper + lower) / 2
                self.set_and_check_required_vm(mid)
                vm_num = self.total_vm()
                if vm_num > self.num_of_vm:
                    lower = mid
                else:
                    upper = mid
            self.set_and_check_required_vm(mid)
            vm = self.total_vm()
            self.constraint_phi = mid
