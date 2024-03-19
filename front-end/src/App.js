import * as React from "react";
import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./hooks/auth";
import PrivateRoute from "./routes/PrivateRoute";
import Users from "./components/user/Users";
import LoginPage from "./components/auth/Login";
import Register from "./components/auth/Register";
import Products from "./components/product/Products";
import Home from "./components";
import NotFound from "./components/NotFound";

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Home />} />
        <Route
          path="/users"
          element={
            <PrivateRoute>
              <Users />
            </PrivateRoute>
          }
        />
        <Route
          path="/users/:userId"
          element={
            <PrivateRoute>
              <Products />
            </PrivateRoute>
          }
        />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </AuthProvider>
  );
}
