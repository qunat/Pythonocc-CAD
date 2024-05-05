from OCC.Core.AIS import AIS_Shape
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.GC import GC_MakeArcOfCircle
from OCC.Core.gp import gp_Trsf, gp_Vec, gp_Pnt,gp_Dir,gp_Circ,gp_Ax2,gp_Lin,gp_Ax1
import math

class Surface(object):
	def __init__(self,parent=None):
		self.parent=parent
		print("init ok")
		pass
	
	def swept(self):
		point0 = [0, 0, 0]
		point1 = [1020, 0, 0]
		point2 = [1020, 470, 0]
		point3 = [0, 470, 0]
		edge0 = BRepBuilderAPI_MakeEdge(gp_Pnt(point0[0], point0[1], point0[2]),
										gp_Pnt(point1[0], point1[1], point1[2])).Edge()
		edge1 = BRepBuilderAPI_MakeEdge(gp_Pnt(point1[0], point1[1], point1[2]),
										gp_Pnt(point2[0], point2[1], point2[2])).Edge()
		edge2 = BRepBuilderAPI_MakeEdge(gp_Pnt(point2[0], point2[1], point2[2]),
										gp_Pnt(point3[0], point3[1], point3[2])).Edge()
		edge3 = BRepBuilderAPI_MakeEdge(gp_Pnt(point3[0], point3[1], point3[2]),
										gp_Pnt(point0[0], point0[1], point0[2])).Edge()
		
		rectange = BRepBuilderAPI_MakeWire(edge0, edge1, edge2, edge3).Wire()
		
		Axis = gp_Dir(1, 0, 0)
		CircleAxis = gp_Ax2(gp_Pnt(1020, -5441.94799169662, 2556.43344201923), Axis)
		Circle = gp_Circ(CircleAxis, 6441)
		
		print("ok0")
		try:
			ArcofCircle0 = GC_MakeArcOfCircle(Circle, gp_Pnt(1020, 470, 0), gp_Pnt(1020, 650, 4648),True)
			spline = BRepBuilderAPI_MakeEdge(ArcofCircle0.Value()).Edge()
		except Exception as e:
			print(e)
		print("ok1")
		wire = BRepBuilderAPI_MakeWire(spline).Wire()
		
		print("ok1")
		point0 = [0, 0, 0]
		point1 = [0, 0, 4583]
		edeg = BRepBuilderAPI_MakeEdge(gp_Pnt(point0[0], point0[1], point0[2]),
									   gp_Pnt(point1[0], point1[1], point1[2])).Edge()
		print("ok2")
		profile_face = BRepBuilderAPI_MakeFace(rectange).Face()
		pipe = BRepOffsetAPI_MakePipe(wire, profile_face).Shape()
		ais_shape = AIS_Shape(pipe)
		self.parent.Displayshape_core.canva._display.Context.Display(ais_shape,False)  # 重新计算更新已经显示的物