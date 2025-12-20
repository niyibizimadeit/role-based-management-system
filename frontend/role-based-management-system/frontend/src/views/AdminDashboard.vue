<template>
  <div class="admin-container">
    <header class="admin-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="admin-title">Admin Panel</h1>
          <p class="admin-subtitle">Manage your platform</p>
        </div>
        <button @click="logout" class="logout-btn">
          <svg class="logout-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
          </svg>
          Logout
        </button>
      </div>
    </header>

    <nav class="admin-nav">
      <div class="nav-container">
        <button
          @click="tab = 'posts'"
          :class="['nav-btn', { active: tab === 'posts' }]"
        >
          <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          Moderate Posts
        </button>
        <button
          @click="tab = 'users'"
          :class="['nav-btn', { active: tab === 'users' }]"
        >
          <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
          </svg>
          Manage Users
        </button>
        <button
          @click="tab = 'logs'"
          :class="['nav-btn', { active: tab === 'logs' }]"
        >
          <svg class="nav-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
          </svg>
          System Logs
        </button>
      </div>
    </nav>

    <main class="admin-main">
      <AdminPosts v-if="tab === 'posts'" :key="tab" />
      <AdminUsers v-if="tab === 'users'" :key="tab" />
      <AdminLogs v-if="tab === 'logs'" :key="tab" />
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import AdminPosts from "./AdminPosts.vue"
import AdminUsers from "./AdminUsers.vue"
import AdminLogs from "./AdminLogs.vue"

const tab = ref("posts")
const router = useRouter()

const logout = () => {
  localStorage.removeItem("token")
  localStorage.removeItem("role")
  router.push("/login")
}
</script>

<style scoped>
.admin-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #F5F5DC 0%, #FAF0E6 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.admin-header {
  background: white;
  border-bottom: 1px solid #F0EDE6;
  box-shadow: 0 2px 10px rgba(139, 69, 19, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.admin-title {
  font-size: 32px;
  font-weight: 700;
  color: #2F2F2F;
  margin: 0;
  font-family: 'Georgia', serif;
}

.admin-subtitle {
  color: #5C5C5C;
  font-size: 16px;
  margin: 0;
  font-weight: 400;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: #8B4513;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: #CD853F;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(139, 69, 19, 0.3);
}

.logout-icon {
  width: 16px;
  height: 16px;
}

.admin-nav {
  background: white;
  border-bottom: 1px solid #F0EDE6;
  box-shadow: 0 1px 3px rgba(139, 69, 19, 0.05);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  gap: 8px;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 24px;
  background: #FAF9F6;
  border: 2px solid #F0EDE6;
  border-bottom: none;
  color: #5C5C5C;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 12px 12px 0 0;
  position: relative;
}

.nav-btn:hover {
  background: #F5F5DC;
  color: #2F2F2F;
}

.nav-btn.active {
  background: #D2B48C;
  color: white;
  border-color: #D2B48C;
}

.nav-btn.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: #D2B48C;
}

.nav-icon {
  width: 18px;
  height: 18px;
}

.admin-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px 24px;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
    text-align: center;
  }

  .admin-title {
    font-size: 28px;
  }

  .nav-container {
    flex-direction: column;
    padding: 16px;
  }

  .nav-btn {
    justify-content: center;
    border-radius: 8px;
    border: 2px solid #F0EDE6;
  }

  .nav-btn.active::after {
    display: none;
  }

  .admin-main {
    padding: 16px;
  }
}
</style>