import React from 'react';

const Header = () => <header><h1>My App</h1></header>;

const Content = () => <main><p>Main content</p></main>;

const Footer = () => <footer><p>Footer</p></footer>;

const App = () => (
  <div>
    <Header />
    <Content />
    <Footer />
  </div>
);

export default App;
