# ###################################################
# Copyright (C) 2012 The Unknown Horizons Team
# team@unknown-horizons.org
# This file is part of Unknown Horizons.
#
# Unknown Horizons is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

import random

import horizons.main
from horizons.gui.window import Window
from horizons.gui.quotes import GAMEPLAY_TIPS, FUN_QUOTES


class MainMenu(Window):
	widget_name = 'mainmenu'

	def show(self):
		event_map={
			'startSingle'      : lambda: self.windows.show(self._gui._singleplayer), # first is the icon in menu
			'start'            : lambda: self.windows.show(self._gui._singleplayer), # second is the label in menu
			'startMulti'       : lambda: self.windows.show(self._gui._multiplayer),
			'start_multi'      : lambda: self.windows.show(self._gui._multiplayer),
			'settingsLink'     : lambda: self.windows.show(self._gui._settings),
			'settings'         : lambda: self.windows.show(self._gui._settings),
			'helpLink'         : self._gui.on_help,
			'help'             : self._gui.on_help,
			'closeButton'      : self.show_quit,
			'quit'             : self.show_quit,
			'dead_link'        : lambda: self.windows.show(self._gui._call_for_support), # call for help; SoC information
			'chimebell'        : lambda: self.windows.show(self._gui._call_for_support),
			'creditsLink'      : lambda: self.windows.show(self._gui._credits),
			'credits'          : lambda: self.windows.show(self._gui._credits),
			'loadgameButton'   : horizons.main.load_game,
			'loadgame'         : horizons.main.load_game,
			'changeBackground' : self._gui.get_random_background_by_button
		}

		self.widget = self._widget_loader[self.widget_name]
		self.widget.mapEvents(event_map)
		self._capture_escape(self.widget)
		self.widget.show()
		self._focus(self.widget)

	def hide(self):
		self.widget.hide()

	def on_escape(self):
		self.show_quit()

	def show_quit(self):
		"""Shows the quit dialog. Closes the game unless the dialog is cancelled."""
		message = _("Are you sure you want to quit Unknown Horizons?")
		if self.windows.show_popup(_("Quit Game"), message, show_cancel_button=True):
			horizons.main.quit()


class LoadingScreen(Window):
	widget_name = 'loadingscreen'

	def show(self):
		self.widget = self._widget_loader[self.widget_name]

		# Add 'Quote of the Load' to loading screen:
		qotl_type_label = self.widget.findChild(name='qotl_type_label')
		qotl_label = self.widget.findChild(name='qotl_label')
		quote_type = int(horizons.globals.fife.get_uh_setting("QuotesType"))
		if quote_type == 2:
			quote_type = random.randint(0, 1) # choose a random type

		if quote_type == 0:
			name = GAMEPLAY_TIPS["name"]
			items = GAMEPLAY_TIPS["items"]
		elif quote_type == 1:
			name = FUN_QUOTES["name"]
			items = FUN_QUOTES["items"]

		qotl_type_label.text = unicode(name)
		qotl_label.text = unicode(random.choice(items)) # choose a random quote / gameplay tip

		self.widget.show()

	def hide(self):
		self.widget.hide()
