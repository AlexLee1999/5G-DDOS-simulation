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

    def set_and_check_required_vm(self, price):
        self.set_price_per_vm(price)
        for asp in self.asp_lst:
            asp.optimize_zv()
        return

    def plot_phi(self):
        phi = 700
        step = 7
        pr = []
        ut = []
        bound = []
        num = []
        for _ in range(1000):
            self.set_and_check_required_vm(phi)
            vm_prior = self.total_vm()
            pr.append(phi)
            ut.append(phi * vm_prior - MPO_cost(vm_prior))
            num.append(vm_prior)
            phi += step
        plt.figure(figsize=(20, 16))
        plt.plot(pr, ut, marker='.', linestyle='-.')
        plt.title('Utility of MPO')
        plt.xlabel('MPO Price')
        plt.ylabel('Utility')
        plt.vlines(self.bd, ymin=0, ymax=max(ut), linestyle='-', color ='red')
        plt.savefig('./utility.jpg')
        plt.close()
        plt.figure(figsize=(20, 16))
        plt.plot(pr, num, marker='.', linestyle='-.')
        plt.vlines(self.bd, ymin=0, ymax=max(num), linestyle='-', color ='red')
        plt.title('Total Purchased VM')
        plt.xlabel('MPO Price')
        plt.ylabel('Purchased VM')
        plt.savefig('./vm_number.jpg')
        plt.close()

    def find_optimize_phi(self):
        print(self.num_of_vm)
        vm_prior = float('inf')
        phi_prior = 0
        for bd in self.bd:
            self.set_and_check_required_vm(bd)
            vm_after = self.total_vm()
            phi_after = bd
            if vm_after < self.num_of_vm and vm_prior > self.num_of_vm:
                break
            vm_prior = vm_after
            phi_prior = phi_after
        print(vm_prior)
        print(vm_after)
        upper = phi_after
        lower = phi_prior
        print(upper)
        print(lower)
        mid = (upper + lower) / 2
        self.set_and_check_required_vm(lower)
        vm_num = self.total_vm()
        print(vm_num)
        while abs(vm_num - self.num_of_vm) > 0.001 and abs(upper - lower) > 1E-8:
            print((abs(vm_num - self.num_of_vm) > 0.001, abs(upper - lower) > 1E-8))
            mid = (upper + lower) / 2
            self.set_and_check_required_vm(mid)
            vm_num = self.total_vm()
            if vm_num > self.num_of_vm:
                lower = mid
            else:
                upper = mid
        print((abs(vm_num - self.num_of_vm) > 0.001, abs(upper - lower) > 1E-8))
        print(mid)
        self.set_and_check_required_vm(mid)
        print(self.total_vm())
