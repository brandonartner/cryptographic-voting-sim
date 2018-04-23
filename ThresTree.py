from Toolkit import *
from Voter import Voter

class TreeNode:
    ''' Nodes used by the Tree object
    '''

    def __init__(self, addr, parent=None):
        self.addr = addr
        self.parent = parent
        self.documents = {}
        self.voter = None
        self.finalized = False

    def split(self, n, k):
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

    def finalize(self,data=None):
        '''Creates a voter object for each non-leaf node.
            data should be a key pair.
        '''
        if not self.finalized:

            if hasattr(self,'children'):
                print('Initializing voter for {} with data {}.'.format(self.addr,data))
                # should this check if data is a key pair
                if data:
                    data = key_to_data(data, self.n)
                    # if data is given, the size of the prime needs to be increased to a bigger multiple of 128
                    #       Note: 128 because the RSA keys need the prime size to be a multiple of 128.
                    self.voter = Voter(self.n,self.k, prime_size=next_multiple_of_128(data))
                else:
                    self.voter = Voter(self.n,self.k)

                keys = self.voter.generate_scheme(data)
                self.finalized = True

                for i, child in enumerate(self.children.values()):
                    child.finalize(keys[i])

            else:
                print('{} has gotten the data {}.'.format(self.addr,data))
                self.data = data
        else:
            print('Error: Node at {} is already finalized.'.format(self.addr))

    def vote(self, doc):
        '''Votes
        '''
        if hasattr(self,'data'):
            # sends data, transformed back into a key, to the parent nodes voter class
            if doc not in self.documents.items():
                self.documents.update({doc[0]:doc[1]})
            self.parent.voter.add_key_to_signature(self.data, doc)

class ThresTree:
    ''' Tree designed to be used with
        Adi Shamir's (n, k)-thresholding scheme
    '''

    def __init__(self):
        self.root = TreeNode('0')

    def search(self, name):
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
        ''' Adds child to node at addr '''

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
        ''' Removes child from node at addr '''

        if hasattr(self, 'finalized'):
            print('Cannot alter finalized tree.')
            return

        node = self.search(addr)
        childAddr = '{}:{}'.format(node.addr, len(node.children.keys()))

        del(node.children[childAddr])

    def propagate(self, data=None):
        if hasattr(self, 'finalized'):
            print('Tree already propagated.')
            return 

        self.root.finalize(data)

        self.finalized = True

    def display(self):
        self.displayHelper(self.root, 0)

    def displayHelper(self, node, depth):
        if hasattr(node, 'data'):
            print('{}{} - [{},{}]'.format(depth*'\t', node.addr, node.data[0], hex(node.data[1])))
        else:
            print('{}{}'.format(depth*'\t', node.addr))

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

