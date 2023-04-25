# -*- coding: utf-8 -*-
from GUI.SelectWidget import SelectWidget
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Ax2,gp_Dir
from sketcher.sketcher_circel import sketch_circel
from sketcher.sketcher_line import sketch_line
from sketcher.sketcher_rectangle import sketch_rectangle

class SketchModule(object):
	def __init__(self,parent=None):
		self.parent=parent
		self.sketch_type=None
		self.select_shape_list = []
		self.dragStartPosX = 0
		self.dragStartPosY = 0
		self.aisline = None
		self.point_count = []
		self.gp_Dir=None
		
	def select_skecth_plane(self):
		self.select_windows=SelectWidget(parent=self.parent)
		self.select_windows.Show()
		
	def uptoplane(self):
		self.parent.InteractiveOperate.InteractiveModule="SKETCH"
		self.parent.Displayshape_core.canva._display.register_select_callback(self.clicked_callback)
		if self.select_windows.comboBox.currentText()=="XY平面":
			self.parent.Displayshape_core.canva._display.View_Top()
			self.parent.Displayshape_core.canva._display.FitAll()
			self.gp_Dir=gp_Dir(0,0,1)
		if self.select_windows.comboBox.currentText()=="YZ平面":
			self.parent.Displayshape_core.canva._display.View_Right()
			self.parent.Displayshape_core.canva._display.FitAll()
			self.gp_Dir=gp_Dir(1,0,0)
		if self.select_windows.comboBox.currentText()=="XZ平面":
			self.parent.Displayshape_core.canva._display.View_Front()
			self.parent.Displayshape_core.canva._display.FitAll()
			self.gp_Dir=gp_Dir(0,1,0)
	
	def clicked_callback(self, shp, *kwargs):
		try:
			print(shp)
			if self.sketch_type==4:
				self.new_do_draw.draw_line(shp)# draw line
			elif self.sketch_type==3:
				self.new_do_draw.draw_circel(shp)
			elif self.sketch_type==2:
				self.new_do_draw.draw_rectangle(shp)
		except Exception as e:
			print(e)
	def do_draw(self):
		if self.sketch_type==4:
			self.new_do_draw=sketch_line(self.parent)# draw line
		elif self.sketch_type==3:
			self.new_do_draw = sketch_circel(self.parent,self.gp_Dir)  # draw ciecel
		elif self.sketch_type==2:
			self.new_do_draw = sketch_rectangle(self.parent,self.gp_Dir)  # draw rectangle

		
	def dynamics_drwa(self):
		if self.sketch_type==4:
			self.new_do_draw.dynamics_drwa_line()# draw line
		elif self.sketch_type==3:
			self.new_do_draw.dynamics_drwa_circel()  # draw circel
		elif self.sketch_type==2:
			self.new_do_draw.dynamics_drwa_rectangle()  # draw rectangle

	def skecth_draw_profile(self):
		self.sketch_type=1# profile draw
		self.do_draw()
	def skecth_draw_rectangle(self):
		self.sketch_type=2# rectangle draw
		self.do_draw()
	def skecth_draw_circel(self):
		self.sketch_type=3# circel draw
		self.do_draw()
	def skecth_draw_line(self):
		self.sketch_type=4# line draw
		self.do_draw()
	def skecth_draw_arc(self):
		self.sketch_type=5# arc draw
		self.do_draw()
	def skecth_draw_spline(self):
		self.sketch_type=6# spline draw
		self.do_draw()
	def skecth_draw_point(self):
		self.sketch_type=7# point draw
		self.do_draw()
		
	
	
	
	
