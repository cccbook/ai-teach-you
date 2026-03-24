"""
雲端服務模型
"""

class CloudService:
    """雲端服務比較"""
    
    @staticmethod
    def compare_models():
        """比較服務模型"""
        print("""
=== IaaS vs PaaS vs SaaS ===

| 特性         | IaaS           | PaaS          | SaaS          |
|--------------|----------------|---------------|---------------|
| 提供內容     | 基礎設施       | 平台          | 軟體          |
| 使用者管理   | 作業系統以上   | 應用程式      | 無            |
| 控制權       | 高             | 中            | 低            |
| 範例         | AWS EC2        | Heroku        | Gmail         |
| 彈性         | 高             | 中            | 低            |
| 複雜度       | 高             | 中            | 低            |

=== IaaS ===
- 虛擬機器
- 儲存
- 網路
- 例: AWS EC2, GCP Compute Engine, Azure VM
- 使用者負責: OS、應用程式、資料

=== PaaS ===
- 執行環境
- 資料庫
- 開發框架
- 例: Heroku, Google App Engine, Azure App Service
- 使用者負責: 應用程式、資料

=== SaaS ===
- 完整軟體
- 透過瀏覽器存取
- 例: Salesforce, Microsoft 365, Google Workspace
- 使用者負責: 資料
""")
    
    @staticmethod
    def pricing_model():
        """定價模型"""
        print("""
=== 雲端定價模型 ===

1. 按需付費 (On-Demand)
   - 按小時/分鐘計費
   - 無長期承諾
   - 例: EC2 按需執行個體

2. 預留實例 (Reserved)
   - 一年/三年承諾
   - 折扣可達 60%
   - 例: AWS RI, Azure RI

3. .spot/搶佔式
   - 折扣可達 90%
   - 可能被回收
   - 例: AWS Spot, GCP Preemptible

4. 伺服器less
   - 按請求計費
   - 無須管理伺服器
   - 例: AWS Lambda, Cloud Functions
""")

# 雲端服務商比較
print("""
=== 主要雲端服務商 ===

AWS:
- 最早、最大
- 服務最完整
- 例: EC2, S3, Lambda, RDS

GCP:
- 技術領先
- 機器學習很強
- 例: Compute Engine, Cloud Storage, BigQuery

Azure:
- Microsoft 生態
- 企業市場強
- 例: VM, Azure SQL, Functions
""")

# 測試
CloudService.compare_models()
CloudService.pricing_model()