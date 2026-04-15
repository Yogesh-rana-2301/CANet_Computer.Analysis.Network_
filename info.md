# Networking Full Forms and Definitions

This file is a comprehensive networking glossary for study and placement preparation.

## How to use this file 
Focus first on high-frequency interview terms: IP, TCP, UDP, DNS, HTTP, HTTPS, NAT, DHCP, VPN, VLAN, BGP.

## Core Internet and Web Terms

| Acronym | Full Form                                           | Definition                                                                                               |
| ------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| URL     | Uniform Resource Locator                            | The address used to locate a resource on the internet (for example, a web page, image, or API endpoint). |
| URI     | Uniform Resource Identifier                         | A general identifier for a resource; a URL is a type of URI.                                             |
| URN     | Uniform Resource Name                               | A URI that names a resource without specifying its location.                                             |
| WWW     | World Wide Web                                      | A system of interlinked web documents and resources accessed via the internet.                           |
| ISP     | Internet Service Provider                           | A company that provides internet connectivity to users and organizations.                                |
| IANA    | Internet Assigned Numbers Authority                 | Global coordinator for IP address allocation, protocol parameters, and DNS root zone management.         |
| ICANN   | Internet Corporation for Assigned Names and Numbers | Organization that oversees domain name and IP addressing coordination globally.                          |
| RFC     | Request for Comments                                | Official technical documents that define internet standards and protocols.                               |
| CDN     | Content Delivery Network                            | Distributed servers that cache and deliver content closer to users for lower latency.                    |

## Addressing, Naming, and Basic Network Concepts

| Acronym | Full Form                      | Definition                                                                                           |
| ------- | ------------------------------ | ---------------------------------------------------------------------------------------------------- |
| IP      | Internet Protocol              | Layer 3 protocol that provides logical addressing and routing of packets across networks.            |
| IPv4    | Internet Protocol version 4    | 32-bit addressing scheme, widely used, with limited address space.                                   |
| IPv6    | Internet Protocol version 6    | 128-bit addressing scheme designed to solve IPv4 address exhaustion and improve scalability.         |
| DNS     | Domain Name System             | Resolves domain names (like example.com) to IP addresses.                                            |
| FQDN    | Fully Qualified Domain Name    | Complete domain name that specifies exact location in DNS hierarchy (for example, host.example.com). |
| TLD     | Top-Level Domain               | Highest level in DNS namespace (for example, .com, .org, .in).                                       |
| TTL     | Time To Live                   | A field that limits packet lifetime or DNS cache duration to avoid stale routing/caching.            |
| MAC     | Media Access Control           | Hardware address used at Layer 2 for local network communication.                                    |
| ARP     | Address Resolution Protocol    | Maps IPv4 addresses to MAC addresses inside a local network.                                         |
| NDP     | Neighbor Discovery Protocol    | IPv6 mechanism for address resolution and neighbor/router discovery.                                 |
| CIDR    | Classless Inter-Domain Routing | Method for flexible IP allocation and route aggregation using prefix notation (for example, /24).    |
| Subnet  | Subnetwork                     | Logical subdivision of an IP network used for segmentation and routing control.                      |
| Gateway | Gateway                        | Device or node that connects different networks, often used as default exit path.                    |

## Models, Encapsulation, and Packet Structure

| Acronym | Full Form                                       | Definition                                                                              |
| ------- | ----------------------------------------------- | --------------------------------------------------------------------------------------- |
| OSI     | Open Systems Interconnection                    | 7-layer conceptual model used to understand and troubleshoot networking.                |
| TCP/IP  | Transmission Control Protocol/Internet Protocol | Practical protocol suite used on the internet.                                          |
| PDU     | Protocol Data Unit                              | Unit of data at a specific layer (for example, frame, packet, segment).                 |
| MTU     | Maximum Transmission Unit                       | Largest packet size (in bytes) that can be transmitted on a link without fragmentation. |
| MSS     | Maximum Segment Size                            | Largest TCP payload segment size, usually based on MTU.                                 |
| DF      | Don't Fragment                                  | IPv4 flag indicating packet should not be fragmented in transit.                        |

## Transport Layer Protocols

