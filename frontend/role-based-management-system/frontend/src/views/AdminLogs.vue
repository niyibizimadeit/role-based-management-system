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

    const formatDate = (timestamp) => {
      return new Date(timestamp).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }

    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    }

    const formatAction = (action) => {
      return action.replace(/_/g, ' ').toLowerCase().replace(/\b\w/g, l => l.toUpperCase())
    }

    const getActionClass = (action) => {
      if (action.includes('CREATE') || action.includes('REGISTER')) return 'create'
      if (action.includes('UPDATE') || action.includes('EDIT')) return 'update'
      if (action.includes('DELETE')) return 'delete'
      if (action.includes('LOGIN')) return 'auth'
      if (action.includes('APPROVE')) return 'approve'
      if (action.includes('REJECT')) return 'reject'
      return 'other'
    }

    const getActionIcon = (action) => {
      if (action.includes('CREATE') || action.includes('REGISTER')) {
        return 'M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z'
      }
      if (action.includes('UPDATE') || action.includes('EDIT')) {
        return 'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z'
      }
      if (action.includes('DELETE')) {
        return 'M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16'
      }
      if (action.includes('LOGIN')) {
        return 'M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1'
      }
      if (action.includes('APPROVE')) {
        return 'M5 13l4 4L19 7'
      }
      if (action.includes('REJECT')) {
        return 'M6 18L18 6M6 6l12 12'
      }
      return 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
    }

    const getLogTypeClass = (action) => {
      if (action.includes('DELETE') || action.includes('REJECT')) return 'danger'
      if (action.includes('CREATE') || action.includes('APPROVE')) return 'success'
      if (action.includes('UPDATE') || action.includes('EDIT')) return 'warning'
      return 'info'
    }

    onMounted(loadLogs)
    </script>

    <style scoped>
    .admin-logs-container {
      display: flex;
      flex-direction: column;
      gap: 24px;
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

    .loading-state {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 16px;
      padding: 48px;
      color: #5C5C5C;
    }

    .loading-spinner {
      width: 32px;
      height: 32px;
      border: 3px solid #F0EDE6;
      border-top: 3px solid #D2B48C;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    .error-state {
      text-align: center;
      padding: 48px 32px;
      color: #DC2626;
      background: white;
      border-radius: 16px;
      box-shadow: 0 4px 20px rgba(139, 69, 19, 0.08);
      border: 1px solid #F5F5DC;
    }

    .error-icon {
      width: 48px;
      height: 48px;
      margin: 0 auto 16px;
    }

    .error-state h3 {
      font-size: 20px;
      font-weight: 600;
      color: #DC2626;
      margin: 0 0 8px 0;
    }

    .logs-table-container {
      background: white;
      border-radius: 16px;
      box-shadow: 0 4px 20px rgba(139, 69, 19, 0.08);
      border: 1px solid #F5F5DC;
      overflow: hidden;
    }

    .logs-header {
      padding: 20px 24px;
      border-bottom: 1px solid #F0EDE6;
      background: linear-gradient(135deg, #FAF9F6 0%, #F5F5DC 100%);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }

    .logs-count {
      font-weight: 600;
      color: #2F2F2F;
      font-size: 14px;
    }

    .logs-info {
      display: flex;
      align-items: center;
      gap: 8px;
      color: #5C5C5C;
      font-size: 12px;
    }

    .info-icon {
      width: 16px;
      height: 16px;
    }

    .logs-table-wrapper {
      overflow-x: auto;
    }

    .logs-table {
      width: 100%;
      border-collapse: collapse;
      min-width: 800px;
    }

    .logs-table thead {
      background: #F9FAFB;
    }

    .logs-table th {
      padding: 16px 20px;
      text-align: left;
      font-weight: 600;
      color: #2F2F2F;
      border-bottom: 2px solid #F0EDE6;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      position: sticky;
      top: 0;
      background: #F9FAFB;
      z-index: 10;
      min-width: 150px;
    }

    .logs-table th div {
      display: flex;
      align-items: center;
      gap: 8px;
      white-space: nowrap;
    }

    .logs-table thead tr {
      display: table-row;
    }

    .header-icon {
      width: 16px;
      height: 16px;
      color: #6B7280;
      flex-shrink: 0;
    }

    .header-icon {
      width: 16px;
      height: 16px;
      color: #6B7280;
    }

    .logs-table td {
      padding: 16px 20px;
      border-bottom: 1px solid #F0EDE6;
      vertical-align: top;
    }

    .log-row {
      transition: background-color 0.2s ease;
    }

    .log-row:hover {
      background: #FAF9F6;
    }

    .log-row.danger {
      border-left: 4px solid #DC2626;
    }

    .log-row.success {
      border-left: 4px solid #10B981;
    }

    .log-row.warning {
      border-left: 4px solid #F59E0B;
    }

    .log-row.info {
      border-left: 4px solid #3B82F6;
    }

    .timestamp {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .date {
      font-weight: 600;
      color: #2F2F2F;
      font-size: 14px;
    }

    .time {
      color: #6B7280;
      font-size: 12px;
    }

    .action-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .action-badge.create {
      background: #D1FAE5;
      color: #065F46;
    }

    .action-badge.update {
      background: #DBEAFE;
      color: #1E40AF;
    }

    .action-badge.delete {
      background: #FEE2E2;
      color: #DC2626;
    }

    .action-badge.auth {
      background: #E0E7FF;
      color: #3730A3;
    }

    .action-badge.approve {
      background: #D1FAE5;
      color: #065F46;
    }

    .action-badge.reject {
      background: #FEF3C7;
      color: #D97706;
    }

    .action-badge.other {
      background: #F3F4F6;
      color: #374151;
    }

    .action-icon {
      width: 14px;
      height: 14px;
    }

    .actor-info {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .actor-avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: linear-gradient(135deg, #D2B48C 0%, #CD853F 100%);
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 12px;
    }

    .system-actor {
      color: #6B7280;
      font-style: italic;
      font-size: 14px;
    }

    .target-info {
      max-width: 300px;
    }

    .target-code {
      background: #F3F4F6;
      padding: 4px 8px;
      border-radius: 4px;
      font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
      font-size: 12px;
      color: #374151;
      word-break: break-all;
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
      .logs-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
      }

      .logs-table-wrapper {
        overflow-x: auto;
      }

      .logs-table {
        min-width: 600px;
      }

      .section-title {
        font-size: 24px;
      }

      .timestamp {
        flex-direction: row;
        gap: 8px;
        align-items: center;
      }

      .target-info {
        max-width: 200px;
      }
    }
    </style>
    
    <template>
      <div class="admin-logs-container">
        <div class="section-header">
          <h2 class="section-title">System Logs</h2>
          <p class="section-subtitle">Monitor platform activity and user actions</p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Loading system logs...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-state">
          <svg class="error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <h3>Failed to load logs</h3>
          <p>{{ error }}</p>
        </div>

        <!-- Logs Table -->
        <div v-else-if="logs.length > 0" class="logs-table-container">
          <div class="logs-header">
            <div class="logs-count">
              Showing {{ logs.length }} recent log entries
            </div>
            <div class="logs-info">
              <svg class="info-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              Logs are automatically cleaned up after 100 entries
            </div>
          </div>

          <div class="logs-table-wrapper">
            <table class="logs-table">
              <thead>
                <tr>
                  <th class="timestamp-col">
                    <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    Timestamp
                  </th>
                  <th class="action-col">
                    <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                    </svg>
                    Action
                  </th>
                  <th class="actor-col">
                    <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                    Actor
                  </th>
                  <th class="target-col">
                    <svg class="header-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    Target
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="log in logs" :key="log.id" class="log-row" :class="getLogTypeClass(log.action)">
                  <td class="timestamp-cell">
                    <div class="timestamp">
                      <div class="date">{{ formatDate(log.timestamp) }}</div>
                      <div class="time">{{ formatTime(log.timestamp) }}</div>
                    </div>
                  </td>
                  <td class="action-cell">
                    <div class="action-badge" :class="getActionClass(log.action)">
                      <svg class="action-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path :d="getActionIcon(log.action)"></path>
                      </svg>
                      {{ formatAction(log.action) }}
                    </div>
                  </td>
                  <td class="actor-cell">
                    <div class="actor-info">
                      <div class="actor-avatar" v-if="log.actor_id">
                        {{ log.actor_id }}
                      </div>
                      <span v-else class="system-actor">System</span>
                    </div>
                  </td>
                  <td class="target-cell">
                    <div class="target-info">
                      <code class="target-code">{{ log.target || 'N/A' }}</code>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
          </svg>
          <h3>No logs available</h3>
          <p>System activity will appear here as users interact with the platform.</p>
        </div>
      </div>
    </template>
    