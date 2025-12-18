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
      <div v-for="post in posts" :key="post.id">
        <h3>{{ post.title }}</h3>
        <p>{{ post.content }}</p>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../api/axios";

const posts = ref([]);
const title = ref("");
const content = ref("");
const error = ref("");
const loading = ref(false);

const loadPosts = async () => {
  loading.value = true;
  error.value = "";

  try {
    const res = await api.get("/posts");
    posts.value = res.data;
  } catch (e) {
    error.value = "Failed to load posts";
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
    error.value = "Failed to create post";
  }
};

onMounted(loadPosts);
</script>