| Acronym | Full Form                            | Definition                                                                                              |
| ------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| TCP     | Transmission Control Protocol        | Reliable, connection-oriented transport protocol with sequencing, acknowledgements, and retransmission. |
| UDP     | User Datagram Protocol               | Lightweight, connectionless transport protocol optimized for low-latency communication.                 |
| SCTP    | Stream Control Transmission Protocol | Transport protocol supporting multi-streaming and multi-homing.                                         |
| QUIC    | Quick UDP Internet Connections       | Modern transport protocol over UDP with built-in TLS and improved handshake/latency.                    |
| RTO     | Retransmission Timeout               | TCP timer value used to decide when to retransmit unacknowledged data.                                  |
| ACK     | Acknowledgement                      | TCP mechanism confirming successful receipt of data.                                                    |
| SYN     | Synchronize                          | TCP flag used to initiate a connection.                                                                 |
| FIN     | Finish                               | TCP flag used to gracefully close a connection.                                                         |
| RST     | Reset                                | TCP flag used to abruptly terminate an invalid or unwanted connection.                                  |

## Routing and Network Control

| Acronym | Full Form                                  | Definition                                                                   |
| ------- | ------------------------------------------ | ---------------------------------------------------------------------------- |
| ICMP    | Internet Control Message Protocol          | Carries network error and diagnostic messages (used by ping and traceroute). |
| BGP     | Border Gateway Protocol                    | Path-vector routing protocol used for inter-domain routing on the internet.  |
| OSPF    | Open Shortest Path First                   | Link-state interior gateway routing protocol using SPF algorithm.            |
| RIP     | Routing Information Protocol               | Distance-vector interior routing protocol based on hop count.                |
| EIGRP   | Enhanced Interior Gateway Routing Protocol | Cisco-developed advanced interior routing protocol.                          |
| IGP     | Interior Gateway Protocol                  | Routing protocol used within a single autonomous system.                     |
| EGP     | Exterior Gateway Protocol                  | Routing protocol used between autonomous systems.                            |
| AS      | Autonomous System                          | Collection of networks under one administrative routing policy.              |
| ASN     | Autonomous System Number                   | Unique number assigned to an autonomous system for BGP routing.              |
| ECMP    | Equal-Cost Multi-Path                      | Technique for load sharing traffic over multiple equal-cost routes.          |
| VRF     | Virtual Routing and Forwarding             | Technology for multiple routing tables on one router for traffic isolation.  |

## Switching and LAN Technologies

| Acronym | Full Form                         | Definition                                                                          |
| ------- | --------------------------------- | ----------------------------------------------------------------------------------- |
| LAN     | Local Area Network                | Network covering a small geographic area such as office or campus.                  |
| WAN     | Wide Area Network                 | Network connecting geographically distant sites.                                    |
| MAN     | Metropolitan Area Network         | Network spanning a city or large campus region.                                     |
| WLAN    | Wireless Local Area Network       | Wireless local network typically based on Wi-Fi standards.                          |
| VLAN    | Virtual Local Area Network        | Logical Layer 2 segmentation that isolates broadcast domains.                       |
| STP     | Spanning Tree Protocol            | Prevents Layer 2 loops by creating a loop-free topology.                            |
| RSTP    | Rapid Spanning Tree Protocol      | Faster convergence version of STP.                                                  |
| LACP    | Link Aggregation Control Protocol | Bundles multiple physical links into one logical link for redundancy and bandwidth. |
| PoE     | Power over Ethernet               | Delivers power and data over the same Ethernet cable.                               |

## Address Translation, Access, and Service Discovery

| Acronym | Full Form                               | Definition                                                                            |
| ------- | --------------------------------------- | ------------------------------------------------------------------------------------- |
| NAT     | Network Address Translation             | Translates private IP addresses to public addresses (and vice versa) at network edge. |
| PAT     | Port Address Translation                | NAT type that maps many private hosts to one public IP using different ports.         |
| SNAT    | Source Network Address Translation      | Translates source IP address, usually for outbound traffic.                           |
| DNAT    | Destination Network Address Translation | Translates destination IP address, usually for inbound traffic.                       |
| DHCP    | Dynamic Host Configuration Protocol     | Automatically assigns IP configuration (IP, gateway, DNS, subnet mask) to hosts.      |
| APIPA   | Automatic Private IP Addressing         | Self-assigned IPv4 address range used when DHCP is unavailable.                       |
| mDNS    | Multicast DNS                           | Local-network DNS-style name resolution without a central DNS server.                 |
| DNS-SD  | DNS Service Discovery                   | Service discovery method built on DNS/mDNS records.                                   |

## Security and Encryption

