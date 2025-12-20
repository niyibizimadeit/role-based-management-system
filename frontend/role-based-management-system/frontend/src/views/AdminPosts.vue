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
      <div>
        <h3>All Posts</h3>
        <div v-for="p in posts" :key="p.id">
          <div v-if="editingId === p.id">
          <input v-model="editTitle" />
          <textarea v-model="editContent"></textarea>
          <button @click="saveEdit(p.id)">Save</button>
          <button @click="editingId = null">Cancel</button>
          </div>

          <div v-else>
          <b>{{ p.title }}</b> — {{ p.status }}
          <button @click="approve(p.id)">Approve</button>
          <button @click="reject(p.id)">Reject</button>
          <button @click="startEdit(p)">Edit</button>
          <button @click="deletePost(p.id)">Delete</button>
        </div>
        </div>
        <br>
        <button @click="logout">Logout</button>
      </div>
    </template>
    