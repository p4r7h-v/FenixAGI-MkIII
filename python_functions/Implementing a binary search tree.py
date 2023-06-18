class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


class BinarySearchTree:

    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if key < node.val:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert_recursive(node.left, key)
        else:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert_recursive(node.right, key)

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None or node.val == key:
            return node

        if key < node.val:
            return self._search_recursive(node.left, key)

        return self._search_recursive(node.right, key)

    def inorder_traversal(self, node):
        if node:
            self.inorder_traversal(node.left)
            print(node.val, end=" ")
            self.inorder_traversal(node.right)


# Example usage
bst = BinarySearchTree()
keys = [50, 30, 20, 40, 70, 60, 80]

for key in keys:
    bst.insert(key)

print("In-order traversal:")
bst.inorder_traversal(bst.root)

search_key = 60
result = bst.search(search_key)
if result:
    print(f"\nFound {search_key} in the binary search tree.")
else:
    print(f"\n{search_key} not found in the binary search tree.")