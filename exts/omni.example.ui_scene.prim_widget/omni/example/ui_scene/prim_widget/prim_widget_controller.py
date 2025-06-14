# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["PrimWidgetController"]

from typing import Dict, List


class PrimWidgetController:
    """
    Controller class that provides public API for managing prim widgets.
    This class can be used by external code to control widget visibility.
    """
    
    def __init__(self, model):
        self._model = model
        self._active_widgets: Dict[str, bool] = {}
    
    def show_widget(self, prim_path: str) -> bool:
        """
        Show a widget for the specified prim path.
        
        Args:
            prim_path: USD prim path (e.g., "/World/Cube")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._model.set_prim_path(prim_path)
            self._model.set_enabled(True)
            self._active_widgets[prim_path] = True
            return True
        except Exception as e:
            print(f"Failed to show widget for {prim_path}: {e}")
            return False
    
    def hide_widget(self, prim_path: str = None) -> bool:
        """
        Hide the widget for the specified prim path, or hide current widget if no path given.
        
        Args:
            prim_path: USD prim path to hide. If None, hides currently displayed widget.
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if prim_path is None:
                # Hide current widget
                current_path = self._model.get_prim_path()
                if current_path:
                    self._active_widgets[current_path] = False
            else:
                self._active_widgets[prim_path] = False
                
            self._model.set_enabled(False)
            return True
        except Exception as e:
            print(f"Failed to hide widget: {e}")
            return False
    
    def toggle_widget(self, prim_path: str) -> bool:
        """
        Toggle widget visibility for the specified prim path.
        
        Args:
            prim_path: USD prim path
            
        Returns:
            True if now visible, False if now hidden
        """
        current_path = self._model.get_prim_path()
        is_enabled = self._model.is_enabled()
        
        if current_path == prim_path and is_enabled:
            # Currently showing this prim, so hide it
            self.hide_widget(prim_path)
            return False
        else:
            # Either showing different prim or not showing anything, so show this prim
            self.show_widget(prim_path)
            return True
    
    def is_widget_visible(self, prim_path: str = None) -> bool:
        """
        Check if a widget is currently visible.
        
        Args:
            prim_path: USD prim path to check. If None, checks currently displayed widget.
            
        Returns:
            True if visible, False otherwise
        """
        if prim_path is None:
            return self._model.is_enabled()
        
        current_path = self._model.get_prim_path()
        return current_path == prim_path and self._model.is_enabled()
    
    def get_current_prim_path(self) -> str:
        """
        Get the prim path of the currently displayed widget.
        
        Returns:
            Current prim path, or empty string if no widget is displayed
        """
        if self._model.is_enabled():
            return self._model.get_prim_path()
        return ""
    
    def get_active_widgets(self) -> List[str]:
        """
        Get list of prim paths that have been marked as active.
        
        Returns:
            List of prim paths
        """
        return [path for path, active in self._active_widgets.items() if active]
    
    def clear_all_widgets(self):
        """Clear all widget states and hide current widget."""
        self._model.set_enabled(False)
        self._active_widgets.clear()