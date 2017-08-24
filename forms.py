from controls import *
from send_email import activation_email
import json

class PostForm():
	def __init__(self):
		self.current = request_info()
		self.filled = filled_reqs()

		self.leng = len(self.current) 
		self.leng_2 = len(self.filled)
		self.state="normal"
		if self.current == [[]]:
			self.leng=0
		if self.filled == [[]]:
			self.leng_2=0
class AdminForm():
	
	def __init__(self):
		self.current = request_info()
		self.filled = filled_reqs()

		self.leng = len(self.current) 
		self.leng_2 = len(self.filled)
		self.state="normal"
		if self.current == [[]]:
			self.leng=0
		if self.filled == [[]]:
			self.leng_2=0

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
		self.id = data["id"]
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
	def delete_req(self, rid):
		del_req(rid)

	def changeName(self, newname):
		change_name(self.id, newname)	
