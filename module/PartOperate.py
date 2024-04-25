# -*- coding: utf-8 -*-
from OCC.Core.AIS import AIS_Shape
from OCC.Core.TopAbs import TopAbs_VERTEX, TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID, TopAbs_SHELL, TopAbs_COMPOUND, TopAbs_WIRE
from OCC.Core.StdSelect import StdSelect_ShapeTypeFilter

class PartOperate(object):
	def __init__(self,parent=None):
		self.parent=parent
		#self.setting()

	def setting(self):
		index=self.parent.ModuleWindowManager.tabwidget.currentIndex()
		name=self.parent.ModuleWindowManager.tabwidget.tabText(index)
		self.name=name
		self.parent.Displayshape_core_dict[self.name].canva._display.register_select_callback(self.line_clicked)

		#solidFilter=StdSelect_ShapeTypeFilter(TopAbs_FACE)#选择过滤器
		#self.parent.Displayshape_core_dict[self.name].canva._display.Context.AddFilter(solidFilter)#设置过滤器

		self.parent.Displayshape_core_dict[self.name].canva._display.SetSelectionModeNeutral()
		self.parent.Displayshape_core_dict[self.name].canva._display.SetSelectionModeFace()

		self.parent.Displayshape_core_dict[self.name].canva.mousePressEvent_Signal.trigger.connect(self.getshape)
		

		

	def getshape(self):
		index=self.parent.ModuleWindowManager.tabwidget.currentIndex()
		name=self.parent.ModuleWindowManager.tabwidget.tabText(index)
		self.name=name
		shape = self.parent.Displayshape_core_dict[self.name].canva._display.Context.DetectedCurrentShape()  # 通过此方法可以当前鼠标点击的ais_shape
		#self.ais_shape=AIS_Shape.DownCast(shape)
		#self.parent.Displayshape_core_dict[self.name].canva._display.Context.Remove(ais_shape,True)
		print(shape)

	def line_clicked(self,shp, *kwargs):
		""" This function is called whenever a line is selected
		"""
		for shape in shp:
			print(shape)

	def part(self):
		index=self.parent.ModuleWindowManager.tabwidget.currentIndex()
		name=self.parent.ModuleWindowManager.tabwidget.tabText(index)
		self.name=name
		#self.parent.Displayshape_core_dict[self.name].canva.mousePressEvent_Signal.trigger.connect(self.getshape)
		self.parent.Displayshape_core_dict[self.name].canva.mouse_move_Signal.trigger.connect(self.getshape)
	def partmove(self):
		try:
			print(self.ais_shape)
		except:
			pass

               