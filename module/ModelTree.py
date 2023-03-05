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
		self.tree_Node_dict={}
		self.root_dict={}
		self.node_dict={}

		# 设置根节点
		self.history_model_root = QTreeWidgetItem(self.tree)
		self.history_model_root.setText(0, '历史模型记录')
		self.history_model_root.setIcon(0, QIcon('sync.ico'))
		self.history_model_root.setCheckState(0, Qt.Checked)

		self.wcs_root = QTreeWidgetItem(self.history_model_root)
		self.wcs_root.setText(0, '坐标系')
		self.wcs_root.setIcon(0, QIcon('sync.ico'))
		self.wcs_root.setCheckState(0, Qt.Checked)

		# todo 优化2 设置根节点的背景颜色
		#brush_red = QBrush(Qt.red)
		#root.setBackground(0, brush_red)
		#brush_blue = QBrush(Qt.blue)
		#root.setBackground(1, brush_blue)
		# 设置树形控件的列的宽度
		self.tree.setColumnWidth(0, 150)
		# 加载根节点的所有属性与子控件
		# self.tree.addTopLevelItem(root)

	def Create_tree_NodeList(self,root_dict={}):
		for part_property in root_dict.values():
			if  part_property.struct=="ASSEMBLY":
				root_order=part_property.order
				root_name=part_property.name
				NodeList = ["father_root"]
				NodeList.append(root_name)
				NodeList.append(part_property.order)
			elif part_property.order[0:len(part_property.order)-2]==root_order:
				NodeList.append(part_property.order)
				self.node_dict[root_order] = NodeList
				
		self.root_dict=root_dict
		print(self.node_dict)
		print(self.node_dict["0:1:1:1"])
		self.Create_ModelTree(self.node_dict["0:1:1:1"])
				
	def Create_ModelTree(self,Nodelist=[]):
		# 设置总装配体根节点/子装配体根节点
		print("start")
		if Nodelist[2]=="0:1:1:1":
			self.tree_root_dict[Nodelist[1]] = QTreeWidgetItem(self.history_model_root)
		else:
			
			self.tree_root_dict[Nodelist[1]] = QTreeWidgetItem(self.tree_root_dict[Nodelist[0]])
		father_root=Nodelist[1]
		print("enter")
		#设置子节点
		for order in Nodelist[3:-1]:
			print(order,"ok")
			if self.root_dict[order].refer == None:
				if self.root_dict[order].struct == "ASSEMBLY":
						nodelist=self.node_dict[order]
						nodelist[0]=father_root
						self.Create_ModelTree(self.node_dict[order])
				else:
						# 设置子节点1
						self.tree_root_child_dict[self.root_dict[order].name] = QTreeWidgetItem(
							self.tree_root_dict[Nodelist[1]])
						self.tree_root_child_dict[self.root_dict[order].name].setText(0, self.root_dict[order].name)
						self.tree_root_child_dict[self.root_dict[order].name].setText(1, 'part')
						self.tree_root_child_dict[self.root_dict[order].name].setIcon(0, QIcon('screenruler.ico'))
						if self.root_dict[order].struct == "PART" and Nodelist.index(order) == len(Nodelist):
							break
						# todo 优化1 设置节点的状态
						# self.tree_root_child_dict[part_property["name"]].setCheckState(0, Qt.Checked)
			else:
				old_order=order
				order = self.root_dict[order].refer
				print(order,0000000000,self.root_dict[order].struct)
				if self.root_dict[order].struct == "ASSEMBLY":
					nodelist = self.node_dict[order]
					print(99999999,nodelist)
					nodelist[0] = father_root
					print(88888888,self.node_dict[order])
					self.Create_ModelTree(self.node_dict[order])
				else:
					# 设置子节点1
					self.tree_root_child_dict[self.root_dict[order].name] = QTreeWidgetItem(
						self.tree_root_dict[Nodelist[1]])
					self.tree_root_child_dict[self.root_dict[order].name].setText(0, self.root_dict[order].name)
					self.tree_root_child_dict[self.root_dict[order].name].setText(1, 'part')
					self.tree_root_child_dict[self.root_dict[order].name].setIcon(0, QIcon('screenruler.ico'))
					print(Nodelist)
					if self.root_dict[order].struct=="PART" and Nodelist.index(old_order)==len(Nodelist)-1:
						print("跳出递归")
						break
			# todo 优化1 设置节点的状态
			# self.tree_root_child_dict[part_property["name"]].setCheckState(0, Qt.Checked)
			
			

					
					
	def Create_Child(self):
		pass
	def Updata_Root(self):
		pass
	def Updata_Child(self):
		pass

