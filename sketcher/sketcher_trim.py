# -*- coding: utf-8 -*-
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
		self.sketch_show=[]
		self.line_id=0
		self.get_all_sketch_show()



	def get_all_sketch_show(self):
		lines=self.parent.Sketcher.new_do_draw_dict["line"].show_line_dict.values()
		#circels=self.parent.Sketcher.new_do_draw_dict["circel"].show_circel_dict.values()
		for line in lines:
			self.sketch_show.append(line)
		print(self.sketch_show)

	def trim(self,shape=None):
		for shp in self.sketch_show:
			try:
				# 创建线段修剪器对象
				print(shape)
				if shp[0].Shape().IsSame(shape[0]):
					continue
				extrema = BRepExtrema.BRepExtrema_DistShapeShape(shp[0].Shape(), shape[0])
				nearest_point = extrema.PointOnShape1(1)
				x, y, z = nearest_point.X(), nearest_point.Y(), nearest_point.Z()
				trim_point=gp_Pnt(x,y,z)
				point = self.parent.Displayshape_core.canva._display.DisplayShape(gp_Pnt(x, y, z), color="YELLOW",
																				  update=False	)  # 重新计算更新已经显示的物
				self.parent.Displayshape_core.canva._display.Repaint()
				explorer=BRepTools_WireExplorer(shape[0])
				startVertex = explorer.CurrentVertex()
				explorer.Next()

				endVertex = explorer.CurrentVertex()
				explorer.Next()
				P1 = BRep_Tool.Pnt(startVertex)  # 转换为pnt数据
				P2 = BRep_Tool.Pnt(endVertex)  # 转换为pnt数据

				#P1 = P1.Coord()
				#P2 = P2.Coord()
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(
					self.parent.Displayshape_core.canva.dragStartPosX,
					self.parent.Displayshape_core.canva.dragStartPosY)
				mouse_point=gp_Pnt(x,y,z)
				distance1=P1.Distance(mouse_point)
				distance2= P2.Distance(mouse_point)
				if distance1>distance2:
					end_point=P1
				else:
					end_point=P2

				aSegment = GC_MakeSegment(trim_point,end_point)
				anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
				aWire = BRepBuilderAPI_MakeWire(anEdge.Edge()).Shape()
				self.parent.Sketcher.new_do_draw_dict["line"].show_line_dict[0][0].SetShape(aWire)  # 将已经显示的零件设置成另外一个新零件
				self.parent.Sketcher.new_do_draw_dict["line"].show_line_dict[0][0].SetWidth(self.width)
				self.parent.Sketcher.new_do_draw_dict["line"].show_line_dict[0][0].SetColor(Quantity_Color(self.color))
				self.parent.Displayshape_core.canva._display.Context.Redisplay(self.parent.Sketcher.new_do_draw_dict["line"].show_line_dict[0][0],
																			   True,
																			   False)  # 重新计算更新已经显示的物体






			except Exception as e:
				print(e)
				pass


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
		
		
			
