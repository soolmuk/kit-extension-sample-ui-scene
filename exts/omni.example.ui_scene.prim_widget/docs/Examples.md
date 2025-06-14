# 사용 예제 (Usage Examples) 🎨

이 문서는 `omni.example.ui_scene.prim_widget` 확장의 다양한 사용 예제를 제공합니다.

> 💡 **귀여운 팁**: 각 예제마다 언제 사용하면 좋은지 귀엽게 설명해드릴게요! 🐾

## 기본 사용법 (Basic Usage)

### 1. 컨트롤러 설정 및 초기화 🚀

> 🌟 **언제 사용해요?**: 처음 시작할 때! 마치 새로운 장난감을 꺼내서 조립하는 기분이에요 ✨

```python
import omni.ext
import omni.usd

# 확장 컨트롤러 가져오기
def get_widget_controller():
    extension_manager = omni.ext.get_extension_manager()
    extension = extension_manager.get_extension("omni.example.ui_scene.prim_widget")
    if extension:
        return extension.get_widget_controller()
    else:
        print("Prim Widget 확장이 활성화되지 않았습니다.")
        return None

controller = get_widget_controller()
```

### 2. 단순 위젯 표시/숨김 👁️‍🗨️

> 🎪 **언제 사용해요?**: "잠깐만, 저 큐브 정보 좀 볼까?" 할 때! 마치 호기심 많은 고양이처럼 prim을 관찰하고 싶을 때 써요 🐱

```python
# 위젯 표시
controller.show_widget("/World/Cube")

# 3초 후 위젯 숨김
import asyncio
async def hide_after_delay():
    await asyncio.sleep(3.0)
    controller.hide_widget("/World/Cube")

# 비동기 실행
asyncio.create_task(hide_after_delay())
```

### 3. 위젯 상태 토글 🎭

> 🔀 **언제 사용해요?**: "음... 보였다 안 보였다 하고 싶어!" 할 때! 마치 까꿍 놀이하는 아기처럼 위젯을 껐다 켰다 하고 싶을 때 완벽해요 👶

```python
# 클릭할 때마다 위젯 토글하는 함수
def toggle_cube_widget():
    prim_path = "/World/Cube"
    is_visible = controller.toggle_widget(prim_path)
    status = "표시됨" if is_visible else "숨겨짐"
    print(f"큐브 위젯 상태: {status}")

# 버튼 클릭 이벤트 등에 연결
toggle_cube_widget()
```

## 고급 사용법 (Advanced Usage)

### 1. 다중 Prim 위젯 관리 🎠

> 🎪 **언제 사용해요?**: "어머, 이 scene에 있는 여러 물체들을 차례차례 보고 싶어!" 할 때! 마치 회전목마 타듯이 여러 prim을 순서대로 구경하고 싶을 때 최고예요 🎡

```python
class MultiPrimWidgetManager:
    def __init__(self, controller):
        self.controller = controller
        self.prim_queue = []
        self.current_index = 0
    
    def add_prim(self, prim_path):
        """관리할 prim 추가"""
        if prim_path not in self.prim_queue:
            self.prim_queue.append(prim_path)
    
    def show_next_widget(self):
        """다음 prim의 위젯 표시"""
        if not self.prim_queue:
            return
        
        # 현재 위젯 숨기기
        self.controller.hide_widget()
        
        # 다음 prim으로 이동
        prim_path = self.prim_queue[self.current_index]
        self.controller.show_widget(prim_path)
        
        self.current_index = (self.current_index + 1) % len(self.prim_queue)
        print(f"다음 위젯 표시: {prim_path}")
    
    def clear_all(self):
        """모든 prim 제거 및 위젯 숨김"""
        self.controller.clear_all_widgets()
        self.prim_queue.clear()
        self.current_index = 0

# 사용 예제
manager = MultiPrimWidgetManager(controller)
manager.add_prim("/World/Cube")
manager.add_prim("/World/Sphere")
manager.add_prim("/World/Cylinder")

# 순환하며 위젯 표시
manager.show_next_widget()  # Cube 표시
manager.show_next_widget()  # Sphere 표시
manager.show_next_widget()  # Cylinder 표시
```

