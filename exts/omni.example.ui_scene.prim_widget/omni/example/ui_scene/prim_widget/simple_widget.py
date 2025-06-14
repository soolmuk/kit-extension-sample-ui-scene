# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["SimpleWidget"]


class SimpleWidget:
    """
    매우 간단한 위젯 클래스
    사용법: SimpleWidget("/World/Cube", True)
    """
    
    def __init__(self, prim_path: str, show: bool = True):
        """
        Args:
            prim_path: USD prim 경로
            show: True면 표시, False면 숨김
        """
        self.prim_path = prim_path
        self._controller = self._get_controller()
        
        if self._controller:
            if show:
                self.show()
            else:
                self.hide()
    
    def _get_controller(self):
        """내부적으로 컨트롤러 가져오기"""
        import omni.ext
        try:
            extension_manager = omni.ext.get_extension_manager()
            extension = extension_manager.get_extension("omni.example.ui_scene.prim_widget")
            if extension:
                return extension.get_widget_controller()
        except Exception as e:
            print(f"컨트롤러 가져오기 실패: {e}")
        return None
    
    def show(self) -> bool:
        """위젯 표시"""
        if self._controller:
            return self._controller.show_widget(self.prim_path)
        return False
    
    def hide(self) -> bool:
        """위젯 숨김"""
        if self._controller:
            return self._controller.hide_widget(self.prim_path)
        return False
    
    def toggle(self) -> bool:
        """위젯 토글"""
        if self._controller:
            return self._controller.toggle_widget(self.prim_path)
        return False
    
    def is_visible(self) -> bool:
        """위젯 표시 상태 확인"""
        if self._controller:
            return self._controller.is_widget_visible(self.prim_path)
        return False
    
    def __repr__(self):
        status = "표시됨" if self.is_visible() else "숨겨짐"
        return f"SimpleWidget('{self.prim_path}', {status})"