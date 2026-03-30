import React from 'react';

const PropsDemo = (props) => {
  return (
    <div>
      <h2>Hello, {props.name}!</h2>
      <p>Age: {props.age}</p>
    </div>
  );
};

export default PropsDemo;
