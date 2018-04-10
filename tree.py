import numpy as np
from polynomials import *

class TreeNode:
    ''' Nodes used by the Tree object
    '''

    def __init__(self, addr, parent=None):
        self.addr = addr
        self.parent = parent

    def split(self, n, k):
        assert n >= k
        
        if hasattr(self, 'n'):
            print('Node already split.')
            return 

        self.n = n
        self.k = k
        self.p = None # set later
        self.children = {}

        for i in range(n):
            childAddr = '{}:{}'.format(self.addr, i+1)
            child = TreeNode(childAddr, self)

            self.children[childAddr] = child

    def makeVoter(self, voter):
        self.voter = voter

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
            node = node.children[label]

        return node

    def propagate(self, data):
        stack = [self.root]
        D = [data]

        while stack:
            node = stack.pop(-1)
            d = D.pop(-1)
            polynomial, p = generate_polynomial(d, node.k)
            node.p = p

            for i, addr in enumerate(node.children.keys()):
                child = node.children[addr]
                x = int(addr.split(':')[-1])
                y = polynomial.evaluate(x)
                key = (x, y)

                if hasattr(child, 'children'):
                    child.children
                    stack.append(child)
                    D.append(key_to_data(key))
                    print('{} added to stack'.format(addr))
                    
                else:
                    # do something with voters
                    print('{} given key {}'.format(addr, key))

if __name__ == '__main__':
    np.random.seed(0)

    tree = ThresTree()
    tree.root.split(5, 3)
    tree.search('0:1').split(4, 2)

    data = 10
    tree.propagate(data)

