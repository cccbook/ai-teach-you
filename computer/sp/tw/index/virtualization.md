# 虛擬化 (Virtualization)

## 概述

虛擬化技術允許在單一硬體上執行多個隔離的作業系統。虛擬化提高了硬體利用率、簡化了伺服器管理，是雲端運算的基礎。

## 歷史

- **1974**：IBM VM/370
- **1998**：VMware 成立
- **2005**：Xen 開源
- **2007**：Intel VT-x, AMD-V
- **現在**：雲端運算主流

## 虛擬化類型

### 1. 硬體虛擬化

```c
// QEMU/KVM 架構
// QEMU: 硬體模擬
// KVM: Linux 核心虛擬化模組

// 核心模組
// /dev/kvm - KVM 裝置
// kvm_intel / kvm_amd - CPU 虛擬化
```

### 2. 容器虛擬化

```bash
# 容器 vs 虛�擬機

# VM:
# ┌────────────┐
# │ Guest OS   │
# │ Kernel     │
# ├────────────┤
# │ Hypervisor │
# ├────────────┤
# │ Host OS    │
# │ Kernel     │
# └────────────┘

# Container:
# ┌────────────┐
# │ Container  │
# │ Libraries  │
# ├────────────┤
# │ Host Kernel│
# └────────────┘
```

### 3. 類型一 vs 類型二

```bash
# 類型一：Hypervisor 直接在硬體上
# VMware ESXi, Xen, Hyper-V

# 類型二：Hypervisor 在作業系統上
# VMware Workstation, VirtualBox, Parallels
```

### 4. 核心特性

```c
// CPU 虛擬化
// - 暫存器虛擬化
// - 分頁虛擬化 (EPT/NPT)
// - 中斷虛擬化

// 記憶體虛擬化
// - 影子頁表
// - 硬體輔助 (EPT)

// 網路虛擬化
// - 虛擬網卡 (virtio)
// - 軟體交換機 (Open vSwitch)

// 儲存虛擬化
// - 虛擬磁碟 (virtio-blk, vmdk)
```

### 5. KVM/QEMU 使用

```bash
# 安裝
apt-get install qemu-kvm libvirt-bin

# 建立 VM
virt-install \
  --name=myvm \
  --ram=2048 \
  --disk path=/var/lib/libvirt/images/myvm.qcow2 \
  --vcpu=2 \
  --os-type=linux \
  --cdrom=/path/to/iso

# 管理 VM
virsh list --all
virsh start myvm
virsh shutdown myvm
virsh destroy myvm
```

### 6. 巢狀虛擬化

```bash
# 在 VM 內執行 VM
# 啟用巢狀虛擬化
modprobe kvm_intel nested=1

# 驗證
cat /sys/module/kvm_intel/parameters/nested
```

## 為什麼學習虛擬化？

1. **雲端運算**：基礎設施
2. **測試環境**：隔離測試
3. **效能優化**：資源分配
4. **開發**：本地開發

## 參考資源

- KVM 文件
- "Virtualization Essentials"
- QEMU 文件
