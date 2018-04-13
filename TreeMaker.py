import re
from ThresTree import ThresTree
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
import click
from fuzzyfinder import fuzzyfinder
from pygments.lexers.python import Python3Lexer

CommandCompleter = WordCompleter(['add', 'split', 'remove', 'clear', 'finalize', 'display', 'help', 'quit'],
                                    ignore_case=True)

class TreeMaker():
	"""docstring for TreeMaker"""
	def __init__(self):
		super(TreeMaker, self).__init__
		self.tree = ThresTree()

	def help(self, command=None):
		"""Prints help information.
		"""
		if command is None or command == 'add':
			print('Name: \n\tadd - Adds n child nodes to the specified node in the treeanization tree.\n')
			print(('Usage: \n\tadd n k [#:#:#:...]\n'
								'n, is the number of children to make.'
								'k, is the number of keys from the children nodes that are needed to sign something.'
								'The last arguement is the address of the node the new nodes is being added to,'
								'if none is specified it is assumed the root is being added (if there isn\'t already).\n'))
			print('-------------------------------------------------------------\n')
		if command is None or command == 'remove':
			print('Name: \n\tremove - Removes the specified node from the organization tree.\n')
			print(('Usage: \n\tremove #:#:#:...\n'
								'The last arguement is the address of the node that is being removed.\n'))
			print('-------------------------------------------------------------\n')
		if command is None or command == 'clear':
			print('Usage: clear\n')
			print('-------------------------------------------------------------\n')
		if command is None or command == 'finalize':
			print('Usage: finalize\n')
			print('-------------------------------------------------------------\n')
		if command is None or command == 'display':
			print('Usage: display [--always;-a]\n')
			print('-------------------------------------------------------------\n')
		if command is None:
			print('Usage: quit|q\n')
			print('-------------------------------------------------------------\n')


	def parse(self,command):
		command = command.lower()
		args = command.split(' ')

		# add n k [#:#:#:...:#]
		if args[0] == 'add':
			if len(args) > 1:
				if len(args) == 3: #and re.match("[0-9]+ [0-9]+",args[1]):
					pass #self.tree.add()
				elif len(args) == 4: #and re.match("[0-9]+ [0-9]+ ([0-9]+:?)+",args[1]):
					pass #self.tree.add()				
				else:
					print("Invalid use of add.")
					self.help('add')

		# split 
		elif args[0] == 'split':
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
				if len(args) == 2 and re.match("(--always|-a)",args[1]):
					pass #self.tree.display(toggle=True)
				else:
					raise 
			else:
				pass #self.tree.display()
		
		# help
		elif args[0] == 'help' or args[0] == 'h':
			if len(args) > 1:
				if len(args) == 2 and re.match("[a-zA-Z]",args[1]):
					self.help(args[1])
				else:
					raise AttributeError(command)
			else:
				self.help()
		else:
			raise NameError(args[0])


	def repl(self):
		while 1:
			try:
				user_input = prompt(u'>>>',
			                        #history=FileHistory('history.txt'),		# uses a history file
			                        auto_suggest=AutoSuggestFromHistory(),	# uses auto suggest from history functionality 
			                        completer=CommandCompleter,				# uses auto complete
			                        lexer=Python3Lexer,						# uses syntax highlighting
			                        )
				if user_input == 'q' or user_input == 'quit':
					break

				self.parse(user_input)

			    #click.echo_via_pager(user_input)

			except NameError as e:
				print(e.args[0] + ': command not found.\nTry \'help\' or \'h\'.')
			except AttributeError as e:
				print(e.args[0] + ': invalid use.\nTry \'help [command]\' or \'h [command]\'.')


if __name__ == '__main__':
	treeMaker = TreeMaker()
	treeMaker.repl()
