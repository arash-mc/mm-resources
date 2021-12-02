import matplotlib as mpl
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, Animation, writers
from IPython.display import HTML
from matplotlib import patches
from matplotlib import cm
import numpy as np
from matplotlib.colors import Normalize


class Viewer():
    def __init__(self, output, label, cm_name='viridis'):
        self.cm_name = cm_name
        self.cb = None
        self.data = output['data'][label]
        self.frame_number = 0
        self.max = len(self.data) - 1
        self.image_shape = self.data[self.frame_number].shape
        nx = len(output['parameters']['inner_values'])
        ny = len(output['parameters']['outer_values'])
        self.nx = nx
        self.ny = ny
        rect_indices = {}
        for i in range(ny):
            rect_indices[i] = {}
        self.rect_indices = rect_indices
        self.phase_diagram = self.make_list_of_zeros(nx, ny)
        self.phase_diagramn = self.make_list_of_nones(nx, ny)
        self.rectlist = list()
        self.rectlistn = list()
        self.grid_list = list()
        self.colormap = cm.get_cmap(cm_name)
        self.cb_ax = None
        self.ax = None
        self.fig = None
        self.none_color = [0.5, 0.5, 0.5, 1]
        self.line_color = [0.8, 0.8, 0.8, 1]
        self.grid_color = [0.4, 0.4, 0.4, 1]
        self.patch_alpha = 1
        self.partial_max = 'on'
        self.partial_min = 'on'
        self.grid = 'on'
        self.output = output
        self.flag = 0
        self.invertedy = 1
        self.colorbar_ticks = [0, 0.2, 0.4, 0.6, 0.8, 1]
        self.colorbar_labels = [format(x*self.max, ".2f")
                                for x in self.colorbar_ticks]
        self.colorbar_title = 'Frame'
        self.colorbar_max = self.max
        self.colorbar_min = 0
        self.patch_on = None
        self.patch_off = None
        self.default_title = ''
        self.colorbar_ticklabel_function = lambda x: x
        self.x_label_function = lambda x: x
        self.y_label_function = lambda x: x
        self.x_label_format = "%.2e"
        self.y_label_format = "%.2e"
        self.norm = Normalize(vmin=self.colorbar_min, vmax=self.colorbar_max)
        self.show_frame_number = 'on'
        parameters = self.output['parameters']
        self.default_xlabel = r'{}'.format(parameters['inner'])
        self.default_ylabel = r'{}'.format(parameters['outer'])
        self.legend = None
        self.legend_on = 'on'
        self.legend_off = 'off'

    def set_colormap(self, cm_name):
        self.cm_name = cm_name
        self.colormap = cm.get_cmap(cm_name)
        # self.cb = mpl.colorbar.ColorbarBase(self.cb_ax, orientation='vertical',
        #      cmap=self.colormap, ticks=[0, 1])
    def fix_colorbar(self,view):
            m = view.cb_ax.get_yticklabels()
            [m[i].set_text(self.colorbar_labels[i]) for i in range(len(m))]
            view.cb_ax.set_yticklabels(m)
    def export_process(self):
        process = {}
        process['cm_name'] = self.cm_name
        process['phase_diagram'] = self.phase_diagram
        process['phase_diagramn'] = self.phase_diagramn
        process['none_color'] = self.none_color
        process['line_color'] = self.line_color
        process['grid_color'] = self.grid_color
        process['patch_alpha'] = self.patch_alpha
        process['partial_max'] = self.partial_max
        process['partial_min'] = self.partial_min
        return process

    def invert(self):
        invertedn = self.phase_diagramn.copy()
        inverted = self.phase_diagram.copy()
        for i, outer in enumerate(self.phase_diagramn):
            for j, inner in enumerate(outer):
                if inner is None:
                    inverted[i][j] = 1
                    invertedn[i][j] = 1
                else:
                    inverted[i][j] = 0
                    invertedn[i][j] = None
        return inverted, invertedn

    def save_figure(self, filename):
        self.fig.savefig(filename)

    def import_process(self, process):
        self.cm_name = process['cm_name']
        self.phase_diagram = process['phase_diagram']
        self.phase_diagramn = process['phase_diagramn']
        self.none_color = process['none_color']
        self.line_color = process['line_color']
        self.grid_color = process['grid_color']
        self.patch_alpha = process['patch_alpha']
        self.partial_max = process['partial_max']
        self.partial_min = process['partial_min']

    def show_markers(self):
        shape = self.image_shape
        xd = shape[1] / self.nx
        yd = shape[0] / self.ny
        for indy in range(self.ny):
            for indx in range(self.nx):
                if self.phase_diagramn[indy][indx] is not None:
                    color = self.colormap(
                        self.phase_diagramn[indy][indx]/self.max)
                    rect = patches.Rectangle((indx * xd, indy * yd), xd, yd, linewidth=1, edgecolor=color,
                                             facecolor='none')
                    self.rect_indices[indy][indx] = rect
                    self.ax.add_patch(rect)

    def make_list_of_zeros(self, nx, ny):
        l = list()
        for i in range(ny):
            l.append(list())
            for j in range(nx):
                l[i].append(0)
        return l

    def make_list_of_nones(self, nx, ny):
        l = list()
        for i in range(ny):
            l.append(list())
            for j in range(nx):
                l[i].append(None)
        return l

    def add_colorbar(self):
        if not self.cb_ax and not self.cb:
            main_ax_position = self.ax.get_position()
            main_ax_xmax = main_ax_position.xmax
            ymin = main_ax_position.ymin
            ymax = main_ax_position.ymax
            self.cb_ax = self.fig.add_axes(
                [main_ax_xmax + 0.03, ymin, 0.02, ymax - ymin])

        self.set_colormap(self.cm_name)
        self.cb = mpl.colorbar.ColorbarBase(self.cb_ax, orientation='vertical',
                                            cmap=self.colormap, ticks=self.colorbar_ticks)
        self.cb_ax.set_title(self.colorbar_title)
        self.cb_ax.set_yticks(self.colorbar_ticks)
        m = self.cb_ax.get_yticklabels()
        [m[i].set_text(self.colorbar_labels[i]) for i in range(len(m))]
        self.cb_ax.set_yticklabels(m)
        # self.cb_ax.set_yticklabels(self.colorbar_labels)
        # self.cb_ax.set_visible(False)

    def add_legend(self):
        if self.legend is None and self.patch_on is not None and self.patch_off is not None:
            self.patch_on.set_alpha(1)
            self.patch_off.set_alpha(1)
            self.legend = self.fig.legend([self.patch_on, self.patch_off], [self.legend_on, self.legend_off],
                                          loc='best', bbox_to_anchor=(0.5, 0.35, 0.5, 0.5)
                                          )
            self.patch_on.set_alpha(self.patch_alpha)
            self.patch_off.set_alpha(self.patch_alpha)

    def remove_legend(self):
        if self.legend is not None:
            self.legend.remove()
            self.legend = None

    def show_colorbar(self):
        if self.cb_ax:
            self.cb_ax.set_visible(True)

    def hide_colorbar(self):
        if self.cb_ax and self.cb:
            # self.cb_ax.set_visible(False)
            # self.cb.remove()
            self.cb_ax.remove()
            self.cb_ax = None
            self.cb = None

    def show_grid(self):
        shape = self.image_shape
        xd = shape[1] / self.nx
        yd = shape[0] / self.ny
        if len(self.grid_list) == 0:
            for i in range(self.ny):
                for j in range(self.nx):
                    rect = patches.Rectangle((j * xd, i * yd), xd, yd, linewidth=1,
                                             edgecolor=self.grid_color, facecolor='none')
                    self.grid_list.append(rect)
                    self.ax.add_patch(rect)

    def hide_grid(self):
        for item in self.grid_list:
            item.remove()
        self.grid_list = list()

    def show(self, frame_number=0):
        shape = self.data[self.frame_number].shape
        parameters = self.output['parameters']
        xd = shape[1] / self.nx
        yd = shape[0] / self.ny
        self.frame_number = frame_number
        if not self.ax:
            self.flag = 1

        if self.fig is None:
            self.flag = 1
            fig = plt.figure()
            self.fig = fig
            ax = plt.gca()
            self.ax = ax
            cid = self.fig.canvas.mpl_connect(
                'button_press_event', self.__onclick__)
            cid2 = self.fig.canvas.mpl_connect(
                'key_press_event', self.__onkeypress__)
            cid3 = self.fig.canvas.mpl_connect('close_event', self.__onclose__)

        if self.show_frame_number == 'on':
            title = self.default_title + ' %d' % self.frame_number
        else:
            title = self.default_title

        new_xlabels = parameters['inner_values']
        new_xlabels = [self.x_label_function(x) for x in new_xlabels]
        n_labels = len(new_xlabels)
        new_locs = np.linspace(xd / 2, shape[1] - xd / 2, n_labels)
        plt.xticks(new_locs, [self.x_label_format %
                   item for item in new_xlabels], rotation=90)
        self.ax.set_xlabel(self.default_xlabel)
        new_ylabels = parameters['outer_values']
        new_ylabels = [self.y_label_function(x) for x in new_ylabels]
        n_labels = len(new_ylabels)
        new_locs = np.linspace(yd / 2, shape[0] - yd / 2, n_labels)
        plt.yticks(new_locs, [self.y_label_format %
                   item for item in new_ylabels])

        self.ax.set_ylabel(self.default_ylabel)
        # if self.cb_ax is None:
        # self.add_colorbar()
        self.ax.imshow(self.data[self.frame_number])
        # self.cb.set_ticks(self.colorbar_ticks)
        # self.cb.set_ticklabels(self.colorbar_labels)
        self.ax.set_title(r'{}'.format(title))
        # self.cb_ax.set_title(self.colorbar_title)
        if self.invertedy == 1:
            self.ax.invert_yaxis()
        if self.grid == 'on':
            self.show_grid()
        if self.flag == 1:
            self.flag = 0
            self.show_markers()
        plt.gcf().subplots_adjust(bottom=0.15)  # preventing the x label from hiding
        plt.show()

    def to_movie(self):
        anim = FuncAnimation(self.fig, self.anim, frames=np.arange(1, 5))
        HTML(anim.to_html5_video())
        return anim

    def anim(self, i):
        self.img = self.data[i]
        plt.imshow(self.img)
        self.ax.set_title(i)
        plt.show()

    def __onclick__(self, event):
        shape = self.image_shape
        xd = shape[1] / self.nx
        yd = shape[0] / self.ny
        ex = event.xdata
        ey = event.ydata
        if ex is not None and ey is not None:  # check if the click was inside the image
            indx = math.floor(ex / xd)
            indy = math.floor(ey / yd)
            if indx in self.rect_indices[indy]:
                self.rect_indices[indy][indx].remove()
                del self.rect_indices[indy][indx]
                self.phase_diagram[indy][indx] = 0
                self.phase_diagramn[indy][indx] = None
            else:
                color = self.colormap(self.frame_number)
                rect = patches.Rectangle(
                    (indx * xd, indy * yd), xd, yd, linewidth=1, edgecolor=color, facecolor='none')
                self.rect_indices[indy][indx] = rect
                self.phase_diagram[indy][indx] = 1
                self.phase_diagramn[indy][indx] = self.frame_number
                self.ax.add_patch(rect)
            plt.show()

    def __onkeypress__(self, event):
        phase_diagram_not_none = [
            x for l in self.phase_diagramn for x in l if x is not None]
        shape = self.image_shape
        xd = shape[1] / self.nx
        yd = shape[0] / self.ny
        color_max = self.colorbar_max
        color_min = self.colorbar_min
        if event.key == 'e':
            self.frame_number = self.frame_number + 1
            if self.frame_number > self.max - 1:
                self.frame_number -= self.max + 1
        elif event.key == 'w':
            self.frame_number = self.frame_number - 1
            if self.frame_number < 0:
                self.frame_number += self.max + 1
        elif event.key == 'u':
            self.colorbar_ticks = [0, 1]
            self.colorbar_labels = ['off', 'on']
            if len(self.rectlist) == 0:
                for i in range(self.ny):
                    for j in range(self.nx):
                        color = self.colormap(
                            0) if self.phase_diagram[i][j] == 0 else self.colormap(1.0)
                        color = list(color)
                        color[3] = self.patch_alpha
                        rect = patches.Rectangle((j * xd, i * yd), xd, yd, linewidth=1, edgecolor=self.line_color,
                                                 facecolor=color)
                        if (self.patch_on is None) and (self.phase_diagram[i][j] == 1):
                            self.patch_on = rect
                        if (self.patch_off is None) and (self.phase_diagram[i][j] == 0):
                            self.patch_off = rect
                        self.hide_colorbar()

                        self.rectlist.append(rect)
                        self.ax.add_patch(rect)
            self.hide_colorbar()
            self.add_legend()

        elif event.key == 'y':
            self.remove_legend()
            # if phase_diagram_not_none:
            # self.show_colorbar()
            label_max = max(
                [y for x in self.phase_diagramn for y in x if y is not None])
            color_max = label_max if self.partial_max == 'on' and label_max > 0 else self.colorbar_max
            label_min = min(
                [y for x in self.phase_diagramn for y in x if y is not None])
            color_min = label_min if self.partial_min == 'on' else self.colorbar_min
            label_max = self.colorbar_ticklabel_function(label_max)
            label_min = self.colorbar_ticklabel_function(label_min)
            color_max = self.colorbar_ticklabel_function(color_max)
            color_min = self.colorbar_ticklabel_function(color_min)
            if color_min > color_max:
                color_max, color_min = color_min, color_max
            print(self.colorbar_max, self.colorbar_min, color_max, color_min)
            self.colorbar_max = self.colorbar_ticklabel_function(
                self.colorbar_max)
            self.colorbar_min = self.colorbar_ticklabel_function(
                self.colorbar_min)
            # self.colorbar_ticks = [0, 0.2, 0.4, 0.6, 0.8, 1]
            self.colorbar_labels = [format(
                (color_min + x * (color_max - color_min)),
                ".2f") for x in self.colorbar_ticks]
            print(self.colorbar_labels)
            # self.show_colorbar()
            self.add_colorbar()
            if len(self.rectlistn) == 0:
                for i in range(self.ny):
                    for j in range(self.nx):
                        multiplier = self.colorbar_max / \
                            abs((color_max - color_min)
                                ) if color_max != color_min else 1
                        phase_value = self.phase_diagramn[i][j]
                        #value = math.floor((phase_value - color_min) * multiplier) if phase_value is not None else None

                        value = self.colorbar_ticklabel_function(
                            phase_value) if phase_value is not None else None
                        self.norm = Normalize(vmin=color_min, vmax=color_max)
                        color = self.colormap(
                            self.norm(value)) if value is not None else self.none_color
                        color = list(color)
                        color[3] = self.patch_alpha
                        #print(color_min,color_max,value,color,norm(value) if value is not None else None)
                        # print(self.phase_diagramn[i][j],value)
                        rect = patches.Rectangle((j * xd, i * yd), xd, yd, linewidth=1,
                                                 edgecolor=self.line_color, facecolor=color)
                        self.rectlistn.append(rect)
                        self.ax.add_patch(rect)
        elif event.key == 't':
            self.patch_on = None
            self.patch_off = None
            for item in self.rectlist:
                item.remove()
            self.rectlist = list()
            for item in self.rectlistn:
                item.remove()
            self.rectlistn = list()
            self.colorbar_ticks = [0, 0.2, 0.4, 0.6, 0.8, 1]
            self.colorbar_labels = [format(x*self.max, ".2f")
                                    for x in self.colorbar_ticks]
            self.remove_legend()
            self.hide_colorbar()
            # if phase_diagram_not_none:
            # self.add_colorbar()
            # self.show_colorbar()

        self.show(self.frame_number)
        plt.show()

    def __onclose__(self, event):
        self.fig = None
        self.ax = None
        self.cb_ax = None
        self.cb = None
        self.grid_list = list()
