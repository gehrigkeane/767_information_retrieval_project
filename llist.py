class posting:
	def __init__(self):
		self.file_name = None # String value
		self.word_num = None # Int value
		self.term_f = None # Int value
		self.next = None # contains the reference to the next posting


class posting_list:
	def __init__(self):
		self.head = None
		self.tail = None
		self.length = 0

	def add(self, fn, wn):
		self.length += 1
		nn = posting() # create a new posting
		nn.file_name = fn
		nn.word_num = [wn]
		nn.term_f = 1

		# Append new nodes to the back of the list
		if self.tail:
			self.tail.next = nn
			self.tail = nn
		else:
			self.head = nn
			self.tail = nn

	def check(self, fn, wn):
		n = self.find(fn) 
		if n:
			# have the correct posting
			n.term_f += 1
			n.word_num.append(wn)
		else:
			# No posting exists with filename
			self.add(fn, wn)

	def find(self, fn):
		n = self.head
		while n:
			if n.file_name == fn:
				return n
			n = n.next
		return None

	def print_postings(self):
		n = self.head # cant point to ll!
		while n:
			print ("[fn:" + str(n.file_name) + ", wn:" + str(n.word_num) + ", tf:" + str(n.term_f) + "] -> ", end="")
			n = n.next
		print ("None", end="")
