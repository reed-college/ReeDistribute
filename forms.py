from controls import request_info, request_info_who, filled_reqs
import json
class PostForm():
    
	def __init__(self):
		self.info = request_info()
		self.leng = len(self.info[0]) 
		self.leng_2 = len(self.info)

	def ListIt(self,post_n,type_n):
		while True:
			try:
				return self.info[post_n][type_n]
			except IndexError:
				#instead of "break" we should have a funciton that just posts "there are no active requests"
				break

	def GetLength(self):
		return self.leng_2

	def reset(self):
		self.info = request_info()
		self.leng = len(self.info[0]) 
		self.leng_2 = len(self.info)
	def filled(self):
		self.info = filled_reqs()
		self.leng = len(self.info[0]) 
		self.leng_2 = len(self.info)
	def unapproved(self):
		self.info = request_info(True)
		self.leng = len(self.info[0]) 
		self.leng_2 = len(self.info)