# 🌐 Application Layer — Study Guide Index

> **OSI Layer 7** ⭐ HIGH PRIORITY — Directly user-facing protocols that appear in almost every interview!
> The Application Layer provides network services directly to end-user applications.

---

## 📚 Files in This Section

| File | Topics |
|------|--------|
| [01_DNS.md](./01_DNS.md) | DNS working, Recursive vs Iterative, Hierarchy, Caching |
| [02_HTTP_HTTPS.md](./02_HTTP_HTTPS.md) | HTTP methods, Status codes, HTTPS, Cookies vs Sessions |
| [03_Other_Protocols.md](./03_Other_Protocols.md) | FTP, SMTP, DHCP |

---

## 🔑 What the Application Layer Does

```
User/Application
      │
      ▼
┌──────────────────────────────────────┐
│        Application Layer (L7)        │
│  DNS, HTTP, FTP, SMTP, DHCP, SSH...  │
└──────────────────────────────────────┘
      │
      ▼
Transport Layer (TCP/UDP)
```

The Application Layer:
- Provides an interface between the **network and the application**
- Defines protocols for **specific services** (web, email, file transfer, naming)
- Uses Transport Layer (TCP/UDP) for actual data delivery

---

## ⚡ Application Layer Quick Cheat Sheet

| Protocol | Port | Transport | Purpose |
|---------|------|-----------|---------|
| **DNS** | 53 | UDP (mostly) / TCP | Domain name → IP resolution |
| **HTTP** | 80 | TCP | Web page transfer |
| **HTTPS** | 443 | TCP | Encrypted web transfer |
| **FTP** | 20 (data), 21 (control) | TCP | File transfer |
| **SMTP** | 25 / 587 | TCP | Sending email |
| **POP3** | 110 | TCP | Receiving email (download) |
| **IMAP** | 143 | TCP | Receiving email (sync) |
| **DHCP** | 67 (server), 68 (client) | UDP | Auto IP assignment |
| **SSH** | 22 | TCP | Secure remote shell |
| **Telnet** | 23 | TCP | Remote shell (insecure) |
| **SNMP** | 161 | UDP | Network management |

---

## 🧭 Protocol Relationship Map

```
Browser types: www.google.com
         │
         ▼
     DNS (port 53)         → resolves to 142.250.68.46
         │
         ▼
   HTTP/HTTPS (80/443)     → fetches the web page
         │
         ▼
     TCP (reliable)        → ensures delivery
         │
         ▼
     IP (routing)          → finds the path
         │
         ▼
   Ethernet (frames)       → delivers on local link
```

---

*Start with [01 — DNS →](./01_DNS.md)*
