<template>
  <div>
    <h3>数据更新</h3>
    <button @click="updateData">更新数据</button>
    <p v-if="updating">更新中...</p>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'

const updating = ref(false)

function updateData() {
  updating.value = true
  // 这里添加实际的数据更新逻辑
  setTimeout(() => {
    updating.value = false
  }, 2000)
}
</script>