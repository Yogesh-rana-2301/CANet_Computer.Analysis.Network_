# 🔐 Network Security — Study Guide Index

> Security is a cross-cutting concern across ALL layers of the network stack.

---

## 📚 Files in This Section

| File | Topics |
|------|--------|
| [01_Network_Security.md](./01_Network_Security.md) | Cryptography, Encryption (AES, DES, RSA), Diffie-Hellman, Hash Functions, Digital Signatures, SSL/TLS, MITM, DDoS |
| [02_Network_Troubleshooting.md](./02_Network_Troubleshooting.md) | Ping, Traceroute ⭐, Common Issues, Packet Loss |

---

## ⚡ Quick Reference

### Cryptography

| Concept | Type | Algorithm | Key |
|---------|------|-----------|-----|
| Symmetric Encryption | Same key both sides | AES, DES, 3DES | Shared secret key |
| Asymmetric Encryption | Public/private key pair | RSA, ECC | Public + Private |
| Hash Function | One-way fingerprint | MD5, SHA-256 | No key |
| Digital Signature | Sign + Verify | RSA + SHA | Private signs, Public verifies |
| Key Exchange | Share secret over public | Diffie-Hellman | Math-based |

### Common Attacks

| Attack | What it does | Defense |
|--------|-------------|---------|
| MITM | Intercepts communications | HTTPS, certificates |
| DDoS | Overwhelms with traffic | Rate limiting, CDN, scrubbing |
| Phishing | Tricks users into giving credentials | User training, MFA |
| DNS Poisoning | Fake DNS entries | DNSSEC |
| ARP Spoofing | Fake ARP replies | DAI, static ARP |

---

*Start with [01 — Network Security →](./01_Network_Security.md)*
