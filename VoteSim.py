import re
from ThresTree import ThresTree
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
from fuzzyfinder import fuzzyfinder
from pygments.lexers.python import Python3Lexer
import sys

commands = {'vote': ['vote addr filename','No Usage Info'],
			
			'documents': ['Shows the documents set for a given address.',
							('documents [#:#:#:...] [-v]\n'
										'\t#:#:#:..., the address of the node the new node is being added to. If none specified, assumes root.\n'
										'\t-v, show only verified. (Currently only works on root node.)\n')],

			'display': ['display','No Usage Info'],

			'help': ['help','No Usage Info'],

			'quit': ['quit','No Usage Info'],

			}

CommandCompleter = WordCompleter(list(commands.keys()),
                                    ignore_case=True)

class VoteSim():
	"""docstring for VoteSim"""
	def __init__(self, tree):
		self.tree = tree


	def help(self, command=None):
		"""Prints help information.
		"""
		# If a command is given and it is in the commands dictionary, print the help info
		if command is not None and command in commands:
			print('------------------------------------------')
			print('{0} - {1[0]}\n\t{1[1]}\n'.format(command,commands[command]))
			print('------------------------------------------\n')
		else:
			# If the command didn't exist or none was given, print the help info for all commands
			for command_name in commands:
				print('------------------------------------------')
				print('{0} - {1[0]}\n\t{1[1]}\n'.format(command_name,commands[command_name]))
				print('------------------------------------------\n')

	def parse(self, user_input):
		command = user_input.split()

		if re.match('vote', command[0]):
			vote = command[1]
			fileName = command[2]

			documentText = open(fileName, 'r').read()
			
			votingNode = self.tree.search(vote)
			if votingNode:
				votingNode.vote((fileName, documentText))

		elif re.match('documents', command[0]):
			addr = '0'
			if False:
				pass	# if an address is specified, set addr to that address
			if '-v' in command:
				self.tree.search(addr).show_documents(verified_only=True)
			else:
				self.tree.search(addr).show_documents()


		elif re.match('display', command[0]):
			self.tree.display()
		elif args[0] == 'help' or args[0] == 'h':
			if len(args) > 1:
				if len(args) == 2 and re.match("[a-zA-Z]+",args[1]):
					self.help(args[1])
				else:
					raise AttributeError(command)
			else:
				self.help()
		else:
			raise NameError(args[0])

		
	def repl(self):
		"""REPL function to simulate a vote. Loops until quit is called.
		"""
		print('Now Simulating a Vote. Enter h for list of commands.')
		while 1:
			try:
				# if the input stream is from keyboard use fancy repl, if not use basic
				if sys.stdin.isatty():
					user_input = prompt(u'>>>',
										# uses a history file
				                        history=FileHistory('voting_history.txt'),
				                        # uses auto suggest from history functionality
				                        auto_suggest=AutoSuggestFromHistory(),
				                        # uses auto complete
				                        completer=CommandCompleter,
				                        # uses python3 syntax highlighting
				                        # this might be pointless
				                        lexer=Python3Lexer,
				                        )
				else:
					user_input = input('>>>')

				if user_input == 'q' or user_input == 'quit':
					break

				self.parse(user_input)

		     
			except NameError as e:
				print(e.args[0] + ': command not found.\nTry \'help\' or \'h\'.')
			except AttributeError as e:
				print(e.args[0] + ': invalid use.\nTry \'help [command]\' or \'h [command]\'.')
			except AssertionError as e:
				print(e.args[0])
