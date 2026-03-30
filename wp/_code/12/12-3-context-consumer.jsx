import React from 'react';
import ThemeContext from './12-1-context-basic.jsx';

const ThemedContent = () => (
  <ThemeContext.Consumer>
    {({ theme }) => (
      <div className={theme}>
        <p>Current theme: {theme}</p>
      </div>
    )}
  </ThemeContext.Consumer>
);

export default ThemedContent;
