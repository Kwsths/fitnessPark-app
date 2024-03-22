import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../hooks/auth";
import UserCard from "./UserCard";
import axiosInstance from "../../services/axiosInstance";
import NewShopModal from "./NewShopModal";

const Users = () => {
  let navigate = useNavigate();
  let auth = useAuth();
  const [users, setUsers] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  React.useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axiosInstance.get("/users");
        setUsers(response.data);
      } catch (error) {
        console.error("Error fetching shops:", error);
      }
    };

    fetchUsers();
  }, []);

  const handleDelete = async (id) => {
    try {
      await axiosInstance.delete(`/users/${id}`);
      setUsers(users.filter((user) => user.id !== id));
    } catch (error) {
      console.error("Error deleting shop:", error);
    }
  };

  const handleShopClick = (id) => {
    navigate(`/athletes/${id}`);
  };

  const handleLogout = () => {
    auth.signout(() => {
      navigate("/");
    });
  };

  return (
    <div className="users">
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <Link to="/">Home</Link>
        <span style={{ fontWeight: "bold", fontSize: "32px" }}>All Users</span>
        <button onClick={handleLogout} className="signout-button">
          Logout
        </button>
      </div>

      <div className="user-list">
        {users.map((user) => (
          <UserCard
            key={user.id}
            id={user.id}
            username={user.username}
            onDelete={handleDelete}
            onClick={handleShopClick}
          />
        ))}
      </div>

    </div>
  );
};

export default Users;
