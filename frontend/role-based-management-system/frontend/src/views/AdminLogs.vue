<script setup>
    import { ref, onMounted } from "vue"
    import api from "../api/axios"
    
    const logs = ref([])
    const loading = ref(false)
    const error = ref("")
    
    const loadLogs = async () => {
      loading.value = true
      error.value = ""
    
      try {
        const res = await api.get("/admin/logs")
        logs.value = res.data
      } catch (e) {
        error.value = "Failed to load logs"
      } finally {
        loading.value = false
      }
    }
    
    onMounted(loadLogs)
    </script>
    
    <template>
      <div>
        <h3>System Logs</h3>
    
        <div v-if="loading">Loading logs...</div>
        <div v-if="error" style="color:red">{{ error }}</div>
    
        <table v-if="!loading && logs.length" border="1" cellpadding="6">
          <thead>
            <tr>
              <th>Time</th>
              <th>Action</th>
              <th>Actor</th>
              <th>Target</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in logs" :key="log.id">
              <td>{{ new Date(log.timestamp).toLocaleString() }}</td>
              <td>{{ log.action }}</td>
              <td>{{ log.actor_id }}</td>
              <td>{{ log.target }}</td>
            </tr>
          </tbody>
        </table>
    
        <div v-if="!loading && logs.length === 0">
          No logs found.
        </div>
      </div>
    </template>
    