import axios from "axios";

const api = axios.create({
  
  baseURL: "https://chatgpt-clone-2-a5ev.onrender.com",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;