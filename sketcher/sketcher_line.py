# -*- coding: utf-8 -*-
import math
import time

from OCC.Core import BRepExtrema
from OCC.Core.BRep import BRep_Tool
from OCC.Core.GCE2d import GCE2d_MakeLine
from OCC.Core.Geom import Geom_CartesianPoint, Geom_Line
from OCC.Core.Graphic3d import Graphic3d_AspectMarker3d
from OCC.Core.Prs3d import Prs3d_PointAspect
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.StdSelect import StdSelect_ShapeTypeFilter
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import TopoDS_Vertex, TopoDS_Wire, TopoDS_Shape, TopoDS_Edge
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from PyQt5.QtGui import QCursor, QPixmap
#from numba import *
from GUI.SelectWidget import SelectWidget
import threading
from OCC.Core.TopAbs import TopAbs_VERTEX, TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID, TopAbs_SHELL, TopAbs_COMPOUND, TopAbs_WIRE
from OCC.Core.GeomAPI import geomapi_To3d,geomapi_To2d
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_BLACK
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.GC import GC_MakeSegment, GC_MakeCircle
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Ax2, gp_Dir, gp_Pln, gp_Origin, gp_Lin2d,gp_Pnt2d
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

from sketcher import sketcher_circel

class Brep_line(object):
	def __init__(self,parent=None,point1=[],point2=[]):
		self.parent=parent
		self.pnt_endpoints_list=[gp_Pnt(point1[0],point1[1],point1[2]),gp_Pnt(point2[0],point2[1],point2[2])]
		self.pnt_middlepoind_list=[None]
		self.ais_shape_line=None
		self.capture_point_list=[None,None,None]
		self.capture_any_point_list = [None]
		self.isDone=None
		self.create_line()
		
	def create_line(self):
		aSegment = GC_MakeSegment(self.pnt_endpoints_list[0],self.pnt_endpoints_list[1])
		plane = gp_Pln(gp_Origin(), self.parent.gp_Dir)
		line = geomapi_To2d(aSegment.Value(), plane)
		line = BRepBuilderAPI_MakeEdge(geomapi_To3d(line, plane)).Edge()
		self.ais_shape=AIS_Shape(line)
		self.ais_shape.SetColor(Quantity_Color(self.parent.color))
		self.ais_shape.SetWidth(self.parent.width)
		
	def rebuild_line(self):
		aSegment = GC_MakeSegment(self.pnt_endpoints_list[0],self.pnt_endpoints_list[1])
		plane = gp_Pln(gp_Origin(), self.parent.gp_Dir)
		line = geomapi_To2d(aSegment.Value(), plane)
		line = BRepBuilderAPI_MakeEdge(geomapi_To3d(line, plane)).Edge()
		self.ais_shape.SetShape(line)
		self.ais_shape.SetColor(Quantity_Color(self.parent.color))
		self.ais_shape.SetWidth(self.parent.width)
	def reset_endpoints(self,point1,point2):
		self.pnt_endpoints_list=[gp_Pnt(point1[0],point1[1],point1[2]),gp_Pnt(point2[0],point2[1],point2[2])]
		
		
		

def timer_decorator(func):
	def wrapper(*args, **kwargs):
		start_time = time.time()
		result = func(*args, **kwargs)
		end_time = time.time()
		execution_time = end_time - start_time
		print(f"函数 {func.__name__} 执行时间为: {execution_time} 秒")
		return result
	return wrapper




