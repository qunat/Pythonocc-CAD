#!/usr/bin/env python

##Copyright 2009-2019 Thomas Paviot (tpaviot@gmail.com)
##
##This file is part of pythonOCC.
##
##pythonOCC is free software: you can redistribute it and/or modify
##it under the terms of the GNU Lesser General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##pythonOCC is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Lesser General Public License for more details.
##
##You should have received a copy of the GNU Lesser General Public License
##along with pythonOCC.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import logging
import os
import sys,math
from PyQt5.QtCore import pyqtSignal, QObject
from Win64.module import  OCCViewer
from OCC.Display.backend import get_qt_modules
from OCC.Display.backend import load_backend
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QMessageBox

backend_str = None
used_backend = load_backend(backend_str)

QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

# check if signal available, not available
# on PySide
HAVE_PYQT_SIGNAL = hasattr(QtCore, 'pyqtSignal')

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)


class qtBaseViewer(QtOpenGL.QGLWidget):
	''' The base Qt Widget for an OCC viewer
	'''
	def __init__(self, parent=None):
		super(qtBaseViewer, self).__init__(parent)
		self._display = None
		self._inited = False

		# enable Mouse Tracking
		self.setMouseTracking(True)

		# Strong focus
		self.setFocusPolicy(QtCore.Qt.WheelFocus)

		# required for overpainting the widget
		self.setAttribute(QtCore.Qt.WA_PaintOnScreen)
		self.setAttribute(QtCore.Qt.WA_NoSystemBackground)

		self.setAutoFillBackground(False)

	def GetHandle(self):
		''' returns an the identifier of the GUI widget.
		It must be an integer
		'''
		win_id = self.winId()  # this returns either an int or voitptr
		if "%s" % type(win_id) == "<type 'PyCObject'>":  # PySide
			### with PySide, self.winId() does not return an integer
			if sys.platform == "win32":
				## Be careful, this hack is py27 specific
				## does not work with python31 or higher
				## since the PyCObject api was changed
				import ctypes
				ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
				ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
				win_id = ctypes.pythonapi.PyCObject_AsVoidPtr(win_id)
		elif not isinstance(win_id, int):  # PyQt4 or 5
			## below integer cast may be required because self.winId() can
			## returns a sip.voitptr according to the PyQt version used
			## as well as the python version
			win_id = int(win_id)
		return win_id

	def resizeEvent(self, event):
		if self._inited:
			super(qtBaseViewer, self).resizeEvent(event)
			self._display.OnResize()

class mouse_move_Signal_Foo(QObject):
	# Define a new signal called 'trigger' that has no arguments.
	trigger = pyqtSignal()
	def connect_and_emit_trigger(self):
		# Connect the trigger signal to a slot.

		self.trigger.connect(self.handle_trigger)
		# Emit the signal.
		self.trigger.emit()

	def handle_trigger(self):
		# Show that the slot has been called.
		#print("very nice")

		pass
	
class wheelEvent_Foo(QObject):
	# Define a new signal called 'trigger' that has no arguments.
	trigger = pyqtSignal()
	def connect_and_emit_trigger(self):
		# Connect the trigger signal to a slot.
		self.trigger.connect(self.handle_trigger)
		# Emit the signal.
		self.trigger.emit()

	def handle_trigger(self):
		# Show that the slot has been called.
		#print("very nice")

		pass
class keyPressEvent_Foo(QObject):
	# Define a new signal called 'trigger' that has no arguments.
	trigger = pyqtSignal()
	def connect_and_emit_trigger(self):
		# Connect the trigger signal to a slot.
		self.trigger.connect(self.handle_trigger)
		# Emit the signal.
		self.trigger.emit()

	def handle_trigger(self):
		# Show that the slot has been called.
		#print("very nice")
		pass
class mousePressEvent_Foo(QObject):
	# Define a new signal called 'trigger' that has no arguments.
	trigger = pyqtSignal()
	def connect_and_emit_trigger(self):
		# Connect the trigger signal to a slot.
		# Emit the signal.
		self.trigger.emit()

	def handle_trigger(self):
		# Show that the slot has been called.
		#print("very nice")
		pass
	
class mouseReleaseEvent_Foo(QObject):
	# Define a new signal called 'trigger' that has no arguments.
	trigger = pyqtSignal()
	def connect_and_emit_trigger(self):
		# Connect the trigger signal to a slot.
		# Emit the signal.
		self.trigger.emit()

	def handle_trigger(self):
		# Show that the slot has been called.
		#print("very nice")
		pass
