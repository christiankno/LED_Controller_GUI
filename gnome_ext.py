import gi

from gi.repository import Gobject, Ide

class MyAppAddin(Gobject.Object, Ide.ApplicationAddin):
	def do_load(self, application):
		print('hello')
	def do_unload(self, application):
		print('goodbye')
		
