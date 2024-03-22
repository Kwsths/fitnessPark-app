import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/auth";

const Home = () => {
  const auth = useAuth();
  const navigate = useNavigate();
  return (
    <div className="home">
      <div className="header">
        <h1 className="title">REST APIs with Flask and Python</h1>
      </div>

      <div className="nav-links">
        <Link to="/athletes">Users</Link>
        {auth.isLoggedIn ? (
          <span
            style={{ cursor: "pointer", color: "#007bff" }}
            onClick={() =>
              auth.signout(() => {
                navigate("/");
              })
            }
          >
            Logout
          </span>
        ) : (
          <Link to="/signin">Login</Link>
        )}
      </div>
    </div>
  );
};

export default Home;
