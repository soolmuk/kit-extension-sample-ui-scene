# 다중 위젯 사용 예제 (Multi-Widget Examples)

이제 `omni.example.ui_scene.prim_widget` 확장이 **다중 위젯(Multiple Widgets)**을 지원합니다! 여러 개의 prim에 동시에 위젯을 표시할 수 있습니다.

## 기본 다중 위젯 사용법 (Basic Multi-Widget Usage)

### 1. 여러 위젯 동시 표시

```python
import omni.ext

# 컨트롤러 가져오기
extension_manager = omni.ext.get_extension_manager()
extension = extension_manager.get_extension("omni.example.ui_scene.prim_widget")
controller = extension.get_widget_controller()

# 여러 prim에 위젯 표시 - 이제 모두 동시에 보입니다!
controller.show_widget("/World/Cube")
controller.show_widget("/World/Sphere")
controller.show_widget("/World/Cylinder")

print(f"표시된 위젯: {controller.get_visible_widgets()}")
# 출력: ['World/Cube', '/World/Sphere', '/World/Cylinder']
```

### 2. 선택적 위젯 숨김

```python
# 특정 위젯만 숨기기
controller.hide_widget("/World/Cube")

# 남은 위젯 확인
print(f"표시된 위젯: {controller.get_visible_widgets()}")
# 출력: ['/World/Sphere', '/World/Cylinder']

# 개별 위젯 토글
controller.toggle_widget("/World/Cube")  # 다시 표시됨
controller.toggle_widget("/World/Sphere")  # 숨겨짐
```

### 3. 위젯 상태 관리

```python
# 모든 위젯 상태 확인
all_widgets = controller.get_all_widgets()
visible_widgets = controller.get_visible_widgets()

print(f"전체 위젯: {all_widgets}")
print(f"표시된 위젯: {visible_widgets}")

# 개별 위젯 상태 확인
for prim_path in all_widgets:
    is_visible = controller.is_widget_visible(prim_path)
    status = "표시됨" if is_visible else "숨겨짐"
    print(f"{prim_path}: {status}")
```

## 고급 다중 위젯 활용 (Advanced Multi-Widget Usage)

### 1. 동적 위젯 그룹 관리

```python
class WidgetGroup:
    def __init__(self, controller, group_name):
        self.controller = controller
        self.group_name = group_name
        self.prim_paths = []
    
    def add_prim(self, prim_path):
        """그룹에 prim 추가"""
        if prim_path not in self.prim_paths:
            self.prim_paths.append(prim_path)
    
    def show_group(self):
        """그룹의 모든 위젯 표시"""
        success_count = 0
        for prim_path in self.prim_paths:
            if self.controller.show_widget(prim_path):
                success_count += 1
        print(f"{self.group_name} 그룹: {success_count}/{len(self.prim_paths)} 위젯 표시됨")
    
    def hide_group(self):
        """그룹의 모든 위젯 숨김"""
        for prim_path in self.prim_paths:
            self.controller.hide_widget(prim_path)
        print(f"{self.group_name} 그룹: 모든 위젯 숨김")
    
    def toggle_group(self):
        """그룹 토글"""
        visible_count = sum(1 for p in self.prim_paths 
                           if self.controller.is_widget_visible(p))
        
        if visible_count > 0:
            self.hide_group()
        else:
            self.show_group()

# 사용 예제
lights_group = WidgetGroup(controller, "조명")
lights_group.add_prim("/World/DistantLight")
lights_group.add_prim("/World/RectLight")
lights_group.add_prim("/World/SphereLight")

props_group = WidgetGroup(controller, "소품")
props_group.add_prim("/World/Cube")
props_group.add_prim("/World/Sphere")
props_group.add_prim("/World/Cylinder")

# 그룹별 제어
lights_group.show_group()    # 조명 위젯들만 표시
props_group.show_group()     # 소품 위젯들도 표시 (조명과 함께)
lights_group.toggle_group()  # 조명 위젯들 토글
```

### 2. 조건부 다중 위젯 표시

```python
import omni.usd
from pxr import UsdGeom, UsdLux

def show_widgets_by_type(prim_type_filter):
    """특정 타입의 모든 prim에 위젯 표시"""
    stage = omni.usd.get_context().get_stage()
    if not stage:
        return []
    
    shown_widgets = []
    
    for prim in stage.Traverse():
        prim_path = str(prim.GetPath())
        
        # 타입별 필터링
        should_show = False
        if prim_type_filter == "mesh" and prim.IsA(UsdGeom.Mesh):
            should_show = True
        elif prim_type_filter == "light" and prim.IsA(UsdLux.Light):
            should_show = True
        elif prim_type_filter == "camera" and prim.IsA(UsdGeom.Camera):
            should_show = True
        
        if should_show:
            if controller.show_widget(prim_path):
                shown_widgets.append(prim_path)
                print(f"{prim_type_filter} 위젯 표시: {prim_path}")
    
    return shown_widgets

# 사용 예제
mesh_widgets = show_widgets_by_type("mesh")     # 모든 메쉬에 위젯
light_widgets = show_widgets_by_type("light")   # 모든 조명에 위젯

print(f"메쉬 위젯 {len(mesh_widgets)}개, 조명 위젯 {len(light_widgets)}개 표시됨")
```

