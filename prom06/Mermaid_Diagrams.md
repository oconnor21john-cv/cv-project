# Network Diagrams - Mermaid Format

These diagrams render automatically in GitHub, VS Code (with Mermaid extension), and many other tools.

## Network Overview

```mermaid
graph LR
    A1[Area 1<br/>Class B<br/>172.16.0.0/16<br/>4 VLANs]
    ISP[ISP<br/>Central Hub<br/>203.0.113.0/24]
    A2[Area 2<br/>Class C<br/>192.168.0.0/16<br/>5 VLANs]
    A3[Area 3<br/>Class A<br/>10.0.0.0/8<br/>9 VLANs]
    
    A1 ---|R1-ISP| ISP
    A2 ---|R7-ISP| ISP
    A3 ---|R11-ISP| ISP
    
    style A1 fill:#81D4FA
    style A2 fill:#A5D6A7
    style A3 fill:#FFCC80
    style ISP fill:#EF9A9A
```

---

## IPv4 Network Topology - Area 1 Detail

```mermaid
graph TB
    subgraph Area1["Area 1: Class B (172.16.0.0/16)"]
        R1[R1<br/>Gateway Router]
        R3[R3<br/>VLAN 4: 172.16.0.1<br/>VLAN 5: 172.16.7.1]
        R4[R4<br/>Aggregation]
        R5[R5<br/>Distribution]
        R6[R6<br/>VLAN 2: 172.16.4.1<br/>VLAN 3: 172.16.6.1]
        S2[S2<br/>Switch]
        S3[S3<br/>Switch]
        
        V4[VLAN 4<br/>172.16.0.0/22<br/>1024 hosts]
        V5[VLAN 5<br/>172.16.7.0/30<br/>2 hosts]
        V2[VLAN 2<br/>172.16.4.0/23<br/>400 hosts]
        V3[VLAN 3<br/>172.16.6.0/24<br/>250 hosts]
    end
    
    ISP[ISP Router]
    
    ISP -->|203.0.113.20/30| R1
    R1 -->|203.0.113.4/30| R4
    R1 -->|203.0.113.8/30| R5
    R4 -->|203.0.113.0/30| R3
    R5 --> S2
    R5 -->|203.0.113.12/30| R6
    S2 --> R4
    S2 --> R3
    R3 --> V4
    R3 --> V5
    R6 --> S3
    S3 --> V2
    S3 --> V3
    
    style R1 fill:#E8F4F8
    style R3 fill:#E8F4F8
    style R4 fill:#E8F4F8
    style R5 fill:#E8F4F8
    style R6 fill:#E8F4F8
    style S2 fill:#FFF4E6
    style S3 fill:#FFF4E6
    style V4 fill:#E8F5E9
    style V5 fill:#E8F5E9
    style V2 fill:#E8F5E9
    style V3 fill:#E8F5E9
    style ISP fill:#FFE6E6
```

---

## IPv4 Network Topology - Area 2 Detail

```mermaid
graph TB
    subgraph Area2["Area 2: Class C (192.168.0.0/16)"]
        R7[R7<br/>VLAN 400: 192.168.0.1]
        R8[R8<br/>VLAN 100: 192.168.0.33<br/>VLAN 200: 192.168.0.49]
        R9[R9<br/>Transit]
        R10[R10<br/>VLAN 300: 192.168.0.65]
        
        S1[S1]
        S4[S4]
        S8[S8]
        S6[S6]
        
        V400[VLAN 400<br/>192.168.0.0/27<br/>18 hosts]
        V100[VLAN 100<br/>192.168.0.32/28<br/>14 hosts]
        V200[VLAN 200<br/>192.168.0.48/28<br/>12 hosts]
        V300[VLAN 300<br/>192.168.0.64/29<br/>5 hosts]
    end
    
    ISP[ISP Router]
    
    ISP -->|203.0.113.24/30| R7
    R7 -->|203.0.113.32/30| R8
    R8 -->|203.0.113.36/30| R9
    R9 -->|203.0.113.40/30| R10
    
    R7 --> S1
    S1 --> V400
    R8 --> S4
    S4 --> V100
    R8 --> S8
    S8 --> V200
    R10 --> S6
    S6 --> V300
    
    style R7 fill:#E8F4F8
    style R8 fill:#E8F4F8
    style R9 fill:#E8F4F8
    style R10 fill:#E8F4F8
    style S1 fill:#FFF4E6
    style S4 fill:#FFF4E6
    style S8 fill:#FFF4E6
    style S6 fill:#FFF4E6
    style V400 fill:#E8F5E9
    style V100 fill:#E8F5E9
    style V200 fill:#E8F5E9
    style V300 fill:#E8F5E9
    style ISP fill:#FFE6E6
```

