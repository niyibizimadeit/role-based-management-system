<template>
    <div>
      <h2>Register</h2>
  
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
  
      <button @click="register">Sign Up</button>
  
      <p v-if="error" style="color:red">{{ error }}</p>
  
      <p>
        Already have an account?
        <span @click="goLogin" style="color: blue; cursor: pointer;">
          Login
        </span>
      </p>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue"
  import api from "../api/axios"
  import { useRouter } from "vue-router"
  
  const username = ref("")
  const password = ref("")
  const error = ref("")
  const router = useRouter()
  
  const register = async () => {
    error.value = ""
  
    try {
      await api.post("/auth/register", {
        username: username.value,
        password: password.value
      })
  
      // after successful registration → go to login
      router.push("/login")
    } catch (err) {
      error.value =
        err.response?.data?.error || "Registration failed"
    }
  }
  
  const goLogin = () => {
    router.push("/login")
  }
  </script>
  