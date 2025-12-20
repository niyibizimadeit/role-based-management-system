<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="header-content">
        <h1 class="dashboard-title">My Dashboard</h1>
        <button @click="logout" class="logout-btn">
          <svg class="logout-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
          </svg>
          Logout
        </button>
      </div>
    </header>

    <main class="dashboard-main">
      <!-- Create Post Section -->
      <section class="create-post-section">
        <div class="section-card">
          <div class="section-header">
            <h2 class="section-title">Create New Post</h2>
            <p class="section-subtitle">Share your thoughts with the community</p>
          </div>

          <form class="create-post-form" @submit.prevent="createPost">
            <div class="form-group">
              <label for="title" class="form-label">Post Title</label>
              <input
                id="title"
                v-model="title"
                type="text"
                placeholder="Enter an engaging title..."
                class="form-input title-input"
                required
                maxlength="200"
              />
            </div>

            <div class="form-group">
              <label for="content" class="form-label">Content</label>
              <textarea
                id="content"
                v-model="content"
                placeholder="Write your post content here..."
                class="form-input content-textarea"
                required
                maxlength="10000"
                rows="6"
              ></textarea>
            </div>

            <button type="submit" class="create-btn" :disabled="!title || !content || loading">
              <svg v-if="!loading" class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
              </svg>
              <div v-if="loading" class="btn-loader"></div>
              <span>{{ loading ? 'Publishing...' : 'Publish Post' }}</span>
            </button>
          </form>

          <div v-if="createError" class="error-message">
            <svg class="error-icon" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
            </svg>
            {{ createError }}
          </div>
        </div>
      </section>

      <!-- My Posts Section -->
      <section class="posts-section">
        <div class="section-header">
          <h2 class="section-title">My Posts</h2>
          <p class="section-subtitle">Manage your published content</p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Loading your posts...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="posts.length === 0" class="empty-state">
          <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <h3>No posts yet</h3>
          <p>Create your first post to get started!</p>
        </div>

        <!-- Posts List -->
        <div v-else class="posts-list">
          <div
            v-for="post in posts"
            :key="post.id"
            class="post-card"
            :class="{ 'editing': editingPost === post.id }"
          >
            <!-- Edit Mode -->
            <div v-if="editingPost === post.id" class="edit-form">
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
                <button @click="saveEdit(post.id)" class="save-btn" :disabled="loading">
                  <svg v-if="!loading" class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                  <div v-if="loading" class="btn-loader"></div>
                  <span>Save</span>
                </button>
                <button @click="cancelEdit" class="cancel-btn" :disabled="loading">
                  Cancel
                </button>
              </div>

              <div v-if="editError" class="error-message">
                <svg class="error-icon" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                </svg>
                {{ editError }}
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
                <div class="post-date" v-if="post.created_at">
                  {{ new Date(post.created_at).toLocaleDateString() }}
                </div>
                <div class="post-actions">
                  <button @click="startEdit(post)" class="edit-btn">
                    <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                    Edit
                  </button>
                  <button @click="removePost(post.id)" class="delete-btn">
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
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../api/axios";

const posts = ref([]);
const title = ref("");
const content = ref("");
const loadError = ref("");
const createError = ref("");
const loading = ref(false);
const editingPost = ref(null)
const editTitle = ref("")
const editContent = ref("")
const editError = ref("")

const router = useRouter();

const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  router.push("/login");
};

const loadPosts = async () => {
  loading.value = true;
  loadError.value = "";

  try {
    const res = await api.get("/posts");
    posts.value = res.data;
  } catch (e) {
    loadError.value = "Failed to load posts";
  } finally {
    loading.value = false;
  }
};


const createPost = async () => {
  try {
    await api.post("/posts", {
      title: title.value,
      content: content.value,
    });
    title.value = "";
    content.value = "";
    loadPosts();
  } catch {
    createError.value = "Failed to create post";
  }
};

const startEdit = (post) => {
  editingPost.value = post.id
  editTitle.value = post.title
  editContent.value = post.content
}

const cancelEdit = () => {
  editingPost.value = null
  editError.value = ""
}

const saveEdit = async (postId) => {
  try {
    await api.put(`/posts/${postId}`, {
      title: editTitle.value,
      content: editContent.value
    })
    editingPost.value = null
    editError.value = ""
    loadPosts()
  } catch (e) {
    editError.value = e.response?.data?.error || "Failed to update post"
  }
}

const removePost = async (postId) => {
  if (!confirm("Delete this post?")) return

  try {
    await api.delete(`/posts/${postId}`)
    loadPosts()
  } catch (e) {
    // Could add error handling here
  }
}


onMounted(loadPosts);
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #F5F5DC 0%, #FAF0E6 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.dashboard-header {
  background: white;
  border-bottom: 1px solid #F0EDE6;
  box-shadow: 0 2px 10px rgba(139, 69, 19, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.dashboard-title {
  font-size: 28px;
  font-weight: 700;
  color: #2F2F2F;
  margin: 0;
  font-family: 'Georgia', serif;
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

.dashboard-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.section-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(139, 69, 19, 0.08);
  border: 1px solid #F5F5DC;
  overflow: hidden;
}

.section-header {
  padding: 24px 32px;
  border-bottom: 1px solid #F0EDE6;
  background: linear-gradient(135deg, #FAF9F6 0%, #F5F5DC 100%);
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: #2F2F2F;
  margin: 0 0 4px 0;
  font-family: 'Georgia', serif;
}

.section-subtitle {
  color: #5C5C5C;
  font-size: 16px;
  margin: 0;
  font-weight: 400;
}

.create-post-form {
  padding: 32px;
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
  font-family: inherit;
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

.title-input {
  font-weight: 600;
}

.content-textarea {
  resize: vertical;
  min-height: 120px;
  line-height: 1.6;
}

.create-btn {
  align-self: flex-start;
  padding: 16px 32px;
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

.create-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(139, 69, 19, 0.3);
}

.create-btn:disabled {
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

.posts-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
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
}

.post-date {
  color: #6B7280;
  font-size: 14px;
  font-weight: 500;
}

.post-actions {
  display: flex;
  gap: 8px;
}

.edit-btn, .delete-btn {
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

.edit-form {
  padding: 24px;
  background: #FAF9F6;
  border-left: 4px solid #D2B48C;
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

.save-btn:hover:not(:disabled) {
  background: #059669;
  transform: translateY(-1px);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
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

.cancel-btn:hover:not(:disabled) {
  background: #4B5563;
  transform: translateY(-1px);
}

.cancel-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
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

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }

  .dashboard-title {
    text-align: center;
    font-size: 24px;
  }

  .dashboard-main {
    padding: 16px;
  }

  .section-header {
    padding: 20px 24px;
  }

  .section-title {
    font-size: 20px;
  }

  .create-post-form {
    padding: 24px;
  }

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
}
</style>
