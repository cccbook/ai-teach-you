"""
ELF（Executable and Linkable Format）解析器
"""

import struct

class ELFParser:
    def __init__(self, data):
        self.data = data
    
    def parse_header(self):
        """解析 ELF 檔頭"""
        # ELF 魔數
        magic = self.data[:4]
        if magic != b'\x7fELF':
            raise ValueError("不是有效的 ELF 檔")
        
        # 檔頭結構
        e_type = struct.unpack('<H', self.data[16:18])[0]
        e_machine = struct.unpack('<H', self.data[18:20])[0]
        e_entry = struct.unpack('<Q', self.data[24:32])[0]
        e_phoff = struct.unpack('<Q', self.data[32:40])[0]
        e_shoff = struct.unpack('<Q', self.data[40:48])[0]
        
        print(f"ELF 類型: {e_type}")
        print(f"目標架構: {e_machine}")
        print(f"入口點: 0x{e_entry:x}")
        print(f"程式頭偏移: {e_phoff}")
        print(f"區段頭偏移: {e_shoff}")
        
        return {'type': e_type, 'entry': e_entry}
    
    def parse_program_headers(self, count, entsize, offset):
        """解析程式頭"""
        headers = []
        for i in range(count):
            base = offset + i * entsize
            p_type = struct.unpack('<I', self.data[base:base+4])[0]
            p_offset = struct.unpack('<Q', self.data[base+8:base+16])[0]
            p_vaddr = struct.unpack('<Q', self.data[base+16:base+24])[0]
            p_filesz = struct.unpack('<Q', self.data[base+32:base+40])[0]
            headers.append({'type': p_type, 'offset': p_offset, 'vaddr': p_vaddr, 'filesz': p_filesz})
        return headers

# 練習：檢視自己的 ELF 檔
# $ readelf -h /bin/ls

# 不同平台的執行檔格式
# Linux: ELF (Executable and Linkable Format)
# Windows: PE (Portable Executable)
# macOS: Mach-O

# PE 格式範例結構
class PEParser:
    """PE (Portable Executable) 解析器"""
    
    DOS_HEADER_SIGNATURE = b'MZ'
    PE_SIGNATURE = b'PE\x00\x00'
    
    def parse(self, data):
        # DOS Header
        if data[:2] != self.DOS_HEADER_SIGNATURE:
            raise ValueError("不是有效的 PE 檔")
        
        # PE 簽名位置
        e_lfanew = struct.unpack('<I', data[60:64])[0]
        
        # PE 簽名
        if data[e_lfanew:e_lfanew+4] != self.PE_SIGNATURE:
            raise ValueError("PE 簽名無效")
        
        print(f"有效的 PE 檔，PE 頭位於: {e_lfanew}")

# Mach-O 格式
class MachOParser:
    """Apple Mach-O 解析器"""
    
    FAT_MAGIC = 0xcafebabe
    MH_MAGIC = 0xfeedface
    
    def parse(self, data):
        magic = struct.unpack('>I', data[:4])[0]
        
        if magic == self.FAT_MAGIC:
            print("Fat Binary (通用二進制)")
        elif magic == self.MH_MAGIC:
            print("32-bit Mach-O")
        else:
            print("64-bit Mach-O")