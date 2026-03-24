"""
嵌入式系統可靠性模式
"""

# 1. 看門狗監控
class Watchdog:
    """看門狗定時器"""
    
    def __init__(self, timeout=1.0):
        self.timeout = timeout
        self.last_pet = time.time()
        self.enabled = True
    
    def pet(self):
        """餵狗"""
        self.last_pet = time.time()
        print("看門狗已重置")
    
    def check(self):
        """檢查"""
        if not self.enabled:
            return True
        
        elapsed = time.time() - self.last_pet
        if elapsed > self.timeout:
            print("看門狗超時！系統將重置")
            return False
        return True

# 2. 錯誤復原
class ErrorRecovery:
    """錯誤復原策略"""
    
    @staticmethod
    def retry(operation, max_retries=3):
        """重試"""
        for attempt in range(max_retries):
            try:
                return operation()
            except Exception as e:
                print(f"嘗試 {attempt+1} 失敗: {e}")
                time.sleep(0.1)
        return None
    
    @staticmethod
    def fallback(primary, fallback_func):
        """降級"""
        try:
            return primary()
        except:
            return fallback_func()

# 3. 資料完整性
class DataIntegrity:
    """資料完整性檢查"""
    
    @staticmethod
    def checksum(data):
        """簡單校驗和"""
        return sum(data) % 256
    
    @staticmethod
    def crc32(data):
        """CRC32"""
        import zlib
        return zlib.crc32(data)
    
    @staticmethod
    def verify(data, expected):
        """驗證"""
        return DataIntegrity.checksum(data) == expected

# 測試
wd = Watchdog(timeout=0.5)
wd.pet()
time.sleep(0.3)
wd.pet()
time.sleep(0.6)  # 將觸發重置
wd.check()

# 錯誤復原
result = ErrorRecovery.retry(
    lambda: 1/0,  # 會失敗的操作
    max_retries=3
)
print(f"重試結果: {result}")

# 資料完整性
data = b"Hello, World!"
checksum = DataIntegrity.checksum(data)
print(f"資料校驗: {DataIntegrity.verify(data, checksum)}")