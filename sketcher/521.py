from OCC.Display.SimpleGui import init_display
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
from OCC.Core.TColgp import TColgp_Array1OfPnt, TColgp_Array1OfPnt2d
from OCC.Core.gp import gp_Pnt, gp_Pnt2d
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.GeomAbs import GeomAbs_C2
from OCC.Core.Geom import Geom_Line
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import Graphic3d_ArrayOfPrimitivesAspect, Graphic3d_TOPA_LEFT

display, start_display, add_menu, add_function_to_menu = init_display()

# 创建两个点
point1 = gp_Pnt(0, 0, 0)
point2 = gp_Pnt(10, 0, 0)

# 创建直线
line = BRepBuilderAPI_MakeEdge(point1, point2).Edge()

# 设置直线颜色和宽度
color = Quantity_Color(Quantity_TOC_RGB, 1, 0, 0)  # 红色
aspect = Graphic3d_ArrayOfPrimitivesAspect(color, 2.0, Graphic3d_TOPA_LEFT)

# 将直线添加到显示对象
display.DisplayShape(line, update=True)
display.Context.SetLineAspect(aspect)

# 显示
start_display()