### 3. 애니메이션된 위젯 표시

```python
import asyncio

async def animated_widget_showcase():
    """위젯들을 순차적으로 표시하는 애니메이션"""
    prim_list = ["/World/Cube", "/World/Sphere", "/World/Cylinder"]
    
    # 1단계: 하나씩 순차 표시
    print("1단계: 순차 표시")
    for i, prim_path in enumerate(prim_list):
        controller.show_widget(prim_path)
        print(f"  {i+1}. {prim_path} 표시됨")
        await asyncio.sleep(1.0)
    
    # 2단계: 잠시 대기
    print("2단계: 모든 위젯 표시 상태 유지")
    await asyncio.sleep(2.0)
    
    # 3단계: 하나씩 순차 숨김
    print("3단계: 순차 숨김")
    for i, prim_path in enumerate(prim_list):
        controller.hide_widget(prim_path)
        print(f"  {i+1}. {prim_path} 숨겨짐")
        await asyncio.sleep(1.0)
    
    # 4단계: 모두 다시 표시
    print("4단계: 모두 다시 표시")
    for prim_path in prim_list:
        controller.show_widget(prim_path)
    
    print("애니메이션 완료!")

# 실행
asyncio.create_task(animated_widget_showcase())
```

### 4. 위젯 상태 모니터링 대시보드

```python
class WidgetDashboard:
    def __init__(self, controller):
        self.controller = controller
        self.monitoring = False
    
    async def start_monitoring(self, interval=2.0):
        """위젯 상태를 실시간으로 모니터링"""
        self.monitoring = True
        print("=== 위젯 대시보드 시작 ===")
        
        while self.monitoring:
            visible_widgets = self.controller.get_visible_widgets()
            all_widgets = self.controller.get_all_widgets()
            hidden_count = len(all_widgets) - len(visible_widgets)
            
            print(f"\n[대시보드] 시간: {asyncio.get_event_loop().time():.1f}")
            print(f"  📊 전체 위젯: {len(all_widgets)}개")
            print(f"  ✅ 표시된 위젯: {len(visible_widgets)}개")
            print(f"  ❌ 숨겨진 위젯: {hidden_count}개")
            
            if visible_widgets:
                print(f"  👁️  표시 목록: {', '.join(visible_widgets)}")
            
            await asyncio.sleep(interval)
    
    def stop_monitoring(self):
        """모니터링 중지"""
        self.monitoring = False
        print("=== 위젯 대시보드 종료 ===")

# 사용 예제
dashboard = WidgetDashboard(controller)

# 백그라운드 모니터링 시작
monitoring_task = asyncio.create_task(dashboard.start_monitoring(3.0))

# 테스트 위젯 조작
await asyncio.sleep(1)
controller.show_widget("/World/Cube")
await asyncio.sleep(3)
controller.show_widget("/World/Sphere")
await asyncio.sleep(3)
controller.toggle_widget("/World/Cylinder")
await asyncio.sleep(3)
controller.hide_widget("/World/Cube")
await asyncio.sleep(3)

# 모니터링 중지
dashboard.stop_monitoring()
```

## 성능 최적화 팁 (Performance Tips)

### 1. 배치 작업 (Batch Operations)

```python
def batch_widget_operations(prim_paths, operation="show"):
    """여러 위젯을 배치로 처리"""
    success_count = 0
    
    for prim_path in prim_paths:
        try:
            if operation == "show":
                success = controller.show_widget(prim_path)
            elif operation == "hide":
                success = controller.hide_widget(prim_path)
            elif operation == "remove":
                success = controller.remove_widget(prim_path)
            else:
                success = False
            
            if success:
                success_count += 1
                
        except Exception as e:
            print(f"배치 작업 실패 - {prim_path}: {e}")
    
    print(f"배치 {operation} 작업: {success_count}/{len(prim_paths)} 성공")
    return success_count

# 사용 예제
prim_list = ["/World/Cube", "/World/Sphere", "/World/Cylinder"]
batch_widget_operations(prim_list, "show")   # 모두 표시
batch_widget_operations(prim_list, "hide")   # 모두 숨김
```

### 2. 메모리 관리

```python
def cleanup_unused_widgets():
    """사용하지 않는 위젯 정리"""
    stage = omni.usd.get_context().get_stage()
    if not stage:
        return
    
    all_widgets = controller.get_all_widgets()
    existing_prims = set()
    
    # 현재 stage에 존재하는 prim들 수집
    for prim in stage.Traverse():
        existing_prims.add(str(prim.GetPath()))
    
    # 존재하지 않는 prim의 위젯 제거
    removed_count = 0
    for widget_path in all_widgets:
        if widget_path not in existing_prims:
            controller.remove_widget(widget_path)
            removed_count += 1
            print(f"제거된 위젯: {widget_path}")
    
    print(f"정리 완료: {removed_count}개 위젯 제거됨")

# 주기적으로 실행
cleanup_unused_widgets()
```

이제 여러 prim에 동시에 위젯을 표시할 수 있습니다!

```python
# 이제 이렇게 하면 둘 다 표시됩니다:
controller.show_widget("/World/Cube")    # Cube 위젯 표시
controller.show_widget("/World/Cone")    # Cone 위젯도 표시 (Cube와 함께!)
```