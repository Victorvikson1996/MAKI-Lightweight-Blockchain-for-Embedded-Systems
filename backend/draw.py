from graphviz import Digraph

def draw_working_mechanism():
    dot = Digraph(comment='Working Mechanism')
    
    # Block Proposer Selection
    dot.node('A', 'Block Proposer Selection\n(Simplified VRF)')
    
    # Block Creation
    dot.node('B', 'Block Creation\n(Proposer creates block with header, transactions, and signature)')
    
    # Block Propagation
    dot.node('C', 'Block Propagation\n(Block propagated to the network)')
    
    # Soft Vote Phase
    dot.node('D', 'Soft Vote Phase\n(Committee of nodes votes on best block proposal)')
    
    # Certify Vote Phase
    dot.node('E', 'Certify Vote Phase\n(Committee verifies protocol adherence)')
    
    # Block Finalization
    dot.node('F', 'Block Finalization\n(Verified block added to mini-blockchain)')
    
    # Binary Radix Trie
    dot.node('G', 'Binary Radix Trie for Transactions\n(Optimizes space and search efficiency)')
    
    # Connections
    dot.edges(['AB', 'BC', 'CD', 'DE', 'EF'])
    dot.edge('F', 'G', label='Transactions organized in binary radix trie')
    
    # Render the diagram
    dot.render('working_mechanism_diagram', format='png', view=True)

# Draw the diagram
draw_working_mechanism()
