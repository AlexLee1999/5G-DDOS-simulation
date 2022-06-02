import matplotlib.pyplot as plt
from math import sqrt
from random import uniform
from const import *
from device import *


"""
bandwidth : total bandwidth of ASP_
frequency : CPU frequency of a VM
"""


class ASP():
    def __init__(self, ratio, num, ASP_type, eff):
        self.type = ASP_type
        self.bandwidth = ASP_BANDWIDTH
        self.frequency = MPO_CPU_FREQUENCY
        self.device_list = []
        self.mal_device_list = []
        self.malicious_ratio = ratio
        self.eff = eff
        self.num_of_malicious_users = int(num * self.malicious_ratio)
        self.num_of_normal_users = num - self.num_of_malicious_users
        self.set_users()
        self.set_service_rate()
        self.set_arrival_rate()
        self.total_pay()
        self.mpo_price = None
        self.chi = uniform(ASP_CHI_LOWER, ASP_CHI_UPPER)
        self.gamma = uniform(ASP_GAMMA_LOWER, ASP_GAMMA_UPPER)
        self.phi = 0
        if self.service_rate < GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff):
            self.sqrt_coff_1 = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (
                (1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff))))
            self.sqrt_coff_2 = sqrt(
                self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.service_rate))
            self.coff_1 = self.arrival_rate / \
                ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff))
            self.coff_2 = self.normal_arrival_rate / self.service_rate + \
                self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)
        else:
            self.sqrt_coff_3 = sqrt(
                self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.service_rate))
            self.coff_3 = self.arrival_rate / self.service_rate
        self.queue_coff = (self.gamma + self.arrival_rate) / self.service_rate
        self.set_boundary()

    def __str__(self):
        return f'''
            arrival rate          : {self.arrival_rate}
            malcious arrival rate : {self.malicious_arrival_rate}
            normal arrival rate   : {self.normal_arrival_rate}
            purchased vm          : {self.z_v}
            IPS vm                : {self.z_h}
            Blocked mal request   : {ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff)}
            Service Rate          : {self.service_rate}
            Case                  : {self.case}
            Gamma                 : {self.gamma}
            Xi                    : {self.chi}
            Queue                 : {(self.gamma + self.arrival_rate) / self.service_rate}
            Malicious request VM  : {(self.malicious_arrival_rate / (GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) * self.chi))}
            Change point          : {self.change_point}
        '''
    """
    set_users : initial users
    """

    def set_users(self):
        if self.type == load_type.AVERAGE:
            for _ in range(self.num_of_normal_users):
                self.device_list.append(Device(
                    self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))
            for _ in range(self.num_of_malicious_users):
                self.mal_device_list.append(Malicious_Device(
                    self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))
        elif self.type == load_type.HIGH:
            for _ in range(self.num_of_normal_users):
                self.device_list.append(Device_high_load(
                    self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))
            for _ in range(self.num_of_malicious_users):
                self.mal_device_list.append(Malicious_Device_high_load(
                    self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))
        elif self.type == load_type.LOW:
            for _ in range(self.num_of_normal_users):
                self.device_list.append(Device_low_load(
                    self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))
            for _ in range(self.num_of_malicious_users):
                self.mal_device_list.append(Malicious_Device_low_load(
                    self.bandwidth / (self.num_of_normal_users + self.num_of_malicious_users)))
    """
    total_pay : calculate the total payment from device
    """

    def total_pay(self):
        self.total_payment = 0
        for dev in self.device_list:
            self.total_payment += dev.price_per_task
    """
    set_service_rate : initial the service rate
    """

    def set_service_rate(self):
        tot_cpu_cycle = 0
        for dev in self.device_list:
            tot_cpu_cycle += dev.required_cpu_cycle
        for dev in self.mal_device_list:
            tot_cpu_cycle += dev.required_cpu_cycle
        self.service_rate = self.frequency / \
            (tot_cpu_cycle / (self.num_of_normal_users + self.num_of_malicious_users))
    """
    set_arrival_rate : initial the arrival rate
    """

    def set_arrival_rate(self):
        self.arrival_rate = 0
        self.malicious_arrival_rate = 0
        self.normal_arrival_rate = 0
        for dev in self.device_list:
            self.arrival_rate += dev.arrival_rate
            self.normal_arrival_rate += dev.arrival_rate
        for dev in self.mal_device_list:
            self.arrival_rate += dev.arrival_rate
            self.malicious_arrival_rate += dev.arrival_rate
    """
    set_mpo_price : get mpo price from mpo
    """

    def set_mpo_price(self, price):
        self.mpo_price = price
    """
    set_malicious_ratio : set malicious ratio of an ASP
    """

    def set_malicious_ratio(self, ratio):
        self.malicious_ratio = ratio
    """
    set_utility : calculate the utility
    """

    def set_utility(self):
        util = 0
        for dev in self.device_list:
            util += (dev.price_per_task *
                     self.uniform_cdf(self.process_time + dev.transmission_time_to_asp))
        self.utility = util - self.mpo_price * self.z_v
        return
    """
    time : calculate processing time with z_v and z_h
    """

    def time(self, z_v, z_h):
        t = 1 / ((z_v - z_h) * self.service_rate -
                 (self.arrival_rate - ASP_H(z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff)))
        return t

    def case2_time(self, z_v):
        if z_v > self.malicious_arrival_rate / (self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)):
            return 1 / ((z_v - self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)) * self.service_rate - (self.normal_arrival_rate))
        else:
            return 1 / ((1-self.chi)*z_v*self.service_rate-(self.arrival_rate-GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)*self.chi*z_v))

    def uniform_cdf(self, time):
        # if time > ASP_DEVICE_LATENCY_UPPER:
        #     return 0
        # elif time < ASP_DEVICE_LATENCY_LOWER:
        #     return 1
        # else:
        return (1 - ((time - ASP_DEVICE_LATENCY_LOWER) / (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)))
    """
    set_boundary : calculate the boundary
    """

    # def set_boundary(self):
    #     z_v = (self.arrival_rate + self.gamma) / self.service_rate
    #     z_h = self.chi * z_v
    #     util1 = 0
    #     util2 = 0
    #     util3 = 0
    #     for dev in self.device_list:
    #         util1 += (dev.price_per_task *
    #                   (self.uniform_cdf(dev.transmission_time_to_asp + self.time(z_v, z_h))))
    #         util2 += (dev.price_per_task *
    #                   (self.uniform_cdf(dev.transmission_time_to_asp + self.time(z_v, 0))))
    #         util3 += (dev.price_per_task * (self.uniform_cdf(dev.transmission_time_to_asp +
    #                   self.time(z_v, self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))))))
    #     if GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) > self.service_rate:  # case 2 & 4
    #         bound_case2 = util1 / z_v
    #         bound_case4 = util3 / z_v
    #         qbound_case2 = self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * ((1 - self.chi) * self.service_rate +
    #                                              self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)))) / (z_v - self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)))) ** 2
    #         qbound_case4 = self.total_payment / (self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)) * (
    #             (self.malicious_arrival_rate + self.gamma) / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) ** (-2)
    #         print(
    #             f"Bound 2 : {bound_case2}, Bound 4 : {bound_case4}, Qbound 2 : {qbound_case2}, Qbound 4 : {qbound_case4}")
    #         if bound_case2 < qbound_case2 and bound_case4 < qbound_case4:  # No queuing
    #             A = 0
    #             for dev in self.device_list:
    #                 A += (dev.price_per_task * (ASP_DEVICE_LATENCY_UPPER - dev.transmission_time_to_asp) / (
    #                     ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))
    #             B = self.total_payment / \
    #                 (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
    #             C = self.service_rate
    #             D = self.malicious_arrival_rate * self.service_rate / \
    #                 GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) + self.arrival_rate - self.malicious_arrival_rate
    #             phi = (A * C * D + 2 * B * C - 2 * C *
    #                    sqrt(B ** 2 + A * B * D)) / (D ** 2)
    #             z_v_zero = sqrt(self.total_payment / ((self.arrival_rate) * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
    #                             * phi)) + self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) + self.normal_arrival_rate / self.service_rate
    #             if z_v_zero < (self.malicious_arrival_rate / (GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) * self.chi)):
    #                 self.change_point = self.total_payment / self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (self.malicious_arrival_rate / (
    #                     self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) - self.normal_arrival_rate / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) ** (-2)
    #                 A = 0
    #                 for dev in self.device_list:
    #                     A += (dev.price_per_task * (ASP_DEVICE_LATENCY_UPPER - dev.transmission_time_to_asp) / (
    #                         ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))
    #                 B = self.total_payment / \
    #                     (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
    #                 C = self.service_rate * \
    #                     (1 - self.chi) + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))
    #                 D = self.arrival_rate
    #                 self.bound = (A * C * D + 2 * B * C - 2 * C *
    #                               sqrt(B ** 2 + A * B * D)) / (D ** 2)
    #                 self.qbound = None
    #                 # print(4)
    #                 self.case = 4
    #             else:
    #                 self.bound = phi
    #                 self.change_point = None
    #                 self.qbound = None
    #                 # print(2)
    #                 self.case = 2
    #         elif bound_case2 > qbound_case2 and bound_case4 > qbound_case4:
    #             if (self.arrival_rate + self.gamma) / self.service_rate > (self.malicious_arrival_rate / (GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) * self.chi)):
    #                 self.bound = bound_case4
    #                 self.qbound = qbound_case4
    #                 if self.qbound > self.bound:
    #                     print(self.qbound, self.bound)
    #                 self.change_point = None
    #                 # print(1)
    #                 self.case = 1
    #             else:
    #                 self.change_point = self.total_payment / self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (self.malicious_arrival_rate / (
    #                     self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) - self.normal_arrival_rate / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) ** (-2)
    #                 self.bound = bound_case2
    #                 self.qbound = qbound_case2
    #                 if self.qbound > self.bound:
    #                     print(self.qbound, self.bound)
    #                 # print(3)
    #                 self.case = 3
    #         elif bound_case2 < qbound_case2 and bound_case4 > qbound_case4:  # 1 & 4
    #             if (self.arrival_rate + self.gamma) / self.service_rate > (self.malicious_arrival_rate / (GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) * self.chi)):
    #                 self.bound = bound_case4
    #                 self.qbound = qbound_case4
    #                 if self.qbound > self.bound:
    #                     print(self.qbound, self.bound)
    #                 self.change_point = None
    #                 # print(1)
    #                 self.case = 1
    #             else:
    #                 self.change_point = self.total_payment / self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (self.malicious_arrival_rate / (
    #                     self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) - self.normal_arrival_rate / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) ** (-2)
    #                 A = 0
    #                 for dev in self.device_list:
    #                     A += (dev.price_per_task * (ASP_DEVICE_LATENCY_UPPER - dev.transmission_time_to_asp) / (
    #                         ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))
    #                 B = self.total_payment / \
    #                     (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
    #                 C = self.service_rate * \
    #                     (1 - self.chi) + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))
    #                 D = self.arrival_rate
    #                 self.bound = (A * C * D + 2 * B * C - 2 * C *
    #                               sqrt(B ** 2 + A * B * D)) / (D ** 2)
    #                 self.qbound = None
    #                 # print(4)
    #                 self.case = 4
    #         else:
    #             A = 0
    #             for dev in self.device_list:
    #                 A += (dev.price_per_task * (ASP_DEVICE_LATENCY_UPPER - dev.transmission_time_to_asp) / (
    #                     ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))
    #             B = self.total_payment / \
    #                 (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
    #             C = self.service_rate
    #             D = self.malicious_arrival_rate * self.service_rate / \
    #                 GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) + self.arrival_rate - self.malicious_arrival_rate
    #             phi = (A * C * D + 2 * B * C - 2 * C *
    #                    sqrt(B ** 2 + A * B * D)) / (D ** 2)
    #             z_v_zero = sqrt(self.total_payment / ((self.arrival_rate) * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
    #                             * phi)) + self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) + self.normal_arrival_rate / self.service_rate
    #             if z_v_zero < (self.malicious_arrival_rate / (GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) * self.chi)):
    #                 self.change_point = self.total_payment / self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (self.malicious_arrival_rate / (
    #                     self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) - self.normal_arrival_rate / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) ** (-2)
    #                 self.bound = bound_case2
    #                 self.qbound = qbound_case2
    #                 if self.qbound > self.bound:
    #                     print(self.qbound, self.bound)
    #                 # print(3)
    #                 self.case = 3
    #             else:
    #                 self.bound = phi
    #                 self.change_point = None
    #                 self.qbound = None
    #                 # print(2)
    #                 self.case = 2

    #     else:  # case3
    #         bound = util2 / z_v
    #         qbound = self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (
    #             (1) * self.service_rate)) / (z_v - self.arrival_rate / ((1) * self.service_rate)) ** 2
    #         self.case = 5
    #         self.change_point = None
    #         if bound < qbound:
    #             A = 0
    #             for dev in self.device_list:
    #                 A += (dev.price_per_task * (ASP_DEVICE_LATENCY_UPPER - dev.transmission_time_to_asp) / (
    #                     ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))
    #             B = self.total_payment / \
    #                 (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
    #             C = self.service_rate
    #             D = self.arrival_rate
    #             self.qbound = None
    #             self.bound = (A * C * D + 2 * B * C - 2 * C *
    #                           sqrt(B ** 2 + A * B * D)) / (D ** 2)
    #         else:
    #             self.bound = bound
    #             self.qbound = qbound
    #     return
    def set_boundary(self):
        z_v = (self.arrival_rate + self.gamma) / self.service_rate
        util1 = 0
        util2 = 0
        for dev in self.device_list:
            util1 += (dev.price_per_task *
                      (self.uniform_cdf(dev.transmission_time_to_asp + self.case2_time(z_v))))
            util2 += (dev.price_per_task *
                      (self.uniform_cdf(dev.transmission_time_to_asp + self.time(z_v, 0))))
        if GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) > self.service_rate:  # case 2 & 4
            bound_case = util1 / z_v
            qbound_case2 = self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * ((1 - self.chi) * self.service_rate +
                                                 self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff))) / (z_v - self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff))) ** 2
            qbound_case4 = self.total_payment / (self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)) * (
                (self.malicious_arrival_rate + self.gamma) / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)) ** (-2)

            A = 0
            for dev in self.device_list:
                A += (dev.price_per_task * (ASP_DEVICE_LATENCY_UPPER - dev.transmission_time_to_asp) / (
                    ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))
            B = self.total_payment / \
                (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
            C = self.service_rate
            D = self.malicious_arrival_rate * self.service_rate / \
                GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) + self.arrival_rate - self.malicious_arrival_rate
            case_B_phi = (A * C * D + 2 * B * C - 2 * C *
                          sqrt(B ** 2 + A * B * D)) / (D ** 2)
            A = 0
            for dev in self.device_list:
                A += (dev.price_per_task * (ASP_DEVICE_LATENCY_UPPER - dev.transmission_time_to_asp) / (
                    ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))
            B = self.total_payment / \
                (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
            C = self.service_rate * \
                (1 - self.chi) + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)
            D = self.arrival_rate
            case_D_phi = (A * C * D + 2 * B * C - 2 * C *
                          sqrt(B ** 2 + A * B * D)) / (D ** 2)
            z_v_zero = sqrt(self.total_payment / ((self.service_rate) * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
                                                  * case_B_phi)) + self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) + self.normal_arrival_rate / self.service_rate
            # print(
            #     f"Bound : {bound_case}, Qbound 2 : {qbound_case2}, Qbound 4 : {qbound_case4}, Z_v_zero : {z_v_zero}, phi_b : {case_B_phi}, phi_d : {case_D_phi}")
            if bound_case > qbound_case4 and (self.malicious_arrival_rate / (GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) * self.chi)) < (self.arrival_rate + self.gamma) / self.service_rate:
                self.bound = bound_case
                self.qbound = qbound_case4
                if self.qbound > self.bound:
                    print(self.qbound, self.bound)
                self.change_point = None
                # print(1)
                self.case = 1
            elif z_v_zero > (self.arrival_rate + self.gamma) / self.service_rate and z_v_zero > (self.malicious_arrival_rate / (GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) * self.chi)):
                self.bound = case_B_phi
                self.change_point = None
                self.qbound = None
                # print(2)
                self.case = 2
            elif (self.malicious_arrival_rate / (GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) * self.chi)) > (self.arrival_rate + self.gamma) / self.service_rate and bound_case > qbound_case2:
                self.change_point = self.total_payment / self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (self.malicious_arrival_rate / (
                    self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)) - self.normal_arrival_rate / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)) ** (-2)
                self.bound = bound_case
                self.qbound = qbound_case2
                if self.qbound > self.bound:
                    print(self.qbound, self.bound)
                # print(3)
                self.case = 3
            else:
                self.change_point = self.total_payment / self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (self.malicious_arrival_rate / (
                    self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)) - self.normal_arrival_rate / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)) ** (-2)
                self.bound = case_D_phi
                self.qbound = None
                # print(4)
                self.case = 4
            # if bound_case < qbound_case2 and bound_case < qbound_case4:  # No queuing
            #     if z_v_zero < (self.malicious_arrival_rate / (GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) * self.chi)):
            #         self.change_point = self.total_payment / self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (self.malicious_arrival_rate / (
            #             self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) - self.normal_arrival_rate / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) ** (-2)
            #         self.bound = case_D_phi
            #         self.qbound = None
            #         # print(4)
            #         self.case = 4
            #     else:

            #         self.bound = case_B_phi
            #         self.change_point = None
            #         self.qbound = None
            #         # print(2)
            #         self.case = 2
            # elif bound_case > qbound_case2 and bound_case > qbound_case4:
            #     if (self.arrival_rate + self.gamma) / self.service_rate > (self.malicious_arrival_rate / (GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) * self.chi)):
            #         self.bound = bound_case
            #         self.qbound = qbound_case4
            #         if self.qbound > self.bound:
            #             print(self.qbound, self.bound)
            #         self.change_point = None
            #         # print(1)
            #         self.case = 1
            #     else:
            #         self.change_point = self.total_payment / self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (self.malicious_arrival_rate / (
            #             self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) - self.normal_arrival_rate / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) ** (-2)
            #         self.bound = bound_case
            #         self.qbound = qbound_case2
            #         if self.qbound > self.bound:
            #             print(self.qbound, self.bound)
            #         # print(3)
            #         self.case = 3
            # elif bound_case < qbound_case2 and bound_case > qbound_case4:  # 1 & 4
            #     if (self.arrival_rate + self.gamma) / self.service_rate > (self.malicious_arrival_rate / (GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) * self.chi)):
            #         self.bound = bound_case
            #         self.qbound = qbound_case4
            #         if self.qbound > self.bound:
            #             print(self.qbound, self.bound)
            #         self.change_point = None
            #         # print(1)
            #         self.case = 1
            #     else:
            #         self.change_point = self.total_payment / self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (self.malicious_arrival_rate / (
            #             self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) - self.normal_arrival_rate / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) ** (-2)
            #         A = 0
            #         for dev in self.device_list:
            #             A += (dev.price_per_task * (ASP_DEVICE_LATENCY_UPPER - dev.transmission_time_to_asp) / (
            #                 ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))
            #         B = self.total_payment / \
            #             (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
            #         C = self.service_rate * \
            #             (1 - self.chi) + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))
            #         D = self.arrival_rate
            #         self.bound = (A * C * D + 2 * B * C - 2 * C *
            #                       sqrt(B ** 2 + A * B * D)) / (D ** 2)
            #         self.qbound = None
            #         # print(4)
            #         self.case = 4
            # else:
            #     A = 0
            #     for dev in self.device_list:
            #         A += (dev.price_per_task * (ASP_DEVICE_LATENCY_UPPER - dev.transmission_time_to_asp) / (
            #             ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))
            #     B = self.total_payment / \
            #         (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
            #     C = self.service_rate
            #     D = self.malicious_arrival_rate * self.service_rate / \
            #         GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) + self.arrival_rate - self.malicious_arrival_rate
            #     phi = (A * C * D + 2 * B * C - 2 * C *
            #            sqrt(B ** 2 + A * B * D)) / (D ** 2)
            #     z_v_zero = sqrt(self.total_payment / ((self.arrival_rate) * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
            #                     * phi)) + self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) + self.normal_arrival_rate / self.service_rate
            #     if z_v_zero < (self.malicious_arrival_rate / (GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) * self.chi)):
            #         self.change_point = self.total_payment / self.service_rate * (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (self.malicious_arrival_rate / (
            #             self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) - self.normal_arrival_rate / self.service_rate - self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))) ** (-2)
            #         self.bound = bound_case
            #         self.qbound = qbound_case2
            #         if self.qbound > self.bound:
            #             print(self.qbound, self.bound)
            #         # print(3)
            #         self.case = 3
            #     else:
            #         self.bound = phi
            #         self.change_point = None
            #         self.qbound = None
            #         # print(2)
            #         self.case = 2

        else:  # case3
            bound = util2 / z_v
            qbound = self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * (
                (1) * self.service_rate)) / (z_v - self.arrival_rate / ((1) * self.service_rate)) ** 2
            self.case = 5
            self.change_point = None
            if bound < qbound:
                A = 0
                for dev in self.device_list:
                    A += (dev.price_per_task * (ASP_DEVICE_LATENCY_UPPER - dev.transmission_time_to_asp) / (
                        ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER))
                B = self.total_payment / \
                    (ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
                C = self.service_rate
                D = self.arrival_rate
                self.qbound = None
                self.bound = (A * C * D + 2 * B * C - 2 * C *
                              sqrt(B ** 2 + A * B * D)) / (D ** 2)
            else:
                self.bound = bound
                self.qbound = qbound
        return
    """
    set_process_time : set the process_time with existing z_v and z_h
    """

    def set_process_time(self):
        self.process_time = 1 / ((self.z_v - self.z_h) * self.service_rate - (
            self.arrival_rate - ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff)))
    """
    optimize_zv : set the optimize z_v and calculate utility
    """

    def optimize_zv(self):
        if GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) > self.service_rate and self.chi != 0:
            if self.case == 1:
                # print(self.case)
                self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price *
                                self.service_rate)) + self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) + self.normal_arrival_rate / self.service_rate
                if self.z_v < (self.gamma + self.arrival_rate) / self.service_rate:
                    self.z_v = (self.gamma + self.arrival_rate) / \
                        self.service_rate
                self.z_h = self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)
                self.set_process_time()
                self.set_utility()
                if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff):
                    print((self.z_v - self.z_h) * self.service_rate -
                          self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff))
                    print('infeasible')
                if self.utility < 0:
                    self.z_v = 0
                    self.z_h = 0
                    self.utility = 0
            elif self.case == 2:
                # print(self.case)
                self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price *
                                self.service_rate)) + self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) + self.normal_arrival_rate / self.service_rate
                self.z_h = self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)
                self.set_process_time()
                self.set_utility()
                if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff):
                    print((self.z_v - self.z_h) * self.service_rate -
                          self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff))
                    print('infeasible')
                if self.utility < 0:
                    self.z_v = 0
                    self.z_h = 0
                    self.utility = 0
            elif self.case == 3:
                # print(self.case)
                self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price *
                                self.service_rate)) + self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) + self.normal_arrival_rate / self.service_rate
                if self.z_v > self.malicious_arrival_rate / (self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)):
                    self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price *
                                    self.service_rate)) + self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) + self.normal_arrival_rate / self.service_rate
                    self.z_h = self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)
                    self.set_process_time()
                    self.set_utility()
                    if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff):
                        print((self.z_v - self.z_h) * self.service_rate -
                              self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff))
                        print('infeasible')
                    if self.utility < 0:
                        self.z_v = 0
                        self.z_h = 0
                        self.utility = 0
                else:
                    self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * ((1 - self.chi) *
                                    self.service_rate + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)))) + self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff))
                    self.z_h = self.chi * self.z_v
                    if self.z_v < (self.gamma + self.arrival_rate) / self.service_rate:
                        self.z_v = (self.gamma + self.arrival_rate) / \
                            self.service_rate
                        self.z_h = self.chi * self.z_v

                    self.set_process_time()
                    self.set_utility()
                    if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff):
                        print((self.z_v - self.z_h) * self.service_rate -
                              self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff))
                        print('infeasible')
                    if self.utility < 0:
                        self.z_v = 0
                        self.z_h = 0
                        self.utility = 0
            elif self.case == 4:
                # print(self.case)
                self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price *
                                self.service_rate)) + self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) + self.normal_arrival_rate / self.service_rate
                if self.z_v > self.malicious_arrival_rate / (self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)):
                    self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price *
                                    self.service_rate)) + self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) + self.normal_arrival_rate / self.service_rate
                    self.z_h = self.malicious_arrival_rate / GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)
                    self.set_process_time()
                    self.set_utility()
                    if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff):
                        print((self.z_v - self.z_h) * self.service_rate -
                              self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff))
                        print('infeasible')
                    if self.utility < 0:
                        self.z_v = 0
                        self.z_h = 0
                        self.utility = 0
                else:
                    self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * ((1 - self.chi) *
                                    self.service_rate + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)))) + self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff))
                    self.z_h = self.chi * self.z_v
                    self.set_process_time()
                    self.set_utility()
                    if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff):
                        print((self.z_v - self.z_h) * self.service_rate -
                              self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff))
                        print('infeasible')
                    if self.utility < 0:
                        self.z_v = 0
                        self.z_h = 0
                        self.utility = 0

        else:
            self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
                            * self.mpo_price * self.service_rate)) + self.arrival_rate / self.service_rate
            self.z_h = 0
            if self.z_v < (self.gamma + self.arrival_rate) / self.service_rate:
                self.z_v = (self.gamma + self.arrival_rate) / self.service_rate
            if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff):
                print((self.z_v - self.z_h) * self.service_rate -
                      self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff))
                print('infeasible')
            self.set_process_time()
            self.set_utility()
            if self.utility < 0:
                self.z_v = 0
                self.z_h = 0
                self.utility = 0

    def optimize_zv_without_constraint(self):
        if GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff) > self.service_rate:
            self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * ((1 - self.chi) *
                            self.service_rate + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)))) + self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff))
            self.z_h = self.chi * self.z_v
            self.set_process_time()
            self.set_utility()
            if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff):
                print('infeasible')
        else:
            self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
                            * self.mpo_price * self.service_rate)) + self.arrival_rate / self.service_rate
            self.z_h = 0
            self.set_process_time()
            self.set_utility()
            if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff):
                print('infeasible')

    # def report_asp(self, price):
    #     self.mpo_price = price
    #     case = 'e'
    #     if GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)) > self.service_rate:
    #         self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * ((1 - self.chi) *
    #                         self.service_rate + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate))))) + self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate)))
    #         if self.z_v < (self.gamma + self.arrival_rate) / self.service_rate:
    #             self.z_v = (self.gamma + self.arrival_rate) / self.service_rate
    #             case = 'q'
    #         self.z_h = self.chi * self.z_v
    #         self.set_process_time()
    #         self.set_utility()
    #         if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff):
    #             print('infeasible')
    #         if self.utility < 0:
    #             self.z_v = 0
    #             self.utility = 0
    #             case = 'z'
    #     else:
    #         self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER)
    #                         * self.mpo_price * self.service_rate)) + self.arrival_rate / self.service_rate
    #         self.z_h = 0
    #         if self.z_v < ((self.gamma + self.arrival_rate) / self.service_rate):
    #             self.z_v = (self.gamma + self.arrival_rate) / self.service_rate
    #             case = 'q'
    #         if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff):
    #             print('infeasible')
    #             self.z_h = 0
    #         self.set_process_time()
    #         self.set_utility()
    #         if self.utility < 0:
    #             self.z_v = 0
    #             self.utility = 0
    #             case = 'z'
    #     return case

    def res(self, price):
        if self.case == 1:
            if price > self.bound:
                return 'z'
            elif price > self.qbound and price < self.bound:
                return 'q'
            else:
                return 'e2'
        elif self.case == 2:
            if price > self.bound:
                return 'z'
            else:
                return 'e2'
        elif self.case == 3:
            if price > self.bound:
                return 'z'
            elif price > self.qbound and price < self.bound:
                return 'q'
            elif price < self.qbound and price > self.change_point:
                return 'e1'
            else:
                return 'e2'
        elif self.case == 4:
            if price > self.bound:
                return 'z'
            elif price < self.bound and price > self.change_point:
                return 'e1'
            else:
                return 'e2'
        else:
            if price > self.bound:
                return 'z'
            elif self.qbound and price > self.qbound:
                return 'q'
            else:
                return 'e3'

    """
    set_zv_zh : set the asp with chi
    """

    def set_zv_zh(self, chi):
        self.chi = chi
        self.z_v = sqrt(self.total_payment / ((ASP_DEVICE_LATENCY_UPPER - ASP_DEVICE_LATENCY_LOWER) * self.mpo_price * ((1 - self.chi) *
                        self.service_rate + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff)))) + self.arrival_rate / ((1 - self.chi) * self.service_rate + self.chi * GLOBAL_ETA((self.malicious_arrival_rate)/(self.arrival_rate), self.eff))
        if self.z_v < (self.gamma + self.arrival_rate) / self.service_rate:
            self.z_v = (self.gamma + self.arrival_rate) / self.service_rate
        self.z_h = self.chi * self.z_v
        self.set_process_time()
        self.set_utility()
        if self.phi * self.z_v * self.service_rate > (self.z_v - self.z_h) * self.service_rate - self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff):
            print((self.z_v - self.z_h) * self.service_rate -
                  self.arrival_rate + ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff))
            # print(self.z_v, self.z_h, self.arrival_rate, ASP_H(self.z_h, self.malicious_arrival_rate, (self.malicious_arrival_rate)/(self.arrival_rate), self.eff), self.malicious_arrival_rate)
            print('infeasible')
        if self.utility < 0:
            self.z_v = 0
            self.utility = 0
            self.z_h = 0