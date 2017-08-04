from controls import request_info, request_info_who
import json
class PostForm():
	info = request_info()
	print(info)
	leng_2 = len(info)
	def ListIt(self,post_n,type_n):
		while True:
			try:
				return request_info_who(post_n,type_n)
			except IndexError:
				break
				#instead of "break" we should have a funciton that just posts "there are no active requests"
	def GetLength(self):
		return self.leng_2