class mouseDoubleClickEvent_Foo(QObject):
	# Define a new signal called 'trigger' that has no arguments.
	trigger = pyqtSignal()
	def connect_and_emit_trigger(self):
		# Connect the trigger signal to a slot.
		# Emit the signal.
		self.trigger.emit()

	def handle_trigger(self):
		# Show that the slot has been called.
		#print("very nice")
		pass
	
class qtViewer3d(qtBaseViewer):

	# emit signal when selection is changed
	# is a list of TopoDS_*
	mouse_move_Signal=pyqtSignal()
	if HAVE_PYQT_SIGNAL:
		sig_topods_selected = QtCore.pyqtSignal(list)

	def __init__(self, *kargs):
		qtBaseViewer.__init__(self, *kargs)
		self.setObjectName("qt_viewer_3d")
		self.parent=kargs[0]
		self._drawbox = False
		self._zoom_area = False
		self._select_area = False
		self._inited = False
		self._leftisdown = False
		self._middleisdown = False
		self._rightisdown = False
		self._selection = None
		self._drawtext = True
		self._qApp = QtWidgets.QApplication.instance()
		self._key_map = {}
		self._current_cursor = "arrow"
		self._available_cursors = {}
		self.dragStartPosX=0
		self.dragStartPosY=0
		self.mousepresstype = None
		self.mousemovelock=False
		self.mousemoved=False
		self.mouse_move_Signal=mouse_move_Signal_Foo()
		self.wheelEvent_Signal=wheelEvent_Foo()
		self.keyPressEvent_Signal=keyPressEvent_Foo()
		self.mousePressEvent_Signal=mousePressEvent_Foo()
		self.mouseReleaseEvent_Signal=mouseReleaseEvent_Foo()
		self.mouseDoubleClickEvent_Signal=mouseDoubleClickEvent_Foo()
		self.scaling_ratio=1
	'''
	def contextMenuEvent(self, event):
			index=self.parent.ModuleWindowManager.tabwidget.currentIndex()
			name=self.parent.ModuleWindowManager.tabwidget.tabText(index)
	        # 创建右键菜单
			contextMenu = QMenu(self)

	        # 添加菜单项
			ActionHide = QAction("隐藏", self)
			ActionTransparent = QAction("透明", self)
			ActionDelete = QAction("删除", self)
			ActionAttributes = QAction("属性", self)

	        # 将菜单项添加到右键菜单中
			contextMenu.addAction(ActionHide)
			contextMenu.addSeparator()  # 添加分隔符
			contextMenu.addAction(ActionTransparent)
			contextMenu.addSeparator()  # 添加分隔符
			contextMenu.addAction(ActionDelete)
			contextMenu.addSeparator()  # 添加分隔符
			contextMenu.addAction(ActionAttributes)

	        # 连接菜单项的事件
			ActionHide.triggered.connect(self.newFile)
			ActionTransparent.triggered.connect(self.openFile)
			print(self.parent.Displayshape_core_dict[name])
			ActionDelete.triggered.connect(self.parent.Displayshape_core_dict[name].HidePart())

	        # 显示右键菜单
			contextMenu.exec_(self.mapToGlobal(event.pos()))
	'''
	
	
	@property
	def qApp(self):
		# reference to QApplication instance
		return self._qApp

	@qApp.setter
	def qApp(self, value):
		self._qApp = value

	def InitDriver(self):
		self._display = OCCViewer.Viewer3d(window_handle=self.GetHandle(), parent=self)
		self._display.Create()
		# background gradient
		self._display.SetModeShaded()
		self._inited = True
		# dict mapping keys to functions
		self._key_map = {ord('W'): self._display.SetModeWireFrame,
						 ord('S'): self._display.SetModeShaded,
						 ord('A'): self._display.EnableAntiAliasing,
						 ord('B'): self._display.DisableAntiAliasing,
						 ord('H'): self._display.SetModeHLR,
						 ord('F'): self._display.FitAll,
						 ord('G'): self._display.SetSelectionMode}
		self.createCursors()

	def createCursors(self):
		module_pth = os.path.abspath(".\\Win64\\python3.7\\Lib\\site-packages\\OCC\\Display")
		icon_pth = os.path.join(module_pth, "icons")

		_CURSOR_PIX_ROT = QtGui.QPixmap(os.path.join(icon_pth, "cursor-rotate.png"))
		_CURSOR_PIX_PAN = QtGui.QPixmap(os.path.join(icon_pth, "cursor-pan.png"))
		_CURSOR_PIX_ZOOM = QtGui.QPixmap(os.path.join(icon_pth, "cursor-magnify.png"))
		_CURSOR_PIX_ZOOM_AREA = QtGui.QPixmap(os.path.join(icon_pth, "cursor-magnify-area.png"))

		self._available_cursors = {
			"arrow": QtGui.QCursor(QtCore.Qt.ArrowCursor),  # default
			"pan": QtGui.QCursor(_CURSOR_PIX_PAN),
			"rotate": QtGui.QCursor(_CURSOR_PIX_ROT),
			"zoom": QtGui.QCursor(_CURSOR_PIX_ZOOM),
			"zoom-area": QtGui.QCursor(_CURSOR_PIX_ZOOM_AREA),
		}

		self._current_cursor = "arrow"

	def keyPressEvent(self, event):
		code = event.key()
		if code == QtCore.Qt.Key_Escape:
			self.parent.InteractiveOperate.InteractiveClose= "finish"
		if code == QtCore.Qt.Key_Enter or code == 16777220:
			self.keyPressEvent_Signal.connect_and_emit_trigger()
			

		if code in self._key_map:
			self._key_map[code]()
		elif code in range(256):
			log.info('key: "%s"(code %i) not mapped to any function' % (chr(code), code))
		else:
			log.info('key: code %i not mapped to any function' % code)

	def focusInEvent(self, event):
		if self._inited:
			self._display.Repaint()

	def focusOutEvent(self, event):
		if self._inited:
			self._display.Repaint()

	def paintEvent(self, event):
		if self._drawbox:
			self._display.Repaint()
			self._display.Repaint()
			painter = QtGui.QPainter(self)
			painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 2))
			rect = QtCore.QRect(*self._drawbox)
			painter.drawRect(rect)

	def wheelEvent(self, event):
		pt = event.pos()
		try:  # PyQt4/PySide
			delta = event.delta()
		except:  # PyQt5
			delta = event.angleDelta().y()
		if delta < 0:
			zoom_factor = 1.05
		else:
			zoom_factor = 0.95

		#dx =int(592/2) - pt.x()
		#dy = int(474/2) - pt.y()
		#self._display.Pan(dx, -dy,zoom_factor,False)
		#self._drawbox = False
		#self._display.SetCenter(int(pt.x()), int(pt.y()))
		#self._display.ResetView()

		pt = event.pos()
		center_x=math.ceil(pt.x()*zoom_factor)
		center_y=math.ceil(pt.y()*zoom_factor)
		self._display.ZoomFactor(zoom_factor)

		"""
		local zoom

		dx = pt.x() - self.dragStartPosX
			dy = pt.y() - self.dragStartPosY
			self.dragStartPosX = pt.x()
			self.dragStartPosY = pt.y()
			self.cursor = "pan"
			self._display.Pan(dx, -dy)
			self._drawbox = False
			self.mousemovelock=True

		"""
		self.scaling_ratio*=zoom_factor
		self.wheelEvent_Signal.connect_and_emit_trigger()

	@property
	def cursor(self):
		return self._current_cursor

	@cursor.setter
	def cursor(self, value):
		if not self._current_cursor == value:

			self._current_cursor = value
			cursor = self._available_cursors.get(value)

			if cursor:
				self.qApp.setOverrideCursor(cursor)
			else:
				self.qApp.restoreOverrideCursor()

	def mousePressEvent(self, event):

		self.mousePressEvent_Signal.connect_and_emit_trigger()
		self.setFocus()
		ev = event.pos()
		self.mousepresstype = event.button()
		self.dragStartPosX = ev.x()
		self.dragStartPosY = ev.y()
		self._display.StartRotation(self.dragStartPosX, self.dragStartPosY)
		self.buttons_list=[]
		if event.button() == QtCore.Qt.RightButton or event.button() == QtCore.Qt.MidButton:
			self.buttons_list.append(QtCore.Qt.RightButton)
		self.buttons_list.clear()
	
	def mouseDoubleClickEvent(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			self.mouseDoubleClickEvent_Signal.connect_and_emit_trigger()
		elif event.button() == QtCore.Qt.RightButton:
			pass

	def mouseReleaseEvent(self, event):
		pt = event.pos()
		modifiers = event.modifiers()
		self.mouseReleaseEvent_Signal.connect_and_emit_trigger()
		if event.button() == QtCore.Qt.LeftButton:
			if self._select_area:
				[Xmin, Ymin, dx, dy] = self._drawbox
				self._display.SelectArea(Xmin, Ymin, Xmin + dx, Ymin + dy)
				self._select_area = False
			else:
				# multiple select if shift is pressed
				if modifiers == QtCore.Qt.ShiftModifier:
					self._display.ShiftSelect(pt.x(), pt.y())
				else:
					# single select otherwise
					self._display.Select(pt.x(), pt.y())

					if (self._display.selected_shapes is not None) and HAVE_PYQT_SIGNAL:
						self.sig_topods_selected.emit(self._display.selected_shapes)


		elif event.button() == QtCore.Qt.RightButton:

			''' catia operate
			if self._zoom_area:
				[Xmin, Ymin, dx, dy] = self._drawbox
				self._display.ZoomArea(Xmin, Ymin, Xmin + dx, Ymin + dy)
				self._zoom_area = False
			'''
			pass

		self.cursor = "arrow"

	def DrawBox(self, event):
		tolerance = 2
		pt = event.pos()
		dx = pt.x() - self.dragStartPosX
		dy = pt.y() - self.dragStartPosY
		if abs(dx) <= tolerance and abs(dy) <= tolerance:
			return
		self._drawbox = [self.dragStartPosX, self.dragStartPosY, dx, dy]


	def mouseMoveEvent(self, evt):
		pt = evt.pos()
		buttons = int(evt.buttons())
		modifiers = evt.modifiers()
		self.mouse_move_Signal.connect_and_emit_trigger()
		self.mousemoved=False
		#MOVE  ADD MYSELF

		# ROTATE
		if evt.buttons() != QtCore.Qt.MidButton and evt.buttons()!=QtCore.Qt.RightButton:
			self.mousemovelock = False

		if (buttons == QtCore.Qt.MidButton and not modifiers == QtCore.Qt.ShiftModifier and
				self.parent.InteractiveOperate.InteractiveModule!="SKETCH" ) and self.mousemovelock==False:
			self.cursor = "rotate"
			self._display.Rotation(pt.x(), pt.y())
			self._drawbox = False
		

		# DYNAMIC ZOOM CATIA OPERATE

		elif (buttons == QtCore.Qt.RightButton and
			  not modifiers == QtCore.Qt.ShiftModifier ) and False:#暂时无用

			self.cursor = "zoom"
			self._display.Repaint()
			self._display.DynamicZoom(abs(self.dragStartPosX),
									  abs(self.dragStartPosY), abs(pt.x()),
									  abs(pt.y()))
			self.dragStartPosX = pt.x()
			self.dragStartPosY = pt.y()
			self._drawbox = False
		

		# PAN 1
		elif evt.buttons() == QtCore.Qt.MidButton | QtCore.Qt.RightButton and  self.parent.InteractiveOperate.InteractiveModule!="SKETCH":
			dx = pt.x() - self.dragStartPosX
			dy = pt.y() - self.dragStartPosY
			self.dragStartPosX = pt.x()
			self.dragStartPosY = pt.y()
			self.cursor = "pan"
			self._display.Pan(dx, -dy)
			self._drawbox = False
			self.mousemovelock=True
			self.mousemoved=True

		# PAN 2
		elif buttons == QtCore.Qt.MidButton and self.parent.InteractiveOperate.InteractiveModule=="SKETCH" :
			
			dx = pt.x() - self.dragStartPosX
			dy = pt.y() - self.dragStartPosY
			self.dragStartPosX = pt.x()
			self.dragStartPosY = pt.y()
			self.cursor = "pan"
			self._display.Pan(dx, -dy)
			self._drawbox = False
			self.mousemoved=True


		# DRAW BOX



		# ZOOM WINDOW
		elif (buttons == QtCore.Qt.RightButton and
			  modifiers == QtCore.Qt.ShiftModifier):
			self._zoom_area = True
			self.cursor = "zoom-area"
			self.DrawBox(evt)
			self.update()
			
		# SELECT AREA
		elif (buttons == QtCore.Qt.LeftButton and
			  modifiers == QtCore.Qt.ShiftModifier):
			self._select_area = True
			self.DrawBox(evt)
			self.update()
		else:
			
			self._drawbox = False
			self._display.MoveTo(pt.x(), pt.y())
			self.cursor = "arrow"
			

		self.dragStartPosX = evt.x()
		self.dragStartPosY = evt.y()
		
		#print(self.dragStartPosX,self.dragStartPosY)
		#self._display.SetCenter(int(pt.x()),int(pt.x()))
