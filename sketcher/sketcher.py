# -*- coding: utf-8 -*-
from OCC.Core import BRepExtrema
from OCC.Core.BRep import BRep_Tool
from OCC.Core.Geom import Geom_CartesianPoint, Geom_Line
from OCC.Core.Prs3d import Prs3d_PointAspect
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.TopoDS import TopoDS_Vertex, TopoDS_Wire
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from GUI.SelectWidget import SelectWidget
import threading
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.GC import GC_MakeSegment
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin
from OCC.Core.AIS import AIS_Shape, AIS_Point
from OCC.Core.Aspect import (Aspect_TOM_POINT,
                             Aspect_TOM_PLUS,
                             Aspect_TOM_STAR,
                             Aspect_TOM_X,
                             Aspect_TOM_O,
                             Aspect_TOM_O_POINT,
                             Aspect_TOM_O_PLUS,
                             Aspect_TOM_O_STAR,
                             Aspect_TOM_O_X,
                             Aspect_TOM_RING1,
                             Aspect_TOM_RING2,
                             Aspect_TOM_RING3,
                             Aspect_TOM_BALL)


class SketchModule(object):
	def __init__(self,parent=None):
		self.parent=parent
		self.sketch_type=None
		self.select_shape_list = []
		self.dragStartPosX = 0
		self.dragStartPosY = 0
		self.aisline = None
		self.point_count = []
		
	def select_skecth_plane(self):
		self.select_windows=SelectWidget(parent=self.parent)
		self.select_windows.Show()
		
	def uptoplane(self):
		self.parent.InteractiveOperate.InteractiveModule="SKETCH"
		self.parent.Displayshape_core.canva._display.register_select_callback(self.clicked_callback)
		if self.select_windows.comboBox.currentText()=="XY平面":
			self.parent.Displayshape_core.canva._display.View_Top()
			self.parent.Displayshape_core.canva._display.FitAll()
			
		if self.select_windows.comboBox.currentText()=="YZ平面":
			self.parent.Displayshape_core.canva._display.View_Right()
			self.parent.Displayshape_core.canva._display.FitAll()
			self.do_draw()
		if self.select_windows.comboBox.currentText()=="XZ平面":
			self.parent.Displayshape_core.canva._display.View_Front()
			self.parent.Displayshape_core.canva._display.FitAll()
			self.do_draw()
	
	def clicked_callback(self, shp, *kwargs):
		try:
			if self.sketch_type==4:
				self.new_do_draw.draw_line(shp)# draw line
		except Exception as e:
			print(e)
	def do_draw(self):
		if self.sketch_type==4:
			self.new_do_draw=sketch_line(self.parent)# draw line
		
	def dynamics_drwa(self):
		self.new_do_draw.dynamics_drwa_line()# draw line
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
		
	
	
	
	
