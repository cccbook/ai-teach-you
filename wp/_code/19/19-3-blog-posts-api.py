from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from 19-1-blog-models import Post, PostCreate

router = APIRouter(prefix="/api/posts", tags=["posts"])

posts_db = []
post_id_counter = 1

def get_current_user(token: str = None):
    from 19-2-blog-auth import verify_request
    return verify_request(token)

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
