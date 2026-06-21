# 🔀 Switching Techniques & Network Delays — Study Guide Index

> Two foundational topics that tie together how data travels through a network and the costs (delays) involved at every step.

---

## 📚 Files in This Section

| File | Topics |
|------|--------|
| [01_Switching_Techniques.md](./01_Switching_Techniques.md) | Circuit Switching, Packet Switching ⭐, Message Switching |
| [02_Network_Delays.md](./02_Network_Delays.md) | Transmission, Propagation, Queuing, Processing Delays |

---

## ⚡ Quick Cheat Sheet

### Switching
| Type | Path | Store full msg? | Real-time? | Example |
|------|------|----------------|-----------|---------|
| Circuit | Dedicated, pre-built | ❌ | ✅ Best | Traditional phone |
| Packet | Dynamic, per-packet | ❌ (buffers) | ✅ Good | Internet (IP) |
| Message | Dynamic, per-message | ✅ Entire msg | ❌ | Email relay |

### Delays
| Delay | Formula | Depends on |
|-------|---------|-----------|
| Transmission | L / R | Packet size, link bandwidth |
| Propagation | d / s | Distance, medium |
| Queuing | Statistical | Traffic load, buffer |
| Processing | Fixed | Router hardware |

---

*Start with [01 — Switching Techniques →](./01_Switching_Techniques.md)*
