from controls import request_info, request_info_who
import json
class PostForm():
	info = request_info()
	print(info)
	leng_2 = len(info)
	leng = len(info[1])
	def ListIt(self,post_n,type_n):
		return request_info_who(post_n,type_n)
