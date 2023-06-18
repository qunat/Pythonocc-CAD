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
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import TopoDS_Vertex, TopoDS_Wire, TopoDS_Shape, TopoDS_Edge
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from PyQt5.QtGui import QCursor, QPixmap
#from numba import *
from GUI.SelectWidget import SelectWidget
import threading
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.GeomAPI import geomapi_To3d,geomapi_To2d
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_BLACK
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.GC import GC_MakeSegment, GC_MakeCircle
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Ax2, gp_Dir, gp_Pln, gp_Origin, gp_Lin2d,gp_Pnt2d
from OCC.Core.AIS import AIS_Shape, AIS_Point
from sketcher.sketcher_line import sketch_line,Brep_line
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




def timer_decorator(func):
	def wrapper(*args, **kwargs):
		start_time = time.time()
		result = func(*args, **kwargs)
		end_time = time.time()
		execution_time = end_time - start_time
		print(f"函数 {func.__name__} 执行时间为: {execution_time} 秒")
		return result
	return wrapper




class sketch_profile(sketch_line):
	def __init__(self, parent=None,gp_Dir=None,width=2,color=Quantity_NOC_BLACK):
		super(sketch_profile, self).__init__()
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






	#@timer_decorator
	def draw_line(self,shape=None):
			if self.parent.InteractiveOperate.InteractiveModule == "SKETCH":
				if self.draw_line_connect!=1:
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_draw_trance)
					self.draw_line_connect=1

				(x, y, z, vx, vy, vz)=self.catch_capure_point(shape)

				if len(self.point_count) == 0:
					print("enter1")
					self.point = [x, y, z]
					self.point_count.append(self.point)
					self.show_line_dict[self.line_id] = None
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_drwa_line)


				elif len(self.point_count) >=1 :#封闭端点
					if gp_Pnt(x,y,z).Coord()==self.show_line_dict[0].get_capture_point_pnt(0).Coord() or gp_Pnt(x,y,z).Coord()==self.show_line_dict[0].get_capture_point_pnt(2).Coord():
						p1 = self.point
						p2 = [x, y, z]
						self.show_line_dict[self.line_id].set_ais_shape(p1, p2)
						self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id].ais_shape, True, False)  # 重新计算更新已经显示的物体
						self.parent.Displayshape_core.canva._display.Context.Display(self.show_line_dict[self.line_id].ais_shape, False)  # 显示的物体
						self.parent.Displayshape_core.canva._display.Context.Display(self.show_line_dict[self.line_id].edge_point_list[0], False)  # 显示的物体
						self.parent.Displayshape_core.canva._display.Context.Display(self.show_line_dict[self.line_id].edge_point_list[1], False)  # 显示的物体
						#self.show_line_dict[self.line_id].redisplay_all()
						self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.disconnect(self.dynamics_drwa_line)
						self.line_id += 1
						self.show_element = self.parent.Sketcher.get_all_sketcher_element()
						self.point_count.clear()
						self.parent.InteractiveOperate.InteractiveClose = None
					else:#连续端点
						p1 = self.point
						p2 = [x, y, z]
						self.show_line_dict[self.line_id].set_ais_shape(p1, p2)
						#self.show_line_dict[self.line_id].redisplay_all()
						self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id].ais_shape, True, False)  # 重新计算更新已经显示的物体
						self.parent.Displayshape_core.canva._display.Context.Display(self.show_line_dict[self.line_id].ais_shape, False)  # 显示的物体
						self.parent.Displayshape_core.canva._display.Context.Display(self.show_line_dict[self.line_id].edge_point_list[0], False)  # 显示的物体
						self.parent.Displayshape_core.canva._display.Context.Display(self.show_line_dict[self.line_id].edge_point_list[1], False)  # 显示的物体
						self.line_id += 1
						self.point_count.append(p2)
						self.point=p2
						self.show_element = self.parent.Sketcher.get_all_sketcher_element()
						self.show_line_dict[self.line_id] = None
						self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_drwa_line)






	#@timer_decorator
	def dynamics_drwa_line(self):
			_dragStartPosY = self.parent.Displayshape_core.canva.dragStartPosY
			_dragStartPosX = self.parent.Displayshape_core.canva.dragStartPosX
			if self.dragStartPosY != _dragStartPosY or self.dragStartPosX != _dragStartPosX:
				
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()
				# print(x, y, z)
				try:
					p1 = self.point
					p2 = [x, y, z]
					if self.show_line_dict[self.line_id] == None :
						self.show_line_dict[self.line_id]=Brep_line(self,p1,p2)
					elif self.parent.InteractiveOperate.InteractiveClose=="finish":
						#self.show_line_dict[self.line_id].remove_ais_shape()
						self.parent.Displayshape_core.canva._display.Context.Remove(self.show_line_dict[self.line_id].ais_shape, False)
						self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.disconnect(self.dynamics_drwa_line)
						self.parent.InteractiveOperate.InteractiveClose = None
					else:
						self.show_line_dict[self.line_id].set_ais_shape(p1, p2)
						pass
				
				except Exception as e:
					pass
			
			self.dragStartPosX = _dragStartPosX
			self.dragStartPosY = _dragStartPosY


		
			
