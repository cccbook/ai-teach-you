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
