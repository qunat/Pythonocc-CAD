# -*- coding: utf-8 -*-
import math

from OCC.Core import BRepExtrema
from OCC.Core.BRep import BRep_Tool
from OCC.Core.GCE2d import GCE2d_MakeLine
from OCC.Core.Geom import Geom_CartesianPoint, Geom_Line
from OCC.Core.Prs3d import Prs3d_PointAspect
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import TopoDS_Vertex, TopoDS_Wire, TopoDS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from PyQt5.QtGui import QCursor, QPixmap

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
		self.middle_poind_list=[]
		self.ais_shape=None
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
		self.redisplay()

	def display_line(self):
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.ais_shape,False)#显示的物体
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.edge_point_list[0], False)  # 显示的物体
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.edge_point_list[1], False)  # 显示的物体

	def redisplay(self):
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.edge_point_list[0], False)  # 显示的物体
		self.parent.parent.Displayshape_core.canva._display.Context.Display(self.edge_point_list[1], False)  # 显示的物体
		self.parent.parent.Displayshape_core.canva._display.Context.Redisplay(self.ais_shape, True,False) #重新计算更新已经显示的物体
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


	def draw_line(self,shape=None):
			if self.parent.InteractiveOperate.InteractiveModule == "SKETCH":
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()

				
				if shape!=[] and isinstance(shape[0],TopoDS_Vertex) :#捕捉端点
					P = BRep_Tool.Pnt(shape[0])
					x,y,z=P.X(),P.Y(),P.Z()
					print("enter1")
					
				if shape!=[] and isinstance(shape[0],TopoDS_Wire) :#捕捉线上任意点
					direction = gp_Dir(vx, vy, vz)
					line = gp_Lin(gp_Pnt(x, y, z), direction)
					ais_line = Geom_Line(line)
					edge_builder = BRepBuilderAPI_MakeEdge(line)
					edge = edge_builder.Edge()
					extrema = BRepExtrema.BRepExtrema_DistShapeShape(shape[0], edge)
					nearest_point = extrema.PointOnShape1(1)
					x, y, z = nearest_point.X(), nearest_point.Y(), nearest_point.Z()
				if shape==[]:
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
								x, y, z = (nearest_point1.X()), (nearest_point1.Y()), (nearest_point1.Z())
								shape_id = key
							pass
						except Exception as e:
							print(e)
							pass
					# 捕捉生产端点
					try:
						if self.show_line_dict[shape_id].edge_point_list[0].Distance(gp_Pnt(x, y, z))<=6:
							print("这就是端点")
						if self.show_line_dict[shape_id].edge_point_list[1].Distance(gp_Pnt(x, y, z))<=6:
							print("这就是端点")
					except Exception as e:
						pass

					if Distance > 10 or Distance == 0:
						self.capture_point_None = 0
					else:
						self.capture_point_None = 1


					
				
				if len(self.point_count) == 0:
					#self.draw_point(x,y,z)
					self.point = [x, y, z]
					self.point_count.append(self.point)
					self.show_line_dict[self.line_id] = None
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_drwa_line)
					#self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_draw_trance)

					
					
				elif len(self.point_count) >= 1 :
					print("mouse point", x, y, z,vx, vy, vz)
					self.InteractiveModule = None
					#self.draw_point(x, y, z)# end point

					if self.capture_point_None!=0:
						print(self.capture_point_None)
						capture_point=BRep_Tool.Pnt(self.capture_point.Vertex())
						x,y,z=capture_point.X(),capture_point.Y(),capture_point.Z()

					#print("capture_point",x,y,z)
					p1=self.point
					p2=[x,y,z]
					self.show_line_dict[self.line_id].set_ais_shape(p1,p2)
					self.line_id+=1
					self.point_count.clear()



	def dynamics_draw_trance(self):
		shape_id=0
		Distance=0
		_dragStartPosY = self.parent.Displayshape_core.canva.dragStartPosY
		_dragStartPosX = self.parent.Displayshape_core.canva.dragStartPosX
		(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()
		direction = gp_Dir(vx, vy, vz)
		line = gp_Lin(gp_Pnt(x, y, z), direction)
		#ais_line = Geom_Line(line)
		edge_builder = BRepBuilderAPI_MakeEdge(line)
		edge = edge_builder.Edge()
		for key in self.show_line_dict.keys():
			try:
				if key==self.line_id  and len(self.point_count) >= 1:
					continue
				extrema = BRepExtrema.BRepExtrema_DistShapeShape(self.show_line_dict[key].Shape(), edge)
				nearest_point1 = extrema.PointOnShape1(1)
				nearest_point2 = extrema.PointOnShape2(1)
				if Distance>nearest_point1.Distance(nearest_point2) or Distance==0:
					Distance=nearest_point1.Distance(nearest_point2)
					x, y, z = (nearest_point1.X()), (nearest_point1.Y()), (nearest_point1.Z())
					shape_id=key
				pass
			except Exception as e:
				print(e)
				pass
		#捕捉生产端点和中点
		if Distance>10 or Distance==0:
			self.capture_point_None=0
		else:
			self.capture_point_None = 1
			print(self.show_line_dict[shape_id].Shape())
			edge=self.show_line_dict[shape_id].Shape()
			vertex_explorer = TopExp_Explorer(edge, TopAbs_VERTEX)
			v1 = TopoDS_Vertex(vertex_explorer.Current())
			vertex_explorer.Next()
			v2 = TopoDS_Vertex(vertex_explorer.Current())
			p1=BRep_Tool.Pnt(v1)
			p2 = BRep_Tool.Pnt(v2)
			self.draw_point(p1.X(),p1.Y(),p1.Z())
			self.draw_point(p2.X(), p2.Y(), p2.Z())



		if len(self.show_line_dict.keys())!=0 and 0<Distance<=10:
			#pixmap = QPixmap('./icons/cursorlocation_2l-transformed.png')
			# 2. 将光标对象传入鼠标对象中
			#cursor = QCursor(pixmap)
			# 3. 设置控件的光标
			#self.parent.setCursor(cursor)
			p = Geom_CartesianPoint(gp_Pnt(x, y, z))
			color = Quantity_Color(0, 0, 0, Quantity_TOC_RGB)
			if self.capture_point_list==[]:
				pass
				self.capture_point= AIS_Point(p)
				self.parent.Displayshape_core.canva._display.Context.Display(self.capture_point,False)  # 重新计算更新已经显示的物
				self.capture_point_list.append(self.capture_point)
			elif len(self.capture_point_list)==1:
				pass
				self.parent.Displayshape_core.canva._display.Context.Remove(self.capture_point,True)
				self.capture_point = AIS_Point(p)
				self.capture_point.Redisplay()
				self.parent.Displayshape_core.canva._display.Context.Display(self.capture_point,False)  # 重新计算更新已经显示的物体
				self.parent.Displayshape_core.canva._display.Repaint()
		else:
			self.parent.unsetCursor()






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
			point = self.parent.Displayshape_core.canva._display.Context.Display(ais_point,
																				 False)  # 重新计算更新已经显示的物
		else:
			point = self.parent.Displayshape_core.canva._display.DisplayShape(gp_Pnt(x,y,z),color="YELLOW",
																			update=False	 )  # 重新计算更新已经显示的物
			self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
			self.parent.Displayshape_core.canva._display.Repaint()



		
			