---

## IPv4 Network Topology - Area 3 Detail

```mermaid
graph TB
    subgraph Area3["Area 3: Class A (10.0.0.0/8)"]
        R11[R11<br/>VLAN 6: 10.130.0.1<br/>VLAN 7: 10.132.96.1]
        R12[R12<br/>VLAN 8: 10.128.0.1<br/>VLAN 9: 10.132.0.1<br/>VLAN 11: 10.132.64.1]
        R13[R13<br/>VLAN 10: 10.0.0.1]
        
        S7[S7]
        S9[S9]
        
        V10[VLAN 10<br/>10.0.0.0/9<br/>5M hosts]
        V6[VLAN 6<br/>10.130.0.0/15<br/>202K hosts]
        V7[VLAN 7<br/>10.132.96.0/21<br/>2K hosts]
        V8[VLAN 8<br/>10.128.0.0/15<br/>200K hosts]
        V11[VLAN 11<br/>10.132.64.0/19<br/>5K hosts]
    end
    
    ISP[ISP Router]
    
    ISP -->|203.0.113.28/30| R11
    R11 -->|203.0.113.44/30| R12
    R12 -->|203.0.113.48/30| R13
    
    R11 --> S7
    S7 --> V6
    S7 --> V7
    R12 --> V8
    R12 --> V11
    R13 --> S9
    S9 --> V10
    
    style R11 fill:#E8F4F8
    style R12 fill:#E8F4F8
    style R13 fill:#E8F4F8
    style S7 fill:#FFF4E6
    style S9 fill:#FFF4E6
    style V10 fill:#E8F5E9
    style V6 fill:#E8F5E9
    style V7 fill:#E8F5E9
    style V8 fill:#E8F5E9
    style V11 fill:#E8F5E9
    style ISP fill:#FFE6E6
```

---

## IPv6 Network Overview

```mermaid
graph TB
    subgraph IPv6["IPv6 Addressing (2001:db8::/32)"]
        A1[Area 1<br/>2001:db8:1000::/36<br/>4 x /64 subnets]
        A2[Area 2<br/>2001:db8:2000::/36<br/>5 x /64 subnets]
        A3[Area 3<br/>2001:db8:3000::/36<br/>9 x /64 subnets]
        ISP[ISP<br/>P2P Links<br/>2001:db8:ff00::/48<br/>13 x /127 subnets]
    end
    
    A1 ---|2001:db8:ff00::14/127| ISP
    A2 ---|2001:db8:ff00::16/127| ISP
    A3 ---|2001:db8:ff00::18/127| ISP
    
    style A1 fill:#E1F5FE
    style A2 fill:#F1F8E9
    style A3 fill:#FFE0B2
    style ISP fill:#FFEBEE
```

---

## Complete Network Hierarchy

```mermaid
graph TB
    Internet[Internet]
    
    ISP[ISP Router<br/>Central Hub]
    
    Internet --> ISP
    
    subgraph Area1["Area 1: Class B"]
        R1_A1[R1] --> R4_A1[R4]
        R1_A1 --> R5_A1[R5]
        R4_A1 --> R3_A1[R3]
        R5_A1 --> R6_A1[R6]
        R3_A1 --> VLAN4[VLAN 4: 1024h]
        R6_A1 --> VLAN2[VLAN 2: 400h]
    end
    
    subgraph Area2["Area 2: Class C"]
        R7_A2[R7] --> R8_A2[R8]
        R8_A2 --> R9_A2[R9]
        R9_A2 --> R10_A2[R10]
        R7_A2 --> VLAN400[VLAN 400: 18h]
        R8_A2 --> VLAN100[VLAN 100: 14h]
    end
    
    subgraph Area3["Area 3: Class A"]
        R11_A3[R11] --> R12_A3[R12]
        R12_A3 --> R13_A3[R13]
        R11_A3 --> VLAN6[VLAN 6: 202Kh]
        R13_A3 --> VLAN10[VLAN 10: 5Mh]
    end
    
    ISP --> R1_A1
    ISP --> R7_A2
    ISP --> R11_A3
    
    style Area1 fill:#E3F2FD
    style Area2 fill:#F1F8E9
    style Area3 fill:#FFF3E0
    style ISP fill:#FFEBEE
```

