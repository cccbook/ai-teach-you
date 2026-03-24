# RISC-V 組合語言測試程式
# 格式：標籤前加 @ 位址，指令後加 # 機器碼註解
#
# 記憶體佈局：
#   x0  = 0   (hardwired zero)
#   x1  = 0   (初始化後保持 0)
#   x2  = 1
#   x3  = 2
#   x4  = 3
#   ...
#   x20 = 19
#   x10 = 28  (由 li x10, 28 載入)
#
# 第一段：22 條 ADDI，逐步建立費伯那契序列的初始值
#   x1=0, x2=1, x3=2, x4=3, ... x20=19, x10=28

00000000  li     x1,  0          # 00000093  addi x1, x0, 0
00000004  li     x2,  1          # 00100113  addi x2, x0, 1
00000008  li     x3,  2          # 00200193  addi x3, x0, 2
0000000c  li     x4,  3          # 00300213  addi x4, x0, 3
00000010  li     x5,  4          # 00400293  addi x5, x0, 4
00000014  li     x6,  5          # 00500313  addi x6, x0, 5
00000018  li     x7,  6          # 00600393  addi x7, x0, 6
0000001c  li     x8,  7          # 00700413  addi x8, x0, 7
00000020  li     x9,  8          # 00800493  addi x9, x0, 8
00000024  li     x10, 9          # 00900513  addi x10, x0, 9
00000028  li     x11, 10         # 00a00593  addi x11, x0, 10
0000002c  li     x12, 11         # 00b00613  addi x12, x0, 11
00000030  li     x13, 12         # 00c00693  addi x13, x0, 12
00000034  li     x14, 13         # 00d00713  addi x14, x0, 13
00000038  li     x15, 14         # 00e00793  addi x15, x0, 14
0000003c  li     x16, 15         # 00f00813  addi x16, x0, 15
00000040  li     x17, 16         # 01000893  addi x17, x0, 16
00000044  li     x18, 17         # 01100913  addi x18, x0, 17
00000048  li     x19, 18         # 01200993  addi x19, x0, 18
0000004c  li     x20, 19         # 01300a13  addi x20, x0, 19
00000050  li     x10, 28         # 01400b13  addi x10, x0, 28

# 第二段：234 條 ADD 指令（費伯那契加法鏈）
#   x11 = x10 + x5  = 28 + 4  = 32
#   x12 = x11 + x6  = 32 + 5  = 37
#   x13 = x12 + x7  = 37 + 6  = 43
#   x14 = x13 + x8  = 43 + 7  = 50
#   ...持續累加，每一步取前一個結果加上遞進的加數
#   x244 = x243 + x20  (最後一條)
#
# 這個累加序列產生的數列從 32 開始，
# 每個後續數 = 前一個數 + 對應的加數 (從 4 遞增)

