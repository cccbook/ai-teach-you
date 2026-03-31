import React, { useState, useCallback } from 'react';

const UseCallbackDemo = () => {
  const [count, setCount] = useState(0);

  const handleClick = useCallback(() => {
    console.log('Clicked!');
  }, []);

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <button onClick={handleClick}>Click Me</button>
    </div>
  );
};

export default UseCallbackDemo;
