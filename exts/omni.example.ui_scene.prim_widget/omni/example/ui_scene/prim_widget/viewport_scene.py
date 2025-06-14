
# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["ViewportScene"]

from omni.ui import scene as sc
import omni.ui as ui

from .multi_widget_manager import MultiWidgetManager
from .prim_widget_controller import PrimWidgetController


class ViewportScene:
    """The Multi Prim Widget Scene, placed into a Viewport"""

    def __init__(self, viewport_window: ui.Window, ext_id: str) -> None:
        self._scene_view = None
        self._viewport_window = viewport_window
        self._manager = None
        self._controller = None

        # Create a unique frame for our SceneView
        with self._viewport_window.get_frame(ext_id):
            # Create a default SceneView (it has a default camera-model)
            self._scene_view = sc.SceneView()
            
            # Create manager and controller
            self._manager = MultiWidgetManager(self._scene_view)
            self._controller = PrimWidgetController(self._manager)

            # Register the SceneView with the Viewport to get projection and view updates
            self._viewport_window.viewport_api.add_scene_view(self._scene_view)

    def __del__(self):
        self.destroy()

    def destroy(self):
        if self._scene_view:
            # Empty the SceneView of any elements it may have
            self._scene_view.scene.clear()
            # Be a good citizen, and un-register the SceneView from Viewport updates
            if self._viewport_window:
                self._viewport_window.viewport_api.remove_scene_view(self._scene_view)
        
        # Clean up references
        self._viewport_window = None
        self._scene_view = None
        self._manager = None
        self._controller = None
    
    def get_widget_controller(self) -> PrimWidgetController:
        """Get the widget controller for external API access."""
        return self._controller