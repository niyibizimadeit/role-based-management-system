<script setup>
  import { ref, onMounted } from "vue";
  import api from "../api/axios";
  
  const users = ref([]);
  const username = ref("");
  const password = ref("");
  const role = ref("USER");
  const error = ref("");
  
  const loadUsers = async () => {
    try {
      const res = await api.get("/admin/users");
      users.value = res.data;
    } catch {
      error.value = "Failed to load users";
    }
  };
  
  const createUser = async () => {
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
    }
  };
  
  const changeRole = async (id, newRole) => {
    await api.put(`/admin/users/${id}/role`, { role: newRole });
    loadUsers();
  };
  
  const deleteUser = async (id) => {
    if (!confirm("Are you sure?")) return;
    await api.delete(`/admin/users/${id}`);
    loadUsers();
  };
  
  onMounted(loadUsers);
  </script>
  
  <template>
    <div>
      <h3>User Management</h3>
  
      <h4>Create User</h4>
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <select v-model="role">
        <option value="USER">USER</option>
        <option value="ADMIN">ADMIN</option>
      </select>
      <button @click="createUser">Create</button>
  
      <p v-if="error" style="color:red">{{ error }}</p>
  
      <hr />
  
      <h4>All Users</h4>
      <table border="1" cellpadding="5">
        <thead>
        <tr>
          <th>Username</th>
          <th>Role</th>
          <th>Actions</th>
        </tr>
        </thead>

        <tbody>
        <tr v-for="u in users" :key="u.id">
          <td>{{ u.username }}</td>
          <td>{{ u.role }}</td>
          <td>
            <button @click="changeRole(u.id, 'ADMIN')">Make Admin</button>
            <button @click="changeRole(u.id, 'USER')">Make User</button>
            <button @click="deleteUser(u.id)" style="color:red">Delete</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </template>
  