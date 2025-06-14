# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["PrimWidgetModel"]

from pxr import Tf
from pxr import Usd
from pxr import UsdGeom
from pxr import UsdShade
from omni.ui import scene as sc
import omni.usd

# The distance to raise above the top of the object's bounding box
TOP_OFFSET = 5


class PrimWidgetModel(sc.AbstractManipulatorModel):
    """
    The model tracks the position and info of a specific prim by path.
    Can be controlled programmatically via prim_path and enabled state.
    """
    
    class PositionItem(sc.AbstractManipulatorItem):
        """
        The Model Item represents the position. It doesn't contain anything
        because we take the position directly from USD when requesting.
        """
        def __init__(self):
            super().__init__()
            self.value = [0, 0, 0]

    def __init__(self):
        super().__init__()
        
        # Current target prim and material
        self._prim = None
        self._current_path = ""
        self._material_name = ""
        self._enabled = False
        
        self._stage_listener = None
        self.position = PrimWidgetModel.PositionItem()
        
        # Save the UsdContext name (we currently only work with a single Context)
        self._usd_context = omni.usd.get_context()

    def set_prim_path(self, prim_path: str):
        """Set the target prim path."""
        if self._current_path == prim_path:
            return
            
        self._current_path = prim_path
        self._update_prim_info()

    def set_enabled(self, enabled: bool):
        """Enable or disable the widget display."""
        if self._enabled == enabled:
            return
            
        self._enabled = enabled
        
        if enabled:
            self._update_prim_info()
        else:
            self._clear_prim_info()
        
        # Notify that the position changed to trigger re-render
        self._item_changed(self.position)

    def is_enabled(self) -> bool:
        """Check if the widget is currently enabled."""
        return self._enabled

    def get_prim_path(self) -> str:
        """Get the current prim path."""
        return self._current_path

    def _update_prim_info(self):
        """Update prim information based on current path."""
        if not self._current_path or not self._enabled:
            return
            
        stage = self._usd_context.get_stage()
        if not stage:
            return
            
        prim = stage.GetPrimAtPath(self._current_path)
        if not prim.IsValid():
            self._clear_prim_info()
            return
            
        if not prim.IsA(UsdGeom.Imageable):
            self._clear_prim_info()
            return
            
        # Set up stage listener for this prim
        if not self._stage_listener:
            self._stage_listener = Tf.Notice.Register(
                Usd.Notice.ObjectsChanged, self._notice_changed, stage
            )
            
        # Get material info
        material, relationship = UsdShade.MaterialBindingAPI(prim).ComputeBoundMaterial()
        if material:
            self._material_name = str(material.GetPath())
        else:
            self._material_name = "N/A"
            
        self._prim = prim
        
        # Position is changed because we have a new target prim
        self._item_changed(self.position)

    def _clear_prim_info(self):
        """Clear prim information."""
        self._prim = None
        self._material_name = ""
        
        # Revoke the Tf.Notice listener
        if self._stage_listener:
            self._stage_listener.Revoke()
            self._stage_listener = None
            
        # Notify that the position changed to trigger re-render
        self._item_changed(self.position)

    def _notice_changed(self, notice: Usd.Notice, stage: Usd.Stage) -> None:
        """Called by Tf.Notice when the current target prim changes."""
        if not self._enabled or not self._current_path:
            return
            
        for p in notice.GetChangedInfoOnlyPaths():
            if self._current_path in str(p.GetPrimPath()):
                self._item_changed(self.position)

    def get_item(self, identifier):
        if identifier == "position":
            return self.position
        if identifier == "name":
            return self._current_path if self._enabled else ""
        if identifier == "material":
            return self._material_name if self._enabled else ""

    def get_as_floats(self, item):
        if item == self.position:
            return self._get_position()
        if item:
            return item.value
        return []

    def _get_position(self):
        """Returns position of the target prim."""
        if not self._enabled or not self._current_path:
            return [0, 0, 0]
            
        stage = self._usd_context.get_stage()
        if not stage:
            return [0, 0, 0]
            
        prim = stage.GetPrimAtPath(self._current_path)
        if not prim.IsValid():
            return [0, 0, 0]
            
        # Get position directly from USD
        box_cache = UsdGeom.BBoxCache(
            Usd.TimeCode.Default(), 
            includedPurposes=[UsdGeom.Tokens.default_]
        )
        bound = box_cache.ComputeWorldBound(prim)
        range = bound.ComputeAlignedBox()
        bboxMin = range.GetMin()
        bboxMax = range.GetMax()
        
        # Find the top center of the bounding box and add a small offset upward
        position = [
            (bboxMin[0] + bboxMax[0]) * 0.5,
            bboxMax[1] + TOP_OFFSET,
            (bboxMin[2] + bboxMax[2]) * 0.5
        ]
        return position