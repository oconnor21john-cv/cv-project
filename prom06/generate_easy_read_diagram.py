"""
Enhanced Network Diagram Generator - Easy to Read Task 2 Style
Creates highly readable network topology diagrams with improved layout
"""

try:
    from graphviz import Digraph
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("Note: Install graphviz for diagram generation: pip install graphviz")

from pathlib import Path


class EasyReadDiagramGenerator:
    """Generate easy-to-read network diagrams in Task 2 style"""
    
    def __init__(self, output_dir="prom06"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def create_easy_read_diagram(self):
        """Generate easy-to-read IPv4 network diagram"""
        if not GRAPHVIZ_AVAILABLE:
            print("Graphviz not available. Please install: pip install graphviz")
            return None
            
        dot = Digraph(comment='IPv4 Network - Easy Read', format='png')
        
        # Enhanced layout for readability
        dot.attr(rankdir='LR',  # Left to right for better horizontal space
                 splines='spline',  # Curved lines for clarity
                 nodesep='1.2', 
                 ranksep='2.0',
                 bgcolor='white', 
                 pad='0.5',
                 concentrate='false',  # Don't merge edges
                 overlap='false')
        
        dot.attr('node', fontname='Arial Bold', fontsize='10')
        dot.attr('edge', fontname='Arial', fontsize='9')
        
        # Professional color scheme
        router_color = '#1976D2'      # Blue
        switch_color = '#0288D1'      # Light blue  
        vlan_color = '#E3F2FD'        # Very light blue
        server_color = '#BBDEFB'      # Light blue
        isp_color = '#263238'         # Dark grey
        
        # ==================== ISP ROUTER ====================
        with dot.subgraph(name='cluster_isp') as isp:
            isp.attr(label='<<B>ISP AREA</B><BR/>Any Public IPs>',
                    style='filled,dashed', 
                    color='black', 
                    fillcolor='#ECEFF1',
                    penwidth='3',
                    fontsize='14')
            
            isp.node('ISP', 
                    label='''ISP ROUTER

G1/1/1: 203.0.113.22
  (to Area 1 - R1)

G1/1/2: 203.0.113.30
  (to Area 3 - R11)

G1/1/3: 203.0.113.26
  (to Area 2 - R7)''',
                    shape='cylinder',
                    fillcolor=isp_color,
                    fontcolor='white',
                    style='filled',
                    width='2.5',
                    height='1.5')
        
        # ==================== AREA 1: CLASS B ====================
        with dot.subgraph(name='cluster_area1') as area1:
            area1.attr(label='<<B>AREA 1: CLASS B</B><BR/><FONT POINT-SIZE="12">172.16.0.0/16</FONT>>',
                      style='filled,dashed',
                      color='#1976D2',
                      fillcolor='#E3F2FD',
                      penwidth='4',
                      fontsize='14')
            
            # Routers with cleaner layout
            area1.node('R1', 
                      label='''R1

G0/0: 203.0.113.6
G0/2: 203.0.113.9
G1/1/1: 203.0.113.21
  (to ISP)''',
                      shape='box',
                      style='filled,rounded',
                      fillcolor=router_color,
                      fontcolor='white')
            
            area1.node('R3',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#1976D2">
                      <TR><TD BGCOLOR="#1976D2"><FONT COLOR="white"><B>R3</B></FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/1: 172.16.0.1</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="8" COLOR="#1565C0">VLAN 4 Gateway</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/0: 172.16.7.1</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="8" COLOR="#1565C0">VLAN 5 Gateway</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="8" COLOR="#666666">P2P: .1, .18</FONT></TD></TR>
                      </TABLE>>',
                      shape='none')
            
            area1.node('R4',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#1976D2">
                      <TR><TD BGCOLOR="#1976D2"><FONT COLOR="white"><B>R4</B></FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/0: 203.0.113.5</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/1: 203.0.113.2</FONT></TD></TR>
                      </TABLE>>',
                      shape='none')
            
            area1.node('R5',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#1976D2">
                      <TR><TD BGCOLOR="#1976D2"><FONT COLOR="white"><B>R5</B></FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/0: 203.0.113.10</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/1: 203.0.113.13</FONT></TD></TR>
                      </TABLE>>',
                      shape='none')
            
            area1.node('R6',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#1976D2">
                      <TR><TD BGCOLOR="#1976D2"><FONT COLOR="white"><B>R6</B></FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/0: 203.0.113.14</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/1: 172.16.4.1</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="8" COLOR="#1565C0">VLANs 2 & 3</FONT></TD></TR>
                      </TABLE>>',
                      shape='none')
            
            # Switches
            area1.node('S2',
                      '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#0288D1"><TR><TD><FONT COLOR="white"><B>S2</B></FONT></TD></TR></TABLE>>',
                      shape='none')
            
            area1.node('S3',
                      '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#0288D1"><TR><TD><FONT COLOR="white"><B>S3</B></FONT></TD></TR><TR><TD><FONT POINT-SIZE="8">Trunk</FONT></TD></TR></TABLE>>',
                      shape='none')
            
            # VLANs with better formatting
            area1.node('VLAN4',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E3F2FD">
                      <TR><TD BGCOLOR="#90CAF9"><B>VLAN 4</B></TD></TR>
                      <TR><TD ALIGN="LEFT">Network: 172.16.0.0/22</TD></TR>
                      <TR><TD ALIGN="LEFT">Hosts: 1024</TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="8">Range: .0.1 - .3.254</FONT></TD></TR>
                      </TABLE>>',
                      shape='none')
            
            area1.node('VLAN5',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E3F2FD">
                      <TR><TD BGCOLOR="#90CAF9"><B>VLAN 5</B></TD></TR>
                      <TR><TD ALIGN="LEFT">Network: 172.16.7.0/30</TD></TR>
                      <TR><TD ALIGN="LEFT">Hosts: 2</TD></TR>
                      </TABLE>>',
                      shape='none')
            
            area1.node('VLAN2',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E3F2FD">
                      <TR><TD BGCOLOR="#90CAF9"><B>VLAN 2</B></TD></TR>
                      <TR><TD ALIGN="LEFT">Network: 172.16.4.0/23</TD></TR>
                      <TR><TD ALIGN="LEFT">Hosts: 400</TD></TR>
                      </TABLE>>',
                      shape='none')
            
            area1.node('VLAN3',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E3F2FD">
                      <TR><TD BGCOLOR="#90CAF9"><B>VLAN 3</B></TD></TR>
                      <TR><TD ALIGN="LEFT">Network: 172.16.6.0/24</TD></TR>
                      <TR><TD ALIGN="LEFT">Hosts: 250</TD></TR>
                      </TABLE>>',
                      shape='none')
        
        # ==================== AREA 2: CLASS C ====================
        with dot.subgraph(name='cluster_area2') as area2:
            area2.attr(label='<<B>AREA 2: CLASS C</B><BR/><FONT POINT-SIZE="12">192.168.0.0/16</FONT>>',
                      style='filled,dashed',
                      color='#388E3C',
                      fillcolor='#E8F5E9',
                      penwidth='4',
                      fontsize='14')
            
            # Routers
            area2.node('R7',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#1976D2">
                      <TR><TD BGCOLOR="#1976D2"><FONT COLOR="white"><B>R7</B></FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/0: 203.0.113.25</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="8" COLOR="#666666">(to ISP)</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/1: 203.0.113.33</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">VLAN 400: 192.168.0.1</FONT></TD></TR>
                      </TABLE>>',
                      shape='none')
            
            area2.node('R8',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#1976D2">
                      <TR><TD BGCOLOR="#1976D2"><FONT COLOR="white"><B>R8</B></FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/0: 203.0.113.34</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/1: 203.0.113.37</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">VLAN 100: .0.33</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">VLAN 200: .0.49</FONT></TD></TR>
                      </TABLE>>',
                      shape='none')
            
            area2.node('R9',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#1976D2">
                      <TR><TD BGCOLOR="#1976D2"><FONT COLOR="white"><B>R9</B></FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/0: 203.0.113.41</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/1: 203.0.113.38</FONT></TD></TR>
                      </TABLE>>',
                      shape='none')
            
            area2.node('R10',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#1976D2">
                      <TR><TD BGCOLOR="#1976D2"><FONT COLOR="white"><B>R10</B></FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/0: 203.0.113.42</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/1: 192.168.0.65</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="8" COLOR="#2E7D32">VLAN 300</FONT></TD></TR>
                      </TABLE>>',
                      shape='none')
            
            area2.node('R2',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#7B1FA2">
                      <TR><TD BGCOLOR="#7B1FA2"><FONT COLOR="white"><B>R2</B></FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/0: 203.0.113.17</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="8" COLOR="#666666">(to R3-Area1)</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/1: 192.168.0.73</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="8" COLOR="#2E7D32">VLAN 1</FONT></TD></TR>
                      </TABLE>>',
                      shape='none')
            
            # Switches
            area2.node('S1', '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#0288D1"><TR><TD><FONT COLOR="white"><B>S1</B></FONT></TD></TR></TABLE>>', shape='none')
            area2.node('S4', '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#0288D1"><TR><TD><FONT COLOR="white"><B>S4</B></FONT></TD></TR></TABLE>>', shape='none')
            area2.node('S8', '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#0288D1"><TR><TD><FONT COLOR="white"><B>S8</B></FONT></TD></TR></TABLE>>', shape='none')
            area2.node('S6', '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#0288D1"><TR><TD><FONT COLOR="white"><B>S6</B></FONT></TD></TR></TABLE>>', shape='none')
            area2.node('S5', '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#0288D1"><TR><TD><FONT COLOR="white"><B>S5</B></FONT></TD></TR></TABLE>>', shape='none')
            
            # VLANs
            area2.node('VLAN400',
                      '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E8F5E9"><TR><TD BGCOLOR="#81C784"><B>VLAN 400</B></TD></TR><TR><TD>192.168.0.0/27</TD></TR><TR><TD>18 hosts</TD></TR></TABLE>>',
                      shape='none')
            area2.node('VLAN100',
                      '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E8F5E9"><TR><TD BGCOLOR="#81C784"><B>VLAN 100</B></TD></TR><TR><TD>192.168.0.32/28</TD></TR><TR><TD>14 hosts</TD></TR></TABLE>>',
                      shape='none')
            area2.node('VLAN200',
                      '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E8F5E9"><TR><TD BGCOLOR="#81C784"><B>VLAN 200</B></TD></TR><TR><TD>192.168.0.48/28</TD></TR><TR><TD>12 hosts</TD></TR></TABLE>>',
                      shape='none')
            area2.node('VLAN300',
                      '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E8F5E9"><TR><TD BGCOLOR="#81C784"><B>VLAN 300</B></TD></TR><TR><TD>192.168.0.64/29</TD></TR><TR><TD>5 hosts</TD></TR></TABLE>>',
                      shape='none')
            area2.node('VLAN1',
                      '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#E8F5E9"><TR><TD BGCOLOR="#81C784"><B>VLAN 1</B></TD></TR><TR><TD>192.168.0.72/30</TD></TR><TR><TD>2 hosts</TD></TR></TABLE>>',
                      shape='none')
        
        # ==================== AREA 3: CLASS A ====================
        with dot.subgraph(name='cluster_area3') as area3:
            area3.attr(label='<<B>AREA 3: CLASS A</B><BR/><FONT POINT-SIZE="12">10.0.0.0/8</FONT>>',
                      style='filled,dashed',
                      color='#D32F2F',
                      fillcolor='#FFEBEE',
                      penwidth='4',
                      fontsize='14')
            
            # Routers
            area3.node('R11',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#1976D2">
                      <TR><TD BGCOLOR="#1976D2"><FONT COLOR="white"><B>R11</B></FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">G0/0: 203.0.113.29</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">VLAN 6: 10.130.0.1</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">VLAN 7: 10.132.96.1</FONT></TD></TR>
                      </TABLE>>',
                      shape='none')
            
            area3.node('R12',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#1976D2">
                      <TR><TD BGCOLOR="#1976D2"><FONT COLOR="white"><B>R12</B></FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">VLAN 8: 10.128.0.1</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">VLAN 9: 10.132.0.1</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">VLAN 11: 10.132.64.1</FONT></TD></TR>
                      </TABLE>>',
                      shape='none')
            
            area3.node('R13',
                      '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#1976D2">
                      <TR><TD BGCOLOR="#1976D2"><FONT COLOR="white"><B>R13</B></FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9">VLAN 10: 10.0.0.1</FONT></TD></TR>
                      <TR><TD ALIGN="LEFT"><FONT POINT-SIZE="8">VLANs 500/600/700</FONT></TD></TR>
                      </TABLE>>',
                      shape='none')
            
            # Key VLANs
            area3.node('VLAN10',
                      '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#FFEBEE"><TR><TD BGCOLOR="#E57373"><B>VLAN 10</B></TD></TR><TR><TD>10.0.0.0/9</TD></TR><TR><TD><B>5M hosts</B></TD></TR></TABLE>>',
                      shape='none')
            area3.node('VLAN6',
                      '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#FFEBEE"><TR><TD BGCOLOR="#E57373"><B>VLAN 6</B></TD></TR><TR><TD>10.130.0.0/15</TD></TR><TR><TD>202K hosts</TD></TR></TABLE>>',
                      shape='none')
            area3.node('VLAN8',
                      '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="#FFEBEE"><TR><TD BGCOLOR="#E57373"><B>VLAN 8</B></TD></TR><TR><TD>10.128.0.0/15</TD></TR><TR><TD>200K hosts</TD></TR></TABLE>>',
                      shape='none')
        
        # ==================== CONNECTIONS ====================
        
        # ISP connections - Bold red
        dot.edge('ISP', 'R1', label='<<B>203.0.113.20/30</B>>', color='#D32F2F', penwidth='3', style='bold')
        dot.edge('ISP', 'R7', label='<<B>203.0.113.24/30</B>>', color='#D32F2F', penwidth='3', style='bold')
        dot.edge('ISP', 'R11', label='<<B>203.0.113.28/30</B>>', color='#D32F2F', penwidth='3', style='bold')
        
        # Area 1 connections
        dot.edge('R1', 'R4', label='203.0.113.4/30', color='#1976D2', penwidth='2')
        dot.edge('R1', 'R5', label='203.0.113.8/30', color='#1976D2', penwidth='2')
        dot.edge('R4', 'R3', label='203.0.113.0/30', color='#1976D2', penwidth='2')
        dot.edge('R5', 'R6', label='203.0.113.12/30', color='#1976D2', penwidth='2')
        dot.edge('R5', 'S2', color='#0288D1', style='dashed')
        dot.edge('S2', 'R4', color='#0288D1', style='dashed')
        dot.edge('S2', 'R1', color='#0288D1', style='dashed')
        dot.edge('R3', 'VLAN4', color='#64B5F6', style='dotted')
        dot.edge('R3', 'VLAN5', color='#64B5F6', style='dotted')
        dot.edge('R6', 'S3', color='#0288D1', style='dashed')
        dot.edge('S3', 'VLAN2', color='#64B5F6', style='dotted')
        dot.edge('S3', 'VLAN3', color='#64B5F6', style='dotted')
        
        # Inter-area link
        dot.edge('R3', 'R2', label='<<B><FONT COLOR="#7B1FA2">Inter-Area</FONT></B><BR/>203.0.113.16/30>', 
                color='#7B1FA2', penwidth='3', style='bold')
        
        # Area 2 connections
        dot.edge('R7', 'R8', label='203.0.113.32/30', color='#388E3C', penwidth='2')
        dot.edge('R8', 'R9', label='203.0.113.36/30', color='#388E3C', penwidth='2')
        dot.edge('R9', 'R10', label='203.0.113.40/30', color='#388E3C', penwidth='2')
        dot.edge('R7', 'S1', color='#0288D1', style='dashed')
        dot.edge('S1', 'VLAN400', color='#81C784', style='dotted')
        dot.edge('R2', 'VLAN1', color='#81C784', style='dotted')
        dot.edge('R8', 'S4', color='#0288D1', style='dashed')
        dot.edge('S4', 'VLAN100', color='#81C784', style='dotted')
        dot.edge('R8', 'S8', color='#0288D1', style='dashed')
        dot.edge('S8', 'VLAN200', color='#81C784', style='dotted')
        dot.edge('R10', 'S6', color='#0288D1', style='dashed')
        dot.edge('S6', 'S5', label='Cascade', color='#0288D1', style='dashed')
        dot.edge('S6', 'VLAN300', color='#81C784', style='dotted')
        
        # Area 3 connections
        dot.edge('R11', 'R12', label='203.0.113.44/30', color='#D32F2F', penwidth='2')
        dot.edge('R12', 'R13', label='203.0.113.48/30', color='#D32F2F', penwidth='2')
        dot.edge('R11', 'VLAN6', color='#E57373', style='dotted')
        dot.edge('R12', 'VLAN8', color='#E57373', style='dotted')
        dot.edge('R13', 'VLAN10', color='#E57373', style='dotted')
        
        # Save diagram
        output_file = self.output_dir / 'IPv4_EasyRead_Diagram'
        try:
            dot.render(output_file, view=False, cleanup=True)
            print(f"SUCCESS: Easy-to-read diagram saved: {output_file}.png")
            return output_file
        except Exception as e:
            print(f"Error saving diagram: {e}")
            with open(f"{output_file}.dot", 'w', encoding='utf-8') as f:
                f.write(dot.source)
            print(f"Graphviz source saved: {output_file}.dot")
            return None


def main():
    """Generate easy-to-read network diagram"""
    print("=" * 70)
    print("Easy-to-Read Network Diagram Generator")
    print("=" * 70)
    
    if not GRAPHVIZ_AVAILABLE:
        print("\nWARNING: Graphviz library not found!")
        print("Please install: pip install graphviz")
        return
    
    generator = EasyReadDiagramGenerator()
    
    print("\nGenerating easy-to-read diagram...\n")
    
    result = generator.create_easy_read_diagram()
    
    if result:
        print("\n" + "=" * 70)
        print("SUCCESS: Diagram generated!")
        print(f"Location: {result}.png")
        print("=" * 70)
    else:
        print("\nCheck for errors above")


if __name__ == "__main__":
    main()

