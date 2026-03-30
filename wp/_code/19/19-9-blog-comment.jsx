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
