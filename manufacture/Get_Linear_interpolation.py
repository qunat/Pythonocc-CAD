# -*- coding: utf-8 -*-
from OCC.Core import BRepGProp, TopExp
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepGProp import brepgprop_LinearProperties
from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeCircle
from OCC.Core.GProp import GProp_GProps
from OCC.Core.Geom2dAPI import Geom2dAPI_Interpolate
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve
from OCC.Core.GCPnts import GCPnts_UniformAbscissa
from OCC.Core.TColgp import TColgp_HArray1OfPnt2d
from OCC.Core.TopExp import topexp
from OCC.Core.gp import gp_Pnt, gp_Pln, gp_Dir, gp_Ax2, gp_Circ

#from OCC.Display.SimpleGui import init_display
#display, start_display, add_menu, add_function_to_menu = init_display()
from OCC.Core.gp import gp_Pnt, gp_Pnt2d, gp_OX2d
from OCC.Core.Geom2d import Geom2d_Circle
from OCC.Core.Geom2dAdaptor import Geom2dAdaptor_Curve
from OCC.Core.GCPnts import GCPnts_UniformAbscissa




def Get_Linear_interpolation_point(Pnt1=[1,1,30],Pnt2=[1,100,1],step=0.1):
    pass
    aPnt1 = gp_Pnt(Pnt1[0],Pnt1[1],Pnt1[2])#起点
    aPnt2 = gp_Pnt(Pnt2[0],Pnt2[1],Pnt2[2])#终点
    aEdge1 = BRepBuilderAPI_MakeEdge(aPnt1, aPnt2).Edge()
    #aCurve = BRep_Tool.Curve(aEdge1)[0]  # 先把它转换为Geom_Curve
    system = GProp_GProps()
    brepgprop_LinearProperties(aEdge1, system)  # 获取线段属性
    n = float(system.Mass() / step)
    mVer1 = topexp.FirstVertex(aEdge1, True)  # 起点
    mVer2 = topexp.LastVertex(aEdge1, True)  # 终点
    P1 = BRep_Tool.Pnt(mVer1)
    P2 = BRep_Tool.Pnt(mVer2)
    #print(P1.X(), P1.Y(), P1.Z())
    mVec = (P2.XYZ() - P1.XYZ())
    #display.DisplayShape(aEdge1, update=True)
    Linear_interpolation_point_list=[]
    for i in range(int(n)):
        mPVec1 = mVec.Normalized() * step * i
        P3 = gp_Pnt(mPVec1.X() + P1.X(), mPVec1.Y() + P1.Y(), mPVec1.Z() + P1.Z())
        Linear_interpolation_point_list.append(P3)
        #display.DisplayShape(P3, update=True)
    return Linear_interpolation_point_list


def Get_face_direction(face):  # 获取平面的法向
    get_surface = BRepAdaptor_Surface(face)  # 获取surface参数的函数
    pln = get_surface.Plane()
    # print(pln.Axis().Direction().XYZ().Coord())
    original_direct = pln.Axis().Direction().XYZ().Coord()
    return original_direct
def Get_Arc_interpolation_point(Pnt1=[],Pnt2=[],Pnt3=[],Direction=None,step=0.1):#pnt1为起点坐标，pnt2为终点坐标，pnt3为i,j,k
    try:

        x0,y0,z0=Pnt1[:]
        x,y,z=Pnt2[:]
        i,j,k=Pnt3[:]
        #print("起点",Pnt1,"终点",Pnt2)
        circle_center=[]#圆心坐标初始化
        # 求圆心坐标
        circle_center=[x0+i,y0+j,z0+k]
        # 计算半径
        r = float(((circle_center[0]-x0)**2+(circle_center[1]-y0)**2)**0.5)
        #print("圆心", circle_center, i, j, k,r)
        Location = gp_Pnt(circle_center[0], circle_center[1], circle_center[2])  # 圆心坐标
        # 判断G02/G03
        if Pnt1[0] !=Pnt2[0] or Pnt1[1] !=Pnt2[1]:#不是整圆
            if Direction=="G02":
                Axis = gp_Dir(0, 0, -1)  # G02
            elif Direction=="G03":
                Axis = gp_Dir(0, 0, 1)  # G03

            CircleAxis = gp_Ax2(Location, Axis)
            Circle = gp_Circ(CircleAxis, r)
            ArcofCircle0 = GC_MakeArcOfCircle(Circle, gp_Pnt(x0, y0, z0), gp_Pnt(x, y, z), True)
            ArcofCircle1 = BRepBuilderAPI_MakeEdge(ArcofCircle0.Value())
            path = BRepBuilderAPI_MakeWire(ArcofCircle1.Edge()).Shape()
            aCurve = BRep_Tool.Curve(ArcofCircle1.Edge())[0]
            ufirst = BRep_Tool.Curve(ArcofCircle1.Edge())[1]
            ulast = BRep_Tool.Curve(ArcofCircle1.Edge())[2]
            gac = GeomAdaptor_Curve(aCurve, ufirst, ulast)
            ua = GCPnts_UniformAbscissa(gac, step)
        else:#整圆
            print("绘制整圆")
            Axis = gp_Dir(0, 0, -1)
            CircleAxis = gp_Ax2(Location, Axis)
            Circle = gp_Circ(CircleAxis, r)
            ArcofCircle0 = GC_MakeArcOfCircle(Circle, 0 / 180 * 3.14, 360 / 180 * 3.14, True)
            ArcofCircle1 = BRepBuilderAPI_MakeEdge(ArcofCircle0.Value())
            #path = BRepBuilderAPI_MakeWire(ArcofCircle1.Edge()).Shape()
            aCurve = BRep_Tool.Curve(ArcofCircle1.Edge())[0]
            gac = GeomAdaptor_Curve(aCurve)
            ua = GCPnts_UniformAbscissa(gac, step)
            print("整圆")
        # 求离散点
        a_sequence = []
        if ua.IsDone():
            n = ua.NbPoints()
            #print(n)
            for count in range(1, n + 1):
                p = gp_Pnt()
                aCurve.D0(ua.Parameter(count), p)
                a_sequence.append(p)
            return a_sequence#圆弧上离线的点列表
        else:
            print("wrong")
        return path
    except Exception as e:

        pass


'''
step=50
print("system.Mass(): ", system.Mass())
nb_ = system.Mass() / step    # step是步长，这句话的意思是等步长平分周长，nb_是平分的点的数目
print(nb_)
gac = GeomAdaptor_Curve(aCurve)
ua = GCPnts_UniformAbscissa(gac, nb_)
print(ua.IsDone())
if ua.IsDone():
    n = ua.NbPoints()
    pts = []
    for count in range(1, n + 1):  # 索引从1开始，到n结束
        p = gp_Pnt()
        aCurve.D0(ua.Parameter(count), p)  # 获取坐标
        pts.append(p)
        print(count)

'''
