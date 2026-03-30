# Django

## 概述

Django 是 Python 的高階 Web 框架，強調快速開發和實用設計。內建 ORM、管理介面、表單處理等完整功能。

## 核心概念

### MTV 架構

- **Model**：資料模型定義
- **Template**：前端模板
- **View**：業務邏輯處理

### 模型

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
```

### 視圖

```python
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
```

### URL 配置

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]
```

## 特色功能

| 功能 | 說明 |
|------|------|
| ORM | 強大的資料庫抽象層 |
| 管理介面 | 自動生成的後台管理 |
| 表單處理 | 表單驗證和渲染 |
| 認證系統 | 內建用戶認證 |
| 快取框架 | 多種快取後端支援 |

## 參考資源

- [Django 官方網站](https://www.djangoproject.com/)
- [Django 中文文檔](https://docs.djangoproject.com/zh-hans/)
