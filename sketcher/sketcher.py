# -*- coding: utf-8 -*-
import threading

from OCC.Core import BRepExtrema
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge

from GUI.SelectWidget import SelectWidget
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Lin, gp_Ax2, gp_Dir, gp_Pln
from OCC.Core.gp import (gp_Pnt2d, gp_Ax2d, gp_Dir2d, gp_Circ2d, gp_Origin2d, gp_DX2d,
                         gp_Ax2, gp_OX2d, gp_Lin2d, gp_Trsf, gp_XOY,
                         gp_Pnt, gp_Vec, gp_Ax3, gp_Pln, gp_Origin, gp_DX, gp_DY,
                         gp_DZ, gp_OZ)
from sketcher.sketcher_circel import sketch_circel
from sketcher.sketcher_line import sketch_line
from sketcher.sketcher_rectangle import sketch_rectangle
from sketcher.sketcher_profile import sketch_profile
from sketcher.sketcher_trim import sketch_trim
from sketcher.sketcher_dimension import Dimension_Manege
from OCC.Core.GeomAPI import geomapi_To3d
from sketcher.sketcher_line import Brep_line
from sketcher.sketcher_circel import Brep_circel

class SketchModule(object):
	def __init__(self,parent=None):
		self.parent=parent
		self.sketch_type=None
		self.select_shape_list = []
		self.gp_Dir=None
		self.show_element={}
		self.new_do_draw_dict={"line":None,"circel":None,"rectangle":None,"arc":None,"profile":None}
		self.parent.Displayshape_core.canva.mouse_move_Signal.trigger.connect(self.show_coordinate)
		self.Dimension_Manege = Dimension_Manege(self)
		
	



	def get_all_sketcher_element(self):
		sketch_element_dict={}
		for element in self.new_do_draw_dict.keys():
			try:
				if self.parent.Sketcher.new_do_draw_dict[element].show_line_dict != [] and (element=="line" or element=="rectangle" or element=="profile"):
					lines = self.parent.Sketcher.new_do_draw_dict[element].show_line_dict.keys()
					for key in lines:
						lable = element + str(key)
						sketch_element_dict[lable] = self.parent.Sketcher.new_do_draw_dict[element].show_line_dict[key]
				elif self.parent.Sketcher.new_do_draw_dict[element].show_circel_dict != [] and (element=="circel"):
					circel = self.parent.Sketcher.new_do_draw_dict[element].show_circel_dict.keys()
					for key in circel:
						lable = element + str(key)
						sketch_element_dict[lable] = self.parent.Sketcher.new_do_draw_dict[element].show_circel_dict[key]


			except:
				pass
		self.show_element=sketch_element_dict
		return sketch_element_dict

	def show_coordinate(self):
		(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()
		coordinate="X:{:.2f}   Y:{:.2f}".format(x,y)
		self.parent.Displayshape_core.canva._display.View.SetProj(vx, vy, vz)
		self.parent.statusbar.showMessage(coordinate)
		
	def select_sketch_plane(self):
		self.select_windows=SelectWidget(parent=self.parent)
		self.select_windows.Show()
		#self.parent.Displayshape_core.canva._display.SetSelectionModeEdge()
		#self.parent.change_ribbon(init_name="Ribbon_sketcher")
		
		
	def quite_sketch(self):
		self.parent.change_ribbon(init_name="Ribbon_main")
		self.parent._ribbon._ribbon_widget.setCurrentIndex(1)
		self.parent.Displayshape_core.canva._display.View_Iso()
		self.parent.Displayshape_core.canva._display.FitAll()
		self.parent.InteractiveOperate.InteractiveModule="Home"
		
	def _2Dto3d(self):
		plane = gp_Pln(gp_Origin(), self.gp_Dir)
		line = BRepBuilderAPI_MakeEdge(geomapi_To3d(self.new_do_draw_dict["line"].show_line_dict[0], plane)).Edge()
		
	def uptoplane(self):
		self.parent.InteractiveOperate.InteractiveModule="SKETCH"
		self.parent.Displayshape_core.canva._display.register_select_callback(self.clicked_callback)
		self.parent.Displayshape_core.Hide_datum()

		if self.select_windows.comboBox.currentText()=="XY平面":
			self.parent.Displayshape_core.canva._display.View_Top()
			self.parent.Displayshape_core.canva._display.FitAll()
			self.gp_Dir=gp_Dir(0,0,1)

		if self.select_windows.comboBox.currentText()=="YZ平面":
			self.parent.Displayshape_core.canva._display.View_Right()
			self.parent.Displayshape_core.canva._display.FitAll()
			self.gp_Dir=gp_Dir(1,0,0)
		if self.select_windows.comboBox.currentText()=="XZ平面":
			self.parent.Displayshape_core.canva._display.View_Front()
			self.parent.Displayshape_core.canva._display.FitAll()
			self.gp_Dir=gp_Dir(0,1,0)
	
	def clicked_callback(self, shp, *kwargs):
		try:
			if self.sketch_type==4:
				self.new_do_draw_dict["line"].draw_line(shp)# draw line
			elif self.sketch_type==3:
				self.new_do_draw_dict["circel"].draw_circel(shp)
			elif self.sketch_type==2:
				self.new_do_draw_dict["rectangle"].draw_rectangle(shp)
			elif self.sketch_type==1:
				self.new_do_draw_dict["profile"].draw_line(shp)
			elif self.sketch_type==8:
				if shp!=[]:
					self.new_do_trim.trim(shp)
				pass
			elif self.sketch_type==10:
				self.do_diamension(shp=shp)
				print(shp)
		except Exception as e:
			print(e)
	def do_draw(self):
		
		if self.sketch_type==4 and self.new_do_draw_dict["line"]==None:
			self.new_do_draw_dict["line"]=sketch_line(self.parent,self.gp_Dir)# draw line
		elif self.sketch_type==3 and self.new_do_draw_dict["circel"]==None:
			self.new_do_draw_dict["circel"] = sketch_circel(self.parent,self.gp_Dir)  # draw ciecel
		elif self.sketch_type==2 and self.new_do_draw_dict["rectangle"]==None:
			self.new_do_draw_dict["rectangle"] = sketch_rectangle(self.parent,self.gp_Dir)  # draw rectangle
		elif self.sketch_type==1 and self.new_do_draw_dict["rectangle"]==None:
			self.new_do_draw_dict["profile"] = sketch_profile(self.parent,self.gp_Dir)  # draw rectangle
			
	def do_diamension(self,shp):
		self.Dimension_Manege.Create_Dimension(shp)
		print("do_diamension")
	def do_trim(self):
		self.new_do_trim=sketch_trim(self.parent)

	def dynamics_drwa(self):
		if self.sketch_type==4:
			self.new_do_draw_dict["line"].dynamics_drwa_line()# draw line
		elif self.sketch_type==3:
			self.new_do_draw_dict["circel"].dynamics_drwa_circel()  # draw circel
		elif self.sketch_type==2:
			self.new_do_draw_dict["rectangel"].dynamics_drwa_rectangle()  # draw rectangle
		elif self.sketch_type==1:
			self.new_do_draw_dict["profile"].dynamics_drwa_line()  #draw profile

	def sketch_draw_profile(self):
		self.get_all_sketcher_element()
		self.sketch_type=1# profile draw
		self.do_draw()
	def sketch_draw_rectangle(self):
		self.get_all_sketcher_element()
		self.sketch_type=2# rectangle draw
		self.do_draw()
	def sketch_draw_circel(self):
		self.get_all_sketcher_element()
		self.sketch_type=3# circel draw
		self.do_draw()
	def sketch_draw_line(self):
		self.get_all_sketcher_element()
		self.sketch_type=4# line draw
		self.do_draw()
	def sketch_draw_arc(self):
		self.get_all_sketcher_element()
		self.sketch_type=5# arc draw
		self.do_draw()
	def sketch_draw_spline(self):
		self.get_all_sketcher_element()
		self.sketch_type=6# spline draw
		self.do_draw()
	def sketch_draw_point(self):
		self.get_all_sketcher_element()
		self.sketch_type=7# point draw
		self.do_draw()
	def sketch_trim(self):
		self.get_all_sketcher_element()
		self.sketch_type = 8  # sketch trim
		self.do_trim()
	def sketch_mirror(self):
		self.get_all_sketcher_element()
		self.sketch_type = 9
	def sketch_diamension(self):
		self.get_all_sketcher_element()
		print("sketch_diamension")
		self.sketch_type = 10
		#self.
	
	def dynamics_draw_trance(self):#公用的草绘动态捕捉
		print("dynamics_draw_trance")
		try:
			if isinstance(self.draw_trance_element, Brep_line):  # 直线捕捉
				self.parent.Displayshape_core.canva._display.Context.Remove(
					self.draw_trance_element.capture_point_list[0], False)  # 移除已经显示的端点
				self.parent.Displayshape_core.canva._display.Context.Remove(
					self.draw_trance_element.capture_point_list[1], False)  # 移除已经显示的中点
				self.parent.Displayshape_core.canva._display.Context.Remove(
					self.draw_trance_element.capture_point_list[2], False)  # 移除已经显示的端点
			else:  # 圆或圆弧捕捉
				self.parent.Displayshape_core.canva._display.Context.Remove(
					self.draw_trance_element.capture_center_point_list[0], False)
				self.parent.Displayshape_core.canva._display.Context.Remove(
					self.draw_trance_element.capture_any_point_list[0], False)  # 移除已经显示的任意点
		
		except Exception as e:
			print(e)
			
		shape_id = 0
		Distance = 0
		_dragStartPosY = self.parent.Displayshape_core.canva.dragStartPosY
		_dragStartPosX = self.parent.Displayshape_core.canva.dragStartPosX
		(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()
		direction = gp_Dir(vx, vy, vz)
		line = gp_Lin(gp_Pnt(x, y, z), direction)
		edge_builder = BRepBuilderAPI_MakeEdge(line)
		edge = edge_builder.Edge()
		try:
			for key in self.show_element.keys():
				try:
					'''
					if key == self.line_id and len(self.point_count) >= 1:
						continue
					if self.show_element == []:
						continue
					'''
					extrema = BRepExtrema.BRepExtrema_DistShapeShape(self.show_element[key].ais_shape.Shape(), edge)
					nearest_point1 = extrema.PointOnShape1(1)
					nearest_point2 = extrema.PointOnShape2(1)
					if Distance > nearest_point1.Distance(nearest_point2) or Distance == 0:
						Distance = nearest_point1.Distance(nearest_point2)
						x, y, z = (nearest_point1.X()), (nearest_point1.Y()), (nearest_point1.Z())
						if "line" in key:
							shape_id = int(key.replace("line", ""))
							element = self.parent.Sketcher.new_do_draw_dict["line"].show_line_dict
						elif "rectangle" in key:
							shape_id = int(key.replace("rectangle", ""))
							element = self.parent.Sketcher.new_do_draw_dict["rectangle"].show_line_dict
						elif "profile" in key:
							shape_id = int(key.replace("profile", ""))
							element = self.parent.Sketcher.new_do_draw_dict["profile"].show_line_dict
						elif "circel" in key:
							shape_id = int(key.replace("circel", ""))
							element = self.parent.Sketcher.new_do_draw_dict["circel"].show_circel_dict
						
						self.draw_trance_element = element[shape_id]
						print(shape_id, 666)
						
					elif Distance > 20:
						self.parent.Displayshape_core.canva._display.Context.Remove(
							element[shape_id].capture_point_list[0], False)  # 移除已经显示的端点
						self.parent.Displayshape_core.canva._display.Context.Remove(
							element[shape_id].capture_point_list[1], False)  # 移除已经显示的中点
						self.parent.Displayshape_core.canva._display.Context.Remove(
							element[shape_id].capture_point_list[2], False)  # 移除已经显示的端点
						self.parent.Displayshape_core.canva._display.Context.Remove(
							element[shape_id].capture_any_point_list[0], False)  # 重移除已经显示的任意点
					pass
				except Exception as e:
					print(e)
					pass
			if Distance >= 25:
				pass
			
			if isinstance(element[shape_id], Brep_line):  # 直线捕捉
				# 捕捉生产端点和中点,任意点
				if Distance > 15 or Distance == 0:
					self.capture_point_None = 0
					try:
						self.parent.Displayshape_core.canva._display.Context.Remove(
							element[shape_id].capture_point_list[0], False)  # 移除已经显示的端点
						self.parent.Displayshape_core.canva._display.Context.Remove(
							element[shape_id].capture_point_list[1], False)  # 移除已经显示的中点
						self.parent.Displayshape_core.canva._display.Context.Remove(
							element[shape_id].capture_point_list[2], False)  # 移除已经显示的端点
						self.parent.Displayshape_core.canva._display.Context.Remove(
							element[shape_id].capture_any_point_list[0], False)  # 移除已经显示的任意点
						self.parent.Displayshape_core.canva._display.Repaint()
						self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
					except Exception as e:
						
						pass
				else:
					try:
						self.parent.Displayshape_core.canva._display.Context.Remove(
							element[shape_id].capture_any_point_list[0], False)  # 移除已经显示的任意点
						pnt = gp_Pnt(x, y, z)
						pnt0 = element[shape_id].get_capture_point_pnt(0)
						pnt1 = element[shape_id].get_capture_point_pnt(1)
						pnt2 = element[shape_id].get_capture_point_pnt(2)
						
						if pnt.Distance(pnt0) >= 15 and pnt.Distance(pnt1) >= 15 and pnt.Distance(pnt2) >= 15:
							element[shape_id].set_capture_any_point(x, y, z)
							self.parent.Displayshape_core.canva._display.Context.Display(
								element[shape_id].capture_any_point_list[0], False)  # 移除已经显示的任意点
						
						self.parent.Displayshape_core.canva._display.Context.Display(
							element[shape_id].capture_point_list[0], False)  # 移除已经显示的端点
						self.parent.Displayshape_core.canva._display.Context.Display(
							element[shape_id].capture_point_list[1], False)  # 移除已经显示的中点
						self.parent.Displayshape_core.canva._display.Context.Display(
							element[shape_id].capture_point_list[2], False)  # 移除已经显示的端点
						self.parent.Displayshape_core.canva._display.Repaint()
						self.parent.Displayshape_core.canva._display.Context.UpdateCurrentViewer()
					except Exception as e:
						print(e)
			elif isinstance(element[shape_id], sketcher_circel.Brep_circel):  # 圆弧捕捉
				print("捕捉圆弧")
				if Distance > 15 or Distance == 0:
					# element[shape_id].remove_capture_point()
					# element[shape_id].remove_capture_any_point(self)
					self.parent.Displayshape_core.canva._display.Context.Remove(
						element[shape_id].capture_center_point_list[0], False)  # 移除已经显示的圆心
					self.parent.Displayshape_core.canva._display.Context.Remove(
						element[shape_id].capture_any_point_list[0], False)  # 移除已经显示的圆弧上的点
					pass
				
				
				else:
					P1 = [x, y, z]
					element[shape_id].create_capture_any_point(P1)
					self.parent.Displayshape_core.canva._display.Context.Display(
						element[shape_id].capture_center_point_list[0], False)  # 移除已经显示的圆心
					self.parent.Displayshape_core.canva._display.Context.Display(
						element[shape_id].capture_any_point_list[0], False)  # 移除已经显示的圆心
			# element[shape_id].display_capture_any_point()
			# element[shape_id].display_capture_point()
		except:
			pass
	
	
	def catch_capure_point(self,shape):#公用的端点捕捉
		if True:  # 捕捉生成的端点
			shape_id = 0
			Distance = 0
			(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()
			direction = gp_Dir(vx, vy, vz)
			line = gp_Lin(gp_Pnt(x, y, z), direction)
			edge_builder = BRepBuilderAPI_MakeEdge(line)
			edge = edge_builder.Edge()
			#return x, y, z, vx, vy, vz
			try:
				for key in self.show_element.keys():
					try:
						if key == self.line_id and len(self.point_count) >= 1:
							continue
						if self.show_element == []:
							continue
						extrema = BRepExtrema.BRepExtrema_DistShapeShape(self.show_element[key].ais_shape.Shape(), edge)
						nearest_point1 = extrema.PointOnShape1(1)
						nearest_point2 = extrema.PointOnShape2(1)
						if Distance > nearest_point1.Distance(nearest_point2) or Distance == 0:
							Distance = nearest_point1.Distance(nearest_point2)
							x1, y1, z1 = (nearest_point1.X()), (nearest_point1.Y()), (nearest_point1.Z())
							if "line" in key:
								shape_id = int(key.replace("line", ""))
								element = self.parent.Sketcher.new_do_draw_dict["line"].show_line_dict
							elif "rectangle" in key:
								shape_id = int(key.replace("rectangle", ""))
								element = self.parent.Sketcher.new_do_draw_dict["rectangle"].show_line_dict
							elif "profile" in key:
								shape_id = int(key.replace("profile", ""))
								element = self.parent.Sketcher.new_do_draw_dict["profile"].show_line_dict
							elif "circel" in key:
								shape_id = int(key.replace("circel", ""))
								element = self.parent.Sketcher.new_do_draw_dict["circel"].show_line_dict

						pass
					except Exception as e:
						print(e)
						pass


				# 捕捉生产端点和中点,任意点
				pnt = gp_Pnt(x, y, z)
				pnt0 = element[shape_id].get_capture_point_pnt(0)
				pnt1 = element[shape_id].get_capture_point_pnt(1)
				pnt2 = element[shape_id].get_capture_point_pnt(2)
				if Distance > 15 or Distance == 0:
					self.capture_point_None = 0
					(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.ProjReferenceAxe()

				else:
					if pnt.Distance(pnt0) <= 15:
						x, y, z = pnt0.X(), pnt0.Y(), pnt0.Z()
					elif pnt.Distance(pnt1) <= 15:
						x, y, z = pnt1.X(), pnt1.Y(), pnt1.Z()
					elif pnt.Distance(pnt2) <= 15:
						x, y, z = pnt2.X(), pnt2.Y(), pnt2.Z()
					else:
						x, y, z = x1, y1, z1
			except Exception as e:
				print(e)
				pass



		return x, y, z, vx, vy, vz