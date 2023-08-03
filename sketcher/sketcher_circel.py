# -*- coding: utf-8 -*-
from OCC.Core import BRepExtrema
from OCC.Core.BRep import BRep_Tool
from OCC.Core.Geom import Geom_CartesianPoint, Geom_Line
from OCC.Core.Prs3d import Prs3d_PointAspect
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.TopoDS import TopoDS_Vertex, TopoDS_Wire
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from GUI.SelectWidget import SelectWidget
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.GC import GC_MakeSegment, GC_MakeCircle
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Ax2,gp_Dir
from OCC.Core.AIS import AIS_Shape, AIS_Point
from sketcher.sketcher_line import sketch_line
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

class Brep_circel(object):
	def __init__(self,parent=None,point1=None,point2=None,gp_dir=None):
		self.parent=parent
		self.center_point=[None]
		self.gp_dir=gp_dir
		self.ais_shape=None
		self.capture_center_point_list=[None]
		self.capture_any_point_list = [None]
		self.create_circel(point1,point2)
		self.isDone=None

	def create_circel(self,p1,p2):
		radius = p1.Distance(p2)
		circel = GC_MakeCircle(p1, self.gp_dir, radius).Value()
		circel_builder = BRepBuilderAPI_MakeEdge(circel)
		circel = circel_builder.Edge()
		self.ais_shape=AIS_Shape(circel)
		self.ais_shape.SetColor(Quantity_Color(self.parent.color))
		self.ais_shape.SetWidth(self.parent.width)
		self.center_point[0]=self.create_center_point(p1)
		print("半径",radius)
		#self.display_circel()
		#self.dispaly_center_point()

	def create_center_point(self,p1):
		x, y, z = p1.Coord()
		point_type = Aspect_TOM_POINT
		p = Geom_CartesianPoint(gp_Pnt(x, y, z))
		color = Quantity_Color(0, 0, 0, Quantity_TOC_RGB)
		ais_point = AIS_Point(p)
		drawer = ais_point.Attributes()
		asp = Prs3d_PointAspect(point_type, color, 4)
		drawer.SetPointAspect(asp)
		ais_point.SetAttributes(drawer)
		return ais_point

	def create_capture_point(self, *args):
		x, y, z = args[0].Coord()
		point_type = Aspect_TOM_O_POINT
		p = Geom_CartesianPoint(gp_Pnt(x, y, z))
		color = Quantity_Color(1, 1, 1, Quantity_TOC_RGB)
		ais_point = AIS_Point(p)
		drawer = ais_point.Attributes()
		asp = Prs3d_PointAspect(point_type, color, 4)
		drawer.SetPointAspect(asp)
		ais_point.SetAttributes(drawer)
		return ais_point

	def create_capture_any_point(self, p1):
		x, y, z = p1
		point_type = Aspect_TOM_O_POINT
		p = Geom_CartesianPoint(gp_Pnt(x, y, z))
		color = Quantity_Color(1, 1, 1, Quantity_TOC_RGB)
		ais_point = AIS_Point(p)
		drawer = ais_point.Attributes()
		asp = Prs3d_PointAspect(point_type, color, 4)
		drawer.SetPointAspect(asp)
		ais_point.SetAttributes(drawer)
		self.capture_any_point_list[0]=ais_point



	def set_ais_shape(self,p1,p2):
		radius = p1.Distance(p2)
		circel = GC_MakeCircle(p1, self.gp_dir, radius).Value()
		circel_builder = BRepBuilderAPI_MakeEdge(circel)
		circel = circel_builder.Edge()
		self.ais_shape.SetWidth(self.parent.width)
		self.ais_shape.SetShape(circel)
		self.ais_shape.SetColor(Quantity_Color(self.parent.color))
		self.ais_shape.SetWidth(self.parent.width)
		self.capture_center_point_list[0]=self.create_capture_point(p1)
		#self.redisplay()
	
	def display_circel(self):
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.ais_shape, False)  # 显示的物体
		self.parent.parent.Displayshape_core.canva._display.Repaint()
		self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
	def dispaly_center_point(self):
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.center_point[0], False)  # 显示的物体
		self.parent.parent.Displayshape_core.canva._display.Repaint()
		self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()

	def redisplay(self):
		self.parent.parent.Displayshape_core.canva._display.Context.Redisplay(self.ais_shape, True,False)  # 重新计算更新已经显示的物体
		self.parent.parent.Displayshape_core.canva._display.Repaint()
		self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
	




class sketch_circel(sketch_line):
	def __init__(self,parent=None,gp_Dir=None):
		super(sketch_circel, self).__init__()
		self.parent = parent
		self.gp_Dir=gp_Dir
		self.dragStartPosX = 0
		self.dragStartPosY = 0
		self.aisline = None
		self.point_count = []
		self.line_dict = {}
		self.pointt_dict = {}
		self.show_circel_dict = {}
		self.point_count = []
		self.circel_id = 0
		self.draw_circel_connect=None

	
	def draw_circel(self, shape=None):
		if self.parent.InteractiveOperate.InteractiveModule == "SKETCH":
			(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()
			if self.draw_circel_connect!=1:
				self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_draw_trance)
				self.draw_circel_connect=1
			x, y, z, vx, vy, vz=self.catch_capure_point(shape)

			if len(self.point_count) == 0:
				self.point = (x, y, z)
				self.point_count.append(self.point)
				self.show_circel_dict[self.circel_id] = None
				self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_drwa_circel)
			
			
			elif len(self.point_count) >= 1:
				self.InteractiveModule = None
				p1=gp_Pnt(self.point_count[-1][0], self.point_count[-1][1], self.point_count[-1][2])
				p2=gp_Pnt(x, y, z)
				self.show_circel_dict[self.circel_id].set_ais_shape(p1,p2)  # 将已经显示的零件设置成另外一个新零件
				self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_circel_dict[self.circel_id].ais_shape, True, False)  # 重新计算更新已经显示的物体
				self.circel_id += 1
				self.point_count.clear()
				self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.disconnect(self.dynamics_drwa_circel)
				#self.show_element = self.parent.Sketcher.get_all_sketcher_element()
	
	def dynamics_drwa_circel(self):
		_dragStartPosY = self.parent.Displayshape_core.canva.dragStartPosY
		_dragStartPosX = self.parent.Displayshape_core.canva.dragStartPosX
		if self.dragStartPosY != _dragStartPosY or self.dragStartPosX != _dragStartPosX:
			
			(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()

			try:
				x0 = self.point[0]
				y0 = self.point[1]
				z0 = self.point[2]
				p1 = gp_Pnt(x0,y0,z0)
				p2 = gp_Pnt(x, y, z)

				if self.show_circel_dict[self.circel_id] == None and p1.Distance(p2)!=0:
					self.show_circel_dict[self.circel_id] = Brep_circel(self,p1,p2,self.gp_Dir)
					self.parent.Displayshape_core.canva._display.Context.Display(self.show_circel_dict[self.circel_id].ais_shape, False)  # 显示圆弧
					self.parent.Displayshape_core.canva._display.Context.Display(self.show_circel_dict[self.circel_id].center_point[0],False)  # 显示圆心
					self.parent.Displayshape_core.canva._display.Repaint()
					self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
				else:
					self.show_circel_dict[self.circel_id].set_ais_shape(p1,p2)  # 将已经显示的零件设置成另外一个新零件
					self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_circel_dict[self.circel_id].ais_shape, True,False)  # 重新计算更新已经显示的物体
				self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
			
			
			except Exception as e:
				print(e)
				pass
		
		self.dragStartPosX = _dragStartPosX
		self.dragStartPosY = _dragStartPosY


