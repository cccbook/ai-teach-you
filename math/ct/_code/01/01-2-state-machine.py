"""
狀態機的Python實作
以自動販賣機為例
"""

from enum import Enum
from typing import Callable, Dict, Optional

class State(Enum):
    IDLE = "idle"                    # 等待投幣
    COIN_INSERTED = "coin_inserted"  # 已投幣
    PRODUCT_SELECTED = "selected"    # 已選商品
    DISPENSING = "dispensing"        # 出貨中
    CHANGE_DUE = "change_due"        # 找零中
    ERROR = "error"                  # 錯誤

class Event(Enum):
    INSERT_COIN = "insert_coin"
    SELECT_PRODUCT = "select_product"
    CONFIRM = "confirm"
    DISPENSE_COMPLETE = "dispense_complete"
    CANCEL = "cancel"
    TIMEOUT = "timeout"

class VendingMachine:
    """
    自動販賣機狀態機
    
    狀態轉換圖：
    
    IDLE ──[投幣]──▶ COIN_INSERTED
    │                    │
    │ [取消]              │ [取消]
    ▼                    ▼
  IDLE ◀──[退幣]────── IDLE
                          │
                          │ [選商品]
                          ▼
                    PRODUCT_SELECTED
                          │
                          │ [確認]
                          ▼
                      DISPENSING ──[完成]──▶ IDLE (或 CHANGE_DUE)
    """
    
    def __init__(self):
        self.current_state = State.IDLE
        self.balance = 0
        self.price = 50  # 商品價格（分）
        self.transitions: Dict[tuple, Callable] = {
            (State.IDLE, Event.INSERT_COIN): 
                (State.COIN_INSERTED, self._handle_coin),
            (State.COIN_INSERTED, Event.SELECT_PRODUCT):
                (State.PRODUCT_SELECTED, self._handle_select),
            (State.COIN_INSERTED, Event.CANCEL):
                (State.IDLE, self._handle_cancel),
            (State.PRODUCT_SELECTED, Event.CONFIRM):
                (State.DISPENSING, self._handle_confirm),
            (State.PRODUCT_SELECTED, Event.CANCEL):
                (State.IDLE, self._handle_cancel),
            (State.DISPENSING, Event.DISPENSE_COMPLETE):
                (State.CHANGE_DUE, self._handle_dispense),
            (State.CHANGE_DUE, Event.TIMEOUT):
                (State.IDLE, self._handle_timeout),
        }
    
    def _handle_coin(self, coin: int):
        self.balance += coin
        print(f"投幣成功：${coin/100:.2f}，餘額：${self.balance/100:.2f}")
    
    def _handle_select(self):
        print(f"選擇商品，價格：${self.price/100:.2f}")
    
    def _handle_confirm(self):
        if self.balance >= self.price:
            print(f"扣款：${self.price/100:.2f}")
            self.balance -= self.price
        else:
            print(f"餘額不足！需要 ${self.price/100:.2f}")
            self.current_state = State.ERROR
    
    def _handle_dispense(self):
        print("商品出貨中...")
        print("商品掉落！")
    
    def _handle_cancel(self):
        if self.balance > 0:
            print(f"退還 ${self.balance/100:.2f}")
        self.balance = 0
    
    def _handle_timeout(self):
        if self.balance > 0:
            print(f"超時，自動退還 ${self.balance/100:.2f}")
        self.balance = 0
    
    def send_event(self, event: Event, data: Optional[int] = None) -> bool:
        """發送事件，觸發狀態轉換"""
        key = (self.current_state, event)
        
        if key in self.transitions:
            new_state, handler = self.transitions[key]
            if data is not None:
                handler(data)
            else:
                handler()
            self.current_state = new_state
            return True
        else:
            print(f"無效轉換：{self.current_state.value} + {event.value}")
            return False
    
    def get_state(self) -> State:
        return self.current_state


def test_vending_machine():
    """測試：完整的購買流程"""
    print("=== 自動販賣機測試 ===\n")
    
    vm = VendingMachine()
    
    print("步驟1: 投幣 $1")
    vm.send_event(Event.INSERT_COIN, 100)
    
    print("\n步驟2: 選擇商品")
    vm.send_event(Event.SELECT_PRODUCT)
    
    print("\n步驟3: 確認購買")
    vm.send_event(Event.CONFIRM)
    
    print("\n步驟4: 出貨完成")
    vm.send_event(Event.DISPENSE_COMPLETE)
    
    print(f"\n最終狀態: {vm.get_state().value}")
    print(f"餘額: ${vm.balance/100:.2f}")


if __name__ == "__main__":
    test_vending_machine()
