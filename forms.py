from controls import request_info, request_info_who, filled_reqs, del_req
import json
class PostForm():
    
	def __init__(self):
		self.info = request_info()
		self.leng = len(self.info[0]) 
		self.leng_2 = len(self.info)
		self.state="normal"

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
		# Call to store info of approved unfilled reqs
		self.info = request_info()
		self.leng = len(self.info[0]) 
		self.leng_2 = len(self.info)
		self.state='normal'

	def filled(self):
    	# Call to store info of filled requests
		self.info = filled_reqs()
		self.leng = len(self.info[0]) 
		self.leng_2 = len(self.info)
		self.state='filled'

	def unapproved(self):
    	# Call to store the unapproved reqs
		self.info = request_info(True)
		self.leng = len(self.info[0]) 
		self.leng_2 = len(self.info)
		self.state='unapproved'

	def delete_req(rid):
		del_req(rid)
		if self.state == 'filled':
			self.filled()
		elif self.state == 'unapproved':
 			self.unapproved()
		else:
			self.reset()	
