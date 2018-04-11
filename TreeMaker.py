import re

class OrgTree():
	"""docstring for OrgTree"""
	def __init__(self, display_toggle=True):
		super(OrgTree, self).__init__() 	
		self.display_toggle = display_toggle


	def add(self, parent_node=None):
		print("Unimplemented: For now, imagine a new node was just added.")
		
	def remove(self, node):
		print("Unimplemented: For now, imagine a node was just deleted.")

	def clear(self):
		print("Unimplemented: For now, imagine the whole tree was deleted.")

	def display(self, toggle=False):
		print("Unimplemented: For now, imagine a beautiful tree was just printed out.")

		if toggle:
			self.display_toggle = not self.display_toggle
			print("OrgTree tree change display set to: "+str(self.display_toggle))

class OrgMaker():
	"""docstring for OrgMaker"""
	def __init__(self):
		super(OrgMaker, self).__init__
		self.org = OrgTree()

	def help(self, command=''):
		"""Prints help information.
		"""
		if command == 'add' or command == '':
			print('Name: \n\tadd - Adds n child nodes to the specified node in the organization tree.')
			print(('Usage: \n\tadd n k [#:#:#:...]'
								'n, is the number of children to make.'
								'k, is the number of keys from the children nodes that are needed to sign something.'
								'The last arguement is the address of the node the new nodes is being added to,'
								'if none is specified it is assumed the root is being added (if there isn\'t already).'))
		if command == 'remove' or command == '':
			print('Name: \n\tremove - Removes the specified node from the organization tree.')
			print(('Usage: \n\tremove #:#:#:...'
								'The last arguement is the address of the node that is being removed.'))
		if command == 'clear' or command == '':
			print('Usage: clear')
		if command == 'finalize' or command == '':
			print('Usage: finalize')
		if command == 'display' or command == '':
			print('Usage: display [--always;-a]')
		if command == '':
			print('Usage: quit|q')


	def parse(self,data):
		args = data.lower().split(' ')

		# add n k [#:#:#:...:#]
		if args[0] == 'add':
			self.org.add()

		# remove #:#:#:...:#
		elif args[0] == 'remove':
			self.org.remove(None)
		
		# clear
		elif args[0] == 'clear':
			self.org.clear()
		
		# finalize
		elif args[0] == 'finalize':
			print('Idk what finalize does rn.')

		# display [--always,-a]
		elif args[0] == 'display':
			if len(args) > 1:
				if len(args) <= 2 and re.match("(--always|-a)",args[1]):
					self.org.display(toggle=True)
				else:
					print("Invalid Use of display.")
					self.help('display')
			else:
				self.org.display()
		
		# help
		elif args[0] == 'help' or args[0] == 'h':
			self.help()
		else:
			print(args[0] + ', is not a recognized command.\nType help or h for a list of commands.')

	def repl(self):
		done = False
		while not done:
			line = input('>>>')
			if line == 'q' or line == 'quit':
				done = True
			else:
				self.parse(line)

if __name__ == '__main__':
	orgMaker = OrgMaker()
	orgMaker.repl()