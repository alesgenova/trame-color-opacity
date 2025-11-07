<script setup lang="ts">
import { defineProps, computed } from 'vue'
import { linearScale, createColorMap } from '@colormap/core';

import type { ColorNode, OpacityNode } from '@/types'
import { MapNodeAdapter } from '@/utils/nodes';

type SlotPropsNames = {
  flattenedNodes: string;
};


const props = defineProps<{
    nodes: ColorNode[];
    slotPropsNames: SlotPropsNames;
}>();

const nodes = defineModel<ColorNode[]>("nodes", {
  required: true,
});

const flattenedNodes = computed(() => props.nodes.map((el) => [el[0], 0.5]));

function flattenedNodesUpdated(newFlattenedNodes: OpacityNode[]) {
    // console.log("NODES UPDATEDDD", newFlattenedNodes);
    const currentNodes = [...props.nodes];

    if (currentNodes.length == newFlattenedNodes.length) {
        const newNodes = newFlattenedNodes.map((el, i) => {
            return [el[0], currentNodes[i][1]] as ColorNode;
        });

        nodes.value = newNodes;
    } else {
        const adaptedColorNodes = currentNodes.map((el) => new MapNodeAdapter(el));
        const scale = linearScale([0, 1], [0, 1]);
        const colormapFn = createColorMap(adaptedColorNodes, scale);

        const epsilon = 0.0001;

        let currNodeId = 0;

        const newNodes: ColorNode[] = [];

        for (let i = 0; i < newFlattenedNodes.length; i ++) {
            if (Math.abs(currentNodes[currNodeId][0] - newFlattenedNodes[i][0]) < epsilon) {
                newNodes.push([newFlattenedNodes[i][0], currentNodes[currNodeId][1]]);
                currNodeId++;
            } else {
                newNodes.push([newFlattenedNodes[i][0], colormapFn(newFlattenedNodes[i][0])]);
            }
        }

        nodes.value = newNodes;
    }
}

</script>

<template>
    <slot
        :[slotPropsNames.flattenedNodes]="flattenedNodes"
        :[`${slotPropsNames.flattenedNodes}Updated`]="flattenedNodesUpdated"
    ></slot>
</template>

<style scoped>
</style>
