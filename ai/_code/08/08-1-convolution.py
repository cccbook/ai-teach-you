import torch
import torch.nn as nn
import torch.nn.functional as F

print("=" * 60)
print("08-1: Convolution Operation")
print("=" * 60)

batch_size = 1
in_channels = 1
height, width = 5, 5
out_channels = 1
kernel_size = 3

input_tensor = torch.randn(batch_size, in_channels, height, width)
kernel = torch.randn(out_channels, in_channels, kernel_size, kernel_size)

print(f"\nInput shape: {input_tensor.shape}")
print(f"Kernel shape: {kernel.shape}")

conv = nn.Conv2d(in_channels, out_channels, kernel_size, bias=False)
conv.weight.data = kernel

output = conv(input_tensor)

print(f"\nOutput shape: {output.shape}")
print(f"\nInput tensor:\n{input_tensor.squeeze()}")
print(f"\nKernel:\n{kernel.squeeze()}")
print(f"\nConvolution output:\n{output.squeeze()}")

print("\n--- Manual Convolution ---")
input_np = input_tensor.squeeze().numpy()
kernel_np = kernel.squeeze().numpy()
manual_output = torch.zeros(3, 3)
for i in range(3):
    for j in range(3):
        manual_output[i, j] = torch.sum(
            input_np[i:i+3, j:j+3] * kernel_np
        )
print(f"Manual convolution result:\n{manual_output}")

print("\n--- Convolution Parameters ---")
print(f"Padding=0, Stride=1: output shape = {output.shape}")

conv_pad = nn.Conv2d(1, 1, 3, padding=1)
output_pad = conv_pad(input_tensor)
print(f"Padding=1, Stride=1: output shape = {output_pad.shape}")

conv_stride = nn.Conv2d(1, 1, 3, stride=2)
output_stride = conv_stride(input_tensor)
print(f"Padding=0, Stride=2: output shape = {output_stride.shape}")

print("\n--- Multiple Channels ---")
input_multi = torch.randn(1, 3, 5, 5)
conv_multi = nn.Conv2d(3, 8, 3)
output_multi = conv_multi(input_multi)
print(f"Input (3 channels): {input_multi.shape}")
print(f"Output (8 channels): {output_multi.shape}")
print(f"Number of parameters: {sum(p.numel() for p in conv_multi.parameters())}")