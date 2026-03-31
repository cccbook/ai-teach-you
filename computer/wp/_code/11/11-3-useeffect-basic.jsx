import React, { useState, useEffect } from 'react';

const UseEffectBasic = () => {
  const [data, setData] = useState('');

  useEffect(() => {
    setData('Data loaded!');
  }, []);

  return <p>{data}</p>;
};

export default UseEffectBasic;
