<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1 class="login-title">Welcome Back</h1>
        <p class="login-subtitle">Sign in to your account</p>
      </div>

      <form class="login-form" @submit.prevent="login">
        <div class="form-group">
          <label for="username" class="form-label">Username</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="Enter your username"
            class="form-input"
            required
          />
        </div>

        <div class="form-group">
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Enter your password"
            class="form-input"
            required
          />
        </div>

        <button type="submit" class="login-btn" :disabled="!username || !password">
          <span class="btn-text">Sign In</span>
          <div class="btn-loader" v-if="loading"></div>
        </button>
      </form>

      <div class="login-footer">
        <p class="signup-text">
          Don't have an account?
          <button @click="goRegister" class="signup-link">Sign up</button>
        </p>
      </div>

      <div v-if="error" class="error-message">
        <svg class="error-icon" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
        </svg>
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import api from "../api/axios";
  import { useRouter } from "vue-router";

  const username = ref("");
  const password = ref("");
  const error = ref("");
  const loading = ref(false);
  const router = useRouter();

  const login = async () => {
    if (!username.value || !password.value) return;

    loading.value = true;
    error.value = "";

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
    } finally {
      loading.value = false;
    }
  };

  const goRegister = () => {
    router.push("/register");
  };
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #F5F5DC 0%, #FAF0E6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(139, 69, 19, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 400px;
  border: 1px solid #F5F5DC;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-title {
  font-size: 28px;
  font-weight: 700;
  color: #2F2F2F;
  margin: 0 0 8px 0;
  font-family: 'Georgia', serif;
}

.login-subtitle {
  color: #5C5C5C;
  font-size: 16px;
  margin: 0;
  font-weight: 400;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  font-weight: 600;
  color: #2F2F2F;
  margin-bottom: 4px;
}

.form-input {
  padding: 16px;
  border: 2px solid #F0EDE6;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.3s ease;
  background: #FAF9F6;
  color: #2F2F2F;
}

.form-input:focus {
  outline: none;
  border-color: #D2B48C;
  box-shadow: 0 0 0 3px rgba(210, 180, 140, 0.1);
  background: white;
}

.form-input::placeholder {
  color: #A0A0A0;
}

.login-btn {
  background: linear-gradient(135deg, #D2B48C 0%, #CD853F 100%);
  color: white;
  border: none;
  padding: 16px 24px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(139, 69, 19, 0.3);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-loader {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.login-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #F0EDE6;
}

.signup-text {
  color: #5C5C5C;
  font-size: 14px;
  margin: 0;
}

.signup-link {
  background: none;
  border: none;
  color: #8B4513;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  font-size: 14px;
  padding: 0;
  margin-left: 4px;
  transition: color 0.3s ease;
}

.signup-link:hover {
  color: #CD853F;
}

.error-message {
  background: #FEF2F2;
  border: 1px solid #FECACA;
  color: #DC2626;
  padding: 12px 16px;
  border-radius: 8px;
  margin-top: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.error-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

@media (max-width: 480px) {
  .login-card {
    padding: 24px;
    margin: 16px;
  }

  .login-title {
    font-size: 24px;
  }
}
</style>