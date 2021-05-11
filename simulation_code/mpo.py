import math
from random import randint, uniform
from const import *
from asp import ASP
import matplotlib.pyplot as plt


class MPO():
    def __init__(self):
        self.price_per_vm = None
        self.asp_lst = []
        self.num_of_asp = randint(MPO_NUM_OF_ASP_LOWER, MPO_NUM_OF_ASP_UPPER)
        self.num_of_vm = uniform(MPO_NUM_OF_VM_LOWER, MPO_NUM_OF_VM_UPPER)
        self.set_asp()
        self.set_bd()
        self.get_queue_bound()

    def set_asp(self):
        for i in range(self.num_of_asp):
            self.asp_lst.append(ASP())

    def set_price_per_vm(self, price):
        self.price_per_vm = price
        for asp in self.asp_lst:
            asp.set_mpo_price(price)

    def total_vm(self):
        tot = 0
        for asp in self.asp_lst:
            tot += asp.z_v
        return tot

    def set_bd(self):
        self.bd = []
        for asp in self.asp_lst:
            asp.set_boundary()
            self.bd.append(asp.bound)
        self.bd.sort()
        return

    def get_queue_bound(self):
        self.qbd = []
        for asp in self.asp_lst:
            asp.set_boundary()
            self.qbd.append(asp.qbound)
        self.qbd.sort()
        return

    def set_and_check_required_vm(self, price):
        self.set_price_per_vm(price)
        for asp in self.asp_lst:
            asp.optimize_zv()
        return

    def plot_phi(self):
        self.find_optimize_phi()
        phi = 700
        step = 7
        pr = []
        ut = []
        bound = []
        num = []
        vm_prior = float('inf')
        for _ in range(1000):
            self.set_and_check_required_vm(phi)
            vm_after = self.total_vm()
            pr.append(phi)
            ut.append(phi * vm_after - MPO_cost(vm_after))
            num.append(vm_after)
            phi += step
            if vm_prior < vm_after:
                print('Total VM is not non-increasing')
            vm_prior = vm_after
        plt.figure(figsize=(20, 16), dpi=100)
        plt.plot(pr, ut, marker='.', linestyle='-.')
        plt.title('Utility of MPO')
        plt.xlabel('MPO Price')
        plt.ylabel('Utility')
        plt.vlines(self.bd, ymin=0, ymax=max(ut), linestyle='-', color='red', label='Boundary')
        plt.vlines(self.constraint_phi, ymin=0, ymax=max(ut), linestyle='-', color='darkorange', label='Price Constraint')
        plt.legend(loc="best")
        plt.savefig('./utility.jpg')
        plt.close()
        plt.figure(figsize=(20, 16), dpi=100)
        plt.plot(pr, num, marker='.', linestyle='-.')
        plt.vlines(self.bd, ymin=0, ymax=max(num), linestyle='-', color='red', label='Boundary')
        plt.hlines(self.num_of_vm, xmin=min(700, self.constraint_phi), xmax=7700, linestyle='-', color='black', label='VM Constraint')
        plt.vlines(self.constraint_phi, ymin=0, ymax=max(num), linestyle='-', color='darkorange', label='Price Constraint')
        plt.title('Total Purchased VM')
        plt.legend(loc="best")
        plt.xlabel('MPO Price')
        plt.ylabel('Purchased VM')
        plt.savefig('./vm_number.jpg')
        plt.close()

    def find_optimize_phi(self):
        vm_prior = float('inf')
        phi_prior = 0.01
        for bd in self.bd:
            self.set_and_check_required_vm(bd)
            vm_after = self.total_vm()
            phi_after = bd
            if vm_after < self.num_of_vm and vm_prior > self.num_of_vm:
                break
            vm_prior = vm_after
            phi_prior = phi_after
        if phi_prior > max(self.qbd):
            self.constraint_phi = phi_prior
        else:
            upper = phi_after
            lower = phi_prior
            mid = (upper + lower) / 2
            self.set_and_check_required_vm(lower)
            vm_num = self.total_vm()
            print(self.num_of_vm)
            while abs(vm_num - self.num_of_vm) > 0.001 and abs(upper - lower) > 1E-8:
                mid = (upper + lower) / 2
                self.set_and_check_required_vm(mid)
                vm_num = self.total_vm()
                print(vm_num)
                print(f'upper : {upper}, lower : {lower}')
                if vm_num > self.num_of_vm:
                    lower = mid
                else:
                    upper = mid
            print(f"Constraint price : {mid}")
            self.set_and_check_required_vm(mid)
            vm = self.total_vm()
            print(vm)
            self.constraint_phi = mid
