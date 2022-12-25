import axios from "axios";

export const agent = axios.create({
  baseURL: "http://localhost:8000",
});
