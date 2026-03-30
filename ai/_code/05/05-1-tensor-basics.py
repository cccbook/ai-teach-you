import torch
import numpy as np


def main():
    print("=" * 50)
    print("PyTorch Tensor Basics")
    print("=" * 50)

    print("\n1. Creating Tensors")
    print("-" * 30)
    
    scalar = torch.tensor(3.14)
    print(f"Scalar: {scalar}, shape: {scalar.shape}, dtype: {scalar.dtype}")
    
    vector = torch.tensor([1, 2, 3, 4, 5])
    print(f"Vector: {vector}, shape: {vector.shape}")
    
    matrix = torch.randn(3, 4)
    print(f"3x4 Matrix:\n{matrix}")
    
    tensor3d = torch.zeros(2, 3, 4)
    print(f"3D Tensor shape: {tensor3d.shape}")

    print("\n2. Tensor from NumPy")
    print("-" * 30)
    np_array = np.array([[1, 2], [3, 4]])
    torch_tensor = torch.from_numpy(np_array)
    print(f"NumPy: {np_array}")
    print(f"Torch: {torch_tensor}")

    print("\n3. Tensor Operations")
    print("-" * 30)
    a = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
    b = torch.tensor([[5, 6], [7, 8]], dtype=torch.float32)
    
    print(f"a + b = \n{a + b}")
    print(f"a * b = \n{a * b}")
    print(f"a @ b (matrix multiply) = \n{a @ b}")
    print(f"a.sum() = {a.sum()}")
    print(f"a.mean() = {a.mean()}")

    print("\n4. Reshape & Squeeze")
    print("-" * 30)
    t = torch.randn(2, 3, 4)
    print(f"Original shape: {t.shape}")
    print(f"Reshape to (6, 4): {t.reshape(6, 4).shape}")
    print(f"Flatten: {t.flatten().shape}")

    print("\n5. Indexing")
    print("-" * 30)
    x = torch.tensor([[10, 20, 30], [40, 50, 60]])
    print(f"x[0] = {x[0]}")
    print(f"x[0, 1] = {x[0, 1]}")
    print(f"x[:, 1] = {x[:, 1]}")

    print("\n6. GPU/CPU Device")
    print("-" * 30)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Current device: {device}")
    tensor_cpu = torch.randn(3, 3)
    tensor_device = tensor_cpu.to(device)
    print(f"Tensor on {device}: {tensor_device.device}")


if __name__ == "__main__":
    main()