class sketch_line(object):
	def __init__(self, parent=None):
		self.parent = parent
		self.dragStartPosX = 0
		self.dragStartPosY = 0
		self.aisline = None
		self.point_count = []
		self.line_dict = {}
		self.pointt_dict = {}
		self.show_line_dict = {}
		self.point_count = []
		self.line_id=0
		
	def draw_line(self,shape=None):
			if self.parent.InteractiveOperate.InteractiveModule == "SKETCH":
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(
					self.parent.Displayshape_core.canva.dragStartPosX,
					self.parent.Displayshape_core.canva.dragStartPosY)
				
				if shape!=[] and isinstance(shape[0],TopoDS_Vertex) :#捕捉端点
					P = BRep_Tool.Pnt(shape[0])
					x,y,z=P.X(),P.Y(),P.Z()
					
				if shape!=[] and isinstance(shape[0],TopoDS_Wire) :#捕捉线上任意点
					direction = gp_Dir(vx, vy, vz)
					line = gp_Lin(gp_Pnt(x, y, z), direction)
					ais_line = Geom_Line(line)
					edge_builder = BRepBuilderAPI_MakeEdge(line)
					edge = edge_builder.Edge()
					extrema = BRepExtrema.BRepExtrema_DistShapeShape(shape[0], edge)
					nearest_point = extrema.PointOnShape1(1)
					x, y, z = nearest_point.X(), nearest_point.Y(), nearest_point.Z()
					
				
				if len(self.point_count) == 0:
					self.draw_point(x,y,z)
					self.point = (x, y, z)
					self.point_count.append(self.point)
					self.show_line_dict[self.line_id] = None
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_drwa_line)
					
					
				elif len(self.point_count) >= 1:
					self.InteractiveModule = None
					self.draw_point(x, y, z)# end point
					aSegment = GC_MakeSegment(
						gp_Pnt(self.point_count[-1][0], self.point_count[-1][1], self.point_count[-1][2]),
						gp_Pnt(x, y, z))
					anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
					aWire = BRepBuilderAPI_MakeWire(anEdge.Edge()).Shape()
					self.show_line_dict[self.line_id][0].SetShape(aWire)  # 将已经显示的零件设置成另外一个新零件
					self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id][0], True,
																				   False)  # 重新计算更新已经显示的物体
					self.line_id+=1
					self.point_count.clear()
		
	def dynamics_drwa_line(self):
			_dragStartPosY = self.parent.Displayshape_core.canva.dragStartPosY
			_dragStartPosX = self.parent.Displayshape_core.canva.dragStartPosX
			if self.dragStartPosY != _dragStartPosY or self.dragStartPosX != _dragStartPosX:
				
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(
					_dragStartPosX,
					_dragStartPosY)
				# print(x, y, z)
				try:
					x0 = self.point[0]
					y0 = self.point[1]
					z0 = self.point[2]
					aSegment = GC_MakeSegment(gp_Pnt(x0, y0, z0), gp_Pnt(x, y, z))
					anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
					aWire = BRepBuilderAPI_MakeWire(anEdge.Edge()).Shape()
					
					if self.show_line_dict[self.line_id] == None:
						self.show_line_dict[self.line_id] = AIS_Shape(aWire)
						self.show_line_dict[self.line_id] = self.parent.Displayshape_core.canva._display.DisplayShape(aWire, True,
																								 False)  # 重新计算更新已经显示的物体
					else:
						self.show_line_dict[self.line_id][0].SetShape(aWire)  # 将已经显示的零件设置成另外一个新零件
					self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id][0], True,
																				   False)  # 重新计算更新已经显示的物体
					self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
				
				
				except Exception as e:
					pass
			
			self.dragStartPosX = _dragStartPosX
			self.dragStartPosY = _dragStartPosY
	

	def draw_point(self,x,y,z,point_type=None,color=None):
		ALL_ASPECTS = [Aspect_TOM_POINT,
					   Aspect_TOM_PLUS,
					   Aspect_TOM_STAR,
					   Aspect_TOM_X,
					   Aspect_TOM_O,
					   Aspect_TOM_O_POINT,
					   Aspect_TOM_O_PLUS,
					   Aspect_TOM_O_STAR,
					   Aspect_TOM_O_X,
					   Aspect_TOM_RING1,
					   Aspect_TOM_RING2,
					   Aspect_TOM_RING3,
					   Aspect_TOM_BALL]
		if point_type!=None:
			point_type = ALL_ASPECTS[point_type]
			p = Geom_CartesianPoint(gp_Pnt(x, y, z))
			color = Quantity_Color(0, 0, 0, Quantity_TOC_RGB)
			ais_point = AIS_Point(p)
			
			drawer = ais_point.Attributes()
			asp = Prs3d_PointAspect(point_type, color, 4)
			drawer.SetPointAspect(asp)
			ais_point.SetAttributes(drawer)
			point = self.parent.Displayshape_core.canva._display.Context.Display(ais_point,
																				 False)  # 重新计算更新已经显示的物
		else:
			point = self.parent.Displayshape_core.canva._display.DisplayShape(gp_Pnt(x,y,z),color="YELLOW",
																			update=False	 )  # 重新计算更新已经显示的物
			self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
			self.parent.Displayshape_core.canva._display.Repaint()
		
		
			
