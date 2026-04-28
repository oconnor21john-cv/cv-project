# IPv6 Addressing Scheme Table

## Area 1: IPv6 Network (2001:db8:1000::/36)

### Router-to-ISP and Point-to-Point Links

| Connection | Network Address | Prefix | Usable IPs | Interface 1 | Interface 2 | Purpose |
|------------|----------------|--------|------------|-------------|-------------|---------|
| ISP ↔ R1 | 2001:db8:1000::/127 | /127 | 2 | ISP: 2001:db8:1000::1 | R1 G0/0: 2001:db8:1000::0 | ISP Connection |
| R2 ↔ Server1 | 2001:db8:1000:10::/127 | /127 | 2 | R2 G0/1: 2001:db8:1000:10::0 | Server: 2001:db8:1000:10::1 | Server Link |
| R4 ↔ Server2 | 2001:db8:1000:11::/127 | /127 | 2 | R4 G0/1: 2001:db8:1000:11::0 | Server: 2001:db8:1000:11::1 | Server Link |
| R5 ↔ R6 | 2001:db8:1000:12::/127 | /127 | 2 | R5 G0/1: 2001:db8:1000:12::0 | R6 G0/0: 2001:db8:1000:12::1 | Router Link |

### Switch Management Networks

| Switch | Network Address | Prefix | Usable IPs | Gateway | Switch IP | Connected Router |
|--------|----------------|--------|------------|---------|-----------|------------------|
| S1 | 2001:db8:1000:1::/64 | /64 | 18.4 quintillion | R1 G0/1: 2001:db8:1000:1::1 | 2001:db8:1000:1::2 | R1 |
| S2 | 2001:db8:1000:2::/64 | /64 | 18.4 quintillion | R1 G0/2: 2001:db8:1000:2::1 | 2001:db8:1000:2::2 | R1 |
| S3a | 2001:db8:1000:3::/64 | /64 | 18.4 quintillion | R3 G0/1: 2001:db8:1000:3::1 | 2001:db8:1000:3::2 | R3 |
| S3b | 2001:db8:1000:4::/64 | /64 | 18.4 quintillion | R6 G0/1: 2001:db8:1000:4::1 | 2001:db8:1000:4::2 | R6 |

### VLANs (Area 1)

| VLAN | Hosts Required | Network Address | Prefix | Address Space | Gateway | First Host IP | Example Host Range | Switch |
|------|----------------|-----------------|--------|---------------|---------|---------------|-------------------|--------|
| VLAN 2 | 400 | 2001:db8:1000:20::/64 | /64 | 18.4 quintillion | 2001:db8:1000:20::1 | 2001:db8:1000:20::2 | ::2 to ::191 (400 addresses) | S3a |
| VLAN 3 | 250 | 2001:db8:1000:22::/64 | /64 | 18.4 quintillion | 2001:db8:1000:22::1 | 2001:db8:1000:22::2 | ::2 to ::fb (250 addresses) | S3a |
| VLAN 4 | 1024 | 2001:db8:1000:24::/64 | /64 | 18.4 quintillion | 2001:db8:1000:24::1 | 2001:db8:1000:24::2 | ::2 to ::401 (1024 addresses) | S3b |
| VLAN 5 | 505 | 2001:db8:1000:28::/64 | /64 | 18.4 quintillion | 2001:db8:1000:28::1 | 2001:db8:1000:28::2 | ::2 to ::1fa (505 addresses) | S3b |

---

## Area 2: IPv6 Network (2001:db8:2000::/36)

### Router-to-ISP Links

| Connection | Network Address | Prefix | Usable IPs | Interface 1 | Interface 2 | Purpose |
|------------|----------------|--------|------------|-------------|-------------|---------|
| ISP ↔ R7 | 2001:db8:2000::/127 | /127 | 2 | ISP: 2001:db8:2000::1 | R7 G0/1: 2001:db8:2000::0 | ISP Connection |

### L3 Switch VLANs and Router Connections