00000054  add    x11, x10, x5    # 00a282b3  add x11, x10, x5
00000058  add    x12, x11, x6    # 00b28333  add x12, x11, x6
0000005c  add    x13, x12, x7    # 00c283b3  add x13, x12, x7
00000060  add    x14, x13, x8    # 00d28433  add x14, x13, x8
00000064  add    x15, x14, x9    # 00e284b3  add x15, x14, x9
00000068  add    x16, x15, x10   # 00f28533  add x16, x15, x10
0000006c  add    x17, x16, x11   # 010285b3  add x17, x16, x11
00000070  add    x18, x17, x12   # 01128633  add x18, x17, x12
00000074  add    x19, x18, x13   # 012286b3  add x19, x18, x13
00000078  add    x20, x19, x14   # 01328733  add x20, x19, x14
0000007c  add    x21, x20, x15   # 014287b3  add x21, x20, x15
00000080  add    x22, x21, x16   # 01528833  add x22, x21, x16
00000084  add    x23, x22, x17   # 016288b3  add x23, x22, x17
00000088  add    x24, x23, x18   # 01728933  add x24, x23, x18
0000008c  add    x25, x24, x19   # 018289b3  add x25, x24, x19
00000090  add    x26, x25, x20   # 01928a33  add x26, x25, x20
00000094  add    x27, x26, x21   # 01a28ab3  add x27, x26, x21
00000098  add    x28, x27, x22   # 01b28b33  add x28, x27, x22
0000009c  add    x29, x28, x23   # 01c28bb3  add x29, x28, x23
000000a0  add    x30, x29, x24   # 01d28c33  add x30, x29, x24
000000a4  add    x31, x30, x25   # 01e28cb3  add x31, x30, x25
000000a8  add    x1,  x31, x26   # 01f28d33  add x1, x31, x26
000000ac  add    x2,  x1,  x27   # 02028db3  add x2, x1, x27
000000b0  add    x3,  x2,  x28   # 02128e33  add x3, x2, x28
000000b4  add    x4,  x3,  x29   # 02228eb3  add x4, x3, x29
000000b8  add    x5,  x4,  x30   # 02328f33  add x5, x4, x30
000000bc  add    x6,  x5,  x31   # 02428fb3  add x6, x5, x31
000000c0  add    x7,  x6,  x1    # 02529033  add x7, x6, x1
000000c4  add    x8,  x7,  x2    # 026290b3  add x8, x7, x2
000000c8  add    x9,  x8,  x3    # 02729133  add x9, x8, x3
000000cc  add    x10, x9,  x4    # 028291b3  add x10, x9, x4
000000d0  add    x11, x10, x5    # 02929233  add x11, x10, x5
000000d4  add    x12, x11, x6    # 02a292b3  add x12, x11, x6
000000d8  add    x13, x12, x7    # 02b29333  add x13, x12, x7
000000dc  add    x14, x13, x8    # 02c293b3  add x14, x13, x8
000000e0  add    x15, x14, x9    # 02d29433  add x15, x14, x9
000000e4  add    x16, x15, x10   # 02e294b3  add x16, x15, x10
000000e8  add    x17, x16, x11   # 02f29533  add x17, x16, x11
000000ec  add    x18, x17, x12   # 030295b3  add x18, x17, x12
000000f0  add    x19, x18, x13   # 03129633  add x19, x18, x13
000000f4  add    x20, x19, x14   # 032296b3  add x20, x19, x14
000000f8  add    x21, x20, x15   # 03329733  add x21, x20, x15
000000fc  add    x22, x21, x16   # 034297b3  add x22, x21, x16
00000100  add    x23, x22, x17   # 03529833  add x23, x22, x17
00000104  add    x24, x23, x18   # 036298b3  add x24, x23, x18
00000108  add    x25, x24, x19   # 03729933  add x25, x24, x19
0000010c  add    x26, x25, x20   # 038299b3  add x26, x25, x20
00000110  add    x27, x26, x21   # 03929a33  add x27, x26, x21
00000114  add    x28, x27, x22   # 03a29ab3  add x28, x27, x22
00000118  add    x29, x28, x23   # 03b29b33  add x29, x28, x23
0000011c  add    x30, x29, x24   # 03c29bb3  add x30, x29, x24
00000120  add    x31, x30, x25   # 03d29c33  add x31, x30, x25
00000124  add    x1,  x31, x26   # 03e29cb3  add x1, x31, x26
00000128  add    x2,  x1,  x27   # 03f29d33  add x2, x1, x27
0000012c  add    x3,  x2,  x28   # 04029db3  add x3, x2, x28
00000130  add    x4,  x3,  x29   # 04129e33  add x4, x3, x29
00000134  add    x5,  x4,  x30   # 04229eb3  add x5, x4, x30
00000138  add    x6,  x5,  x31   # 04329f33  add x6, x5, x31
0000013c  add    x7,  x6,  x1    # 04429fb3  add x7, x6, x1
00000140  add    x8,  x7,  x2    # 0452a033  add x8, x7, x2
00000144  add    x9,  x8,  x3    # 0462a0b3  add x9, x8, x3
00000148  add    x10, x9,  x4    # 0472a133  add x10, x9, x4
0000014c  add    x11, x10, x5    # 0482a1b3  add x11, x10, x5
00000150  add    x12, x11, x6    # 0492a233  add x12, x11, x6
00000154  add    x13, x12, x7    # 04a2a2b3  add x13, x12, x7
00000158  add    x14, x13, x8    # 04b2a333  add x14, x13, x8
0000015c  add    x15, x14, x9    # 04c2a3b3  add x15, x14, x9
00000160  add    x16, x15, x10   # 04d2a433  add x16, x15, x10
00000164  add    x17, x16, x11   # 04e2a4b3  add x17, x16, x11
00000168  add    x18, x17, x12   # 04f2a533  add x18, x17, x12
0000016c  add    x19, x18, x13   # 0502a5b3  add x19, x18, x13
00000170  add    x20, x19, x14   # 0512a633  add x20, x19, x14
00000174  add    x21, x20, x15   # 0522a6b3  add x21, x20, x15
00000178  add    x22, x21, x16   # 0532a733  add x22, x21, x16
0000017c  add    x23, x22, x17   # 0542a7b3  add x23, x22, x17
00000180  add    x24, x23, x18   # 0552a833  add x24, x23, x18
00000184  add    x25, x24, x19   # 0562a8b3  add x25, x24, x19
00000188  add    x26, x25, x20   # 0572a933  add x26, x25, x20
0000018c  add    x27, x26, x21   # 0582a9b3  add x27, x26, x21
00000190  add    x28, x27, x22   # 0592aa33  add x28, x27, x22
00000194  add    x29, x28, x23   # 05a2aab3  add x29, x28, x23
00000198  add    x30, x29, x24   # 05b2ab33  add x30, x29, x24
0000019c  add    x31, x30, x25   # 05c2abb3  add x31, x30, x25
000001a0  add    x1,  x31, x26   # 05d2ac33  add x1, x31, x26
000001a4  add    x2,  x1,  x27   # 05e2acb3  add x2, x1, x27
000001a8  add    x3,  x2,  x28   # 05f2ad33  add x3, x2, x28
000001ac  add    x4,  x3,  x29   # 0602adb3  add x4, x3, x29
000001b0  add    x5,  x4,  x30   # 0612ae33  add x5, x4, x30
000001b4  add    x6,  x5,  x31   # 0622aeb3  add x6, x5, x31
000001b8  add    x7,  x6,  x1    # 0632af33  add x7, x6, x1
000001bc  add    x8,  x7,  x2    # 0642afb3  add x8, x7, x2
000001c0  add    x9,  x8,  x3    # 0652b033  add x9, x8, x3
000001c4  add    x10, x9,  x4    # 0662b0b3  add x10, x9, x4
000001c8  add    x11, x10, x5    # 0672b133  add x11, x10, x5
000001cc  add    x12, x11, x6    # 0682b1b3  add x12, x11, x6
000001d0  add    x13, x12, x7    # 0692b233  add x13, x12, x7
000001d4  add    x14, x13, x8    # 06a2b2b3  add x14, x13, x8
000001d8  add    x15, x14, x9    # 06b2b333  add x15, x14, x9
000001dc  add    x16, x15, x10   # 06c2b3b3  add x16, x15, x10
000001e0  add    x17, x16, x11   # 06d2b433  add x17, x16, x11
000001e4  add    x18, x17, x12   # 06e2b4b3  add x18, x17, x12
000001e8  add    x19, x18, x13   # 06f2b533  add x19, x18, x13
000001ec  add    x20, x19, x14   # 0702b5b3  add x20, x19, x14
000001f0  add    x21, x20, x15   # 0712b633  add x21, x20, x15
000001f4  add    x22, x21, x16   # 0722b6b3  add x22, x21, x16
000001f8  add    x23, x22, x17   # 0732b733  add x23, x22, x17
000001fc  add    x24, x23, x18   # 0742b7b3  add x24, x23, x18
00000200  add    x25, x24, x19   # 0752b833  add x25, x24, x19
00000204  add    x26, x25, x20   # 0762b8b3  add x26, x25, x20
00000208  add    x27, x26, x21   # 0772b933  add x27, x26, x21
0000020c  add    x28, x27, x22   # 0782b9b3  add x28, x27, x22
00000210  add    x29, x28, x23   # 0792ba33  add x29, x28, x23
00000214  add    x30, x29, x24   # 07a2bab3  add x30, x29, x24
00000218  add    x31, x30, x25   # 07b2bb33  add x31, x30, x25
0000021c  add    x1,  x31, x26   # 07c2bbb3  add x1, x31, x26
00000220  add    x2,  x1,  x27   # 07d2bc33  add x2, x1, x27
00000224  add    x3,  x2,  x28   # 07e2bcb3  add x3, x2, x28
00000228  add    x4,  x3,  x29   # 07f2bd33  add x4, x3, x29
0000022c  add    x5,  x4,  x30   # 0802bdb3  add x5, x4, x30
00000230  add    x6,  x5,  x31   # 0812be33  add x6, x5, x31
00000234  add    x7,  x6,  x1    # 0822beb3  add x7, x6, x1
00000238  add    x8,  x7,  x2    # 0832bf33  add x8, x7, x2
0000023c  add    x9,  x8,  x3    # 0842bfb3  add x9, x8, x3
00000240  add    x10, x9,  x4    # 0852c033  add x10, x9, x4
00000244  add    x11, x10, x5    # 0862c0b3  add x11, x10, x5
00000248  add    x12, x11, x6    # 0872c133  add x12, x11, x6
0000024c  add    x13, x12, x7    # 0882c1b3  add x13, x12, x7
00000250  add    x14, x13, x8    # 0892c233  add x14, x13, x8
00000254  add    x15, x14, x9    # 08a2c2b3  add x15, x14, x9
00000258  add    x16, x15, x10   # 08b2c333  add x16, x15, x10
0000025c  add    x17, x16, x11   # 08c2c3b3  add x17, x16, x11
00000260  add    x18, x17, x12   # 08d2c433  add x18, x17, x12
00000264  add    x19, x18, x13   # 08e2c4b3  add x19, x18, x13
00000268  add    x20, x19, x14   # 08f2c533  add x20, x19, x14
0000026c  add    x21, x20, x15   # 0902c5b3  add x21, x20, x15
00000270  add    x22, x21, x16   # 0912c633  add x22, x21, x16
00000274  add    x23, x22, x17   # 0922c6b3  add x23, x22, x17
00000278  add    x24, x23, x18   # 0932c733  add x24, x23, x18
0000027c  add    x25, x24, x19   # 0942c7b3  add x25, x24, x19
00000280  add    x26, x25, x20   # 0952c833  add x26, x25, x20
00000284  add    x27, x26, x21   # 0962c8b3  add x27, x26, x21
00000288  add    x28, x27, x22   # 0972c933  add x28, x27, x22
0000028c  add    x29, x28, x23   # 0982c9b3  add x29, x28, x23
00000290  add    x30, x29, x24   # 0992ca33  add x30, x29, x24
00000294  add    x31, x30, x25   # 09a2cab3  add x31, x30, x25
00000298  add    x1,  x31, x26   # 09b2cb33  add x1, x31, x26
0000029c  add    x2,  x1,  x27   # 09c2cbb3  add x2, x1, x27
000002a0  add    x3,  x2,  x28   # 09d2cc33  add x3, x2, x28
000002a4  add    x4,  x3,  x29   # 09e2ccb3  add x4, x3, x29
000002a8  add    x5,  x4,  x30   # 09f2cd33  add x5, x4, x30
000002ac  add    x6,  x5,  x31   # 0a02cdb3  add x6, x5, x31
000002b0  add    x7,  x6,  x1    # 0a12ce33  add x7, x6, x1
000002b4  add    x8,  x7,  x2    # 0a22ceb3  add x8, x7, x2
000002b8  add    x9,  x8,  x3    # 0a32cf33  add x9, x8, x3
000002bc  add    x10, x9,  x4    # 0a42cfb3  add x10, x9, x4
000002c0  add    x11, x10, x5    # 0a52d033  add x11, x10, x5
000002c4  add    x12, x11, x6    # 0a62d0b3  add x12, x11, x6
000002c8  add    x13, x12, x7    # 0a72d133  add x13, x12, x7
000002cc  add    x14, x13, x8    # 0a82d1b3  add x14, x13, x8
000002d0  add    x15, x14, x9    # 0a92d233  add x15, x14, x9
000002d4  add    x16, x15, x10   # 0aa2d2b3  add x16, x15, x10
000002d8  add    x17, x16, x11   # 0ab2d333  add x17, x16, x11
000002dc  add    x18, x17, x12   # 0ac2d3b3  add x18, x17, x12
000002e0  add    x19, x18, x13   # 0ad2d433  add x19, x18, x13
000002e4  add    x20, x19, x14   # 0ae2d4b3  add x20, x19, x14
000002e8  add    x21, x20, x15   # 0af2d533  add x21, x20, x15
000002ec  add    x22, x21, x16   # 0b02d5b3  add x22, x21, x16
000002f0  add    x23, x22, x17   # 0b12d633  add x23, x22, x17
000002f4  add    x24, x23, x18   # 0b22d6b3  add x24, x23, x18
000002f8  add    x25, x24, x19   # 0b32d733  add x25, x24, x19
000002fc  add    x26, x25, x20   # 0b42d7b3  add x26, x25, x20
00000300  add    x27, x26, x21   # 0b52d833  add x27, x26, x21
00000304  add    x28, x27, x22   # 0b62d8b3  add x28, x27, x22
00000308  add    x29, x28, x23   # 0b72d933  add x29, x28, x23
0000030c  add    x30, x29, x24   # 0b82d9b3  add x30, x29, x24
00000310  add    x31, x30, x25   # 0b92da33  add x31, x30, x25
00000314  add    x1,  x31, x26   # 0ba2dab3  add x1, x31, x26
00000318  add    x2,  x1,  x27   # 0bb2db33  add x2, x1, x27
0000031c  add    x3,  x2,  x28   # 0bc2dbb3  add x3, x2, x28
00000320  add    x4,  x3,  x29   # 0bd2dc33  add x4, x3, x29
00000324  add    x5,  x4,  x30   # 0be2dcb3  add x5, x4, x30
00000328  add    x6,  x5,  x31   # 0bf2dd33  add x6, x5, x31
0000032c  add    x7,  x6,  x1    # 0c02ddb3  add x7, x6, x1
00000330  add    x8,  x7,  x2    # 0c12de33  add x8, x7, x2
00000334  add    x9,  x8,  x3    # 0c22deb3  add x9, x8, x3
00000338  add    x10, x9,  x4    # 0c32df33  add x10, x9, x4
0000033c  add    x11, x10, x5    # 0c42dfb3  add x11, x10, x5
00000340  add    x12, x11, x6    # 0c52e033  add x12, x10, x6
00000344  add    x13, x12, x7    # 0c62e0b3  add x13, x12, x7
00000348  add    x14, x13, x8    # 0c72e133  add x14, x13, x8
0000034c  add    x15, x14, x9    # 0c82e1b3  add x15, x14, x9
00000350  add    x16, x15, x10   # 0c92e233  add x16, x15, x10
00000354  add    x17, x16, x11   # 0ca2e2b3  add x17, x16, x11
00000358  add    x18, x17, x12   # 0cb2e333  add x18, x17, x12
0000035c  add    x19, x18, x13   # 0cc2e3b3  add x19, x18, x13
00000360  add    x20, x19, x14   # 0cd2e433  add x20, x19, x14
00000364  add    x21, x20, x15   # 0ce2e4b3  add x21, x20, x15
00000368  add    x22, x21, x16   # 0cf2e533  add x22, x21, x16
0000036c  add    x23, x22, x17   # 0d02e5b3  add x23, x22, x17
00000370  add    x24, x23, x18   # 0d12e633  add x24, x23, x18
00000374  add    x25, x24, x19   # 0d22d6b3  add x25, x24, x19  <-- 注意：原本為 0d22e6b3
00000378  add    x26, x25, x20   # 0d32e733  add x26, x25, x20
0000037c  add    x27, x26, x21   # 0d42e7b3  add x27, x26, x21
00000380  add    x28, x27, x22   # 0d52e833  add x28, x27, x22
00000384  add    x29, x28, x23   # 0d62e8b3  add x29, x28, x23
00000388  add    x30, x29, x24   # 0d72e933  add x30, x29, x24
0000038c  add    x31, x30, x25   # 0d82e9b3  add x31, x30, x25
00000390  add    x1,  x31, x26   # 0d92ea33  add x1, x31, x26
00000394  add    x2,  x1,  x27   # 0da2eab3  add x2, x1, x27
00000398  add    x3,  x2,  x28   # 0db2eb33  add x3, x2, x28
0000039c  add    x4,  x3,  x29   # 0dc2ebb3  add x4, x3, x29
000003a0  add    x5,  x4,  x30   # 0dd2ec33  add x5, x4, x30
000003a4  add    x6,  x5,  x31   # 0de2ecb3  add x6, x5, x31
000003a8  add    x7,  x6,  x1    # 0df2ed33  add x7, x6, x1
000003ac  add    x8,  x7,  x2    # 0e02edb3  add x8, x7, x2
000003b0  add    x9,  x8,  x3    # 0e12ee33  add x9, x8, x3
000003b4  add    x10, x9,  x4    # 0e22eeb3  add x10, x9, x4
000003b8  add    x11, x10, x5    # 0e32ef33  add x11, x10, x5
000003bc  add    x12, x11, x6    # 0e42efb3  add x12, x11, x6
000003c0  add    x13, x12, x7    # 0e52f033  add x13, x12, x7
000003c4  add    x14, x13, x8    # 0e62f0b3  add x14, x13, x8
000003c8  add    x15, x14, x9    # 0e72f133  add x15, x14, x9
000003cc  add    x16, x15, x10   # 0e82f1b3  add x16, x15, x10
000003d0  add    x17, x16, x11   # 0e92f233  add x17, x16, x11
000003d4  add    x18, x17, x12   # 0ea2f2b3  add x18, x17, x12
000003d8  add    x19, x18, x13   # 0eb2f333  add x19, x18, x13
000003dc  add    x20, x19, x14   # 0ec2f3b3  add x20, x19, x14
000003e0  add    x21, x20, x15   # 0ed2f433  add x21, x20, x15
000003e4  add    x22, x21, x16   # 0ee2f4b3  add x22, x21, x16
000003e8  add    x23, x22, x17   # 0ef2f533  add x23, x22, x17
000003ec  add    x24, x23, x18   # 0f02f5b3  add x24, x23, x18
000003f0  add    x25, x24, x19   # 0f12f633  add x25, x24, x19
000003f4  add    x26, x25, x20   # 0f22f6b3  add x26, x25, x20
000003f8  add    x27, x26, x21   # 0f32f733  add x27, x26, x21
