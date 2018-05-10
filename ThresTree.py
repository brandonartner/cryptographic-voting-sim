from Toolkit import *
from Voter import Voter

class TreeNode:
    """ Nodes used by the Tree object

    Attributes:
        addr (String): Address of this node.
        parent (TreeNode): Parent node.
        documents (list): Documents list.
        voter (Voter): Voter object.
        finalized (boolean): Keeps track of whether this node has been finalized.
        current_vote (String, String): The documents that is currently being voted on.
        already_voted (list): List of node address that have already voted.

    Note:
        already_voted variable is only used if this node has child nodes.

    """

    def __init__(self, addr, parent=None):
        """Split a node from being a leaf to having children.

        Args:
            addr (String): The address of the node with the format '#:#:#:...'

            parent (TreeNode): The parent node.
 
        """

        self.addr = addr
        self.parent = parent
        self.documents = {}
        self.voter = None
        self.finalized = False
        self.current_vote = None
        self.already_voted = []


    def split(self, n, k):
        """Split a node from being a leaf to having children.

        Args:
            n (int): The number of key to generate for this voter.

            k (int): The number of vote required to pass a vote.
 
        """

        assert n >= k, 'n<k: invalid arguements. n must be greater than or equal to k.'
        
        if self.voter:
            # Maybe raise an exception instead, idk which type though?
            print('Cannot split voter node.')
            return 

        self.children = {}
        self.n = n
        self.k = k

        for i in range(n):
            childAddr = '{}:{}'.format(self.addr, i+1)
            child = TreeNode(childAddr, self)

            self.children[childAddr] = child


    def finalize(self, data=None):
        """Creates a voter object for each non-leaf node and sets key data for each leaf.

        Args: 
            data (int, int): key data from parent nodes

        Returns: 
            boolean: True if the signature is correct, False otherwise.
 
        """

        if not self.finalized:

            if hasattr(self,'children'):
                if data:
                    print('Initializing voter for {} with data:\n ({},{}).\n'.format(self.addr, data[0], base_convert(data[1],92)))
                else:
                    print('Initializing voter for {} with data:\n {}.'.format(self.addr,data))

                # should this check if data is a key pair
                if data:
                    data = key_to_data(data, self.n)
                    # if data is given, the size of the prime needs to be increased to a bigger multiple of 128
                    #       Note: 128 because the RSA keys need the prime size to be a multiple of 128.
                    self.voter = Voter(self, self.n,self.k, prime_size=next_multiple_of_128(data))
                else:
                    self.voter = Voter(self, self.n,self.k)

                keys = self.voter.generate_scheme(data)
                self.finalized = True

                for i, child in enumerate(self.children.values()):
                    child.finalize(keys[i])

            else:
                print('{} has gotten the data:\n ({},{}).\n'.format(self.addr, data[0], base_convert(data[1],92)))
                self.data = data
        else:
            print('Error: Node at {} is already finalized.'.format(self.addr))


    def vote(self, doc, key=None):
        """Votes on a given document

        Args: 
            doc (String, String): The document being voted on. First element is the file name. Second is the document's text.

            key (int, int): key data passed up from child nodes

        Todo: 
            Turn current_vote into a queue of documents waiting to be voted on.
        """
        if self.addr in self.parent.already_voted:
            print('{} has already voted in the current vote.'.format(self.addr))
            return

        if hasattr(self, 'data'):
            # if the node has data, then it is a leaf and its key is added to the active vote.

            if not self.parent.documents.get(doc[0]):
                # If the document being voted on isn't in the documents list, add it
                print('Document \'{}\' has been added to {}\'s documents list.'.format(doc[0], self.parent.addr))
                self.parent.documents[doc[0]] = [doc[1],(0,0)]

            elif doc[1] != self.parent.documents[doc[0]][0]:
                # If the document being voted on is different in the documents list, update it?
                # Probably shouldn't be able to just change the document text like this.
                print('Document \'{}\' has been updated and is now available for voting on.'.format(doc[0]))
                self.parent.documents[doc[0]] = [doc[1],(0,0)]

            self.__send_vote(doc, self.data)

        elif key:
            self.__send_vote(doc, key)


    def __send_vote(self, doc, key):
        """Private helper function, submit the vote and ensures that the document is the one being voted on.

        Args:
            doc (String, String): The document being voted on. First element is the file name. Second is the document's text.

            key (int, int): key data being sent for a vote.

        Todo: 
            Turn current_vote into a queue of documents waiting to be voted on.
        """

        if not self.parent.current_vote or self.parent.current_vote == doc:
            # if there isn't a different document being voted on
            print('{} voted to sign {}.'.format(self.addr,doc))
            self.parent.current_vote = doc
            self.parent.already_voted.append(self.addr)
            signature, vote_finished = self.parent.voter.add_key_to_signature(key, doc)

            if signature and self.parent:
                self.parent.documents[doc[0]][1] = signature
                print('\'{}\' has been signed by node {}'.format(doc[0],self.parent.addr))
                self.parent.current_vote = None

                self.parent.already_voted = []

            if vote_finished and self.parent:
                self.parent.current_vote = None
                self.parent.already_voted = []
        else:
            print('{} tried to vote to sign {}, but {} is being voted on.'.format(self.addr,doc,self.current_vote))


    def show_documents(self, verified_only=False):
        """Displays all of the documents for root.

        Args: 
            verified_only (boolean): Flag to only print verified/signed documents

        Todo: 
            Implement this for all levels of ducument sets. e.g. print documents for address 0:2. 
            Requires implementing DSA signing on all levels.
        """

        print('\n-------------------------------------')
        for docname,doc in self.documents.items():
            if len(doc)==2:
                verified = self.voter.verify(doc[0],doc[1])
            else:
                verified = False

            if not verified_only:
                print('Title: {}\n Text: {}'.format(docname,doc[0]))
                print('Document is Signed.\n' if verified else 'Document is Unsigned.\n')
            elif verified:
                print('Title: {}\n Text: {}'.format(docname,doc[0]))
                print('Document is Signed.\n')

            print('-------------------------------------')


