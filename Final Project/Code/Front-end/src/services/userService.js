import http from "./httpService";

const authApiEndpoint = "/auth/users/";

export function register(user) {
  return http.post(authApiEndpoint, {
    email: user.email,
    first_name: user.firstName,
    last_name: user.lastName,
    password: user.password,
  });
}
