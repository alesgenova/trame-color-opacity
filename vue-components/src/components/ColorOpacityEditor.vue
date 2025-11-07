<script setup lang="ts">
import {
  defineModel,
  withDefaults,
} from "vue";

import type { ColorNode, OpacityNode, RGBAColor, Vector2D } from '@/types'
import NodeScaler from "@/components/internal/NodeScaler.vue";
import ViewportContainer from "@/components/internal/ViewportContainer.vue";
import BackgroundShaper from "./internal/BackgroundShaper.vue";
import BackgroundView from "./internal/BackgroundView.vue";
import ControlsView from "./internal/ControlsView.vue";
import NodeMerger from "./internal/NodeMerger.vue";
import BackgroundShaperFull from "./internal/BackgroundShaperFull.vue";
import NodeFlattener from "./internal/NodeFlattener.vue";
import BackgroundShaperHistograms from "./internal/BackgroundShaperHistograms.vue";

interface Props {
  scalarRange: Vector2D;
  histogramsRange: Vector2D;
  backgroundShape: "full" | "opacity" | "histograms";
  backgroundOpacity: boolean;
  histograms: Vector2D[];
  showHistograms: boolean;
  style: string;
  viewportPadding: Vector2D;
  histogramsColor: RGBAColor;
  handleColor: RGBAColor;
  handleBorderColor: RGBAColor;
  handleRadius: number;
  lineWidth: number;
}

type Events = {};

const props = withDefaults(defineProps<Props>(), {
  backgroundShape: "opacity",
  showHistograms: false,
  histogramsColor: () => [0, 0, 0, 0.25],
  viewportPadding: () => [8, 8],
  handleColor: () => [0.125, 0.125, 0.125, 1],
  handleBorderColor: () => [0.75, 0.75, 0.75, 1],
  handleRadius: 7,
  lineWidth: 2,
});

defineEmits<Events>();

const colorNodes = defineModel<ColorNode[]>("colorNodes", {
  required: true,
});

const opacityNodes = defineModel<OpacityNode[]>("opacityNodes", {
  required: true,
});

</script>

<template>
  <div class="color-opacity-editor-root-container" :style="style">
    <NodeScaler v-model:nodes="histograms" :xRange="scalarRange" :yRange="histogramsRange" :slotPropsNames="{scaledNodes: 'scaledHistograms'}" v-slot="{ scaledHistograms, scaledHistogramsUpdated }">
      <NodeScaler v-model:nodes="colorNodes" :xRange="scalarRange" :slotPropsNames="{scaledNodes: 'scaledColorNodes'}" v-slot="{ scaledColorNodes, scaledColorNodesUpdated }">
        <NodeScaler v-model:nodes="opacityNodes" :xRange="scalarRange" :slotPropsNames="{scaledNodes: 'scaledOpacityNodes'}" v-slot="{ scaledOpacityNodes, scaledOpacityNodesUpdated }">
          <ViewportContainer v-slot="{ viewportSize }" class="color-opacity-editor-opacity-container">
            <BackgroundShaper :backgroundShape :opacityNodes="scaledOpacityNodes" :histograms="scaledHistograms" v-slot="{ shape }">
              <NodeMerger v-if="backgroundOpacity" :colorNodes="scaledColorNodes" :opacityNodes="scaledOpacityNodes" v-slot="{ colorOpacityNodes }">
                <BackgroundView :shape :size="viewportSize" :padding="viewportPadding" :nodes="colorOpacityNodes"></BackgroundView>
              </NodeMerger>
              <BackgroundView v-else :shape :size="viewportSize" :padding="viewportPadding" :nodes="scaledColorNodes"></BackgroundView>
            </BackgroundShaper>

            <BackgroundShaperHistograms v-if="showHistograms" :nodes="scaledHistograms" v-slot="{ shape }">
              <BackgroundView :shape :size="viewportSize" :padding="viewportPadding" :nodes="[[0, histogramsColor]]" class="color-opacity-editor-canvas"></BackgroundView>
            </BackgroundShaperHistograms>

            <ControlsView
              :size="viewportSize" :padding="viewportPadding" showLine
              :radius="handleRadius" :lineWidth="lineWidth" :color="handleColor" :borderColor="handleBorderColor"
              :nodes="scaledOpacityNodes" @update:nodes="scaledOpacityNodesUpdated"
            ></ControlsView>
          </ViewportContainer>

          <ViewportContainer v-slot="{ viewportSize }" class="color-opacity-editor-color-container">
            <BackgroundShaperFull v-slot="{ shape }">
              <BackgroundView :shape :size="viewportSize" :padding="viewportPadding" :nodes="scaledColorNodes"></BackgroundView>
            </BackgroundShaperFull>
            <NodeFlattener :nodes="scaledColorNodes" @update:nodes="scaledColorNodesUpdated" :slotPropsNames="{flattenedNodes: 'flattenedColorNodes'}" v-slot="{ flattenedColorNodes, flattenedColorNodesUpdated }">
              <ControlsView
                :size="viewportSize" :padding="[viewportPadding[0], 0]"
                :radius="handleRadius" :color="handleColor" :borderColor="handleBorderColor" :showLine="false"
                :nodes="flattenedColorNodes" @update:nodes="flattenedColorNodesUpdated"
              ></ControlsView>
            </NodeFlattener>
          </ViewportContainer>
        </NodeScaler>
      </NodeScaler>
    </NodeScaler>
  </div>
</template>

<style scoped>
.color-opacity-editor-root-container {
  display: flex;
  flex-direction: column;
}

.color-opacity-editor-opacity-container {
  width: 100%;
  flex-grow: 1;
  position: relative;
  overflow: hidden;
}

.color-opacity-editor-canvas {
  position: absolute;
  top: 0;
  left: 0;
}

.color-opacity-editor-color-container {
  width: 100%;
  height: 2.5rem;
  position: relative;
  overflow: hidden;
}
</style>
