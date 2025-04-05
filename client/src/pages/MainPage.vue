<template>
  <div>
    <h1>Users</h1>
    <Button
      label="Create User"
      @click="openCreateDialog"
      style="margin-bottom: 1rem"
    />
    <DataTable :value="users">
      <Column header="Username">
        <template #body="slotProps">
          <router-link :to="`/user/${slotProps.data._id}`">
            {{ slotProps.data.username }}
          </router-link>
        </template>
      </Column>
      <Column header="Active">
        <template #body="slotProps">
          {{ slotProps.data.active }}
        </template>
      </Column>
      <Column header="Roles">
        <template #body="slotProps">
          {{
            slotProps.data.roles && slotProps.data.roles.length
              ? slotProps.data.roles.join(", ")
              : "N/A"
          }}
        </template>
      </Column>
      <Column header="Created at">
        <template #body="slotProps">
          {{ formatTimestamp(slotProps.data.created_ts) }}
        </template>
      </Column>
      <Column header="Last updated at">
        <template #body="slotProps">
          {{ formatTimestamp(slotProps.data.last_updated_ts) }}
        </template>
      </Column>
      <Column header="Actions">
        <template #body="slotProps">
          <button
            class="p-button p-component"
            @click="openEditDialog(slotProps.data)"
          >
            Edit
          </button>
          <button
            class="p-button p-component p-button-danger"
            style="margin-left: 6px"
            @click="deleteUser(slotProps.data._id)"
          >
            Delete
          </button>
        </template>
      </Column>
    </DataTable>
    <UserDialog
      v-if="showDialog"
      :user="selectedUser"
      @close="closeDialog"
      @saved="onUserSaved"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Button from "primevue/button";

import UserDialog from "../components/UserDialog.vue";

const users = ref([]);
const showDialog = ref(false);
const selectedUser = ref(null);

function formatTimestamp(ts) {
  if (!ts) return "";
  const numericTs = parseFloat(ts);
  const finalTs = numericTs < 1000000000000 ? numericTs * 1000 : numericTs;
  return new Date(finalTs).toLocaleString();
}

async function fetchUsers() {
  try {
    const res = await axios.get("http://localhost:5000/api/users");
    console.log("Retorno do back-end:", res.data);
    users.value = res.data;
  } catch (err) {
    console.error(err);
  }
}

function openCreateDialog() {
  selectedUser.value = null;
  showDialog.value = true;
}

function openEditDialog(user) {
  selectedUser.value = { ...user };
  showDialog.value = true;
}

async function deleteUser(id) {
  if (confirm("Are you sure you want to delete this user?")) {
    await axios.delete(`http://localhost:5000/api/users/${id}`);
    fetchUsers();
  }
}

function closeDialog() {
  showDialog.value = false;
}

function onUserSaved() {
  closeDialog();
  fetchUsers();
}

onMounted(() => {
  fetchUsers();
});
</script>
