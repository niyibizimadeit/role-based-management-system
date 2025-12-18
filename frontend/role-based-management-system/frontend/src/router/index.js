import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Dashboard from "../views/Dashboard.vue";
import Admin from "../views/Admin.vue";

const routes = [
  {
    path: "/login",
    component: Login,
    meta: { public: true },
  },
  {
    path: "/dashboard",
    component: Dashboard,
    meta: { requiresAuth: true, role: "USER" },
  },
  {
    path: "/admin",
    component: Admin,
    meta: { requiresAuth: true, role: "ADMIN" },
  },
  {
    path: "/",
    redirect: "/login",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  // Public routes
  if (to.meta.public) {
    return next();
  }

  // Auth required but no token
  if (to.meta.requiresAuth && !token) {
    return next("/login");
  }

  // Role check
  if (to.meta.role && to.meta.role !== role) {
    return next("/dashboard");
  }

  next();
});

export default router;
