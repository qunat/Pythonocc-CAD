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
		self.pnt_endpoints_list=[gp_Pnt(point1),gp_Pnt(point2)]
		self.pnt_middlepoind_list=[None]
		self.ais_shape_line=AIS_Shape()
		self.capture_point_list=[None,None,None]
		self.capture_any_point_list = [None]
		self.isDone=None
		
	def create_line(self):
		aSegment = GC_MakeSegment(self.pnt_endpoints_list[0],self.pnt_endpoints_list[1])
		plane = gp_Pln(gp_Origin(), self.parent.gp_Dir)
		line = geomapi_To2d(aSegment.Value(), plane)
		line = BRepBuilderAPI_MakeEdge(geomapi_To3d(line, plane)).Edge()
		self.ais_shape=AIS_Shape(line)
		self.ais_shape.SetColor(Quantity_Color(self.parent.color))
		self.ais_shape.SetWidth(self.parent.width)

'''
	def create_end_point(self,p):
		x, y, z = p
		point_type = Aspect_TOM_POINT
		p = Geom_CartesianPoint(gp_Pnt(x, y, z))
		color = Quantity_Color(0, 0, 0, Quantity_TOC_RGB)
		ais_point = AIS_Point(p)
		drawer = ais_point.Attributes()
		asp = Prs3d_PointAspect(point_type, color, 4)
		drawer.SetPointAspect(asp)
		ais_point.SetAttributes(drawer)
		return ais_point

	def create_capture_point(self,*args):
		if len(args)==1:
			x,y,z=args[0]
			point_type = Aspect_TOM_O_POINT
			p = Geom_CartesianPoint(gp_Pnt(x, y, z))
			color = Quantity_Color(1, 1, 1, Quantity_TOC_RGB)
			ais_point = AIS_Point(p)
			drawer = ais_point.Attributes()
			asp = Prs3d_PointAspect(point_type, color, 4)
			drawer.SetPointAspect(asp)
			ais_point.SetAttributes(drawer)
			return ais_point
		elif len(args)==2:
			x0, y0, z0 = args[0]
			x1, y1, z1 = args[1]
			x = (x0 + x1) / 2
			y = (y0 + y1) / 2
			z = (z0 + z1) / 2
			point_type = Aspect_TOM_O_POINT
			p = Geom_CartesianPoint(gp_Pnt(x, y, z))
			color = Quantity_Color(1, 1, 1, Quantity_TOC_RGB)
			ais_point = AIS_Point(p)
			drawer = ais_point.Attributes()
			asp = Prs3d_PointAspect(point_type, color, 4)
			drawer.SetPointAspect(asp)
			ais_point.SetAttributes(drawer)
			return ais_point

	def set_ais_shape(self,p1,p2):
		x0, y0, z0 = p1
		x1, y1, z1 = p2
		aSegment = GC_MakeSegment(gp_Pnt(x0, y0, z0), gp_Pnt(x1, y1, z1))
		anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
		aWire = BRepBuilderAPI_MakeWire(anEdge.Edge()).Shape()
		plane = gp_Pln(gp_Origin(), self.parent.gp_Dir)
		line = geomapi_To2d(aSegment.Value(), plane)
		line = BRepBuilderAPI_MakeEdge(geomapi_To3d(line, plane)).Edge()
		self.ais_shape.SetShape(line)
		self.ais_shape.SetColor(Quantity_Color(self.parent.color))
		self.ais_shape.SetWidth(self.parent.width)
		self.parent.parent.Displayshape_core.canva._display.Context.Remove(self.edge_point_list[0], True)
		self.parent.parent.Displayshape_core.canva._display.Context.Remove(self.edge_point_list[1], True)
		self.edge_point_list[0] = self.create_end_point(p1)
		self.edge_point_list[1] = self.create_end_point(p2)
		self.capture_point_list[0]=self.create_capture_point(p1)
		self.capture_point_list[1] = self.create_capture_point(p1,p2)
		self.capture_point_list[2] = self.create_capture_point(p2)

	def set_capture_any_point(self,x,y,z):
		p1=[x,y,z]
		self.capture_any_point_list[0] = self.create_capture_point(p1)

	def get_end_point_pnt(self,point):
		Vertex0 = self.edge_point_list[point].Vertex()
		pnt = BRep_Tool.Pnt(Vertex0)
		return pnt
	def get_capture_point_pnt(self,point):
		Vertex0 = self.capture_point_list[point].Vertex()
		pnt = BRep_Tool.Pnt(Vertex0)
		return pnt
	def display_line(self):
		#self.parent.parent.Displayshape_core.canva._display.Context.Display(self.ais_shape,False)#显示的物体
		#self.parent.parent.Displayshape_core.canva._display.Repaint()
		#self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
		pass


	def redisplay(self):
		#self.parent.parent.Displayshape_core.canva._display.Context.Redisplay(self.ais_shape, True,False) #重新计算更新已经显示的物体
		#self.parent.parent.Displayshape_core.canva._display.Repaint()
		#self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
		pass

	def display_all(self):
		#self.parent.parent.Displayshape_core.canva._display.Context.Display(self.ais_shape,False)#显示的物体
		#self.parent.parent.Displayshape_core.canva._display.Context.Display(self.edge_point_list[0], False)  # 显示的物体
		#self.parent.parent.Displayshape_core.canva._display.Context.Display(self.edge_point_list[1], False)  # 显示的物体
		#self.parent.parent.Displayshape_core.canva._display.Repaint()
		#self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
		pass

	def redisplay_all(self):
		#self.parent.parent.Displayshape_core.canva._display.Context.Display(self.edge_point_list[0], False)  # 显示的物体
		#self.parent.parent.Displayshape_core.canva._display.Context.Display(self.edge_point_list[1], False)  # 显示的物体
		#self.parent.parent.Displayshape_core.canva._display.Context.Redisplay(self.ais_shape, True,False) #重新计算更新已经显示的物体
		#self.parent.parent.Displayshape_core.canva._display.Repaint()
		#self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
		pass

	def remove_ais_shape(self):
		#self.parent.parent.Displayshape_core.canva._display.Context.Remove(self.ais_shape, False)
		#self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
		pass
'''
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



	


	@timer_decorator
	def draw_line(self,shape=None):
			if self.parent.InteractiveOperate.InteractiveModule == "SKETCH":
				if self.draw_line_connect!=1 or True:
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_draw_trance)
					self.draw_line_connect=1
				(x, y, z, vx, vy, vz)=self.catch_capure_point(shape)
				if len(self.point_count) == 0:
					self.point = [x, y, z]
					self.point_count.append(self.point)
					self.show_line_dict[self.line_id] = None
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_draw_trance)
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_drwa_line)
					


				elif len(self.point_count) >= 1 :
					self.InteractiveModule = None
					if self.capture_point_None!=0:
						print(self.capture_point_None)


					p1=self.point
					p2=[x,y,z]
					self.show_line_dict[self.line_id].set_ais_shape(p1,p2)
					self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id].ais_shape, True,False)  # 重新计算更新已经显示的物体
					self.parent.Displayshape_core.canva._display.Context.Display(self.show_line_dict[self.line_id].ais_shape, False)  # 显示的物体
					self.parent.Displayshape_core.canva._display.Context.Display(self.show_line_dict[self.line_id].edge_point_list[0],False)  # 显示的物体
					self.parent.Displayshape_core.canva._display.Context.Display(self.show_line_dict[self.line_id].edge_point_list[1],False)  # 显示的物体
					#self.show_line_dict[self.line_id].redisplay_all()
					self.line_id+=1
					self.point_count.clear()
					start_time=time.time()
					#self.show_element = self.parent.Sketcher.get_all_sketcher_element()
					end_time=time.time()
					print("获取所有的sketcher元素的时间",end_time-start_time)
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.disconnect(self.dynamics_drwa_line)
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.disconnect(self.dynamics_draw_trance)
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.disconnect()
					print(self.parent.Displayshape_core.canva.mouse_move_Signal.trigger)
					#self.end_time=time.time()




	

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
					else:
						self.show_line_dict[self.line_id].pnt_endpoints_list=[gp_Pnt(p1),gp_Pnt(p2)]
						pass
				
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
			#myMarker =Graphic3d_AspectMarker3d(Aspect_TOM_CIRCLE,Quantity_Color(1.0, 0.0, 0.0, Quantity_TOC_RGB),10.0 )

			point = self.parent.Displayshape_core.canva._display.Context.Display(ais_point,
																				 False)  # 重新计算更新已经显示的物
		else:
			point = self.parent.Displayshape_core.canva._display.DisplayShape(gp_Pnt(x,y,z),color="YELLOW",
																			update=False	 )  # 重新计算更新已经显示的物
			self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
			self.parent.Displayshape_core.canva._display.Repaint()



		
			
