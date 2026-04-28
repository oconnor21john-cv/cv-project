"""
Network Diagram Generator
Creates visual network topology diagrams with IPv4 and IPv6 addressing
Uses graphviz for professional-looking network diagrams
"""

try:
    from graphviz import Digraph
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("Note: Install graphviz for diagram generation: pip install graphviz")

import json
from pathlib import Path


class NetworkDiagramGenerator:
    """Generate network topology diagrams with IP addressing"""
    
    def __init__(self, output_dir="network_diagrams"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def create_ipv4_diagram(self):
        """Generate IPv4 network diagram"""
        if not GRAPHVIZ_AVAILABLE:
            print("Graphviz not available. Please install: pip install graphviz")
            return None
            
        dot = Digraph(comment='IPv4 Network Topology', format='png')
        dot.attr(rankdir='TB', splines='ortho', nodesep='0.8', ranksep='1.2')
        dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
        
        # Define color scheme
        router_color = '#E8F4F8'
        switch_color = '#FFF4E6'
        pc_color = '#E8F5E9'
        isp_color = '#FFE6E6'
        
        # ISP Router (center)
        with dot.subgraph(name='cluster_isp') as isp:
            isp.attr(label='ISP Area', style='filled', color='lightgrey')
            isp.node('ISP', 'ISP Router\n\nG1/1/1: 203.0.113.22\nG1/1/2: 203.0.113.30\nG1/1/3: 203.0.113.26',
                    fillcolor=isp_color, fontsize='10')
        
        # Area 1: Class B Network
        with dot.subgraph(name='cluster_area1') as area1:
            area1.attr(label='Area 1: Class B (172.16.0.0/16)', style='filled', color='#B3E5FC')
            
            # Routers
            area1.node('R1', 'R1\n\nG0/0: 203.0.113.6\nG0/2: 203.0.113.9\nG1/1/1: 203.0.113.21',
                      fillcolor=router_color, fontsize='9')
            area1.node('R2', 'R2\n\nG0/0: 203.0.113.17\nG0/1: 192.168.0.73',
                      fillcolor=router_color, fontsize='9')
            area1.node('R3', 'R3\n\nVLAN 4: 172.16.0.1\nVLAN 5: 172.16.7.1\nP2P: .1, .18',
                      fillcolor=router_color, fontsize='9')
            area1.node('R4', 'R4\n\nG0/0: 203.0.113.5\nG0/1: 203.0.113.2',
                      fillcolor=router_color, fontsize='9')
            area1.node('R5', 'R5\n\nG0/0: 203.0.113.10\nG0/1: 203.0.113.13',
                      fillcolor=router_color, fontsize='9')
            area1.node('R6', 'R6\n\nVLAN 2: 172.16.4.1\nVLAN 3: 172.16.6.1',
                      fillcolor=router_color, fontsize='9')
            
            # Switches
            area1.node('S2', 'S2', fillcolor=switch_color, fontsize='9')
            area1.node('S3', 'S3', fillcolor=switch_color, fontsize='9')
            
            # VLANs
            area1.node('VLAN4', 'VLAN 4\n1024 hosts\n172.16.0.0/22',
                      fillcolor=pc_color, fontsize='8', shape='box')
            area1.node('VLAN5', 'VLAN 5\n2 hosts\n172.16.7.0/30',
                      fillcolor=pc_color, fontsize='8', shape='box')
            area1.node('VLAN2', 'VLAN 2\n400 hosts\n172.16.4.0/23',
                      fillcolor=pc_color, fontsize='8', shape='box')
            area1.node('VLAN3', 'VLAN 3\n250 hosts\n172.16.6.0/24',
                      fillcolor=pc_color, fontsize='8', shape='box')
        
        # Area 2: Class C Network
        with dot.subgraph(name='cluster_area2') as area2:
            area2.attr(label='Area 2: Class C (192.168.0.0/16)', style='filled', color='#C8E6C9')
            
            # Routers
            area2.node('R7', 'R7\n\nVLAN 400: 192.168.0.1\nISP: 203.0.113.25',
                      fillcolor=router_color, fontsize='9')
            area2.node('R8', 'R8\n\nVLAN 100: 192.168.0.33\nVLAN 200: 192.168.0.49',
                      fillcolor=router_color, fontsize='9')
            area2.node('R9', 'R9\n\nG0/0: 203.0.113.41\nG0/1: 203.0.113.38',
                      fillcolor=router_color, fontsize='9')
            area2.node('R10', 'R10\n\nVLAN 300: 192.168.0.65',
                      fillcolor=router_color, fontsize='9')
            
            # Switches
            area2.node('S1', 'S1', fillcolor=switch_color, fontsize='9')
            area2.node('S4', 'S4', fillcolor=switch_color, fontsize='9')
            area2.node('S5', 'S5', fillcolor=switch_color, fontsize='9')
            area2.node('S6', 'S6', fillcolor=switch_color, fontsize='9')
            area2.node('S8', 'S8', fillcolor=switch_color, fontsize='9')
            
            # VLANs
            area2.node('VLAN400', 'VLAN 400\n18 hosts\n192.168.0.0/27',
                      fillcolor=pc_color, fontsize='8', shape='box')
            area2.node('VLAN100', 'VLAN 100\n14 hosts\n192.168.0.32/28',
                      fillcolor=pc_color, fontsize='8', shape='box')
            area2.node('VLAN200', 'VLAN 200\n12 hosts\n192.168.0.48/28',
                      fillcolor=pc_color, fontsize='8', shape='box')
            area2.node('VLAN300', 'VLAN 300\n5 hosts\n192.168.0.64/29',
                      fillcolor=pc_color, fontsize='8', shape='box')
            area2.node('VLAN1', 'VLAN 1\n2 hosts\n192.168.0.72/30',
                      fillcolor=pc_color, fontsize='8', shape='box')
        
        # Area 3: Class A Network
        with dot.subgraph(name='cluster_area3') as area3:
            area3.attr(label='Area 3: Class A (10.0.0.0/8)', style='filled', color='#FFCCBC')
            
            # Routers
            area3.node('R11', 'R11\n\nVLAN 6: 10.130.0.1\nVLAN 7: 10.132.96.1\nISP: 203.0.113.29',
                      fillcolor=router_color, fontsize='9')
            area3.node('R12', 'R12\n\nVLAN 8: 10.128.0.1\nVLAN 9: 10.132.0.1\nVLAN 11: 10.132.64.1',
                      fillcolor=router_color, fontsize='9')
            area3.node('R13', 'R13\n\nVLAN 10: 10.0.0.1\nVLANs 500/600/700',
                      fillcolor=router_color, fontsize='9')
            
            # Switches
            area3.node('S7', 'S7', fillcolor=switch_color, fontsize='9')
            area3.node('S9', 'S9', fillcolor=switch_color, fontsize='9')
            
            # Major VLANs
            area3.node('VLAN10', 'VLAN 10\n5M hosts\n10.0.0.0/9',
                      fillcolor=pc_color, fontsize='8', shape='box')
            area3.node('VLAN6', 'VLAN 6\n202K hosts\n10.130.0.0/15',
                      fillcolor=pc_color, fontsize='8', shape='box')
            area3.node('VLAN8', 'VLAN 8\n200K hosts\n10.128.0.0/15',
                      fillcolor=pc_color, fontsize='8', shape='box')
        
        # Connections - Area 1
        dot.edge('ISP', 'R1', label='203.0.113.20/30', fontsize='8')
        dot.edge('R1', 'R4', label='203.0.113.4/30', fontsize='8')
        dot.edge('R1', 'R5', label='203.0.113.8/30', fontsize='8')
        dot.edge('R4', 'R3', label='203.0.113.0/30', fontsize='8')
        dot.edge('R3', 'R2', label='203.0.113.16/30', fontsize='8')
        dot.edge('R5', 'R6', label='203.0.113.12/30', fontsize='8')
        dot.edge('R5', 'S2', fontsize='8')
        dot.edge('S2', 'R4', fontsize='8')
        dot.edge('S2', 'R3', fontsize='8')
        dot.edge('R3', 'VLAN4', fontsize='8')
        dot.edge('R3', 'VLAN5', fontsize='8')
        dot.edge('R2', 'VLAN1', fontsize='8')
        dot.edge('R6', 'S3', fontsize='8')
        dot.edge('S3', 'VLAN2', fontsize='8')
        dot.edge('S3', 'VLAN3', fontsize='8')
        
        # Connections - Area 2
        dot.edge('ISP', 'R7', label='203.0.113.24/30', fontsize='8')
        dot.edge('R7', 'R8', label='203.0.113.32/30', fontsize='8')
        dot.edge('R8', 'R9', label='203.0.113.36/30', fontsize='8')
        dot.edge('R9', 'R10', label='203.0.113.40/30', fontsize='8')
        dot.edge('R7', 'S1', fontsize='8')
        dot.edge('S1', 'VLAN400', fontsize='8')
        dot.edge('R8', 'S4', fontsize='8')
        dot.edge('S4', 'VLAN100', fontsize='8')
        dot.edge('R8', 'S8', fontsize='8')
        dot.edge('S8', 'VLAN200', fontsize='8')
        dot.edge('R10', 'S6', fontsize='8')
        dot.edge('S6', 'S5', fontsize='8')
        dot.edge('S5', 'VLAN300', fontsize='8')
        
        # Connections - Area 3
        dot.edge('ISP', 'R11', label='203.0.113.28/30', fontsize='8')
        dot.edge('R11', 'R12', label='203.0.113.44/30', fontsize='8')
        dot.edge('R12', 'R13', label='203.0.113.48/30', fontsize='8')
        dot.edge('R11', 'S7', fontsize='8')
        dot.edge('S7', 'VLAN6', fontsize='8')
        dot.edge('R12', 'VLAN8', fontsize='8')
        dot.edge('R13', 'S9', fontsize='8')
        dot.edge('S9', 'VLAN10', fontsize='8')
        
        # Save diagram
        output_file = self.output_dir / 'IPv4_Network_Topology'
        dot.render(output_file, view=False, cleanup=True)
        print(f"✓ IPv4 diagram saved: {output_file}.png")
        return output_file
    
    def create_ipv6_diagram(self):
        """Generate IPv6 network diagram"""
        if not GRAPHVIZ_AVAILABLE:
            print("Graphviz not available. Please install: pip install graphviz")
            return None
            
        dot = Digraph(comment='IPv6 Network Topology', format='png')
        dot.attr(rankdir='TB', splines='ortho', nodesep='0.8', ranksep='1.2')
        dot.attr('node', shape='box', style='rounded,filled', fontname='Arial')
        
        # Define color scheme
        router_color = '#E1F5FE'
        switch_color = '#FFF9C4'
        pc_color = '#F1F8E9'
        isp_color = '#FFEBEE'
        
        # ISP Router
        with dot.subgraph(name='cluster_isp') as isp:
            isp.attr(label='ISP Area (IPv6)', style='filled', color='lightgrey')
            isp.node('ISP', 'ISP Router\n\nG1/1/1: 2001:db8:ff00::14\nG1/1/2: 2001:db8:ff00::18\nG1/1/3: 2001:db8:ff00::16',
                    fillcolor=isp_color, fontsize='10')
        
        # Area 1
        with dot.subgraph(name='cluster_area1') as area1:
            area1.attr(label='Area 1: 2001:db8:1000::/36', style='filled', color='#B3E5FC')
            
            area1.node('R1', 'R1\n\n::ff00::2\n::ff00::5\n::ff00::15',
                      fillcolor=router_color, fontsize='9')
            area1.node('R3', 'R3\n\nVLAN 4: ::1000:4::1\nVLAN 5: ::1000:5::1',
                      fillcolor=router_color, fontsize='9')
            area1.node('R6', 'R6\n\nVLAN 2: ::1000:2::1\nVLAN 3: ::1000:3::1',
                      fillcolor=router_color, fontsize='9')
            
            area1.node('VLAN4_v6', 'VLAN 4\n2001:db8:1000:4::/64',
                      fillcolor=pc_color, fontsize='8', shape='box')
            area1.node('VLAN2_v6', 'VLAN 2\n2001:db8:1000:2::/64',
                      fillcolor=pc_color, fontsize='8', shape='box')
        
        # Area 2
        with dot.subgraph(name='cluster_area2') as area2:
            area2.attr(label='Area 2: 2001:db8:2000::/36', style='filled', color='#C8E6C9')
            
            area2.node('R7', 'R7\n\nVLAN 400: ::2000:400::1',
                      fillcolor=router_color, fontsize='9')
            area2.node('R8', 'R8\n\nVLAN 100: ::2000:100::1\nVLAN 200: ::2000:200::1',
                      fillcolor=router_color, fontsize='9')
            area2.node('R10', 'R10\n\nVLAN 300: ::2000:300::1',
                      fillcolor=router_color, fontsize='9')
            
            area2.node('VLAN400_v6', 'VLAN 400\n2001:db8:2000:400::/64',
                      fillcolor=pc_color, fontsize='8', shape='box')
            area2.node('VLAN100_v6', 'VLAN 100\n2001:db8:2000:100::/64',
                      fillcolor=pc_color, fontsize='8', shape='box')
        
        # Area 3
        with dot.subgraph(name='cluster_area3') as area3:
            area3.attr(label='Area 3: 2001:db8:3000::/36', style='filled', color='#FFCCBC')
            
            area3.node('R11', 'R11\n\nVLAN 6: ::3000:6::1\nVLAN 7: ::3000:7::1',
                      fillcolor=router_color, fontsize='9')
            area3.node('R12', 'R12\n\nVLAN 8: ::3000:8::1\nVLAN 11: ::3000:11::1',
                      fillcolor=router_color, fontsize='9')
            area3.node('R13', 'R13\n\nVLAN 10: ::3000:10::1',
                      fillcolor=router_color, fontsize='9')
            
            area3.node('VLAN10_v6', 'VLAN 10\n2001:db8:3000:10::/64\n(5M hosts)',
                      fillcolor=pc_color, fontsize='8', shape='box')
            area3.node('VLAN6_v6', 'VLAN 6\n2001:db8:3000:6::/64\n(202K hosts)',
                      fillcolor=pc_color, fontsize='8', shape='box')
        
        # Connections
        dot.edge('ISP', 'R1', label='2001:db8:ff00::14/127', fontsize='8')
        dot.edge('ISP', 'R7', label='2001:db8:ff00::16/127', fontsize='8')
        dot.edge('ISP', 'R11', label='2001:db8:ff00::18/127', fontsize='8')
        
        dot.edge('R1', 'R3', label='P2P /127', fontsize='8')
        dot.edge('R1', 'R6', label='P2P /127', fontsize='8')
        dot.edge('R3', 'VLAN4_v6', fontsize='8')
        dot.edge('R6', 'VLAN2_v6', fontsize='8')
        
        dot.edge('R7', 'R8', label='2001:db8:ff00::20/127', fontsize='8')
        dot.edge('R8', 'R10', label='P2P /127', fontsize='8')
        dot.edge('R7', 'VLAN400_v6', fontsize='8')
        dot.edge('R8', 'VLAN100_v6', fontsize='8')
        
        dot.edge('R11', 'R12', label='2001:db8:ff00::30/127', fontsize='8')
        dot.edge('R12', 'R13', label='2001:db8:ff00::32/127', fontsize='8')
        dot.edge('R11', 'VLAN6_v6', fontsize='8')
        dot.edge('R13', 'VLAN10_v6', fontsize='8')
        
        # Save diagram
        output_file = self.output_dir / 'IPv6_Network_Topology'
        dot.render(output_file, view=False, cleanup=True)
        print(f"✓ IPv6 diagram saved: {output_file}.png")
        return output_file
    
    def create_simplified_overview(self):
        """Create a simplified high-level overview"""
        if not GRAPHVIZ_AVAILABLE:
            return None
            
        dot = Digraph(comment='Network Overview', format='png')
        dot.attr(rankdir='LR', splines='ortho')
        dot.attr('node', shape='box3d', style='filled', fontname='Arial Bold', fontsize='12')
        
        # Areas
        dot.node('Area1', 'Area 1\nClass B\n172.16.0.0/16\n\n4 VLANs\n1,676 hosts\n\nIPv6:\n2001:db8:1000::/36',
                fillcolor='#81D4FA', width='2.5')
        dot.node('ISP', 'ISP\nCentral Hub\n\nIPv4: 203.0.113.0/24\nIPv6: 2001:db8:ff00::/48',
                fillcolor='#EF9A9A', width='2.5')
        dot.node('Area2', 'Area 2\nClass C\n192.168.0.0/16\n\n5 VLANs\n51 hosts\n\nIPv6:\n2001:db8:2000::/36',
                fillcolor='#A5D6A7', width='2.5')
        dot.node('Area3', 'Area 3\nClass A\n10.0.0.0/8\n\n9 VLANs\n5.4M hosts\n\nIPv6:\n2001:db8:3000::/36',
                fillcolor='#FFCC80', width='2.5')
        
        # Connections
        dot.edge('Area1', 'ISP', label='R1 ↔ ISP', fontsize='10', penwidth='2')
        dot.edge('Area2', 'ISP', label='R7 ↔ ISP', fontsize='10', penwidth='2')
        dot.edge('Area3', 'ISP', label='R11 ↔ ISP', fontsize='10', penwidth='2')
        
        output_file = self.output_dir / 'Network_Overview'
        dot.render(output_file, view=False, cleanup=True)
        print(f"✓ Overview diagram saved: {output_file}.png")
        return output_file


def main():
    """Generate all network diagrams"""
    print("=" * 60)
    print("Network Diagram Generator")
    print("=" * 60)
    
    if not GRAPHVIZ_AVAILABLE:
        print("\n⚠️  Graphviz library not found!")
        print("\nTo install:")
        print("  1. Install Python package: pip install graphviz")
        print("  2. Install Graphviz software: https://graphviz.org/download/")
        print("\nFor Windows: choco install graphviz (or download installer)")
        print("For Mac: brew install graphviz")
        print("For Linux: sudo apt-get install graphviz")
        return
    
    generator = NetworkDiagramGenerator()
    
    print("\nGenerating diagrams...\n")
    
    # Generate all diagrams
    generator.create_simplified_overview()
    generator.create_ipv4_diagram()
    generator.create_ipv6_diagram()
    
    print("\n" + "=" * 60)
    print("✓ All diagrams generated successfully!")
    print(f"✓ Check the 'network_diagrams' folder")
    print("=" * 60)


if __name__ == "__main__":
    main()