| VLAN/Network | Hosts Required | Network Address | Prefix | Address Space | Gateway/Interface 1 | Interface 2 | Connected Device |
|--------------|----------------|-----------------|--------|---------------|---------------------|-------------|------------------|
| VLAN 400 | 18 | 2001:db8:2000:400::/64 | /64 | 18.4 quintillion | L3-3: 2001:db8:2000:400::1 | R7 G0/0: 2001:db8:2000:400::2 | R7 |
| VLAN 300 | 5 | 2001:db8:2000:300::/64 | /64 | 18.4 quintillion | L3-3: 2001:db8:2000:300::1 | R10 G0/0: 2001:db8:2000:300::2 | R10 |
| VLAN 1 | 2 | 2001:db8:2000:1::/127 | /127 | 2 | L3-3: 2001:db8:2000:1::0 | L3-2: 2001:db8:2000:1::1 | L3-2 |
| VLAN 200 | 12 | 2001:db8:2000:200::/64 | /64 | 18.4 quintillion | L3-2: 2001:db8:2000:200::1 | R9 G0/0: 2001:db8:2000:200::2 | R9 |
| VLAN 100 | 8 | 2001:db8:2000:100::/64 | /64 | 18.4 quintillion | L3-2: 2001:db8:2000:100::1 | R8 G0/0: 2001:db8:2000:100::2 | R8 |

### Switch Networks (Area 2)

| Switch | Hosts Required | Network Address | Prefix | Address Space | Gateway | First Host IP | Example Range | Router |
|--------|----------------|-----------------|--------|---------------|---------|---------------|---------------|--------|
| S6 | 25 | 2001:db8:2000:10::/64 | /64 | 18.4 quintillion | R10 G0/1: 2001:db8:2000:10::1 | 2001:db8:2000:10::2 | ::2 to ::1a (25 addresses) | R10 |
| S5 | 60 | 2001:db8:2000:11::/64 | /64 | 18.4 quintillion | R9 G0/1: 2001:db8:2000:11::1 | 2001:db8:2000:11::2 | ::2 to ::3d (60 addresses) | R9 |
| S4 | 14 | 2001:db8:2000:12::/64 | /64 | 18.4 quintillion | R8 G0/1: 2001:db8:2000:12::1 | 2001:db8:2000:12::2 | ::2 to ::f (14 addresses) | R8 |

---

## Area 3: IPv6 Network (2001:db8:3000::/36)

### Router-to-ISP Links

| Connection | Network Address | Prefix | Usable IPs | Interface 1 | Interface 2 | Purpose |
|------------|----------------|--------|------------|-------------|-------------|---------|
| ISP ↔ R11 | 2001:db8:3000::/127 | /127 | 2 | ISP: 2001:db8:3000::1 | R11 G0/0: 2001:db8:3000::0 | ISP Connection |

### L3 Switch VLANs and Router Connections

| VLAN | Hosts Required | Network Address | Prefix | Address Space | Gateway/Interface 1 | Interface 2 | Connected Device |
|------|----------------|-----------------|--------|---------------|---------------------|-------------|------------------|
| VLAN 500 | 20 | 2001:db8:3000:500::/64 | /64 | 18.4 quintillion | L3-1: 2001:db8:3000:500::1 | R11 G0/2: 2001:db8:3000:500::2 | R11 |
| VLAN 700 | 80 | 2001:db8:3000:700::/64 | /64 | 18.4 quintillion | L3-1: 2001:db8:3000:700::1 | R12 G0/0: 2001:db8:3000:700::2 | R12 |
| VLAN 600 | 40 | 2001:db8:3000:600::/64 | /64 | 18.4 quintillion | L3-1: 2001:db8:3000:600::1 | R13 G0/0: 2001:db8:3000:600::2 | R13 |

### Large VLANs (Area 3)

