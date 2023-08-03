# -*- coding: utf-8 -*-
from OCC.Core import BRepExtrema
from OCC.Core.BRep import BRep_Tool
from OCC.Core.Geom import Geom_CartesianPoint, Geom_Line
from OCC.Core.Prs3d import Prs3d_PointAspect
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.TopoDS import TopoDS_Vertex, TopoDS_Wire, TopoDS_Builder, TopoDS_Compound
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from GUI.SelectWidget import SelectWidget
import threading
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.GC import GC_MakeSegment, GC_MakeCircle
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Ax2,gp_Dir
from OCC.Core.AIS import AIS_Shape, AIS_Point
from GUI import SketcherWidget


from sketcher.sketcher_line import sketch_line,Brep_line


class sketch_rectangle(sketch_line):
	def __init__(self, parent=None,gp_Dir=None):
		super(sketch_rectangle, self).__init__()
		self.parent = parent
		self.gp_Dir = gp_Dir
		self.dragStartPosX = 0
		self.dragStartPosY = 0
		self.aisline = None
		self.point_count = []
		self.line_dict = {}
		self.pointt_dict = {}
		self.show_line_dict = {}
		self.point_count = []
		self.line_id=0
		sketch_rectangle_gui=SketcherWidget.SketcherWidget(parent=parent)
		sketch_rectangle_gui.show()
		self.draw_line_connect=None
		
	def draw_rectangle(self,shape=None):
			if self.parent.InteractiveOperate.InteractiveModule == "SKETCH":
				if self.draw_line_connect != 1:
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_draw_trance)
					self.draw_trance_element=1


				x, y, z, vx, vy, vz=self.catch_capure_point(shape)#启用端点捕捉
				if len(self.point_count) == 0:
					self.point = (x, y, z)
					self.point_count.append(self.point)
					self.show_line_dict[self.line_id] = None
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.dynamics_drwa_rectangle)


				elif len(self.point_count) >= 1:
					self.InteractiveModule = None
					rectangle_list=self.process_rectangle(self.point_count[0][0],self.point_count[0][1],self.point_count[0][2],x,y,z,model=1)
					self.parent.Displayshape_core.canva._display.Context.Erase(self.show_line_dict[self.line_id],True)
					self.show_line_dict.pop(self.line_id)
					
					for rectangle in rectangle_list:
						try:
							self.show_line_dict[self.line_id]=Brep_line(self,rectangle[0],rectangle[1])  # 将已经显示的零件设置成另外一个新零件
							self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id].ais_shape, True, False)  # 重新计算更新已经显示的物体
							self.parent.Displayshape_core.canva._display.Context.Display(self.show_line_dict[self.line_id].edge_point_list[0], False)  # 显示的物体
							self.parent.Displayshape_core.canva._display.Context.Display(self.show_line_dict[self.line_id].edge_point_list[1], False)  # 显示的物体
						except Exception as e:
							print(e)
						self.line_id+=1
					self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
					self.point_count.clear()
					#self.show_element = self.parent.Sketcher.get_all_sketcher_element()
					#print(self.show_line_dict)
					self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.disconnect(self.dynamics_drwa_rectangle)
		
	def dynamics_drwa_rectangle(self):
			_dragStartPosY = self.parent.Displayshape_core.canva.dragStartPosY
			_dragStartPosX = self.parent.Displayshape_core.canva.dragStartPosX
			if self.dragStartPosY != _dragStartPosY or self.dragStartPosX != _dragStartPosX:
				
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()
				# print(x, y, z)
				try:
					x0 = self.point[0]
					y0 = self.point[1]
					z0 = self.point[2]
					rectangle=self.process_rectangle(x0,y0,z0,x,y,z).Shape()
					
					if self.show_line_dict[self.line_id] == None:
						self.show_line_dict[self.line_id] = AIS_Shape(rectangle)
						self.parent.Displayshape_core.canva._display.Context.Display(self.show_line_dict[self.line_id], True)  # 重新计算更新已经显示的物体
					else:
						self.show_line_dict[self.line_id].SetShape(rectangle)  # 将已经显示的零件设置成另外一个新零件
						self.show_line_dict[self.line_id].SetWidth(self.width)
						self.show_line_dict[self.line_id].SetColor(Quantity_Color(self.color))
					self.parent.Displayshape_core.canva._display.Context.Redisplay(self.show_line_dict[self.line_id], True,
																				   False)  # 重新计算更新已经显示的物体
					self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
				
				except Exception as e:
					pass
			
			self.dragStartPosX = _dragStartPosX
			self.dragStartPosY = _dragStartPosY
	

	def process_rectangle(self,x0,y0,z0,x1,y1,z1,model=0):
		if self.gp_Dir.Z() == 1:  # xy
			P0 = gp_Pnt(x0, y0, z0)
			P1 = gp_Pnt(x1, y0, z0)
			P2 = gp_Pnt(x1, y1, z0)
			P3 = gp_Pnt(x0, y1, z0)
		
		elif self.gp_Dir.Y() == 1:  # xz
			P0 = gp_Pnt(x0, y0, z0)
			P1 = gp_Pnt(x1, y0, z0)
			P2 = gp_Pnt(x1, y0, z1)
			P3 = gp_Pnt(x0, y0, z1)
		elif self.gp_Dir.X() == 1:  # yz
			P0 = gp_Pnt(x0, y0, z0)
			P1 = gp_Pnt(x0, y1, z0)
			P2 = gp_Pnt(x0, y1, z1)
			P3 = gp_Pnt(x0, y0, z1)
		
		aSegment1 = GC_MakeSegment(P0, P1)
		anEdge1 = BRepBuilderAPI_MakeEdge(aSegment1.Value())
		aWire1 = BRepBuilderAPI_MakeWire(anEdge1.Edge())
		aSegment2 = GC_MakeSegment(P1, P2)
		anEdge2 = BRepBuilderAPI_MakeEdge(aSegment2.Value())
		aWire2 = BRepBuilderAPI_MakeWire(anEdge2.Edge())
		aSegment3 = GC_MakeSegment(P2, P3)
		anEdge3 = BRepBuilderAPI_MakeEdge(aSegment3.Value())
		aWire3 = BRepBuilderAPI_MakeWire(anEdge3.Edge())
		aSegment4 = GC_MakeSegment(P3, P0)
		anEdge4 = BRepBuilderAPI_MakeEdge(aSegment4.Value())
		aWire4 = BRepBuilderAPI_MakeWire(anEdge4.Edge())
		if model==0:
			
			aRectangle = BRepBuilderAPI_MakeWire(aWire1.Edge(), aWire2.Edge(), aWire3.Edge(), aWire4.Edge())
		elif model==1:
			#aRectangle = [aWire1, aWire2, aWire3, aWire4]
			P0=[P0.X(),P0.Y(),P0.Z()]
			P1 = [P1.X(), P1.Y(), P1.Z()]
			P2 = [P2.X(), P2.Y(), P2.Z()]
			P3 = [P3.X(), P3.Y(), P3.Z()]
			aRectangle = [[P0,P1], [P1,P2], [P2,P3], [P3,P0]]
		
		
		#self.new_build = TopoDS_Builder()  # 建立一个TopoDS_Builder()
		#self.aCompound = TopoDS_Compound()  # 定义一个复合体
		#self.new_build.MakeCompound(self.aCompound)  # 生成一个复合体DopoDS_shape
		#self.new_build.Add(self.aCompound,aWire1.Shape())
		#self.new_build.Add(self.aCompound, aWire2.Shape())
		#self.new_build.Add(self.aCompound, aWire3.Shape())
		#self.new_build.Add(self.aCompound, aWire4.Shape())
		
		return aRectangle

