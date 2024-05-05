__author__ = 'magnus'

stylesheet_instance = None


def get_stylesheet(name):
	global stylesheet_instance
	if not stylesheet_instance:
		stylesheet_instance = Stylesheets()
	return stylesheet_instance.get_stylesheet(name)


class Stylesheets(object):
	def __init__(self):
		self._stylesheets = {}
		self.make_stylesheet("main", "Win64/stylesheets/main.css")
		self.make_stylesheet("ribbon", "Win64/stylesheets/ribbon.css")
		self.make_stylesheet("ribbonPane", "Win64/stylesheets/ribbonPane.css")
		self.make_stylesheet("ribbonButton", "Win64/stylesheets/ribbonButton.css")
		self.make_stylesheet("ribbonSmallButton", "Win64/stylesheets/ribbonSmallButton.css")
		self.make_stylesheet("tittlebarButton", "Win64/stylesheets/tittlebarButton.css")
		self.make_stylesheet("tittlebarButtonWindown", "Win64/stylesheets/tittlebarButtonWindown.css")
		self.make_stylesheet("ViewLeaderButton", "Win64/stylesheets/ViewLeaderButton.css")
		self.make_stylesheet("ViewLeader", "Win64/stylesheets/ViewLeader.css")


	def make_stylesheet(self, name, path):
		with open(path,encoding="utf-8") as data_file:
			stylesheet = data_file.read()

		self._stylesheets[name] = stylesheet

	def get_stylesheet(self, name):
		stylesheet = ""
		try:
			stylesheet = self._stylesheets[name]
		except KeyError:
			print("stylesheet " + name + " not found")
		return stylesheet
