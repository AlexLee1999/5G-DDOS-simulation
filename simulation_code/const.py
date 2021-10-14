from cvxpy import CVXOPT
from cvxpy.settings import CVXOPT, ECOS
from enum import Enum

########################################
# These are the parameters of Global
# Prefix with GLOBAL_
########################################
GLOBAL_ETA = 50
# Conference 5000
ITER = 1000
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
DEVICE_DISTANCE_UPPER = 100
DEVICE_DISTANCE_LOWER = 50
# frequency
DEVICE_FREQUENCY = 2.1
# required cpu cycle
DEVICE_REQUIRED_CPU_CYCLE_UPPER = 0.9E8
# Conference 0.9E6
DEVICE_REQUIRED_CPU_CYCLE_LOWER = 0.1E8
# Conference 0.1E6
DEVICE_REQUIRED_CPU_CYCLE_HIGH_UPPER = 0.9E8
DEVICE_REQUIRED_CPU_CYCLE_HIGH_LOWER = 0.5E8
DEVICE_REQUIRED_CPU_CYCLE_LOW_UPPER = 0.5E8
DEVICE_REQUIRED_CPU_CYCLE_LOW_LOWER = 0.1E8
# task size
DEVICE_TASK_SIZE_UPPER = 50  # 5 kB
# Conference 5
DEVICE_TASK_SIZE_LOWER = 40  # 4 kB
# Conference 4
# arrival rate
DEVICE_ARRIVAL_RATE_UPPER = 3
DEVICE_ARRIVAL_RATE_LOWER = 1
# price per task
DEVICE_PRICE_PER_TASK_UPPER = 100
# COnference 10
DEVICE_PRICE_PER_TASK_LOWER = 1

########################################
# These are the parameters of ASP
# Prefix with ASP_
########################################
# latency
ASP_DEVICE_LATENCY_UPPER = 1000E-3
# Confernece 100E-3
ASP_DEVICE_LATENCY_LOWER = 5E-3

ASP_BANDWIDTH = 4 * 10E8
# Conference 20 * 10E6
ASP_CHI_LOWER = 0.1
# Conference 0.999
ASP_CHI_UPPER = 0.2
# Conference 0.999
ASP_GAMMA_LOWER = 20
# COnference 100
ASP_GAMMA_UPPER = 40
# Conference 100

###################################################
# H function


def ASP_H(x, lambda_m):
    return min(GLOBAL_ETA * x, lambda_m)


########################################
# These are the parameters of MPO
# Prefix with MPO_
########################################
MPO_NUM_OF_ASP = 5

MPO_NUM_OF_VM_LOWER = 1000
MPO_NUM_OF_VM_UPPER = 1000

MPO_CPU_FREQUENCY = 0.25 * 10E9


def MPO_cost(x):
    return 0.01 * x ** 2


CVX_SOLVER = CVXOPT


class load_type(Enum):
    HIGH = 1
    AVERAGE = 2
    LOW = 3
    RATIO = 4


# PLOT config

FIG_SIZE = (50, 25)
DPI = 400
LINE_WIDTH = 4
LABEL_FONT_SIZE = 100
LEGEND_FONT_SIZE = 100
TICKS_FONT_SIZE = 80
MARKER_SIZE = 30
MARKER_EDGE_WIDTH = 3


NUM_LST = [400, 600, 800, 1000, 1200, 1400]
RATIO_LST = [0.08, 0.1, 0.2, 0.3, 0.4, 0.5]
STEP = 3
