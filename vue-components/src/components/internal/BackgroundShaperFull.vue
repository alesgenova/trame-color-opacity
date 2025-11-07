<script setup lang="ts">
import { Vector2D } from '@/types';
import { defineProps, computed, ref } from 'vue'

// const props = defineProps<{
// }>();

// const shape = computed(() => [
//     [0, 0],
//     [1, 0],
//     [1, 1],
//     [0, 1],
// ]);

// const shape = ref<Vector2D[]>([
//     [0, 0],
//     [1, 0],
//     [1, 1],
//     [0, 1],
// ]);

</script>

<template>
    <slot
        :shape="[
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1],
        ]"
    ></slot>
</template>

<style scoped>
</style>
