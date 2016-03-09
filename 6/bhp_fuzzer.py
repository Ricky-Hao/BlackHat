from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator

from java.util import List, ArrayList

import random

class BurpExtender(IBurpExtender,IIntruderPayloadGeneratorFactory):
	def registerExtenderCallbacks(self, callbacks):
		self._callbacks=callbacks
		self._helpers=callbacks.getHelpers()

		callbacks.registerIntruderPayloadGeneratorFactory(self)

		return 

	def getGeneratorName(self):
		return "BHP Payload Generator"

	def createNewInstance(self, attack):
		return BHPFuzzer(self,attack)


class BHPFuzzer(IIntruderPayloadGenerator):
	def __init__(self, extender, attack):
		self._extender=extender
		self._helpers=extender._helpers
		self._attack=attack
		self.max_payloads=10
		self.num_iterations=0

		return 

	def hasMorePayloads(self):
		if self.num_iterations==self.max_payloads:
			return False
		else:
			return True

	def getNextPayload(self, current_payload):

		#转换成字符串
		payload="".join(chr(x) for x in current_payload)

		#调用简单的变形器对POST请求进行模糊测试
		payload=self.mutate_payload(payload)

		#增加FUZZ次数
		self.num_iterations+=1

		return payload

	def reset(self):
		self.num_iterations=0
		return 

	def mutate_payload(self, original_payload):
		#仅生成随机数或者调用一个外部脚本
		picker=random.randint(1,3)

		#在载荷中选取一个随机的偏移量去变形
		offset=random.randint(0,len(original_payload)-1)
		payload=original_payload[:offset]

		#在随机偏移位置插入SQL注入尝试
		if picker==1:
			payload+="'"

		#插入跨站尝试
		if picker==2:
			payload+="<script>alert('BHP!');</script>"

		#随机重复原始载荷
		if picker==3:

			chunk_length=random.randint(len(payload[offset:]),len(payload)-1)
			repeater=random.randint(1,10)

			for i in range(repeat):
				payload+=original_payload[offset;offset+chunk_length]

		#添加载荷中的剩余字节
		payload+=original_payload[offset:]

		return payload