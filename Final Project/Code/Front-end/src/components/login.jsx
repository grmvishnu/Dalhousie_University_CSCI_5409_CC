import Joi from "joi";
import { useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import Input from "./input";
import auth from "../services/authService";

const Login = () => {
  const [user, setUser] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState({});

  const handleChange = ({ currentTarget: input }) => {
    const account = { ...user };
    account[input.name] = input.value;
    setUser(account);
  };

  const schema = Joi.object({
    email: Joi.string()
      .email({ tlds: { allow: false } })
      .required()
      .label("Email"),
    password: Joi.string().min(8).required().label("Password"),
  });

  const validate = () => {
    const result = schema.validate(user, { abortEarly: false });

    if (!result.error) {
      return null;
    }
    const errors = {};
    for (let item of result.error.details) {
      errors[item.path[0]] = item.message;
    }

    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const errors = validate();
    setErrors(errors || {});
    if (errors) {
      return;
    }

    try {
      await auth.login(user.email, user.password);
      window.location = "/";
    } catch (ex) {
      if (
        ex.response &&
        ex.response.status >= 400 &&
        ex.response.status < 500
      ) {
        toast.error(ex.response.data.detail);
      }
    }
  };

  return (
    <form className="form-layout text-center" onSubmit={handleSubmit}>
      <Input
        type="text"
        placeholder="Email"
        name="email"
        onChange={handleChange}
        value={user.email}
        error={errors.email}
      />
      <Input
        type="password"
        placeholder="Password"
        name="password"
        onChange={handleChange}
        value={user.password}
        error={errors.password}
      />

      <button className="btn btn-primary">Sign In</button>
      <div className="text-center">
        <span>New User? </span>
        <Link to="/register" className="auth-link">
          Register
        </Link>
      </div>
    </form>
  );
};

export default Login;
