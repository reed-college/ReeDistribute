from wtforms import Form, BooleanField, StringField, PasswordField, validators
from controls import request_info, request_info_who
import json
class PostForm():
	info = request_info()
	print(info)
	leng_2 = len(info)
	leng = len(info[1])
	def ListIt(self,post_n,type_n):
		return request_info_who(post_n,type_n)
			# amount_needed = i[1]
			# amount_given = i[2]
			# title = i[3]
			# desc = i[4]
			# req_id = i[5]



	# i = json.dumps(info)[1]
# class GetInfo(PostForm)
