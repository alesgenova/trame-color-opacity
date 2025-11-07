<script setup lang="ts">
import { defineProps, useTemplateRef, onMounted, computed, watch } from 'vue'
import type { ColorNode, ColorOpacityNode } from '@/types'
import type { Point } from '@/types'
import type { Vector2D } from '@/types'
import { drawCanvasBackground } from '@/utils/canvas';

const props = defineProps<{
    nodes: ColorOpacityNode[] | ColorNode[];
    shape: Point[];
    size: Vector2D;
    padding: Vector2D;
}>();

const canvas = useTemplateRef<HTMLCanvasElement>("background-canvas");

const contentSize = computed<Vector2D>(() => [
    Math.max(props.size[0] - 2 * props.padding[0], 0),
    Math.max(props.size[1] - 2 * props.padding[1], 0)
]);

watch(() => [canvas, props.size, props.padding, props.shape, props.nodes], () => {
    if (!canvas.value) {
        return;
    }

    const context = canvas.value.getContext('2d');

    if (!context) {
        return;
    }

    canvas.value.width = props.size[0];
    canvas.value.height = props.size[1];

    drawCanvasBackground(context, props.size, props.padding, contentSize.value, props.shape, props.nodes);
});

onMounted(() => {
    if (!canvas.value) {
        return;
    }

    const context = canvas.value.getContext('2d');

    if (!context) {
        return;
    }

    canvas.value.width = props.size[0];
    canvas.value.height = props.size[1];

    drawCanvasBackground(context, props.size, props.padding, contentSize.value, props.shape, props.nodes);
})
</script>

<template>
  <canvas class="trame-colormap-background" ref="background-canvas"></canvas>
</template>

<style scoped>
.trame-colormap-background {
  width: 100%;
  height: 100%;
}
</style>
