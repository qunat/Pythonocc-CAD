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
		self.tree.setColumnCount(2)# 设置列数
		self.tree.setHeaderLabels(['名称', '附件',"最新"])# 设置树形控件头部的标题
		self.tree.setAlternatingRowColors(True)
		#self.tree.setRootIsDecorated(False)
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
		
		#基准面X
		self.datum_root_x = QTreeWidgetItem(self.history_model_root)
		self.datum_root_x.setText(0, 'X基准面')
		self.datum_root_x.setIcon(0, QIcon('./icons/datumplane.png'))
		self.datum_root_x.setCheckState(0, Qt.Checked)
		# 基准面Y
		self.datum_root_y = QTreeWidgetItem(self.history_model_root)
		self.datum_root_y.setText(0, 'Y基准面')
		self.datum_root_y.setIcon(0, QIcon('./icons/datumplane.png'))
		self.datum_root_y.setCheckState(0, Qt.Checked)
		# 基准面Z
		self.datum_root_z = QTreeWidgetItem(self.history_model_root)
		self.datum_root_z.setText(0, 'Z基准面')
		self.datum_root_z.setIcon(0, QIcon('./icons/datumplane.png'))
		self.datum_root_z.setCheckState(0, Qt.Checked)
		

		# todo 优化2 设置根节点的背景颜色
		#brush_red = QBrush(Qt.red)
		#self.history_model_root.setBackground(0, brush_red)
		#brush_blue = QBrush(Qt.blue)
		#root.setBackground(1, brush_blue)
		# 设置树形控件的列的宽度
		self.tree.setColumnWidth(0, 250)
		# 加载根节点的所有属性与子控件
		# self.tree.addTopLevelItem(root)
	def Clear_tree_NodeList(self):
		item = self.tree.currentItem()
		# 固定根节点
		root = self.tree.invisibleRootItem()
		for item in self.tree.selectedItems():
			(item.parent() or root).removeChild(item)

	def Create_tree_NodeList(self,root_dict={}):
		root_order=None
		for part_property in root_dict.values():
			if part_property.name==None:
				continue
			elif  part_property.struct=="ASSEMBLY":
				root_order=part_property.order
				root_name=part_property.name
				NodeList = ["father_root"]
				NodeList.append(root_name)
				NodeList.append(part_property.order)
				
			elif part_property.order[0:part_property.order.rfind(":")]==root_order:
				NodeList.append(part_property.order)
				self.node_dict[root_order] = NodeList
				
		self.root_dict=root_dict
		self.Create_ModelTree(self.node_dict["0:1:1:1"])
		self.tree.expandAll()  # 节点全部展开


				
	def Create_ModelTree(self,Nodelist=[]):
		# 设置总装配体根节点/子装配体根节点
		#print("start")
		if Nodelist[2]=="0:1:1:1":
			self.tree_root_dict[Nodelist[1]] = QTreeWidgetItem(self.history_model_root)
			self.tree_root_dict[Nodelist[1]].setText(0, Nodelist[1])
			self.tree_root_dict[Nodelist[1]].setIcon(0, QIcon('screenruler.ico'))
			self.tree_root_dict[Nodelist[1]].setCheckState(0, Qt.Checked)
			
		else:
			
			self.tree_root_dict[Nodelist[1]] = QTreeWidgetItem(self.tree_root_dict[Nodelist[0]])
			self.tree_root_dict[Nodelist[1]].setText(0, Nodelist[1])
			self.tree_root_dict[Nodelist[1]].setIcon(0, QIcon('screenruler.ico'))
			self.tree_root_dict[Nodelist[1]].setCheckState(0, Qt.Checked)
		father_root=Nodelist[1]
		#print("enter",Nodelist[3:len(Nodelist)])
		#设置子节点
		print(Nodelist)
		for order in Nodelist[3:len(Nodelist)]:
			#print(order,"ok")
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
						self.tree_root_child_dict[self.root_dict[order].name].setIcon(0, QIcon('screenruler.ico'))
						self.tree_root_child_dict[self.root_dict[order].name].setCheckState(0, Qt.Checked)
						if self.root_dict[order].struct == "PART" and Nodelist.index(order) == len(Nodelist)-1:
							break
						# todo 优化1 设置节点的状态
						# self.tree_root_child_dict[part_property["name"]].setCheckState(0, Qt.Checked)
			else:
				old_order=order
				order = self.root_dict[order].refer
				if self.root_dict[order].struct == "ASSEMBLY":
					nodelist = self.node_dict[order]
					nodelist[0] = father_root
					self.Create_ModelTree(self.node_dict[order])
				else:
					# 设置子节点1
					self.tree_root_child_dict[self.root_dict[order].name] = QTreeWidgetItem(self.tree_root_dict[Nodelist[1]])
					self.tree_root_child_dict[self.root_dict[order].name].setText(0, self.root_dict[order].name)
					self.tree_root_child_dict[self.root_dict[order].name].setIcon(0, QIcon('screenruler.ico'))
					self.tree_root_child_dict[self.root_dict[order].name].setCheckState(0, Qt.Checked)
					#print(self.root_dict[order].name)
					if self.root_dict[order].struct=="PART" and Nodelist.index(old_order)==len(Nodelist)-1:
						#print(114,Nodelist.index(old_order))
						break
			# todo 优化1 设置节点的状态
			# self.tree_root_child_dict[part_property["name"]].setCheckState(0, Qt.Checked)
		#print(self.tree_root_dict)
			

					
	def Create_Child(self):
		pass
	def Updata_Root(self):
		pass
	def Updata_Child(self):
		pass

