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
