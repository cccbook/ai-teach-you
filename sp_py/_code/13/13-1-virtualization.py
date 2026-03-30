"""
虛擬化技術
"""

# 1. 模擬虛擬化（Full Virtualization）
class VirtualMachine:
    """完整虛擬機"""
    
    def __init__(self, name, memory_mb=1024, cpu_cores=1):
        self.name = name
        self.memory = memory_mb * 1024 * 1024  # bytes
        self.cpu_cores = cpu_cores
        self.virtual_disks = []
        self.virtual_nics = []
        self.state = 'stopped'
    
    def start(self):
        """啟動虛擬機"""
        self.state = 'running'
        print(f"虛擬機 {self.name} 啟動")
        print(f"  CPU: {self.cpu_cores} 核心")
        print(f"  記憶體: {self.memory // (1024*1024)} MB")
    
    def stop(self):
        """停止虛擬機"""
        self.state = 'stopped'
        print(f"虛擬機 {self.name} 停止")
    
    def add_disk(self, size_gb):
        """新增虛擬磁碟"""
        disk = {'size': size_gb * 1024**3, 'name': f"{self.name}-disk{len(self.virtual_disks)}"}
        self.virtual_disks.append(disk)
        print(f"新增磁碟: {disk['name']}, {size_gb}GB")
    
    def add_network(self):
        """新增虛擬網卡"""
        nic = {'mac': f"52:54:00:{':'.join(f'{random.randint(0,255):02x}' for _ in range(2))}"}
        self.virtual_nics.append(nic)
        print(f"新增網卡: {nic['mac']}")

# 2. 容器虛擬化
class Container:
    """容器"""
    
    def __init__(self, image, name=None):
        self.image = image
        self.name = name or image
        self.environment = {}
        self.mounts = []
        self.limits = {'cpu': 1.0, 'memory': '512m'}
        self.state = 'created'
    
    def run(self):
        """執行容器"""
        self.state = 'running'
        print(f"容器 {self.name} 執行中 (image: {self.image})")
        print(f"  CPU limit: {self.limits['cpu']}")
        print(f"  Memory: {self.limits['memory']}")
    
    def stop(self):
        """停止容器"""
        self.state = 'stopped'
        print(f"容器 {self.name} 停止")
    
    def set_env(self, key, value):
        """設定環境變數"""
        self.environment[key] = value
    
    def mount(self, host_path, container_path):
        """掛載目錄"""
        self.mounts.append({'host': host_path, 'container': container_path})

# 3. 虛擬化類型比較
print("""
=== 虛擬化類型 ===

1. 完整虛擬化（Full）
   - 模擬完整硬體
   - 例: QEMU, VirtualBox
   - 需要 Hypervisor

2. 半虛擬化（Para）
   - 修改 Guest OS
   - 例: Xen, VMware
   - 效能較好

3. 容器虛擬化
   - 共享核心
   - 例: Docker, LXC
   - 輕量快速

4. 作業系統層虛擬化
   - 例: FreeBSD Jails, Solaris Zones
""")

# 測試
vm = VirtualMachine("test-vm", memory_mb=2048, cpu_cores=2)
vm.add_disk(40)
vm.add_disk(100)
vm.add_network()
vm.start()
vm.stop()