Alex Cartwright
CSI-270 : Data Structures with Python
12/4/2020
Chapter 7.13-7.17 AVL Trees + Binary Search Tree balancing
"""
import pandas as pd
import numpy as np


class TreeNode:
    """
    Initializes a Tree Node object to categorize the node and its
    index, payload, anf any children or parent if applicable.
    """
    def __init__(self,key,val,left=None,right=None,parent=None):
        """
        Initializer for TreeNode object
        :param key: (int) index that the node is at
        :param val: () value or payload assigned to the TreeNode
        :param left: (TreeNode) TreeNode found as the left child
        :param right: (TreeNode) TreeNode found as right child
        :param parent: (TreeNode) TreeNode that is parent of this
        """
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        """
        Does this TreeNode have a left child
        :return: the left TreeNode child. If none found, then None
        """
        return self.leftChild

    def hasRightChild(self):
        """
        Does this TreeNode have a right child
        :return: the right TreeNode child. If none found, then None
        """
        return self.rightChild

    def isLeftChild(self):
        """
        Is this TreeNode a left child
        :return: True if this TreeNode has a parent AND is the left
        child of that node; else, False
        """
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        """
        Is this TreeNode a right child
        :return: True if this TreeNode has a parent AND is the right
        child of that node; else, False
        """
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        """
        Is this TreeNode the Root node
        :return: True if this TreeNode has no parent; else, False
        """
        return not self.parent

    def isLeaf(self):
        """
        Is this TreeNode a Leaf node
        :return: True if this TreeNode has no children; else, False
        """
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        """
        Does this TreeNode have any children
        :return: True if this Treenode has a child; else, False
        """
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        """
        Does this TreeNode have 2 children
        :return: True if this TreeNode has both left and right
        child; else, False
        """
        return self.rightChild and self.leftChild

    def spliceOut(self):
        """
        Removes a successor.
        :return:
        """
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None
        elif self.hasAnyChildren():
            if self.hasLeftChild():
                if self.isLeftChild():
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
                self.leftChild.parent = self.parent
            else:
                if self.isLeftChild():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild
                self.rightChild.parent = self.parent

    def findSuccessor(self):
        """
        If a node is being removed that has two children, find his
        successor to put in his place. The successor should be the
        next succesesive key.
        :return:
        """
        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            if self.parent:
                   if self.isLeftChild():
                       succ = self.parent
                   else:
                       self.parent.rightChild = None
                       succ = self.parent.findSuccessor()
                       self.parent.rightChild = self
        return succ

    def findMin(self):
        """
        Searching the right tree from the "to-be-removed" node,
        parse the left-most node children until the minimum largest
        node is dicovered.
        :return: (TreeNode) Minimum largest TreeNode from the
        "to-be-removed" node key
        """
        current = self
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def replaceNodeData(self,key,value,lc,rc):
        """
        Replace the node information at this Node; for deleting nodes
        :param key: (int) key to update
        :param value: () Value to update
        :param lc: (TreeNode) left child to update
        :param rc: (TreeNode) right child to update
        :return: None
        """
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self



class BinarySearchTree:
    """
    Used to manipulate or update the TreeNode.
    """

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        """
        Return the size of the current binary tree
        :return: (int) Size of current binary tree
        """
        return self.size

    def __len__(self):
        return self.size

    def put(self,key,val):
        """
        Test if the tree already has a root and create a new
        TreeNode if applicable as the Root.
        :param key: (int) index of the new Node
        :param val: () Value/payload that the new Node has
        :return: None
        """
        if self.root:
            self._put(key,val,self.root)
        else:
            self.root = TreeNode(key,val)
        self.size = self.size + 1

    def _put(self,key,val,currentNode):
        """
        If a Tree has a root, find the appropriate place to add the
        new TreeNode and insert it. Helper method to put()
        :param key: key to put
        :param val: value to put
        :param currentNode: Node to start at
        :return: None
        """
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                   self._put(key,val,currentNode.leftChild)
            else:
                   currentNode.leftChild = TreeNode(key, val,
                                                parent=currentNode)
        else:
            if currentNode.hasRightChild():
                   self._put(key,val,currentNode.rightChild)
            else:
                   currentNode.rightChild = TreeNode(key, val,
                                                parent=currentNode)

    def __setitem__(self,k,v):
       """
       Adds new item to the Tree
       :param k: key to put
       :param v: value to put
       :return: None
       """
       self.put(k,v)

    def get(self,key):
       """
       Get a the payload from a given key
       :param key: key being sought
       :return: payload if the key is found
       """
       if self.root:
           res = self._get(key,self.root)
           if res:
                  return res.payload
           else:
                  return None
       else:
           return None


    def _get(self,key,currentNode):
       """
       get - helper meathod to get key from current node
       :param key: key to get
       :param currentNode: Node to start at
       :return: payload of the key being sought
       """
       if not currentNode:
           return None
       elif currentNode.key == key:
           return currentNode
       elif key < currentNode.key:
           return self._get(key,currentNode.leftChild)
       else:
           return self._get(key,currentNode.rightChild)

    def __getitem__(self,key):
       """
       Overwrite the getitem function to perform self.get()
       :param key: key to get
       :return: payload of that key
       """
       return self.get(key)

    def __contains__(self,key):
       """
       Built-in function overwrite for contains; if the Tree
       contains a key
        :param key:
        :return: True if the Tree contains key; else false
       """
       if self._get(key,self.root):
           return True
       else:
           return False

    def delete(self,key):
      """
        Use the delete() function to remove a node from the tree.
        :param key:
        :return:
      """
      if self.size > 1:
         nodeToRemove = self._get(key,self.root)
         if nodeToRemove:
             self.remove(nodeToRemove)
             self.size = self.size-1
         else:
             raise KeyError('Error, key not in tree')
      elif self.size == 1 and self.root.key == key:
         self.root = None
         self.size = self.size - 1
      else:
         raise KeyError('Error, key not in tree')

    def __delitem__(self,key):
       self.delete(key)

    def remove(self,currentNode):
         """
         Remove a node from a Tree.
         :param currentNode: (TreeNode) node to be removed
         :return: None
         """
         if currentNode.isLeaf(): #leaf
           if currentNode == currentNode.parent.leftChild:
               currentNode.parent.leftChild = None
           else:
               currentNode.parent.rightChild = None
         elif currentNode.hasBothChildren(): #interior
           succ = currentNode.findSuccessor()
           succ.spliceOut()
           currentNode.key = succ.key
           currentNode.payload = succ.payload

         else: # this node has one child
           if currentNode.hasLeftChild():
             if currentNode.isLeftChild():
                 currentNode.leftChild.parent = currentNode.parent
                 currentNode.parent.leftChild = currentNode.leftChild
             elif currentNode.isRightChild():
                 currentNode.leftChild.parent = currentNode.parent
                 currentNode.parent.rightChild = currentNode.leftChild
             else:
                 currentNode.replaceNodeData(currentNode.leftChild.key,
                                    currentNode.leftChild.payload,
                                    currentNode.leftChild.leftChild,
                                    currentNode.leftChild.rightChild)
           else:
             if currentNode.isLeftChild():
                 currentNode.rightChild.parent = currentNode.parent
                 currentNode.parent.leftChild = currentNode.rightChild
             elif currentNode.isRightChild():
                 currentNode.rightChild.parent = currentNode.parent
                 currentNode.parent.rightChild = currentNode.rightChild
             else:
                 currentNode.replaceNodeData(currentNode.rightChild.key,
                                    currentNode.rightChild.payload,
                                    currentNode.rightChild.leftChild,
                                    currentNode.rightChild.rightChild)
class AVLTreeNode(TreeNode):
    """
    TreeNode Child class to include balanceFactor attribute
    """
    def __init__(self, *args, **kwargs):
        super(AVLTreeNode, self).__init__(*args, **kwargs)
        self.balanceFactor = 0

class AVLTree(BinarySearchTree):
    """
    AVL Tree to balance a BinarySearchTree based on AVLTreeNode 
    balanceFactor attribute
    """
    def put(self, key, val):
        """
        Put a new AVL Tree Node object in the AVL Tree
        :param key: key to put
        :param val: value to put
        :return: None
        """
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = AVLTreeNode(key, val)

        self.size += 1

    def _put(self, key, val, currentNode):
        """
        Put method's helper method to handle special cases to put 
        new item into AVL Tree
        :param key: key to put
        :param val: valut to put
        :param currentNode: node to start from
        :return: None
        """
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = AVLTreeNode(key, val,
                                                      parent=currentNode)
                self.updateBalance(currentNode.leftChild)
        else:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = AVLTreeNode(key, val,
                                                       parent=currentNode)
                self.updateBalance(currentNode.rightChild)

    def updateBalance(self, node):
        """
        Update the balance of the AVL Tree from a node
        :param node: node to check and update balance of
        :return: None?
        """
        if node.balanceFactor > 1 or node.balanceFactor < -1:
            self.rebalance(node)
            return

        if node.parent is not None:
            if node.isLeftChild():
                node.parent.balanceFactor += 1
            elif node.isRightChild():
                node.parent.balanceFactor -= 1

            if node.parent.balanceFactor != 0:
                self.updateBalance(node.parent)

    def rebalance(self, node):
        """
        Rebalance the tree based on a node's balance factor
        :param node: node to test
        :return: None
        """
        if node.balanceFactor < 0:
            if node.rightChild.balanceFactor > 0:
                self.rotate_right(node.rightChild)
                self.rotate_left(node)
            else:
                self.rotate_left(node)
        elif node.balanceFactor > 0:
            if node.leftChild.balanceFactor < 0:
                self.rotate_left(node.leftChild)
                self.rotate_right(node)
            else:
                self.rotate_right(node)

    def rotate_left(self, rot_root):
        """
        Perform a left roration from a given node/root
        :param rot_root: "higher" value to perform rotation upon
        :return: None
        """
        new_root = rot_root.rightChild
        rot_root.rightChild = new_root.leftChild

        if new_root.leftChild is not None:
            new_root.leftChild.parent = rot_root
        new_root.parent = rot_root.parent

        if rot_root.isRoot():
            self.root = new_root
        else:
            if rot_root.isLeftChild():
                rot_root.parent.leftChild = new_root
            else:
                rot_root.parent.rightChild = new_root

        new_root.leftChild = rot_root
        rot_root.parent = new_root

        rot_root.balanceFactor = (rot_root.balanceFactor + 1
                                   - min(new_root.balanceFactor, 0))

        new_root.balanceFactor = (new_root.balanceFactor + 1
                                   + max(rot_root.balanceFactor, 0))

    def rotate_right(self, rot_root):
        """
        Perform a right roration from a given node/root
        :param rot_root: "higher" value to perform rotation upon
        :return: None
        """
        new_root = rot_root.leftChild
        rot_root.leftChild = new_root.rightChild

        if new_root.rightChild != None:
            new_root.rightChild.parent = rot_root
        new_root.parent = rot_root.parent

        if rot_root.isRoot():
            self.root = new_root
        else:
            if rot_root.isLeftChild():
                rot_root.parent.leftChild = new_root
            else:
                rot_root.parent.rightChild = new_root

        new_root.rightChild = rot_root
        rot_root.parent = new_root

        rot_root.balanceFactor = (rot_root.balanceFactor - 1
                                  - max(new_root.balanceFactor, 0))

        new_root.balanceFactor = (new_root.balanceFactor - 1
                                  + min(rot_root.balanceFactor, 0))


url = str(input("Enter the directory location of "
                  "FC_SHD_subsidy_analysis_2020-06-30.csv:"))
data_points = pd.read_csv(url)

def furman(data_points):
    """
    Code for using the Furman dataset. Not for current submission
    :param data_points:
    :return:
    """
    lats = data_points.latitude.to_dict()
    longs = data_points.longitude.to_dict()
    keys = {}
    i = 0
    for k in longs:
        keys[int(str(int(longs[k]*100000)) +
                 str(int(lats[k]*100000)))] = data_points.iloc[[i]]
        i +=1

    furman_tree = AVLTree()
    furman_tree.put(-73931474069799, pd.DataFrame([[40.6979914576,
                        -73.9314722564]],columns=["latitude",
                                                   "longitude"]))
    """furman_tree.root = AVLTreeNode(key=-73931474069799,
                                   val=pd.DataFrame([[
                40.6979914576,-73.9314722564]],columns=["latitude",
                                                   "longitude"]))"""
    for key in keys:
        furman_tree.put(key, keys[key])

    return furman_tree

furman_tree = furman(data_points)
""" At this point, the data is accurately loaded into an AVL Tree 
and is functionally a tree with all the data points in the format: 
    Key = concat(long*10000, lat*10000)
    Value = the dataframe row for that item
"""
print(furman_tree.root) #Will print the root... for testing