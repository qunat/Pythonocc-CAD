# -*- coding: utf-8 -*-
import math

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
from numba import *
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


class Brep_line(object):
	def __init__(self,parent=None,point1=[],point2=[]):
		self.parent=parent
		self.edge_point_list=[None,None]
		self.middle_poind_list=[None]
		self.ais_shape=None
		self.capture_point_list=[None,None,None]
		self.capture_any_point_list = [None]
		self.create_line(point1,point2)

	def create_line(self,p1=[],p2=[]):
		x0,y0,z0=p1
		x1,y1,z1=p2
		aSegment = GC_MakeSegment(gp_Pnt(x0,y0,z0),gp_Pnt(x1,y1,z1))
		anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
		aWire = BRepBuilderAPI_MakeWire(anEdge.Edge()).Shape()
		plane = gp_Pln(gp_Origin(), self.parent.gp_Dir)
		line = geomapi_To2d(aSegment.Value(), plane)
		line = BRepBuilderAPI_MakeEdge(geomapi_To3d(line, plane)).Edge()

		self.ais_shape=AIS_Shape(line)
		self.ais_shape.SetColor(Quantity_Color(self.parent.color))
		self.ais_shape.SetWidth(self.parent.width)
		self.edge_point_list[0]=self.create_end_point(p1)
		self.edge_point_list[1] = self.create_end_point(p2)
		self.display_line()


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

		self.redisplay()
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
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.ais_shape,False)#显示的物体
		self.parent.parent.Displayshape_core.canva._display.Repaint()
		self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()


	def redisplay(self):
		self.parent.parent.Displayshape_core.canva._display.Context.Redisplay(self.ais_shape, True,False) #重新计算更新已经显示的物体
		self.parent.parent.Displayshape_core.canva._display.Repaint()
		self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()

	def display_all(self):
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.ais_shape,False)#显示的物体
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.edge_point_list[0], False)  # 显示的物体
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.edge_point_list[1], False)  # 显示的物体
		self.parent.parent.Displayshape_core.canva._display.Repaint()
		self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()

	def redisplay_all(self):
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.edge_point_list[0], False)  # 显示的物体
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.edge_point_list[1], False)  # 显示的物体
		self.parent.parent.Displayshape_core.canva._display.Context.Redisplay(self.ais_shape, True,False) #重新计算更新已经显示的物体
		self.parent.parent.Displayshape_core.canva._display.Repaint()
		self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
	def display_capture_point(self):
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.capture_point_list[0], False)  # 显示的物体
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.capture_point_list[1], False)  # 显示的物体
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.capture_point_list[2], False)  # 显示的物体
		self.parent.parent.Displayshape_core.canva._display.Repaint()
		self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()

	def remove_capture_point(self):
		self.parent.parent.Displayshape_core.canva._display.Context.Remove(self.capture_point_list[0], True)  #移除捕捉的任意点
		self.parent.parent.Displayshape_core.canva._display.Context.Remove(self.capture_point_list[1], True)  #移除捕捉的任意点
		self.parent.parent.Displayshape_core.canva._display.Context.Remove(self.capture_point_list[2], True)  #移除捕捉的任意点
		self.parent.parent.Displayshape_core.canva._display.Repaint()
		self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()


	def display_capture_any_point(self):
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.capture_any_point_list[0],
																			False)  # 显示的物体
		self.parent.parent.Displayshape_core.canva._display.Repaint()
		self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()

	def remove_capture_any_point(self):
		self.parent.parent.Displayshape_core.canva._display.Context.Remove(self.capture_any_point_list[0], False)  # 移除
		self.parent.parent.Displayshape_core.canva._display.Repaint()
		self.parent.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()





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

	def catch_capure_point(self,shape):#捕捉绘制点
		(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()
		if shape != [] and isinstance(shape[0], TopoDS_Vertex):  # 捕捉端点
			P = BRep_Tool.Pnt(shape[0])
			x, y, z = P.X(), P.Y(), P.Z()
		if shape != [] and isinstance(shape[0], TopoDS_Edge):  # 捕捉线上任意点
			direction = gp_Dir(vx, vy, vz)
			line = gp_Lin(gp_Pnt(x, y, z), direction)
			edge_builder = BRepBuilderAPI_MakeEdge(line)
			edge = edge_builder.Edge()
			extrema = BRepExtrema.BRepExtrema_DistShapeShape(shape[0], edge)
			nearest_point = extrema.PointOnShape1(1)
			x, y, z = nearest_point.X(), nearest_point.Y(), nearest_point.Z()
		if shape == []:  # 捕捉生成的端点
			shape_id = 0
			Distance = 0
			_dragStartPosY = self.parent.Displayshape_core.canva.dragStartPosY
			_dragStartPosX = self.parent.Displayshape_core.canva.dragStartPosX
			(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()
			direction = gp_Dir(vx, vy, vz)
			line = gp_Lin(gp_Pnt(x, y, z), direction)
			edge_builder = BRepBuilderAPI_MakeEdge(line)
			edge = edge_builder.Edge()
			for key in self.show_line_dict.keys():
				try:
					if key == self.line_id and len(self.point_count) >= 1:
						continue
					extrema = BRepExtrema.BRepExtrema_DistShapeShape(self.show_line_dict[key].ais_shape.Shape(), edge)
					nearest_point1 = extrema.PointOnShape1(1)
					nearest_point2 = extrema.PointOnShape2(1)
					if Distance > nearest_point1.Distance(nearest_point2) or Distance == 0:
						Distance = nearest_point1.Distance(nearest_point2)
						shape_id = key
					pass
				except Exception as e:
					print(e)
					pass

			try:
				point0 = self.show_line_dict[shape_id].get_end_point_pnt(0)
				point1 = self.show_line_dict[shape_id].get_end_point_pnt(1)
				if point0.Distance(gp_Pnt(x, y, z)) <= 10:
					x = point0.X()
					y = point0.Y()
					z = point0.Z()
				elif point1.Distance(gp_Pnt(x, y, z)) <= 10:
					x = point1.X()
					y = point1.Y()
					z = point1.Z()
				else:
					(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()
			except Exception as e:
				print(e)
				pass
		return x, y, z, vx, vy, vz



	def draw_line(self,shape=None):
			if self.parent.InteractiveOperate.InteractiveModule == "SKETCH":
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()
				(x, y, z, vx, vy, vz)=self.catch_capure_point(shape)

				if len(self.point_count) == 0:
					self.point = [x, y, z]
					self.point_count.append(self.point)
					self.show_line_dict[self.line_id] = None
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_drwa_line)
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_draw_trance)

				elif len(self.point_count) >= 1 :
					self.InteractiveModule = None

					if self.capture_point_None!=0:
						print(self.capture_point_None)
						capture_point=BRep_Tool.Pnt(self.capture_point.Vertex())
						x,y,z=capture_point.X(),capture_point.Y(),capture_point.Z()

					p1=self.point
					p2=[x,y,z]
					self.show_line_dict[self.line_id].set_ais_shape(p1,p2)
					self.show_line_dict[self.line_id].redisplay_all()
					self.line_id+=1
					self.point_count.clear()
					self.show_element = self.parent.Sketcher.get_all_sketcher_element()



	def dynamics_draw_trance(self):
		shape_id=0
		Distance=0
		_dragStartPosY = self.parent.Displayshape_core.canva.dragStartPosY
		_dragStartPosX = self.parent.Displayshape_core.canva.dragStartPosX
		(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()
		direction = gp_Dir(vx, vy, vz)
		line = gp_Lin(gp_Pnt(x, y, z), direction)
		edge_builder = BRepBuilderAPI_MakeEdge(line)
		edge = edge_builder.Edge()
		try:
			for key in self.show_element.keys():
				try:
					if key == self.line_id and len(self.point_count) >= 1:
						continue
					if self.show_element == []:
						continue
					extrema = BRepExtrema.BRepExtrema_DistShapeShape(self.show_element[key].ais_shape.Shape(), edge)
					nearest_point1 = extrema.PointOnShape1(1)
					nearest_point2 = extrema.PointOnShape2(1)
					if Distance > nearest_point1.Distance(nearest_point2) or Distance == 0:
						Distance = nearest_point1.Distance(nearest_point2)
						x, y, z = (nearest_point1.X()), (nearest_point1.Y()), (nearest_point1.Z())
						if "line" in key:
							shape_id = int(key.replace("line", ""))
							element=self.parent.Sketcher.new_do_draw_dict["line"].show_line_dict
						elif "rectangle" in key:
							shape_id = int(key.replace("rectangle", ""))
							element = self.parent.Sketcher.new_do_draw_dict["rectangle"].show_line_dict

					pass
				except Exception as e:
					print(e)
					pass

			# 捕捉生产端点和中点,任意点
			if Distance > 15 or Distance == 0:
				self.capture_point_None = 0
				try:
					element[shape_id].remove_capture_point()
					element[shape_id].remove_capture_any_point()
					self.parent.Displayshape_core.canva._display.Repaint()
					self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
				except Exception as e:
					pass
			else:
				try:
					element[shape_id].remove_capture_any_point()
					pnt1=element[shape_id].get_capture_point_pnt(1)
					pnt2=gp_Pnt(x,y,z)
					if pnt2.Distance(pnt1)>=15:
						element[shape_id].set_capture_any_point(x, y, z)
						element[shape_id].display_capture_any_point()

					element[shape_id].display_capture_point()
					self.parent.Displayshape_core.canva._display.Repaint()
					self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
				except Exception as e:
					print(e)


		except:
			pass


	def dynamics_drwa_line(self):
			_dragStartPosY = self.parent.Displayshape_core.canva.dragStartPosY
			_dragStartPosX = self.parent.Displayshape_core.canva.dragStartPosX
			if self.dragStartPosY != _dragStartPosY or self.dragStartPosX != _dragStartPosX:
				
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()
				# print(x, y, z)
				try:
					p1 = self.point
					p2 = [x, y, z]
					if self.show_line_dict[self.line_id] == None:
						self.show_line_dict[self.line_id]=Brep_line(self,p1,p2)

					else:
						self.show_line_dict[self.line_id].set_ais_shape(p1, p2)
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



		
			
