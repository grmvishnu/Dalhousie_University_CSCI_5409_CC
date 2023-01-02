import React, { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";

const Header = ({ user }) => {
  const collapseRef = React.createRef();
  const [screenWidth, setScreenWidth] = useState(0);

  useEffect(() => {
    setScreenWidth(window.innerWidth);
  }, [screenWidth]);

  const handleCollapse = () => {
    if (screenWidth < 992) collapseRef.current.click();
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark">
      <button
        ref={collapseRef}
        className="navbar-toggler m-2 mr-auto"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span className="navbar-toggler-icon"></span>
      </button>

      <div className="collapse navbar-collapse" id="navbarSupportedContent">
        <ul className="navbar-nav mx-auto">
          {user && (
            <li className="nav-item active">
              <NavLink className="nav-link" to="/" onClick={handleCollapse}>
                Home
              </NavLink>
            </li>
          )}

          {user && (
            <li className="nav-item">
              <NavLink
                className="nav-link"
                to="/profile"
                onClick={handleCollapse}
              >
                Profile
              </NavLink>
            </li>
          )}

          {user && (
            <li className="nav-item">
              <NavLink
                className="nav-link"
                to="/convert"
                onClick={handleCollapse}
              >
                Convert
              </NavLink>
            </li>
          )}

          {user && (
            <li className="nav-item">
              <NavLink
                className="nav-link"
                to="/logout"
                onClick={handleCollapse}
              >
                Logout
              </NavLink>
            </li>
          )}

          {!user && (
            <li className="nav-item">
              <NavLink
                className="nav-link"
                to="/login"
                onClick={handleCollapse}
              >
                Login
              </NavLink>
            </li>
          )}

          {!user && (
            <li className="nav-item">
              <NavLink
                className="nav-link"
                to="/register"
                onClick={handleCollapse}
              >
                Register
              </NavLink>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Header;
