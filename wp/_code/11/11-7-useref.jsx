import React, { useRef } from 'react';

const UseRefDemo = () => {
  const inputRef = useRef(null);
  const countRef = useRef(0);

  const focusInput = () => {
    inputRef.current.focus();
  };

  const increment = () => {
    countRef.current += 1;
    console.log('Count:', countRef.current);
  };

  return (
    <div>
      <input ref={inputRef} />
      <button onClick={focusInput}>Focus</button>
      <button onClick={increment}>Count</button>
    </div>
  );
};

export default UseRefDemo;