---

## VLAN Distribution Across Areas

```mermaid
pie title "Host Distribution by Area"
    "Area 1 (1,676)" : 1676
    "Area 2 (51)" : 51
    "Area 3 (5,419,140)" : 5419140
```

```mermaid
pie title "Number of VLANs per Area"
    "Area 1" : 4
    "Area 2" : 5
    "Area 3" : 9
```

---

## Router Interconnection Map

```mermaid
graph LR
    subgraph core["Core Layer"]
        ISP[ISP<br/>Hub]
    end
    
    subgraph dist["Distribution Layer"]
        R1[R1<br/>Area 1]
        R7[R7<br/>Area 2]
        R11[R11<br/>Area 3]
    end
    
    subgraph access["Access Layer"]
        R3[R3]
        R6[R6]
        R8[R8]
        R10[R10]
        R12[R12]
        R13[R13]
    end
    
    ISP ---|P2P /30| R1
    ISP ---|P2P /30| R7
    ISP ---|P2P /30| R11
    
    R1 --> R3
    R1 --> R6
    R7 --> R8
    R7 --> R10
    R11 --> R12
    R11 --> R13
    
    style ISP fill:#EF9A9A
    style R1 fill:#81D4FA
    style R7 fill:#A5D6A7
    style R11 fill:#FFCC80
```

---

## IPv4 vs IPv6 Comparison

```mermaid
graph TB
    subgraph IPv4["IPv4 Design"]
        A1v4[Area 1<br/>172.16.0.0/16<br/>VLSM: /22 to /30]
        A2v4[Area 2<br/>192.168.0.0/16<br/>VLSM: /27 to /30]
        A3v4[Area 3<br/>10.0.0.0/8<br/>VLSM: /9 to /27]
        P2Pv4[P2P Links<br/>203.0.113.0/24<br/>All /30]
    end
    
    subgraph IPv6["IPv6 Design"]
        A1v6[Area 1<br/>2001:db8:1000::/36<br/>All /64]
        A2v6[Area 2<br/>2001:db8:2000::/36<br/>All /64]
        A3v6[Area 3<br/>2001:db8:3000::/36<br/>All /64]
        P2Pv6[P2P Links<br/>2001:db8:ff00::/48<br/>All /127]
    end
    
    A1v4 -.Maps to.-> A1v6
    A2v4 -.Maps to.-> A2v6
    A3v4 -.Maps to.-> A3v6
    P2Pv4 -.Maps to.-> P2Pv6
    
    style IPv4 fill:#BBDEFB
    style IPv6 fill:#C8E6C9
```

---

## Viewing Instructions

### In VS Code:
1. Install "Markdown Preview Mermaid Support" extension
2. Open this file
3. Press `Ctrl+Shift+V` (or `Cmd+Shift+V` on Mac) for preview

### In GitHub:
- These diagrams render automatically when viewing this file on GitHub

### Online Viewer:
- Visit: https://mermaid.live/
- Copy/paste any diagram code

### Export as Image:
1. Go to https://mermaid.live/
2. Paste diagram code
3. Click "Download PNG" or "Download SVG"

---

## Customization

To modify these diagrams:
1. Edit the text between the triple backticks
2. Adjust node names, labels, or connections
3. Change colors with `style` commands
4. Add new nodes or subgraphs as needed

Mermaid syntax guide: https://mermaid.js.org/

---

*Generated: October 26, 2025*