| VLAN | Hosts Required | Network Address | Prefix | Total Address Space | Gateway | First Host IP | Address Range | Switch |
|------|----------------|-----------------|--------|---------------------|---------|---------------|---------------|--------|
| VLAN 6 | 202,000 | 2001:db8:3000:6::/48 | /48 | 1.2 × 10¹⁹ addresses | 2001:db8:3000:6::1 | 2001:db8:3000:6::2 | 2001:db8:3000:6:0:0:0:2 to 2001:db8:3000:6:ffff:ffff:ffff:fffe | S7 |
| VLAN 7 | 2,000 | 2001:db8:3000:7::/64 | /64 | 18.4 quintillion | 2001:db8:3000:7::1 | 2001:db8:3000:7::2 | ::2 to ::7d1 (2000 addresses) | S7 |
| VLAN 8 | 200,000 | 2001:db8:3000:8::/48 | /48 | 1.2 × 10¹⁹ addresses | 2001:db8:3000:8::1 | 2001:db8:3000:8::2 | 2001:db8:3000:8:0:0:0:2 to 2001:db8:3000:8:ffff:ffff:ffff:fffe | S8 |
| VLAN 9 | 10,000 | 2001:db8:3000:9::/64 | /64 | 18.4 quintillion | 2001:db8:3000:9::1 | 2001:db8:3000:9::2 | ::2 to ::2711 (10000 addresses) | S8 |
| VLAN 10 | 5,000,000 | 2001:db8:3000:a::/40 | /40 | 3.1 × 10²³ addresses | 2001:db8:3000:a::1 | 2001:db8:3000:a::2 | 2001:db8:3000:a:0:0:0:2 to 2001:db8:3000:a:ff:ffff:ffff:fffe | S9 |
| VLAN 11 | 5,000 | 2001:db8:3000:b::/64 | /64 | 18.4 quintillion | 2001:db8:3000:b::1 | 2001:db8:3000:b::2 | ::2 to ::1389 (5000 addresses) | S9 |

---

## IPv6 Prefix Length Reference

| Prefix | Address Space | Typical Use |
|--------|---------------|-------------|
| /127 | 2 addresses | Point-to-point links (RFC 6164) |
| /64 | 18,446,744,073,709,551,616 (18.4 quintillion) | Standard subnet for hosts |
| /48 | 1,208,925,819,614,629,174,706,176 (1.2 × 10¹⁹) | Large organization subnet |
| /40 | 309,485,009,821,345,068,724,781,056 (3.1 × 10²³) | Extremely large networks |
| /36 | 4,951,760,157,141,521,099,596,496,896 (5.0 × 10²⁴) | Area allocation |

---

## Summary Statistics

### Area 1 (2001:db8:1000::/36)
- **Total Subnets**: 12
- **Prefix Lengths Used**: /127, /64
- **Total Addressable Hosts**: Virtually unlimited (billions per subnet)
- **Design Philosophy**: Standard /64 for all host networks, /127 for point-to-point

### Area 2 (2001:db8:2000::/36)
- **Total Subnets**: 9
- **Prefix Lengths Used**: /127, /64
- **Total Addressable Hosts**: Virtually unlimited
- **Design Philosophy**: Consistent /64 allocation, simplified addressing

### Area 3 (2001:db8:3000::/36)
- **Total Subnets**: 10
- **Prefix Lengths Used**: /127, /40, /48, /64
- **Total Addressable Hosts**: Virtually unlimited (even for 5M+ host VLANs)
- **Design Philosophy**: /48 for massive VLANs, /40 for extreme cases, /64 standard

### Overall IPv6 Network
- **Base Prefix**: 2001:db8::/32 (Documentation prefix)
- **Total Subnets**: 31
- **Hierarchical Structure**: Yes (by area)
- **SLAAC Support**: Yes (all /64 subnets)
- **DHCPv6 Compatible**: Yes
- **Future-Proof**: Extremely scalable with massive address space

---

## IPv6 Advantages Demonstrated

1. **No Address Exhaustion**: Even VLAN 10 with 5 million hosts uses only a tiny fraction of a /64
2. **Simplified Subnetting**: Standard /64 for nearly everything eliminates complex calculations
3. **Hierarchical Addressing**: Clean area-based allocation (1000, 2000, 3000)
4. **Auto-Configuration**: SLAAC capable on all host networks
5. **No NAT Required**: True end-to-end connectivity
6. **Easy to Remember**: Logical numbering scheme (VLAN IDs in hex)

---

## Configuration Methods

### Static Assignment
- Infrastructure devices (routers, L3 switches)
- Gateways (always ::1 in subnet)
- Servers

### SLAAC (Stateless Address Autoconfiguration)
- Client devices
- Automatic configuration from router advertisements
- Privacy extensions available (RFC 4941)

### DHCPv6 (Stateful)
- When additional options needed (DNS, NTP, etc.)
- Centralized management
- Can work alongside SLAAC

