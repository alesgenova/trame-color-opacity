import type { MapNode as ExtMapNode } from '@colormap/core/dist/types';

import { MapNode } from '@/types';

export class MapNodeAdapter<T> implements ExtMapNode<T> {
    _node: MapNode<T>;

    constructor(node: MapNode<T>) {
        this._node = node;
    }

    get value() {
        return this._node[0];
    }

    get mapped() {
        return this._node[1];
    }
}
