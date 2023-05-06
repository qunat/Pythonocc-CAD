from PyQt5.QtWidgets import *
from GUI.RibbonTab import RibbonTab
from GUI import gui_scale
from GUI.StyleSheets import get_stylesheet

__author__ = 'magnus'


class RibbonWidget(QToolBar):
	def __init__(self, parent):
		QToolBar.__init__(self, parent)
		self.setStyleSheet(get_stylesheet("ribbon"))
		self.setObjectName("ribbonWidget")
		self.setWindowTitle("Ribbon")
		self._ribbon_widget = QTabWidget(self)
		self._ribbon_widget.setMaximumHeight(120*gui_scale())
		self._ribbon_widget.setMinimumHeight(110*gui_scale())
		self.setMovable(False)
		self.addWidget(self._ribbon_widget)
		self.ribbon_tab_dict={}
		
	def add_ribbon_tab(self, name):
		self.ribbon_tab_dict[name] = RibbonTab(self, name)
		self.ribbon_tab_dict[name].setObjectName("tab_" + name)
		self._ribbon_widget.addTab(self.ribbon_tab_dict[name], name)
		return self.ribbon_tab_dict[name]
	

	def set_active(self, name):
		self.setCurrentWidget(self.findChild("tab_" + name))
		
	def add_ribbon_button(self,name):
		pass
		