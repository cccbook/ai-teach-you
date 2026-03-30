import React from 'react';

const UserCard = ({ name, email, age }) => {
  return (
    <div className="user-card">
      <h3>{name}</h3>
      <p>Email: {email}</p>
      <p>Age: {age}</p>
    </div>
  );
};

export default UserCard;
