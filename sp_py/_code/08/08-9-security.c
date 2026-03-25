// 嵌入式系統安全性範例

// 1. 看門狗定時器
void init_watchdog() {
    // 設定看門狗，1秒後重置
    WDTCTL = WDTPW + WDTTMSEL + WDTIS_2;  // 1秒
}

// 2. 記憶體保護單元 (MPU)
void configure_mpu() {
    // 設定記憶體區域權限
    MPU->RNR = 0;              // Region 0
    MPU->RBAR = 0x20000000;    // SRAM 起始
    MPU->RASR = MPU_REGION_SIZE_64KB | 
                MPU_REGION_READ_WRITE |
                MPU_REGION_NOT_EXECUTE;
}

// 3. CRC 校驗
uint32_t crc32(uint8_t *data, size_t len) {
    uint32_t crc = 0xFFFFFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= data[i];
        for (int j = 0; j < 8; j++) {
            crc = (crc >> 1) ^ (0xEDB88320 & -(crc & 1));
        }
    }
    return ~crc;
}

// 4. 錯誤更正碼 (ECC)
void enable_ecc() {
    // 啟用 ECC 用於 SRAM/Flash
    FMC->ECCCTL |= FMC_ECC_EN;
}