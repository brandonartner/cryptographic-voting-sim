import re
from ThresTree import ThresTree

class TreeMaker():
	"""docstring for TreeMaker"""
	def __init__(self):
		super(TreeMaker, self).__init__
		self.tree = ThresTree()

	def help(self, command=''):
		"""Prints help information.
		"""
		if command == 'add' or command == '':
			print('Name: \n\tadd - Adds n child nodes to the specified node in the treeanization tree.')
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
			pass #self.tree.add()

		# split 
		elif args[0] == 'split'
			pass #self.tree.split()

		# remove #:#:#:...:#
		elif args[0] == 'remove':
			pass #self.tree.remove(None)
		
		# clear
		elif args[0] == 'clear':
			pass #self.tree.clear()
		
		# finalize
		elif args[0] == 'finalize':
			print('Idk what finalize does rn.')

		# display [--always,-a]
		elif args[0] == 'display':
			if len(args) > 1:
				if len(args) <= 2 and re.match("(--always|-a)",args[1]):
					pass #self.tree.display(toggle=True)
				else:
					print("Invalid Use of display.")
					self.help('display')
			else:
				pass #self.tree.display()
		
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
	treeMaker = TreeMaker()
	treeMaker.repl()
