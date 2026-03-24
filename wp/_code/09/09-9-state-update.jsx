import React, { useState } from 'react';

const StateUpdate = () => {
  const [text, setText] = useState('Hello');

  const updateText = () => {
    setText(text === 'Hello' ? 'World' : 'Hello');
  };

  return (
    <div>
      <p>{text}</p>
      <button onClick={updateText}>Toggle</button>
    </div>
  );
};

export default StateUpdate;
