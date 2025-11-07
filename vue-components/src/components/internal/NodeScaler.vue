<script setup lang="ts">
import { defineProps, computed } from 'vue'

import { isColorNodes, type ColorNode, type ColorOpacityNode, type OpacityNode, type Vector2D, type Vector4D } from '@/types'


type SlotPropsNames = {
  scaledNodes: string;
};

const props = defineProps<{
    xRange: Vector2D | undefined;
    yRange: Vector2D | undefined;
    xLog: boolean;
    yLog: boolean;
    slotPropsNames: SlotPropsNames;
}>();

const nodes = defineModel<OpacityNode[] | ColorNode[]>("nodes", {
  required: true,
});

const scaledNodes = computed(() => {
    const scaleX = props.xRange != undefined;
    const scaleY = props.yRange != undefined;

    let scaledNodes = [...nodes.value] as OpacityNode[] | ColorNode[];

    if (nodes.value.length == 0 || (!scaleX && !scaleY)) {
        return scaledNodes;
    }

    if (isColorNodes(scaledNodes)) {
        if (scaleX) {
            let xSpan = Math.abs(props.xRange[1] - props.xRange[0]);
            scaledNodes = scaledNodes.map((el) => [(el[0] - props.xRange[0]) / xSpan, el[1]]);
        }
    } else {
        if (scaleX) {
            let xSpan = Math.abs(props.xRange[1] - props.xRange[0]);
            scaledNodes = scaledNodes.map((el) => [(el[0] - props.xRange[0]) / xSpan, el[1]]);
        }

        if (scaleY) {
            let ySpan = Math.abs(props.yRange[1] - props.yRange[0]);
            scaledNodes = scaledNodes.map((el) => [el[0], (el[1] - props.yRange[0]) / ySpan]);
        }
    }

    return scaledNodes;
});

function onScaledNodesUpdate(newScaledNodes: OpacityNode[] | ColorNode[]) {
    const scaleX = props.xRange != undefined;
    const scaleY = props.yRange != undefined;

    let newNodes = [...newScaledNodes] as OpacityNode[] | ColorNode[];

    if (newNodes.length == 0 || (!scaleX && !scaleY)) {
        nodes.value = newNodes;
        return;
    }

    if (isColorNodes(newNodes)) {
        if (scaleX) {
            let xSpan = Math.abs(props.xRange[1] - props.xRange[0]);
            newNodes = newNodes.map((el) => [props.xRange[0] + el[0] * xSpan, el[1]]);
        }
    } else {
        if (scaleX) {
            let xSpan = Math.abs(props.xRange[1] - props.xRange[0]);
            newNodes = newNodes.map((el) => [props.xRange[0] + el[0] * xSpan, el[1]]);
        }

        if (scaleY) {
            let ySpan = Math.abs(props.yRange[1] - props.yRange[0]);
            newNodes = newNodes.map((el) => [el[0], props.yRange[0] + el[1] * ySpan]);
        }
    }

    nodes.value = newNodes;
}

</script>

<template>
    <slot
        :[slotPropsNames.scaledNodes]="scaledNodes"
        :[`${slotPropsNames.scaledNodes}Updated`]="onScaledNodesUpdate"
    ></slot>
</template>

<style scoped>
</style>
