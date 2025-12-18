<template>
    <div>
      <h2>Login</h2>
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button @click="login">Login</button>
      <p v-if="error">{{ error }}</p>
    </div>
  </template>
  
  <script setup>
  localStorage.removeItem("token");
localStorage.removeItem("role");

  import { ref } from "vue";
  import api from "../api/axios";
  import { useRouter } from "vue-router";
  
  const username = ref("");
  const password = ref("");
  const error = ref("");
  const router = useRouter();
  
  const login = async () => {
    try {
      const res = await api.post("/auth/login", {
        username: username.value,
        password: password.value,
      });
  
      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("role", res.data.role);
  
      if (res.data.role === "ADMIN") {
        router.push("/admin");
      } else {
        router.push("/dashboard");
      }

    } catch {
      error.value = "Invalid credentials";
    }
  };
  </script>
  