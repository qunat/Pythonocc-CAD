# -*- coding: utf-8 -*-
# !/usr/bin/env python

import logging,os
import time
from OCC.Core.BRep import BRep_Tool
from OCC.Core.Geom import Geom_Circle
from OCC.Display.OCCViewer import OffscreenRenderer
from OCC.Display.backend import load_backend, get_qt_modules
from PyQt5 import QtCore, QtWidgets, Qt
from module import Process_message, Process_message_word
from OCC.Extend.TopologyUtils import TopologyExplorer
import re,copy
from OCC.Core.AIS import AIS_Shape, AIS_RadiusDimension, AIS_AngleDimension, AIS_LengthDimension
from OCC.Core.TopAbs import (TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX,
                             TopAbs_SHELL, TopAbs_SOLID)
from ui import MainGui

# ------------------------------------------------------------开始初始化环境
log = logging.getLogger(__name__)


def check_callable(_callable):
    if not callable(_callable):
        raise AssertionError("The function supplied is not callable")


backend_str = None
size = [850, 873]
display_triedron = True
background_gradient_color1 = [212, 212, 212]
background_gradient_color2 = [128, 128, 128]



if os.getenv("PYTHONOCC_OFFSCREEN_RENDERER") == "1":
    # create the offscreen renderer
    offscreen_renderer = OffscreenRenderer()
    def do_nothing(*kargs, **kwargs):
        """ takes as many parameters as you want,
        ans does nothing
        """
        pass
    def call_function(s, func):
        """ A function that calls another function.
        Helpfull to bypass add_function_to_menu. s should be a string
        """
        check_callable(func)
        log.info("Execute %s :: %s menu fonction" % (s, func.__name__))
        func()
        log.info("done")
    # returns empty classes and functions
used_backend = load_backend(backend_str)
log.info("GUI backend set to: %s", used_backend)
# ------------------------------------------------------------初始化结束
from PyQt5.QtGui import QPixmap, QFont, QBrush, QMovie, QIcon, QCursor
QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()
from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Builder, TopoDS_Compound, topods_CompSolid, TopoDS_Edge, TopoDS_Face,\
TopoDS_Vertex

from OCC.Extend.DataExchange import read_iges_file, read_step_file, read_stl_file, write_step_file, write_stl_file, \
    write_iges_file
from PyQt5.QtWidgets import QComboBox, QPushButton, QHBoxLayout, QMdiArea, QMdiSubWindow, QTextEdit, QApplication, \
    QFileDialog, QProgressBar, QMessageBox, QTableView, QDockWidget, QListWidget
import sys
from  module import ShowGui,ProcessBar

# SET QSS
Stylesheet = """
#MainWindow {

    border-radius: 10px;
}
#closeButton {
    min-width: 36px;
    min-height: 36px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
#closeButton:hover {
    color: white;
    background: red;
}
"""


