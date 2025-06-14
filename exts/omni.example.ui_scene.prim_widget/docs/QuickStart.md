# 빠른 시작 가이드 (Quick Start Guide) 🚀

이 가이드는 가장 간단한 방법으로 prim widget을 사용하는 방법을 알려드려요!

## 🎯 초간단 사용법 (Super Simple Usage)

### 방법 1: 한 줄로 끝내기! ⚡

```python
import omni.example.ui_scene.prim_widget as widget

# 위젯 표시 - 한 줄이면 끝!
widget.show_widget("/World/Cube")    # ✅ 큐브 위젯 바로 표시!

# 위젯 숨김 - 이것도 한 줄!
widget.hide_widget("/World/Cube")    # ❌ 큐브 위젯 숨김!

# 위젯 토글 - 켜져있으면 끄고, 꺼져있으면 켜기!
widget.toggle_widget("/World/Sphere")  # 🔄 스피어 위젯 토글!
```

### 방법 2: 클래스 스타일로! 🎨

```python
from omni.example.ui_scene.prim_widget import SimpleWidget

# 생성과 동시에 표시!
cube = SimpleWidget("/World/Cube", True)     # 큐브 위젯 바로 표시! ✨
sphere = SimpleWidget("/World/Sphere", False) # 스피어 위젯 생성하지만 숨김

# 나중에 조작하기
cube.hide()        # 큐브 숨김
sphere.show()      # 스피어 표시  
cube.toggle()      # 큐브 토글

# 상태 확인
if cube.is_visible():
    print("큐브가 보여요! 👀")

print(cube)  # 현재 상태 출력: "SimpleWidget('/World/Cube', 표시됨)"
```

### 방법 3: 고급 기능까지! 🔥

```python
import omni.example.ui_scene.prim_widget as widget

# 컨트롤러 가져오기
controller = widget.get_controller()

# 여러 위젯 동시에!
controller.show_widget("/World/Cube")
controller.show_widget("/World/Sphere") 
controller.show_widget("/World/Cylinder")

# 현재 표시된 위젯들 확인
visible_widgets = controller.get_visible_widgets()
print(f"표시된 위젯들: {visible_widgets}")

# 모든 위젯 숨기기
controller.hide_all_widgets()
```

## 🌟 실전 예제들

### 📦 여러 박스 한번에 보기
```python
import omni.example.ui_scene.prim_widget as widget

box_paths = ["/World/Box1", "/World/Box2", "/World/Box3"]

# 모든 박스에 위젯 표시
for box_path in box_paths:
    widget.show_widget(box_path)
    print(f"{box_path} 위젯 표시됨! 📦")
```

### 🎭 위젯 쇼타임!
```python
from omni.example.ui_scene.prim_widget import SimpleWidget
import asyncio

async def widget_show():
    # 3개의 위젯 생성 (처음엔 숨김)
    widgets = [
        SimpleWidget("/World/Cube", False),
        SimpleWidget("/World/Sphere", False), 
        SimpleWidget("/World/Cylinder", False)
    ]
    
    # 하나씩 순서대로 등장!
    for i, w in enumerate(widgets):
        print(f"{i+1}번째 위젯 등장! ✨")
        w.show()
        await asyncio.sleep(1.0)  # 1초 대기
    
    print("모든 위젯이 등장했어요! 🎉")

# 실행
asyncio.create_task(widget_show())
```

### 🔍 특정 타입만 보기
```python
import omni.example.ui_scene.prim_widget as widget
import omni.usd
from pxr import UsdGeom

def show_all_meshes():
    """모든 메쉬에 위젯 표시하기"""
    stage = omni.usd.get_context().get_stage()
    if not stage:
        return
    
    mesh_count = 0
    for prim in stage.Traverse():
        if prim.IsA(UsdGeom.Mesh):
            prim_path = str(prim.GetPath())
            if widget.show_widget(prim_path):
                mesh_count += 1
                print(f"메쉬 발견! {prim_path} 위젯 표시 📐")
    
    print(f"총 {mesh_count}개의 메쉬 위젯이 표시됐어요! 🎯")

# 실행
show_all_meshes()
```

## 💡 꿀팁들

### 🎮 토글 버튼 만들기
```python
import omni.example.ui_scene.prim_widget as widget

def toggle_button_for_cube():
    """큐브 위젯 토글 버튼 함수"""
    is_visible = widget.toggle_widget("/World/Cube")
    status = "👁️ 보임" if is_visible else "🙈 숨김"
    print(f"큐브 위젯: {status}")

# 버튼 클릭할 때마다 이 함수 호출!
toggle_button_for_cube()
```

### 🏃‍♂️ 빠른 정리
```python
import omni.example.ui_scene.prim_widget as widget

def quick_cleanup():
    """모든 위젯 한번에 정리"""
    controller = widget.get_controller()
    if controller:
        controller.clear_all_widgets()
        print("모든 위젯 정리 완료! 🧹✨")

quick_cleanup()
```

## 🎉 마무리

이제 세 가지 방법 중 마음에 드는 걸로 골라서 사용하세요!

1. **한 줄로 끝내기** → `widget.show_widget("/World/Cube")` 
2. **클래스 스타일** → `SimpleWidget("/World/Cube", True)`  
3. **고급 기능** → `controller = widget.get_controller()`

**즐거운 위젯팅 되세요!** 🎊✨