### 2. 선택 기반 위젯 자동 표시 🎯

> 🐕 **언제 사용해요?**: "내가 클릭하는 것마다 자동으로 정보가 나왔으면 좋겠어!" 할 때! 마치 충성스러운 강아지처럼 당신이 선택하는 모든 것을 따라다니며 정보를 보여줄 때 써요 🐕‍🦺

```python
import omni.usd

class SelectionBasedWidget:
    def __init__(self, controller):
        self.controller = controller
        self.usd_context = omni.usd.get_context()
        
        # 선택 변경 이벤트 구독
        self.events = self.usd_context.get_stage_event_stream()
        self.selection_sub = self.events.create_subscription_to_pop(
            self._on_selection_changed, 
            name="Selection Widget Controller"
        )
    
    def _on_selection_changed(self, event):
        """선택 변경 시 자동으로 위젯 표시"""
        if event.type == int(omni.usd.StageEventType.SELECTION_CHANGED):
            selection = self.usd_context.get_selection()
            selected_paths = selection.get_selected_prim_paths()
            
            if selected_paths:
                # 첫 번째 선택된 prim에 위젯 표시
                prim_path = selected_paths[0]
                self.controller.show_widget(prim_path)
                print(f"선택된 prim에 위젯 표시: {prim_path}")
            else:
                # 선택 해제 시 위젯 숨김
                self.controller.hide_widget()
                print("선택 해제됨, 위젯 숨김")
    
    def destroy(self):
        """리소스 정리"""
        if self.selection_sub:
            self.selection_sub.unsubscribe()

# 사용 예제
auto_widget = SelectionBasedWidget(controller)

# 나중에 정리할 때
# auto_widget.destroy()
```

### 3. 조건부 위젯 표시 🔍

> 🕵️ **언제 사용해요?**: "메쉬만 보고 싶어!" 또는 "조명만 체크하고 싶어!" 할 때! 마치 탐정처럼 특정 종류의 물체들만 골라서 조사하고 싶을 때 완벽해요 🔎

```python
import omni.usd
from pxr import UsdGeom

def show_widget_for_mesh_prims():
    """메쉬 prim에만 위젯 표시하는 함수"""
    stage = omni.usd.get_context().get_stage()
    if not stage:
        return
    
    # 모든 prim 순회
    for prim in stage.Traverse():
        # 메쉬 prim인지 확인
        if prim.IsA(UsdGeom.Mesh):
            prim_path = str(prim.GetPath())
            
            # 특정 이름 패턴이 있는 메쉬만 대상
            if "Cube" in prim_path or "Sphere" in prim_path:
                print(f"메쉬 prim 발견: {prim_path}")
                
                # 위젯 표시 (3초간)
                controller.show_widget(prim_path)
                
                # 비동기로 3초 후 숨김
                async def hide_delayed(path):
                    await asyncio.sleep(3.0)
                    controller.hide_widget(path)
                
                asyncio.create_task(hide_delayed(prim_path))
                break  # 첫 번째만 표시

# 사용
show_widget_for_mesh_prims()
```

### 4. 위젯 상태 모니터링 📊

> 🤖 **언제 사용해요?**: "지금 뭐가 켜져있고 꺼져있는지 계속 확인하고 싶어!" 할 때! 마치 부지런한 로봇 비서처럼 위젯 상태를 실시간으로 체크하고 싶을 때 써요 📱

