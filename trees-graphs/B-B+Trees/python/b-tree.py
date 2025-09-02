from math import log, floor, ceil
from random import randint
from typing import Any, List, Optional, Tuple

class BTreeNode:
    def __init__(self, is_leaf: bool = False) -> None:
        """Represents a single node in a B-tree

        Parameters
        ----------
        is_leaf : bool, optional
            Indicates whether the node is a leaf node. Default is False
        """
        self.is_leaf: bool = is_leaf
        self.keys: List[Tuple[int, Any]] = []
        self.children: List['BTreeNode'] = []


class BTree:
    def __init__(self, min_degree: int) -> None:
        """Constructs an empty B-tree

        Parameters
        ----------
        min_degree : int
            The minimum degree (t) of the B-tree. Each node can contain at most 2*t - 1 keys

        Notes
        -----
        The B-tree maintains balance by ensuring that each node (except root) has between t and 2t children
        """
        self.root: BTreeNode = BTreeNode(is_leaf=True)
        self.t: int = min_degree

    def insert(self, key_value: Tuple[int, Any]) -> None:
        """Inserts a key-value pair into the B-tree

        Parameters
        ----------
        key_value : tuple of (int, Any)
            The key-value pair to insert

        Notes
        -----
        If the root node is full, the tree grows in height
        """
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            new_root = BTreeNode()
            self.root = new_root
            new_root.children.insert(0, root)
            self.split_child(new_root, 0)
            self.insert_non_full(new_root, key_value)
        else:
            self.insert_non_full(root, key_value)

    def insert_non_full(self, node: BTreeNode, key_value: Tuple[int, Any]) -> None:
        """Helper method to insert a key-value into a node that is not full

        Parameters
        ----------
        node : BTreeNode
            Node into which the key is to be inserted

        key_value : tuple of (int, Any)
            The key-value pair to insert
        """
        i = len(node.keys) - 1
        if node.is_leaf:
            node.keys.append((None, None))
            while i >= 0 and key_value[0] < node.keys[i][0]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key_value
        else:
            while i >= 0 and key_value[0] < node.keys[i][0]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self.split_child(node, i)
                if key_value[0] > node.keys[i][0]:
                    i += 1
            self.insert_non_full(node.children[i], key_value)

    def delete(self, node: BTreeNode, key_value: Tuple[int, Any]) -> None:
        """Deletes a key from the B-tree

        Parameters
        ----------
        node : BTreeNode
            The current node from which to start deletion

        key_value : tuple of (int, Any)
            The key-value pair to delete

        Notes
        -----
        Supports recursive deletion including merge and redistribution
        """
        t = self.t
        i = 0
        while i < len(node.keys) and key_value[0] > node.keys[i][0]:
            i += 1
        if node.is_leaf:
            if i < len(node.keys) and node.keys[i][0] == key_value[0]:
                node.keys.pop(i)
            return
        if i < len(node.keys) and node.keys[i][0] == key_value[0]:
            self.delete_internal_node(node, key_value, i)
        elif len(node.children[i].keys) >= t:
            self.delete(node.children[i], key_value)
        else:
            if i != 0 and i + 2 < len(node.children):
                if len(node.children[i - 1].keys) >= t:
                    self.delete_sibling(node, i, i - 1)
                elif len(node.children[i + 1].keys) >= t:
                    self.delete_sibling(node, i, i + 1)
                else:
                    self.delete_merge(node, i, i + 1)
            elif i == 0:
                if len(node.children[i + 1].keys) >= t:
                    self.delete_sibling(node, i, i + 1)
                else:
                    self.delete_merge(node, i, i + 1)
            elif i + 1 == len(node.children):
                if len(node.children[i - 1].keys) >= t:
                    self.delete_sibling(node, i, i - 1)
                else:
                    self.delete_merge(node, i, i - 1)
            self.delete(node.children[i], key_value)

    def delete_internal_node(self, node: BTreeNode, key_value: Tuple[int, Any], index: int) -> None:
        """
        Deletes a key from an internal node

        Parameters
        ----------
        node : BTreeNode
            Node containing the key

        key_value : tuple of (int, Any)
            Key-value pair to delete

        index : int
            Index of key in node.keys
        """
        t = self.t
        if len(node.children[index].keys) >= t:
            node.keys[index] = self.delete_predecessor(node.children[index])
        elif len(node.children[index + 1].keys) >= t:
            node.keys[index] = self.delete_successor(node.children[index + 1])
        else:
            self.delete_merge(node, index, index + 1)
            self.delete_internal_node(node.children[index], key_value, t - 1)

    def delete_predecessor(self, node: BTreeNode) -> Tuple[int, Any]:
        """
        Deletes and returns the predecessor key in subtree rooted at node

        Parameters
        ----------
        node : BTreeNode
            Subtree root to find the predecessor in

        Returns
        -------
        tuple
            Predecessor key-value pair
        """
        if node.is_leaf:
            return node.keys.pop()
        n = len(node.keys) - 1
        if len(node.children[n].keys) >= self.t:
            self.delete_sibling(node, n + 1, n)
        else:
            self.delete_merge(node, n, n + 1)
        return self.delete_predecessor(node.children[n])

    def delete_successor(self, node: BTreeNode) -> Tuple[int, Any]:
        """
        Deletes and returns the successor key in subtree rooted at node

        Parameters
        ----------
        node : BTreeNode
            Subtree root to find the successor in

        Returns
        -------
        tuple
            Successor key-value pair
        """
        if node.is_leaf:
            return node.keys.pop(0)
        if len(node.children[1].keys) >= self.t:
            self.delete_sibling(node, 0, 1)
        else:
            self.delete_merge(node, 0, 1)
        return self.delete_successor(node.children[0])

    def delete_merge(self, parent_node: BTreeNode, index1: int, index2: int) -> None:
        """
        Merges two children of a node during deletion

        Parameters
        ----------
        parent_node : BTreeNode
            The parent node

        index1 : int
            Index of one child to merge

        index2 : int
            Index of the other child to merge
        """
        child1 = parent_node.children[index1]
        if index2 > index1:
            child2 = parent_node.children[index2]
            child1.keys.append(parent_node.keys[index1])
            child1.keys.extend(child2.keys)
            child1.children.extend(child2.children)
            parent_node.keys.pop(index1)
            parent_node.children.pop(index2)
            merged_node = child1
        else:
            child2 = parent_node.children[index2]
            child2.keys.append(parent_node.keys[index2])
            child2.keys.extend(child1.keys)
            child2.children.extend(child1.children)
            parent_node.keys.pop(index2)
            parent_node.children.pop(index1)
            merged_node = child2

        if parent_node == self.root and len(parent_node.keys) == 0:
            self.root = merged_node

    def delete_sibling(self, parent_node: BTreeNode, index: int, sibling_index: int) -> None:
        """Redistributes keys between siblings to maintain B-tree properties

        Parameters
        ----------
        parent_node : BTreeNode
            The parent node

        index : int
            Index of the underfull child

        sibling_index : int
            Index of the sibling
        """
        child = parent_node.children[index]
        if index < sibling_index:
            sibling = parent_node.children[sibling_index]
            child.keys.append(parent_node.keys[index])
            parent_node.keys[index] = sibling.keys.pop(0)
            if sibling.children:
                child.children.append(sibling.children.pop(0))
        else:
            sibling = parent_node.children[sibling_index]
            child.keys.insert(0, parent_node.keys[index - 1])
            parent_node.keys[index - 1] = sibling.keys.pop()
            if sibling.children:
                child.children.insert(0, sibling.children.pop())

    def split_child(self, parent_node: BTreeNode, child_index: int) -> None:
        """Splits a full child node into two and updates the parent node

        Parameters
        ----------
        parent_node : BTreeNode
            The node with the full child

        child_index : int
            Index of the child to split
        """
        t = self.t
        full_child = parent_node.children[child_index]
        new_child = BTreeNode(is_leaf=full_child.is_leaf)

        parent_node.children.insert(child_index + 1, new_child)
        parent_node.keys.insert(child_index, full_child.keys[t - 1])

        new_child.keys = full_child.keys[t:]
        full_child.keys = full_child.keys[:t - 1]

        if not full_child.is_leaf:
            new_child.children = full_child.children[t:]
            full_child.children = full_child.children[:t]

    def print_tree(self, node: BTreeNode, level: int = 0) -> None:
        """Prints the B-tree structure to the console

        Parameters
        ----------
        node : BTreeNode
            The starting node (usually the root)

        level : int, optional
            Current tree depth level. Used for indentation
        """
        print(f"Level {level} keys={len(node.keys)}:", end=" ")
        for key in node.keys:
            print(key, end=" ")
        print()
        for child in node.children:
            self.print_tree(child, level + 1)

    def search_key(self, key: int, node: Optional[BTreeNode] = None) -> Optional[Tuple[BTreeNode, int]]:
        """Searches for a key in the B-tree

        Parameters
        ----------
        key : int
            The key to search for

        node : BTreeNode, optional
            Node to start search from. If None, starts from root

        Returns
        -------
        tuple or None
            Tuple of (node, index) if key is found; None otherwise

        Examples
        --------
        ```
        tree.search_key(42) # (BTreeNode, index)
        ```
        """
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i][0]:
            i += 1
        if i < len(node.keys) and key == node.keys[i][0]:
            return node, i
        elif node.is_leaf:
            return None
        else:
            return self.search_key(key, node.children[i])

if __name__ == '__main__':
  number_of_nodes = 1_000_000
  max_node_value = 100_000
  search_value = randint(0,max_node_value-1)
  t_value = 16
    
  B = BTree(t_value) 
  m = t_value * 2
  print(f"""
tree constructed with
\tt: {t_value}
\tMax Value: {max_node_value}
\tMinimum Height: {ceil(log(number_of_nodes+1, m))-1}
\tMaximum Height: {floor(log((number_of_nodes+1)/2, t_value))}
\tMinimum keys per level: {t_value-1}
\tMaximum Keys per level: {2*t_value - 1}
\tApproximate Average Searches: {log(number_of_nodes)//1}
\tApproximate Maximum Searches: {(log(number_of_nodes) * log(m))//1}
""")

  for i in range(number_of_nodes):
    B.insert((i,randint(0,max_node_value)))

  res = B.search_key(search_value)
  if res is not None:
    print(f"Keys in result row:\n\t{res[0].keys}\nTook {res[1]+1} checks to find {search_value}")
  else:
    print(f"Value {search_value} was not in tree")
