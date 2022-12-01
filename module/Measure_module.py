#codeing=utf-8
from OCC.Core.AIS import AIS_LengthDimension
from OCC.Core.BRep import BRep_Tool
from OCC.Core.Geom import Geom_Circle
from OCC.Core.TopoDS import TopoDS_Vertex, TopoDS_Edge
from OCC.Core.gp import gp_Pnt
from PyQt5.QtWidgets import QMessageBox


class Measure_function(object):
    def __init__(self):
        pass
    def measure_line_distance(self,shp,*kwargs):
        for shape in shp:  # this should be a TopoDS_Edge
            # print(type(shape))
            if shape.IsNull():
                continue
            elif isinstance(shape, TopoDS_Vertex):
                point = BRep_Tool.Pnt(shape)
                self.measure_shape_list.append(point)
            elif isinstance(shape, TopoDS_Edge):
                select = BRep_Tool.Curve(shape)[0]
                if not Geom_Circle.DownCast(select):
                    pass
                else:
                    possible_circle = Geom_Circle.DownCast(select)
                    # 从Geom_Curve向下类型转换为Geom_Circle
                    circle_ = possible_circle.Circ()
                    # 得到gp_Circ类型的圆
                    loc = circle_.Location()  # 圆心， gp_Pnt 类型
                    self.measure_shape_list.append(loc)

            else:
                self.measure_shape_list.append(shape)

            if len(self.measure_shape_list) == 2:
                try:
                    if isinstance(self.measure_shape_list[0], gp_Pnt):
                        distance = self.measure_shape_list[0].Distance(self.measure_shape_list[1])
                        measure_result = (distance)

                    else:
                        am = AIS_LengthDimension(self.measure_shape_list[0], self.measure_shape_list[1])
                        # self.canva._display.Context.Display(am,True)
                        measure_result = am.GetValue()

                    measure_result = "测量结果:" + "{:2.2f}".format(measure_result) + "mm"
                    reply = QMessageBox.information(self,  # 使用infomation信息框
                                                    "测量结果",
                                                    str(measure_result),
                                                    QMessageBox.Yes)
                except:
                    self.statusbar.showMessage("必须选择同样的元素")
                finally:
                    self.measure_shape_list.clear()

            elif len(self.measure_shape_list) > 2:
                pass
                self.measure_shape_list.clear()

    def measure_diameter(self,shp,*kwargs):
        for shape in shp:  # this should be a TopoDS_Edge
            if shape.IsNull():
                continue
            else:
                self.measure_shape_list.append(shape)

            if len(self.measure_shape_list) == 1:
                try:
                    if isinstance(self.measure_shape_list, TopoDS_Edge):
                        select = BRep_Tool.Curve(self.measure_shape_list[0])[0]
                        if not Geom_Circle.DownCast(select):
                            pass
                        else:
                            possible_circle = Geom_Circle.DownCast(select)
                            # 从Geom_Curve向下类型转换为Geom_Circle
                            circle_ = possible_circle.Circ()
                            # 得到gp_Circ类型的圆
                            loc = circle_.Location()  # 圆心， gp_Pnt 类型
                            radius = circle_.Radius()  # 半径
                            measure_result = radius * 2
                        # am = AIS_RadiusDimension(self.measure_shape_list[0], self.measure_shape_list[1])
                    elif isinstance(self.measure_shape_list[0], TopoDS_Face):
                        for e in TopologyExplorer(self.measure_shape_list[0]).edges():
                            select = BRep_Tool.Curve(e)[0]
                            if not Geom_Circle.DownCast(select):
                                pass
                            else:
                                possible_circle = Geom_Circle.DownCast(select)  # 从Geom_Curve向下类型转换为Geom_Circle
                                circle_ = possible_circle.Circ()  # 得到gp_Circ类型的圆
                                loc = circle_.Location()  # 圆心， gp_Pnt 类型
                                radius = circle_.Radius()  # 半径
                                # print(loc.X(), loc.Y(), loc.Z(), radius)
                                # ls_point = [loc.X(), loc.Y(), loc.Z(), radius]
                                measure_result = radius * 2

                                break

                    measure_result = "测量结果:直径" + "{:2.2f}".format(measure_result) + "mm"
                    reply = QMessageBox.information(self,  # 使用infomation信息框
                                                    "测量结果",
                                                    str(measure_result),
                                                    QMessageBox.Yes)
                except:
                    self.statusbar.showMessage("必须选择同样的元素")
                finally:
                    self.measure_shape_list.clear()

            elif len(self.measure_shape_list) > 1:
                pass
                self.measure_shape_list.clear()

