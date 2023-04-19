# -*- coding: utf-8 -*-
class InteractiveOperate(object):
	def __init__(self,parent=None):
		self.parent=parent
		self.InteractiveModule=None
		self.select_shape_list=[]
		
		
	def clicked_callback(self,shp, *kwargs):
		try:
			if self.InteractiveModule=="SKETCH":
				print(5555,shp)
				
		
		except Exception as e:
			print(e)
	