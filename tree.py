from polynomials import *

class TreeNode:
    ''' Nodes used by the Tree object
    '''

    def __init__(self, addr, parent=None):
        self.addr = addr
        self.parent = parent

    def split(self, n, k):
        assert n >= k

        self.n = n
        self.k = k
        self.children = {}

        for i in range(n):
            childAddr = '{}:{}'.format(self.addr, i)
            child = TreeNode(childAddr, self)

            self.children[childAddr] = child

    def leaf(self, data):
        self.data = data

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

    def propagate(self):
        stack = [self.root]

        while stack:
            node = stack.pop()

            for child in node.children

    def remove(self, name):
        pass

if __name__ == '__main__':
    tree = ThresTree()
    tree.root.split(5, 3)
    tree.search('0:1').split(4, 2)

    print(tree.root.children)
    print(tree.search('0:1').children)