class Mywindown(QtWidgets.QMainWindow, ShowGui.Ui_MainWindow,MainGui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Mywindown, self).__init__(parent)
        # 3D显示设置
        self.setWindowTitle("pythonocc-CAD")
        # ----------------------------------------------------------------------------------
        self.sinal = 0
        self.tabWidget_5.currentChanged['int'].connect(self.Refresh)  # 切换时刷新
        self.Out_put_stp.triggered.connect(self.Output_stp_data)
        self.Out_put_iges.triggered.connect(self.Output_iges_data)
        self.Out_put_stl.triggered.connect(self.Output_stl_data)

        # -------------------------------------------------------------------------------------视图操作
        self.Quit.triggered.connect(self.Quit_)
        self.actionView_Right.triggered.connect(self.View_Right)
        self.actionView_Left.triggered.connect(self.View_Left)
        self.actionView_Top.triggered.connect(self.View_Top)
        self.actionView_Bottom.triggered.connect(self.View_Bottom)
        self.actionView_Front.triggered.connect(self.View_Front)
        self.actionView_Iso.triggered.connect(self.View_Iso)
        self.action_Fitall.triggered.connect(self.View_fitall)


        # -------------------------------------------------------------------------------------测量菜单
        self.Measure_distance.triggered.connect(self.Measure_distance_fun)
        self.Measure_diameter.triggered.connect(self.Measure_diameter_fun)
        # --------------------------------------------------------------------------------------显示软件版本
        self.AboutVision.triggered.connect(self.Vision)
        self.AboutDownload.triggered.connect(self.AboutDownload_)

    def View_Bottom(self):
        pass
        self.canva._display.View_Bottom()

    def View_Front(self):
        pass
        self.canva._display.View_Front()

    def View_Iso(self):
        pass
        self.canva._display.View_Iso()

    def View_Left(self):
        pass
        self.canva._display.View_Left()

    def View_Right(self):
        pass
        self.canva._display.View_Right()

    def View_Top(self):
        pass
        self.canva._display.View_Top()

    def View_fitall(self):
        pass
        self.canva._display.FitAll()

    def doubleClickedHandle(self, index):
        text = self.model().item(index.row(), 0).text()
        self.doubleClickedItem.emit(text)

    def outSelect(self, Item=None):
        if Item == None:
            return

    def Refresh(self):
        self.canva._display.Repaint()
        self.graphicsView.show()



    def Translation_Assemble(self):  # 转换为装配体
        pass
        try:
            self.new_build = TopoDS_Builder()  # 建立一个TopoDS_Builder()
            self.New_Compound = TopoDS_Compound()  # 定义一个复合体
            self.new_build.MakeCompound(self.New_Compound)  # 生成一个复合体DopoDS_shape
            for shape in self.aCompound:
                self.new_build.Add(self.New_Compound, shape)
            self.aCompound = self.New_Compound
        except:
            pass

    def Assemble_Rename(self):
        try:
            Part_NO = 0
            with open(self.save_part_path, "r") as f:
                words = f.read()
                f.close()
            p = re.compile(r"Open CASCADE STEP translator 7.4 1.\d{1,2}")  # h获取子装配体名称
            assemble_part_name_list = p.findall(words)
            for i in range(0, (len(assemble_part_name_list)), 2):
                pass
                new_name = self.filename + "-" + str(Part_NO)
                words = words.replace(assemble_part_name_list[i], new_name)
                Part_NO += 1
            with open(self.save_part_path, "w+") as f:  # 重新写入stp
                f.write(words)
                f.close()
                # print("succeed")


        except:
            pass

    def Output_stp_data(self):  # 将数据转换成stp并导出
        try:
            pass
            self.Translation_Assemble()
            path = "../" + self.filename
            fileName, ok = QFileDialog.getSaveFileName(self, "文件保存", path, "All Files (*) (*.step)")
            write_step_file(self.aCompound, fileName)
            self.save_part_path = fileName
            self.Assemble_Rename()
            self.statusbar.showMessage("零件导出成功")

        except:
            pass
            self.statusbar.showMessage("错误：没用模型可以导出")

    def Output_iges_data(self):  # 将数据转换成iges并导出
        try:
            pass
            self.Translation_Assemble()
            path = "./" + self.filename
            fileName, ok = QFileDialog.getSaveFileName(self, "文件保存", path, "All Files (*) (*.iges)")
            write_iges_file(self.aCompound, fileName)
            self.save_part_path = fileName
            self.statusbar.showMessage("零件导出成功")

        except:
            pass
            self.statusBar.showMessage('错误：没用模型可以导出')

    def Output_stl_data(self):  # stl
        try:
            pass
            self.Translation_Assemble()
            path = "./" + self.filename
            fileName, ok = QFileDialog.getSaveFileName(self, "文件保存", path, "All Files (*) (*.iges)")
            write_stl_file(self.aCompound, fileName)
            self.save_part_path = fileName
            self.statusbar.showMessage("零件导出成功")

        except:
            pass
            self.statusBar.showMessage('错误：没用模型可以导出')

    def centerOnScreen(self):
        '''Centers the window on the screen.'''
        resolution = QtWidgets.QApplication.desktop().screenGeometry()
        x = (resolution.width() - self.frameSize().width()) / 2
        y = (resolution.height() - self.frameSize().height()) / 2
        self.move(x, y)

    def Measure_distance_fun(self):
        pass
        self.measure_signale = 1  # 测量长度
        self.measure_shape_list = []
        self.canva._display.SetSelectionModeNeutral()
        self.canva._display.SetSelectionMode(TopAbs_FACE)  # 设置选择模式
        self.canva._display.SetSelectionMode(TopAbs_EDGE)  # 设置选择模式
        self.canva._display.SetSelectionMode(TopAbs_VERTEX) # 设置选择模式
        self.statusbar.showMessage("请选择要测量距离的两个面或者两条边")

    def Measure_diameter_fun(self):
        pass
        self.measure_signale = 2  # 测量直径
        self.measure_shape_list = []
        self.canva._display.SetSelectionModeNeutral()
        self.canva._display.SetSelectionMode(TopAbs_FACE)  # 设置选择模式
        self.canva._display.SetSelectionMode(TopAbs_EDGE)  # 设置选择模式
        self.statusbar.showMessage("请选择圆弧或者圆弧面")
        # print("选择面")
    def line_clicked(self, shp, *kwargs):
        """ This function is called whenever
        """
        try:
            if self.measure_signale == 1:
                for shape in shp:  # this should be a TopoDS_Edge
                    # print(type(shape))
                    if shape.IsNull():
                        continue
                    elif isinstance(shape,TopoDS_Vertex):
                        point = BRep_Tool.Pnt(shape)
                        self.measure_shape_list.append(point)
                    elif isinstance(shape,TopoDS_Edge):
                        select = BRep_Tool.Curve(shape)[0]
                        if not Geom_Circle.DownCast(select):
                            pass
                        else:
                            possible_circle = Geom_Circle.DownCast(select)
                            # 从Geom_Curve向下类型转换为Geom_Circle
                            circle_ = possible_circle.Circ()
                            # 得到gp_Circ类型的圆
                            loc = circle_.Location()  # 圆心， gp_Pnt 类型
                            self.measure_shape_list.append(loc)

                    else:
                        self.measure_shape_list.append(shape)

                    if len(self.measure_shape_list) == 2:
                        try:
                            if isinstance(self.measure_shape_list[0],gp_Pnt):
                                distance=self.measure_shape_list[0].Distance(self.measure_shape_list[1])
                                measure_result=(distance)

                            else:
                                am = AIS_LengthDimension(self.measure_shape_list[0], self.measure_shape_list[1])
                                # self.canva._display.Context.Display(am,True)
                                measure_result = am.GetValue()

                            measure_result = "测量结果:" + "{:2.2f}".format(measure_result) + "mm"
                            reply = QMessageBox.information(self,  # 使用infomation信息框
                                                            "测量结果",
                                                            str(measure_result),
                                                            QMessageBox.Yes)
                        except:
                            self.statusbar.showMessage("必须选择同样的元素")
                        finally:
                            self.measure_shape_list.clear()

                    elif len(self.measure_shape_list) > 2:
                        pass
                        self.measure_shape_list.clear()


            elif self.measure_signale == 2:#测量直径
                for shape in shp:  # this should be a TopoDS_Edge
                    if shape.IsNull():
                        continue
                    else:
                        self.measure_shape_list.append(shape)

                    if len(self.measure_shape_list) == 1:
                        try:
                            if isinstance(self.measure_shape_list,TopoDS_Edge):
                                select = BRep_Tool.Curve(self.measure_shape_list[0])[0]
                                if not Geom_Circle.DownCast(select):
                                    pass
                                else:
                                    possible_circle = Geom_Circle.DownCast(select)
                                    # 从Geom_Curve向下类型转换为Geom_Circle
                                    circle_ = possible_circle.Circ()
                                    # 得到gp_Circ类型的圆
                                    loc = circle_.Location()  # 圆心， gp_Pnt 类型
                                    radius = circle_.Radius()  # 半径
                                    measure_result = radius * 2
                                # am = AIS_RadiusDimension(self.measure_shape_list[0], self.measure_shape_list[1])
                            elif isinstance(self.measure_shape_list[0],TopoDS_Face):
                                for e in TopologyExplorer(self.measure_shape_list[0]).edges():
                                    select = BRep_Tool.Curve(e)[0]
                                    if not Geom_Circle.DownCast(select):
                                        pass
                                    else:
                                        possible_circle = Geom_Circle.DownCast(select)  # 从Geom_Curve向下类型转换为Geom_Circle
                                        circle_ = possible_circle.Circ()  # 得到gp_Circ类型的圆
                                        loc = circle_.Location()  # 圆心， gp_Pnt 类型
                                        radius = circle_.Radius()  # 半径
                                        # print(loc.X(), loc.Y(), loc.Z(), radius)
                                        #ls_point = [loc.X(), loc.Y(), loc.Z(), radius]
                                        measure_result = radius * 2

                                        break




                            measure_result = "测量结果:直径" + "{:2.2f}".format(measure_result) + "mm"
                            reply = QMessageBox.information(self,  # 使用infomation信息框
                                                            "测量结果",
                                                            str(measure_result),
                                                            QMessageBox.Yes)
                        except:
                            self.statusbar.showMessage("必须选择同样的元素")
                        finally:
                            self.measure_shape_list.clear()

                    elif len(self.measure_shape_list) > 1:
                            pass
                            self.measure_shape_list.clear()
        except:
            pass




    def Process_message(self):
        self.process_message = Process_message()
        self.process_message.show()
        QApplication.processEvents()

    def Quit_(self):  # 退出
        self.close()

    def Vision(self):
        pass
        self.new_vison.show()

    def AboutDownload_(self):
        self.new_AboutDownload.show()



