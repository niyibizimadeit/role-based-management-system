<script setup>
    import { ref, onMounted } from "vue"
    import api from "../api/axios"
    import { useRouter } from "vue-router"

    const posts = ref([])
    const editingId = ref(null)
    const editTitle = ref("")
    const editContent = ref("")
    const router = useRouter()


    const loadPosts = async () => {
      const res = await api.get("/admin/posts")
      posts.value = res.data
    }

    const approve = async (id) => {
      await api.put(`/admin/posts/${id}/approve`)
      loadPosts()
    }

    const reject = async (id) => {
      await api.put(`/admin/posts/${id}/reject`)
      loadPosts()
    }

    const startEdit = (post) => {
    editingId.value = post.id
    editTitle.value = post.title
    editContent.value = post.content
    }

    const saveEdit = async (id) => {
    await api.put(`/admin/posts/${id}`, {
    title: editTitle.value,
    content: editContent.value,
    })
    editingId.value = null
    loadPosts()
    }

    const deletePost = async (id) => {
    if (!confirm("Delete this post?")) return
    await api.delete(`/admin/posts/${id}`)
    loadPosts()
    }

    const logout = () => {
    localStorage.removeItem("token")
    localStorage.removeItem("role")
    router.push("/login")
    }

    onMounted(loadPosts)
    </script>

    <template>
      <div class="admin-posts-container">
        <div class="section-header">
          <h2 class="section-title">Post Moderation</h2>
          <p class="section-subtitle">Review and manage user-generated content</p>
        </div>

        <!-- Loading State -->
        <div v-if="false" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Loading posts...</p>
        </div>

        <!-- Posts List -->
        <div v-if="posts.length > 0" class="posts-list">
          <div
            v-for="post in posts"
            :key="post.id"
            class="post-card"
            :class="{ 'editing': editingId === post.id }"
          >
            <!-- Edit Mode -->
            <div v-if="editingId === post.id" class="edit-form">
              <div class="form-group">
                <label class="form-label">Title</label>
                <input
                  v-model="editTitle"
                  type="text"
                  class="form-input"
                  maxlength="200"
                />
              </div>

              <div class="form-group">
                <label class="form-label">Content</label>
                <textarea
                  v-model="editContent"
                  class="form-input content-textarea"
                  maxlength="10000"
                  rows="4"
                ></textarea>
              </div>

              <div class="edit-actions">
                <button @click="saveEdit(post.id)" class="save-btn">
                  <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  Save Changes
                </button>
                <button @click="editingId = null" class="cancel-btn">
                  Cancel
                </button>
              </div>
            </div>

            <!-- View Mode -->
            <div v-else class="post-content">
              <div class="post-header">
                <h3 class="post-title">{{ post.title }}</h3>
                <div class="post-status" :class="post.status.toLowerCase()">
                  {{ post.status }}
                </div>
              </div>

              <div class="post-body">
                <p class="post-text">{{ post.content }}</p>
              </div>

              <div class="post-footer">
                <div class="post-meta">
                  <span class="post-author">Author ID: {{ post.author_id }}</span>
                  <span class="post-date" v-if="post.created_at">
                    {{ new Date(post.created_at).toLocaleDateString() }}
                  </span>
                </div>
                <div class="post-actions">
                  <button @click="approve(post.id)" class="approve-btn" :disabled="post.status === 'approved'">
                    <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                    Approve
                  </button>
                  <button @click="reject(post.id)" class="reject-btn" :disabled="post.status === 'rejected'">
                    <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                    Reject
                  </button>
                  <button @click="startEdit(post)" class="edit-btn">
                    <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                    Edit
                  </button>
                  <button @click="deletePost(post.id)" class="delete-btn">
                    <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <h3>No posts to moderate</h3>
          <p>All posts have been reviewed or there are no user submissions yet.</p>
        </div>
      </div>
    </template>

    <style scoped>
    .admin-posts-container {
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

    .posts-list {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .post-card {
      background: white;
      border-radius: 16px;
      box-shadow: 0 4px 20px rgba(139, 69, 19, 0.08);
      border: 1px solid #F5F5DC;
      overflow: hidden;
      transition: all 0.3s ease;
    }

    .post-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 30px rgba(139, 69, 19, 0.12);
    }

    .post-card.editing {
      border-color: #D2B48C;
      box-shadow: 0 4px 20px rgba(210, 180, 140, 0.2);
    }

    .post-content {
      padding: 24px;
    }

    .post-header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 16px;
      gap: 16px;
    }

    .post-title {
      font-size: 20px;
      font-weight: 700;
      color: #2F2F2F;
      margin: 0;
      line-height: 1.3;
      flex: 1;
    }

    .post-status {
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      flex-shrink: 0;
    }

    .post-status.draft {
      background: #FEF3C7;
      color: #D97706;
    }

    .post-status.pending {
      background: #DBEAFE;
      color: #2563EB;
    }

    .post-status.approved {
      background: #D1FAE5;
      color: #065F46;
    }

    .post-status.rejected {
      background: #FEE2E2;
      color: #DC2626;
    }

    .post-body {
      margin-bottom: 20px;
    }

    .post-text {
      color: #374151;
      line-height: 1.6;
      font-size: 16px;
      margin: 0;
    }

    .post-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 16px;
      border-top: 1px solid #F0EDE6;
      flex-wrap: wrap;
      gap: 16px;
    }

    .post-meta {
      display: flex;
      flex-direction: column;
      gap: 4px;
      color: #6B7280;
      font-size: 14px;
    }

    .post-author {
      font-weight: 500;
    }

    .post-date {
      font-size: 12px;
    }

    .post-actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .approve-btn, .reject-btn, .edit-btn, .delete-btn {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 8px 16px;
      border: none;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .approve-btn {
      background: #10B981;
      color: white;
    }

    .approve-btn:hover:not(:disabled) {
      background: #059669;
      transform: translateY(-1px);
    }

    .reject-btn {
      background: #F59E0B;
      color: white;
    }

    .reject-btn:hover:not(:disabled) {
      background: #D97706;
      transform: translateY(-1px);
    }

    .edit-btn {
      background: #D2B48C;
      color: white;
    }

    .edit-btn:hover {
      background: #CD853F;
      transform: translateY(-1px);
    }

    .delete-btn {
      background: #DC2626;
      color: white;
    }

    .delete-btn:hover {
      background: #B91C1C;
      transform: translateY(-1px);
    }

    .approve-btn:disabled, .reject-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }

    .btn-icon {
      width: 16px;
      height: 16px;
    }

    .edit-form {
      padding: 24px;
      background: #FAF9F6;
      border-left: 4px solid #D2B48C;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-bottom: 16px;
    }

    .form-label {
      font-size: 14px;
      font-weight: 600;
      color: #2F2F2F;
    }

    .form-input {
      padding: 12px;
      border: 2px solid #F0EDE6;
      border-radius: 8px;
      font-size: 14px;
      transition: all 0.3s ease;
      background: white;
      color: #2F2F2F;
    }

    .form-input:focus {
      outline: none;
      border-color: #D2B48C;
      box-shadow: 0 0 0 3px rgba(210, 180, 140, 0.1);
    }

    .content-textarea {
      resize: vertical;
      min-height: 100px;
    }

    .edit-actions {
      display: flex;
      gap: 12px;
      margin-top: 16px;
    }

    .save-btn {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 10px 20px;
      background: #10B981;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .save-btn:hover {
      background: #059669;
      transform: translateY(-1px);
    }

    .cancel-btn {
      padding: 10px 20px;
      background: #6B7280;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .cancel-btn:hover {
      background: #4B5563;
      transform: translateY(-1px);
    }

    .empty-state {
      text-align: center;
      padding: 64px 32px;
      color: #5C5C5C;
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
      .post-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
      }

      .post-footer {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
      }

      .post-actions {
        width: 100%;
        justify-content: flex-end;
      }

      .edit-actions {
        flex-direction: column;
      }

      .section-title {
        font-size: 24px;
      }
    }
    </style>