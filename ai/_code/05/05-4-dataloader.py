import torch
from torch.utils.data import Dataset, DataLoader


def main():
    print("=" * 50)
    print("DataLoader and Custom Datasets")
    print("=" * 50)

    print("\n1. Custom Dataset")
    print("-" * 30)

    class MyDataset(Dataset):
        def __init__(self, x_data, y_data):
            self.x = torch.tensor(x_data, dtype=torch.float32)
            self.y = torch.tensor(y_data, dtype=torch.float32)

        def __len__(self):
            return len(self.x)

        def __getitem__(self, idx):
            return self.x[idx], self.y[idx]

    X = [[i, i+1, i+2] for i in range(10)]
    y = [[i * 2] for i in range(10)]
    dataset = MyDataset(X, y)
    print(f"Dataset length: {len(dataset)}")
    print(f"First sample: {dataset[0]}")

    print("\n2. DataLoader with Batching")
    print("-" * 30)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

    for batch_idx, (batch_x, batch_y) in enumerate(dataloader):
        print(f"Batch {batch_idx}: x.shape={batch_x.shape}, y.shape={batch_y.shape}")
        print(f"  batch_x: {batch_x}")
        print(f"  batch_y: {batch_y.tolist()}")
        if batch_idx >= 1:
            break

    print("\n3. Using TensorDataset")
    print("-" * 30)
    from torch.utils.data import TensorDataset
    x = torch.randn(100, 5)
    y = torch.randn(100, 1)
    tensor_ds = TensorDataset(x, y)
    loader = DataLoader(tensor_ds, batch_size=10, shuffle=False)
    for bx, by in loader:
        print(f"Batch: x={bx.shape}, y={by.shape}")
        break

    print("\n4. DataLoader Options")
    print("-" * 30)
    loader = DataLoader(
        dataset,
        batch_size=4,
        shuffle=True,
        num_workers=0,
        drop_last=False
    )
    print(f"batch_size=4, shuffle=True, drop_last=False")

    print("\n5. Custom Dataset with Transform")
    print("-" * 30)

    class TransformedDataset(Dataset):
        def __init__(self, data, transform=None):
            self.data = data
            self.transform = transform

        def __len__(self):
            return len(self.data)

        def __getitem__(self, idx):
            sample = self.data[idx]
            if self.transform:
                sample = self.transform(sample)
            return sample

    data = [torch.tensor([i]) for i in range(5)]
    transform_ds = TransformedDataset(data, transform=lambda x: x * 2)
    print(f"Original: {data[2]}")
    print(f"After transform: {transform_ds[2]}")

    print("\n6. IterableDataset")
    print("-" * 30)

    class IterableData(torch.utils.data.IterableDataset):
        def __iter__(self):
            for i in range(8):
                yield torch.tensor([i]), torch.tensor([i * 10])

    iter_ds = IterableData()
    iter_loader = DataLoader(iter_ds, batch_size=3)
    for batch in iter_loader:
        print(f"Iterable batch: {batch}")
        break


if __name__ == "__main__":
    main()