import math
from random import randint
from const import *
from asp import ASP
import matplotlib.pyplot as plt

class MPO():
    def __init__(self):
        self.price_per_vm = None
        self.asp_lst = []
        self.num_of_asp = randint(MPO_NUM_OF_ASP_LOWER, MPO_NUM_OF_ASP_UPPER)
        self.set_asp()
        self.bd = []
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
        for asp in self.asp_lst:
            asp.set_boundary()
            if  asp.rbound > 0 and asp.rbound < 7000:
                self.bd.append(asp.rbound)
            if  asp.mbound > 0 and asp.mbound < 7000:
                self.bd.append(asp.mbound)

        return
    def optimize_phi(self):
        phi = 700
        step = 7
        pr = []
        ut = []
        bound = []
        num = []
        for _ in range(1000):
            self.set_price_per_vm(phi)
            for asp in self.asp_lst:
                asp.optimize_zv()
            vm_prior = self.total_vm()
            # print(vm_prior)
            # self.set_price_per_vm(phi + step)
            # for asp in self.asp_lst:
            #     asp.optimize_zv()
            # vm_after = self.total_vm()
            pr.append(phi)
            ut.append(phi * vm_prior - MPO_cost(vm_prior))
            num.append(vm_prior)
            phi += step
            # print(vm_after)
            # if ((vm_prior * phi) - (vm_after * (phi + step))) <= 0:
            #     print(phi)
            #     print(((vm_prior * phi) - (vm_after * (phi + step))))
            #     print('break')
            #     break
        #self.setbd()
        self.set_bd()

        plt.figure(figsize=(20, 16))
        plt.plot(pr, ut, marker='.', linestyle='-.')
        plt.vlines(self.bd, ymin=0, ymax=max(ut), linestyle='-', color ='red')
        plt.savefig('./utility.jpg')
        plt.close()

        plt.figure(figsize=(20, 16))
        plt.plot(pr, num, marker='.', linestyle='-.')
        plt.vlines(self.bd, ymin=0, ymax=max(num), linestyle='-', color ='red')
        plt.savefig('./vm_number.jpg')
        plt.close()
