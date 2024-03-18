# -*- coding: utf-8 -*-
from OCC.Display.backend import load_backend
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QApplication, QStyleFactory
from ui import MainGui
import sys
from  module import ShowGui

class Mywindown(QtWidgets.QMainWindow, ShowGui.Ui_MainWindow,MainGui.Ui_MainWindow):
	def __init__(self, parent=None):
		super(Mywindown, self).__init__(parent)
		# 3D显示设置
		self.TittleBar.windownre_pushButton.Add_Action(action_1=self.showMaximized,action_2=self.showNormal)
		self.TittleBar.winwownminimizing_pushButton.Add_Action(action_1=self.showMinimized)
		self.TittleBar.exit_pushButton.Add_Action(action_1=sys.exit)
		self.setWindowTitle("BrepCAD")

	def centerOnScreen(self):
		'''Centers the window on the screen.'''
		resolution = QtWidgets.QApplication.desktop().screenGeometry()
		x = (resolution.width() - self.frameSize().width()) / 2
		y = (resolution.height() - self.frameSize().height()) / 2
		self.move(x, y)
	
	def changeEvent(self, e):
		if e.type() == QtCore.QEvent.WindowStateChange:
			if self.isMinimized():
				#print("窗口最小化")
				pass
			elif self.isMaximized():
				#print("窗口最大化")
				pass
			elif self.isFullScreen():
				#print("全屏显示")
				pass
			elif self.isActiveWindow():
				#print("活动窗口")
				pass
		
	


if __name__ == '__main__':
	# checks if QApplication already exists
	QApplication.setStyle(QStyleFactory.create('Fusion'))
	app = QtWidgets.QApplication.instance()
	if not app:
		app = QtWidgets.QApplication(sys.argv)
	# 启动界面
	try:
		splash = QtWidgets.QSplashScreen(QtGui.QPixmap("./Pic/setup_pic.png"))  # 启动图片设置
		splash.show()
		splash.showMessage("软件启动中......")
	except:
		pass
	# --------------------
	win = Mywindown()
	win.show()
	win.Displayshape_core.canva.InitDriver()
	win.Displayshape_core.canva.qApp = app
	win.Displayshape_core.canva._display.display_triedron()
	#win.Displayshape_core.canva._display.set_bg_gradient_color(background_gradient_color1,
															   #background_gradient_color2)
	win.Displayshape_core.Displaydatum()
	win.Displayshape_core.SetBackgroundImage()
	win.Displayshape_core.DisplayCube()
	#win.InteractiveOperate.Setting()
	#win.Displayshape_core.canva._display.register_select_callback(win.InteractiveOperate.clicked_callback)
	# make the application float to the top
	splash.finish(win)
	win.raise_()
	#win.showMaximized()
	app.exec_()
