# AI 輔助測試生成 Prompt

> 來源：第 4 章「單一 Agent 開發」

---

## 測試生成 Prompt 模板

### 基本模板

```
請為以下程式碼生成 pytest 測試：

[貼上程式碼]

請包含：
- 正常情況測試
- 邊界情況測試
- 錯誤情況測試
```

### 實際範例

```python
# 測試對象
def calculate_discount(price: float, discount_percent: float) -> float:
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)
```

### Prompt

```
請為以下函數生成 pytest 測試：

def calculate_discount(price: float, discount_percent: float) -> float:
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)

請包含：
- 正常折扣計算
- 0% 折扣
- 100% 折扣
- 負數折扣（應拋出異常）
- 超過 100% 折扣（應拋出異常）
```

---

## API 測試 Prompt

```
請為以下 FastAPI 路由生成測試：

@router.post("/products")
def create_product(product: ProductCreate):
    # 建立商品邏輯

請使用 pytest + httpx 生成整合測試：
- 測試成功建立
- 測試 Validation Error
- 測試重複建立
```
