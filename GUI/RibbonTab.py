from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from GUI.RibbonPane import RibbonPane


class RibbonTab(QWidget):
	def __init__(self, parent, name):
		QWidget.__init__(self, parent)
		layout = QHBoxLayout()
		self.setLayout(layout)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)
		layout.setAlignment(Qt.AlignLeft)

	def add_ribbon_pane(self, name):
		ribbon_pane = RibbonPane(self, name)
		self.layout().addWidget(ribbon_pane)
		return ribbon_pane

	def add_spacer(self):
		self.layout().addSpacerItem(QSpacerItem(1, 1, QSizePolicy.MinimumExpanding))
		self.layout().setStretch(self.layout().count() - 1, 1)
		
	def set_ribbon_pane(self):
		pass