<template>
    <div>
      <h2>Admin Panel</h2>
  
      <nav>
        <button @click="tab = 'posts'">Moderate Posts</button>
        <button @click="tab = 'users'">Manage Users</button>
        <button @click="() => { console.log('LOGS CLICKED'); tab = 'logs' }">
            Logs
        </button>

        <AdminLogs v-if="view === 'logs'" />

      </nav>
  


      <AdminPosts
      v-if="tab === 'posts'"
      :key="tab"
      />

      <AdminUsers
      v-if="tab === 'users'"
      :key="tab"
      />

      <AdminLogs
      v-if="tab === 'logs'"
      :key="tab"
      />

    </div>
  </template>
  
  <script setup>
  import { ref } from "vue"
  import AdminPosts from "./AdminPosts.vue"
  import AdminUsers from "./AdminUsers.vue"
  import AdminLogs from "./AdminLogs.vue"

  
  const tab = ref("posts")
  
  </script>
  