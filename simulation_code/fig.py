import pickle
import matplotlib.pyplot as plt
from const import *

class Fig(object) :
    def __init__ (self, x_lst, data_dic, x_title, y_title, fig_name, marker_dic):
        self.x_lst = x_lst
        self.data_dic = data_dic
        self.x_title = x_title
        self.y_title = y_title
        self.fig_name = fig_name
        self.marker_dic = marker_dic

def write_fig(fig, fig_name):
    with open('fig_db/%s.db' % fig_name, 'wb') as handle:
        pickle.dump(fig, handle, protocol=pickle.HIGHEST_PROTOCOL)

def plot_fig(fig):
    plt.figure(figsize=FIG_SIZE, dpi=DPI)
    for d in fig.data_dic:
        plt.plot(fig.x_lst, fig.data_dic[d], marker=fig.marker_dic[d], markerfacecolor='none', label=d, linewidth=LINE_WIDTH, markersize=MARKER_SIZE, mew=MARKER_EDGE_WIDTH)
    plt.legend(loc="best", fontsize=LEGEND_FONT_SIZE)
    plt.xlabel(fig.x_title, fontsize=LABEL_FONT_SIZE)
    plt.ylabel(fig.y_title, fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=TICKS_FONT_SIZE)
    plt.yticks(fontsize=TICKS_FONT_SIZE)
    plt.savefig('./temp.jpg')
    plt.close()

def read_fig(fig_path):
    with open(f'{fig_path}', 'rb') as handle:
        fig = pickle.load(handle)
    return fig