"""
Opens a single PyQt window displaying the ycam image with counts.
"""

import numpy as np
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import sys
from initialize_ycam import cam


# Interpret image data as row-major instead of col-major
pg.setConfigOptions(imageAxisOrder='row-major')

app = QtGui.QApplication([])
plot = pg.PlotItem()

# Create window with ImageView widget
win = QtGui.QMainWindow()
win.resize(800, 800)
imv = pg.ImageView(view=plot)
win.setCentralWidget(imv)
win.show()
win.setWindowTitle('pyqtgraph example: ImageView')
marqueeBox_x1, marqueeBox_x2 = 300, 625
marqueeBox_y1, marqueeBox_y2 = 230, 620
normBox_x1, normBox_x2 = 220, 280
normBox_y1, normBox_y2 = 510, 570
imv_v = imv.getView()


def draw_box(imv_v, x1, x2, y1, y2):
    imv_v.addItem(pg.PlotCurveItem(x=[x1, x1],
                                   y=[y1, y2]))
    imv_v.addItem(pg.PlotCurveItem(x=[x2, x2],
                                   y=[y1, y2]))
    imv_v.addItem(pg.PlotCurveItem(x=[x1, x2],
                                   y=[y1, y1]))
    imv_v.addItem(pg.PlotCurveItem(x=[x1, x2],
                                   y=[y2, y2]))


draw_box(imv_v, marqueeBox_x1, marqueeBox_x2,
         marqueeBox_y1, marqueeBox_y2)
draw_box(imv_v, normBox_x1, normBox_x2,
         normBox_y1, normBox_y2)


def update():
    try:
        im = cam.snap()
        marquee_im = im[marqueeBox_y1:marqueeBox_y2,
                        marqueeBox_x1:marqueeBox_x2]
        norm_im = im[normBox_y1:normBox_y2, normBox_x1:normBox_x2]
        marquee_counts, norm_counts = np.sum(marquee_im), np.sum(norm_im)
        ratio_counts = marquee_counts / norm_counts
        labelStyle = {'color': '#FFF', 'font-size': '70px'}
        plot.setLabel(
            axis='bottom', text='marquee/norm: \n{:.2e}'.format(ratio_counts), **labelStyle)
        imv.setImage(im)
    except Exception as e:
        print(e)
        print('exiting gracefully')


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        print('closing connection to camera...')
        cam.close()