# API 문서 (API Documentation)

## PrimWidgetController 클래스

`PrimWidgetController`는 prim 위젯을 제어하기 위한 메인 API 클래스입니다.

### 컨트롤러 인스턴스 가져오기 (Getting Controller Instance)

```python
import omni.ext

# 확장 매니저에서 확장 인스턴스 가져오기
extension_manager = omni.ext.get_extension_manager()
extension = extension_manager.get_extension("omni.example.ui_scene.prim_widget")

# 컨트롤러 인스턴스 가져오기
controller = extension.get_widget_controller()
```

## 메서드 (Methods)

### show_widget(prim_path: str) → bool

지정된 prim 경로에 위젯을 표시합니다.

**Parameters:**
- `prim_path` (str): USD prim 경로 (예: "/World/Cube")

**Returns:**
- `bool`: 성공 시 True, 실패 시 False

**Example:**
```python
# 큐브에 위젯 표시
success = controller.show_widget("/World/Cube")
if success:
    print("위젯이 성공적으로 표시되었습니다.")
```

### hide_widget(prim_path: str = None) → bool

지정된 prim 경로의 위젯을 숨기거나, 경로가 없으면 현재 위젯을 숨깁니다.

**Parameters:**
- `prim_path` (str, optional): USD prim 경로. None이면 현재 표시된 위젯을 숨김

**Returns:**
- `bool`: 성공 시 True, 실패 시 False

**Example:**
```python
# 특정 prim의 위젯 숨기기
controller.hide_widget("/World/Cube")

# 현재 표시된 위젯 숨기기
controller.hide_widget()
```

### toggle_widget(prim_path: str) → bool

지정된 prim 경로의 위젯 표시 상태를 토글합니다.

**Parameters:**
- `prim_path` (str): USD prim 경로

**Returns:**
- `bool`: 토글 후 표시 상태 (True: 표시됨, False: 숨겨짐)

**Example:**
```python
# 위젯 상태 토글
is_visible = controller.toggle_widget("/World/Sphere")
print(f"위젯 표시 상태: {'표시됨' if is_visible else '숨겨짐'}")
```

### is_widget_visible(prim_path: str = None) → bool

위젯의 표시 상태를 확인합니다.

**Parameters:**
- `prim_path` (str, optional): 확인할 USD prim 경로. None이면 현재 표시된 위젯 상태 확인

**Returns:**
- `bool`: 표시 중이면 True, 숨겨져 있으면 False

**Example:**
```python
# 특정 prim 위젯 상태 확인
if controller.is_widget_visible("/World/Cube"):
    print("큐브 위젯이 표시되고 있습니다.")

# 현재 위젯 상태 확인
if controller.is_widget_visible():
    print("현재 위젯이 표시되고 있습니다.")
```

### get_current_prim_path() → str

현재 표시되고 있는 위젯의 prim 경로를 가져옵니다.

**Returns:**
- `str`: 현재 prim 경로, 표시된 위젯이 없으면 빈 문자열

**Example:**
```python
current_path = controller.get_current_prim_path()
if current_path:
    print(f"현재 표시된 위젯의 prim 경로: {current_path}")
else:
    print("현재 표시된 위젯이 없습니다.")
```

### get_active_widgets() → List[str]

활성 상태로 표시된 적이 있는 모든 prim 경로 목록을 가져옵니다.

**Returns:**
- `List[str]`: 활성 prim 경로 목록

**Example:**
```python
active_widgets = controller.get_active_widgets()
print(f"활성 위젯 목록: {active_widgets}")
```

### clear_all_widgets() → None

모든 위젯 상태를 초기화하고 현재 위젯을 숨깁니다.

**Example:**
```python
# 모든 위젯 상태 초기화
controller.clear_all_widgets()
print("모든 위젯이 초기화되었습니다.")
```

## 에러 처리 (Error Handling)

API 메서드들은 예외 발생 시 콘솔에 에러 메시지를 출력하고 False를 반환합니다. 안정적인 사용을 위해 반환값을 확인하는 것을 권장합니다.

```python
# 에러 처리 예제
success = controller.show_widget("/Invalid/Path")
if not success:
    print("위젯 표시에 실패했습니다. prim 경로를 확인하세요.")
```

## 주의사항 (Important Notes)

1. **Prim 유효성**: 지정된 prim 경로가 유효하고 `UsdGeom.Imageable` 타입이어야 합니다.
2. **단일 위젯**: 한 번에 하나의 위젯만 표시할 수 있습니다.
3. **USD Context**: USD stage가 로드되어 있어야 위젯이 정상적으로 동작합니다.
4. **Viewport 의존성**: 활성 viewport가 있어야 위젯이 렌더링됩니다.