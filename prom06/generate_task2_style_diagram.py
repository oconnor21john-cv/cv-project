"""
Enhanced Network Diagram Generator - Task 2 Style
Creates detailed network topology diagrams matching Task 2 visual style
with comprehensive IPv4 addressing information
"""

try:
    from graphviz import Digraph
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("Note: Install graphviz for diagram generation: pip install graphviz")

from pathlib import Path


class Task2StyleDiagramGenerator:
    """Generate Task 2 style network diagrams with detailed addressing"""
    
    def __init__(self, output_dir="prom06"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def create_detailed_ipv4_diagram(self):
        """Generate detailed IPv4 network diagram in Task 2 style"""
        if not GRAPHVIZ_AVAILABLE:
            print("Graphviz not available. Please install: pip install graphviz")
            return None
            
        dot = Digraph(comment='IPv4 Network Topology - Task 2 Style', format='png')
        dot.attr(rankdir='TB', splines='polyline', nodesep='1.0', ranksep='1.5', 
                 bgcolor='white', pad='0.5')
        dot.attr('node', fontname='Arial', fontsize='9')
        dot.attr('edge', fontname='Arial', fontsize='8')
        
        # Color scheme matching Task 2
        router_color = '#4A90A4'  # Teal blue
        switch_color = '#5B8FA3'  # Similar teal
        server_color = '#6B9FB3'  # Lighter teal
        area1_color = '#B3D9E5'   # Light blue
        area2_color = '#B8E6B8'   # Light green
        area3_color = '#FFB3B3'   # Light red
        
        # ISP Router (center) - with detailed interfaces
        with dot.subgraph(name='cluster_isp') as isp:
            isp.attr(label='ISP Area: Any public IPs', style='dashed,filled', 
                    color='black', fillcolor='lightgrey', penwidth='2')
            isp.node('ISP', '''ISP Router

G1/1/1: 203.0.113.22
    (to R1)
G1/1/2: 203.0.113.30
    (to R11)
G1/1/3: 203.0.113.26
    (to R7)''',
                    shape='cylinder', fillcolor='black', fontcolor='white', 
                    style='filled', fontsize='9', width='2')
        
        # ==================== AREA 1: CLASS B ====================
        with dot.subgraph(name='cluster_area1') as area1:
            area1.attr(label='Area 1: Class B - 172.16.0.0/16', 
                      style='dashed,filled', color='blue', fillcolor=area1_color, 
                      penwidth='3', fontsize='12')
            
            # Core routers with detailed interface info
            area1.node('R1', '''R1
G0/0: 203.0.113.6
G0/2: 203.0.113.9
G1/1/1: 203.0.113.21
    (to ISP)''',
                      shape='cylinder', fillcolor=router_color, fontcolor='white', 
                      style='filled', width='1.3')
            
            area1.node('R3', '''R3
G0/1: 172.16.0.1
    (VLAN 4)
G0/0: 172.16.7.1
    (VLAN 5)
P2P: 203.0.113.1
    203.0.113.18''',
                      shape='cylinder', fillcolor=router_color, fontcolor='white', 
                      style='filled', width='1.5')
            
            area1.node('R4', '''R4
G0/0: 203.0.113.5
G0/1: 203.0.113.2
172.16.5.2''',
                      shape='cylinder', fillcolor=router_color, fontcolor='white', 
                      style='filled', width='1.3')
            
            area1.node('R5', '''R5
G0/0: 203.0.113.10
G0/1: 203.0.113.13
172.16.5.1''',
                      shape='cylinder', fillcolor=router_color, fontcolor='white', 
                      style='filled', width='1.3')
            
            area1.node('R6', '''R6
G0/0: 203.0.113.14
    (to R5)
G0/1: 172.16.4.1
    172.16.6.1
    (VLANs 2&3 trunk)''',
                      shape='cylinder', fillcolor=router_color, fontcolor='white', 
                      style='filled', width='1.3')
            
            # Switches with VLAN info
            area1.node('S2', '''S2
172.16.5.1''',
                      shape='box', fillcolor=switch_color, fontcolor='white', 
                      style='filled,rounded')
            
            area1.node('S3', '''S3
G0/1 (trunk)''',
                      shape='box', fillcolor=switch_color, fontcolor='white', 
                      style='filled,rounded')
            
            # VLANs with detailed addressing
            area1.node('VLAN4', '''VLAN 4 PC
172.16.0.2
1024 hosts
172.16.0.0/22

Range:
.1 - .3.254''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8')
            
            area1.node('VLAN5', '''VLAN 5 PC
172.16.7.2
2 hosts
172.16.7.0/30

Range:
.7.1 - .7.2''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8')
            
            area1.node('VLAN2', '''VLAN 2 PC
172.16.4.2
400 hosts
172.16.4.0/23

Range:
.4.1 - .5.254''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8')
            
            area1.node('VLAN3', '''VLAN 3 PC
172.16.6.2
250 hosts
172.16.6.0/24

Range:
.6.1 - .6.254''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8')
        
        # ==================== AREA 2: CLASS C ====================
        with dot.subgraph(name='cluster_area2') as area2:
            area2.attr(label='Area 2: Class C - 192.168.0.0/16', 
                      style='dashed,filled', color='green', fillcolor=area2_color, 
                      penwidth='3', fontsize='12')
            
            # Routers
            area2.node('R7', '''R7
G0/0: 203.0.113.25
    (to ISP)
G0/1: 203.0.113.33
    (to R8)
VLAN 400:
    192.168.0.1''',
                      shape='cylinder', fillcolor=router_color, fontcolor='white', 
                      style='filled', width='1.3')
            
            area2.node('R8', '''R8
G0/0: 203.0.113.34
G0/1: 203.0.113.37
VLAN 100:
    192.168.0.33
VLAN 200:
    192.168.0.49''',
                      shape='cylinder', fillcolor=router_color, fontcolor='white', 
                      style='filled', width='1.3')
            
            area2.node('R9', '''R9
G0/0: 203.0.113.41
G0/1: 203.0.113.38''',
                      shape='cylinder', fillcolor=router_color, fontcolor='white', 
                      style='filled', width='1.2')
            
            area2.node('R10', '''R10
G0/0: 203.0.113.42
G0/1: 192.168.0.65
    (VLAN 300)''',
                      shape='cylinder', fillcolor=router_color, fontcolor='white', 
                      style='filled', width='1.2')
            
            area2.node('R2', '''R2
G0/0: 203.0.113.17
    (to R3 in Area 1)
G0/1: 192.168.0.73
    (VLAN 1)''',
                      shape='cylinder', fillcolor=router_color, fontcolor='white', 
                      style='filled', width='1.2')
            
            # Switches
            area2.node('S1', 'S1\n192.168.0.1',
                      shape='box', fillcolor=switch_color, fontcolor='white', 
                      style='filled,rounded')
            
            area2.node('S4', 'S4\nVLAN 100',
                      shape='box', fillcolor=switch_color, fontcolor='white', 
                      style='filled,rounded')
            
            area2.node('S8', 'S8\nVLAN 200',
                      shape='box', fillcolor=switch_color, fontcolor='white', 
                      style='filled,rounded')
            
            area2.node('S6', 'S6\nVLAN 300',
                      shape='box', fillcolor=switch_color, fontcolor='white', 
                      style='filled,rounded')
            
            area2.node('S5', 'S5\nCascade',
                      shape='box', fillcolor=switch_color, fontcolor='white', 
                      style='filled,rounded')
            
            # VLANs
            area2.node('VLAN400', '''VLAN 400
18 hosts
192.168.0.0/27

Range: .1 - .30''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8')
            
            area2.node('VLAN100', '''Server
VLAN 100
192.168.0.34
14 hosts
.32/28

Range: .33-.46''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8')
            
            area2.node('VLAN200', '''Server
VLAN 200
192.168.0.50
12 hosts
.48/28

Range: .49-.62''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8')
            
            area2.node('VLAN300', '''Server
VLAN 300
192.168.0.66
5 hosts
.64/29

Range: .65-.70''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8')
            
            area2.node('VLAN1', '''Server
VLAN 1
192.168.0.74
2 hosts
.72/30''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8')
        
        # ==================== AREA 3: CLASS A ====================
        with dot.subgraph(name='cluster_area3') as area3:
            area3.attr(label='Area 3: Class A - 10.0.0.0/8', 
                      style='dashed,filled', color='red', fillcolor=area3_color, 
                      penwidth='3', fontsize='12')
            
            # Routers
            area3.node('R11', '''R11
G0/0: 203.0.113.29
    (to ISP)
G0/1: 203.0.113.45
G0/2 (trunk)
VLAN 6: 10.130.0.1
VLAN 7: 10.132.96.1''',
                      shape='cylinder', fillcolor=router_color, fontcolor='white', 
                      style='filled', width='1.5')
            
            area3.node('R12', '''R12
G0/0: 203.0.113.46
G0/1: 203.0.113.49
(trunk)
VLAN 8: 10.128.0.1
VLAN 9: 10.132.0.1
VLAN 11: 10.132.64.1''',
                      shape='cylinder', fillcolor=router_color, fontcolor='white', 
                      style='filled', width='1.5')
            
            area3.node('R13', '''R13
G0/0: 203.0.113.50
G0/1 (trunk)
VLAN 10: 10.0.0.1
VLAN 500:
    10.132.104.193
VLAN 600:
    10.132.104.129
VLAN 700:
    10.132.104.1''',
                      shape='cylinder', fillcolor=router_color, fontcolor='white', 
                      style='filled', width='1.5')
            
            # Switches
            area3.node('S7', '''S7
VLAN 6
VLAN 7''',
                      shape='box', fillcolor=switch_color, fontcolor='white', 
                      style='filled,rounded')
            
            area3.node('S9', 'S9\nVLAN 10',
                      shape='box', fillcolor=switch_color, fontcolor='white', 
                      style='filled,rounded')
            
            # VLANs - Large ones
            area3.node('VLAN10', '''VLAN 10
5,000,000 hosts
10.0.0.0/9

Gateway: 10.0.0.1
Range:
10.0.0.2 -
10.127.255.254''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8', width='1.5')
            
            area3.node('VLAN6', '''VLAN 6 PC
202,000 hosts
10.130.0.0/15

Gateway: 10.130.0.1
Range:
10.130.0.2 -
10.131.255.254''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8')
            
            area3.node('VLAN7', '''VLAN 7 PC
2,000 hosts
10.132.96.0/21

Gateway: 10.132.96.1
Range:
10.132.96.2 -
10.132.103.254''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8')
            
            area3.node('VLAN8', '''VLAN 8 PC
200,000 hosts
10.128.0.0/15

Gateway: 10.128.0.1''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8')
            
            area3.node('VLAN9', '''VLAN 9 PC
10,000 hosts
10.132.0.0/18

Gateway: 10.132.0.1''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8')
            
            area3.node('VLAN11', '''VLAN 11 PC
5,000 hosts
10.132.64.0/19

Gateway: 10.132.64.1''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='8')
            
            area3.node('VLAN_SMALL', '''VLAN 500: 20 hosts
10.132.104.192/27

VLAN 600: 40 hosts
10.132.104.128/26

VLAN 700: 80 hosts
10.132.104.0/25''',
                      shape='note', fillcolor=server_color, fontcolor='black', 
                      style='filled', fontsize='7')
        
        # ==================== CONNECTIONS ====================
        
        # ISP to Areas - Bold lines
        dot.edge('ISP', 'R1', label='203.0.113.20/30\n.21<->.22', 
                color='red', penwidth='2', style='bold')
        dot.edge('ISP', 'R7', label='203.0.113.24/30\n.25<->.26', 
                color='red', penwidth='2', style='bold')
        dot.edge('ISP', 'R11', label='203.0.113.28/30\n.29<->.30', 
                color='red', penwidth='2', style='bold')
        
        # Area 1 Connections
        dot.edge('R1', 'R4', label='203.0.113.4/30\n.5<->.6', penwidth='1.5')
        dot.edge('R1', 'R5', label='203.0.113.8/30\n.9<->.10', penwidth='1.5')
        dot.edge('R4', 'R3', label='203.0.113.0/30\n.1<->.2', penwidth='1.5')
        dot.edge('R5', 'R6', label='203.0.113.12/30\n.13<->.14', penwidth='1.5')
        dot.edge('R5', 'S2', label='172.16.5.1', style='dashed')
        dot.edge('S2', 'R4', label='172.16.5.2', style='dashed')
        dot.edge('S2', 'R1', label='172.16.5.x', style='dashed')
        dot.edge('R3', 'VLAN4', label='G0/1\n.0.1', style='dotted', color='blue')
        dot.edge('R3', 'VLAN5', label='G0/0\n.7.1', style='dotted', color='blue')
        dot.edge('R6', 'S3', label='G0/1\nTrunk', style='dashed')
        dot.edge('S3', 'VLAN2', label='VLAN 2\n.4.1-.5.254', style='dotted', color='blue')
        dot.edge('S3', 'VLAN3', label='VLAN 3\n.6.1-.6.254', style='dotted', color='blue')
        
        # Inter-area link (Area 1 to Area 2)
        dot.edge('R3', 'R2', label='203.0.113.16/30\n.17<->.18\nInter-area', 
                penwidth='2', color='purple', style='bold')
        
        # Area 2 Connections
        dot.edge('R7', 'R8', label='203.0.113.32/30\n.33<->.34', penwidth='1.5')
        dot.edge('R8', 'R9', label='203.0.113.36/30\n.37<->.38', penwidth='1.5')
        dot.edge('R9', 'R10', label='203.0.113.40/30\n.41<->.42', penwidth='1.5')
        dot.edge('R7', 'S1', style='dashed')
        dot.edge('S1', 'VLAN400', label='VLAN 400', style='dotted', color='green')
        dot.edge('R2', 'VLAN1', label='G0/1\nVLAN 1', style='dotted', color='green')
        dot.edge('R8', 'S4', label='G0/1', style='dashed')
        dot.edge('S4', 'VLAN100', label='VLAN 100', style='dotted', color='green')
        dot.edge('R8', 'S8', label='G0/2', style='dashed')
        dot.edge('S8', 'VLAN200', label='VLAN 200', style='dotted', color='green')
        dot.edge('R10', 'S6', label='G0/1', style='dashed')
        dot.edge('S6', 'S5', label='Cascade\n(same VLAN)', style='dashed')
        dot.edge('S6', 'VLAN300', label='VLAN 300\n.65-.70', style='dotted', color='green')
        dot.edge('S5', 'VLAN300', label='Same subnet', style='dotted', color='green')
        
        # Area 3 Connections
        dot.edge('R11', 'R12', label='203.0.113.44/30\n.45<->.46', penwidth='1.5')
        dot.edge('R12', 'R13', label='203.0.113.48/30\n.49<->.50', penwidth='1.5')
        dot.edge('R11', 'S7', label='G0/2\nTrunk', style='dashed')
        dot.edge('S7', 'VLAN6', label='VLAN 6', style='dotted', color='red')
        dot.edge('S7', 'VLAN7', label='VLAN 7', style='dotted', color='red')
        dot.edge('R12', 'VLAN8', label='VLAN 8', style='dotted', color='red')
        dot.edge('R12', 'VLAN9', label='VLAN 9', style='dotted', color='red')
        dot.edge('R12', 'VLAN11', label='VLAN 11', style='dotted', color='red')
        dot.edge('R13', 'S9', label='G0/1\nTrunk', style='dashed')
        dot.edge('S9', 'VLAN10', label='VLAN 10\n5M hosts', style='dotted', color='red')
        dot.edge('R13', 'VLAN_SMALL', label='Small VLANs\n500/600/700', 
                style='dotted', color='red')
        
        # Save diagram
        output_file = self.output_dir / 'IPv4_Task2_Style_Diagram'
        try:
            dot.render(output_file, view=False, cleanup=True)
            print(f"SUCCESS: Task 2 style IPv4 diagram saved: {output_file}.png")
            return output_file
        except Exception as e:
            print(f"Error saving diagram: {e}")
            # Save source for debugging
            with open(f"{output_file}.dot", 'w', encoding='utf-8') as f:
                f.write(dot.source)
            print(f"SUCCESS: Graphviz source saved: {output_file}.dot")
            return None


def main():
    """Generate Task 2 style network diagram"""
    print("=" * 70)
    print("Network Diagram Generator - Task 2 Style")
    print("=" * 70)
    
    if not GRAPHVIZ_AVAILABLE:
        print("\nWARNING: Graphviz library not found!")
        print("\nTo install:")
        print("  1. Install Python package: pip install graphviz")
        print("  2. Install Graphviz software: https://graphviz.org/download/")
        print("\nFor Windows:")
        print("  - Download from: https://graphviz.org/download/")
        print("  - Or use: winget install graphviz")
        print("  - Add to PATH: C:\\Program Files\\Graphviz\\bin")
        print("\nAfter installing, restart your terminal/IDE!")
        return
    
    generator = Task2StyleDiagramGenerator()
    
    print("\nGenerating Task 2 style diagram with IPv4 addressing...\n")
    
    result = generator.create_detailed_ipv4_diagram()
    
    if result:
        print("\n" + "=" * 70)
        print("SUCCESS: Diagram generated successfully!")
        print(f"Location: {result}.png")
        print("=" * 70)
    else:
        print("\nWARNING: Check for errors above")


if __name__ == "__main__":
    main()

