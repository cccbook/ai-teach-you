import torch
import torch.nn as nn

print("=" * 60)
print("08-6: Transfer Learning and Fine-Tuning")
print("=" * 60)

print("\n--- Loading Pretrained Model ---")
model = nn.Sequential(
    nn.Conv2d(3, 64, 3, padding=1),
    nn.ReLU(),
    nn.AdaptiveAvgPool2d((1, 1)),
    nn.Flatten(),
    nn.Linear(64, 10)
)

print("Created a dummy model (simulating pretrained)")

print("\n--- Freezing Layers ---")
for param in model[:3].parameters():
    param.requires_grad = False

print("Frozen first 3 layers (conv, relu, pool)")
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Total params: {total_params:,}, Trainable: {trainable_params:,}")

print("\n--- Fine-Tuning Strategy ---")
def apply_fine_tuning(model, strategy='full'):
    if strategy == 'full':
        for param in model.parameters():
            param.requires_grad = True
    elif strategy == 'classifier':
        for param in model[:-1].parameters():
            param.requires_grad = False
    elif strategy == 'partial':
        layers_to_freeze = list(model.children())[:3]
        for layer in layers_to_freeze:
            for param in layer.parameters():
                param.requires_grad = False
    return model

model2 = apply_fine_tuning(model, strategy='classifier')
trainable = sum(p.numel() for p in model2.parameters() if p.requires_grad)
print(f"Strategy 'classifier': {trainable:,} trainable params")

model3 = apply_fine_tuning(model, strategy='partial')
trainable = sum(p.numel() for p in model3.parameters() if p.requires_grad)
print(f"Strategy 'partial': {trainable:,} trainable params")

print("\n--- Using torchvision models ---")
try:
    from torchvision.models import resnet18, ResNet18_Weights
    model_resnet = resnet18(weights=ResNet18_Weights.DEFAULT)
    print(f"ResNet18 loaded: {sum(p.numel() for p in model_resnet.parameters()):,} params")
    
    model_resnet.fc = nn.Linear(512, 10)
    print("Replaced final layer for 10-class classification")
    
    print("\n--- Freeze Backbone ---")
    for param in model_resnet.parameters():
        param.requires_grad = False
    for param in model_resnet.fc.parameters():
        param.requires_grad = True
    print("Frozen backbone, only final layer trainable")
    
except Exception as e:
    print(f"Note: {e}")

print("\n--- Learning Rate Scheduling ---")
base_lr = 0.001
lr_multiply = 10
def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']

optimizer = torch.optim.SGD([
    {'params': model.fc.parameters(), 'lr': base_lr * lr_multiply},
    {'params': model[0].parameters(), 'lr': base_lr}
], momentum=0.9)

print(f"Classifier LR: {get_lr(optimizer)}")
print(f"Backbone LR: {get_lr(optimizer)}")

print("\n--- Data Augmentation for Transfer Learning ---")
from torchvision import transforms
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
test_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
print("Training transform: RandomCrop, Flip, ColorJitter + ImageNet normalization")
print("Test transform: Resize, CenterCrop + ImageNet normalization")