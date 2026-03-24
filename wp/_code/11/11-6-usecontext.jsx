import React, { createContext, useContext } from 'react';

const ThemeContext = createContext('light');

const ThemedButton = () => {
  const theme = useContext(ThemeContext);
  return <button className={theme}>Button</button>;
};

const App = () => (
  <ThemeContext.Provider value="dark">
    <ThemedButton />
  </ThemeContext.Provider>
);

export default App;
