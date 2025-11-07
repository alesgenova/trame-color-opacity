from trame_color_opacity.widgets import HtmlElement, add_named_models

class ViewportContainer(HtmlElement):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-viewport-container",
            **kwargs,
        )

        self._attr_names += []

        self._event_names += []

        slot_props = [
            "viewportSize",
        ]
        self._attributes["slot"] = f'v-slot="{{ {", ".join(slot_props)} }}"'

class NodeMerger(HtmlElement):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-node-merger",
            **kwargs,
        )

        self._attr_names += [
            ("color_nodes", "colorNodes"),
            ("opacity_nodes", "opacityNodes"),
        ]

        self._event_names += []

        slot_props = [
            "colorOpacityNodes",
        ]
        self._attributes["slot"] = f'v-slot="{{ {", ".join(slot_props)} }}"'

class BackgroundView(HtmlElement):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-background-view",
            **kwargs,
        )

        self._attr_names += [
            "size",
            "padding",
            "nodes",
            "shape",
        ]

        self._event_names += []

class ControlsView(HtmlElement):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-controls-view",
            **kwargs,
        )

        named_models = [
            "nodes",
        ]

        self._attr_names += [
            "size",
            "padding",
            "radius",
            ("show_line", "showLine"),
            ("line_width", "lineWidth"),
        ]

        self._event_names += []

        add_named_models(self, named_models)

class NodeFlattener(HtmlElement):
    FLATTENED_NODES_SLOT_PROP = "flattenedNodes"
    _next_id = 0

    def __init__(
        self,
        flattened_nodes_slot_prop=FLATTENED_NODES_SLOT_PROP,
        **kwargs,
    ):
        slot_props_names = {
            NodeFlattener.FLATTENED_NODES_SLOT_PROP: flattened_nodes_slot_prop,
        }

        # Place the specific slot_props_names for this instance of the AlertsProvider
        # into a unique location in the state
        slot_props_names_state_key = f"flattener_slot_props_{NodeFlattener._next_id}"
        NodeFlattener._next_id += 1

        super().__init__(
            "trame-coe-node-flattener",
            slot_props_names=(slot_props_names_state_key, slot_props_names),
            **kwargs,
        )

        self._attr_names += [
            ("slot_props_names", "slotPropsNames"),
        ]

        named_models = [
            "nodes",
        ]

        add_named_models(self, named_models)

        slot_props = [
            flattened_nodes_slot_prop,
            f"{flattened_nodes_slot_prop}Updated",
        ]

        self._attributes["slot"] = f'v-slot="{{ { ", ".join(slot_props) } }}"'


class BaseShaper(HtmlElement):
    def __init__(
        self,
        tag,
        **kwargs,
    ):
        super().__init__(
            tag,
            **kwargs,
        )

        slot_props = [
            "shape",
        ]
        self._attributes["slot"] = f'v-slot="{{ {", ".join(slot_props)} }}"'

class BackgroundShaperFull(BaseShaper):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-background-shaper-full",
            **kwargs,
        )

class BackgroundShaperOpacity(BaseShaper):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-background-shaper-opacity",
            **kwargs,
        )

        self._attr_names += [
            "nodes",
        ]

class BackgroundShaperHistograms(BaseShaper):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-background-shaper-histograms",
            **kwargs,
        )

        self._attr_names += [
            "nodes",
        ]

class NodeScaler(HtmlElement):
    SCALED_NODES_SLOT_PROP = "scaledNodes"
    _next_id = 0

    def __init__(
        self,
        scaled_nodes_slot_prop=SCALED_NODES_SLOT_PROP,
        **kwargs,
    ):
        slot_props_names = {
            NodeScaler.SCALED_NODES_SLOT_PROP: scaled_nodes_slot_prop,
        }

        # Place the specific slot_props_names for this instance of the AlertsProvider
        # into a unique location in the state
        slot_props_names_state_key = f"scaler_slot_props_{NodeScaler._next_id}"
        NodeScaler._next_id += 1

        super().__init__(
            "trame-coe-node-scaler",
            slot_props_names=(slot_props_names_state_key, slot_props_names),
            **kwargs,
        )

        self._attr_names += [
            ("x_range", "xRange"),
            ("y_range", "yRange"),
            ("slot_props_names", "slotPropsNames"),
        ]

        named_models = [
            "nodes",
        ]

        add_named_models(self, named_models)

        slot_props = [
            scaled_nodes_slot_prop,
            f"{scaled_nodes_slot_prop}Updated",
        ]

        self._attributes["slot"] = f'v-slot="{{ { ", ".join(slot_props) } }}"'
