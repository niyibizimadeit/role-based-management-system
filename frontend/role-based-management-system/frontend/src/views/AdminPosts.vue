<script setup>
    import { ref, onMounted } from "vue"
    import api from "../api/axios"
    
    const posts = ref([])
    
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
    
    onMounted(loadPosts)
    </script>
    
    <template>
      <div>
        <h3>All Posts</h3>
        <div v-for="p in posts" :key="p.id">
          <b>{{ p.title }}</b> — {{ p.status }}
          <button @click="approve(p.id)">Approve</button>
          <button @click="reject(p.id)">Reject</button>
        </div>
      </div>
    </template>
    