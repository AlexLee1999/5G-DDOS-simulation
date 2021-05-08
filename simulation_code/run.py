from asp import ASP
from const import *
from device import Device
from mpo import MPO

if __name__ == '__main__':
    mpo = MPO()
    mpo.optimize_phi()
    asp = ASP()
    asp.plot_max()
