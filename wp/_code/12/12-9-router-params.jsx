import { BrowserRouter, Routes, Route, useParams } from 'react-router-dom';

const UserProfile = () => {
  const { id } = useParams();
  return <h1>User ID: {id}</h1>;
};

const PostDetail = () => {
  const { postId } = useParams();
  return <h1>Post ID: {postId}</h1>;
};

const App = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/user/:id" element={<UserProfile />} />
      <Route path="/post/:postId" element={<PostDetail />} />
    </Routes>
  </BrowserRouter>
);

export default App;
