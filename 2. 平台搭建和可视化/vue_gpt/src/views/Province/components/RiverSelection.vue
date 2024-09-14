<template>
  <div>
    <h3>河流选择</h3>
    <select v-model="selectedRiver">
      <option value="river1">河流1</option>
      <option value="river2">河流2</option>
      <!-- 其他河流选项 -->
    </select>
    <p>选中的河流: {{ selectedRiver }}</p>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const selectedRiver = ref('river1')
</script>