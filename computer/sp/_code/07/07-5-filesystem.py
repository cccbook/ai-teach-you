"""
檔案系統實現
"""

import os

# 索引節點（inode）結構
class Inode:
    def __init__(self, inumber):
        self.inumber = inumber
        self.type = 'file'  # file, directory
        self.size = 0
        self.blocks = []
        self.permissions = 0o644
        self.links = 1
    
    def add_block(self, block_num):
        self.blocks.append(block_num)
        self.size = 512

# 目錄項目
class DirEntry:
    def __init__(self, name, inumber):
        self.name = name
        self.inumber = inumber

# 簡化的檔案系統
class SimpleFileSystem:
    def __init__(self, total_blocks=100):
        self.total_blocks = total_blocks
        self.free_blocks = set(range(total_blocks))
        self.inodes = [None] * 20  # 最多20個 inode
        self.root_inode = self.create_inode('directory')
    
    def create_inode(self, itype):
        """建立 inode"""
        for i, inode in enumerate(self.inodes):
            if inode is None:
                self.inodes[i] = Inode(i)
                self.inodes[i].type = itype
                return i
        return -1
    
    def allocate_block(self):
        """分配區塊"""
        if self.free_blocks:
            return self.free_blocks.pop()
        return -1
    
    def create_file(self, path):
        """建立檔案"""
        parts = path.split('/')
        parent = self.root_inode
        
        # 找到父目錄
        for part in parts[:-1]:
            if not part:
                continue
            # 搜尋子目錄...
        
        # 建立新 inode
        inumber = self.create_inode('file')
        inode = self.inodes[inumber]
        
        # 分配區塊
        block = self.allocate_block()
        if block >= 0:
            inode.add_block(block)
        
        return inumber
    
    def read_file(self, inumber):
        """讀取檔案"""
        inode = self.inodes[inumber]
        return f"內容: {inode.size} bytes, {len(inode.blocks)} blocks"

# 練習：使用 os 模組操作檔案
def file_operations():
    """檔案操作練習"""
    
    # 建立目錄結構
    os.makedirs('test_dir/sub_dir', exist_ok=True)
    
    # 寫入檔案
    with open('test_dir/file.txt', 'w') as f:
        f.write('Hello, File System!')
    
    # 讀取檔案
    with open('test_dir/file.txt', 'r') as f:
        content = f.read()
        print(content)
    
    # 列舉目錄
    print(os.listdir('test_dir'))
    
    # 取得檔案資訊
    stat = os.stat('test_dir/file.txt')
    print(f"大小: {stat.st_size}, 修改時間: {stat.st_mtime}")
    
    # 刪除
    os.remove('test_dir/file.txt')
    os.rmdir('test_dir/sub_dir')
    os.rmdir('test_dir')

# FAT32 風格的檔案系統模擬
class FAT32:
    """簡化的 FAT32 檔案系統"""
    
    def __init__(self, size):
        self.fat = [0] * (size // 512)  # 檔案配置表
        self.root_dir = {}
    
    def allocate_cluster(self):
        """配置叢集"""
        for i, entry in enumerate(self.fat):
            if entry == 0:
                self.fat[i] = 0xFFFFFFFF  # End of chain
                return i
        return -1
    
    def write_file(self, filename, data):
        """寫入檔案"""
        clusters_needed = (len(data) + 511) // 512
        chain = []
        
        for _ in range(clusters_needed):
            cluster = self.allocate_cluster()
            if cluster == -1:
                break
            chain.append(cluster)
        
        self.root_dir[filename] = {
            'chain': chain,
            'size': len(data)
        }
        
        print(f"檔案 {filename} 使用叢集: {chain}")
        return chain
    
    def read_file(self, filename):
        """讀取檔案"""
        if filename in self.root_dir:
            info = self.root_dir[filename]
            print(f"讀取 {filename}: {info['size']} bytes, 叢集: {info['chain']}")
        else:
            print(f"檔案不存在: {filename}")

# 測試
fat = FAT32(10000)
fat.write_file('test.txt', 'Hello FAT32!')
fat.read_file('test.txt')
