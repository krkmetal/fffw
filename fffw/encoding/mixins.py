from typing import TYPE_CHECKING

from fffw.graph import base, VIDEO, VideoMeta

if TYPE_CHECKING:
    StreamValidationTarget = base.Dest
else:
    StreamValidationTarget = object


class StreamValidationMixin(StreamValidationTarget):

    def connect_edge(self, edge: base.Edge) -> base.Edge:
        self.validate_edge_kind(edge)
        self.validate_edge_device(edge)
        return super().connect_edge(edge)

    def validate_edge_kind(self, edge: base.Edge) -> None:
        kind = getattr(self, 'kind', None)
        if kind is None:
            return
        if edge.kind != kind:
            # Audio filter can't handle video stream and so on
            raise ValueError(edge.kind)

    def validate_edge_device(self, edge: base.Edge) -> None:
        if edge.kind != VIDEO:
            return
        meta = edge.get_meta_data(self)
        if not isinstance(meta, VideoMeta):
            return
        filter_hardware = getattr(self, 'hardware', None)
        device = meta.device
        edge_hardware = None if device is None else device.hardware
        if filter_hardware != edge_hardware:
            # A stream uploaded to a video card could not be processed with CPU
            # filter.
            raise ValueError(edge_hardware)
