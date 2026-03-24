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
