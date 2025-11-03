import API from './api';

export const getPosts = () => {
  return API.get('/posts/');
};

export const createPost = (postData: any) => {
    // We need to set up the interceptor to send the token
    const token = localStorage.getItem('access_token');
    return API.post('/posts/', postData, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
}
