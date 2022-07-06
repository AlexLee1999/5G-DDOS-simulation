from cvxpy import CVXOPT
from cvxpy.settings import CVXOPT, ECOS, SCS
from enum import Enum

########################################
# These are the parameters of Global
# Prefix with GLOBAL_
########################################
# GLOBAL_ETA = 50
DEFAULT_ETA = 50
def GLOBAL_ETA(mal, eff):
    return eff * mal
# Conference 5000
ITER = 1500
JPG_ENABLE = False
DEFAULT_DEVICE_NUM = 1000
# Conference 100
DEFAULT_DEVICE_RATIO = 0.1
# COnference 0.5
########################################
# These are the parameters of Device
# Prefix with DEVICE_
########################################
# tx_power
DEVICE_TX_POWER = 199.5262315
# distance
DEVICE_DISTANCE_UPPER = 50
DEVICE_DISTANCE_LOWER = 50
# frequency
DEVICE_FREQUENCY = 2.1
# required cpu cycle    
# DEVICE_REQUIRED_CPU_CYCLE_UPPER = 0.9E8
# # Conference 0.9E6
# DEVICE_REQUIRED_CPU_CYCLE_LOWER = 0.1E8
# # Conference 0.1E6
# DEVICE_REQUIRED_CPU_CYCLE_HIGH_UPPER = 0.9E8
# DEVICE_REQUIRED_CPU_CYCLE_HIGH_LOWER = 0.8E8
# DEVICE_REQUIRED_CPU_CYCLE_LOW_UPPER = 0.2E8
# DEVICE_REQUIRED_CPU_CYCLE_LOW_LOWER = 0.1E8
# task size
DEVICE_TASK_SIZE_UPPER = 12
DEVICE_TASK_SIZE_LOWER = 8

DEVICE_TASK_SIZE_HIGH_UPPER = 12
DEVICE_TASK_SIZE_HIGH_LOWER = 11

DEVICE_TASK_SIZE_LOW_UPPER = 9
DEVICE_TASK_SIZE_LOW_LOWER = 8
CPU_CYCLE_PER_BITS = 500
# arrival rate
DEVICE_ARRIVAL_RATE_UPPER = 1
DEVICE_ARRIVAL_RATE_LOWER = 0.6
# price per task
DEVICE_PRICE_PER_TASK_UPPER = 100
# Conference 10
DEVICE_PRICE_PER_TASK_LOWER = 1

########################################
# These are the parameters of ASP
# Prefix with ASP_
########################################
# latency
ASP_DEVICE_LATENCY_UPPER = 1000E-3
# Confernece 100E-3
ASP_DEVICE_LATENCY_LOWER = 15E-3

ASP_BANDWIDTH = 4E8
# Conference 20 * 10E6
ASP_CHI_LOWER = 0.1
# Conference 0.999
ASP_CHI_UPPER = 0.2
# Conference 0.999
ASP_GAMMA_LOWER = 20
# Conference 100
ASP_GAMMA_UPPER = 40
# Conference 100

###################################################
# H function


def ASP_H(x, lambda_m, mal, eff):
    return min(GLOBAL_ETA(mal, eff) * x, lambda_m)


########################################
# These are the parameters of MPO
# Prefix with MPO_
########################################
MPO_NUM_OF_ASP = 5

MPO_NUM_OF_VM = 1000


MPO_VM_CPU_FREQUENCY = 0.2 * 1E9


def MPO_cost(x):
    return 0.01 * x ** 2


CVX_SOLVER = ECOS
ALTER_CVX_SOLVER = SCS


class load_type(Enum):
    HIGH = 1
    AVERAGE = 2
    LOW = 3
    RATIO = 4


# PLOT config parameters

FIG_SIZE = (50, 25)
DPI = 400
LINE_WIDTH = 4
LABEL_FONT_SIZE = 100
LEGEND_FONT_SIZE = 60
TICKS_FONT_SIZE = 80
MARKER_SIZE = 30
MARKER_EDGE_WIDTH = 3


NUM_LST = [200, 400, 600, 800, 1000]
RATIO_LST = [0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25]
EFF_LST = [5, 30, 50, 100, 150, 200, 250, 300]
EPSILON = 0.0001
IPS_PROP_COFF = 0.3
EFF_IPS_PROP_COFF = 0.0001