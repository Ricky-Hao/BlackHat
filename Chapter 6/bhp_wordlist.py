#coding=utf-8
from burp import IBurpExtender
from burp import IContextMenuFactory

from javax.swing import JMenuItem
from java.util import List, ArrayList
from java.net import URL

import re
from datetime import datetime
from HTMLParser import HTMLParser

class TagStripper(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.page_text=[]

	def handle_data(self, data):
		self.page_text.append(data)

	def handle_comment(self, data):
		self.handle_data(data)

	def strip(self, html):
		self.feed(html)
		return "".join(self.page_text)

class BurpExtender(IBurpExtender, IContextMenuFactory): 
	def registerExtenderCallbacks(self, callbacks):
		self._callbacks=callbacks
		self._helpers=callbacks.getHelpers()
		self.context=None
		self.hosts=set()

		#按部就班
		self.wordlist=set(["password"])

		#建立起我们的扩展工具
		callbacks.setExtensionMenu("BHP Wordlist")
		callbacks.registerContextMenuFactory(self)

		return 

	def createMenuItems(self, context_menu):
		self.context=context_menu
		menu_list=ArrayList()
		menu_list.add(JMenuItem("Create Woedlist",actionPerformed=self.wordlist_menu))

		return menu_list

	def wordlist_menu(self, event):

		#抓取用户点击的细节
		http_traffic=self.context.getSelectedMessages()

		for traffic in http_traffic:
			http_service=traffic.getHttpService()
			host=http_service.getHost()

			self.hosts.add(host)

			http_response=traffic.getResponse()

			if http_response:
				self.get_words(http_response)

		self.display_wordlist()

		return 

	def get_words(self, http_response):
		headers, body=http_response.tostring().split('\r\n\r\n',1)

		#忽略下一个响应
