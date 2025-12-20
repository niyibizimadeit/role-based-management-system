<template>
  <div>
    <h2>User Dashboard</h2>

    <h3>Create Post</h3>
    <input v-model="title" placeholder="Title" />
    <textarea v-model="content" placeholder="Content"></textarea>
    <button @click="createPost">Publish</button>

    <p v-if="error" style="color:red">{{ error }}</p>

    <hr />

    <h3>My Posts</h3>
    <div>
    <!-- Loading -->
    <div v-if="loading">Loading posts...</div>

    <!-- Empty -->
    <div v-else-if="posts.length === 0">
      No posts yet.
    </div>

    <!-- Posts -->
    <div v-else>
      <div v-for="post in posts" :key="post.id" style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">
        <div v-if="editingPost === post.id">
          <input v-model="editTitle" />
          <textarea v-model="editContent"></textarea>
          <button @click="saveEdit(post.id)">Save</button>
          <button @click="cancelEdit">Cancel</button>
        </div>

        <div v-else>
          <h3>{{ post.title }}</h3>
          <p>{{ post.content }}</p>
          <small>Status: {{ post.status }}</small><br />
          <button @click="startEdit(post)">Edit</button>
          <button @click="removePost(post.id)">Delete</button>
        </div>
      </div>
    </div>
  </div>
  <button @click="logout">Logout</button>
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
}

const saveEdit = async (postId) => {
  await api.put(`/posts/${postId}`, {
    title: editTitle.value,
    content: editContent.value
  })
  editingPost.value = null
  loadPosts()
}

const removePost = async (postId) => {
  if (!confirm("Delete this post?")) return

  await api.delete(`/posts/${postId}`)
  loadPosts()
}


onMounted(loadPosts);
</script>
