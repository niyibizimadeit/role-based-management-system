<script setup>
  import { ref, onMounted } from "vue";
  import api from "../api/axios";

  const users = ref([]);
  const username = ref("");
  const password = ref("");
  const role = ref("USER");
  const error = ref("");
  const loading = ref(false);

  const loadUsers = async () => {
    try {
      const res = await api.get("/admin/users");
      users.value = res.data;
    } catch {
      error.value = "Failed to load users";
    }
  };

  const createUser = async () => {
    if (!username.value || !password.value) return;

    loading.value = true;
    error.value = "";

    try {
      await api.post("/admin/users", {
        username: username.value,
        password: password.value,
        role: role.value,
      });
      username.value = "";
      password.value = "";
      role.value = "USER";
      loadUsers();
    } catch (e) {
      error.value = e.response?.data?.error || "Failed to create user";
    } finally {
      loading.value = false;
    }
  };

  const changeRole = async (id, newRole) => {
    try {
      await api.put(`/admin/users/${id}/role`, { role: newRole });
      loadUsers();
    } catch (e) {
      console.error("Failed to change role:", e);
    }
  };

  const deleteUser = async (id) => {
    if (!confirm("Are you sure you want to delete this user?")) return;
    try {
      await api.delete(`/admin/users/${id}`);
      loadUsers();
    } catch (e) {
      console.error("Failed to delete user:", e);
    }
  };

  onMounted(loadUsers);
</script>