| Acronym | Full Form                          | Definition                                                                         |
| ------- | ---------------------------------- | ---------------------------------------------------------------------------------- |
| HTTPS   | Hypertext Transfer Protocol Secure | HTTP over TLS encryption for secure web communication.                             |
| TLS     | Transport Layer Security           | Cryptographic protocol that secures data in transit.                               |
| SSL     | Secure Sockets Layer               | Legacy predecessor to TLS; now deprecated.                                         |
| PKI     | Public Key Infrastructure          | System of certificates, keys, and trusted authorities for identity and encryption. |
| CA      | Certificate Authority              | Trusted entity that issues and signs digital certificates.                         |
| CSR     | Certificate Signing Request        | Request generated to obtain a digital certificate from a CA.                       |
| VPN     | Virtual Private Network            | Encrypted tunnel across untrusted networks for private communication.              |
| IPsec   | Internet Protocol Security         | Suite of protocols securing IP traffic via authentication and encryption.          |
| AH      | Authentication Header              | IPsec protocol providing integrity/authentication (not encryption).                |
| ESP     | Encapsulating Security Payload     | IPsec protocol providing encryption, integrity, and authentication.                |
| IDS     | Intrusion Detection System         | Monitors traffic and alerts on suspicious activity.                                |
| IPS     | Intrusion Prevention System        | Detects and actively blocks malicious traffic.                                     |
| WAF     | Web Application Firewall           | Protects web apps by filtering HTTP traffic and common attacks.                    |
| ACL     | Access Control List                | Rule set that permits or denies traffic based on defined criteria.                 |
| DDoS    | Distributed Denial of Service      | Attack using many sources to overwhelm a target and disrupt service.               |

## Common Application Protocols

| Acronym   | Full Form                             | Definition                                                                 |
| --------- | ------------------------------------- | -------------------------------------------------------------------------- |
| HTTP      | Hypertext Transfer Protocol           | Stateless application protocol for web communication.                      |
| FTP       | File Transfer Protocol                | Legacy protocol for transferring files between client and server.          |
| SFTP      | SSH File Transfer Protocol            | Secure file transfer protocol running over SSH.                            |
| TFTP      | Trivial File Transfer Protocol        | Very simple UDP-based file transfer protocol with minimal features.        |
| SMTP      | Simple Mail Transfer Protocol         | Standard protocol for sending email.                                       |
| POP3      | Post Office Protocol version 3        | Email retrieval protocol that typically downloads mail locally.            |
| IMAP      | Internet Message Access Protocol      | Email retrieval protocol that keeps messages synchronized on server.       |
| SNMP      | Simple Network Management Protocol    | Protocol for monitoring and managing network devices.                      |
| NTP       | Network Time Protocol                 | Synchronizes system clocks across networked devices.                       |
| SSH       | Secure Shell                          | Encrypted remote login and command execution protocol.                     |
| Telnet    | Telnet                                | Legacy remote terminal protocol without encryption.                        |
| RDP       | Remote Desktop Protocol               | Microsoft protocol for remote graphical desktop access.                    |
| SIP       | Session Initiation Protocol           | Signaling protocol to establish/manage VoIP sessions.                      |
| RTP       | Real-time Transport Protocol          | Carries real-time media streams such as audio/video.                       |
| RTCP      | Real-time Transport Control Protocol  | Companion to RTP for quality feedback and stream control.                  |
| MQTT      | Message Queuing Telemetry Transport   | Lightweight publish-subscribe protocol for IoT and constrained networks.   |
| AMQP      | Advanced Message Queuing Protocol     | Open messaging protocol for reliable queue-based communication.            |
| CoAP      | Constrained Application Protocol      | Lightweight REST-like protocol for constrained IoT devices.                |
| LDAP      | Lightweight Directory Access Protocol | Protocol to query and manage directory services.                           |
| Kerberos  | Kerberos                              | Ticket-based authentication protocol for secure identity verification.     |
| WebSocket | WebSocket                             | Full-duplex persistent communication channel over a single TCP connection. |

## Wireless and Mobile Networking

| Acronym | Full Form                    | Definition                                                             |
| ------- | ---------------------------- | ---------------------------------------------------------------------- |
| Wi-Fi   | Wireless Fidelity            | Family of IEEE 802.11 wireless LAN technologies.                       |
| SSID    | Service Set Identifier       | Name of a wireless network.                                            |
| BSSID   | Basic Service Set Identifier | Unique MAC identifier of a specific wireless access point radio.       |
| WPA2    | Wi-Fi Protected Access 2     | Common Wi-Fi security standard using AES-based encryption.             |
| WPA3    | Wi-Fi Protected Access 3     | Newer Wi-Fi security standard with stronger authentication/encryption. |
| LTE     | Long-Term Evolution          | 4G mobile broadband technology.                                        |
| NR      | New Radio                    | 5G radio access technology.                                            |

