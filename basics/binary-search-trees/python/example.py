# Modified from https://github.com/shushrutsharma/Data-Structures-and-Algorithms-Python/blob/master/03.%20Data%20Structures/Trees/Binary_Search_Tree.py

from __future__ import annotations # Allows for self type hinting
from random import randint         # Used to generate random numbers
from dataclasses import dataclass  # Used to make objects more memory efficient

@dataclass
class Node:
    value: int
    left: Node = None
    right: Node = None

@dataclass
class BST:
    root:Node = None
    number_of_nodes:int = 0

    def insert(self, value:int) -> None:
        """
        
        For the insert method, we check if the root node is None, then we make the root node point to the new node
        Otherwise, we create a temporary pointer which points to the root node at first.
        Then we compare the data of the new node to the data of the node pointed by the temporary node.
        If it is greater then first we check if the right child of the temporary node exists, if it does, then we update the temporary node to its right child
        Otherwise we make the new node the right child of the temporary node
        And if the new node data is less than the temporary node data, we follow the same procedure as above this time with the left child.
        The complexity is O(log N) in avg case and O(n) in worst case.

        Parameters
        ----------
        value : int
            The number to append
        """
        new_node = Node(value)
        if self.root == None:
            self.root = new_node
            self.number_of_nodes += 1
            return
        else:
            current_node = self.root
            while(current_node.left != new_node) and (current_node.right != new_node):
                if new_node.value > current_node.value:
                    if current_node.right == None:
                        current_node.right = new_node
                    else:
                        current_node = current_node.right
                elif new_node.value < current_node.value:
                    if current_node.left == None:
                        current_node.left = new_node
                    else:
                        current_node = current_node.left
                else:
                    return # Node is in tree
            self.number_of_nodes += 1
            return 

    def search(self,value:int) -> tuple[bool, int]:
        """Search for a Node, and return a bool indicating if it is there and the number of operations it took to find or not find it
        
        It will follow similar logic as to the insert method to reach the correct position.

        Parameters
        ----------
        value : int
            The number to search for

        Returns
        -------
        bool, int
            Boolean is if it was found, the int is the number of operations to find (or not find) number
        """
        operations = 0
        if self.root == None:
            return False, 1
        else:
            current_node = self.root
            while True:
                if current_node == None:
                    operations += 1
                    return False, operations
                if current_node.value == value:
                    operations += 1
                    return True, operations
                elif current_node.value > value:
                    operations += 1
                    current_node = current_node.left
                elif current_node.value < value:
                    operations += 1
                    current_node = current_node.right


    def remove(self, value:int) -> None:
        """Removes a node of provided value if it's present

        Parameters
        ----------
        value : int
            The integer to remove
        """
        if self.root == None: #Tree is empty
            return
        current_node = self.root
        parent_node = None
        while current_node!=None: #Traversing the tree to reach the desired node or the end of the tree
            if current_node.value > value:
                parent_node = current_node
                current_node = current_node.left
            elif current_node.value < value:
                parent_node = current_node
                current_node = current_node.right
            else: #Match is found. Different cases to be checked
                #Node has left child only
                if current_node.right == None:
                    if parent_node == None:
                        self.root = current_node.left
                        return
                    else:
                        if parent_node.value > current_node.value:
                            parent_node.left = current_node.left
                            return
                        else:
                            parent_node.right = current_node.left
                            return

                #Node has right child only
                elif current_node.left == None:
                    if parent_node == None:
                        self.root = current_node.right
                        return
                    else:
                        if parent_node.value > current_node.value:
                            parent_node.left = current_node.right
                            return
                        else:
                            parent_node.right = current_node.right
                            return

                #Node has neither left nor right child
                elif current_node.left == None and current_node.right == None:
                    if parent_node == None: #Node to be deleted is root
                        current_node = None
                        return
                    if parent_node.value > current_node.value:
                        parent_node.left = None
                        return
                    else:
                        parent_node.right = None
                        return

                #Node has both left and right child
                elif current_node.left != None and current_node.right != None:
                    del_node = current_node.right
                    del_node_parent = current_node.right
                    while del_node.left != None: #Loop to reach the leftmost node of the right subtree of the current node
                        del_node_parent = del_node
                        del_node = del_node.left
                    current_node.value = del_node.value #The value to be replaced is copied
                    if del_node == del_node_parent: #If the node to be deleted is the exact right child of the current node
                        current_node.right = del_node.right
                        return
                    if del_node.right == None: #If the leftmost node of the right subtree of the current node has no right subtree
                        del_node_parent.left = None
                        return
                    else: #If it has a right subtree, we simply link it to the parent of the del_node
                        del_node_parent.left = del_node.right
                        return
        return


def test_number_of_checks(number_of_nodes:int=10_000, number_of_searches:int=100, max_number: int=1_000_000) -> tuple[list[int],list[int]]:
    """Tests a list and BST of number_of_nodes of random numbers between 0-1_000_000 number_of_searches times

    Returns
    -------
    tuple[list[int],list[int]]
        A tuple of two lists of integers, the first is the number of checks the BST did, and second is number of checks the linear search did
    """
    bst = BST()
    l = [0 for _ in range(number_of_nodes)] # Pre-allocating memory for list
    
    for _ in range(number_of_nodes):
        x = randint(0, max_number)
        bst.insert(x)
        l.append(x)

    l.sort() # sort the list

    bst_checks = []
    list_checks = []
    
    for _ in range(number_of_searches): # Search for random numbers
        x = randint(0, max_number)

        bst_checks.append(bst.search(x)[1])

        for index, item in enumerate(l):
            if item > x:
                list_checks.append(index+1)
                break
            if item == x:
                list_checks.append(index+1)
                break
    return bst_checks, list_checks


if __name__ == '__main__':
    runs = [] # Averages

    number_of_runs = 10

    bst_average = 0
    l_average = 0

    for _ in range(number_of_runs):
        bst_checks, list_checks = test_number_of_checks()

        runs.append([sum(bst_checks)/len(bst_checks), sum(list_checks)/len(list_checks)])
        bst_average += sum(bst_checks)/len(bst_checks)
        l_average += sum(list_checks)/len(list_checks)
        print(f"BST Number of checks: {bst_checks}\nList Number of checks: {list_checks}")
    
    print(f"\n{'='*30}\nBST averaged {bst_average/number_of_runs} checks\nList averaged {l_average/number_of_runs} checks\nBST was {(l_average/number_of_runs)/(bst_average/number_of_runs):.2f}x faster")

