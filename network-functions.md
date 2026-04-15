# Network Functions (Quick Notes)

This file explains the function of important networking items in simple interview-ready language.

## 1. Core Services

### DHCP (Dynamic Host Configuration Protocol)

Function:

- Automatically gives devices network settings.
- Assigns IP address, subnet mask, default gateway, and DNS server.

Why important:

- Without DHCP, every device must be configured manually.

Common ports:

- UDP 67 (server), UDP 68 (client)

### DNS (Domain Name System)

Function:

- Translates domain names to IP addresses.

Why important:

- Humans remember names, but networks route using IP addresses.

Common port:

- UDP 53 (most queries), TCP 53 (zone transfer or large responses)

### NAT (Network Address Translation)

Function:

- Translates private IP addresses to public IP addresses and back.

Why important:

- Saves public IPv4 addresses and hides internal network structure.

### ARP (Address Resolution Protocol)

Function:

- Finds the MAC address for a known IPv4 address inside a local network.

Why important:

- Local delivery needs MAC addresses, not only IP addresses.

## 2. Transport and Internet Protocols

### TCP (Transmission Control Protocol)

Function:

- Reliable, ordered, connection-oriented data delivery.

Why important:

- Used when data must arrive correctly (web logins, file transfer, banking).

### UDP (User Datagram Protocol)

Function:

- Fast, connectionless transport with low overhead.

Why important:

- Useful for real-time traffic where speed matters more than perfect reliability.

### ICMP (Internet Control Message Protocol)

Function:

- Carries network error and diagnostic messages.

Why important:

- Used by tools like ping and traceroute for troubleshooting.

### HTTP / HTTPS

Function:

- HTTP transfers web data.
- HTTPS does the same with TLS encryption.

Why important:

- HTTPS protects confidentiality and integrity of web traffic.

Common ports:

- HTTP: TCP 80
- HTTPS: TCP 443

## 3. Network Devices and Their Functions

### Switch

Function:

- Connects devices in the same LAN and forwards frames using MAC addresses.

### Router

Function:

- Connects different networks and forwards packets using IP routing.

### Firewall

Function:

- Allows or blocks traffic based on security rules (IP, port, protocol, direction).

### Access Point (AP)

Function:

- Provides Wi-Fi access and bridges wireless clients into the LAN.

### Load Balancer

Function:

- Distributes incoming traffic across multiple servers.

Why important:

- Improves performance, scalability, and availability.

## 4. Quick Interview One-Liners

- DHCP gives IP configuration automatically.
- DNS converts names to IP addresses.
- NAT lets private hosts share public internet access.
- ARP maps IPv4 addresses to MAC addresses in a LAN.
- TCP is reliable and ordered; UDP is faster with less overhead.
- A switch works mainly inside a LAN; a router connects networks.
- A firewall enforces traffic security policy.
