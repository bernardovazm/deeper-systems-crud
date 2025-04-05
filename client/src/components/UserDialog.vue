<template>
  <Dialog
    header="User Form"
    v-model:visible="dialogVisible"
    :modal="true"
    @hide="close"
  >
    <div class="p-fluid">
      <div class="p-field">
        <label for="username">Username</label>
        <InputText id="username" v-model="localUser.username" />
      </div>
      <div class="p-field">
        <label for="password">Password</label>
        <Password id="password" v-model="localUser.password" toggleMask />
      </div>
      <div class="p-field">
        <label for="timezone">Timezone</label>
        <InputText id="timezone" v-model="localUser.preferences.timezone" />
      </div>
      <div class="p-field">
        <label for="active">Active</label>
        <ToggleSwitch v-model="localUser.active" style="margin-left: 10px" />
      </div>
      <!-- Roles (simples) -->
      <div class="p-field">
        <label for="roles">Roles (separated with commas)</label>
        <InputText id="roles" v-model="rolesStr" />
      </div>
    </div>
    <template #footer>
      <Button label="Cancel" @click="close" class="p-button-text" />
      <Button label="Save" @click="saveUser" />
    </template>
  </Dialog>
</template>

<script>
import { ref, onMounted } from "vue";
import Dialog from "primevue/dialog";
import InputText from "primevue/inputtext";
import ToggleSwitch from "primevue/toggleswitch";
import Password from "primevue/password";
import Button from "primevue/button";
import axios from "axios";

export default {
  name: "UserDialog",
  components: { Dialog, InputText, ToggleSwitch, Password, Button },
  props: {
    user: {
      type: Object,
      default: null,
    },
  },
  setup(props, { emit }) {
    const dialogVisible = ref(true);
    const localUser = ref({
      username: "",
      password: "",
      active: true,
      preferences: {
        timezone: "",
      },
      roles: [],
    });
    const rolesStr = ref("");

    onMounted(() => {
      if (props.user) {
        localUser.value = JSON.parse(JSON.stringify(props.user));
        rolesStr.value = localUser.value.roles?.join(", ") || "";
      }
    });

    const close = () => {
      dialogVisible.value = false;
      emit("close");
    };

    const saveUser = async () => {
      localUser.value.roles = rolesStr.value
        .split(",")
        .map((r) => r.trim())
        .filter((r) => r);

      if (!localUser.value._id) {
        await axios.post("http://localhost:5000/api/users", localUser.value);
      } else {
        const localCopy = JSON.parse(JSON.stringify(localUser.value));
        delete localCopy._id;
        await axios.put(
          `http://localhost:5000/api/users/${localUser.value._id}`,
          localCopy
        );
      }
      emit("saved");
    };

    return {
      dialogVisible,
      localUser,
      rolesStr,
      close,
      saveUser,
    };
  },
};
</script>

<style scoped>
.p-field {
  margin-bottom: 1rem; /* Espaço entre os campos */
  width: 100%; /* Garante que cada campo ocupe a largura inteira */
}

input,
.p-password,
.p-inputtext,
.p-password > *:not(svg) {
  width: 100%; /* Faz com que os campos de input ocupem 100% da largura */
}
</style>
