from burp import IBurpExtender
from burp import IContextMenuFactory

from javax.swing import JMenuItem
from java.util import List, ArrayList
from java.util import URL

import socket
import urllib
import json
import re
import base64

bing_api_key=""

class BurpExtender(IBurpExtender,IContextMenuFactory):
	def registerExtenderCallbacks(self, callbacks):
		self._callbacks=callbacks
		self._helpers=callbacks.getHelpers()
		self.context=None

		#我们建立起扩展工具
		callbacks.setExtensionName("BHP Bing")
		callbacks.registerContextMenuFactory(self)

		return 

	def createMenuItems(self, context_menu):
		self.context=context_menu
		menu_list=ArrayList()
		menu_list.add(JMenuItem("Send to Bing",actionPerformed=self.bing_menu))
		return menu_list

	def bing_menu(self, event):

		#获取用户点击的详细信息
		http_traffic=self.context.getSelectedMessages()

		print("%d requests highlighted" % len(http_traffic))

		for traffic in http_traffic:
			http_service=traffic.getHttpService()
			host=http_service.getHost()

			print("User selected host: %s" % host)

			self.bing_search(host)

		return 

	def bing_search(self, host):

		#检查参数是否为IP地址或主机名
		is_ip=re.match("[0-9]+(?:\.[0-9]+){3}",host)

		if is_ip:
			ip_address=host
			domain=False
		else:
			ip_address=socket.gethostbyname(host)
			domain=True

		bing_query_string="'ip:%s'" % ip_address
		self.bing_query(bing_query_string)

		if domain:
			bing_query_string="'domain:%s'" % host
			self.bing_query(bing_query_string)


	def bing_query(self, bing_query_string):

		print("Performing Bing search: %s" % bing_query_string)

		#编码我们的查询
		quoted_query=urllib.quote(bing_query_string)

		http_request="GET https://api.datamarket.azure.com/Bing/Search/Web?$format=json&$top=20&$Query=%s HTTP/1.1\r\n" % quoted_query
		http_request+="Host: api.datamarket.azure.com\r\n"
		http_request+="Connection: close\r\n"
		http_request+="Authorization: Basic %s\r\n" % base64.b64encode(":%s" % bing_api_key)
		http_request+="User-Agent: Blackhat Python\r\n\r\n"

		json_body=self._callbacks.makeHttpRequest("api.datamarket.azure.com",443,True,http_request).tostring()

		json_body=json_body.split("\r\n\r\n",1)[1]
		
		try:
			r=json.loads(json_body)

			if len(r["d"]["results"]):
				for site in r["d"]["results"]:

					print("*" * 100)
					print(site["Title"])
					print(site["Url"])
					print(site['Description'])
					print("*" * 100)

					j_url=URL(site["Url"])

			if not self._callbacks.isInScope(j_url):
				print("Adding to Burp scope")
				self._callbacks.includeinScope(j_url)

		except:
			print("No results from Bing")
			pass
		
		return 