## Cloud and Modern Networking

| Acronym | Full Form                        | Definition                                                                                 |
| ------- | -------------------------------- | ------------------------------------------------------------------------------------------ |
| VPC     | Virtual Private Cloud            | Logically isolated virtual network environment in cloud platforms.                         |
| VNet    | Virtual Network                  | Azure term for isolated virtual cloud network.                                             |
| ENI     | Elastic Network Interface        | Virtual network interface attached to cloud instances (AWS term).                          |
| SG      | Security Group                   | Stateful virtual firewall controlling instance-level traffic (cloud).                      |
| NACL    | Network Access Control List      | Subnet-level stateless traffic filter (cloud).                                             |
| IGW     | Internet Gateway                 | Cloud component enabling internet access for public subnet resources.                      |
| NAT GW  | NAT Gateway                      | Managed cloud NAT service for private subnet outbound internet access.                     |
| LB      | Load Balancer                    | Distributes client traffic across multiple backend servers/services.                       |
| ALB     | Application Load Balancer        | Layer 7 load balancer that routes by host/path and HTTP attributes.                        |
| NLB     | Network Load Balancer            | Layer 4 load balancer optimized for high performance and low latency.                      |
| SDN     | Software-Defined Networking      | Network control architecture where control plane is programmable/centralized.              |
| NFV     | Network Functions Virtualization | Runs network functions (firewall, router, etc.) as software on virtualized infrastructure. |

## Operations, Quality, and Troubleshooting

| Acronym     | Full Form                                 | Definition                                                                                      |
| ----------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------- |
| QoS         | Quality of Service                        | Traffic prioritization and policy controls to meet latency, jitter, and bandwidth requirements. |
| SLA         | Service Level Agreement                   | Contracted performance target (for example uptime, latency, availability).                      |
| RTT         | Round-Trip Time                           | Time taken for a packet to travel to destination and back.                                      |
| Jitter      | Jitter                                    | Variation in packet delay over time; important for voice/video quality.                         |
| Throughput  | Throughput                                | Actual data transfer rate achieved over a network.                                              |
| Bandwidth   | Bandwidth                                 | Maximum capacity of a network link to carry data.                                               |
| Packet Loss | Packet Loss                               | Percentage of packets that fail to reach destination.                                           |
| NOC         | Network Operations Center                 | Team/location responsible for network monitoring and incident response.                         |
| SIEM        | Security Information and Event Management | Centralized platform for collecting, correlating, and analyzing security logs/events.           |
| NetFlow     | NetFlow                                   | Flow-based traffic metadata export used for visibility and analysis.                            |
| sFlow       | Sampled Flow                              | Packet-sampling based traffic monitoring technology.                                            |

## Ports You Should Remember (Interview Quick List)

| Protocol/Service | Port    | Notes                                            |
| ---------------- | ------- | ------------------------------------------------ |
| HTTP             | 80      | Web traffic (unencrypted)                        |
| HTTPS            | 443     | Web traffic with TLS                             |
| DNS              | 53      | UDP mainly, TCP for larger replies/zone transfer |
| SSH              | 22      | Secure remote shell                              |
| Telnet           | 23      | Insecure legacy remote shell                     |
| FTP              | 21      | Control channel                                  |
| SMTP             | 25      | Mail transfer                                    |
| POP3             | 110     | Mail retrieval                                   |
| IMAP             | 143     | Mail retrieval/sync                              |
| DHCP             | 67/68   | Server/client ports                              |
| SNMP             | 161/162 | Management/traps                                 |
| NTP              | 123     | Time sync                                        |
| LDAP             | 389     | Directory access                                 |
| LDAPS            | 636     | LDAP over TLS                                    |
| RDP              | 3389    | Remote desktop                                   |
| MQTT             | 1883    | Default plaintext MQTT                           |
| MQTTS            | 8883    | MQTT over TLS                                    |

## Placement Revision Strategy

1. Day 1: IP, TCP, UDP, DNS.
2. Day 2: HTTP/HTTPS, TLS, ports.
3. Day 3: Subnet, VLAN, routing protocols, NAT.
4. Day 4: VPN, firewalls, IDS/IPS, ACL.
5. Day 5: Cloud networking terms (VPC, SG, NACL, IGW, NAT GW, LB).
6. Day 6: Wireless + troubleshooting terms (RTT, jitter, loss, throughput).
7. Day 7: Mock interview with rapid-fire definitions.

If you can define each acronym in one sentence with one practical example, your networking fundamentals are interview-ready.
