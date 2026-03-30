import React, { useState, useMemo } from 'react';

const UseMemoDemo = () => {
  const [count, setCount] = useState(0);
  const [number, setNumber] = useState(5);

  const factorial = useMemo(() => {
    console.log('Calculating...');
    return [...Array(number)].map((_, i) => i + 1).reduce((a, b) => a * b, 1);
  }, [number]);

  return (
    <div>
      <p>Factorial of {number}: {factorial}</p>
      <button onClick={() => setCount(count + 1)}>Re-render: {count}</button>
      <button onClick={() => setNumber(number + 1)}>Number +</button>
    </div>
  );
};

export default UseMemoDemo;
