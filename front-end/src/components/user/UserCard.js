import React from 'react';

const UserCard = ({ id, username, onDelete, onClick }) => {
  const handleDelete = (event) => {
    event.stopPropagation();
    onDelete(id);
  };

  const handleClick = () => {
    onClick(id);
  };

  return (
    <div className="user-card" onClick={handleClick}>
      <h3>{username}</h3>
      <button onClick={handleDelete} className="delete-button">
        Delete
      </button>
    </div>
  );
};

export default UserCard;
