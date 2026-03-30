// 嵌入式系統範例：Arduino 控制 LED
// 硬體: ATmega328P, 16MHz, 2KB RAM, 32KB Flash

#define LED_PIN 13

void setup() {
    pinMode(LED_PIN, OUTPUT);  // 設定腳位為輸出
}

void loop() {
    digitalWrite(LED_PIN, HIGH);  // LED 亮
    delay(1000);                   // 延遲 1 秒
    digitalWrite(LED_PIN, LOW);   // LED 滅
    delay(1000);                   // 延遲 1 秒
}

// 嵌入式系統特性：
// 1. 資源受限 - RAM/ROM 有限
// 2. 即時性 - 需要確定性的回應時間
// 3. 低功耗 - 电池供电设备
// 4. 無人值守 - 长时间运行
// 5. 專用性 - 单个功能或有限功能