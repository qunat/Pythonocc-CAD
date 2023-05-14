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
from OCC.Core.Aspect import Aspect_TOM_PLUS,Aspect_TOM_O

class InteractiveOperate(object):
	def __init__(self,parent=None):
		self.parent=parent
		self.InteractiveModule=None
		self.select_shape_list=[]
		self.dragStartPosX = 0
		self.dragStartPosY = 0
		self.aisline=None
		self.point_count=[]

	def Setting(self):
		HighlightStyle = self.parent.Displayshape_core.canva._display.Context.HighlightStyle()
		HighlightStyle.SetColor(Quantity_Color(0 / 255, 128 / 255, 0 / 255, Quantity_TOC_RGB))
		SelectionStyle = self.parent.Displayshape_core.canva._display.Context.SelectionStyle()
		HighlightStyle.SetMethod(Aspect_TOM_O)# 颜色显示方式
		# SelectionStyle.SetMethod(Aspect_TOHM_COLOR)# 颜色显示方式
		SelectionStyle.SetColor(Quantity_Color(0 / 255, 0 / 255, 0 / 255, Quantity_TOC_RGB))  # 设置选择后颜色
		# SelectionStyle.t_select_style->SetDisplayMode(1)#整体高亮
		# t_select_style->SetTransparency(0.1)

		#高亮点的样式设置
		#aspectMarker=Graphic3d_AspectMarker3d(Aspect_TOM_PLUS)
		#aspectMarker.SetColor(Quantity_Color(1.0, 0.0, 0.0, Quantity_TOC_RGB))
		#asp = Prs3d_PointAspect(Aspect_TOM_PLUS, Quantity_Color(1.0, 0.0, 0.0, Quantity_TOC_RGB), 4)


		self.parent.Displayshape_core.canva._display.Context.SetSelectionStyle(HighlightStyle)
		self.parent.Displayshape_core.canva._display.Context.SetSelectionStyle(SelectionStyle)
		#self.parent.Displayshape_core.canva._display.Context.SetHighlightStyle(aspectMarker)

		#myGroup = Graphic3d_Group(self.parent.Displayshape_core.canva._display.GetView())
		#myMarker = Graphic3d_MarkerImage(Aspect_TOM_O, Quantity_Color(c), 8, 1)
		#myGroup.Marker(myMarker)





