import "./App.css";
import React, { useState, useEffect } from "react";
import { ToastContainer } from "react-toastify";
import { Route, Routes, Navigate } from "react-router-dom";
import Login from "./components/login";
import Register from "./components/register";
import Home from "./components/home";
import NotFound from "./components/notFound";
import Logout from "./components/logout";
import Convert from "./components/convert";
import Header from "./components/header";
import Profile from "./components/profile";
import { ProtectedRoute } from "./components/ProtectedRoute";
import auth from "./services/authService";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const getData = async () => {
      const currentUser = await auth.getCurrentUser();
      setUser(currentUser);
    };

    getData();
  }, []);

  return (
    <React.Fragment>
      <ToastContainer />
      <Header user={user} />
      <div className="container pt-4">
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/not-found" element={<NotFound />} />
          <Route
            path="/logout"
            element={
              <ProtectedRoute user={user}>
                <Logout />
              </ProtectedRoute>
            }
          />
          <Route
            path="/convert"
            element={
              <ProtectedRoute user={user}>
                <Convert />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute user={user}>
                <Profile />
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<Home />} />
          <Route path="*" element={<Navigate to="/not-found" />} />
        </Routes>
      </div>
    </React.Fragment>
  );
}

export default App;
