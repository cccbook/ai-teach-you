import React from 'react';

const name = 'Alice';
const age = 25;

const element = (
  <div>
    <h1>Hello, {name}!</h1>
    <p>You are {age} years old.</p>
    <p>Next year: {age + 1}</p>
  </div>
);

export default element;
