# -*- coding: utf-8 -*-
import threading
import time

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.GC import GC_MakeSegment
from OCC.Core.Graphic3d import Graphic3d_Group, Graphic3d_MarkerImage, Graphic3d_AspectMarker3d
from OCC.Core.Prs3d import Prs3d_PointAspect
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.gp import gp_Pnt
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Aspect import Aspect_TOM_PLUS,Aspect_TOM_O,Aspect_TOM_X,Aspect_TOHM_COLOR,Aspect_TOM_BALL
from OCC.Core.TopAbs import TopAbs_VERTEX,TopAbs_FACE,TopAbs_EDGE,TopAbs_SOLID
from OCC.Core.AIS import AIS_Shape, AIS_Shaded, AIS_TexturedShape, AIS_WireFrame, AIS_Shape_SelectionMode
from OCC.Core.Graphic3d import Graphic3d_AspectMarker3d

class InteractiveOperate(object):
	def __init__(self,parent=None):
		self.parent=parent
		self.InteractiveModule=None
		self.select_shape_list=[]
		self.dragStartPosX = 0
		self.dragStartPosY = 0
		self.aisline=None
		self.point_count=[]
		self.InteractiveClose=None

	def Setting(self,Prs3d_TypeOfHighlight=0):
		self.parent.Displayshape_core.canva._display.Context.SetAutomaticHilight(True)
		self.parent.Displayshape_core.canva._display.SetSelectionMode(TopAbs_VERTEX)
		self.parent.Displayshape_core.canva._display.Context.Deactivate()
		self.parent.Displayshape_core.canva._display.Context.Activate(AIS_Shape_SelectionMode(TopAbs_FACE),True)
		self.parent.Displayshape_core.canva._display.Context.UpdateSelected(True)
		self.parent.Displayshape_core.canva._display.Context.SetAutoActivateSelection(True)
		
		HighlightStyle = self.parent.Displayshape_core.canva._display.Context.HighlightStyle()
		HighlightStyle.SetColor(Quantity_Color(255 / 255, 128 / 255, 0 / 255, Quantity_TOC_RGB))
		SelectionStyle = self.parent.Displayshape_core.canva._display.Context.SelectionStyle()
		HighlightStyle.SetMethod(Aspect_TOHM_COLOR)  # 颜色显示方式
		# SelectionStyle.SetMethod(Aspect_TOHM_COLOR)# 颜色显示方式
		SelectionStyle.SetColor(Quantity_Color(0 / 255, 0 / 255, 0 / 255, Quantity_TOC_RGB))  # 设置选择后颜色
		SelectionStyle.SetDisplayMode(0)  # 整体高亮
		#aspectMarker = Graphic3d_AspectMarker3d(Aspect_TOM_PLUS)
		
		asp = Prs3d_PointAspect(Aspect_TOM_BALL, Quantity_Color(1.0, 0.5, 1.0, Quantity_TOC_RGB), 20)
		#asp.SetTypeOfMarker(Prs3d_TOM_CIRCLE)
		#SetTypeOfMarker(Prs3d_TypeOfMarker::Prs3d_TOM_CIRCLE)
		asp.SetScale( 2)
		HighlightStyle.SetPointAspect(asp)
		self.parent.Displayshape_core.canva._display.Context.SetHighlightStyle(0,HighlightStyle)
		self.parent.Displayshape_core.canva._display.Context.SetSelectionStyle(SelectionStyle)
		self.parent.Displayshape_core.canva._display.SetSelectionMode(TopAbs_VERTEX)
		self.parent.Displayshape_core.canva._display.SetSelectionMode(-1)

		# SelectionStyle.t_select_style->SetDisplayMode(1)#整体高亮
		# t_select_style->SetTransparency(0.1)
		# 高亮点的样式设置
		# aspectMarker=Graphic3d_AspectMarker3d(Aspect_TOM_PLUS)
		# aspectMarker.SetColor(Quantity_Color(1.0, 0.0, 0.0, Quantity_TOC_RGB))
		#self.parent.Displayshape_core.canva._display.Context.SetHighlightStyle(aspectMarker)
		#SetMethod()
		#myGroup = Graphic3d_Group(self.parent.Displayshape_core.canva._display.GetView())
		#myMarker = Graphic3d_MarkerImage(Aspect_TOM_O, Quantity_Color(c), 8, 1)
		#myGroup.Marker(myMarker)



 

