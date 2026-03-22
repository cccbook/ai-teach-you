# 39. OS Virtualization——From xv6 to Modern Kernels

## 39.1 Virtualization Basics

Virtualization allows one hardware to run multiple operating systems simultaneously.

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Guest 1   │ │   Guest 2   │ │   Guest 3   │
│  (VM 1)    │ │  (VM 2)    │ │  (VM 3)    │
├─────────────┤ ├─────────────┤ ├─────────────┤
│  Guest OS   │ │  Guest OS   │ │  Guest OS   │
├─────────────┤ ├─────────────┤ ├─────────────┤
│  Hypervisor │ (KVM / Xen / VMware)
├─────────────┤
│   Hardware  │ (CPU, Memory, Storage, Network)
└─────────────┘
```

## 39.2 Virtualization Types

| Type | Description | Examples |
|------|-------------|----------|
| Full virtualization | Guest unmodified | VMware, QEMU |
| Paravirtualization | Guest modified | Xen, VirtIO |
| Hardware-assisted | CPU supports virtualization | KVM, VMware |

## 39.3 RISC-V Virtualization

### 39.3.1 H Extension

RISC-V's H extension provides hardware virtualization support.

## 39.4 From xv6 to Modern Kernel

| Feature | xv6 | Linux |
|---------|-----|-------|
| CPU | Single core support | Multi-core support |
| Memory | Fixed allocation | Dynamic management |
| File system | Simplified v6 | ext4, btrfs |
| Network | None | Full TCP/IP |
| Containers | None | Docker |

## 39.5 Summary

In this chapter we learned:
- Basic virtualization concepts
- Virtualization types
- Evolution from xv6 to modern kernel

## 39.6 Exercises

1. Research KVM implementation
2. Compare Xen and KVM
3. Create a VM in QEMU
