# -*- coding: utf-8 -*-
class PartOperate(object):
	def __init__(self,parent=None):
		self.parent=parent
		index=self.parent.ModuleWindowManager.tabwidget.currentIndex()
		name=self.parent.ModuleWindowManager.tabwidget.tabText(index)
		self.name=name
		self.parent.Displayshape_core_dict[self.name].canva.mousePressEvent_Signal.trigger.connect(self.getshape)

	def partmove(self):
		index=self.parent.ModuleWindowManager.tabwidget.currentIndex()
		name=self.parent.ModuleWindowManager.tabwidget.tabText(index)
		shape = self.parent.Displayshape_core_dict[name].canva._display.Context.Current()  # 通过此方法可以获取尺寸
		

	def getshape(self):
		shape = self.parent.Displayshape_core_dict[self.name].canva._display.Context.Current()  # 通过此方法可以获取尺寸
		print(shape)

