# Object that can create Dynamic nodeTree Data Structures
# Perfect for Machine Learning because when you think about it a nodeTree can actually be the equivalent of
# Any Vector consisting of features represented in multi dimensional space :)
# Can be used like JSON to create dynamic data structures fx. rapid design of file readers that used diffrent data structures
# In Theory this structure can handle any tree structure since, an maybe even my combination counter chains
# Do not set parrentNode for the root node, use "" or the Tree algorithm will get confuzed
# BUT ALLWAYS SET parrent node of all nodes under the root!!
# Uses same principle as hash Tables/Lists "key, value" pairs but here its just called nodeId, value
# Based on nodeTree but has addition functionality used in Analysis suchs as
# All node handling has 3 method types ex. for addNode
#   - addNode/addRelNode "add new node by value either relative to this node or at new last node if thisNodes parrentNode, def. add to end"
#   - addNodeObj/addRelNodeObj "add new node by object either relative to this node or at new last node if thisNodes parrentNode"
#   - addNodeObjCopy/addRelNodeObjCopy " add new node by object as a copy of otherNode either relative to this node or at new last node if thisNodes parrentNode"
#   - nodeTree can handly Unique nodes on two levels: 
# 0 = node is not unique  
# 1 = node is unique within entire nodeTree (nodeTree uniqueness)  
# 2 = node is unique within nodeChain, hence unique to its peerNodes (peerNode uniqueness)
# 3 = node is unique within parrentNode sub-nodeTree (subNode uniqueness)
# 4 = node is unqie within thisNode and its sub-nodeTree (sub-nodeTree uniqueness)
# - Auto Sorting by Frequency, most to least og least to most
# - Auto Frequency counting
# Uses a Simi-recursive Algorithm: Which mean instead of using alot of stack space calling it self recursiveli it returns nodes so the
# recursive process is minimized :)
# STATUS: COMPLETE, WORKING & TESTED
# IMPORTANT!! REMEMBER BINARY MATH: when looking-through arrays, lists, tables etc.. remeber ix goes from 0 - arraySize - 1, since 0 is counted in binary math!!
# WORKAROUND: Use "for item in array" and manually update ix, this way you wont have to worry about binary math ;)
# GOOD CODE PRACTICE: WHEN INPUT VALIDATION FAIL "Invalid input args" THE METHOD SHOULD TERMINATE AS FAST AS POSSIBLE
# TODO: Replace the Find node ix with thisNode where possible to speed up nodeTree methods (OK)
# TODO: Test It (OK)
# TODO: implement error_ attribute (OK)
# TODO: implement uniqueLevel_ so the node "knowns" wheter it is unique and how unique it is? (OK)
# TODO: If this nodeTree should handle dynamic dataTypes we must implement dynamic dataType handling on all value_ handlings/actions
class analysisNodeTree(object):
    def __init__(self, name_ = "", value_ = "",  parrentNode_="", nodeLevelSeparator_="."):
        self.subNodes_ = []
        self.parrentNode_ = parrentNode_
        self.nodeLevelSeparator_ = nodeLevelSeparator_
        self.freq_ = 1 # Frequncy count for thisNode value "def. 1 the node it self"
        self.error_ = "" # Hold "thisError text, can be read to see what went wrong when a nodeTree method returns nothing"
        self.uniqueLevel_ = 0 # Assume this node should not exist uniquely in the nodeTree "let other Metods decide this question!!"

        # Is this root node?
        if(self.parrentNode_ == ""):
            # This is Root so just set node ix 0
            self.nodeIx_ = 0
        else:
            # Calc node ix used when auto generating nodeId's
            self.nodeIx_ = self.parrentNode_.subNodeCount_

        self.value_ = value_
        self.name_ = name_
        self.subNodeCount_ = 0

        # is this a root node?
        if(self.parrentNode_ != ""):
            # Generate new key "NodeId" using the nodes location in the tree
            self.nodeId_ = self.parrentNode_.nodeId_ + self.nodeLevelSeparator_ + str(self.nodeIx_)
            # Update nodeLevel (Keeps track of what level in the nodeTree thisNode is at)
            self.nodeLevel_ = self.getNodeLevel()            
        else: # Assume this is root
            self.nodeId_ = "root"
            # Update nodeLevel
            self.nodeLevel_ = 0

        # Has name been specified?
        if(self.name_ == ""):
            # No node name so just assign def.
            self.name_ = "Node " + self.nodeId_            

    # Gets the level of thisNode based on its nodeId
    def getNodeLevel(self):
        thisNode = self
        
        ix=0
        nodeLevel=0
        while(ix != -1):
            ix = thisNode.nodeId_.find(thisNode.nodeLevelSeparator_, ix)
            # was a nodeLevel seperator found?
            if(ix > -1):
                nodeLevel += 1
                # Prepare search for next nodeLevel separator
                ix = ix + 1 
        
        # Return the nodeLevel
        return nodeLevel

    # Gets last/thisError that occured while handling thisNode
    def getError(self):
        return self.error_