```python
class WidgetStatusMonitor:
    def __init__(self, controller):
        self.controller = controller
        self.monitoring = False
    
    async def start_monitoring(self, interval=1.0):
        """위젯 상태를 주기적으로 모니터링"""
        self.monitoring = True
        
        while self.monitoring:
            current_path = self.controller.get_current_prim_path()
            active_widgets = self.controller.get_active_widgets()
            
            print(f"[모니터] 현재 위젯: {current_path or '없음'}")
            print(f"[모니터] 활성 위젯 수: {len(active_widgets)}")
            
            if active_widgets:
                print(f"[모니터] 활성 위젯 목록: {', '.join(active_widgets)}")
            
            await asyncio.sleep(interval)
    
    def stop_monitoring(self):
        """모니터링 중지"""
        self.monitoring = False

# 사용 예제
monitor = WidgetStatusMonitor(controller)

# 모니터링 시작 (백그라운드에서 실행)
asyncio.create_task(monitor.start_monitoring(2.0))

# 테스트용 위젯 조작
controller.show_widget("/World/Cube")
await asyncio.sleep(3)
controller.toggle_widget("/World/Sphere")
await asyncio.sleep(3)

# 모니터링 중지
monitor.stop_monitoring()
```

## 실전 통합 예제 (Real-world Integration)

### UI 윈도우와 통합 🖥️

> 🎨 **언제 사용해요?**: "버튼으로 클릭클릭하면서 위젯을 조작하고 싶어!" 할 때! 마치 예쁜 리모컨처럼 GUI로 위젯들을 편리하게 제어하고 싶을 때 최고예요 🎮

```python
import omni.ui as ui

class PrimWidgetUI:
    def __init__(self, controller):
        self.controller = controller
        self.window = None
        self.current_path_model = ui.SimpleStringModel()
        
        self._build_ui()
    
    def _build_ui(self):
        """UI 윈도우 구성"""
        self.window = ui.Window("Prim Widget Controller", width=300, height=200)
        
        with self.window.frame:
            with ui.VStack(spacing=5):
                ui.Label("Prim Widget Controller", style={"font_size": 16})
                ui.Spacer(height=5)
                
                # Prim 경로 입력
                with ui.HStack():
                    ui.Label("Prim Path:", width=80)
                    self.path_field = ui.StringField(model=self.current_path_model)
                
                # 버튼들
                with ui.HStack():
                    ui.Button("Show", clicked_fn=self._on_show_clicked)
                    ui.Button("Hide", clicked_fn=self._on_hide_clicked)
                    ui.Button("Toggle", clicked_fn=self._on_toggle_clicked)
                
                # 상태 표시
                ui.Spacer(height=10)
                self.status_label = ui.Label("상태: 대기 중")
                
                # 활성 위젯 목록
                ui.Spacer(height=5)
                ui.Label("활성 위젯:")
                self.active_list = ui.TreeView()
    
    def _on_show_clicked(self):
        prim_path = self.current_path_model.as_string
        if prim_path:
            success = self.controller.show_widget(prim_path)
            if success:
                self.status_label.text = f"위젯 표시: {prim_path}"
            else:
                self.status_label.text = "위젯 표시 실패"
            self._update_active_list()
    
    def _on_hide_clicked(self):
        self.controller.hide_widget()
        self.status_label.text = "위젯 숨김"
        self._update_active_list()
    
    def _on_toggle_clicked(self):
        prim_path = self.current_path_model.as_string
        if prim_path:
            is_visible = self.controller.toggle_widget(prim_path)
            status = "표시됨" if is_visible else "숨겨짐"
            self.status_label.text = f"토글: {prim_path} - {status}"
            self._update_active_list()
    
    def _update_active_list(self):
        """활성 위젯 목록 업데이트"""
        active_widgets = self.controller.get_active_widgets()
        # TreeView 업데이트 로직 (실제 구현에서는 TreeView 모델 사용)
        print(f"활성 위젯: {active_widgets}")

# UI 생성 및 표시
widget_ui = PrimWidgetUI(controller)
```

## 마무리 🎉

이러한 예제들을 통해 다양한 상황에서 prim widget controller를 활용할 수 있습니다!

> 🌈 **최종 팁**: 각 예제는 레고 블록처럼 조합해서 사용할 수 있어요! 
> - 기본 사용법으로 시작해서 → 고급 기능을 추가하고 → UI까지 만들면 완벽! 
> - 마치 요리하듯이 필요한 재료(함수)들을 골라서 맛있는 요리(기능)를 만들어보세요 👨‍🍳✨

**즐거운 위젯 라이프 되세요!** 🎊🎈