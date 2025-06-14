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
    Controller class that provides public API for managing multiple prim widgets.
    This class can be used by external code to control widget visibility.
    Supports multiple widgets simultaneously.
    """
    
    def __init__(self, multi_widget_manager):
        self._manager = multi_widget_manager
    
    def show_widget(self, prim_path: str) -> bool:
        """
        Show a widget for the specified prim path.
        Multiple widgets can be active simultaneously.
        
        Args:
            prim_path: USD prim path (e.g., "/World/Cube")
            
        Returns:
            True if successful, False otherwise
        """
        return self._manager.show_widget(prim_path)
    
    def hide_widget(self, prim_path: str) -> bool:
        """
        Hide the widget for the specified prim path.
        
        Args:
            prim_path: USD prim path to hide
            
        Returns:
            True if successful, False otherwise
        """
        return self._manager.hide_widget(prim_path)
    
    def toggle_widget(self, prim_path: str) -> bool:
        """
        Toggle widget visibility for the specified prim path.
        
        Args:
            prim_path: USD prim path
            
        Returns:
            True if now visible, False if now hidden
        """
        return self._manager.toggle_widget(prim_path)
    
    def is_widget_visible(self, prim_path: str) -> bool:
        """
        Check if a widget is currently visible.
        
        Args:
            prim_path: USD prim path to check
            
        Returns:
            True if visible, False otherwise
        """
        return self._manager.is_widget_visible(prim_path)
    
    def get_visible_widgets(self) -> List[str]:
        """
        Get list of currently visible widget prim paths.
        
        Returns:
            List of visible prim paths
        """
        return self._manager.get_visible_widgets()
    
    def get_all_widgets(self) -> List[str]:
        """
        Get list of all widget prim paths (visible and hidden).
        
        Returns:
            List of all prim paths
        """
        return self._manager.get_all_widgets()
    
    def remove_widget(self, prim_path: str) -> bool:
        """
        Completely remove a widget (not just hide).
        
        Args:
            prim_path: USD prim path
            
        Returns:
            True if removed, False if not found
        """
        return self._manager.remove_widget(prim_path)
    
    def clear_all_widgets(self):
        """Clear all widget states and remove all widgets."""
        self._manager.clear_all_widgets()
    
    def hide_all_widgets(self):
        """Hide all widgets without removing them."""
        self._manager.hide_all_widgets()
    
    def show_all_widgets(self):
        """Show all existing widgets."""
        self._manager.show_all_widgets()