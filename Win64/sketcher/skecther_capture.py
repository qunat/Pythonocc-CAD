#-*-coding:utf8-*-
from OCC.Core import BRepExtrema
from OCC.Core.Geom import Geom_CartesianPoint, Geom_Line
from OCC.Core.Prs3d import Prs3d_PointAspect
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
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

from PyQt5 import QtCore
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_BLACK

class sketcher_capture(object):
	def __init__(self,parent=None):
		self.parent = parent
		self.gp_Dir = gp_Dir
		self.dragStartPosX = 0
		self.dragStartPosY = 0
		self.aisline = None
		self.point_count = []
		self.line_dict = {}
		self.point_dict = {}
		self.show_circel_dict = {}
		self.point_count = []
		self.circel_id = 0
		self.draw_circel_connect = None
		self.ais_point = None
		self.ais_point_dict = {}
		self.perious_ais_point_ID = None
		self.mousePress_select_point_ID = None
		self.bspline_curve = None
		self.bspline_curve_dict = None
		self.dialogWidget = None
		self.Distance = 0
		self.dynamics_point_move_point_shield = False
		self.windownname=self.parent.ModuleWindowManager.GetWindownName()
		print("sketcher_capture init")
		#self.parent.Displayshape_core_dict[self.windownname].canva.mouse_move_Signal.trigger.connect(self.dynamics_point_highlight)
		#self.parent.Displayshape_core_dict[self.windownname].canva.mousePressEvent_Signal.trigger.connect(self.mousepress)
		
	def mousepress(self):
		if self.parent.Displayshape_core_dict[self.windownname].canva.mousepresstype == QtCore.Qt.LeftButton:
			(x, y, z, vx, vy, vz) = self.parent.Displayshape_core_dict[self.windownname].ProjReferenceAxe()
			if self.ais_point == None:
				self.perious_ais_point_ID = None
			else:
				self.mousePress_select_point_ID = self.perious_ais_point_ID
			
			try:
				self.parent.Displayshape_core_dict[self.windownname].canva._display.Context.Remove(self.ais_point, False)
				self.parent.Displayshape_core_dict[self.windownname].canva.mouse_move_Signal.trigger.disconnect(self.dynamics_point_highlight)
				self.parent.Displayshape_core_dict[self.windownname].canva.mouse_move_Signal.trigger.connect(self.dynamics_point_move_point)
				self.parent.Displayshape_core_dict[self.windownname].canva.mouseReleaseEvent_Signal.trigger.connect(self.mouserelease)
			except Exception as e:
				print("提前结束")
				pass
			
			print("mouse press id", self.perious_ais_point_ID, self.ais_point, self.dialogWidget)
		
	
	def mouserelease(self):
		try:
			self.parent.Displayshape_core_dict[self.windownname].canva.mouse_move_Signal.trigger.disconnect(self.dynamics_point_move_point)
			self.parent.Displayshape_core_dict[self.windownname].canva.mouse_move_Signal.trigger.connect(self.dynamics_point_highlight)
		except:
			pass
	
	def dynamics_point_highlight(self):
		shape_id = 0
		Distance = 0
		_dragStartPosY = self.parent.Displayshape_core_dict[self.windownname].canva.dragStartPosY
		_dragStartPosX = self.parent.Displayshape_core_dict[self.windownname].canva.dragStartPosX
		(x, y, z, vx, vy, vz) = self.parent.Displayshape_core_dict[self.windownname].ProjReferenceAxe()
		direction = gp_Dir(vx, vy, vz)
		line = gp_Lin(gp_Pnt(x, y, z), direction)
		edge_builder = BRepBuilderAPI_MakeEdge(line)
		edge = edge_builder.Edge()
		if self.ais_point == None:
			for ID in self.point_dict.keys():
				try:
					extrema = BRepExtrema.BRepExtrema_DistShapeShape(self.show_element[key].ais_shape.Shape(), edge)
					nearest_point1 = extrema.PointOnShape1(1)
					nearest_point2 = extrema.PointOnShape2(1)
					if Distance > nearest_point1.Distance(nearest_point2) or Distance == 0:
						Distance = nearest_point1.Distance(nearest_point2)
						x, y, z = (nearest_point2.X()), (nearest_point2.Y()), (nearest_point2.Z())
						self.perious_ais_point_ID = ID

				
				except Exception as e:
					print(e)
					pass
			
			if Distance < 20 * (1 / self.parent.Displayshape_core_dict[self.windownname].canva.scaling_ratio):
				self.draw_point(x, y, 0, 0, None, 9, [0, 0, 255])
				self.Distance = Distance
			
			elif Distance > 20 * (1 / self.parent.Displayshape_core_dict[self.windownname].canva.scaling_ratio) and self.ais_point != None:
				self.perious_ais_point_ID = None
				self.Distance = 50
				pass
		
		
		else:
			try:
				_dragStartPosY = self.parent.Displayshape_core_dict[self.windownname].canva.dragStartPosY
				_dragStartPosX = self.parent.Displayshape_core_dict[self.windownname].canva.dragStartPosX
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core_dict[self.windownname].ProjReferenceAxe()
				direction = gp_Dir(vx, vy, vz)
				nearest_point1 = gp_Pnt(x, y, 0)
				Distance = self.point_dict[self.perious_ais_point_ID].Distance(nearest_point1)
				if Distance > 20 * (1 / self.parent.Displayshape_core_dict[self.windownname].canva.scaling_ratio):
					self.parent.Displayshape_core_dict[self.windownname].canva._display.Context.Remove(self.ais_point, False)
					self.ais_point = None
					self.perious_ais_point_ID = None
					print("yes")
			except Exception as e:
				print(e)
				pass
	
	def dynamics_point_move_point(self):
		if self.perious_ais_point_ID != None and self.ais_point == None:
			self.dynamics_point_move_point_shield = True
			self.parent.Displayshape_core_dict[self.windownname].canva._display.Context.Remove(self.ais_point_dict[self.perious_ais_point_ID],
																		False)
			(x, y, z, vx, vy, vz) = self.parent.Displayshape_core_dict[self.windownname].ProjReferenceAxe()
			# ------------------------------------
			self.dialogWidget.qdoubleSpinBox_x.setValue(x)
			self.dialogWidget.qdoubleSpinBox_y.setValue(y)
			self.dialogWidget.qdoubleSpinBox_z.setValue(z)
			
			self.mousePress_select_point_ID = self.perious_ais_point_ID
			self.ais_point_dict[self.perious_ais_point_ID] = self.draw_point(x, y, 0, 1)
			self.parent.Displayshape_core_dict[self.windownname].canva._display.Context.Display(self.ais_point_dict[self.perious_ais_point_ID],
																		 False)
			self.parent.Displayshape_core_dict[self.windownname].canva._display.Context.UpdateCurrentViewer()
			bspline_curve = self.generate_bspline(self.perious_ais_point_ID, gp_Pnt(x, y, z))
			edge = BRepBuilderAPI_MakeEdge(bspline_curve).Edge()
			self.bspline_curve.SetShape(edge)
			self.parent.Displayshape_core_dict[self.windownname].canva._display.Context.Redisplay(self.bspline_curve, True,
																		   False)  # 重新计算更新已经显示的物
			self.parent.Displayshape_core_dict[self.windownname].canva._display.Repaint()
			self.parent.Displayshape_core_dict[self.windownname].canva._display.Context.UpdateCurrentViewer()
			self.dynamics_point_move_point_shield = False
	
	def draw_point(self, x, y, z, mode=0, id=None, point_type=0, color=None):
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
		if mode == 0:
			if point_type != None:
				point_type = ALL_ASPECTS[point_type]
				p = Geom_CartesianPoint(gp_Pnt(x, y, z))
				if color != None:
					color = Quantity_Color(color[0] / 255, color[1] / 255, color[2] / 255, Quantity_TOC_RGB)
				
				else:
					color = Quantity_Color(0, 0, 0, Quantity_TOC_RGB)
				
				if id == None:
					self.ais_point = AIS_Point(p)
					drawer = self.ais_point.Attributes()
					asp = Prs3d_PointAspect(ALL_ASPECTS[point_type], color, 3)
					drawer.SetPointAspect(asp)
					self.ais_point.SetAttributes(drawer)
					self.parent.Displayshape_core_dict[self.windownname].canva._display.Context.Display(self.ais_point,
																				 False)  # 重新计算更新已经显示的物
				
				else:
					self.ais_point_dict[id] = AIS_Point(p)
					drawer = self.ais_point_dict[id].Attributes()
					asp = Prs3d_PointAspect(ALL_ASPECTS[point_type], color, 3)
					drawer.SetPointAspect(asp)
					self.ais_point_dict[id].SetAttributes(drawer)
					
					self.parent.Displayshape_core_dict[self.windownname].canva._display.Context.Display(self.ais_point_dict[id],
																				 False)  # 重新计算更新已经显示的物
		
		
		elif mode == 1:
			if point_type != None:
				point_type = ALL_ASPECTS[point_type]
				p = Geom_CartesianPoint(gp_Pnt(x, y, z))
				if color != None:
					color = Quantity_Color(color[0] / 255, color[1] / 255, color[2] / 255, Quantity_TOC_RGB)
				
				else:
					color = Quantity_Color(0, 0, 0, Quantity_TOC_RGB)
				
				ais_point = AIS_Point(p)
				drawer = ais_point.Attributes()
				asp = Prs3d_PointAspect(ALL_ASPECTS[point_type], color, 3)
				drawer.SetPointAspect(asp)
				ais_point.SetAttributes(drawer)
				
				return ais_point