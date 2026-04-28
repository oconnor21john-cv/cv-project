"""
Enhanced Network Diagram Generator - Easy to Read
Simple version with clean text labels
"""

try:
    from graphviz import Digraph
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False

from pathlib import Path


def create_easy_read_diagram():
    """Generate easy-to-read IPv4 network diagram"""
    if not GRAPHVIZ_AVAILABLE:
        print("Graphviz not available")
        return None
        
    dot = Digraph(comment='IPv4 Network - Easy Read', format='png')
    
    # Better layout - LR for horizontal flow with ISP in middle
    dot.attr(rankdir='LR',
             splines='polyline',
             nodesep='0.8',
             ranksep='2.5',
             bgcolor='white',
             pad='0.75',
             fontname='Arial')
    
    dot.attr('node', fontname='Arial Bold', fontsize='11')
    dot.attr('edge', fontname='Arial', fontsize='9')
    
    # Colors
    router_color = '#1565C0'
    switch_color = '#0277BD'
    vlan_color = '#B3E5FC'
    isp_color = '#212121'
    
    # ISP - Will be positioned in the middle
    with dot.subgraph(name='cluster_isp') as isp:
        isp.attr(label='ISP AREA\nPublic IPs',
                style='filled,dashed',
                color='black',
                fillcolor='#E0E0E0',
                penwidth='3',
                fontsize='14',
                rank='same')  # Keep ISP at same rank
        
        isp.node('ISP',
                label='ISP ROUTER\n\nG1/1/1: .22 (R1)\nG1/1/2: .30 (R11)\nG1/1/3: .26 (R7)\n\n203.0.113.0/24',
                shape='cylinder',
                fillcolor=isp_color,
                fontcolor='white',
                style='filled',
                width='2.5',
                height='1.8')
    
    # AREA 1
    with dot.subgraph(name='cluster_area1') as area1:
        area1.attr(label='AREA 1: CLASS B\n172.16.0.0/16',
                  style='filled,dashed',
                  color='#1565C0',
                  fillcolor='#E3F2FD',
                  penwidth='4',
                  fontsize='14')
        
        area1.node('R1', 'R1\n\nG0/0: .6\nG0/2: .9\nG1/1/1: .21',
                  shape='box', style='filled,rounded', fillcolor=router_color, fontcolor='white', width='1.5')
        area1.node('R3', 'R3\n\nVLAN 4: 172.16.0.1\nVLAN 5: 172.16.7.1\nP2P: .1, .18',
                  shape='box', style='filled,rounded', fillcolor=router_color, fontcolor='white', width='1.8')
        area1.node('R4', 'R4\n\nG0/0: .5\nG0/1: .2',
                  shape='box', style='filled,rounded', fillcolor=router_color, fontcolor='white', width='1.3')
        area1.node('R5', 'R5\n\nG0/0: .10\nG0/1: .13',
                  shape='box', style='filled,rounded', fillcolor=router_color, fontcolor='white', width='1.3')
        area1.node('R6', 'R6\n\nG0/0: .14\nVLAN 2&3\nTrunk',
                  shape='box', style='filled,rounded', fillcolor=router_color, fontcolor='white', width='1.3')
        
        area1.node('S2', 'S2', shape='box', style='filled', fillcolor=switch_color, fontcolor='white')
        area1.node('S3', 'S3\nTrunk', shape='box', style='filled', fillcolor=switch_color, fontcolor='white')
        
        area1.node('VLAN4', 'VLAN 4\n172.16.0.0/22\n1024 hosts',
                  shape='note', style='filled', fillcolor=vlan_color)
        area1.node('VLAN5', 'VLAN 5\n172.16.7.0/30\n2 hosts',
                  shape='note', style='filled', fillcolor=vlan_color)
        area1.node('VLAN2', 'VLAN 2\n172.16.4.0/23\n400 hosts',
                  shape='note', style='filled', fillcolor=vlan_color)
        area1.node('VLAN3', 'VLAN 3\n172.16.6.0/24\n250 hosts',
                  shape='note', style='filled', fillcolor=vlan_color)
    
    # AREA 2
    with dot.subgraph(name='cluster_area2') as area2:
        area2.attr(label='AREA 2: CLASS C\n192.168.0.0/16',
                  style='filled,dashed',
                  color='#388E3C',
                  fillcolor='#E8F5E9',
                  penwidth='4',
                  fontsize='14')
        
        area2.node('R7', 'R7\n\nG0/0: .25 (ISP)\nG0/1: .33\nVLAN 400: .0.1',
                  shape='box', style='filled,rounded', fillcolor=router_color, fontcolor='white', width='1.6')
        area2.node('R8', 'R8\n\nG0/0: .34\nG0/1: .37\nVLAN 100: .0.33\nVLAN 200: .0.49',
                  shape='box', style='filled,rounded', fillcolor=router_color, fontcolor='white', width='1.6')
        area2.node('R9', 'R9\n\nG0/0: .41\nG0/1: .38',
                  shape='box', style='filled,rounded', fillcolor=router_color, fontcolor='white', width='1.3')
        area2.node('R10', 'R10\n\nG0/0: .42\nVLAN 300: .0.65',
                  shape='box', style='filled,rounded', fillcolor=router_color, fontcolor='white', width='1.4')
        area2.node('R2', 'R2\nBORDER ROUTER\n\nG0/0: .17 (Area1)\nVLAN 1: .0.73',
                  shape='box', style='filled,rounded', fillcolor='#7B1FA2', fontcolor='white', width='1.7')
        
        area2.node('S1', 'S1', shape='box', style='filled', fillcolor=switch_color, fontcolor='white')
        area2.node('S4', 'S4', shape='box', style='filled', fillcolor=switch_color, fontcolor='white')
        area2.node('S8', 'S8', shape='box', style='filled', fillcolor=switch_color, fontcolor='white')
        area2.node('S6', 'S6', shape='box', style='filled', fillcolor=switch_color, fontcolor='white')
        area2.node('S5', 'S5', shape='box', style='filled', fillcolor=switch_color, fontcolor='white')
        
        vlan2_color = '#C8E6C9'
        area2.node('VLAN400', 'VLAN 400\n192.168.0.0/27\n18 hosts',
                  shape='note', style='filled', fillcolor=vlan2_color)
        area2.node('VLAN100', 'VLAN 100\n192.168.0.32/28\n14 hosts',
                  shape='note', style='filled', fillcolor=vlan2_color)
        area2.node('VLAN200', 'VLAN 200\n192.168.0.48/28\n12 hosts',
                  shape='note', style='filled', fillcolor=vlan2_color)
        area2.node('VLAN300', 'VLAN 300\n192.168.0.64/29\n5 hosts',
                  shape='note', style='filled', fillcolor=vlan2_color)
        area2.node('VLAN1', 'VLAN 1\n192.168.0.72/30\n2 hosts',
                  shape='note', style='filled', fillcolor=vlan2_color)
    
    # AREA 3
    with dot.subgraph(name='cluster_area3') as area3:
        area3.attr(label='AREA 3: CLASS A\n10.0.0.0/8',
                  style='filled,dashed',
                  color='#D32F2F',
                  fillcolor='#FFEBEE',
                  penwidth='4',
                  fontsize='14')
        
        area3.node('R11', 'R11\n\nG0/0: .29 (ISP)\nVLAN 6: 10.130.0.1\nVLAN 7: 10.132.96.1',
                  shape='box', style='filled,rounded', fillcolor=router_color, fontcolor='white', width='1.8')
        area3.node('R12', 'R12\n\nVLAN 8: 10.128.0.1\nVLAN 9: 10.132.0.1\nVLAN 11: 10.132.64.1',
                  shape='box', style='filled,rounded', fillcolor=router_color, fontcolor='white', width='1.9')
        area3.node('R13', 'R13\n\nVLAN 10: 10.0.0.1\nVLANs 500/600/700',
                  shape='box', style='filled,rounded', fillcolor=router_color, fontcolor='white', width='1.7')
        
        area3.node('S7', 'S7', shape='box', style='filled', fillcolor=switch_color, fontcolor='white')
        area3.node('S9', 'S9', shape='box', style='filled', fillcolor=switch_color, fontcolor='white')
        
        vlan3_color = '#FFCDD2'
        area3.node('VLAN10', 'VLAN 10\n10.0.0.0/9\n5,000,000 hosts',
                  shape='note', style='filled', fillcolor=vlan3_color, fontsize='10')
        area3.node('VLAN6', 'VLAN 6\n10.130.0.0/15\n202,000 hosts',
                  shape='note', style='filled', fillcolor=vlan3_color)
        area3.node('VLAN7', 'VLAN 7\n10.132.96.0/21\n2,000 hosts',
                  shape='note', style='filled', fillcolor=vlan3_color)
        area3.node('VLAN8', 'VLAN 8\n10.128.0.0/15\n200,000 hosts',
                  shape='note', style='filled', fillcolor=vlan3_color)
        area3.node('VLAN9', 'VLAN 9\n10.132.0.0/18\n10,000 hosts',
                  shape='note', style='filled', fillcolor=vlan3_color)
        area3.node('VLAN11', 'VLAN 11\n10.132.64.0/19\n5,000 hosts',
                  shape='note', style='filled', fillcolor=vlan3_color)
    
    # CONNECTIONS
    # Force layout with invisible edges to position areas around ISP
    # Area 1 on left
    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('R1')
        s.node('ISP')
    
    # Area 3 on right  
    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('ISP')
        s.node('R11')
    
    # ISP - Bold connections
    dot.edge('R1', 'ISP', label='.20/30', color='#D32F2F', penwidth='4', style='bold', dir='both')
    dot.edge('ISP', 'R7', label='.24/30', color='#D32F2F', penwidth='4', style='bold')
    dot.edge('ISP', 'R11', label='.28/30', color='#D32F2F', penwidth='4', style='bold', dir='both')
    
    # Area 1
    dot.edge('R1', 'R4', label='.4/30', color='#1565C0', penwidth='2.5')
    dot.edge('R1', 'R5', label='.8/30', color='#1565C0', penwidth='2.5')
    dot.edge('R4', 'R3', label='.0/30', color='#1565C0', penwidth='2.5')
    dot.edge('R5', 'R6', label='.12/30', color='#1565C0', penwidth='2.5')
    dot.edge('R5', 'S2', color='#0277BD', style='dashed', penwidth='2')
    dot.edge('S2', 'R4', color='#0277BD', style='dashed', penwidth='2')
    dot.edge('S2', 'R1', color='#0277BD', style='dashed', penwidth='2')
    dot.edge('R3', 'VLAN4', color='#64B5F6', style='dotted', penwidth='2')
    dot.edge('R3', 'VLAN5', color='#64B5F6', style='dotted', penwidth='2')
    dot.edge('R6', 'S3', color='#0277BD', style='dashed', penwidth='2')
    dot.edge('S3', 'VLAN2', color='#64B5F6', style='dotted', penwidth='2')
    dot.edge('S3', 'VLAN3', color='#64B5F6', style='dotted', penwidth='2')
    
    # Inter-area
    dot.edge('R3', 'R2', label='INTER-AREA\n.16/30', color='#7B1FA2', penwidth='4', style='bold')
    
    # Area 2
    dot.edge('R7', 'R8', label='.32/30', color='#388E3C', penwidth='2.5')
    dot.edge('R8', 'R9', label='.36/30', color='#388E3C', penwidth='2.5')
    dot.edge('R9', 'R10', label='.40/30', color='#388E3C', penwidth='2.5')
    dot.edge('R7', 'S1', color='#0277BD', style='dashed', penwidth='2')
    dot.edge('S1', 'VLAN400', color='#81C784', style='dotted', penwidth='2')
    dot.edge('R2', 'VLAN1', color='#81C784', style='dotted', penwidth='2')
    dot.edge('R8', 'S4', color='#0277BD', style='dashed', penwidth='2')
    dot.edge('S4', 'VLAN100', color='#81C784', style='dotted', penwidth='2')
    dot.edge('R8', 'S8', color='#0277BD', style='dashed', penwidth='2')
    dot.edge('S8', 'VLAN200', color='#81C784', style='dotted', penwidth='2')
    dot.edge('R10', 'S6', color='#0277BD', style='dashed', penwidth='2')
    dot.edge('S6', 'S5', label='Cascade', color='#0277BD', style='dashed', penwidth='2')
    dot.edge('S6', 'VLAN300', color='#81C784', style='dotted', penwidth='2')
    
    # Area 3
    dot.edge('R11', 'R12', label='.44/30', color='#D32F2F', penwidth='2.5')
    dot.edge('R12', 'R13', label='.48/30', color='#D32F2F', penwidth='2.5')
    dot.edge('R11', 'S7', color='#0277BD', style='dashed', penwidth='2')
    dot.edge('S7', 'VLAN6', color='#EF9A9A', style='dotted', penwidth='2')
    dot.edge('S7', 'VLAN7', color='#EF9A9A', style='dotted', penwidth='2')
    dot.edge('R12', 'VLAN8', color='#EF9A9A', style='dotted', penwidth='2')
    dot.edge('R12', 'VLAN9', color='#EF9A9A', style='dotted', penwidth='2')
    dot.edge('R12', 'VLAN11', color='#EF9A9A', style='dotted', penwidth='2')
    dot.edge('R13', 'S9', color='#0277BD', style='dashed', penwidth='2')
    dot.edge('S9', 'VLAN10', color='#EF9A9A', style='dotted', penwidth='2')
    
    # Save
    output_dir = Path("prom06")
    output_file = output_dir / 'IPv4_EasyRead_Diagram'
    try:
        dot.render(output_file, view=False, cleanup=True)
        print(f"SUCCESS: Easy-to-read diagram saved: {output_file}.png")
        return output_file
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    print("=" * 70)
    print("Easy-to-Read Network Diagram Generator")
    print("=" * 70)
    print()
    
    if not GRAPHVIZ_AVAILABLE:
        print("ERROR: Graphviz not available")
    else:
        result = create_easy_read_diagram()
        if result:
            print("\n" + "=" * 70)
            print(f"Diagram: {result}.png")
            print("=" * 70)

