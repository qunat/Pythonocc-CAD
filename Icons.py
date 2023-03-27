from PyQt5.QtGui import *
import os
__author__ = 'magnus'

icons_instance = None


def get_icon(name):
	global icons_instance
	if not icons_instance:
		icons_instance = Icons()
	return icons_instance.icon(name)


class Icons(object):
	def __init__(self):
		self._icons = {}
		self.set_all_icons_name()
		self.make_icon("default", "icons/folder.png")
		#self.make_icon("folder", "icons/folder.png")
		#self.make_icon("open", "icons/folder.png")
		#self.make_icon("save", "icons/save.png")
		#self.make_icon("icon", "icons/icon.png")
		#self.make_icon("exit", "icons/exit.png")
		#self.make_icon("paste", "icons/paste.png")
		#self.make_icon("zoom", "icons/zoom.png")
		#self.make_icon("copy", "icons/copy.png")
		#self.make_icon("about", "icons/about.png")
		#self.make_icon("license", "icons/license.png")
		#self.make_icon("sketch", "icons/direct_sketch.2l.png")
		
	def set_all_icons_name(self,path="./icons"):
		for filename in os.listdir(path):
			if filename.endswith(".png"):
				icon_name=filename.replace(".png","")
				icon_path="icons/"+filename
				self.make_icon(icon_name, icon_path)
				
			
	
	def make_icon(self, name, path):
		icon = QIcon()
		icon.addPixmap(QPixmap(path), QIcon.Normal, QIcon.Off)
		self._icons[name] = icon

	def icon(self, name):
		icon = self._icons["default"]
		try:
			icon = self._icons[name]
		except KeyError:
			print("icon " + name + " not found")
		return icon
