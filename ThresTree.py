from Toolkit import *

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

        if hasattr(self, 'voter'):
            print('Cannot split voter node.')
            return 

        self.n = n
        self.k = k
        self.p = None # set during propagation
        self.children = {}

        for i in range(n):
            childAddr = '{}:{}'.format(self.addr, i+1)
            child = TreeNode(childAddr, self)

            self.children[childAddr] = child

    def makeVoter(self, voter):
        if hasattr(self, 'n'):
            print('Organization node cannot also be voter node.')
            return

        if hasattr(self, 'voter'):
            print('This node is already a voter node.')
            return 

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
                y = polynomial.evaluate(x) % p
                key = (x, y)

                if hasattr(child, 'children'):
                    child.children
                    stack.append(child)
                    D.append(key_to_data(key, p))
                    print('{} added to stack'.format(addr))
                    
                else:
                    # do something with voters
                    print('{} given key {}'.format(addr, key))

        self.finalized = True

    def display(self):
        self.displayHelper(self.root, 0)

    def displayHelper(self, node, depth):
        print('{}{}'.format(depth*'\t', node.addr))

        if hasattr(node, 'children'):
            for child in node.children.values():
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

