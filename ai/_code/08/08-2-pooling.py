import torch
import torch.nn as nn

print("=" * 60)
print("08-2: Pooling Operations")
print("=" * 60)

input_tensor = torch.randn(1, 1, 4, 4)
print(f"\nInput shape: {input_tensor.shape}")
print(f"Input tensor:\n{input_tensor.squeeze()}")

print("\n--- Max Pooling ---")
max_pool = nn.MaxPool2d(kernel_size=2)
output_max = max_pool(input_tensor)
print(f"MaxPool2d(2x2): {output_max.shape}")
print(f"Output:\n{output_max.squeeze()}")

print("\n--- Average Pooling ---")
avg_pool = nn.AvgPool2d(kernel_size=2)
output_avg = avg_pool(input_tensor)
print(f"AvgPool2d(2x2): {output_avg.shape}")
print(f"Output:\n{output_avg.squeeze()}")

print("\n--- Global Pooling ---")
global_max = nn.AdaptiveMaxPool2d(1)
global_avg = nn.AdaptiveAvgPool2d(1)
print(f"AdaptiveMaxPool2d(1): {global_max(input_tensor).shape}")
print(f"AdaptiveAvgPool2d(1): {global_avg(input_tensor).shape}")

print("\n--- Different Kernel Sizes ---")
input_6x6 = torch.randn(1, 1, 6, 6)
for k in [2, 3]:
    mp = nn.MaxPool2d(k)
    print(f"Kernel {k}: output shape = {mp(input_6x6).shape}")

print("\n--- Pooling with Stride ---")
pool_stride = nn.MaxPool2d(kernel_size=2, stride=2)
output_stride = pool_stride(input_tensor)
print(f"MaxPool2d(2x2, stride=2): {output_stride.shape}")

print("\n--- Global Average Pooling in CNN ---")
x = torch.randn(1, 512, 7, 7)
gap = nn.AdaptiveAvgPool2d(1)
x_gap = gap(x)
print(f"Feature map (512, 7, 7) -> GAP -> {x_gap.shape}")
print(f"Flattened: {x_gap.view(x_gap.size(0), -1).shape}")