#-------------------- All Nodes Handling --------------
#-------------------- ADD peerNode Handling -----------    
    # Add new peerNodeObj on same parrentNode/nodeChain as thisNode as new last-subNode
    def addPeerNodeObj(self, newPeerNode_, uniqueLevel_=0):
        thisNode = self
        
        # Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => rootNode does not have peerNodes
            thisNode.error_ = "addPeerNodeObj: rootNode does have peerNodes!!"
            return ""

        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1                
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Ensure the newPeerNode has been associated/linked to thisNodes parrentNode
        newPeerNode_.parrentNode_ = thisNode.parrentNode_
        # Ensure the newPeerNode has the specified uniqueness level
        newPeerNode_.uniqueLevel_ = uniqueLevel_
        
        # Add the new peerNode
        thisNode.parrentNode_.subNodes_.append(newPeerNode_)

        # Update sub node count
        thisNode.parrentNode_.subNodeCount_ += 1
        # Ensure nodeIx is has lastNode ix so it can be fixed 
        newPeerNode_.nodeIx_ = thisNode.parrentNode_.subNodeCount_ - 1

        # Fix newPeerNode & its sub-nodeTree nodeId's
        newPeerNode_.updateSubNodeTreeNodeIds()

        return newPeerNode_

    # Add new peerNodeObj (by value) relative to Node Specified by Id as new lastNode, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def addPeerNodeObjById(self, nodeId_, newPeerNode_, uniqueLevel_=0):
        thisNode = self
        startNode = thisNode
        
        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(newPeerNode_.uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Find the reference node
        thisParrentNode=""
        while(thisNode != ""):
            # Is this the node we are looking for?
            if(thisNode.nodeId_.lower() == nodeId_.lower()):
                thisParrentNode = thisNode.parrentNode_
                break

            # Get next node
            thisNode = thisNode.getNextNode(startNode)

        # Was the ref. node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "addPeerNodeObjById: Unable to find node with Id" + nodeId_            
            return ""
        
        # Assume the ref. node was found
        # Ensure the newPeerNode has been associated/linked to thisNodes parrentNode
        newPeerNode_.parrentNode_ = thisNode.parrentNode_ 
        # Ensure the newPeerNode has the specified uniqueness level
        newPeerNode_.uniqueLevel_ = uniqueLevel_        
        
        # Add the new peerNode
        thisNode.parrentNode_.subNodes_.append(newPeerNode_)

        # Update sub node count
        thisNode.parrentNode_.subNodeCount_ += 1
        # Ensure nodeIx is has lastNode ix so it can be fixed 
        newPeerNode_.nodeIx_ = thisNode.parrentNode_.subNodeCount_ - 1        

        # Fix newPeerNode & its sub-nodeTree nodeId's
        newPeerNode_.updateSubNodeTreeNodeIds()

        return newPeerNode_

    # Add new peerNodeObj (by value) relative to Node Specified by Name as new lastNode, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def addPeerNodeObjByName(self, name_, newPeerNode_, uniqueLevel_=0):
        thisNode = self
        startNode = thisNode
        
        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()            
            existingNode = thisRootNode.findNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Find the reference node
        thisParrentNode=""
        while(thisNode != ""):
            # Is this the node we are looking for?
            if(thisNode.name_.lower() == name_.lower()):
                thisParrentNode = thisNode.parrentNode_
                break

            # Get next node
            thisNode = thisNode.getNextNode(startNode)

        # Was the ref. node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "addPeerNodeObjByName: Unable to find node with name " + name_            
            return ""
        
        # Assume the ref. node was found
        # Ensure the newPeerNode has been associated/linked to thisNodes parrentNode
        newPeerNode_.parrentNode_ = thisNode.parrentNode_ 
        # Ensure the newPeerNode has the specified uniqueness level
        newPeerNode_.uniqueLevel_ = uniqueLevel_        
        
        # Add the new peerNode
        thisNode.parrentNode_.subNodes_.append(newPeerNode_)

        # Update sub node count
        thisNode.parrentNode_.subNodeCount_ += 1
        # Ensure nodeIx is has lastNode ix so it can be fixed 
        newPeerNode_.nodeIx_ = thisNode.parrentNode_.subNodeCount_ - 1        

        # Fix newPeerNode & its sub-nodeTree nodeId's
        newPeerNode_.updateSubNodeTreeNodeIds()

        return newPeerNode_


#------------------------ INSERT peerNode Handling ---------------------
    # Insert new peerNodeObj on same parrentNode/nodeChain as thisNode & relative to thisNode
    def insertPeerNodeObj(self, newPeerNode_, uniqueLevel_=0):
        thisNode = self
        
        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Ensure the newPeerNode has been associated/linked to thisNodes parrentNode
        newPeerNode_.parrentNode_ = thisNode.parrentNode_
        # Ensure the newPeerNode has the specified uniqueness level
        newPeerNode_.uniqueLevel_ = uniqueLevel_         
        
        # Insert the new peerNode before node at ix
        thisNode.parrentNode_.subNodes_.insert(thisNode.nodeIx_, newPeerNode_)

        # Update sub node count
        thisNode.parrentNode_.subNodeCount_ += 1
        # Ensure nodeIx is has lastNode ix so it can be fixed 
        newPeerNode_.nodeIx_ = thisNode.nodeIx_ - 1

        # Fix newPeerNode & its sub-nodeTree nodeId's
        newPeerNode_.updateSubNodeTreeNodeIds()

        return newPeerNode_

    # Insert new peerNodeObj (by value) relative to Node Specified by Id, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def insertPeerNodeObjById(self, nodeId_, newPeerNode_, uniqueLevel_=0):
        thisNode = self
        startNode = thisNode
        
        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Find the reference node
        thisParrentNode=""
        while(thisNode != ""):
            # Is this the node we are looking for?
            if(thisNode.nodeId_.lower() == nodeId_.lower()):
                thisParrentNode = thisNode.parrentNode_
                break

            # Get next node
            thisNode = thisNode.getNextNode(startNode)

        # Was the ref. node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "insertPeerNodeObjById: Unable to find node with Id" + nodeId_            
            return ""
        
        # Assume the ref. node was found
        # Ensure the newPeerNode has been associated/linked to thisNodes parrentNode
        newPeerNode_.parrentNode_ = thisNode.parrentNode_
        # Ensure the newPeerNode has the specified uniqueness level
        newPeerNode_.uniqueLevel_ = uniqueLevel_        
        
        # Insert the new peerNode before node at ix
        thisNode.parrentNode_.subNodes_.insert(thisNode.nodeIx_, newPeerNode_)

        # Update sub node count
        thisNode.parrentNode_.subNodeCount_ += 1
        # Ensure nodeIx is has lastNode ix so it can be fixed 
        newPeerNode_.nodeIx_ = thisNode.nodeIx_ - 1

        # Fix newPeerNode & its sub-nodeTree nodeId's
        newPeerNode_.updateSubNodeTreeNodeIds()

        return newPeerNode_    

    # Insert new peerNodeObj (by value) relative to Node Specified by name, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def insertPeerNodeObjByName(self, name_, newPeerNode_, uniqueLevel_=0):
        thisNode = self
        startNode = thisNode

        # Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => rootNodes do not have peerNodes            
            thisNode.error_ = "insertPeerNodeObjByName: rootNodes does not have peerNodes!!"
            return ""
        
        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()            
            existingNode = thisRootNode.findNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Find the reference node
        thisParrentNode=""
        while(thisNode != ""):
            # Is this the node we are looking for?
            if(thisNode.name_.lower() == name_.lower()):
                thisParrentNode = thisNode.parrentNode_
                break

            # Get next node
            thisNode = thisNode.getNextNode(startNode)

        # Was the ref. node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "insertPeerNodeObjByName: Unable to find node with name " + name_            
            return ""
        
        # Assume the ref. node was found
        # Ensure the newPeerNode has been associated/linked to thisNodes parrentNode
        newPeerNode_.parrentNode_ = thisNode.parrentNode_
        # Ensure the newPeerNode has the specified uniqueness level
        newPeerNode_.uniqueLevel_ = uniqueLevel_         
        
        # Add the new peerNode
        thisNode.parrentNode_.subNodes_.insert(thisNode.nodeIx_, newPeerNode_)

        # Update sub node count
        thisNode.parrentNode_.subNodeCount_ += 1
        # Ensure nodeIx is has lastNode ix so it can be fixed 
        newPeerNode_.nodeIx_ = thisNode.nodeIx_ - 1        

        # Fix newPeerNode & its sub-nodeTree nodeId's
        newPeerNode_.updateSubNodeTreeNodeIds()

        return newPeerNode_

    # Insert new peerNodeObj (by value) on same parrentNode/nodeChain as thisNode & relative to nodeIx
    # use rootNode if you are unsure where the node is located
    def insertPeerNodeObjByIx(self, nodeIx_, newPeerNode_, uniqueLevel_=0):
        thisNode = self
        
        # Is this a rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => rootNodes does not have peerNodes
            thisNode.error_ = "insertPeerNodeObjByIx: rootNodes does not have peerNodes!!"            
            return ""

        # Is nodeIx valid?
        if(nodeIx_ > thisNode.parrentNode_.subNodeCount_ - 1):
            # YES => Invalid nodeIx
            thisNode.error_ = "insertPeerNodeObjByIx: Unable to find a node with ix " + str(nodeIx_)            
            return ""

        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(newPeerNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Get the referece Node
        thisParrentNode = thisNode.parrentNode_
        thisNode = thisParrentNode.subNodes_[nodeIx_]
        
        # Assume the ref. node was found
        # Ensure the newPeerNode has been associated/linked to thisNodes parrentNode
        newPeerNode_.parrentNode_ = thisNode.parrentNode_
        # Ensure the newPeerNode has the specified uniqueness level
        newPeerNode_.uniqueLevel_ = uniqueLevel_         
        
        # Add the new peerNode
        thisNode.parrentNode_.subNodes_.insert(thisNode.nodeIx_, newPeerNode_)

        # Update sub node count
        thisNode.parrentNode_.subNodeCount_ += 1
        # Ensure nodeIx has insertedNode ix so it can be fixed 
        newPeerNode_.nodeIx_ = thisNode.nodeIx_ - 1        

        # Fix newPeerNode & its sub-nodeTree nodeId's
        newPeerNode_.updateSubNodeTreeNodeIds()

        return newPeerNode_

# -----------  ADD subNode Handling -------
    # Add new subNodeObj to thisNode as new last-subNode
    def addSubNodeObj(self, newSubNode_, uniqueLevel_=0):
        thisNode = self
        
        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Ensure the newSubNode has been associated/linked to thisNodes, has thisNode as parrentNode
        newSubNode_.parrentNode_ = thisNode
        # Ensure the newSubNode has the specified uniqueness level
        newSubNode_.uniqueLevel_ = uniqueLevel_
        
        # Add the new subNode
        thisNode.subNodes_.append(newSubNode_)

        # Update sub node count
        thisNode.subNodeCount_ += 1
        # Ensure nodeIx is has lastNode ix so it can be fixed 
        newSubNode_.nodeIx_ = thisNode.subNodeCount_ - 1        

        # Fix newSubNode & its sub-nodeTree nodeId's
        newSubNode_.updateSubNodeTreeNodeIds()

        return newSubNode_

    # Add new subNodeObj (by value) to Node Specified by Id as new lastNode, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def addSubNodeObjById(self, nodeId_, newSubNode_, uniqueLevel_=0):
        thisNode = self
        startNode = thisNode
        
        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Find the reference node
        thisParrentNode=""
        while(thisNode != ""):
            # Is this the node we are looking for?
            if(thisNode.nodeId_.lower() == nodeId_.lower()):
                thisParrentNode = thisNode.parrentNode_
                break

            # Get next node
            thisNode = thisNode.getNextNode(startNode)

        # Was the ref. node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "addSubNodeObjById: Unable to find node with Id " + nodeId_            
            return ""
        
        # Assume the ref. node was found
        # Ensure the newSubNode has been associated/linked to thisNodes, has thisNode as parrentNode
        newSubNode_.parrentNode_ = thisNode
        # Ensure the newSubNode has the specified uniqueness level
        newSubNode_.uniqueLevel_ = uniqueLevel_        
        
        # Add the new subNode
        thisNode.subNodes_.append(newSubNode_)

        # Update sub node count
        thisNode.subNodeCount_ += 1
        # Ensure nodeIx is has lastNode ix so it can be fixed 
        newSubNode_.nodeIx_ = thisNode.subNodeCount_ - 1        

        # Fix newSubNode & its sub-nodeTree nodeId's
        newSubNode_.updateSubNodeTreeNodeIds()

        return newSubNode_

    # Add new subNodeObj (by value) to Node Specified by Name as new lastNode, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def addSubNodeObjByName(self, name_, newSubNode_, uniqueLevel_=0):
        thisNode = self
        startNode = thisNode
        
        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()            
            existingNode = thisRootNode.findNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Find the reference node
        thisParrentNode=""
        while(thisNode != ""):
            # Is this the node we are looking for?
            if(thisNode.name_.lower() == name_.lower()):
                thisParrentNode = thisNode.parrentNode_
                break

            # Get next node
            thisNode = thisNode.getNextNode(startNode)

        # Was the ref. node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "addSubNodeObjByName: Unable to find node with name " + name_            
            return ""
        
        # Assume the ref. node was found
        # Ensure the newSubNode has been associated/linked to thisNodes, has thisNode as parentNode
        newSubNode_.parrentNode_ = thisNode
        # Ensure the newSubNode has the specified uniqueness level
        newSubNode_.uniqueLevel_ = uniqueLevel_        
        
        # Add the new subNode
        thisNode.subNodes_.append(newSubNode_)

        # Update sub node count
        thisNode.subNodeCount_ += 1
        # Ensure nodeIx is has lastNode ix so it can be fixed 
        newSubNode_.nodeIx_ = thisNode.subNodeCount_ - 1        

        # Fix newPeerNode & its sub-nodeTree nodeId's
        newSubNode_.updateSubNodeTreeNodeIds()

        return newSubNode_

#------------------------ INSERT subNode Handling ---------------------
    # Insert new subNodeObj on thisNodes & relative to nodeIx
    def insertSubNodeObj(self, nodeIx_, newSubNode_, uniqueLevel_=0):
        thisNode = self
        
        # Is nodeIx valid?
        if(nodeIx_ > thisNode.subNodeCount_ - 1):
            # NO => Invalid nodeIx            
            thisNode.error_ = "insertSubNodeObj: Unable to find node with ix " + str(nodeIx_)            
            return ""

        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Ensure the newSubNode has been associated/linked to thisNodes, has thisNode as parrentNode
        newSubNode_.parrentNode_ = thisNode
        # Ensure the newSubNode has the specified uniqueness level
        newSubNode_.uniqueLevel_ = uniqueLevel_        
        
        # insert the new subNode
        thisNode.subNodes_.insert(nodeIx_, newSubNode_)

        # Update sub node count
        thisNode.subNodeCount_ += 1
        # Ensure nodeIx is has lastNode ix so it can be fixed 
        newSubNode_.nodeIx_ = thisNode.subNodeCount_ - 1        

        # Fix newPeerNode & its sub-nodeTree nodeId's
        newSubNode_.updateSubNodeTreeNodeIds()

        return newSubNode_

    # Insert new subNodeObj (by value) on Node Specified by Id & relative to nodeIx, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def insertSubNodeObjById(self, nodeId_, nodeIx_, newSubNode_, uniqueLevel_=0):
        thisNode = self
        startNode = thisNode
        
        # Is nodeIx valid?
        if(nodeIx_ > thisNode.subNodeCount_ - 1):
            # NO => Invalid nodeIx
            thisNode.error_ = "insertSubNodeObjById: Unable to find subNode with Ix " + str(nodeIx_)            
            return ""

        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Find the reference node
        thisParrentNode=""
        while(thisNode != ""):
            # Is this the node we are looking for?
            if(thisNode.nodeId_.lower() == nodeId_.lower()):
                thisParrentNode = thisNode
                break

            # Get next node
            thisNode = thisNode.getNextNode(startNode)

        # Was the ref. node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "insertSubNodeObjById: Unable to find node with Id " + nodeId_            
            return ""
        
        # Assume the ref. node was found
        # Ensure the newSubNode has been associated/linked to thisNode, has thisNode as parrentNode
        newSubNode_.parrentNode_ = thisNode
        # Ensure the newSubNode has the specified uniqueness level
        newSubNode_.uniqueLevel_ = uniqueLevel_        
        
        # Insert the new subNode
        thisNode.subNodes_.insert(nodeIx_, newSubNode_)

        # Update sub node count
        thisNode.subNodeCount_ += 1
        # Ensure nodeIx is has lastNode ix so it can be fixed 
        newSubNode_.nodeIx_ = thisNode.subNodeCount_ - 1        

        # Fix newSubNode & its sub-nodeTree nodeId's
        newSubNode_.updateSubNodeTreeNodeIds()

        return newSubNode_    

    # Insert new subNodeObj (by value) on node specified by name & relative to nodeIx, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def insertSubNodeObjByName(self, name_, nodeIx_, newSubNode_, uniqueLevel_=0):
        thisNode = self
        startNode = thisNode
        
        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()            
            existingNode = thisRootNode.findNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Find the reference node
        thisParrentNode=""
        while(thisNode != ""):
            # Is this the node we are looking for?
            if(thisNode.name_.lower() == name_.lower()):
                thisParrentNode = thisNode.parrentNode_
                break

            # Get next node
            thisNode = thisNode.getNextNode(startNode)

        # Was the ref. node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "insertSubNodeObjByName: Unable to find node with name " + name_            
            return ""
        
        # Get ref. subNode

        # is NodeIx valid?
        if(nodeIx_ > thisNode.subNodeCount_ - 1):
            # NO => Invalid nodeIx
            thisNode.error_ = "insertSubNodeObjByName: Unable to find subNode with ix " + str(nodeIx_)            
            return ""        

        # Assume the ref. node was found
        # Ensure the newSubNode has been associated/linked to thisNodes, has thisNode as parrentNode
        newSubNode_.parrentNode_ = thisNode
        # Ensure the newSubNode has the specified uniqueness level
        newSubNode_.uniqueLevel_ = uniqueLevel_    
        
        # Insert the new subNode
        thisNode.subNodes_.insert(nodeIx_, newSubNode_)

        # Update sub node count
        thisNode.subNodeCount_ += 1
        # Ensure nodeIx is has lastNode ix so it can be fixed 
        newSubNode_.nodeIx_ = thisNode.subNodeCount_ - 1        

        # Fix newSubNode & its sub-nodeTree nodeId's
        newSubNode_.updateSubNodeTreeNodeIds()
        
        return newSubNode_

    # Insert new subNodeObj (by value) on thisNode & relative to nodeIx
    # use rootNode if you are unsure where the node is located
    def insertSubNodeObjByIx(self, nodeIx_, newSubNode_, uniqueLevel_=0):
        thisNode = self
        
        # Is nodeIx valid?
        if(nodeIx_ < 0)|(nodeIx_ > thisNode.subNodeCount_ - 1):
            # NO => Invalid nodeIx
            thisNode.error_ = "insertSubNodeObjByIx: Unable to find subNode with ix " + str(nodeIx_)            
            return ""

        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(newSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
                     
        # Assume the ref. node was found
        # Ensure the newSubNode has been associated/linked to thisNodes, has thisNode as parrentNode
        newSubNode_.parrentNode_ = thisNode
        # Ensure the newSubNode has the specified uniqueness level
        newSubNode_.uniqueLevel_ = uniqueLevel_         
        
        # Insert the new subNode
        thisNode.subNodes_.insert(nodeIx_, newSubNode_)

        # Update sub node count
        thisNode.subNodeCount_ += 1
        # Ensure nodeIx is has lastNode ix so it can be fixed 
        newSubNode_.nodeIx_ = thisNode.subNodeCount_ - 1        

        # Fix newPeerNode & its sub-nodeTree nodeId's
        newSubNode_.updateSubNodeTreeNodeIds()

        return newSubNode_        
#--------------------------       
# ------------------- Add Node Helper/Wrapper Methdos ------------------------------
# --------------------  Add Node Helper Methods -----------------
    # Add new peerNode (by value) relative to Node Specified by Id as new lastNode, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def addPeerNodeById(self, nodeId_, name_="", value_="", uniqueLevel_=0):
        thisNode = self
        # Create new node
        newPeerNode = analysisNodeTree(name_, value_, thisNode.parrentNode_, thisNode.nodeLevelSeparator_)

        # Add the new node as new lastNode on same node as thisNode
        thisNode = thisNode.addPeerNodeObj(newPeerNode, uniqueLevel_)

        return thisNode

    # Add new peerNode (by value) relative to Node Specified by Name as new lastNode, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def addPeerNodeByName(self, nodeName_, name_="", value_="", uniqueLevel_=0):
        thisNode = self

        # Create new node
        newPeerNode = analysisNodeTree(name_, value_, thisNode.parrentNode_, thisNode.nodeLevelSeparator_)

        # Add the new peerNode as new lastNode on same node as thisNode
        thisNode = thisNode.addPeerNodeObj(newPeerNode, uniqueLevel_)

        return thisNode

#------------------------------------------------------
#-------------- add peerNode Helper Methods --------
    # Add new peerNode (by value) on same parrentNode/nodeChain as thisNode, as new lastNode
    def addPeerNode(self, name_="", value_="", uniqueLevel_=0):
        thisNode = self

        # Create new node
        newPeerNode = analysisNodeTree(name_, value_, thisNode.parrentNode_, thisNode.nodeLevelSeparator_)

        # Add the new node as new lastNode 
        thisNode = thisNode.addPeerNodeObj(newPeerNode, uniqueLevel_)

        return thisNode

    # Add copy of new peerNode (by object) on same parrentNode/nodeChain as thisNode as new lastNode
    def addPeerNodeObjCopy(self, newNode_, uniqueLevel_=0):
        thisNode = self

        # Create new node as copy of otherNode
        newNode = newNode_.copyNode()

        # Add the new node as new lastNode
        thisNode = thisNode.addPeerNodeObj(newNode, uniqueLevel_)

        return thisNode

#-------- add subNode Helper Methods ------------
    # Add new subNode (by value) to thisNode as new last-subNode
    def addSubNode(self, name_="", value_="", uniqueLevel_=0):
        thisNode = self
        
        # Create new node
        newSubNode = analysisNodeTree(name_, value_, thisNode, thisNode.nodeLevelSeparator_)

        # Add the new subNode to thisNode
        thisNode = thisNode.addSubNodeObj(newSubNode, uniqueLevel_)

        return thisNode    
            
    # Add copy of new subNodeObj (by object) to thisNode as new lastNode
    def addSubNodeObjCopy(self, newSubNode_, uniqueLevel_=0):
        thisNode = self
    
        # Create copy of otherNode
        newSubNode = newSubNode_.copyNode()

        # Add the new subNode to thisNode
        thisNode = thisNode.addSubNodeObj(newSubNode, uniqueLevel_)

        return thisNode

#----------------------

#----------- Insert Helper/Wrapper Methods -----------------------------

#----------- Insert node Helper methods -----------------
# Build to search entire sub-nodeTree of thisNode
    # Add new subNode (by value) to Node Specified by Id as new lastNode, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def addSubNodeById(self, nodeId_, name_="", value_="", uniqueLevel_=0):
        thisNode = self
        
        # Create new subNode "Dont worry about parrentNode it is fixed by the core add subnode method"
        newSubNode = analysisNodeTree(name_, value_, thisNode.parrentNode_, thisNode.nodeLevelSeparator_)

        # Add the new subNode to node specified by id
        thisNode = thisNode.addSubNodeObjById(nodeId_, newSubNode, uniqueLevel_)

        return thisNode

    # Add new subNode (by value) to Node Specified by Name as new lastNode, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def addSubNodeByName(self, nodeName_, name_="", value_="", uniqueLevel_=0):
        thisNode = self

        # Create new subNode
        newSubNode = analysisNodeTree(name_, value_, thisNode.parrentNode_, thisNode.nodeLevelSeparator_)

        # Add the new subNode as new lastNode for node specified by name
        thisNode = thisNode.addSubNodeObjByName(nodeName_, newSubNode, uniqueLevel_)

        return thisNode

# -------------- Insert peerNode Helper methods ----------------
# Build to search only peerNodes, parrentNode->subNodes/nodeChain

    # Insert new peerNode (by value) relative to Node Specified by Id, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def insertPeerNodeById(self, nodeId_, name_="", value_="", uniqueLevel_=0):
        thisNode = self

        # Create new node
        newPeerNode = analysisNodeTree(name_, value_, thisNode.parrentNode_, thisNode.nodeLevelSeparator_)

        # Insert the new peerNode rel to thisNode
        thisNode = thisNode.insertPeerNodeObjById(nodeId_, newPeerNode, uniqueLevel_)

        return thisNode

    # Insert new peerNode (by value) relative to Node Specified by Name, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def insertPeerNodeByName(self, nodeName_, name_="", value_="", uniqueLevel_=0):
        thisNode = self

        # Create new node
        newPeerNode = analysisNodeTree(name_, value_, thisNode.parrentNode_, thisNode.nodeLevelSeparator_)

        # Insert the new node rel to node specified by name
        thisNode = thisNode.insertPeerNodeObjByName(nodeName_, newPeerNode, uniqueLevel_)

        return thisNode

    # Insert new peerNode (by value) on same parrentNode/nodeChain as thisNode & relative to NodeIx, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def insertPeerNodeByIx(self, nodeIx_, name_="", value_="", uniqueLevel_=0):
        thisNode = self

        # Create new node
        newPeerNode = analysisNodeTree(name_, value_, thisNode.parrentNode_, thisNode.nodeLevelSeparator_)

        # Insert the new peerNode rel to thisNode
        thisNode = thisNode.insertPeerNodeObjByIx(nodeIx_, newPeerNode, uniqueLevel_)

        return thisNode        

    # Insert new peerNode (by value) on same parrentNode/nodeChain as thisNode & relative to thisNode
    def insertPeerNode(self, name_="", value_="", uniqueLevel_=0):
        thisNode = self

        # Create new node
        newPeerNode = analysisNodeTree(name_, value_, thisNode.parrentNode_, thisNode.nodeLevelSeparator_)

        # Insert the new node rel to thisNode
        thisNode = thisNode.insertPeerNodeObj(newPeerNode, uniqueLevel_)

        return thisNode

    # Insert copy of new peerNode (by object) on same parrentNode/nodeChain as thisNode & relative to thisNode
    def insertPeerNodeObjCopy(self, newNode_, uniqueLevel_=0):
        thisNode = self

        # Create new node as copy of otherNode
        newNode = newNode_.copyNode()

        # Insert the new node rel to thisNode
        thisNode = thisNode.insertPeerNodeObj(newNode, uniqueLevel_)

        return thisNode

#-------------- Insert subNode Helper methods ---------------------
# Build to search only thisNodes->subNodes/nodeChain     
    # Insert new subNode (by value) on Node Specified by Id & relative to nodeIx, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def insertSubNodeById(self, nodeId_, nodeIx_, name_="", value_="", uniqueLevel_=0):
        thisNode = self
        
        # Create new subNode "Dont worry about parrentNode it is fixed by the core add subnode method"
        newSubNode = analysisNodeTree(name_, value_, thisNode.parrentNode_, thisNode.nodeLevelSeparator_)

        # Insert the new subNode to node specified by id at relative node ix
        thisNode = thisNode.insertSubNodeObjById(nodeId_, nodeIx_, newSubNode, uniqueLevel_)

        return thisNode

    # Insert new subNode (by value) on Node Specified by Name & relative to nodeIx, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def insertSubNodeByName(self, nodeName_, nodeIx_, name_="", value_="", uniqueLevel_=0):
        thisNode = self

        # Create new subNode
        newSubNode = analysisNodeTree(name_, value_, thisNode.parrentNode_, thisNode.nodeLevelSeparator_)

        # Insert the new subNode on node specified by name at relative nodeIx
        thisNode = thisNode.insertSubNodeObjByName(nodeName_, nodeIx_, newSubNode, uniqueLevel_)

        return thisNode

    # Insert new subNode (by value) on thisNode & relative to nodeIx, Search from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure where the node is located
    def insertSubNodeByIx(self, nodeIx_, name_="", value_="", uniqueLevel_=0):
        thisNode = self
        
        # Create new subNode "Dont worry about parrentNode it is fixed by the core add subnode method"
        newSubNode = analysisNodeTree(name_, value_, thisNode, thisNode.nodeLevelSeparator_)

        # Insert the new subNode on thisNode & relative to subNode specified by Ix
        thisNode = thisNode.insertSubNodeObjByIx(nodeIx_, newSubNode, uniqueLevel_)

        return thisNode        

    # Insert new subNode (by value) on thisNode & relative to nodeIx
    def insertSubNode(self, nodeIx_, name_="", value_="", uniqueLevel_=0):
        thisNode = self
        
        # Create new node
        newSubNode = analysisNodeTree(name_, value_, thisNode, thisNode.nodeLevelSeparator_)

        # Insert the new node rel to node ix
        thisNode = thisNode.insertSubNodeObjByIx(nodeIx_, newSubNode, uniqueLevel_)

        return thisNode

    # Insert copy of new subNodeObj (by object) to thisNode & relative to nodeIx
    def insertSubNodeObjCopy(self, nodeIx_, newSubNode_, uniqueLevel_=0):
        thisNode = self

        # Create copy of otherNode
        newSubNode = newSubNode_.copyNode()

        # Insert the new node rel to nodeIx
        thisNode = thisNode.insertSubNodeObj(nodeIx_, newSubNode, uniqueLevel_)

        return thisNode
        
#-------------------------------------------------

#----------- REPLACE node handling -----------------------

# TODO: Implement core functions like add & insert nodes and used wrapper/helper functions that calls them!! (OK)

    # replace node specified by Id with otherNode, Search from thisNode to end of its sub-nodeTree
    def replaceNodeObjById(self, nodeId_, otherNode_, uniqueLevel_=0):
        thisNode = self 
        startNode = thisNode

        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self        
        
        thisParrentNode = ""
        while(thisNode != ""):
            # is this the node we are looking for?
            if(thisNode.nodeId_.lower() == nodeId_.lower()):
                # Node located
                thisParrentNode = thisNode.parrentNode_
                break

            # Get next node
            thisNode = thisNode.getNextNode(startNode)
        
        # Was the node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "replaceNodeObjById: Unable to find node with Id " + nodeId_            
            return ""
                
        # Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => rootNodes cannot be replaced
            self.error_ = "replaceNodeObjById: rootNodes cannot be replaced!!"            
            return ""

        # Assume the node was found
        ix = thisNode.nodeIx_
        # Fix parrentNode association/Link to thisNode
        otherNode_.parrentNode_ = thisParrentNode
        # Ensure the otherNode has the specified uniqueness level
        otherNode_.uniqueLevel_ = uniqueLevel_        
        # Replace the node
        thisParrentNode.subNodes_[ix] = otherNode_
        # Fix nodeIds for the swapped node and its sub-nodeTree
        thisParrentNode.subNodes_[ix].updateSubNodeTreeNodeIds()

        return thisParrentNode.subNodes_[ix]

    # replace node specified by name with otherNode, relative search from thisNode to end of its sub-nodeTree
    def replaceNodeObjByName(self, name_, otherNode_, uniqueLevel_=0):
        thisNode = self 
        startNode = thisNode

        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self        

        thisParrentNode = ""
        while(thisNode != ""):
            # is this the node we are looking for?
            if(thisNode.name_.lower() == name_.lower()):
                # Node located
                thisParrentNode = thisNode.parrentNode_
                break

            # Get next node
            thisNode = thisNode.getNextNode(startNode)
                
        # Was ref. Node found?
        if(thisParrentNode == ""):
            # NO 
            self.error_ = "replaceNodeObjByName: Unable to find node with name " + name_            
            return ""

        # Assume the node was found
        ix = thisNode.nodeIx_
        # Fix parrentNode association/Link to thisNode
        otherNode_.parrentNode_ = thisParrentNode
        # Ensure the otherNode has the specified uniqueness level
        otherNode_.uniqueLevel_ = uniqueLevel_        
        # Replace the node
        thisParrentNode.subNodes_[ix] = otherNode_
        # Fix nodeIds for the swapped node and its sub-nodeTree
        thisParrentNode.subNodes_[ix].updateSubNodeTreeNodeIds()

        return thisParrentNode.subNodes_[ix]        

#-------- replace peerNode handling -----------
    # replace thisNode with the otherNode
    def replaceNodeObj(self, otherNode_, uniqueLevel_=0):
        thisNode = self        
        thisParrentNode = thisNode.parrentNode_
                
        # Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => rootNodes cannot be replaced
            thisNode.error_ = "replaceNodeObj: rootNodes cannot be replaced!!"
            return ""

        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Get thisNode ix
        ix = thisNode.nodeIx_
        # Fix parrentNode association/Link to thisNodes parrentNode
        otherNode_.parrentNode_ = thisParrentNode
        # Ensure the otherNode has the specified uniqueness level
        otherNode_.uniqueLevel_ = uniqueLevel_        
        # Replace the node
        thisParrentNode.subNodes_[ix] = otherNode_
        # Fix nodeIds for the swapped node and its sub-nodeTree
        thisParrentNode.subNodes_[ix].updateSubNodeTreeNodeIds()

        return thisParrentNode.subNodes_[ix]

    # Replace thisNode with a copy of otherNode_
    def replaceNodeObjCopy(self, otherNode_, uniqueLevel_=0):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_ 
        
        # Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => rootNodes cannot be replaced
            thisNode.error_ = "replaceNodeObjCopy: rootNodes cannot be replaced!!"            
            return ""

        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Create Copy of otherNode
        otherNode = otherNode_.copyNode()

        # Get thisNodes ix
        ix = thisNode.nodeIx_
                
        # Fix thisNodes association/linking to parrentNode
        otherNode.parrentNode_ = thisParrentNode
        # Ensure the otherNode has the specified uniqueness level
        otherNode.uniqueLevel_ = uniqueLevel_        
        # Replace subNode
        thisParrentNode.subNodes_[ix] = otherNode
        # Fix subNode & its sub-nodeTree nodeIds
        thisParrentNode.subNodes[ix].updateSubNodeTreeNodeIds()

        return thisParrentNode.subNodes_[ix]       

#-------- replace subNode handling ------------
    # replace thisNodes sub-nodeTree with the otherNodes sub-nodeTree "replace nodeChain"
    def replaceSubNodeTreeObj(self, otherSubNode_):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_
        
        # Get thisNodes ix
        ix = thisNode.nodeIx_
                
        # Replace sub-nodeTree
        thisParrentNode.subNodes_[ix].subNodes_ = otherSubNode_.subNodes_
        thisParrentNode.subNodes_[ix].subNodeCount_ = otherSubNode_.subNodeCount_

        # Fix thisNodes sub-nodeTree association/linking to parrentNode
        for node in thisParrentNode.subNodes_[ix].subNodes_:
            # fix subNodes association/link to parrentNode
            node.parrentNode_ = thisNode

        # Fix subNode & its sub-nodeTree nodeIds
        thisParrentNode.subNodes_[ix].updateSubNodeTreeNodeIds()

        return thisParrentNode.subNodes_[ix]
        
    # replace thisNodes sub-nodeTree with copy of otherNodes sub-nodeTree "replace nodeChain"
    def replaceSubNodeTreeObjCopy(self, otherSubNode_):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_
        
        # Create Copy of otherNode
        otherSubNode = otherSubNode_.copyNode()

#----------------------------------------
#------------------------------------------------

        # Get thisNodes nodeIx
        ix = thisNode.nodeIx_
                
        # Assume the node was not found
        # Replace sub-nodeTree
        thisParrentNode.subNodes_[ix].subNodes_ = otherSubNode.subNodes_
        thisParrentNode.subNodes_[ix].subNodeCount_ = otherSubNode.subNodeCount_

        # Fix thisNodes sub-nodeTree association/linking to parrentNode
        for node in thisParrentNode.subNodes_[ix].subNodes_:
            # fix subNodes association/link to parrentNode
            node.parrentNode_ = thisNode

        # Fix subNode & its sub-nodeTree nodeIds
        thisParrentNode.subNodes[ix].updateSubNodeTreeNodeIds()

        return thisParrentNode.subNodes_[ix]

    # replace sub-nodeChain of node specified by Id with otherNode, Search from thisNode to end of its sub-nodeTree
    def replaceSubNodeTreeObjById(self, nodeId_, otherNode_, uniqueLevel_=0):
        thisNode = self 
        startNode = thisNode

        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self        
        
        thisParrentNode = ""
        while(thisNode != ""):
            # is this the node we are looking for?
            if(thisNode.nodeId_.lower() == nodeId_.lower()):
                # Node located
                thisParrentNode = thisNode.parrentNode_
                break

            # Get next node
            thisNode = thisNode.getNextNode(startNode)
        
        # Was the node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "replaceSubNodeTreeObjById: Unable to find node with Id " + nodeId_            
            return ""
                
        # Assume the node was found
        ix = thisNode.nodeIx_
        # Fix parrentNode association/Link to thisNode
        otherNode_.parrentNode_ = thisParrentNode
        # Ensure the otherNode has the specified uniqueness level
        otherNode_.uniqueLevel_ = uniqueLevel_        
        # Replace the node
        thisParrentNode.subNodes_[ix] = otherNode_.subNode_
        thisParrentNode.subNodes_[ix].subNodeCount_ = otherNode_.subNodeCount_
        # Fix nodeIds for the swapped node and its sub-nodeTree
        thisParrentNode.subNodes_[ix].updateSubNodeTreeNodeIds()

        return thisParrentNode.subNodes_[ix]

    # replace node specified by name with otherNode, relative search from thisNode to end of its sub-nodeTree
    def replaceSubNodeTreeObjByName(self, name_, otherNode_, uniqueLevel_=0):
        thisNode = self 
        startNode = thisNode

        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(otherNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self        
        
        thisParrentNode = ""
        while(thisNode != ""):
            # is this the node we are looking for?
            if(thisNode.name_.lower() == name_.lower()):
                # Node located
                thisParrentNode = thisNode.parrentNode_
                break

            # Get next node
            thisNode = thisNode.getNextNode(startNode)
        
        # Was the node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "replaceSubNodeTreeObjByName: Unable to find node with name " + name_            
            return ""
                
        # Assume the node was found
        ix = thisNode.nodeIx_
        # Fix parrentNode association/Link to thisNode
        otherNode_.parrentNode_ = thisParrentNode
        # Ensure the otherNode has the specified uniqueness level
        otherNode_.uniqueLevel_ = uniqueLevel_        
        # Replace the node
        thisParrentNode.subNodes_[ix] = otherNode_.subNodes_
        thisParrentNode.subNodes_[ix].subNodeCount_ = otherNode_.subNodeCount_
        # Fix nodeIds for the swapped node and its sub-nodeTree
        thisParrentNode.subNodes_[ix].updateSubNodeTreeNodeIds()

        return thisParrentNode.subNodes_[ix]            

    # replace thisNodes sub-NodeTree specified by nodeIx with the otherNode, Search in thisNodes subNodes
    def replaceSubNodeObj(self, nodeIx_, otherSubNode_, uniqueLevel_=0):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_
        
        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Is nodeIx valid?
        if(nodeIx_ < 0)|(nodeIx_ > thisNode.subNodeCount_ - 1): # Remember binary math!!
            # NO => Invalid nodeix
            thisNode.error_ = "replaceSubNodeObj: Unable to find node with Ix " + str(nodeIx_)
            return ""

        thisSubNode = thisNode.subNodes_[nodeIx_]

        # fix/Ensure the otherSubNode_ is associated/linked to thisNodes Parrent before the replace
        otherSubNode_.parrentNode_ = thisParrentNode
        # Ensure the otherSubNode has the specified uniqueness level
        otherSubNode_.uniqueLevel_ = uniqueLevel_

        # Replacse thisSubNode with otherSubNode
        thisNode.subNodes_[nodeIx_] = otherSubNode_

        # Fix thisSubNodes sub-nodeTree association/linking to parrentNode
        for node in thisNode.subNodes_[nodeIx_].subNodes_:
            # fix subNodes association/link to parrentNode
            node.parrentNode_ = thisSubNode
                
        # Fix thisSubNode & its sub-nodeTree nodeIds
        thisNode.subNodes_[nodeIx_].updateSubNodeTreeNodeIds()

        return thisNode.subNodes_[nodeIx_]

    # replace thisNodes subNode specified by nodeId with the otherNode, Search in thisNode subNodes
    def replaceSubNodeObjById(self, nodeId_, otherSubNode_, uniqueLevel_=0):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_
        
        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Find subNode with specified nodeId
        thisParrentNode = ""
        ix = 0
        for node in thisNode.subNodes_:
            # is This the node we are looking for?
            if(node.nodeId_.lower() == nodeId_.lower()):
                thisParrentNode = thisNode
                break

        # was the node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "replaceSubNodeObjById: Unable to find node with Id " + nodeId_            
            return ""
        
        # Get nodeIx
        ix = node.nodeIx_
        thisSubNode = thisNode.subNodes_[ix]

        # fix/Ensure the otherSubNode_ is associated/linked to thisNodes Parrent before the replace
        otherSubNode_.parrentNode_ = thisParrentNode
        # Ensure the otherSubNode has the specified uniqueness level
        otherSubNode_.uniqueLevel_ = uniqueLevel_        

        # Replacse thisSubNode with otherSubNode
        thisNode.subNodes_[ix] = otherSubNode_

        # Fix thisSubNodes sub-nodeTree association/linking to parrentNode
        for node in thisNode.subNodes_[ix].subNodes_:
            # fix subNodes association/link to parrentNode
            node.parrentNode_ = thisSubNode
                
        # Fix thisSubNode & its sub-nodeTree nodeIds
        thisNode.subNodes_[ix].updateSubNodeTreeNodeIds()

        return thisNode.subNodes_[ix]

    # replace thisNodes subNode specified by name with the otherNode, Search in thisNode subNodes
    def replaceSubNodeObjByName(self, name_, otherSubNode_, uniqueLevel_=0):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_
        
        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        # Find subNode with specified nodeId
        thisParrentNode = ""
        ix = 0
        for node in thisNode.subNodes_:
            # is This the node we are looking for?
            if(node.name_.lower() == name_.lower()):
                thisParrentNode = thisNode
                break

        # was the node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "replaceSubNodeObjByName: Unable to find node with name " + name_            
            return ""
        
        # Get nodeIx
        ix = node.nodeIx_
        thisSubNode = thisNode.subNodes_[ix]

        # fix/Ensure the otherSubNode_ is associated/linked to thisNodes Parrent before the replace
        otherSubNode_.parrentNode_ = thisParrentNode
        # Ensure the otherSubNode has the specified uniqueness level
        otherSubNode_.uniqueLevel_ = uniqueLevel_        

        # Replacse thisSubNode with otherSubNode
        thisNode.subNodes_[ix] = otherSubNode_        

        # Fix thisSubNodes sub-nodeTree association/linking to parrentNode
        for node in thisNode.subNodes_[ix].subNodes_:
            # fix subNodes association/link to parrentNode
            node.parrentNode_ = thisSubNode
                
        # Fix thisSubNode & its sub-nodeTree nodeIds
        thisNode.subNodes_[ix].updateSubNodeTreeNodeIds()

        return thisNode.subNodes_[ix]

    # replace thisNodes subNode specified by nodeIx with the otherNode, Search in thisNodes subNodes
    def replaceSubNodeObjByIx(self, nodeIx_, otherSubNode_, uniqueLevel_=0):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        # Is nodeIx valid?
        if(nodeIx_ < 0)|(nodeIx_ > thisNode.subNodeCount_ - 1): # Remember binary math!!
            # NO => Invalid nodeix
            thisNode.error_ = "replaceSubNodeObjByIx: Unable to find node with Ix " + str(nodeIx_)            
            return ""        
        
        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self

        thisSubNode = thisNode.subNodes_[nodeIx_]

        # fix/Ensure the otherSubNode_ is associated/linked to thisNodes Parrent before the replace
        otherSubNode_.parrentNode_ = thisParrentNode
        # Ensure the otherSubNode has the specified uniqueness level
        otherSubNode_.uniqueLevel_ = uniqueLevel_        

        # Replace thisSubNode with otherSubNode
        thisNode.subNodes_[nodeIx_] = otherSubNode_

        # Fix thisSubNodes sub-nodeTree association/linking to parrentNode
        for node in thisNode.subNodes_[nodeIx_].subNodes_:
            # fix subNodes association/link to parrentNode
            node.parrentNode_ = thisSubNode
                
        # Fix thisSubNode & its sub-nodeTree nodeIds
        thisNode.subNodes_[nodeIx_].updateSubNodeTreeNodeIds()

        return thisNode.subNodes_[nodeIx_]                

    # Replace thisNodes subNode specified by nodeIx with copy of otherNode
    def replaceSubNodeObjCopy(self, nodeIx_, otherSubNode_, uniqueLevel_=0):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        # Is nodeIx valid?
        if(nodeIx_ < 0)|(nodeIx_ > thisNode.subNodeCount_ - 1): # Remember binary math!!
            # NO => Invalid nodeix
            thisNode.error_ = "replaceSubNodeObjCopy: Unable to find node with Ix " + str(nodeIx_)            
            return ""

        # Is node->value unique?
        # Is it nodeTree Uniqueness?
        if(uniqueLevel_ == 1):
            # Does this node allready exist?
            thisRootNode = thisNode.getRootNode()
            existingNode = thisRootNode.findNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exit just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it peerNode Uniqueness?
        if(uniqueLevel_ == 2):
            # Does this node allready exist as a peerNode?
            existingNode = thisNode.findPeerNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update frequency "match count"
                existingNode.freq_ += 1
                return self
        # Is it subNode Uniqueness?
        if(uniqueLevel_ == 3):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findSubNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self
        # Is it sub-nodeTree Uniqueness
        if(uniqueLevel_ == 4):
            # Does this node allready exist as a subNode?
            existingNode = thisNode.findNodeByValue(otherSubNode_.value_)
            if(existingNode != ""):
                # Node exist just update freq "match count"
                existingNode.freq_ += 1
                return self        
        
        # Create copy of otherSubNode
        otherSubNode = otherSubNode_.copyNode()
        thisSubNode = thisNode.subNodes_[nodeIx_]

        # fix/Ensure the otherSubNode_ is associated/linked to thisNodes Parrent before the replace
        otherSubNode.parrentNode_ = thisParrentNode
        # Ensure the otherSubNode has the specified uniqueness level
        otherSubNode_.uniqueLevel_ = uniqueLevel_        

        # Replacse thisSubNode with otherSubNode
        thisNode.subNodes_[nodeIx_] = otherSubNode

        # Fix thisSubNodes sub-nodeTree association/linking to parrentNode
        for node in thisNode.subNodes_[nodeIx_].subNodes_:
            # fix subNodes association/link to parrentNode
            node.parrentNode_ = thisSubNode
                
        # Fix thisSubNode & its sub-nodeTree nodeIds
        thisNode.subNodes_[nodeIx_].updateSubNodeTreeNodeIds()

        return thisNode.subNodes_[nodeIx_]
#-----------------------------------
#--------------------- REPLACE Helper/Wrapper Methods -----------------

#------------------- Gloabl Search -----------------------------------
    # Find node with specifed nodeId (id), relative search from thisNode to end of its sub-nodeTree
    # use rootNode if you are unsure about where the node is located
    def findNodeById(self, nodeId_, caseSensitive=0):
        thisNode = self
        startNode = thisNode

        # Search for the Node with the specified NodeId in this Nodes sub-Tree
        while(thisNode != ""):
        
            # is this caseSesnsitive search?
            if(caseSensitive == 0):                  
                # Is This the node we are looking for?
                if(thisNode.nodeId_.lower() == nodeId_.lower()):
                    # Node found retun it
                    return thisNode
            else: # Assume case sensitive search
                # Is This the node we are looking for?
                if(thisNode.nodeId_ == nodeId_):
                    # Node found retun it
                    return thisNode                
            
            # Get Next Node
            thisNode = thisNode.getNextNode(startNode)
        
        # Assume the node was not found
        self.error_ = "findNodeById: Unable to find the node with Id " + nodeId_
        return ""

    # Same as findNodeById, but uses the get/set method naming convention
    # Searches relative from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure about where the node is
    def getNodeById(self, nodeId_, caseSensitive=0):
        thisNode = self
        startNode = thisNode

        # Search for the Node with the specified NodeId in this Nodes sub-Tree
        while(thisNode != ""):
        
            # is this caseSesnsitive search?
            if(caseSensitive == 0):                  
                # Is This the node we are looking for?
                if(thisNode.nodeId_.lower() == nodeId_.lower()):
                    # Node found retun it
                    return thisNode
            else: # Assume case sensitive search
                # Is This the node we are looking for?
                if(thisNode.nodeId_ == nodeId_):
                    # Node found retun it
                    return thisNode                
            
            # Get Next Node
            thisNode = thisNode.getNextNode(startNode)
        
        # Assume the node was not found
        self.error_ = "getNodeById: Unable to find the node with Id " + nodeId_        
        return ""        

    # Find first node with specifed name, relative search from thisNode to end of its sub-nodeTree
    # Use rootNode if your are unsure where the node is located
    def findNodeByName(self, name_, caseSensitive=0):
        thisNode = self
        startNode = thisNode        

        # Search for the Node with the specified NodeId in this Nodes sub-Tree
        while(thisNode != ""):
        
            # is this caseSesnsitive search?
            if(caseSensitive == 0):                  
                # Is This the node we are looking for?
                if(thisNode.name_.lower() == name_.lower()):
                    # Node found retun it
                    return thisNode
            else: # Assume case sensitive search
                # Is This the node we are looking for?
                if(thisNode.name_ == name_):
                    # Node found retun it
                    return thisNode                
            
            # Get Next Node
            thisNode = thisNode.getNextNode(startNode)
        
        # Assume the node was not found
        self.error_ = "findNodeByName: Unable to find the node with name " + name_        
        return ""

    # Find first node with specifed name, relative search from thisNode to end of its sub-nodeTree
    # Use rootNode if your are unsure where the node is located
    def getNodeByName(self, name_, caseSensitive=0):
        thisNode = self
        startNode = thisNode        

        # Search for the Node with the specified NodeId in this Nodes sub-Tree
        while(thisNode != ""):
        
            # is this caseSesnsitive search?
            if(caseSensitive == 0):                  
                # Is This the node we are looking for?
                if(thisNode.name_.lower() == name_.lower()):
                    # Node found retun it
                    return thisNode
            else: # Assume case sensitive search
                # Is This the node we are looking for?
                if(thisNode.name_ == name_):
                    # Node found retun it
                    return thisNode                
            
            # Get Next Node
            thisNode = thisNode.getNextNode(startNode)
        
        # Assume the node was not found
        self.error_ = "getNodeByName: Unable to find the node with name " + name_        
        return ""        

    # Finds first node with specified value
    # Searches relative from thisNode to end of its sub-nodeTree
    # Use rootNode if you are unsure where the value is located
    # Can be used to detect wether a given value has allready be added to node tree when handling uniqe data.
    def findNodeByValue(self, value_, caseSensitive=0):
        thisNode = self
        startNode = thisNode
        
        # Search for the Node with the specified NodeId in this Nodes sub-Tree
        while(thisNode != ""):
            
            # is this caseSesnsitive search?
            if(caseSensitive == 0):                  
                # Is This the node we are looking for?
                if(thisNode.value_.lower() == value_.lower()):
                    # Node found retun it
                    return thisNode
            else: # Assume case sensitive search
                # Is This the node we are looking for?
                if(thisNode.value_ == value_):
                    # Node found retun it
                    return thisNode

            # Get Next Node
            thisNode = thisNode.getNextNode(startNode)
        
        # Assume the node was not found, values dataType is unknowns so we will let the expcition handler "getString" handle it
        self.error_ = "findNodeByValue: Unable to find a node->value " + self.getString(value_) + " in " + startNode.name_ + " sub-nodeTree"        
        return ""

    # Finds first node with specified value
    # Searches relative from thisNode to end of its sub-nodeTree
    # Use rootNode if you are unsure where the value is located
    # Can be used to detect wether a given value has allready be added to node tree when handling uniqe data.
    def getNodeByValue(self, value_, caseSensitive=0):
        thisNode = self
        startNode = thisNode
        
        # Search for the Node with the specified NodeId in this Nodes sub-Tree
        while(thisNode != ""):
            
            # is this caseSesnsitive search?
            if(caseSensitive == 0):                  
                # Is This the node we are looking for?
                if(thisNode.value_.lower() == value_.lower()):
                    # Node found retun it
                    return thisNode
            else: # Assume case sensitive search
                # Is This the node we are looking for?
                if(thisNode.value_ == value_):
                    # Node found retun it
                    return thisNode

            # Get Next Node
            thisNode = thisNode.getNextNode(startNode)
        
        # Assume the node was not found
        self.error_ = "getNodeByValue: Unable to find a node->value " + self.getString(value_) + " in " + startNode.name_ + " sub-nodeTree"        
        return ""

#----------------------- node dataAnalysis methods ------------------    
    # Finds frequency of node value
    # Searches relative from thisNode to end of its sub-nodeTree
    # Use rootNode if you are unsure where the value is located
    # Can be used in data-analysis to count the frequency of a given value if you have decided not to use the unique feature in the nodeTree
    def getNodeByValueFreq(self, value_, caseSensitive=0):
        thisNode = self
        startNode = thisNode
        
        # Search for every Node with the specified NodeId in this Nodes sub-Tree
        valueFreq= 0
        while(thisNode != ""):
            
            # is this caseSesnsitive search?
            if(caseSensitive == 0):                  
                # Is This the node we are looking for?
                if(thisNode.value_.lower() == value_.lower()):
                    # Node found update freq
                    valueFreq += 1
            else: # Assume case sensitive search
                # Is This the node we are looking for?
                if(thisNode.value_ == value_):
                    # Node found update value freq
                    valueFreq += 1

            # Get Next Node
            thisNode = thisNode.getNextNode(startNode)
        
        # return the value frequency
        return valueFreq

    #----------- peerNode dataAnalysis methods------------
    # Returns nodeTree containg all differences between the peerNodes in thisNodes parrentNodes sub-nodeChain
    # TODO. Implement it (OK)
    # TODO: Implement all uniqueness Levels
    def getPeerNodeValueDifferences(self, caseSensitive=0, uniqueLevel_=0):
        thisNode = self

        # Create New NodeTree for storing diffrences
        diffNodeTree = analysisNodeTree("Value Differences")
        
        # Should be the difference be counted using build in frequency count?
        if uniqueLevel_ > 0:
            for subNode in thisNode.parrentNode_.subNodes_:
                # Is this value unique?
                if subNode.freq_ < 2:
                    # Has a subNode been created for this Diffrence?
                    diffNode = diffNodeTree.getSubNodeByName(subNode.nodeId_)
                    if(diffNode == ""):
                        diffNode = diffNodeTree.addSubNode(subNode.nodeId_, subNode.value_)
                    else:
                        diffNode.value_ = subNode.value_

                    # Update Diffrence freq/count
                    diffNodeTree.freq_ += 1                    

            # Return the nodeTree containing all diffrences
            return diffNodeTree

        else:
            # Compare Diffrences "Find Unique fields"
            uniqueNode = 1
            for subNodeA in thisNode.parrentNode_.subNodes_:
                # Assume the node is unique
                uniqueNode = 1
                for subNodeB in thisNode.parrentNode_.subNodes_: # No need to dbl check prev values
                    # Is this self?
                    if subNodeA != subNodeB:
                        # Is subNodeB diffrent from subNodeA?
                        # Is compare case sensitive?
                        if(caseSensitive):
                            if subNodeA.value_.lower() == subNodeB.value_.lower():
                                # Exit for since subNode is not unique
                                uniqueNode = 0
                                break
                        else:
                            if subNodeA.value_ == subNodeB.value_:
                                # Exit for since subNode is not unique
                                uniqueNode = 0
                                break

                # Was the node Unique within sub-nodeChain?
                if uniqueNode == 1:
                    # Has a subNode been created for this Diffrence?
                    diffNode = diffNodeTree.getSubNodeByName(subNodeA.nodeId_)
                    if(diffNode == ""):
                        diffNode = diffNodeTree.addSubNode(subNodeA.nodeId_, subNodeA.value_)
                    else:
                        diffNode.value_ = subNodeA.value_ 

                    # Update difference freq/count
                    diffNodeTree.freq_ += 1

            # Return the nodeTree containing the differences
            return diffNodeTree               

        # Assume no diffrences to be found
        self.error_ = "getPeerNodeValueDifferences: No Differences found in " + thisNode.name_ + " peerNodes"        
        return ""

    # Returns nodeTree containg all differences between the two peerNodes sub-nodeChain
    # TODO. Implement it
    def getPeerNodeValuesDifferences(self, caseSensitive=0, uniqueLevel_=0):
        thisNode = self

        # Create New NodeTree for storing diffrences
        diffNodeTree = analysisNodeTree("Value Differences")
        
        # Should be the difference be counted using build in frequency count?
        if uniqueLevel_ > 0:
            for subNode in thisNode.parrentNode_.subNodes_:
                # Is this value unique?
                if subNode.freq_ < 2:
                    # Has a subNode been created for this Diffrence?
                    diffNode = diffNodeTree.getSubNodeByName(subNode.nodeId_)
                    if(diffNode == ""):
                        diffNode = diffNodeTree.addSubNode(subNode.nodeId_, subNode.value_)
                    else:
                        diffNode.value_ = subNode.value_

                    # Update Diffrence freq/count
                    diffNodeTree.freq_ += 1                    

            # Return the nodeTree containing all diffrences
            return diffNodeTree

        else:
            # Compare Diffrences "Find Unique fields"
            uniqueNode = 1
            for subNodeA in thisNode.parrentNode_.subNodes_:
                # Assume the node is unique
                uniqueNode = 1
                for subNodeB in thisNode.parrentNode_.subNodes_: # No need to dbl check prev values
                    # Is this self?
                    if subNodeA != subNodeB:
                        # Is subNodeB diffrent from subNodeA?
                        # Is compare case sensitive?
                        if(caseSensitive):
                            if subNodeA.value_.lower() == subNodeB.value_.lower():
                                # Exit for since subNode is not unique
                                uniqueNode = 0
                                break
                        else:
                            if subNodeA.value_ == subNodeB.value_:
                                # Exit for since subNode is not unique
                                uniqueNode = 0
                                break

                # Was the node Unique within sub-nodeChain?
                if uniqueNode == 1:
                    # Has a subNode been created for this Diffrence?
                    diffNode = diffNodeTree.getSubNodeByName(subNodeA.nodeId_)
                    if(diffNode == ""):
                        diffNode = diffNodeTree.addSubNode(subNodeA.nodeId_, subNodeA.value_)
                    else:
                        diffNode.value_ = subNodeA.value_ 

                    # Update difference freq/count
                    diffNodeTree.freq_ += 1

            # Return the nodeTree containing the differences
            return diffNodeTree               

        # Ass no diffrences to be found
        return ""        
    
    # Returns nodeTree containg all similarities between the subNodes in thisNodes nodeChain
    # TODO. Implement it (OK)
    def getPeerNodeValueSimilarities(self, caseSensitive=0, uniqueLevel_=0):
        thisNode = self
        
        # Create New NodeTree for storing diffrences
        simiNodeTree = analysisNodeTree("Value Similarities")
        simiNodeTree.freq_ = 0 # Ensure freq starts at 0 since we are are not using freq for its normal purpose
        
        # Should be the difference be counted using build in frequency count?
        if uniqueLevel_ > 0:
            for subNode in thisNode.parrentNode_.subNodes_:
                # Is this value non-unique?, hence does this exists more then once in the sub-nodeChain
                if subNode.freq_ > 1:
                    # Has a subNode been created for this Diffrence?
                    simiNode = simiNodeTree.getSubNodeByName(subNode.nodeId_)
                    if(simiNode == ""):
                        simiNode = simiNodeTree.addSubNode(subNode.nodeId_, subNode.value_)
                        simiNode.freq_ = subNode.freq_
                    else:
                        simiNode.value_ = subNode.value_
                        simiNode.freq_ = subNode.freq_

                    # Update Diffrence freq/count
                    simiNodeTree.freq_ += 1                    

            # Return the nodeTree containing all diffrences
            return simiNodeTree

        else:
            # Compare Similarities "Find Dublet fields"
            for subNodeA in thisNode.parrentNode_.subNodes_:
                # Assume the node is unique
                for subNodeB in thisNode.parrentNode_.subNodes_: # No need to dbl check prev values
                    # Is this self?
                    if subNodeA != subNodeB:
                        # Is subNodeB diffrent from subNodeA?
                        # Is compare case sensitive?
                        if(caseSensitive):
                            if subNodeA.value_.lower() == subNodeB.value_.lower():
                                # Has this value allready been added to nodeTree?
                                simiNode = simiNodeTree.getNodeByName(subNodeB.nodeId_)

                                if simiNode != "":
                                    # Just update the freq count for this node->value
                                    simiNode.freq_ += 1
                                else:
                                    # Add the new vaue to the nodeTree
                                    simiNodeTree.addSubNode(subNodeA.nodeIx_, subNodeA.value_)
                                                                
                        else:
                            if subNodeA.value_ == subNodeB.value_:
                                # Has this value allready been added to nodeTree?
                                simiNode = simiNodeTree.getNodeByName(subNodeB.nodeId_)

                                if simiNode != "":
                                    # Just update the freq count for this node->value
                                    simiNode.freq_ += 1
                                else:
                                    # Add the new vaue to the nodeTree
                                    simiNodeTree.addSubNode(subNodeA.nodeIx_, subNodeA.value_)

                                    # Update number of similarities
                                    simiNodeTree.freq_ += 1
                                
            # Return the nodeTree containing the similarities
            return simiNodeTree

        # Assume no similarities found between thisNodes peerNodes
        self.error_ = "getPeerNodeValueSimilarities: No Similarities found in " + thisNode.name_ + " peerNodes"        
        return ""

    # Returns nodeTree containg all similarities between the subNodes in thisNodes nodeChain
    # TODO. Implement it
    def getPeerNodesValueSimilarities(self, caseSensitive=0, uniqueLevel_=0):
        thisNode = self
        
        # Create New NodeTree for storing diffrences
        simiNodeTree = analysisNodeTree("Value Similarities")
        simiNodeTree.freq_ = 0 # Ensure freq starts at 0 since we are are not using freq for its normal purpose
        
        # Should be the difference be counted using build in frequency count?
        if uniqueLevel_ > 0:
            for subNode in thisNode.parrentNode_.subNodes_:
                # Is this value non-unique?, hence does this exists more then once in the sub-nodeChain
                if subNode.freq_ > 1:
                    # Has a subNode been created for this Diffrence?
                    simiNode = simiNodeTree.getSubNodeByName(subNode.nodeId_)
                    if(simiNode == ""):
                        simiNode = simiNodeTree.addSubNode(subNode.nodeId_, subNode.value_)
                        simiNode.freq_ = subNode.freq_
                    else:
                        simiNode.value_ = subNode.value_
                        simiNode.freq_ = subNode.freq_

                    # Update Diffrence freq/count
                    simiNodeTree.freq_ += 1                    

            # Return the nodeTree containing all diffrences
            return simiNodeTree

        else:
            # Compare Similarities "Find Dublet fields"
            for subNodeA in thisNode.parrentNode_.subNodes_:
                # Assume the node is unique
                for subNodeB in thisNode.parrentNode_.subNodes_: # No need to dbl check prev values
                    # Is this self?
                    if subNodeA != subNodeB:
                        # Is subNodeB diffrent from subNodeA?
                        # Is compare case sensitive?
                        if(caseSensitive):
                            if subNodeA.value_.lower() == subNodeB.value_.lower():
                                # Has this value allready been added to nodeTree?
                                simiNode = simiNodeTree.getNodeByName(subNodeB.nodeId_)

                                if simiNode != "":
                                    # Just update the freq count for this node->value
                                    simiNode.freq_ += 1
                                else:
                                    # Add the new vaue to the nodeTree
                                    simiNodeTree.addSubNode(subNodeA.nodeIx_, subNodeA.value_)
                                                                
                        else:
                            if subNodeA.value_ == subNodeB.value_:
                                # Has this value allready been added to nodeTree?
                                simiNode = simiNodeTree.getNodeByName(subNodeB.nodeId_)

                                if simiNode != "":
                                    # Just update the freq count for this node->value
                                    simiNode.freq_ += 1
                                else:
                                    # Add the new vaue to the nodeTree
                                    simiNodeTree.addSubNode(subNodeA.nodeIx_, subNodeA.value_)

                                    # Update number of similarities
                                    simiNodeTree.freq_ += 1
                                
            # Return the nodeTree containing the similarities
            return simiNodeTree

        # Assume no similarities found between thisNodes peerNodes
        self.error_ = "getPeerNodesValueSimilarities: No Similarities found in " + thisNode.name_ + " peerNodes"        
        return ""        
    #------------------------------------------------    
    #------------------------------------------------

    #---------------------------------------------
#--------------- subNode searching -------------

    #--------- subNode Data-analysis methods -----------    
    # Returns nodeTree containg all differences between the subNodes in thisNodes nodeChain
    # Name is the name nodeId for the unique node and value is the value of the unique node
    # TODO. Implement it (OK)
    def getSubNodeValueDifferences(self, caseSensitive=0, uniqueLevel_=0):
        thisNode = self

        # Create New NodeTree for storing diffrences
        diffNodeTree = analysisNodeTree("Value Differences")
        diffNodeTree.freq_ = 0 # Ensure freq starts at 0 since we are are not using freq for its normal purpose
        
        # Should be the difference be counted using build in frequency count?
        if uniqueLevel_ > 0:
            for subNode in thisNode.subNodes_:
                # Is this value unique?
                if subNode.freq_ < 2:
                    # Has a subNode been created for this Diffrence?
                    diffNode = diffNodeTree.getSubNodeByName(subNode.nodeId_)
                    if(diffNode == ""):
                        diffNode = diffNodeTree.addSubNode(subNode.nodeId_, subNode.value_)
                    else:
                        diffNode.value_ = subNode.value_

                    # Update Diffrence freq/count
                    diffNodeTree.freq_ += 1                    

            # Return the nodeTree containing all diffrences
            return diffNodeTree

        else:
            # Compare Diffrences "Find Unique fields"
            uniqueNode = 1
            for subNodeA in thisNode.subNodes_:
                # Assume the node is unique
                uniqueNode = 1
                for subNodeB in thisNode.subNodes_: # No need to dbl check prev values
                    # Is this self?
                    if subNodeA != subNodeB:
                        # Is subNodeB diffrent from subNodeA?
                        # Is compare case sensitive?
                        if(caseSensitive):
                            if subNodeA.value_.lower() == subNodeB.value_.lower():
                                # Exit for since subNode is not unique
                                uniqueNode = 0
                                break
                        else:
                            if subNodeA.value_ == subNodeB.value_:
                                # Exit for since subNode is not unique
                                uniqueNode = 0
                                break

                # Was the node Unique within sub-nodeChain?
                if uniqueNode == 1:
                    # Has a subNode been created for this Diffrence?
                    diffNode = diffNodeTree.getSubNodeByName(subNodeA.nodeId_)
                    if(diffNode == ""):
                        diffNode = diffNodeTree.addSubNode(subNodeA.nodeId_, subNodeA.value_)
                    else:
                        diffNode.value_ = subNodeA.value_ 

                    # Update difference freq/count
                    diffNodeTree.freq_ += 1

            # Return the nodeTree containing the differences
            return diffNodeTree               

        # Assume no diffrences to be found
        self.error_ = "getSubNodeValueDifferences: No Differences found in " + thisNode.name_ + "s sub-nodeChain"        
        return ""

    # Returns nodeTree containg all differences between the subNodes in thisNodes nodeChain
    # Name is the name nodeId for the unique node and value is the value of the unique node
    # TODO. Implement it
    def getSubNodesValueDifferences(self, caseSensitive=0, uniqueLevel_=0):
        thisNode = self

        # Create New NodeTree for storing diffrences
        diffNodeTree = analysisNodeTree("Value Differences")
        diffNodeTree.freq_ = 0 # Ensure freq starts at 0 since we are are not using freq for its normal purpose
        
        # Should be the difference be counted using build in frequency count?
        if uniqueLevel_ > 0:
            for subNode in thisNode.subNodes_:
                # Is this value unique?
                if subNode.freq_ < 2:
                    # Has a subNode been created for this Diffrence?
                    diffNode = diffNodeTree.getSubNodeByName(subNode.nodeId_)
                    if(diffNode == ""):
                        diffNode = diffNodeTree.addSubNode(subNode.nodeId_, subNode.value_)
                    else:
                        diffNode.value_ = subNode.value_

                    # Update Diffrence freq/count
                    diffNodeTree.freq_ += 1                    

            # Return the nodeTree containing all diffrences
            return diffNodeTree

        else:
            # Compare Diffrences "Find Unique fields"
            uniqueNode = 1
            for subNodeA in thisNode.subNodes_:
                # Assume the node is unique
                uniqueNode = 1
                for subNodeB in thisNode.subNodes_: # No need to dbl check prev values
                    # Is this self?
                    if subNodeA != subNodeB:
                        # Is subNodeB diffrent from subNodeA?
                        # Is compare case sensitive?
                        if(caseSensitive):
                            if subNodeA.value_.lower() == subNodeB.value_.lower():
                                # Exit for since subNode is not unique
                                uniqueNode = 0
                                break
                        else:
                            if subNodeA.value_ == subNodeB.value_:
                                # Exit for since subNode is not unique
                                uniqueNode = 0
                                break

                # Was the node Unique within sub-nodeChain?
                if uniqueNode == 1:
                    # Has a subNode been created for this Diffrence?
                    diffNode = diffNodeTree.getSubNodeByName(subNodeA.nodeId_)
                    if(diffNode == ""):
                        diffNode = diffNodeTree.addSubNode(subNodeA.nodeId_, subNodeA.value_)
                    else:
                        diffNode.value_ = subNodeA.value_ 

                    # Update difference freq/count
                    diffNodeTree.freq_ += 1

            # Return the nodeTree containing the differences
            return diffNodeTree               

        # Assume no diffrences to be found
        self.error_ = "getSubNodesValueDifferences: No Differences found in between " + thisNode.name_ + " sub-nodeChain & xx nodes sub-nodeChain"        
        return ""        

    # Returns nodeTree containg all similarities & differences between the subNodes in thisNodes nodeChain
    # Name is the name nodeId for the unique node and value is the value of the unique node
    # TODO. Implement it
    def getSubNodeValueFreqAnalysis(self, caseSensitive=0, uniqueLevel_=0):
        thisNode = self

        # Create New NodeTree for storing diffrences
        compNodeTree = analysisNodeTree("Value Analysis")

        # Calc Diffrences
        compNodeTree.addSubNodeObj(thisNode.getSubNodeValueDifferences(caseSensitive, uniqueLevel_))
        compNodeTree.addSubNodeObj(thisNode.getSubNodeValueSimilarities(caseSensitive, uniqueLevel_))

        # return nodeTree Containg all similarites and diffrences
        return compNodeTree

    # Returns nodeTree containg all similarities & differences between the subNodes in thisNodes nodeChain
    # Name is the name nodeId for the unique node and value is the value of the unique node
    # TODO. Implement it
    def getSubNodesValueFreqAnalysis(self, caseSensitive=0, uniqueLevel_=0):
        thisNode = self

        # Create New NodeTree for storing diffrences
        compNodeTree = analysisNodeTree("Value Analysis")

        # Calc Diffrences
        compNodeTree.addSubNodeObj(thisNode.getSubNodeValueDifferences(caseSensitive, uniqueLevel_))
        compNodeTree.addSubNodeObj(thisNode.getSubNodeValueSimilarities(caseSensitive, uniqueLevel_))

        # return nodeTree Containg all similarites and diffrences
        return compNodeTree        

    # Returns nodeTree containg all similarities between the subNodes in thisNodes nodeChain
    # TODO. Implement it
    def getSubNodeValueSimilarities(self, caseSensitive=0, uniqueLevel_=0):
        thisNode = self

        # Create New NodeTree for storing diffrences
        simiNodeTree = analysisNodeTree("Value Similarities")
        simiNodeTree.freq_ = 0 # Ensure freq starts at 0 since we are are not using freq for its normal purpose
        
        # Should be the difference be counted using build in frequency count?
        if uniqueLevel_ > 0:
            for subNode in thisNode.subNodes_:
                # Is this value non-unique?, hence does this exists more then once in the sub-nodeChain
                if subNode.freq_ > 1:
                    # Has a subNode been created for this Diffrence?
                    simiNode = simiNodeTree.getSubNodeByName(subNode.nodeId_)
                    if(simiNode == ""):
                        simiNode = simiNodeTree.addSubNode(subNode.nodeId_, subNode.value_)
                        simiNode.freq_ = subNode.freq_
                    else:
                        simiNode.value_ = subNode.value_
                        simiNode.freq_ = subNode.freq_

                    # Update Diffrence freq/count
                    simiNodeTree.freq_ += 1                    

            # Return the nodeTree containing all diffrences
            return simiNodeTree

        else:
            # Compare Similarities "Find Dublet fields"
            for subNodeA in thisNode.subNodes_:
                # Assume the node is unique
                for subNodeB in thisNode.subNodes_: # No need to dbl check prev values
                    # Is this self?
                    if subNodeA != subNodeB:
                        # Is subNodeB diffrent from subNodeA?
                        # Is compare case sensitive?
                        if(caseSensitive):
                            if subNodeA.value_.lower() == subNodeB.value_.lower():
                                # Has this value allready been added to nodeTree?
                                simiNode = simiNodeTree.getNodeByName(subNodeB.nodeId_)

                                if simiNode != "":
                                    # Just update the freq count for this node->value
                                    simiNode.freq_ += 1
                                else:
                                    # Add the new vaue to the nodeTree
                                    simiNodeTree.addSubNode(subNodeA.nodeIx_, subNodeA.value_)
                                                                
                        else:
                            if subNodeA.value_ == subNodeB.value_:
                                # Has this value allready been added to nodeTree?
                                simiNode = simiNodeTree.getNodeByName(subNodeB.nodeId_)

                                if simiNode != "":
                                    # Just update the freq count for this node->value
                                    simiNode.freq_ += 1
                                else:
                                    # Add the new vaue to the nodeTree
                                    simiNodeTree.addSubNode(subNodeA.nodeIx_, subNodeA.value_)

                                    # Update number of similarities
                                    simiNodeTree.freq_ += 1
                                
            # Return the nodeTree containing the similarities
            return simiNodeTree

        # Assume No Similarities found
        self.error_ = "getSubNodeValueSimilarities: No Similarities found in between " + thisNode.name_ + " sub-nodeChain"
        return ""

    # Returns nodeTree containg all similarities between the subNodes in thisNodes nodeChain
    # TODO. Implement it
    def getSubNodesValueSimilarities(self, caseSensitive=0, uniqueLevel_=0):
        thisNode = self

        # Create New NodeTree for storing diffrences
        simiNodeTree = analysisNodeTree("Value Similarities")
        simiNodeTree.freq_ = 0 # Ensure freq starts at 0 since we are are not using freq for its normal purpose
        
        # Should be the difference be counted using build in frequency count?
        if uniqueLevel_ > 0:
            for subNode in thisNode.subNodes_:
                # Is this value non-unique?, hence does this exists more then once in the sub-nodeChain
                if subNode.freq_ > 1:
                    # Has a subNode been created for this Diffrence?
                    simiNode = simiNodeTree.getSubNodeByName(subNode.nodeId_)
                    if(simiNode == ""):
                        simiNode = simiNodeTree.addSubNode(subNode.nodeId_, subNode.value_)
                        simiNode.freq_ = subNode.freq_
                    else:
                        simiNode.value_ = subNode.value_
                        simiNode.freq_ = subNode.freq_

                    # Update Diffrence freq/count
                    simiNodeTree.freq_ += 1                    

            # Return the nodeTree containing all diffrences
            return simiNodeTree

        else:
            # Compare Similarities "Find Dublet fields"
            for subNodeA in thisNode.subNodes_:
                # Assume the node is unique
                for subNodeB in thisNode.subNodes_: # No need to dbl check prev values
                    # Is this self?
                    if subNodeA != subNodeB:
                        # Is subNodeB diffrent from subNodeA?
                        # Is compare case sensitive?
                        if(caseSensitive):
                            if subNodeA.value_.lower() == subNodeB.value_.lower():
                                # Has this value allready been added to nodeTree?
                                simiNode = simiNodeTree.getNodeByName(subNodeB.nodeId_)

                                if simiNode != "":
                                    # Just update the freq count for this node->value
                                    simiNode.freq_ += 1
                                else:
                                    # Add the new vaue to the nodeTree
                                    simiNodeTree.addSubNode(subNodeA.nodeIx_, subNodeA.value_)
                                                                
                        else:
                            if subNodeA.value_ == subNodeB.value_:
                                # Has this value allready been added to nodeTree?
                                simiNode = simiNodeTree.getNodeByName(subNodeB.nodeId_)

                                if simiNode != "":
                                    # Just update the freq count for this node->value
                                    simiNode.freq_ += 1
                                else:
                                    # Add the new vaue to the nodeTree
                                    simiNodeTree.addSubNode(subNodeA.nodeIx_, subNodeA.value_)

                                    # Update number of similarities
                                    simiNodeTree.freq_ += 1
                                
            # Return the nodeTree containing the similarities
            return simiNodeTree

        # Assume no Similarities has been found
        self.error_ = "getSubNodesValueSimilarities: No Similarities found between " + thisNode.name_ + " sub-nodeChain and xx nodes sub-nodeChain"
        return ""            
    #------------------------------------------------     

    # Find subNode with specified nodeId (id), relative search in thisNodes subNodes/nodeChain
    # TODO: Implement caseSenstive option
    def findSubNodeById(self, nodeId_, caseSensitive=0):
        thisNode = self

        # Is this leafNode?
        if(thisNode.subNodeCount_ == 0):
            # YES => leafNodes dont have subNodes
            self.error_ = "findSubNodeById: leafNodes dont have subNodes!!"
            return ""

        # Find the subNode
        for node in thisNode.subNodes_:
            #Is this the subNode we are looking for?
            if(node.nodeId_.lower() == nodeId_.lower()):
                return node

        # Assume the node was not found
        self.error_ = "findSubNodeById: Unable to find the node with Id " + nodeId_        
        return ""

    # Same as findSubNodeById, but uses the get/set method naming convention
    # Searches relative from thisNode and to end of its sub-nodeTree
    # use rootNode if you are unsure about where the node is
    # TODO: Implement caseSenstive option
    def getSubNodeById(self, nodeId_, caseSensitive=0):
        thisNode = self

        # Is this leafNode?
        if(thisNode.subNodeCount_ == 0):
            # YES => leafNodes dont have subNodes
            self.error_ = "getSubNodeById: leafNodes dont have subNodes!!" + nodeId_            
            return ""

        # Find the subNode
        for node in thisNode.subNodes_:
            #Is this the subNode we are looking for?
            if(node.nodeId_.lower() == nodeId_.lower()):
                return node

        # Assume the node was not found
        self.error_ = "getSubNodeById: Unable to find the node with Id " + nodeId_        
        return ""        

    # Find subNode with specifed name, relative search in thisNodes subNodes
    # TODO. Implement caseSesntive option
    def findSubNodeByName(self, name_, caseSensitive=0):
        thisNode = self

        # Is this leafNode?
        if(thisNode.subNodeCount_ == 0):
            # YES => leafNodes dont have subNodes
            self.error_ = "findSubNodeByName: leafNodes dont have subNodes!!"
            return ""

        # Find the subNode
        for node in thisNode.subNodes_:
            #Is this the subNode we are looking for?
            if(node.name_.lower() == name_.lower()):
                return node

        # Assume the node was not found
        self.error_ = "findSubNodeByName: Unable to find the node with name " + name_        
        return ""

    # Find subNode with specifed name, relative search in thisNodes subNodes
    # TODO: Implement caseSesntive option
    def getSubNodeByName(self, name_, caseSensitive=0):
        thisNode = self

        # Is this leafNode?
        if(thisNode.subNodeCount_ == 0):
            # YES => leafNodes dont have subNodes
            self.error_ = "getSubNodeByName: leafNodes dont have subNodes!!"            
            return ""

        # Find the subNode
        for node in thisNode.subNodes_:
            #Is this the subNode we are looking for?
            if(node.name_.lower() == name_.lower()):
                return node

        # Assume the node was not found
        self.error_ = "getSubNodeByName: Unable to find the node with name " + name_
        return ""        

    # Finds first node with specified value
    # Searches relative in thisNodes subNodes
    # Can be used to detect wether a given value has allready be added to node tree when handling uniqe data.
    # TODO: Implement caseSenstive option
    def findSubNodeByValue(self, value_, caseSensitive=0):
        thisNode = self

        # Is this leafNode?
        if(thisNode.subNodeCount_ == 0):
            # YES => leafNodes dont have subNodes
            self.error_ = "findSubNodeByValue: leafNodes dont have subNodes!!"            
            return ""

        # Find the subNode
        for node in thisNode.subNodes_:
            #Is this the subNode we are looking for?
            if(node.value_.lower() == value_.lower()):
                return node

        # Assume the node was not found
        self.error_ = "findSubNodeByValue: Unable to find the node with value " + self.getString(value_)        
        return ""

    # Finds first node with specified value
    # Searches relative in thisNodes subNodes
    # Can be used to detect wether a given value has allready be added to node tree when handling uniqe data.
    # TODO: Implement caseSesnitive option
    def getSubNodeByValue(self, value_, caseSensitive=0):
        thisNode = self

        # Is this leafNode?
        if(thisNode.subNodeCount_ == 0):
            # YES => leafNodes dont have subNodes
            self.error_ = "getSubNodeByValue: leafNodes dont have subNodes!!"
            return ""

        # Find the subNode
        for node in thisNode.subNodes_:
            #Is this the subNode we are looking for?
            if(node.value_.lower() == value_.lower()):
                return node

        # Assume the node was not found
        self.error_ = "getSubNodeByValue: Unable to find the node with value " + self.getString(value_)        
        return ""            

# ------------ nodeTree Traversal/Navigation helper functions --------------
    # Returns first peerNode of thisNode
    def getFirstPeerNode(self):
        thisNode = self
        
        # Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => rootNode has no peerNodes
            self.error_ = "getFirstPeerNode: rootNodes dont have peerNodes!!"            
            return ""

        # Get parrentNode
        thisNode = thisNode.parrentNode_
        # Does this node have subNodes?
        if(thisNode.subNodeCount_ == 0):
            # NO => This node dont have subNodes
            self.error_ = "getFirstPeerNode: No peerNode found!!"            
            return ""

        thisNode = thisNode.subNodes_[0]

        return thisNode

    # Returns last peerNode of thisNode
    def getLastPeerNode(self):
        thisNode = self
        
        # Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => rootNode has no peerNodes
            self.error_ = "getLastPeerNode: rootNodes dont have peerNodes!!"            
            return ""

        # Get parrentNode
        thisNode = thisNode.parrentNode_
        # Does this node have subNodes?
        if(thisNode.subNodeCount_ == 0):
            # NO => This node dont have subNodes
            self.error_ = "getLastPeerNode: No peerNode found!!"            
            return ""
            
        thisNode = thisNode.subNodes_[thisNode.subNodeCount_ - 1] # Remember binary math!!

        return thisNode

    # Returns first subNode of thisNode
    def getFirstSubNode(self):
        thisNode = self
        
        # Is this leafNode?
        if(thisNode.subNodeCount_ == 0):
            # YES => leafNode has no subNodes
            self.error_ = "getFirstSubNode: leafNodes dont have subNodes!!"            
            return ""

        thisNode = thisNode.subNodes_[0]

        return thisNode

    # Returns last subNode of thisNode
    def getLastSubNode(self):
        thisNode = self
        
        # Is this leafNode?
        if(thisNode.subNodeCount_ == 0):
            # YES => leafNode has no subNodes
            self.error_ = "getLastSubNode: leafNodes dont have subNodes!!"            
            return ""
            
        thisNode = thisNode.subNodes_[thisNode.subNodeCount_ - 1] # Remember binary math!!

        return thisNode

    # Returns next parrentNode relative to thisNode
    def getNextParrentNode(self):
        thisNode = self

        # Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => rootNode has no parrentNode
            self.error_ = "getNextParrentNode: rootNodes dont have parrentNodes!!"            
            return ""

        # move upto Parrent
        thisNode = thisNode.parrentNode_
        # Get next peerNode
        thisNode = thisNode.getNextPeerNode()

        return thisNode
    
    # Returns prev parrentNode relative to thisNode     
    def getPrevParrentNode(self):
        thisNode = self

        # Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => rootNode has no parrentNode
            self.error_ = "getPrevParrentNode: rootNodes dont have parrentNodes!!"            
            return ""

        # move upto Parrent
        thisNode = thisNode.parrentNode_
        # Get prev peerNode
        thisNode = thisNode.getPrevPeerNode()

        return thisNode        

#---------------------------------------------------------------------
    # Find thisNodes peerNode by Id
    def findPeerNodeById(self, nodeId_, caseSensitive=0):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        # Is this rootNode?
        if(thisNode.parrentNode_ ==""):
            # YES => rootNode does not have peerNodes
            self.error_ = "findPeerNodeById: rootNodes dont have peerNodes!!"            
            return ""
        
        for node in thisParrentNode.subNodes_:
            # Is this caseSenstive search?
            if(caseSensitive == 0):
                # Is this the peerNode we are looking for?
                if(node.nodeId_.lower() == nodeId_.lower()):
                    return node
            else: # Assume case senstive search
                if(node.nodeId_ == nodeId_):
                    return node

        # Assume the peerNode did not exist
        self.error_ = "findPeerNodeById: Unable to find peerNode with Id" + nodeId_        
        return ""

    # Find peerNode with specific value, Searches relative in thisNode parrentNodes subNodes 
    def findPeerNodeByValue(self, value_, caseSensitive=0):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        #Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => rootNodes has no peerNodes
            self.error_ = "findPeerNodeByValue: rootNodes dont have peerNodes!!"            
            return ""

        # Search for the specifed peerNode->value
        for node in thisParrentNode.subNodes_:
            # is this caseSesnsitive search?
            if(caseSensitive == 0):                  
                # Is This the node we are looking for?
                if(node.value_.lower() == value_.lower()):
                    # Node found retun it
                    return node
            else: # Assume case sensitive search
                # Is This the node we are looking for?
                if(node.value_ == value_):
                    # Node found retun it
                    return node

        # Assume the nodes was not found
        self.error_ = "findPeerNodeById: Unable to find node with value " + self.getString(value_)

        return ""
#-----------------------------------------------------       
# TODO: Implement it the same was at add, inseret, replace, hence core methods that helper/wrapper methdos can call to rapidly (OK)
# Implement additional helper methods
#-------------- REMOVE node handling ------------
    # Remove thisNode
    def removeNodeObj(self):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        #Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => You cannot remove rootNode
            self.error_ = "removeNodeObj: rootNodes cannot be removed!!"            
            return ""
        
        # Remove the node
        thisParrentNode.subNodes_.remove(thisNode)

        # Update subNode Count
        thisParrentNode.subNodeCount_ -= 1

        # Fix ParrentNode and its entire sub-nodeTree
        thisParrentNode.updateSubNodeTreeNodeIds()

        return thisParrentNode

    # Remove node specified by Id, Search from thisNode to end of its sub-nodeTree
    def removeNodeObjById(self, nodeId_):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        #Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => You cannot remove rootNode
            self.error_ = "removeNodeObjById: rootNodes cannot be removed!!"            
            return ""
        
        # Find the node
        thisParrentNode = ""
        while(thisNode != ""):
            # Is this the node we are looking for?
            if(thisNode.nodeId_.lower() == nodeId_.lower()):
                # Node found
                thisParrentNode = thisNode.parrentNode_
                # Forced exit node has been found
                break

        # Was the node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "removeNodeObjById: Unable to find node with Id " + nodeId_            
            return "" 

        # Remove the node
        thisParrentNode.subNodes_.remove(thisNode)

        # Update subNode Count
        thisParrentNode.subNodeCount_ -= 1

        # Fix ParrentNode and its entire sub-nodeTree
        thisParrentNode.updateSubNodeTreeNodeIds()

        return thisParrentNode

    # Remove node specified by name, Search from thisNode to end of its sub-nodeTree
    def removeNodeObjByName(self, name_):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        #Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => You cannot remove rootNode
            self.error_ = "removeNodeObjByName: rootNodes cannot be removed!!"            
            return ""
        
        # Find the node
        thisParrentNode = ""
        while(thisNode != ""):
            # Is this the node we are looking for?
            if(thisNode.name_.lower() == name_.lower()):
                # Node found
                thisParrentNode = thisNode.parrentNode_
                # Forced exit node has been found
                break

        # Was the node found?
        if(thisParrentNode == ""):
            # YES
            self.error_ = "removeNodeObjByName: Unable to find node with name " + name_            
            return "" 

        # Remove the node
        thisParrentNode.subNodes_.remove(thisNode)

        # Update subNode Count
        thisParrentNode.subNodeCount_ -= 1

        # Fix ParrentNode and its entire sub-nodeTree
        thisParrentNode.updateSubNodeTreeNodeIds()

        return thisParrentNode        

#----------- Remove peerNode Handling -------------    
    # Remove peerNode relative to node specified Id, Search from thisNode to end of its sub-nodeChain
    def removePeerNodeObjById(self, nodeId_):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        #Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => You cannot remove rootNode
            self.error_ = "removePeerNodeObjById: rootNodes cannot be removed!!"
            return ""
        
        # Find the peerNode
        thisParrentNode =""
        for node in thisNode.parrentNode_:
            # Is this the node we are looking for?
            if(node.nodeId_.lower() == nodeId_):
                # YES
                thisParrentNode = node.parrentNode_
                thisNode = node
                break

        # Was the node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "removePeerNodeObjById: Unable to find peerNode with Id " + nodeId_             
            return ""

        # Remove the node
        thisParrentNode.subNodes_.remove(thisNode)

        # Update subNode Count
        thisParrentNode.subNodeCount_ -= 1

        # Fix ParrentNode and its entire sub-nodeTree
        thisParrentNode.updateSubNodeTreeNodeIds()

        return thisParrentNode

    # Remove peerNode relative to node specified name, Search from thisNode to end of its sub-nodeChain
    def removePeerNodeObjByName(self, name_):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        #Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => You cannot remove rootNode
            self.error_ = "removePeerNodeObjByName: rootNodes cannot be removed!!"            
            return ""
        
        # Find the peerNode
        thisParrentNode =""
        for node in thisNode.parrentNode_:
            # Is this the node we are looking for?
            if(node.name_.lower() == name_):
                # YES
                thisParrentNode = node.parrentNode_
                thisNode = node
                break

        # Was the node found?
        if(thisParrentNode == ""):
            # NO
            self.error_ = "removePeerNodeObjByName: Unable to find peerNode with name " + name_            
            return ""

        # Remove the node
        thisParrentNode.subNodes_.remove(thisNode)

        # Update subNode Count
        thisParrentNode.subNodeCount_ -= 1

        # Fix ParrentNode and its entire sub-nodeTree
        thisParrentNode.updateSubNodeTreeNodeIds()

        return thisParrentNode

    # Remove peerNode on same parrentNode/nodeChain as thisNode & relative nodeIx
    def removePeerNodeObjByIx(self, nodeIx_=0):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        #Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => You cannot remove rootNode
            self.error_ = "removePeerNodeObjByIx: rootNodes cannont be removed!!"            
            return ""
        
        # Is nodeIx valid?
        if(nodeIx_ < 0)|(nodeIx_ > thisParrentNode.subNodeCount - 1):
            # NO
            self.error_ = "removePeerNodeObjByIx: Unable to find peerNode with Ix " + str(nodeIx_)            
            return ""

        # Get peerNode
        thisNode = thisParrentNode.subNodes_[nodeIx_]

        # Remove the node
        thisParrentNode.subNodes_.remove(thisNode)

        # Update subNode Count
        thisParrentNode.subNodeCount_ -= 1

        # Fix ParrentNode and its entire sub-nodeTree
        thisParrentNode.updateSubNodeTreeNodeIds()

        return thisParrentNode            

#------------------ Remove suNode handling -----------------
    # Remove subNode on thisNode & relative at nodeIx
    def removeSubNodeObj(self, nodeIx_=0):
        thisNode = self
        thisParrentNode = thisNode

        #Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => You cannot remove rootNode
            self.error_ = "removeSubNodeObj: rootNodes cannot be removed!!"            
            return ""
        
        # Is nodeIx valid?
        if(nodeIx_ < 0)|(nodeIx_ > thisParrentNode.subNodeCount_ - 1):
            # NO
            self.error_ = "removeSubNodeObj: Unable to find subNode with Ix " + str(nodeIx_)            
            return ""

        # Get subNode
        thisNode = thisNode.subNodes_[nodeIx_]

        # Remove the node
        thisParrentNode.subNodes_.remove(thisNode)

        # Update subNode Count
        thisParrentNode.subNodeCount_ -= 1

        # Fix ParrentNode and its entire sub-nodeTree
        thisParrentNode.updateSubNodeTreeNodeIds()

        return thisParrentNode

    # Remove subNode on node specified by Id relative to node specified by Ix, Search from thisNode to end of its sub-nodeTree
    def removeSubNodeObjById(self, nodeId_, nodeIx_=0):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_
        startNode = thisNode
        
        # Find the node
        thisParrentNode =""
        while(thisNode != ""):
            # Is this the node we are looking for?
            if(thisNode.nodeId_.lower() == nodeIx_.lower()):
                # YES
                thisParrentNode = thisNode

            # Get next node
            thisNode = thisNode.getNextNode(startNode)
        
        # Has the node been found?
        if(thisParrentNode != ""):
            # NO
            self.error_ = "removeSubNodeObjById: Unable to find node with Id " + nodeId_            
            return ""
        
        # Is node Ix valid?
        if(nodeIx_ < 0)|(nodeIx_ > thisParrentNode.subNodeCount_ - 1):
            # NO
            self.error_ = "removeSubNodeObjById: Unable to find subNode with Ix " + str(nodeIx_)            
            return ""

        # Assume nodeIx is valid
        thisNode = thisParrentNode.subNodes_[nodeIx_]

        # Remove the SubNode
        thisParrentNode.subNodes_.remove(thisNode)

        # Update subNode Count
        thisParrentNode.subNodeCount_ -= 1

        # Fix ParrentNode and its entire sub-nodeTree
        thisParrentNode.updateSubNodeTreeNodeIds()

        return thisParrentNode        

    # Remove subNode on node specified by name relative to node specified by Ix, Search from thisNode to end of its sub-nodeTree
    def removeSubNodeObjByName(self, name_, nodeIx_=0):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_
        startNode = thisNode
        
        # Find the node
        thisParrentNode =""
        while(thisNode != ""):
            # Is this the node we are looking for?
            if(thisNode.name_.lower() == name_.lower()):
                # YES
                thisParrentNode = thisNode

            # Get next node
            thisNode = thisNode.getNextNode(startNode)
        
        # Has the node been found?
        if(thisParrentNode != ""):
            # NO
            self.error_ = "removeSubNodeObjByName: Unable to find node with name " + name_            
            return ""
        
        # Is node Ix valid?
        if(nodeIx_ < 0)|(nodeIx_ > thisParrentNode.subNodeCount_ - 1):
            # NO
            self.error_ = "removeSubNodeObjByName: Unable to find subNode with Ix " + str(nodeIx_)            
            return ""

        # Assume nodeIx is valid
        thisNode = thisParrentNode.subNodes_[nodeIx_]

        # Remove the SubNode
        thisParrentNode.subNodes_.remove(thisNode)

        # Update subNode Count
        thisParrentNode.subNodeCount_ -= 1

        # Fix ParrentNode and its entire sub-nodeTree
        thisParrentNode.updateSubNodeTreeNodeIds()

        return thisParrentNode

    # Remove subNode on thisNode & relative nodeIx
    def removeSubNodeObjByIx(self, nodeIx_=0):
        thisNode = self
        thisParrentNode = thisNode
                
        # Is node Ix valid?
        if(nodeIx_ < 0)|(nodeIx_ > thisParrentNode.subNodeCount_ - 1):
            # NO
            self.error_ = "removeSubNodeObjByIx: Unable to find subNode with Ix " + str(nodeIx_)            
            return ""

        # Assume nodeIx is valid
        thisNode = thisParrentNode.subNodes_[nodeIx_]

        # Remove the SubNode
        thisParrentNode.subNodes_.remove(thisNode)

        # Update subNode Count
        thisParrentNode.subNodeCount_ -= 1

        # Fix ParrentNode and its entire sub-nodeTree
        thisParrentNode.updateSubNodeTreeNodeIds()

        return thisParrentNode

#----------------------- Remove node Helper/Wrapper Methods ------------------
#----------------------- Remove node Helper Methods ----------------------    
    # Remove thisNode
    def removeNode(self):
        thisNode = self

        thisParrentNode = thisNode.removeNodeObj()

        return thisParrentNode

    # Remove node specified by Id, Search from thisNode to end of its sub-nodeTree
    def removeNodeById(self, nodeId_):
        thisNode = self

        thisParrentNode = thisNode.removeNodeObjById(nodeId_)

        return thisParrentNode

    # Remove node specified by name, Search from thisNode to end of its sub-nodeTree
    def removeNodeByName(self, name_):
        thisNode = self

        thisParrentNode = thisNode.removeNodeObjByName(name_)

        return thisParrentNode    
#------------------ REMOVE peerNode Helper/Wrapper Methods --------------------------

    # Remove peerNode relative to node specified Id, Search from thisNode to end of its sub-nodeChain
    def removePeerNodeById(self, nodeId_):
        thisNode = self

        thisParrentNode = thisNode.removePeerNodeObjById(nodeId_)

        return thisParrentNode

	# Remove peerNode relative to node specified name, Search from thisNode to end of its sub-nodeChain
    def removePeerNodeByName(self, name_):
        thisNode = self

        thisParrentNode = thisNode.removePeerNodeObjByName(name_)

        return thisParrentNode        
		
    # Remove peerNode on same parrentNode/nodeChain as thisNode & relative nodeIx
    def removePeerNodeByIx(self, nodeIx_=0):
        thisNode = self

        thisParrentNode = thisNode.removePeerNodeObjByIx(nodeIx_)

        return thisParrentNode
		
#------------------ Remove subNode Helper/Wrapper Methods -----------------
    # Remove subNode on thisNode & relative at nodeIx
    def removeSubNode(self, nodeIx_=0):
        thisNode = self

        thisParrentNode = thisNode.removeSubNodeObj(nodeIx_)

        return thisParrentNode        
	
	# Remove subNode on node specified by Id relative to node specified by Ix, Search from thisNode to end of its sub-nodeTree
    def removeSubNodeById(self, nodeId_, nodeIx_=0):
        thisNode = self

        thisParrentNode = thisNode.removeSubNodeObjById(nodeId_, nodeIx_)

        return thisParrentNode        

    # Remove subNode on node specified by name relative to node specified by Ix, Search from thisNode to end of its sub-nodeTree
    def removeSubNodeByName(self, name_, nodeIx_=0):
        thisNode = self

        thisParrentNode = thisNode.removeSubNodeObjByName(name_, nodeIx_)

        return thisParrentNode        
	
    # Remove subNode on thisNode & relative nodeIx
    def removeSubNodeByIx(self, nodeIx_=0):
        thisNode = self

        thisParrentNode = thisNode.removeSubNodeObjByIx(nodeIx_)

        return thisParrentNode        
	
#---------------- node Searching & Navigation Methods -------------------        

    # returns thisNodes peerNode specified by nodeIx if it has one
    def getPeerNodeByIx(self, nodeIx_=0):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        #Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => rootNode does not have peerNodes
            self.error_ = "getPeerNodeByIx: rootNodes dont have peerNodes!!"            
            return ""

        # Is this nodeIx valid?
        if(nodeIx_ > thisParrentNode.subNodeCount_ - 1): # Remember binary math!!
            # NO => invalid nodeIx, ret nothing
            self.error_ = "getPeerNodeByIx: Unable to find node with Ix " + str(nodeIx_)
            return ""
        
        # Assume the node ix is valid
        thisNode = thisParrentNode.subNodes_[nodeIx_]
        
        return thisNode

    # returns thisNodes subNode specified by nodeIx if it has one
    def getSubNodeByIx(self, nodeIx_=0):
        thisNode = self

        #Is this leafNode?
        if(thisNode.subNodeCount_ == 0):
            # YES => leafNodes does not have subNodes
            self.error_ = "getSubNodeByIx: leafNodes does not have subNodes "            
            return ""

        # Is this nodeIx valid?
        if(nodeIx_ < 0)|(nodeIx_ > thisNode.subNodeCount_ - 1): # Remember Binary math!!
            # NO => invalid nodeIx, ret nothing
            self.error_ = "getSubNodeByIx: Unable to find node with Ix " + str(nodeIx_)            
            return ""
        
        # Assume node ix is valid
        # Get the subNode
        thisNode = thisNode.subNodes_[nodeIx_]
        
        return thisNode

    # returns thisNodes next-peerNode if it has one
    def getNextPeerNode(self):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        # Is this rootNode?
        if(thisNode.parrentNode_ ==""):
            # YES => Root node does not have peer nodes, ret nothing
            self.error_ = "getNextPeerNode: rootNodes dont have peerNodes"            
            return ""

        # Assume this node does have peerNodes
        # Is this last-node in this sub-nodeChain?
        if(thisNode.nodeIx_ >= thisParrentNode.subNodeCount_ - 1): #Remember its Binary count so array->lastIx = array->size - 1
            # YES => No more peerNodes in this sub-nodeChain
            self.error_ = "getNextPeerNode: no next peerNode found"            
            return ""

        # Assume there are more peerNodes
        # Get next peerNode
        thisNode = thisParrentNode.subNodes_[thisNode.nodeIx_+1]
        
        return thisNode

    # returns thisNodes prev-peerNode if it has one
    def getPrevPeerNode(self):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        # Is this rootNode?
        if(thisNode.parrentNode_ ==""):
            # YES => Root node does not have peer nodes, ret nothing
            self.error_ = "getPrevPeerNode: rootNodes dont have peerNodes"
            return ""

        # Assume this node does have peerNodes
        # Is this first-node in this sub-nodeChain?
        if(thisNode.nodeIx_ <= 0):
            # No more prev peerNodes in this sub-nodeChain
            self.error_ = "getPrevPeerNode: no previous peerNode found"            
            return ""

        # Assume there are more prev-peerNodes
        # Get prev peerNode
        thisNode = thisParrentNode.subNodes_[thisNode.nodeIx_-1]
        
        return thisNode

    # Return the nextNode if all nodes hassent been looked-through
    # use startNode_ if you want to restrict search to a specific node and its sub-nodeTree
    def getNextNode(self, startNode_=""):
        thisNode = self

        # Has node travesal/look-through been restricted to a specific node and its sub-nodeTree?
        if(startNode_ != ""):
            # Has sub-nodeTree been been looked-through?
            if(thisNode.nodeLevel_ == startNode_.nodeLevel_):
                if(thisNode != startNode_):
                    # YES => Tree read complete
                    return ""
            # is thisNode on a higher nodeLevel then startNode?
            if(thisNode.nodeLevel_ < startNode_.nodeLevel_):
                # YES => Tree read complete
                return ""

        # is thisNode a leafNode?
        if(thisNode.subNodeCount_ != 0):
            # NO
#-----------------------------------------------------------------------------            
#**            thisNode = thisNode.getFirstSubNode() # In-line for speed
#-----------------------------------------------------------------------------
            thisNode = thisNode.subNodes_[0]
#--------------------------------------------------------------------------------                
            return thisNode
        else: # Assume no more subNode or leafNode
            # YES => Get next valid node
            while(True):
                # Has node travesal/look-through been restricted to a specific node and its sub-nodeTree?
                if(startNode_ != ""):
                    # YES => Has sub-nodeTree been been looked-through?
                    # is thisNode on same nodeLevel as startNode?
                    if(thisNode.nodeLevel_ == startNode_.nodeLevel_):
                        # YES
                        #  Is thisNode the startNode?
                        if(thisNode != startNode_):
                            # NO => Tree read complete
                            return ""

                    # Is thisNodes at a higher nodeLevel then startNode?
                    if(thisNode.nodeLevel_ < startNode_.nodeLevel_):
                        # YES => Tree read complete
                        return ""

                # Keep Track of thisNode
                prevNode = thisNode
#------------------------------------------------------------------------------------              
#**                thisNode = thisNode.getNextPeerNode() # In-line for speed
#------------------------------------------------------------------------------------
                thisParrentNode = thisNode.parrentNode_
                # Is this rootNode?
                if(thisParrentNode != ""):
                    # NO
                    lastSubNode = thisParrentNode.subNodes_[thisParrentNode.subNodeCount_ - 1]
                    # Is thisNode the last subNode?
                    if(thisNode != lastSubNode): # Remember binary math!!
                        # NO
                        thisNode = thisParrentNode.subNodes_[thisNode.nodeIx_+1]
                    else:
                        # YES
                        thisNode = ""
                else:
                    # YES
                    thisNode=""
#-------------------------------------------------------------                    
                # Is thisNode valid?
                if(thisNode != ""):
                    # YES
                    return thisNode
                else: 
                    # NO => Restore prevNode state
                    thisNode = prevNode
                    # Assume no more peerNode on this sub-nodeTree
                    # Is thisNodes Parrent startNode?
                    # Has startNode been specified?
                    if(startNode_ != ""):
                        # YES
                        # Is thisNodes parrentNode the startNode?
                        if(thisNode.parrentNode_ == startNode_):
                            # YES => Tree read complete
                            return ""
#--------------------------------------------------------------------------                        
#**                    thisNode = thisNode.getNextParrentNode() # In-lined for speed
#-----------------------------------------------------------------------------------------
                    thisParrentNode = thisNode.parrentNode_
                    thisGrandParrentNode = thisParrentNode.parrentNode_
                    # Does thisNode have a grandParrentNode?
                    if(thisGrandParrentNode != ""):
                        # YES
                        lastParrentNode = thisGrandParrentNode.subNodes_[thisGrandParrentNode.subNodeCount_ - 1]
                        # is thisNodes parrentNode the last parrentNode?
                        if(thisParrentNode != lastParrentNode): # Remember binary math!!
                            # NO
                            thisNode = thisGrandParrentNode.subNodes_[thisParrentNode.nodeIx_+1]
                        else:
                            # YES
                            thisNode = ""
                    else:
                        # NO
                        thisNode=""
#------------------------------------------------------------------------------------------                    
                    # Is thisNode valid?
                    if(thisNode != ""):
                        # YES
                        return thisNode
                    else:
                        # NO => Restore prevNode state
                        thisNode = prevNode

                    # Is this rootNode?
                    if(thisNode.parrentNode_ == ""):
                        # YES => This is root node, no more nodes to read
                        return ""
                    else:
                        # NO => Has last node been been read?
                        thisParrentNode = thisNode.parrentNode_
                        # Is thisNode a subNode of root?
                        if(thisNode.nodeLevel_ == 1):
                            # YES
                            lastSubNode = thisParrentNode.subNodes_[thisParrentNode.subNodeCount_ - 1]
                            # Is thisNode the last subNode?
                            if(thisNode == lastSubNode):
                                # YES => Last node has been read
                                return ""
                        else:
                            # NO
                            # Is startNode the rootNode?
                            if(startNode_.parrentNode_ == ""):
                                # YES
                                return ""

        
    def getParrentNode(self):
        # Get thisNodes parrentNode
        return self.parrentNode_

    def getSubNodeCount(self):
        return self.subNodeCount_

    def hasSubNodes(self):
        if self.subNodeCount_ > 0:
            return True
        else:
            return False

    def hasParrentNode(self):
        # Is this a rootNode?
        if self.parrentNode_ != "":
            # NO
            return True
        else: # YES => Assume this is rootNode
            return False

    # Returns wheter thisNode is root
    def isRootNode(self):
        # Is this the rootNode?
        if(self.parrentNode_ == ""):
            return True
        else:
            return False

    # Method that returns wheter thisNode is a leafNode
    def isLeafNode(self):
        # Is thisNode a leafNode?
        if(self.subNodeCount_ == 0):
            # YES
            return True
        else: # NO
            return False
            
    # Method used to go all the way back to rootNode
    def getRootNode(self):
        thisNode = self
        # Move up the nodeTree until rootNode is found
        while(thisNode.parrentNode_ != ""):
            thisNode = thisNode.parrentNode_
        return thisNode

    def setName(self, name_):        
        # Update the Node->name
        self.name_ = name_
        return True

    # Get the Node->name
    def getName(self):
        # Return the node->name
        return self.name_

    def setValue(self, value_):        
        # Update the Node->value
        self.value_ = value_
        return True

    # Get the Node->value
    def getValue(self):
        # Return the node->value
        return  self.getString(self.value_)

    # auto gen. new nodeId for non root nodes
    def genNodeId(self):
        # Ensure nodeId is not allready generated
        # Has thisNodes nodeId allready been specified?
        if(self.nodeId_ != ""):
            # YES
            self.error_ = "genNodeId: thisNode allready has a Id!!"
            return False

        # Is this root node?
        if(self.parrentNode_ == ""):
            # YES => Root node key cannot be changed forced exit
            return False

        # Generate and update new key "NodeId"        
        self.nodeId_ = self.parrentNode_.nodeId_ + self.nodeLevelSeparator_ + str(self.nodeIx_)
        return True

#------------------------ nodeId, ix, and Level methods, Ensures that a sub nodes location is always reflected by its Id, level, ix ----------
    # Auto update thisNodes and all its peerNodes nodeId & nodeLevels in case they have been corrupted by copy, insert or replace functions
    def updatePeerNodeIds(self):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        # Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => Root node key cannot be changed forced exit
            self.error_ = "updatePeerNodeIds: rootNodes dont have peerNodes!!"            
            return False
        
        # Generate & update NodeIds
        ix = 0
        for node in thisParrentNode.subNodes_:
            # Get next node
            # Fix node ix just in case it has been corrupted too
            node.nodeIx_ = ix
            node.nodeId_ = thisParrentNode.nodeId_ + node.nodeLevelSeparator_ + str(node.nodeIx_)
            # update thisNodes nodeLevel
            node.nodeLevel_ = node.getNodeLevel()

            # Update node ix
            ix += 1            
        
        # Return number of updated nodeIds
        return ix

    # Auto update thisNode & its subNodes nodeIds & nodeLevels in case they have been corrupted by copy, insert or replace functions
    def updateSubNodeIds(self):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        # Fix thisNode ix
        # Get Index
        ix = 0
        nodeFound = 0
        for node in thisParrentNode.subNodes_:
            # Is this the subNode we are looking for?
            if(thisNode == node):
                # YES => Ensure thisNode points to the subNode
                thisNode = node
                # node found, signal it
                nodeFound = 1
                break

            # Update node ix
            ix += 1

        # Was the node found?
        if(nodeFound):
            # YES => Update index, nodeId & nodeLevel
            thisNode.nodeIx_ = ix
            thisNode.nodeId_ = thisParrentNode.nodeId_ + thisNode.nodeLevelSeparator_ + str(thisNode.nodeIx_)
            thisNode.nodeLevel_ = thisNode.getNodeLevel()

            # Has value frequency been initialized?
            if(thisNode.freq_ == 0):
                thisNode.freq_ = 1
        else:
            # Unable to locate the node in parrentNodes subNodes
            self.error_ = "updateSubNodeIds: Unable to locate thisNode in parrentNode sub-nodeChain!!"
            return ""

        # Is thisNode as leafNode?
        if(thisNode.subNodeCount_ == 0):
            # YES => leafNodes does not have subNodes!!
            self.error_ = "updateSubNodeIds: leafNodes does not have subNodes!!"
            return ""

        # Generetae & update all thisNodes subNodes nodeId
        ix = 0
        for node in thisNode.subNodes_:
            # Fix node ix just in case it has been corrupted too
            node.nodeIx_ = ix            
            # Generate and update new NodeId        
            node.nodeId_ = thisNode.nodeId_ + node.nodeLevelSeparator_ + str(node.nodeIx_)
            # update thisNodes nodeLevel
            node.nodeLevel_ = node.getNodeLevel()
            # Has value frequency been initialized?
            if(node.freq_ == 0):
                node.freq_ = 1

            # Update node ix
            ix += 1

        return ix

    # Update thisNode & its sub-nodeTrees nodesIds & Levels in case they have been corrupted by moving nodes around
    def updateSubNodeTreeNodeIds(self):
        thisNode = self
        startNode = thisNode.parrentNode_ # Must be from parrent to detect when the thisNodes sub-nodeTree has been looked-through

        # look-through thisNodes sub-nodeTree
        while(thisNode != ""):
            # Fix thisNodes subNodeIds
            thisNode.updateSubNodeIds()

            # Get next node
            thisNode = thisNode.getNextNode(startNode)

        return self 

    # Update the subNodes parrentNode association/linking to thisNode, to ensure they have
    # thisNode as parrentNode. Usefull after parrentNode change after copy, insert, replace actions on nodes
    def updateParrentNodeLink(self):
        thisNode = self

        # Is this a leafNode?
        if(thisNode.subNodeCount_ == 0):
            # YES => leafNodes does not have subNodes
            self.error_ = "updateParrentNodeLink: leafNodes dont have subNodes!!"            
            return ""

        # look-through thisNodes subNodes/sub-nodeChain
        for node in thisNode.subNodes_:
            # fix subNodes association/link to parrentNode
            node.parrentNode_ = thisNode

        return thisNode    
#-------------------------------------------        

    def getNodeId(self):
        # Return this nodes NodeId
        return self.nodeId_

# ----- Analysis functionality ------

#------------------------------------

    # Swaps thisNode and its sub-nodeTree with otherNode and its sub-nodeTree
    # usefull when sorting by freq
    def swapNodes(self, otherNode_):
        thisNode = self
        
        thisParrentNode = thisNode.parrentNode_
        otherParrentNode = otherNode_.parrentNode_
        
        # Is this rootNode?
        if((thisParrentNode == "") | (otherParrentNode == "")):
            # YES => rootNodes cannot be replaced
            self.error_ = "swapNodes: rootNodes cannot be replaced!!"            
            return ""

        # Create copies of the nodes to swap # NOTE: MUST BE COPIES & NOT ORG SINCE THE ORG NODES ARE LOST ON FIRST NODE "REPLACE"
        nodeA = thisNode.copyNode()
        nodeB = otherNode_.copyNode()            

        # Get nodeIx of the nodes to swap # NOTE: MUST be ix copies since the Org node->nodeIx's are swapped!!
        ixA = nodeA.nodeIx_
        ixB = nodeB.nodeIx_
        
        # Swap the parrentNodes (fix parrent association/linking)
        nodeA.parrentNode_ = otherParrentNode
        nodeB.parrentNode_ = thisParrentNode

        # Swap the subNodes NOTE: For some reason node cannot be swapped unless its directly accessed in the array :O
        thisParrentNode.subNodes_[ixA] = nodeB
        otherParrentNode.subNodes_[ixB] = nodeA

        # Fix nodeIds for the swapped nodes and their sub-nodeTree
        thisParrentNode.subNodes_[ixA].updateSubNodeTreeNodeIds()
        otherParrentNode.subNodes_[ixB].updateSubNodeTreeNodeIds()
                
        return thisParrentNode.subNodes_[ixA]
        
    # Swaps thisNode sub-nodeTree with otherNodes sub-nodeTree
    # usefull when sorting by freq
    def swapSubNodes(self, otherNode_):
        thisNode = self
        
        thisParrentNode = thisNode.parrentNode_
        otherParrentNode = otherNode_.parrentNode_
        
        # Is this rootNode?
        if((thisParrentNode == "") | (otherParrentNode == "")):
            # YES => rootNodes cannot be replaced
            self.error_ = "swapSubNodes: rootNodes cannot be replaced!!"            
            return ""

        # Create copies of the nodes to swap NOTE: MUST BE COPIES SINCE THE ORG. NODES ARE LOST ON FIRST "REPLACE"
        nodeA = thisNode.copyNode()
        nodeB = otherNode_.copyNode()            
        
        # Swap the sub-nodeTrees
        thisNode.subNodes_ = nodeB.subNodes_
        thisNode.subNodeCount_ = nodeB.subNodeCount_

        otherNode_.subNodes_ = nodeA.subNodes_
        otherNode_.subNodeCount_ = nodeA.subNodeCount_

        # Fix parrentNode assocation/linking for thisNode
        for node in thisNode.subNodes_:
            node.parrentNode_ = thisNode

        # Fix parrentNode association/linking for otherNode
        for node in otherNode_.subNodes_:
            node.parrentNode_ = otherNode_

        # Fix nodeIds for the swapped nodes and their sub-nodeTree
        thisNode.updateSubNodeTreeNodeIds()
        otherNode_.updateSubNodeTreeNodeIds()
                
        return thisNode

    # Removes all peerNodes in the nodeChain, thisNode exist in
    def removePeerNodes(self):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        # Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => rootNode does not have peerNodes
            self.error_ = "removePeerNodes: rootNodes dont have peerNodes & rootNodes cannot be removed!!"            
            return ""
    
        # Remove all subNodes "destroy sub-nodeChain"
        thisParrentNode.subNodes_ = []
        thisParrentNode.subNodeCount_ = 0

        return thisParrentNode

    # Removes thisNodes subNodes if it has any
    def removeSubNodes(self):
        thisNode = self

        # Is this leafNode?
        if(thisNode.subNodeCount_ == 0):
            # YES => leafNodes have no subNodes
            self.error_ = "removeSubNodes: leafNodes dont have subNodes!!"            
            return ""

        # Remove all subNodes "destroy sub-nodeChain"
        thisNode.subNodes_ = []
        thisNode.subNodeCount_ = 0        

        return thisNode

    # Sorts thisNodes & its peerNodes by frequency def. least freq to most freq "Ready for Anormalie detection"
    def sortPeerNodesByFreq(self, sortOrder_=0):
        thisNode = self
        thisParrentNode = thisNode.parrentNode_

        # Is this rootNode?
        if(thisNode.parrentNode_ == ""):
            # YES => rootNode has no peerNodes
            self.error_ = "sortPeerNodesByFreq: rootNodes dont have peerNodes!!"            
            return ""

        # Sort the peerNodes by freq
        sortCount = 0
        for subNodeA in thisParrentNode.subNodes_: # Rember binary math!!
            for subNodeB in thisParrentNode.subNodes_[subNodeA.nodeIx_:]:        
                
                # Sort least to most freq?
                if(sortOrder_ == 1):
                    # is subNodeB more freq then subNodeA?
                    if(subNodeB.freq_ > subNodeA.freq_):
                        # swap the two nodes
                        subNodeA = subNodeA.swapNode(subNodeB)
                        sortCount += 1
                else: # Assume sort most to least freq?
                    # is subNodeB less freq then subNodeA?
                    if(subNodeB.freq_ < subNodeA.freq_):
                        # swap the two nodes, and get the new subNodeA
                        subNodeA = subNodeA.swapNode(subNodeB)
                        sortCount += 1

        # Fix parrentNode and its sub-nodeTrees NodeId's
        thisParrentNode.updateSubNodeTreeNodeIds()                    

        # return number of nodes sorted
        return sortCount

    # Sorts thisNodes subNodes by frequency def. least freq to most freq "Ready for Anormalie detection"
    def sortSubNodesByFreq(self, sortOrder_=0):
        thisNode = self

        # Is this leafNode?
        if(thisNode.subNodeCount_ == 0):
            # YES => leafNodes has no subNodes
            self.error_ = "sortSubNodesByFreq: leafNodes dont have subNodes!!"            
            return ""

        # Sort thisNodes subNodes/sub-nodeChain by frequency "match count"
        sortCount = 0
        for subNodeA in thisNode.subNodes_: # Rember binary math!!
            for subNodeB in thisNode.subNodes_[subNodeA.nodeIx_:]:
                
                # Sort least to most freq?
                if(sortOrder_ == 1):
                    # is subNodeB more freq then subNodeA?
                    if(subNodeB.freq_ > subNodeA.freq_):
                        # swap the two nodes
                        subNodeA = subNodeA.swapNodes(subNodeB)
                        sortCount += 1
                else: # Assume sort most to least freq?
                    # is subNodeB less freq then subNodeA?
                    if(subNodeB.freq_ < subNodeA.freq_):
                        # swap the two nodes
                        subNodeA = subNodeA.swapNodes(subNodeB)
                        sortCount += 1

        # Fix thisNode & its sub-nodeTree nodeIds
        thisNode.updateSubNodeTreeNodeIds()                    

        # return number of nodes sorted
        return sortCount

#--------------------- COPY node Methods ----------------------
    # Returns a copy of thisNode and its entire sub-nodeTree
    def copyNode(self):
        thisNode = self
        startNode = thisNode
        
        # Create new nodeTree
        nodeTreeCopy = analysisNodeTree(thisNode.name_, thisNode.value_, thisNode.parrentNode_, thisNode.nodeLevelSeparator_)
        thatNode = nodeTreeCopy

        # Copy thisNode attributes one-by-one to copy of node to ensure they have correct values
        nodeTreeCopy.nodeId_ = thisNode.nodeId_ # No need handled by constructor
        nodeTreeCopy.nodeIx_ = thisNode.nodeIx_ # No need handled by construtor when parrentNode is known
        nodeTreeCopy.nodeLevel_ = thisNode.nodeLevel_ # No need handled by constructor
        nodeTreeCopy.freq_ = thisNode.freq_
        nodeTreeCopy.uniqueLevel_ = thisNode.uniqueLevel_
        
        # Does thisNode hav subNodes?
        if(thisNode.subNodeCount_ == 0):
            # NO => No sub nodes to copy just return copy of this node
            return nodeTreeCopy

        # Keep track of prev node
        prevNode = thisNode
        # Get First node of sub-nodeTree
        thisNode = thisNode.getNextNode(startNode)

        # Copy sub-nodeTree node-by-node
        while(thisNode != ""):
                    
            # Is next node a peerNode?
            if(thisNode.nodeLevel_ == prevNode.nodeLevel_):
                # YES => Add new peerNode
                thatNode = thatNode.addPeerNode(thisNode.name_, thisNode.value_)

            # is next node a subNode?
            if(thisNode.nodeLevel_ > prevNode.nodeLevel_):
                # YES => add new subNode
                thatNode = thatNode.addSubNode(thisNode.name_, thisNode.value_)

            # is next node parrentNode?
            if(thisNode.nodeLevel_ < prevNode.nodeLevel_):
                # YES => add parrentNode
                thatNode = thatNode.parrentNode_
                thatNode = thatNode.addPeerNode(thisNode.name_, thisNode.value_)

            # Keep track of prev node
            prevNode = thisNode
            # Get Next node
            thisNode = thisNode.getNextNode(startNode)

        # Return copy of the node and its sub-nodeTree
        return nodeTreeCopy

    # Returns a copy of thisNodes sub-nodeTree
    # basically the same as CopyNode except this one makes rootNode a standard root node
    def copySubNodes(self):
        thisNode = self
        startNode = thisNode
        
        # Create new nodeTree
        nodeTreeCopy = analysisNodeTree("", "", "", thisNode.nodeLevelSeparator_)
        thatNode = nodeTreeCopy

        # Does thisNode hav subNodes?
        if(thisNode.subNodeCount_ == 0):
            # NO => No sub nodes to copy just return copy of this node
            return nodeTreeCopy

        # Keep track of prev node
        prevNode = thisNode
        # Get First node of sub-nodeTree
        thisNode = thisNode.getNextNode(startNode)

        # Copy sub-nodeTree node-by-node
        while(thisNode != ""):
                    
            # Is next node a peerNode?
            if(thisNode.nodeLevel_ == prevNode.nodeLevel_):
                # YES => Add new peerNode
                thatNode = thatNode.addPeerNode(thisNode.name_, thisNode.value_)

            # is next node a subNode?
            if(thisNode.nodeLevel_ > prevNode.nodeLevel_):
                # YES => add new subNode
                thatNode = thatNode.addSubNode(thisNode.name_, thisNode.value_)

            # is next node parrentNode?
            if(thisNode.nodeLevel_ < prevNode.nodeLevel_):
                # YES => add parrentNode
                thatNode = thatNode.parrentNode_
                thatNode = thatNode.addPeerNode(thisNode.name_, thisNode.value_)

            # Keep track of prev node
            prevNode = thisNode
            # Get Next node
            thisNode = thisNode.getNextNode(startNode)

        # Return copy of the node and its sub-nodeTree
        return nodeTreeCopy

#-------------------------------------------------        

# --------------------- Simi Recursive sub-nodeTree readering ----------------
    # Reads node in thisNodes sub-nodeTree node-by-node
    # Uses all nodeTree methods so it abit slow due to alot of function calls
    # Just a demonstartion of how the nodeTree can be looked-through using its methods
    def getNextNodeInSubNodeTree(self, startNode_):
        thisNode = self

        # Has sub-nodeTree been been looked-through?
        if(thisNode.nodeLevel_ == startNode_.nodeLevel_):
            if(thisNode.nodeId_ != startNode_.nodeId_):
                # YES => Tree read complete
                return ""
        if(thisNode.nodeLevel_ < startNode_.nodeLevel_):
            # YES => Tree read complete
            return ""

        # does this node have subNodes?
        if(thisNode.subNodeCount_ != 0):
            # YES => get first subNode
            thisNode = thisNode.getFirstSubNode()
            return thisNode
        else: # Assume no more subNode or leafNode
            # Get next valid node
            while(True):
                # Has sub-nodeTree been been read?
                if(thisNode.nodeLevel_ == startNode_.nodeLevel_):
                    if(thisNode.nodeId_ != startNode_.nodeId_):
                        # YES => Tree read complete
                        return ""
                if(thisNode.nodeLevel_ < startNode_.nodeLevel_):
                    # YES => Tree read complete
                    return ""

                # Keep Track of thisNode
                prevNode = thisNode
                thisNode = thisNode.getNextPeerNode()
                # Is thisNode valid?
                if(thisNode != ""):
                    # YES
                    return thisNode
                else:
                    # NO => Restore prevNode state
                    thisNode = prevNode
                    # Assume no more peerNode on this sub-nodeTree
                    # Is thisNodes parrentNode the startNode?
                    if(thisNode.parrentNode_ == startNode_):
                        # YES => Tree read complete
                        return ""
                    else: # NO
                        thisNode = thisNode.getNextParrentNode()
                    # Is thisNode valid?
                    if(thisNode != ""):
                        # YES
                        return thisNode
                    else:
                        # NO => Restore prevNode state
                        thisNode = prevNode

#-----------------------------
    # Method designed to return any/unknown data type as a string
    # Usefull when dealing with dynamic Attributes Types
    def getString(self, data_):
        # Test the value type using Exceptions
        try:
            thisData = "" + data_
            
            # The data is a string s just return it
            return data_
        finally: # Assume the value is a number
            # Convert it to string and return it
            thisData = str(data_)
            return thisData