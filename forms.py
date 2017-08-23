from controls import *
from send_email import activation_email
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

	def delete_req(self, rid):
		del_req(rid)
		if self.state == 'filled':
			self.filled()
		elif self.state == 'unapproved':
 			self.unapproved()
		else:
			self.reset()

	def invite_member(self, email, code):
		activation_email(email, code)
		create_pending(email, code)
	

class AccountForm():
	def __init__(self, username):
		data = my_info(username)
		self.username = username
		self.email = username + "@reed.edu"
		self.name = data["name"]
		self.admin = data["admin"]
		self.approved = data["approved"]
		current, filled = my_reqs(username)
		if current == None:
			self.currentRequests = [[]]
			self.currentLen= 0
		else:
			self.currentRequests = current
			self.currentLen= len(current)
		if filled == None:
			self.filledRequests = [[]]
			self.filledLen= 0
		else:			
			self.filledRequests = filled
			self.filledLen= len(filled)
