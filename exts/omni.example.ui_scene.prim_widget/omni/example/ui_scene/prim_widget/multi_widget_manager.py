# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["MultiWidgetManager"]

from typing import Dict, List, Optional
from .prim_widget_model import PrimWidgetModel
from .prim_widget_manipulator import PrimWidgetManipulator


class MultiWidgetManager:
    """
    Manager class that handles multiple prim widgets simultaneously.
    Each prim gets its own model and manipulator instance.
    """
    
    def __init__(self, scene_view):
        self._scene_view = scene_view
        self._active_widgets: Dict[str, Dict] = {}  # prim_path -> {model, manipulator, enabled}
    
    def show_widget(self, prim_path: str) -> bool:
        """
        Show a widget for the specified prim path.
        Creates new widget if it doesn't exist.
        
        Args:
            prim_path: USD prim path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if prim_path not in self._active_widgets:
                # Create new widget components
                model = PrimWidgetModel()
                
                # Add manipulator to the scene
                with self._scene_view.scene:
                    manipulator = PrimWidgetManipulator(model=model)
                
                self._active_widgets[prim_path] = {
                    'model': model,
                    'manipulator': manipulator,
                    'enabled': False
                }
            
            # Enable the widget
            widget_info = self._active_widgets[prim_path]
            widget_info['model'].set_prim_path(prim_path)
            widget_info['model'].set_enabled(True)
            widget_info['enabled'] = True
            
            return True
            
        except Exception as e:
            print(f"Failed to show widget for {prim_path}: {e}")
            return False
    
    def hide_widget(self, prim_path: str) -> bool:
        """
        Hide the widget for the specified prim path.
        
        Args:
            prim_path: USD prim path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if prim_path in self._active_widgets:
                widget_info = self._active_widgets[prim_path]
                widget_info['model'].set_enabled(False)
                widget_info['enabled'] = False
                return True
            return False
            
        except Exception as e:
            print(f"Failed to hide widget for {prim_path}: {e}")
            return False
    
    def toggle_widget(self, prim_path: str) -> bool:
        """
        Toggle widget visibility for the specified prim path.
        
        Args:
            prim_path: USD prim path
            
        Returns:
            True if now visible, False if now hidden
        """
        if prim_path in self._active_widgets and self._active_widgets[prim_path]['enabled']:
            self.hide_widget(prim_path)
            return False
        else:
            self.show_widget(prim_path)
            return True
    
    def is_widget_visible(self, prim_path: str) -> bool:
        """
        Check if a widget is currently visible.
        
        Args:
            prim_path: USD prim path
            
        Returns:
            True if visible, False otherwise
        """
        return (prim_path in self._active_widgets and 
                self._active_widgets[prim_path]['enabled'])
    
    def get_visible_widgets(self) -> List[str]:
        """
        Get list of currently visible widget prim paths.
        
        Returns:
            List of visible prim paths
        """
        return [path for path, info in self._active_widgets.items() 
                if info['enabled']]
    
    def get_all_widgets(self) -> List[str]:
        """
        Get list of all widget prim paths (visible and hidden).
        
        Returns:
            List of all prim paths
        """
        return list(self._active_widgets.keys())
    
    def remove_widget(self, prim_path: str) -> bool:
        """
        Completely remove a widget (not just hide).
        
        Args:
            prim_path: USD prim path
            
        Returns:
            True if removed, False if not found
        """
        if prim_path in self._active_widgets:
            widget_info = self._active_widgets[prim_path]
            
            # Disable the model first
            widget_info['model'].set_enabled(False)
            
            # Remove from scene (manipulator will be garbage collected)
            # Note: In practice, you might need to explicitly remove from scene
            
            del self._active_widgets[prim_path]
            return True
        return False
    
    def clear_all_widgets(self):
        """Clear all widgets."""
        for prim_path in list(self._active_widgets.keys()):
            self.remove_widget(prim_path)
    
    def hide_all_widgets(self):
        """Hide all widgets without removing them."""
        for prim_path in self._active_widgets:
            self.hide_widget(prim_path)
    
    def show_all_widgets(self):
        """Show all existing widgets."""
        for prim_path in self._active_widgets:
            self.show_widget(prim_path)