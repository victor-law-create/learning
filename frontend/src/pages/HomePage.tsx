import React, { useEffect, useState } from 'react';
import { getPosts } from '../services/postService';
import { Link, useNavigate } from 'react-router-dom';

interface Post {
  id: number;
  author: { username: string };
  content: string;
  is_product: boolean;
  price: string;
  category: string;
}

const HomePage: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [error, setError] = useState<string | null>(null);
  const isAuthenticated = !!localStorage.getItem('access_token');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const { data } = await getPosts();
        setPosts(data);
      } catch (err) {
        setError('Failed to fetch posts.');
      }
    };
    fetchPosts();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/login');
  };

  return (
    <div>
      <nav>
        {isAuthenticated ? (
          <>
            <Link to="/create-post">Create Post</Link> | <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link> | <Link to="/register">Register</Link>
          </>
        )}
      </nav>
      <h1>Vicodom Feed</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        {posts.map((post) => (
          <div key={post.id} style={{ border: '1px solid #ccc', margin: '10px', padding: '10px' }}>
            <h3>{post.author.username}</h3>
            <p>{post.content}</p>
            {post.is_product && (
              <div>
                <p><strong>Price:</strong> ${post.price}</p>
                <p><strong>Category:</strong> {post.category}</p>
                <button>Add to Cart</button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomePage;