class sketch_line(object):
	def __init__(self, parent=None,gp_Dir=None,width=2,color=Quantity_NOC_BLACK):
		self.parent = parent
		self.gp_Dir=gp_Dir
		self.width = width
		self.color=color
		self.dragStartPosX = 0
		self.dragStartPosY = 0
		self.aisline = None
		self.point_count = []
		self.line_dict = {}
		self.pointt_dict = {}
		self.show_line_dict = {}
		self.point_count = []
		self.line_id=0
		self.capture_point=None
		self.capture_point_list=[]
		self.capture_point_None=0
		self.capture_edge_point_list=[]
		self.capture_middle_point_list = []
		self.draw_line_connect=0
		self.draw_trance_element=None
		solidFilter=StdSelect_ShapeTypeFilter(TopAbs_EDGE)#选择过滤器
		self.parent.Displayshape_core.canva._display.Context.AddFilter(solidFilter)#设置过滤器



	


	#@timer_decorator
	def draw_line(self,shape=None):
			if self.parent.InteractiveOperate.InteractiveModule == "SKETCH":
				if self.draw_line_connect!=1 or True:
					#self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.parent.Sketcher.dynamics_draw_trance)
					self.draw_line_connect=1
				(x, y, z, vx, vy, vz)=self.parent.Sketcher.catch_capure_point(shape)
				
				if len(self.point_count) == 0:
					self.point = [x, y, z]
					self.point_count.append(self.point)
					print(x, y, z, vx, vy, vz)
					self.show_line_dict[self.line_id] = None
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.parent.Sketcher.dynamics_draw_trance)
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_drwa_line)
					self.draw_point(self.point[0],self.point[1],self.point[2])
					


				elif len(self.point_count) >= 1 :
					self.InteractiveModule = None
					if self.capture_point_None!=0:
						print(self.capture_point_None)


					p1=self.point
					p2=[x,y,z]
					self.show_line_dict[self.line_id].reset_endpoints(p1,p2)
					self.show_line_dict[self.line_id].rebuild_line()
					self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id].ais_shape, True,False)  # 重新计算更新已经显示的物体
					
					self.draw_point(p2[0], 	p2[1], 	p2[2])
					self.parent.InteractiveOperate.Setting()
					self.line_id+=1
					self.point_count.clear()
					self.show_element = self.parent.Sketcher.get_all_sketcher_element()
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.disconnect(self.dynamics_drwa_line)
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.disconnect(self.parent.Sketcher.dynamics_draw_trance)
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.disconnect()
					
					
					




	

	@timer_decorator
	def dynamics_drwa_line(self):
			_dragStartPosY = self.parent.Displayshape_core.canva.dragStartPosY
			_dragStartPosX = self.parent.Displayshape_core.canva.dragStartPosX
			if self.dragStartPosY != _dragStartPosY or self.dragStartPosX != _dragStartPosX:
				
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()
				try:
					p1 = self.point
					p2 = [x, y, z]
					
					if self.show_line_dict[self.line_id] == None:
						self.show_line_dict[self.line_id]=Brep_line(self,p1,p2)
						self.parent.Displayshape_core.canva._display.Context.Display(self.show_line_dict[self.line_id].ais_shape, False)  # 显示的物体
					else:
						self.show_line_dict[self.line_id].reset_endpoints(p1,p2)
						self.show_line_dict[self.line_id].rebuild_line()
						self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id].ais_shape, True,False)  # 重新计算更新已经显示的物体
						pass
				
				except Exception as e:
					pass
			
			self.dragStartPosX = _dragStartPosX
			self.dragStartPosY = _dragStartPosY

	def draw_point(self,x,y,z,point_type=0,color=None):

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
			a123 = asp.Aspect()
			a123.SetType(Aspect_TOM_POINT)
			asp.SetAspect(a123)
			#ais_point.SetAutoHilight(False)
			
			#asp.SetScale(4.0)
			#asp.SetTypeOfMarker(Aspect_TOM_POINT)
			drawer.SetPointAspect(asp)
			
			
			a123 = asp.Aspect()
			a123.SetType(Aspect_TOM_POINT)
			asp.SetAspect(a123)
			ais_point.SetAspect(asp)
			
			ais_point.SetAttributes(drawer)
			self.parent.InteractiveOperate.Setting(drawer)
			#myMarker =Graphic3d_AspectMarker3d(Aspect_TOM_CIRCLE,Quantity_Color(1.0, 0.0, 0.0, Quantity_TOC_RGB),10.0 )
	
			

			self.parent.Displayshape_core.canva._display.Context.Display(ais_point,
																				 False)  # 重新计算更新已经显示的物
		else:
			self.parent.Displayshape_core.canva._display.DisplayShape(gp_Pnt(x,y,z),color="YELLOW",
																			update=False	 )  # 重新计算更新已经显示的物
			self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
			self.parent.Displayshape_core.canva._display.Repaint()



		
			
