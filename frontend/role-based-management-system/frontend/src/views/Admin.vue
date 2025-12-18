<template>
  <div>
    <h2>Admin Panel</h2>

    <div v-for="post in posts" :key="post.id" style="margin-bottom: 12px;">
      <h3>{{ post.title }}</h3>
      <p>{{ post.content }}</p>
      <p>Status: {{ post.status }}</p>

      <button v-if="post.status === 'PENDING'" @click="approve(post.id)">
        Approve
      </button>
      <button v-if="post.status === 'PENDING'" @click="reject(post.id)">
        Reject
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../api/axios";

const posts = ref([]);

const fetchPosts = async () => {
  const res = await api.get("/admin/posts");
  posts.value = res.data;
};

const approve = async (id) => {
  await api.put(`/admin/posts/${id}/approve`);
  fetchPosts();
};

const reject = async (id) => {
  await api.put(`/admin/posts/${id}/reject`);
  fetchPosts();
};

onMounted(fetchPosts);
</script>