class ThresTree:
    """ Tree designed to be used with Adi Shamir's (n, k)-thresholding scheme.

    Attributes:
        root (TreeNode): The root node of the tree.

    """

    def __init__(self):
        self.root = TreeNode('0')

    def search(self, name):
        """Searches for a node at a given address.

        Args: 
            name (String): Address of node with the format '#:#:#:...'.

        Returns: 
            TreeNode: A node with the corresponding address.
 
        """

        if name == '0':
            return self.root

        location = name.split(':')

        node = self.root
        label = location[0]

        for addr in location[1:]:
            label = label + ':' + addr
            node = node.children.get(label)

            if node == None:
                print('{} does not exist.'.format(name))
                return

        return node

    def addChild(self, addr):
        """Add a child node to a node at a given address.

        Args:
            addr (String): Address of node that new node is being added to with the format '#:#:#:...'.
 
        """


        if hasattr(self, 'finalized'):
            print('Cannot alter finalized tree.')
            return

        node = self.search(addr)

        if hasattr(node, 'n'):
            numChildren = len(node.children.keys())
            childAddr = '{}:{}'.format(node.addr, numChildren+1)
            child = TreeNode(childAddr, node)

            node.children[childAddr] = child

        else:
            print('Cannot add to unsplit node.')

    def removeChild(self, addr):
        """Removes a child node of a node at a given address. Removes a random child node.

        Args: 
            addr (String): Address of node that node is being removed from with the format '#:#:#:...'.
 
        """

        if hasattr(self, 'finalized'):
            print('Cannot alter finalized tree.')
            return

        node = self.search(addr)
        childAddr = '{}:{}'.format(node.addr, len(node.children.keys()))

        del(node.children[childAddr])

    def propagate(self, data=None):
        """Propogates the tree with data. If none is given a DSA key-pair will be generated by the Voter class.

        Args: 
            data (int): The data to be propogated down the tree. (Usually None)
 

        """
        if hasattr(self, 'finalized'):
            print('Tree already propagated.')
            return 

        self.root.finalize(data)

        self.finalized = True

    def display(self):
        print('--------------------------------------------------')
        self.displayHelper(self.root, 0)
        print('--------------------------------------------------')

    def displayHelper(self, node, depth):
        if hasattr(node, 'data'):
            print('{}{}'.format(depth*'\t', node.addr))
        else:
            print('{}{} - Currently Voting On: {}'.format(depth*'\t', node.addr, node.current_vote))

        if hasattr(node, 'children'):
            for child in node.children.values():
                # too bad python doesn't have tail call optimization
                self.displayHelper(child, depth+1)


if __name__ == '__main__':
    import numpy as np
    np.random.seed(0)

    tree = ThresTree()

    tree.root.split(5, 3)
    tree.search('0:1').split(4, 2)
    tree.addChild('0:1')
    tree.removeChild('0')

    data = 10
    tree.propagate(data)
    tree.addChild('0:1')
    tree.removeChild('0')
    tree.display()
    tree.search('0:5')

