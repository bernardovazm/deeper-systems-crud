<template>
  <div v-if="user" class="user-profile-container">
    <h2>{{ user.username }}'s Profile</h2>
    <p><strong>Roles:</strong> {{ formattedRoles }}</p>
    <p><strong>Active:</strong> {{ formattedActive }}</p>
    <p><strong>Created at:</strong> {{ formattedCreated }}</p>
    <p><strong>Last updated at:</strong> {{ formattedUpdated }}</p>
    <Button label="Edit" @click="openEditDialog" />
    <Button label="Delete" class="p-button-danger" @click="onDelete" />
    <Button
      label="Back"
      severity="secondary"
      variant="outlined"
      @click="goBack"
    />
    <UserDialog
      v-if="showDialog"
      :user="selectedUser"
      @close="closeDialog"
      @saved="onUserSaved"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import Button from "primevue/button";
import UserDialog from "../components/UserDialog.vue";

function formatTimestamp(ts) {
  if (!ts) return "";
  const numericTs = parseFloat(ts);
  const finalTs = numericTs < 1000000000000 ? numericTs * 1000 : numericTs;
  return new Date(finalTs).toLocaleString();
}

function formatRoles(roles) {
  if (!roles || roles.length === 0) return "N/A";
  return roles.join(", ");
}

const route = useRoute();
const router = useRouter();

const user = ref(null);
const showDialog = ref(false);
const selectedUser = ref(null);

async function fetchUser() {
  const userId = route.params.id;
  try {
    const res = await axios.get(`http://localhost:5000/api/users/${userId}`);
    user.value = res.data;
  } catch (error) {
    alert(error.response.data.error || "User not found");
    router.push("/");
  }
}

const formattedRoles = computed(() => formatRoles(user.value?.roles));
const formattedActive = computed(() => user.value?.active);
const formattedCreated = computed(() =>
  formatTimestamp(user.value?.created_ts)
);
const formattedUpdated = computed(() =>
  !!user.value?.last_updated_ts
    ? formatTimestamp(user.value?.last_updated_ts)
    : "User was not updated"
);

function openEditDialog() {
  selectedUser.value = { ...user.value };
  showDialog.value = true;
}

function closeDialog() {
  showDialog.value = false;
}

function onUserSaved() {
  closeDialog();
  fetchUser();
}

function goBack() {
  router.back();
}

async function onDelete() {
  if (confirm(`Are you sure you want to delete ${user.value.username}?`)) {
    await axios.delete(`http://localhost:5000/api/users/${user.value._id}`);
    router.push("/");
  }
}

onMounted(() => {
  fetchUser();
});
</script>

<style scoped>
.user-profile-container {
  display: grid;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1vh;
}
</style>
