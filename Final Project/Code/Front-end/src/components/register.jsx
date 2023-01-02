import { useState } from "react";
import { Link } from "react-router-dom";
import Input from "./input";
import Joi from "joi";
import ListError from "./listError";

import { register } from "../services/userService";
import auth from "../services/authService";
import { toast } from "react-toastify";

const Register = () => {
  const [user, setUser] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [errors, setErrors] = useState({});

  const handleChange = ({ currentTarget: input }) => {
    const account = { ...user };
    account[input.name] = input.value;
    setUser(account);
  };

  const schema = Joi.object({
    firstName: Joi.string().required().label("First Name"),
    lastName: Joi.string().required().label("Last Name"),
    email: Joi.string()
      .email({ tlds: { allow: false } })
      .required()
      .label("Email"),
    password: Joi.string().min(8).required().label("Password"),
    confirmPassword: Joi.any()
      .equal(Joi.ref("password"))
      .required()
      .messages({ "any.only": "Password does not match" }),
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
      await register({
        firstName: user.firstName,
        lastName: user.lastName,
        email: user.email,
        password: user.password,
      });
      await auth.login(user.email, user.password);
      window.location = "/";
    } catch (ex) {
      if (
        ex.response &&
        ex.response.status >= 400 &&
        ex.response.status < 500
      ) {
        toast.error(<ListError errors={Object.values(ex.response.data)} />, {
          icon: false,
        });
      }
    }
  };

  return (
    <form className="form-layout text-center" onSubmit={handleSubmit}>
      <Input
        type="text"
        placeholder="First Name"
        name="firstName"
        onChange={handleChange}
        value={user.firstName}
        error={errors.firstName}
      />
      <Input
        type="text"
        placeholder="Last Name"
        name="lastName"
        onChange={handleChange}
        value={user.lastName}
        error={errors.lastName}
      />
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
      <Input
        type="password"
        placeholder="Confirm Password"
        name="confirmPassword"
        onChange={handleChange}
        value={user.confirmPassword}
        error={errors.confirmPassword}
      />
      <button className="btn btn-primary">Register</button>
      <div className="text-center">
        <Link to="/login" className="auth-link">
          Already have an account?
        </Link>
      </div>
    </form>
  );
};

export default Register;
