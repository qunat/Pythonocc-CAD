# -*- coding: utf-8 -*-
import math

from OCC.Core import BRepExtrema, BRepAlgoAPI, TopoDS, BRepBuilderAPI, TopExp, TopAbs
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepTools import BRepTools_WireExplorer
from OCC.Core.Geom import Geom_CartesianPoint, Geom_Line
from OCC.Core.Prs3d import Prs3d_PointAspect
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.TopExp import topexp
from OCC.Core.TopoDS import TopoDS_Vertex, TopoDS_Wire, TopoDS_Edge
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Extend.TopologyUtils import TopologyExplorer

from GUI.SelectWidget import SelectWidget
import threading
from OCC.Core.Quantity import *
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_BLACK
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.GC import GC_MakeSegment, GC_MakeCircle
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Ax2,gp_Dir
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

class sketch_trim(object):
	def __init__(self, parent=None,width=2,color=Quantity_NOC_BLACK):
		self.parent = parent
		self.width = width
		self.color=color
		self.sketch_show_dict= {}
		self.line_id=0
		self.get_all_sketch_show()



	def get_all_sketch_show(self):
		try:
			if self.parent.Sketcher.new_do_draw_dict["line"].show_line_dict != []:
				lines = self.parent.Sketcher.new_do_draw_dict["line"].show_line_dict.keys()
				for key in lines:
					lable = "line" + str(key)
					self.sketch_show_dict[lable] = self.parent.Sketcher.new_do_draw_dict["line"].show_line_dict[key]
		except:
			pass

		try:
			if self.parent.Sketcher.new_do_draw_dict["rectangle"].show_line_dict != []:
				rectangles = self.parent.Sketcher.new_do_draw_dict["rectangle"].show_line_dict.keys()
				for key in rectangles:
					lable = "rectangle" + str(key)
					self.sketch_show_dict[lable] = self.parent.Sketcher.new_do_draw_dict["rectangle"].show_line_dict[
						key]
		except:
			pass



	
		print(self.sketch_show_dict)

	def trim(self,shape=None):
		self.sketch_show_dict = {}
		self.get_all_sketch_show()
		trim_point_min_1 = None
		trim_point_min_2 = None
		distan_min_1 = 0
		distan_min_2 = 0
		type=None
		print(shape)
		for key in self.sketch_show_dict.keys():
			try:
				# 创建线段修剪器对象
				if key[0:4]=="line":
					key = int(key.replace("line", ""))
					shp = self.parent.Sketcher.new_do_draw_dict["line"].show_line_dict[key]
					if shp.Shape().IsSame(shape[0]):
						type = "line"
						trim_shape_key = key
						continue

				elif key[0:9]=="rectangle":
					key = int(key.replace("rectangle", ""))
					shp = self.parent.Sketcher.new_do_draw_dict["rectangle"].show_line_dict[key]
					if shp.Shape().IsSame(shape[0]):
						trim_shape_key = key
						type = "rectangle"
						continue


				extrema = BRepExtrema.BRepExtrema_DistShapeShape(shp.Shape(), shape[0])
				nearest_point_1 = extrema.PointOnShape1(1)
				nearest_point_2 = extrema.PointOnShape2(1)

				if math.floor(nearest_point_1.Distance(nearest_point_2)) != 0:
					continue
				x, y, z = nearest_point_1.X(), nearest_point_1.Y(), nearest_point_1.Z()
				trim_point = gp_Pnt(x, y, z)

				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(
					self.parent.Displayshape_core.canva.dragStartPosX,
					self.parent.Displayshape_core.canva.dragStartPosY)
				mouse_point = gp_Pnt(x, y, z)
				distance = trim_point.Distance(mouse_point)

				if distan_min_1 == 0:
					distan_min_1 = distance
					trim_point_min_1 = trim_point

				elif distance < distan_min_1:
					trim_point_min_2 = trim_point_min_1
					distan_min_2 = distan_min_1
					distan_min_1 = distance
					trim_point_min_1 = trim_point
				else:
					if distance < distan_min_2 or distan_min_2 == 0:
						distan_min_2 = distance
						trim_point_min_2 = trim_point

				if trim_point_min_2==None:
					trim_point_min_2=trim_point_min_1
			except Exception as e:
				print(e)
				pass
		#----------------------------------------------------line_trim-----------------------------------------------
		self.trim_line(shape,trim_point_min_1, trim_point_min_2, distan_min_1, distan_min_2, trim_shape_key,type)




	def trim_line(self, shape, trim_point_min_1, trim_point_min_2, distan_min_1, distan_min_2, trim_shape_key,type="line"):
		#To do trim line

		distance = trim_point_min_1.Distance(trim_point_min_2)
		point = self.parent.Displayshape_core.canva._display.DisplayShape(trim_point_min_1, color="YELLOW",
																		  update=False)  # 重新计算更新已经显示的物
		self.parent.Displayshape_core.canva._display.Repaint()
		point = self.parent.Displayshape_core.canva._display.DisplayShape(trim_point_min_2, color="YELLOW",
																		  update=False)  # 重新计算更新已经显示的物
		self.parent.Displayshape_core.canva._display.Repaint()
		# --------------------------------------------------------------------------------------------------
		explorer = BRepTools_WireExplorer(shape[0])
		startVertex = explorer.CurrentVertex()
		explorer.Next()

		endVertex = explorer.CurrentVertex()
		explorer.Next()
		P1 = BRep_Tool.Pnt(startVertex)  # 转换为pnt数据
		P2 = BRep_Tool.Pnt(endVertex)  # 转换为pnt数据

		(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(
			self.parent.Displayshape_core.canva.dragStartPosX,
			self.parent.Displayshape_core.canva.dragStartPosY)
		mouse_point = gp_Pnt(x, y, z)

		if math.floor(distan_min_1 + distan_min_2) == math.floor(distance) and distance!=0:

			distance1 = P1.Distance(trim_point_min_1)
			distance2 = P1.Distance(trim_point_min_2)
			if distance1 < distance2:
				end_point_1 = P1
				end_point_2 = P2
			else:
				end_point_1 = P2
				end_point_2 = P1

			aSegment = GC_MakeSegment(trim_point_min_1, end_point_1)
			anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
			aWire = BRepBuilderAPI_MakeWire(anEdge.Edge()).Shape()
			self.parent.Sketcher.new_do_draw_dict[type].show_line_dict[trim_shape_key].SetShape(
				aWire)  # 将已经显示的零件设置成另外一个新零件
			self.parent.Sketcher.new_do_draw_dict[type].show_line_dict[trim_shape_key].SetWidth(self.width)
			self.parent.Sketcher.new_do_draw_dict[type].show_line_dict[trim_shape_key].SetColor(
				Quantity_Color(Quantity_NOC_BLACK))
			self.parent.Displayshape_core.canva._display.Context.Redisplay(
				self.parent.Sketcher.new_do_draw_dict[type].show_line_dict[trim_shape_key], True,
				False)  # 重新计算更新已经显示的物体

			aSegment = GC_MakeSegment(trim_point_min_2, end_point_2)
			anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
			aWire = BRepBuilderAPI_MakeWire(anEdge.Edge()).Shape()

			key = self.parent.Sketcher.new_do_draw_dict[type].line_id
			self.parent.Sketcher.new_do_draw_dict[type].show_line_dict[key] = AIS_Shape(aWire)
			self.parent.Sketcher.new_do_draw_dict[type].show_line_dict[key].SetWidth(self.width)
			self.parent.Sketcher.new_do_draw_dict[type].show_line_dict[key].SetColor(Quantity_Color(self.color))
			self.parent.Displayshape_core.canva._display.Context.Display(
				self.parent.Sketcher.new_do_draw_dict[type].show_line_dict[key], True)  # 重新计算更新已经显示的物体
			self.parent.Sketcher.new_do_draw_dict[type].line_id +=1

		else:
			distance1 = P1.Distance(mouse_point)
			distance2 = P2.Distance(mouse_point)
			if distance1 > distance2:
				end_point = P1
			else:
				end_point = P2

			if math.ceil(trim_point_min_1.Distance(P1))==0 or math.ceil(trim_point_min_1.Distance(P2))==0:#交点和端的重合
				self.parent.Displayshape_core.canva._display.Context.Erase(self.parent.Sketcher.new_do_draw_dict[type].show_line_dict[trim_shape_key],True)
				self.parent.Sketcher.new_do_draw_dict[type].show_line_dict.pop(trim_shape_key)

			else:
				aSegment = GC_MakeSegment(trim_point_min_1, end_point)
				anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
				aWire = BRepBuilderAPI_MakeWire(anEdge.Edge()).Shape()
				self.parent.Sketcher.new_do_draw_dict[type].show_line_dict[trim_shape_key].SetShape(
					aWire)  # 将已经显示的零件设置成另外一个新零件
				self.parent.Sketcher.new_do_draw_dict[type].show_line_dict[trim_shape_key].SetWidth(self.width)
				self.parent.Sketcher.new_do_draw_dict[type].show_line_dict[trim_shape_key].SetColor(
					Quantity_Color(self.color))
				self.parent.Displayshape_core.canva._display.Context.Redisplay(
					self.parent.Sketcher.new_do_draw_dict[type].show_line_dict[trim_shape_key], True,
					False)  # 重新计算更新已经显示的物体




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
		
		
			
