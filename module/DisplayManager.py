# -*- coding: utf-8 -*-
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepTools import breptools_Write, breptools_Read, breptools_Triangulation
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.TopoDS import TopoDS_Face, TopoDS_Shape, TopoDS_Edge, TopoDS_Solid
from PyQt5.QtWidgets import QFileDialog

from module import qtDisplay
from OCC.Extend.DataExchange import read_step_file,read_iges_file,read_stl_file
from module import assemble


class DisplayManager(object):
    def __init__(self,widget):
        self.canve=qtDisplay.qtViewer3d(widget)
        self.widget=widget
        self.part_maneger_core_dict={}
    def Dispalyshape(self):
        self.canve._display.DisplayColoredShape()

    def Open_part(self):
        try:
            self.chose_document = QFileDialog.getOpenFileName(self.widget, '打开文件', './',
                                                              " STP files(*.stp , *.step);;(*.iges);;(*.stl)")  # 选择转换的文价夹
            filepath = self.chose_document[0]  # 获取打开文件夹路径
            # 判断文件类型 选择对应的导入函数
            end_with = str(filepath).lower()
            if end_with.endswith(".step") or end_with.endswith("stp"):
                self.import_shape,assemble_relation_list,DumpToString =assemble.read_step_file_with_names_colors(filepath)

                for shpt_lbl_color in self.import_shape:
                    label, c,property= self.import_shape[shpt_lbl_color]
                    #color=Quantity_Color(c.Red(),c.Green(), c.Blue(),Quantity_TOC_RGB)
                    if  not isinstance(shpt_lbl_color,TopoDS_Solid):#排除非solid
                        continue
                    return_shape=self.canve._display.DisplayShape(shpt_lbl_color, color=Quantity_Color(c.Red(),
                                                                                     c.Green(),
                                                                                     c.Blue(),
                                                                                     Quantity_TOC_RGB))
                    self.part_maneger_core_dict[label]=return_shape
                self.widget.statusbar.showMessage("状态：打开成功")  ###
                self.widget.statusBar().showMessage('状态：软件运行正常')
                return assemble_relation_list
            elif end_with.endswith(".iges") or end_with.endswith(".igs"):
                self.import_shape = read_iges_file(filepath)
                self.widget.statusbar.showMessage("状态：打开成功")  ###
                self.widget.statusBar().showMessage('状态：软件运行正常')
            elif end_with.endswith(".stl") or end_with.endswith(".stl"):
                self.import_shape = read_stl_file(filepath)
                breptools_Triangulation()
                breptools_Write(self.import_shape, 'box.brep')
                read_box = TopoDS_Shape()
                builder = BRep_Builder()
                breptools_Read(read_box, 'box.brep', builder)
                self.canve._display.DisplayShape(read_box)
                self.widget.statusbar.showMessage("状态：打开成功")  ###
                self.widget.statusBar().showMessage('状态：软件运行正常')

        except Exception as e:
            print(e)

    def Import_stp(self):
        try:
            self.chose_document = QFileDialog.getOpenFileName(self.widget, '打开文件', './',
                                                              " STP files(*.stp , *.step);;(*.iges);;(*.stl)")  # 选择转换的文价夹
            filepath = self.chose_document[0]  # 获取打开文件夹路径
            # 判断文件类型 选择对应的导入函数
            end_with = str(filepath).lower()
            if end_with.endswith(".step") or end_with.endswith("stp"):
                self.import_shape,assemble_relation_list =assemble.read_step_file_with_names_colors(filepath)
                print(9999)
                for shpt_lbl_color in self.import_shape:
                    label, c,property= self.import_shape[shpt_lbl_color]
                    #color=Quantity_Color(c.Red(),c.Green(), c.Blue(),Quantity_TOC_RGB)
                    return_shape=self.canve._display.DisplayShape(shpt_lbl_color, color=Quantity_Color(c.Red(),
                                                                                     c.Green(),
                                                                                     c.Blue(),
                                                                                     Quantity_TOC_RGB))
                    self.part_maneger_core_dict[label]=return_shape
            print(self.part_maneger_core_dict)
            self.widget.statusbar.showMessage("状态：打开成功")  ###
            self.widget.statusBar().showMessage('状态：软件运行正常')
            return assemble_relation_list
        except Exception as e:
            print(e)
    def Import_iges(self):
        pass
        try:
            self.chose_document = QFileDialog.getOpenFileName(self.widget, '打开文件', './',
                                                              " STP files(*.stp , *.step);;(*.iges);;(*.stl)")  # 选择转换的文价夹
            filepath = self.chose_document[0]  # 获取打开文件夹路径
            # 判断文件类型 选择对应的导入函数
            end_with = str(filepath).lower()
            if end_with.endswith("iges"):
                self.import_shape = read_iges_file(filepath)
            self.widget.statusbar.showMessage("状态：打开成功")  ###
            self.widget.statusBar().showMessage('状态：软件运行正常')

        except:
            pass
    def Import_stl(self):
        try:
            self.chose_document = QFileDialog.getOpenFileName(self.widget, '打开文件', './',
                                                              " STP files(*.stp , *.step);;(*.iges);;(*.stl)")  # 选择转换的文价夹
            filepath = self.chose_document[0]  # 获取打开文件夹路径
            # 判断文件类型 选择对应的导入函数
            end_with = str(filepath).lower()
            if end_with.endswith("stl"):
                self.import_shape = read_stl_file(filepath)
            self.widget.statusbar.showMessage("状态：打开成功")  ###
            self.widget.statusBar().showMessage('状态：软件运行正常')
        except:
            pass