class Process_message(QtWidgets.QMainWindow, Process_message.Ui_Form):  # 零件加载过程界面
    def __init__(self, parent=None):
        super(Process_message, self).__init__(parent)
        self.setupUi(self)
        # self.pushButton=QtWidgets.QPushButton()
        # self.pushButton.setGeometry(0,0,10,10)

    def process_message_show(self):
        pass
        self.label.setObjectName("label")
        self.gif = QMovie(':/picture/icons/loading.gif')
        self.label.setMovie(self.gif)
        self.gif.start()
        self.show()


class Process_message_word(QtWidgets.QMainWindow, Process_message_word.Ui_Form):  # 零件加载过程界面
    def __init__(self, parent=None):
        super(Process_message_word, self).__init__(parent)
        self.setupUi(self)
        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setGeometry(0, 0, 10, 10)




def line_clicked(shp, *kwargs):
    """ This function is called whenever a line is selected
    """

# following couple of lines is a tweak to enable ipython --gui='qt'
if __name__ == '__main__':
    app = QtWidgets.QApplication.instance()  # checks if QApplication already exists
    if not app:  # create QApplication if it doesnt exist
        app = QtWidgets.QApplication(sys.argv)
    # 启动界面
    try:
        splash = QtWidgets.QSplashScreen(QtGui.QPixmap("./Pic/setup_pic.png"))  # 启动图片设置
        splash.show()
        splash.showMessage("软件启动中......")
    except:
        pass
    # --------------------
    win = Mywindown()
    win.show()
    win.centerOnScreen()
    win.Displayshape_core.canve.InitDriver()
    win.resize(size[0], size[1])
    win.Displayshape_core.canve.qApp = app

    display = win.Displayshape_core.canve._display
    display.display_triedron()
    display.register_select_callback(win.line_clicked)
    if background_gradient_color1 and background_gradient_color2:
        # background gradient
        display.set_bg_gradient_color(background_gradient_color1, background_gradient_color2)
    win.raise_()  # make the application float to the top
    win.showMaximized()

    try:
        splash.finish(win)
    except:
        pass
    app.exec_()
