from .extension import *
from .prim_widget_controller import PrimWidgetController
from .simple_widget import SimpleWidget

# 간편한 사용을 위한 함수들
def show_widget(prim_path: str) -> bool:
    """
    간편하게 위젯 표시하는 함수
    
    Args:
        prim_path: USD prim 경로
        
    Returns:
        성공 여부
    """
    import omni.ext
    try:
        extension_manager = omni.ext.get_extension_manager()
        extension = extension_manager.get_extension("omni.example.ui_scene.prim_widget")
        if extension:
            controller = extension.get_widget_controller()
            return controller.show_widget(prim_path)
    except Exception as e:
        print(f"위젯 표시 실패: {e}")
    return False

def hide_widget(prim_path: str) -> bool:
    """
    간편하게 위젯 숨김하는 함수
    
    Args:
        prim_path: USD prim 경로
        
    Returns:
        성공 여부
    """
    import omni.ext
    try:
        extension_manager = omni.ext.get_extension_manager()
        extension = extension_manager.get_extension("omni.example.ui_scene.prim_widget")
        if extension:
            controller = extension.get_widget_controller()
            return controller.hide_widget(prim_path)
    except Exception as e:
        print(f"위젯 숨김 실패: {e}")
    return False

def toggle_widget(prim_path: str) -> bool:
    """
    간편하게 위젯 토글하는 함수
    
    Args:
        prim_path: USD prim 경로
        
    Returns:
        토글 후 표시 상태
    """
    import omni.ext
    try:
        extension_manager = omni.ext.get_extension_manager()
        extension = extension_manager.get_extension("omni.example.ui_scene.prim_widget")
        if extension:
            controller = extension.get_widget_controller()
            return controller.toggle_widget(prim_path)
    except Exception as e:
        print(f"위젯 토글 실패: {e}")
    return False

def get_controller():
    """컨트롤러 인스턴스 가져오기"""
    import omni.ext
    try:
        extension_manager = omni.ext.get_extension_manager()
        extension = extension_manager.get_extension("omni.example.ui_scene.prim_widget")
        if extension:
            return extension.get_widget_controller()
    except Exception as e:
        print(f"컨트롤러 가져오기 실패: {e}")
    return None