<template>
  <div class="admin-users-container">
    <div class="section-header">
      <h2 class="section-title">User Management</h2>
      <p class="section-subtitle">Create and manage user accounts and permissions</p>
    </div>

    <!-- Create User Form -->
    <div class="create-user-section">
      <div class="form-card">
        <div class="form-header">
          <h3 class="form-title">Create New User</h3>
          <p class="form-subtitle">Add a new user to the platform</p>
        </div>

        <form class="user-form" @submit.prevent="createUser">
          <div class="form-row">
            <div class="form-group">
              <label for="username" class="form-label">Username</label>
              <input
                id="username"
                v-model="username"
                type="text"
                placeholder="Enter username"
                class="form-input"
                required
                minlength="3"
              />
            </div>

            <div class="form-group">
              <label for="password" class="form-label">Password</label>
              <input
                id="password"
                v-model="password"
                type="password"
                placeholder="Enter password"
                class="form-input"
                required
                minlength="6"
              />
            </div>

            <div class="form-group">
              <label for="role" class="form-label">Role</label>
              <select v-model="role" class="form-select" required>
                <option value="USER">User</option>
                <option value="ADMIN">Administrator</option>
              </select>
            </div>
          </div>

          <button type="submit" class="create-user-btn" :disabled="!username || !password || loading">
            <svg v-if="!loading" class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
            </svg>
            <div v-if="loading" class="btn-loader"></div>
            <span>{{ loading ? 'Creating...' : 'Create User' }}</span>
          </button>
        </form>

        <div v-if="error" class="error-message">
          <svg class="error-icon" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
          </svg>
          {{ error }}
        </div>
      </div>
    </div>

    <!-- Users List -->
    <div class="users-section">
      <div class="section-header">
        <h3 class="section-title">All Users</h3>
        <p class="section-subtitle">Manage existing user accounts</p>
      </div>

      <div v-if="users.length > 0" class="users-table-container">
        <table class="users-table">
          <thead>
            <tr>
              <th class="username-col">Username</th>
              <th class="role-col">Role</th>
              <th class="status-col">Status</th>
              <th class="actions-col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id" class="user-row">
              <td class="username-cell">
                <div class="user-info">
                  <div class="user-avatar">
                    {{ user.username.charAt(0).toUpperCase() }}
                  </div>
                  <span class="username">{{ user.username }}</span>
                </div>
              </td>
              <td class="role-cell">
                <span class="role-badge" :class="user.role.toLowerCase()">
                  {{ user.role }}
                </span>
              </td>
              <td class="status-cell">
                <span class="status-indicator" :class="user.is_active ? 'active' : 'inactive'">
                  {{ user.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="actions-cell">
                <div class="action-buttons">
                  <button
                    v-if="user.role !== 'ADMIN'"
                    @click="changeRole(user.id, 'ADMIN')"
                    class="action-btn promote-btn"
                    title="Make Administrator"
                  >
                    <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path>
                    </svg>
                    Promote
                  </button>
                  <button
                    v-if="user.role !== 'USER'"
                    @click="changeRole(user.id, 'USER')"
                    class="action-btn demote-btn"
                    title="Make Regular User"
                  >
                    <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"></path>
                    </svg>
                    Demote
                  </button>
                  <button
                    @click="deleteUser(user.id)"
                    class="action-btn delete-btn"
                    title="Delete User"
                  >
                    <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
        </svg>
        <h3>No users found</h3>
        <p>Create your first user account above.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-users-container {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.section-header {
  text-align: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 28px;
  font-weight: 700;
  color: #2F2F2F;
  margin: 0 0 8px 0;
  font-family: 'Georgia', serif;
}

.section-subtitle {
  color: #5C5C5C;
  font-size: 16px;
  margin: 0;
  font-weight: 400;
}

.create-user-section {
  display: flex;
  justify-content: center;
}

.form-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(139, 69, 19, 0.08);
  border: 1px solid #F5F5DC;
  padding: 32px;
  width: 100%;
  max-width: 800px;
}

.form-header {
  text-align: center;
  margin-bottom: 24px;
}

.form-title {
  font-size: 24px;
  font-weight: 700;
  color: #2F2F2F;
  margin: 0 0 8px 0;
  font-family: 'Georgia', serif;
}

.form-subtitle {
  color: #5C5C5C;
  font-size: 16px;
  margin: 0;
}

.user-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
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
}

.form-input, .form-select {
  padding: 12px 16px;
  border: 2px solid #F0EDE6;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  background: #FAF9F6;
  color: #2F2F2F;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #D2B48C;
  box-shadow: 0 0 0 3px rgba(210, 180, 140, 0.1);
  background: white;
}

.form-select {
  cursor: pointer;
}

.create-user-btn {
  align-self: flex-start;
  padding: 14px 28px;
  background: linear-gradient(135deg, #D2B48C 0%, #CD853F 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 8px rgba(139, 69, 19, 0.2);
}

.create-user-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(139, 69, 19, 0.3);
}

.create-user-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

.btn-loader {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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

.users-table-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(139, 69, 19, 0.08);
  border: 1px solid #F5F5DC;
  overflow: hidden;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table thead {
  background: linear-gradient(135deg, #FAF9F6 0%, #F5F5DC 100%);
}

.users-table th {
  padding: 16px 20px;
  text-align: left;
  font-weight: 600;
  color: #2F2F2F;
  border-bottom: 2px solid #F0EDE6;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.users-table td {
  padding: 16px 20px;
  border-bottom: 1px solid #F0EDE6;
}

.user-row:hover {
  background: #FAF9F6;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #D2B48C 0%, #CD853F 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
}

.username {
  font-weight: 600;
  color: #2F2F2F;
}

.role-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.role-badge.admin {
  background: #FEE2E2;
  color: #DC2626;
}

.role-badge.user {
  background: #DBEAFE;
  color: #2563EB;
}

.status-indicator {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-indicator.active {
  background: #D1FAE5;
  color: #065F46;
}

.status-indicator.inactive {
  background: #F3F4F6;
  color: #6B7280;
}

.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.promote-btn {
  background: #10B981;
  color: white;
}

.action-btn.promote-btn:hover {
  background: #059669;
  transform: translateY(-1px);
}

.action-btn.demote-btn {
  background: #F59E0B;
  color: white;
}

.action-btn.demote-btn:hover {
  background: #D97706;
  transform: translateY(-1px);
}

.action-btn.delete-btn {
  background: #DC2626;
  color: white;
}

.action-btn.delete-btn:hover {
  background: #B91C1C;
  transform: translateY(-1px);
}

.btn-icon {
  width: 14px;
  height: 14px;
}

.empty-state {
  text-align: center;
  padding: 64px 32px;
  color: #5C5C5C;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(139, 69, 19, 0.08);
  border: 1px solid #F5F5DC;
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  color: #D2B48C;
}

.empty-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: #2F2F2F;
  margin: 0 0 8px 0;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .users-table-container {
    overflow-x: auto;
  }

  .users-table {
    min-width: 600px;
  }

  .action-buttons {
    flex-direction: column;
    align-items: flex-start;
  }

  .section-title {
    font-size: 24px;
  }

  .form-card {
    padding: 24px;
  }
}
</style>