class sketch_circel(sketch_line):
	def __init__(self,parent=None):
		super(sketch_line, self).__init__()
	
	def draw_line(self, shape=None):
		if self.parent.InteractiveOperate.InteractiveModule == "SKETCH":
			(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(
				self.parent.Displayshape_core.canva.dragStartPosX,
				self.parent.Displayshape_core.canva.dragStartPosY)
			
			if shape != [] and isinstance(shape[0], TopoDS_Vertex):  # 捕捉端点
				P = BRep_Tool.Pnt(shape[0])
				x, y, z = P.X(), P.Y(), P.Z()
			
			if shape != [] and isinstance(shape[0], TopoDS_Wire):  # 捕捉线上任意点
				direction = gp_Dir(vx, vy, vz)
				line = gp_Lin(gp_Pnt(x, y, z), direction)
				ais_line = Geom_Line(line)
				edge_builder = BRepBuilderAPI_MakeEdge(line)
				edge = edge_builder.Edge()
				extrema = BRepExtrema.BRepExtrema_DistShapeShape(shape[0], edge)
				nearest_point = extrema.PointOnShape1(1)
				x, y, z = nearest_point.X(), nearest_point.Y(), nearest_point.Z()
			
			if len(self.point_count) == 0:
				self.draw_point(x, y, z)
				self.point = (x, y, z)
				self.point_count.append(self.point)
				self.show_line_dict[self.line_id] = None
				self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_drwa_line)
			
			
			elif len(self.point_count) >= 1:
				self.InteractiveModule = None
				self.draw_point(x, y, z)  # end point
				aSegment = GC_MakeSegment(
					gp_Pnt(self.point_count[-1][0], self.point_count[-1][1], self.point_count[-1][2]),
					gp_Pnt(x, y, z))
				anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
				aWire = BRepBuilderAPI_MakeWire(anEdge.Edge()).Shape()
				self.show_line_dict[self.line_id][0].SetShape(aWire)  # 将已经显示的零件设置成另外一个新零件
				self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id][0],
																			   True,
																			   False)  # 重新计算更新已经显示的物体
				self.line_id += 1
				self.point_count.clear()
	
	def dynamics_drwa_line(self):
		_dragStartPosY = self.parent.Displayshape_core.canva.dragStartPosY
		_dragStartPosX = self.parent.Displayshape_core.canva.dragStartPosX
		if self.dragStartPosY != _dragStartPosY or self.dragStartPosX != _dragStartPosX:
			
			(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(
				_dragStartPosX,
				_dragStartPosY)
			# print(x, y, z)
			try:
				x0 = self.point[0]
				y0 = self.point[1]
				z0 = self.point[2]
				aSegment = GC_MakeSegment(gp_Pnt(x0, y0, z0), gp_Pnt(x, y, z))
				anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
				aWire = BRepBuilderAPI_MakeWire(anEdge.Edge()).Shape()
				
				if self.show_line_dict[self.line_id] == None:
					self.show_line_dict[self.line_id] = AIS_Shape(aWire)
					self.show_line_dict[self.line_id] = self.parent.Displayshape_core.canva._display.DisplayShape(aWire,
																												  True,
																												  False)  # 重新计算更新已经显示的物体
				else:
					self.show_line_dict[self.line_id][0].SetShape(aWire)  # 将已经显示的零件设置成另外一个新零件
				self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id][0],
																			   True,
																			   False)  # 重新计算更新已经显示的物体
				self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
			
			
			except Exception as e:
				pass
		
		self.dragStartPosX = _dragStartPosX
		self.dragStartPosY = _dragStartPosY