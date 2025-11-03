import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createPost } from '../services/postService';

const CreatePostPage: React.FC = () => {
  const [content, setContent] = useState('');
  const [isProduct, setIsProduct] = useState(false);
  const [price, setPrice] = useState('');
  const [category, setCategory] = useState('');
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    const postData = {
      content,
      is_product: isProduct,
      price: isProduct ? price : null,
      category: isProduct ? category : '',
    };
    try {
      await createPost(postData);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred while creating the post.');
    }
  };

  return (
    <div>
      <h1>Create a New Post</h1>
      <form onSubmit={handleSubmit}>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <div>
          <label>Content:</label>
          <textarea value={content} onChange={(e) => setContent(e.target.value)} required />
        </div>
        <div>
          <label>
            <input type="checkbox" checked={isProduct} onChange={(e) => setIsProduct(e.target.checked)} />
            Is this a product for sale?
          </label>
        </div>
        {isProduct && (
          <>
            <div>
              <label>Price:</label>
              <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} required />
            </div>
            <div>
              <label>Category:</label>
              <input type="text" value={category} onChange={(e) => setCategory(e.target.value)} required />
            </div>
          </>
        )}
        <button type="submit">Create Post</button>
      </form>
    </div>
  );
};

export default CreatePostPage;
