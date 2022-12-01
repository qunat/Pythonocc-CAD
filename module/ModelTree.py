# _*_ coding: utf-8 _*_
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QKeySequence as QKSec
from PyQt5.QtGui import QIcon,QBrush
from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget


class ModelTree(QtWidgets.QWidget):
    def __init__(self):
        super(ModelTree, self).__init__()
        self.tree = QTreeWidget()
        self.tree.expandAll()# 节点全部展开
        self.tree.setStyle(QtWidgets.QStyleFactory.create('windows'))#有加号
        self.tree.setColumnCount(1)# 设置列数
        self.tree.setHeaderLabels(['控件', '值'])# 设置树形控件头部的标题
        self.tree_root_dict={}
        self.tree_root_child_dict = {}

        # 设置根节点
        self.root = QTreeWidgetItem(self.tree)
        self.root.setText(0, '零件')
        self.root.setIcon(0, QIcon('sync.ico'))
        self.root.setCheckState(0, Qt.Checked)

        wcs_root = QTreeWidgetItem(self.root)
        wcs_root.setText(0, '坐标系')
        wcs_root.setIcon(0, QIcon('sync.ico'))
        wcs_root.setCheckState(0, Qt.Checked)

        # todo 优化2 设置根节点的背景颜色
        #brush_red = QBrush(Qt.red)
        #root.setBackground(0, brush_red)
        #brush_blue = QBrush(Qt.blue)
        #root.setBackground(1, brush_blue)
        # 设置树形控件的列的宽度
        self.tree.setColumnWidth(0, 150)
        # 加载根节点的所有属性与子控件
        # self.tree.addTopLevelItem(root)


    def Create_ModelTree(self,list):
        # 设置根节点
        for part_property in list:
            if part_property["isassemble"]==True:
                assamble_name=part_property["name"]
                self.tree_root_dict[part_property["name"]] = QTreeWidgetItem(self.root)
                self.tree_root_dict[part_property["name"]].setText(0, part_property["name"])
                self.tree_root_dict[part_property["name"]].setIcon(0, QIcon('sync.ico'))
                # todo 优化2 设置根节点的背景颜色
                brush_red = QBrush(Qt.red)
                #self.tree_root_dict[part_property["name"]].setBackground(0, brush_red)
                brush_blue = QBrush(Qt.blue)
                #self.tree_root_dict[part_property["name"]].setBackground(1, brush_blue)
                #self.tree_root_dict[part_property["name"]].setColumnWidth(0, 150)
            elif part_property["isassemble"]==False and list[0]["isassemble"]==True:
                # 设置子节点1
                self.tree_root_child_dict[part_property["name"]] = QTreeWidgetItem()
                self.tree_root_child_dict[part_property["name"]].setText(0, part_property["name"])
                self.tree_root_child_dict[part_property["name"]].setText(1, 'part')
                self.tree_root_child_dict[part_property["name"]].setIcon(0, QIcon('screenruler.ico'))
                # todo 优化1 设置节点的状态
                self.tree_root_child_dict[part_property["name"]].setCheckState(0, Qt.Checked)
                self.tree_root_dict[assamble_name].addChild(self.tree_root_child_dict[part_property["name"]])
            elif part_property["isassemble"]==False and list[0]["isassemble"]==False:#非装配体机构
                # 设置子节点1
                self.tree_root_dict[part_property["name"]] = QTreeWidgetItem(self.root)
                self.tree_root_dict[part_property["name"]].setText(0, part_property["name"])
                self.tree_root_dict[part_property["name"]].setIcon(0, QIcon('sync.ico'))
                self.tree_root_dict[part_property["name"]].setCheckState(0, Qt.Checked)

    def Create_Child(self):
        pass
    def Updata_Root(self):
        pass
    def Updata_Child(self):
        pass

