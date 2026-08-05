import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Auth() {
  const navigate = useNavigate();

  const [isLogin, setIsLogin] = useState(true);

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async () => {
    try {
      if (isLogin) {
        const response = await api.post("/login", {
          email,
          password,
        });

        localStorage.setItem(
          "token",
          response.data.access_token
        );

        navigate("/chat");
      } else {
        await api.post("/register", {
          username,
          email,
          password,
        });

        alert("Registration Successful!");

        setIsLogin(true);
      }
    } catch (error) {
      alert(error.response?.data?.detail || "Something went wrong");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>ChatGPT Clone</h1>

        <h2>{isLogin ? "Sign In" : "Create Account"}</h2>

        {!isLogin && (
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        )}

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleSubmit}>
          {isLogin ? "Login" : "Register"}
        </button>

        <p>
          {isLogin
            ? "Don't have an account?"
            : "Already have an account?"}

          <span
            onClick={() => setIsLogin(!isLogin)}
            style={{
              color: "#10a37f",
              cursor: "pointer",
              marginLeft: "5px",
            }}
          >
            {isLogin ? "Register" : "Login"}
          </span>
        </p>
      </div>
    </div>
  );
}

export default Auth;