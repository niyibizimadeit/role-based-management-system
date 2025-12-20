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
    error.value = "Failed to create post";
  }
};

onMounted(loadPosts);
</script>
