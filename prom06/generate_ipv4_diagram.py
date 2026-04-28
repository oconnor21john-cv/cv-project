#!/usr/bin/env python3
"""
Generate Network Diagram with IPv4 Addresses Applied
Creates a comprehensive visual representation of the three-area network topology
"""

import graphviz
from pathlib import Path

def create_ipv4_network_diagram():
    """Create detailed network diagram with IPv4 addressing"""
    
    # Create a new directed graph with custom styling
    dot = graphviz.Digraph(comment='Multi-Area Network with IPv4 Addressing')
    dot.attr(rankdir='TB', splines='ortho', nodesep='0.8', ranksep='1.2')
    dot.attr('node', style='filled', fontname='Arial', fontsize='10')
    dot.attr('edge', fontname='Arial', fontsize='8')
    
    # Define color scheme
    colors = {
        'isp': '#2C3E50',
        'router': '#3498DB',
        'switch': '#1ABC9C',
        'l3_switch': '#16A085',
        'server': '#E74C3C',
        'pc': '#95A5A6',
        'area1_bg': '#EBF5FB',
        'area2_bg': '#E8F8F5',
        'area3_bg': '#FDEDEC'
    }
    
    # ISP Router
    dot.node('ISP', 'ISP Router\nPublic IPs', 
             shape='doublecircle', fillcolor=colors['isp'], fontcolor='white', 
             fontsize='12', width='1.5', height='1.5')
    
    # ==================== AREA 1: CLASS B ====================
    with dot.subgraph(name='cluster_area1') as area1:
        area1.attr(label='Area 1: Class B Network\n172.16.0.0/16', 
                   style='dashed', color='blue', penwidth='3', 
                   bgcolor=colors['area1_bg'], fontsize='14', fontcolor='blue')
        
        # Routers
        area1.node('R1', 'R1\n\nG0/0: 172.16.0.2/30\nG0/1: 172.16.1.1/24\nG0/2: 172.16.2.1/24', 
                   shape='box3d', fillcolor=colors['router'], fontcolor='white')
        
        area1.node('R2', 'R2\n\nG0/0: 172.16.1.2/24\nG0/1: 172.16.10.1/30', 
                   shape='box3d', fillcolor=colors['router'], fontcolor='white')
        
        area1.node('R3', 'R3\n\nG0/0: 172.16.1.3/24\nG0/1: 172.16.3.1/24', 
                   shape='box3d', fillcolor=colors['router'], fontcolor='white')
        
        area1.node('R4', 'R4\n\nG0/0: 172.16.2.2/24\nG0/1: 172.16.11.1/30', 
                   shape='box3d', fillcolor=colors['router'], fontcolor='white')
        
        area1.node('R5', 'R5\n\nG0/0: 172.16.2.3/24\nG0/1: 172.16.12.1/30', 
                   shape='box3d', fillcolor=colors['router'], fontcolor='white')
        
        area1.node('R6', 'R6\n\nG0/0: 172.16.12.2/30\nG0/1: Trunk', 
                   shape='box3d', fillcolor=colors['router'], fontcolor='white')
        
        # Switches
        area1.node('S1', 'S1\n\n172.16.1.0/24', 
                   shape='box', fillcolor=colors['switch'], fontcolor='white')
        
        area1.node('S2', 'S2\n\n172.16.2.0/24', 
                   shape='box', fillcolor=colors['switch'], fontcolor='white')
        
        area1.node('S3a', 'S3a\n\n172.16.3.0/24\nVLANs 2 & 3', 
                   shape='box', fillcolor=colors['switch'], fontcolor='white')
        
        area1.node('S3b', 'S3b\n\n172.16.4.0/24\nVLANs 4 & 5', 
                   shape='box', fillcolor=colors['switch'], fontcolor='white')
        
        # Servers
        area1.node('Server1', 'Server\n172.16.10.2/30', 
                   shape='cylinder', fillcolor=colors['server'], fontcolor='white')
        
        area1.node('Server2', 'Server\n172.16.11.2/30', 
                   shape='cylinder', fillcolor=colors['server'], fontcolor='white')
        
        # VLANs on S3a (connected to R3)
        area1.node('VLAN2', 'VLAN 2\n400 hosts\n172.16.20.0/23\nGW: .20.1', 
                   shape='folder', fillcolor=colors['pc'], fontcolor='black')
        
        area1.node('VLAN3', 'VLAN 3\n250 hosts\n172.16.22.0/24\nGW: .22.1', 
                   shape='folder', fillcolor=colors['pc'], fontcolor='black')
        
        # VLANs on S3b (connected to R6 trunk)
        area1.node('VLAN4', 'VLAN 4\n1024 hosts\n172.16.24.0/22\nGW: .24.1', 
                   shape='folder', fillcolor=colors['pc'], fontcolor='black')
        
        area1.node('VLAN5', 'VLAN 5\n505 hosts\n172.16.28.0/23\nGW: .28.1', 
                   shape='folder', fillcolor=colors['pc'], fontcolor='black')
    
    # ==================== AREA 2: CLASS C ====================
    with dot.subgraph(name='cluster_area2') as area2:
        area2.attr(label='Area 2: Class C Network\n192.168.0.0/16', 
                   style='dashed', color='green', penwidth='3', 
                   bgcolor=colors['area2_bg'], fontsize='14', fontcolor='green')
        
        # Routers
        area2.node('R7', 'R7\n\nG0/1: 192.168.0.2/30\nG0/0: 192.168.1.2/27', 
                   shape='box3d', fillcolor=colors['router'], fontcolor='white')
        
        area2.node('R8', 'R8\n\nG0/0: 192.168.5.2/28\nG0/1: 192.168.12.1/27', 
                   shape='box3d', fillcolor=colors['router'], fontcolor='white')
        
        area2.node('R9', 'R9\n\nG0/0: 192.168.4.2/28\nG0/1: 192.168.11.1/26', 
                   shape='box3d', fillcolor=colors['router'], fontcolor='white')
        
        area2.node('R10', 'R10\n\nG0/0: 192.168.2.2/29\nG0/1: 192.168.10.1/27', 
                   shape='box3d', fillcolor=colors['router'], fontcolor='white')
        
        # L3 Switches
        area2.node('L3_3', 'L3-3\n\nVLAN 400: 192.168.1.1/27\nVLAN 300: 192.168.2.1/29\nVLAN 1: 192.168.3.1/30', 
                   shape='component', fillcolor=colors['l3_switch'], fontcolor='white')
        
        area2.node('L3_2', 'L3-2\n\nVLAN 1: 192.168.3.2/30\nVLAN 200: 192.168.4.1/28\nVLAN 100: 192.168.5.1/28', 
                   shape='component', fillcolor=colors['l3_switch'], fontcolor='white')
        
        # Switches
        area2.node('S4', 'S4\n14 hosts\n192.168.12.0/27', 
                   shape='box', fillcolor=colors['switch'], fontcolor='white')
        
        area2.node('S5', 'S5\n60 hosts\n192.168.11.0/26', 
                   shape='box', fillcolor=colors['switch'], fontcolor='white')
        
        area2.node('S6', 'S6\n25 hosts\n192.168.10.0/27', 
                   shape='box', fillcolor=colors['switch'], fontcolor='white')
        
        # End devices
        area2.node('PC_S4', 'PC', shape='rectangle', fillcolor=colors['pc'], fontcolor='black')
        area2.node('PC_S5', 'PC', shape='rectangle', fillcolor=colors['pc'], fontcolor='black')
        area2.node('PC_S6', 'PC', shape='rectangle', fillcolor=colors['pc'], fontcolor='black')
    
    # ==================== AREA 3: CLASS A ====================
    with dot.subgraph(name='cluster_area3') as area3:
        area3.attr(label='Area 3: Class A Network\n10.0.0.0/8', 
                   style='dashed', color='red', penwidth='3', 
                   bgcolor=colors['area3_bg'], fontsize='14', fontcolor='red')
        
        # Routers
        area3.node('R11', 'R11\n\nG0/0: 10.0.0.2/30\nG0/1: Trunk\nG0/2: 10.10.1.2/27', 
                   shape='box3d', fillcolor=colors['router'], fontcolor='white')
        
        area3.node('R12', 'R12\n\nG0/0: 10.10.2.2/25\nG0/1: Trunk', 
                   shape='box3d', fillcolor=colors['router'], fontcolor='white')
        
        area3.node('R13', 'R13\n\nG0/0: 10.10.3.2/26\nG0/1: Trunk', 
                   shape='box3d', fillcolor=colors['router'], fontcolor='white')
        
        # L3 Switch
        area3.node('L3_1', 'L3-1\n\nVLAN 500: 10.10.1.1/27\nVLAN 700: 10.10.2.1/25\nVLAN 600: 10.10.3.1/26', 
                   shape='component', fillcolor=colors['l3_switch'], fontcolor='white')
        
        # Switches
        area3.node('S7', 'S7\n\nVLAN 6: 10.1.0.0/14\nVLAN 7: 10.5.0.0/21', 
                   shape='box', fillcolor=colors['switch'], fontcolor='white')
        
        area3.node('S8', 'S8\n\nVLAN 8: 10.20.0.0/14\nVLAN 9: 10.24.0.0/18', 
                   shape='box', fillcolor=colors['switch'], fontcolor='white')
        
        area3.node('S9', 'S9\n\nVLAN 10: 10.64.0.0/9\nVLAN 11: 10.128.0.0/19', 
                   shape='box', fillcolor=colors['switch'], fontcolor='white')
        
        # VLANs
        area3.node('VLAN6', 'VLAN 6\n202,000 hosts\n10.1.0.0/14\nGW: 10.1.0.1', 
                   shape='folder', fillcolor=colors['pc'], fontcolor='black')
        
        area3.node('VLAN7', 'VLAN 7\n2,000 hosts\n10.5.0.0/21\nGW: 10.5.0.1', 
                   shape='folder', fillcolor=colors['pc'], fontcolor='black')
        
        area3.node('VLAN8', 'VLAN 8\n200,000 hosts\n10.20.0.0/14\nGW: 10.20.0.1', 
                   shape='folder', fillcolor=colors['pc'], fontcolor='black')
        
        area3.node('VLAN9', 'VLAN 9\n10,000 hosts\n10.24.0.0/18\nGW: 10.24.0.1', 
                   shape='folder', fillcolor=colors['pc'], fontcolor='black')
        
        area3.node('VLAN10', 'VLAN 10\n5,000,000 hosts\n10.64.0.0/9\nGW: 10.64.0.1', 
                   shape='folder', fillcolor=colors['pc'], fontcolor='black')
        
        area3.node('VLAN11', 'VLAN 11\n5,000 hosts\n10.128.0.0/19\nGW: 10.128.0.1', 
                   shape='folder', fillcolor=colors['pc'], fontcolor='black')
    
    # ==================== CONNECTIONS ====================
    
    # ISP to Area Routers
    dot.edge('ISP', 'R1', label='G1/1/1 - G0/0\n172.16.0.0/30\n2 hosts', 
             color='black', penwidth='2')
    dot.edge('ISP', 'R7', label='G1/1/3 - G0/1\n192.168.0.0/30\n2 hosts', 
             color='black', penwidth='2')
    dot.edge('ISP', 'R11', label='G1/1/2 - G0/0\n10.0.0.0/30\n2 hosts', 
             color='black', penwidth='2')
    
    # Area 1 Connections
    dot.edge('R1', 'S1', label='G0/1', color='blue')
    dot.edge('R1', 'S2', label='G0/2', color='blue')
    
    dot.edge('S1', 'R2', label='G0/0', color='blue')
    dot.edge('R2', 'Server1', label='G0/1\n2 hosts', color='blue')
    
    dot.edge('S1', 'R3', label='G0/0', color='blue')
    dot.edge('R3', 'S3a', label='G0/1', color='blue')
    dot.edge('S3a', 'VLAN2', label='', color='blue', style='dashed')
    dot.edge('S3a', 'VLAN3', label='', color='blue', style='dashed')
    
    dot.edge('S2', 'R4', label='G0/0', color='blue')
    dot.edge('R4', 'Server2', label='G0/1\n2 hosts', color='blue')
    
    dot.edge('S2', 'R5', label='G0/0', color='blue')
    dot.edge('R5', 'R6', label='G0/1 - G0/0\n172.16.12.0/30', color='blue')
    dot.edge('R6', 'S3b', label='G0/1 (Trunk)', color='blue', style='bold')
    dot.edge('S3b', 'VLAN4', label='', color='blue', style='dashed')
    dot.edge('S3b', 'VLAN5', label='', color='blue', style='dashed')
    
    # Area 2 Connections
    dot.edge('R7', 'L3_3', label='G0/0\nVLAN 400\n18 hosts', color='green')
    dot.edge('L3_3', 'R10', label='VLAN 300\n5 hosts', color='green')
    dot.edge('R10', 'S6', label='G0/1\n25 hosts', color='green')
    dot.edge('S6', 'PC_S6', label='', color='green')
    
    dot.edge('L3_3', 'L3_2', label='VLAN 1\n2 hosts', color='green')
    
    dot.edge('L3_2', 'R9', label='VLAN 200\n12 hosts', color='green')
    dot.edge('R9', 'S5', label='G0/1\n60 hosts', color='green')
    dot.edge('S5', 'PC_S5', label='', color='green')
    
    dot.edge('L3_2', 'R8', label='VLAN 100\n8 hosts', color='green')
    dot.edge('R8', 'S4', label='G0/1\n14 hosts', color='green')
    dot.edge('S4', 'PC_S4', label='', color='green')
    
    # Area 3 Connections
    dot.edge('R11', 'S7', label='G0/1 (Trunk)', color='red', style='bold')
    dot.edge('S7', 'VLAN6', label='202,000 hosts', color='red', style='dashed')
    dot.edge('S7', 'VLAN7', label='2,000 hosts', color='red', style='dashed')
    
    dot.edge('R11', 'L3_1', label='G0/2\nVLAN 500\n20 hosts', color='red')
    
    dot.edge('L3_1', 'R12', label='VLAN 700\n80 hosts', color='red')
    dot.edge('R12', 'S8', label='G0/1 (Trunk)', color='red', style='bold')
    dot.edge('S8', 'VLAN8', label='200,000 hosts', color='red', style='dashed')
    dot.edge('S8', 'VLAN9', label='10,000 hosts', color='red', style='dashed')
    
    dot.edge('L3_1', 'R13', label='VLAN 600\n40 hosts', color='red')
    dot.edge('R13', 'S9', label='G0/1 (Trunk)', color='red', style='bold')
    dot.edge('S9', 'VLAN10', label='5,000,000 hosts', color='red', style='dashed')
    dot.edge('S9', 'VLAN11', label='5,000 hosts', color='red', style='dashed')
    
    return dot

def main():
    """Generate and save the IPv4 network diagram"""
    print("Generating IPv4 Network Diagram...")
    
    output_dir = Path(__file__).parent
    
    # Create the diagram
    diagram = create_ipv4_network_diagram()
    
    # Save as PNG and PDF
    output_base = output_dir / 'Network_Diagram_IPv4'
    
    try:
        diagram.render(str(output_base), format='png', cleanup=True)
        print(f"[OK] PNG diagram saved: {output_base}.png")
        
        diagram.render(str(output_base), format='pdf', cleanup=True)
        print(f"[OK] PDF diagram saved: {output_base}.pdf")
        
        # Also save the DOT source
        with open(f"{output_base}.dot", 'w') as f:
            f.write(diagram.source)
        print(f"[OK] DOT source saved: {output_base}.dot")
        
        print("\n[SUCCESS] IPv4 Network Diagram generation complete!")
        
    except Exception as e:
        print(f"[ERROR] Error generating diagram: {e}")
        print("Make sure Graphviz is installed: https://graphviz.org/download/")

if __name__ == '__main__':
    main()

