# 第 19 章：專案實戰 - 部落格

## 概述

本章實作一個完整的部落格系統，包含使用者認證、文章管理、評論功能。

## 19.1 部落格資料模型

定義部落格的資料結構。

[程式檔案：19-1-blog-models.py](../_code/19/19-1-blog-models.py)

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r"^[\w\.-]+@[\w\.-]+\.\w+$")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class User(UserBase):
    id: int
    created_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: Optional[User] = None
    comments_count: int = 0

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    post_id: int
    author_id: int
    created_at: datetime
    author: Optional[User] = None

    class Config:
        from_attributes = True
```

## 19.2 部落格認證

使用者註冊和登入功能。

[程式檔案：19-2-blog-auth.py](../_code/19/19-2-blog-auth.py)

```python
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

SECRET_KEY = "secret-key-change-in-production"
ALGORITHM = "HS256"

users_db = {}
user_id_counter = 1

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/api/auth/register")
async def register(username: str, email: str, password: str):
    global user_id_counter
    if any(u.get("username") == username for u in users_db.values()):
        raise HTTPException(status_code=400, detail="Username exists")
    
    user = {
        "id": user_id_counter,
        "username": username,
        "email": email,
        "password": hash_password(password),
        "created_at": datetime.now(),
        "is_active": True
    }
    users_db[username] = user
    user_id_counter += 1
    return {"message": "User created", "username": username}

@app.post("/api/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me")
async def get_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username or username not in users_db:
            raise HTTPException(status_code=401)
        return users_db[username]
    except:
        raise HTTPException(status_code=401)
```

## 19.3 文章 API

文章的 CRUD 端點。

[程式檔案：19-3-blog-posts-api.py](../_code/19/19-3-blog-posts-api.py)

```python
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from 19-1-blog-models import Post, PostCreate

router = APIRouter(prefix="/api/posts", tags=["posts"])

posts_db = []
post_id_counter = 1

@router.get("", response_model=List[Post])
async def list_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None
):
    result = posts_db.copy()
    if search:
        result = [p for p in result if search.lower() in p.title.lower()]
    start = (page - 1) * limit
    return result[start:start+limit]

@router.post("", response_model=Post, status_code=201)
async def create_post(post: PostCreate, author_id: int = 1):
    global post_id_counter
    new_post = Post(
        id=post_id_counter,
        title=post.title,
        content=post.content,
        author_id=author_id,
        created_at=datetime.now(),
        comments_count=0
    )
    posts_db.append(new_post)
    post_id_counter += 1
    return new_post

@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: int):
    for post in posts_db:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, post: PostCreate):
    for p in posts_db:
        if p.id == post_id:
            p.title = post.title
            p.content = post.content
            return p
    raise HTTPException(status_code=404, detail="Post not found")

@router.delete("/{post_id}")
async def delete_post(post_id: int):
    global posts_db
    posts_db = [p for p in posts_db if p.id != post_id]
    return {"status": "deleted"}
```

## 19.4 評論 API

評論的 CRUD 端點。

[程式檔案：19-4-blog-comments-api.py](../_code/19/19-4-blog-comments-api.py)

```python
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from 19-1-blog-models import Comment, CommentCreate

router = APIRouter(prefix="/api/posts/{post_id}/comments", tags=["comments"])

comments_db = []
comment_id_counter = 1

@router.get("", response_model=List[Comment])
async def list_comments(post_id: int):
    return [c for c in comments_db if c.post_id == post_id]

@router.post("", response_model=Comment, status_code=201)
async def create_comment(post_id: int, comment: CommentCreate, author_id: int = 1):
    global comment_id_counter
    new_comment = Comment(
        id=comment_id_counter,
        post_id=post_id,
        content=comment.content,
        author_id=author_id,
        created_at=datetime.now()
    )
    comments_db.append(new_comment)
    comment_id_counter += 1
    return new_comment

@router.delete("/{comment_id}")
async def delete_comment(post_id: int, comment_id: int):
    global comments_db
    comments_db = [c for c in comments_db if c.id != comment_id or c.post_id != post_id]
    return {"status": "deleted"}
```

## 19.5 前端主頁面

React 前端主應用程式。

[程式檔案：19-5-blog-frontend.jsx](../_code/19/19-5-blog-frontend.jsx)

```javascript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import PostList from './pages/PostList';
import PostDetail from './pages/PostDetail';
import Login from './pages/Login';
import Register from './pages/Register';
import CreatePost from './pages/CreatePost';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <main className="container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/posts" element={<PostList />} />
            <Route path="/posts/:id" element={<PostDetail />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/create" element={<CreatePost />} />
          </Routes>
        </main>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
```

## 19.6 文章列表

顯示所有文章的頁面。

[程式檔案：19-6-blog-post-list.jsx](../_code/19/19-6-blog-post-list.jsx)

```javascript
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

function PostList() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const res = await api.get('/posts');
      setPosts(res.data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="post-list">
      <h1>Blog Posts</h1>
      {posts.length === 0 ? (
        <p>No posts yet.</p>
      ) : (
        posts.map(post => (
          <article key={post.id} className="post-card">
            <h2>
              <Link to={`/posts/${post.id}`}>{post.title}</Link>
            </h2>
            <p className="post-meta">
              By {post.author?.username || 'Anonymous'} on{' '}
              {new Date(post.created_at).toLocaleDateString()}
            </p>
            <p className="post-excerpt">
              {post.content.substring(0, 150)}...
            </p>
            <Link to={`/posts/${post.id}`} className="read-more">
              Read more
            </Link>
          </article>
        ))
      )}
    </div>
  );
}

