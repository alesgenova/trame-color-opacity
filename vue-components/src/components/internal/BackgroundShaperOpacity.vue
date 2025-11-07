<script setup lang="ts">
import { OpacityNode } from '@/types';
import { defineProps, computed } from 'vue'

const props = defineProps<{
    nodes: OpacityNode[];
}>();

const shape = computed(() => {
    const empty = props.nodes.length == 0;
    let startY = 0;
    let endY = 0;

    if (!empty) {
        startY = props.nodes[0][1];
        endY = props.nodes[props.nodes.length - 1][1];
    }

    return [
        [0, 0],
        [0, startY],
        ...props.nodes,
        [1, endY],
        [1, 0],
    ];
});

</script>

<template>
    <slot
        :shape
    ></slot>
</template>

<style scoped>
</style>
