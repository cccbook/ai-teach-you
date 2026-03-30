import React, { useState, useEffect } from 'react';

const UseEffectDependency = () => {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');

  useEffect(() => {
    console.log('Count changed:', count);
  }, [count]);

  useEffect(() => {
    console.log('Name changed:', name);
  }, [name]);

  return (
    <div>
      <p>Count: {count}</p>
      <input value={name} onChange={e => setName(e.target.value)} />
      <button onClick={() => setCount(count + 1)}>Add</button>
    </div>
  );
};

export default UseEffectDependency;