export default PostList;
```

## 19.7 文章詳情

顯示單篇文章及其評論。

[程式檔案：19-7-blog-post-detail.jsx](../_code/19/19-7-blog-post-detail.jsx)

```javascript
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import CommentSection from '../components/CommentSection';

function PostDetail() {
  const { id } = useParams();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPost();
  }, [id]);

  const fetchPost = async () => {
    try {
      const res = await api.get(`/posts/${id}`);
      setPost(res.data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!post) return <div>Post not found</div>;

  return (
    <article className="post-detail">
      <h1>{post.title}</h1>
      <div className="post-meta">
        <span>By {post.author?.username || 'Anonymous'}</span>
        <span>{new Date(post.created_at).toLocaleDateString()}</span>
      </div>
      <div className="post-content">
        {post.content}
      </div>
      <hr />
      <CommentSection postId={post.id} />
    </article>
  );
}

export default PostDetail;
```

## 19.8 文章編輯器

建立和編輯文章的頁面。

[程式檔案：19-8-blog-editor.jsx](../_code/19/19-8-blog-editor.jsx)

```javascript
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

function CreatePost() {
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) return;

    setLoading(true);
    try {
      await api.post('/posts', { title, content });
      navigate('/posts');
    } catch (error) {
      console.error('Error creating post:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-post">
      <h1>Create New Post</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter post title"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="content">Content</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Write your post content..."
            rows="10"
            required
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Publishing...' : 'Publish'}
        </button>
      </form>
    </div>
  );
}

export default CreatePost;
```

## 19.9 評論元件

文章評論區元件。

[程式檔案：19-9-blog-comment.jsx](../_code/19/19-9-blog-comment.jsx)

```javascript
import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

function CommentSection({ postId }) {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const { user } = useAuth();

  useEffect(() => {
    fetchComments();
  }, [postId]);

  const fetchComments = async () => {
    try {
      const res = await api.get(`/posts/${postId}/comments`);
      setComments(res.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    try {
      const res = await api.post(`/posts/${postId}/comments`, {
        content: newComment
      });
      setComments([...comments, res.data]);
      setNewComment('');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleDelete = async (commentId) => {
    try {
      await api.delete(`/posts/${postId}/comments/${commentId}`);
      setComments(comments.filter(c => c.id !== commentId));
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="comment-section">
      <h3>Comments ({comments.length})</h3>
      
      {user && (
        <form onSubmit={handleSubmit} className="comment-form">
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Write a comment..."
          />
          <button type="submit">Post</button>
        </form>
      )}

      <div className="comments-list">
        {comments.map(comment => (
          <div key={comment.id} className="comment">
            <p className="comment-content">{comment.content}</p>
            <p className="comment-meta">
              {comment.author?.username} - {new Date(comment.created_at).toLocaleDateString()}
            </p>
            {user?.id === comment.author_id && (
              <button onClick={() => handleDelete(comment.id)}>Delete</button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default CommentSection;
```

## 19.10 完整實作說明

[程式檔案：19-10-blog-complete.md](../_code/19/19-10-blog-complete.md)

```markdown
# Blog System Complete Implementation

## Backend (FastAPI)
- `19-1-blog-models.py` - Pydantic models for User, Post, Comment
- `19-2-blog-auth.py` - Authentication with JWT and password hashing
- `19-3-blog-posts-api.py` - CRUD endpoints for blog posts
- `19-4-blog-comments-api.py` - Comments API endpoints

## Frontend (React)
- `19-5-blog-frontend.jsx` - Main App with routing
- `19-6-blog-post-list.jsx` - List all blog posts
- `19-7-blog-post-detail.jsx` - View single post with comments
- `19-8-blog-editor.jsx` - Create/edit blog posts
- `19-9-blog-comment.jsx` - Comment section component

## Features
1. User registration and login with JWT
2. Create, read, update, delete posts
3. Add and delete comments
4. Paginated post list
5. Search posts by title
```

## 重點回顧

| 功能 | 說明 |
|------|------|
| JWT 認證 | 使用者登入和 Token |
| 文章管理 | CRUD 操作 |
| 評論系統 | 嵌套評論 |
| 分頁 | 文章列表分頁 |

## 練習題

1. 加入文章分類功能
2. 實作文章標籤
3. 加入文章圖片上傳
4. 建立作者個人頁面
