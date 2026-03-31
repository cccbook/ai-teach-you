"""
嵌入式系統資源估算
"""

class EmbeddedSystem:
    """嵌入式系統資源評估"""
    
    def __init__(self):
        self.cpu = None          # CPU 型號
        self.ram = 0             # RAM 大小 (KB)
        self.flash = 0           # Flash 大小 (KB)
        self.clock = 0           # 時脈 (MHz)
        self.power_consumption = 0  # 功耗 (mW)
    
    def estimate_resources(self, application):
        """估算應用所需資源"""
        
        # 記憶體估算
        code_size = application.get('code_lines', 0) * 4  # 每行約 4 bytes
        data_size = application.get('variables', 0) * 4   # 每個變數約 4 bytes
        stack_size = application.get('max_stack', 256)    # 堆疊深度
        
        total_ram = code_size + data_size + stack_size
        
        # 檢查是否適合目標平台
        if total_ram > self.ram:
            print(f"警告: 需要 {total_ram}KB RAM，超過 {self.ram}KB")
        else:
            print(f"記憶體足夠: 需要 {total_ram}KB")
        
        # 執行時間估算
        cycles = application.get('operations', 0) * 10  # 假設每操作 10 時脈
        execution_time = cycles / (self.clock * 1000000)  # 秒
        print(f"執行時間: {execution_time*1000:.2f} ms")
        
        return {
            'ram': total_ram,
            'execution_time': execution_time,
            'power_estimate': execution_time * self.power_consumption
        }

# 測試
system = EmbeddedSystem()
system.cpu = "ATmega328P"
system.ram = 2 * 1024      # 2KB
system.flash = 32 * 1024   # 32KB
system.clock = 16          # 16MHz
system.power_consumption = 50  # 50mW @ 5V

app = {
    'code_lines': 500,
    'variables': 50,
    'max_stack': 128,
    'operations': 10000
}

system.estimate_resources(app)