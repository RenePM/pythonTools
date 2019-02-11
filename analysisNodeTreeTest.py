import analysisNodeTree


def autoNodeIdTest():
    # Create a node test-tree
    # Root node NO parrent!!
    myRootNode = analysisNodeTree.analysisNodeTree("", "root")

    # Under root all most have parrent node
    # Manaual Tree creation test
    myNode = myRootNode.addSubNode("", "2")
    myNode.addSubNode("", "value A")
    myNode.addSubNode("", "value B")
    myRootNode.addSubNode("", "0")
    myRootNode.addSubNode("", "0")
    myRootNode.addSubNode("", "0")
    myRootNode.addSubNode("", "0")

    # Test dynamic dataType handling Works but dynamicData handling is not fully implemented
    #**newNode = myRootNode.addSubNode("", 10)
    #**thisValue = newNode.getValue()

    # Start the recursive process by setting root-node (OK)
    thisNode = myRootNode
    while(1):

        if thisNode == "":
            print("nodeTree Read complete...")
            break
        else:
            print("Node found: " + "key: " + thisNode.getNodeId() + " value: " + thisNode.getValue())

        # Get next node
        thisNode = thisNode.getNextNodeInSubNodeTree(myRootNode)

    # Test Restircted to sub-nodeTree (OK)
    thisNode = myNode
    while(1):

        if thisNode == "":
            print("nodeTree Read complete...")
            break
        else:
            print("Node found: " + "key: " + thisNode.getNodeId() + " value: " + thisNode.getValue())

        # Get next node
        thisNode = thisNode.getNextNodeInSubNodeTree(myNode)    

    thisNode = myRootNode
    while(1):

        if thisNode == "":
            print("nodeTree Read complete...")
            break
        else:
            print("Node found: " + "key: " + thisNode.getNodeId() + " value: " + thisNode.getValue())

        # Get next node
        thisNode = thisNode.getNextNode()

    # Test restircted to sub-nodeTree look-thorugh (OK)
    thisNode = myNode
    while(1):

        if thisNode == "":
            print("nodeTree Read complete...")
            break
        else:
            print("Node found: " + "key: " + thisNode.getNodeId() + " value: " + thisNode.getValue())

        # Get next node
        thisNode = thisNode.getNextNode(myNode)

    thisNode = myRootNode
        
    thisNode = thisNode.findNodeById("root.2")
    print("KeyValuesRemoved: " + thisNode.getValue())
    thisNode = thisNode.findPeerNodeById("root.0")
    thisNode = thisNode.findNodeById("root.0.1")
    print("KeyValuesRemoved: " + thisNode.getValue())
    thisNode = myRootNode.findNodeByValue("value B")
    print("KeyValuesRemoved: " + thisNode.getValue())

    # Test sub-nodeTree Swapping (OK)
    nodeA = myRootNode.findNodeById("root.3")
    nodeB = myRootNode.findNodeById("root.0")
    nodeA.swapSubNodes(nodeB)
    nodeA.swapSubNodes(nodeB) # Swap back again

    # Test node Swapping (OK)
    nodeA = myRootNode.findNodeById("root.3")
    nodeB = myRootNode.findNodeById("root.0")
    nodeA.swapNodes(nodeB)
    nodeA = myRootNode.findNodeById("root.3")
    nodeB = myRootNode.findNodeById("root.0")
    nodeA.swapNodes(nodeB) # Swap back again    

    # Test copy (OK)
    nodeC = myRootNode.copyNode()
    nodeD = myRootNode.copySubNodes()

    # Test insert "node insert uses same method at add rel"
    # Odd thisNode in this script somehow gets changed when used in nodeTree class script 
    # So parrentNode link points at the myRootNode copy :O
    # Get this thisNode back on track (point at node in myRootNode) # fixed using prcise ix of subNodes in parrentNodes sub-nodeChain
    thisNode = myRootNode.findNodeByValue("value B")

    # Test insert by value peerNode realtive to thisNode (OK)
    thisNode.insertPeerNode("inserted node value", "inserted node value")
    
    # Test "insert" peerNode by Object relative to thisNode (OK)
    nodeF = analysisNodeTree.analysisNodeTree("inserted peerNode obj", "inserted peerNode obj")
    thisNode = myRootNode.findNodeById("root.0.0")
    thisNode.insertPeerNodeObj(nodeF)

    # Test insert subNode by value relative to nodeIx (OK)
    thisNode.insertSubNode(0, "inserted subNode value", "inserted subNode value")

    # Test insert subNode by object relative to nodeIx (OK)
    nodeG = analysisNodeTree.analysisNodeTree("inserted subNode obj", "inserted subNode obj")
    thisNode.insertSubNodeObj(0, nodeG)

    # Test replace (OK)
    
    # Test replace peerNode by Object (OK)
    nodeF = analysisNodeTree.analysisNodeTree("replaced peerNode obj", "replaced peerNode obj")
    thisNode = myRootNode.findNodeById("root.0.0")
    thisNode.replaceNodeObj(nodeF)

    # Test replace subNode by object (OK)
    nodeG = analysisNodeTree.analysisNodeTree("replaced subNode obj", "replaced subNode obj")
    thisNode = myRootNode.findNodeById("root.0.3")
    thisNode.replaceSubNodeTreeObj(nodeG)

    # Test move backward in peerNodes (OK)
    thisNode = myRootNode.findNodeById("root.2")
    while(thisNode != ""):
        thisNode = thisNode.getPrevPeerNode()

    # Test move forward in peerNodes (OK)
    thisNode = myRootNode.findNodeById("root.2")
    while(thisNode != ""):
        thisNode = thisNode.getNextPeerNode()

    # Test move backward in subNodes # NOT IMPLEMENTED YET
#**    thisNode = myRootNode
#**    someNode = myRootNode.findNodeById("root.2")
#**    while(someNode != ""):
#**        someNode = someNode.getPrevSubNodeByIx(someNode.nodeIx_)
        
    # Test move forward in subNodes
#**    thisNode = myRootNode
#**    someNode = myRootNode.findNodeById("root.2")
#**    while(someNode != ""):
#**        someNode = someNode.getNextSubNodeByIx(someNode.nodeIx_)


    # Test remove some subNode
    thisNode = myRootNode.findNodeById("root.0")
    thisNode = thisNode.removeSubNodeByIx(1)

    # Test remove thisNode
    thisNode = myRootNode.findNodeById("root.0.0")
    thisNode = thisNode.removeNode()

    # Test remove someNode # NOT IMPLEMENTED YET for PeerNodes
#**    thisNode = thisNode.findNodeById("root.0")
#**    thisNode = thisNode.removePeerNodeByIx(thisNode.nodeIx_ + 1)

    thisNode = myRootNode.addSubNode("sortedByFreq")
    thisNode.addSubNode("HELLO", "HELLO A", 1)
    thisNode.addSubNode("HELLO", "HELLO A", 1)
    thisNode.addSubNode("HELLO", "HELLO A", 1)
    thisNode.addSubNode("HELLO", "HELLO B", 1)
    thisNode.addSubNode("HELLO", "HELLO B", 1)
    thisNode.addSubNode("HELLO", "HELLO B", 1)
    thisNode.addSubNode("HELLO", "HELLO J", 1)
    thisNode.addSubNode("HELLO", "HELLO C", 1)
    thisNode.addSubNode("HELLO", "HELLO C", 1)
    thisNode.addSubNode("HELLO", "HELLO C", 1)
    thisNode.addSubNode("HELLO", "HELLO Ø", 1)
    thisNode.addSubNode("HELLO", "HELLO C", 1)
    thisNode.addSubNode("HELLO", "HELLO D", 1)
    thisNode.addSubNode("HELLO", "HELLO D", 1)
    thisNode.addSubNode("HELLO", "HELLO E", 1)
    thisNode.addSubNode("HELLO", "HELLO E", 1)
    thisNode.addSubNode("HELLO", "HELLO Z", 1)
    thisNode.addSubNode("HELLO", "HELLO Å", 1)
    thisNode.addSubNode("HELLO", "HELLO F", 1)

    thisNode = myRootNode.findNodeByName("sortedByFreq")
    sortedNodeTree = thisNode.sortSubNodesByFreq() # Almost working, dossent sort last array ix, so i need to fix this
    breakPoint = 1
    diffNodeTree = thisNode.getSubNodeValueDifferences(0,1)
    simiNodeTree = thisNode.getSubNodeValueSimilarities(0,1)
    compNodeTree = thisNode.getSubNodeValueFreqAnalysis(0, 1)
    breakPoint = 1



autoNodeIdTest()
# Create a node test-tree
# Root node NO parrent!!
myRootNode = analysisNodeTree.analysisNodeTree("root", "root")

# Under root all most have parrent node
# Manaual Tree creation test
myNode = myRootNode.addSubNode("keysAdded", "2")
myNode.addSubNode("keysAdded->ValueA", "value A")
myNode.addSubNode("keysAdded->ValueB", "value B")
myRootNode.addSubNode("keyValuesAdded", "0")
myRootNode.addSubNode("keysRemoved", "0")
myRootNode.addSubNode("keyValuesRemoved", "0")
myRootNode.addSubNode("keyValuesModified", "0")


# Start the recursive process by setting root-node
thisNode = myRootNode
while(1):

    if thisNode == "":
        print("nodeTree Read complete...")
        break
    else:
        print("Node found: " + "nodeId: " + thisNode.getNodeId() + " value: " + thisNode.getValue())

    # Get next node
    thisNode = thisNode.getNextNode()

thisNode = myRootNode
        
thisNode = thisNode.findNodeByName("keyValuesRemoved")
print("KeyValuesRemoved: " + thisNode.getValue())
thisNode = thisNode.findNodeByName("keysAdded->ValueB")
print("KeyValuesRemoved: " + thisNode.getValue())
thisNode = myRootNode.findNodeByValue("value B")
print("KeyValuesRemoved: " + thisNode.getValue())






