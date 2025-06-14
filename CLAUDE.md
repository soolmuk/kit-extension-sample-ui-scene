g# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains sample Omniverse Kit extensions demonstrating the `omni.ui.scene` API for creating 3D viewport manipulators and UI overlays. It includes four main extensions:

- **Object Info** (`omni.example.ui_scene.object_info`) - Displays 3D info popover tooltips above selected prims
- **Widget Info** (`omni.example.ui_scene.widget_info`) - Shows a 3D widget with prim path and scale slider above selected objects  
- **Light Manipulator** (`omni.example.ui_scene.light_manipulator`) - Custom manipulator for RectLights to control width, height, and intensity
- **Slider Manipulator** (`omni.example.ui_scene.slider_manipulator`) - Custom slider manipulator above selected prims to control scale

## Architecture

### Extension Structure
Each extension follows the standard Omniverse Kit extension pattern:
- `config/extension.toml` - Extension metadata and dependencies
- `omni/example/ui_scene/<extension_name>/` - Main Python module
  - `extension.py` - Main extension class inheriting from `omni.ext.IExt`
  - `viewport_scene.py` - Manages the `SceneView` and viewport integration
  - `*_manipulator.py` - Custom manipulator implementation using `omni.ui.scene`
  - `*_model.py` - Data model and USD interactions

### Core Components
- **Extension Class**: Inherits from `omni.ext.IExt`, handles startup/shutdown lifecycle
- **ViewportScene**: Creates and manages `sc.SceneView` within viewport frames
- **Manipulator**: Custom 3D UI elements using `omni.ui.scene` API
- **Model**: Handles USD stage interactions and data management

### Key Dependencies
- `omni.ui.scene` - Core 3D UI framework
- `omni.usd` - USD stage and prim access
- `omni.kit.viewport.utility` - Viewport window management

## Development Commands

### App Linking
Link to an Omniverse app for development:
```bash
# Windows
link_app.bat

# Linux
link_app.sh

# Specify specific app
link_app.bat --app code

# Specify custom path
link_app.bat --path "C:/Users/bob/AppData/Local/ov/pkg/create-2022.1.3"
```

### Testing
Run tests for extensions:
```bash
# Tests are defined in extension.toml [[test]] sections
# Run via Kit with test framework (specific commands depend on linked app)
```

### Extension Loading
Extensions can be loaded via:
1. Extension Manager UI with search path: `git://github.com/NVIDIA-Omniverse/kit-extension-sample-ui-scene?branch=main&dir=exts`
2. Direct development after app linking

## Key Patterns

### Extension Lifecycle
```python
class MyExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        viewport_window = get_active_viewport_window()
        self._viewport_scene = ViewportScene(viewport_window, ext_id)
    
    def on_shutdown(self):
        if self._viewport_scene:
            self._viewport_scene.destroy()
```

### Scene Management
```python
# Create SceneView within viewport frame
with viewport_window.get_frame(ext_id):
    scene_view = sc.SceneView()
    with scene_view.scene:
        MyManipulator(model=MyModel())
    viewport_window.viewport_api.add_scene_view(scene_view)
```

### USD Integration
Extensions interact with USD stage through:
- `omni.usd.get_context().get_stage()`
- Selection change callbacks
- Prim attribute modifications
- Transform manipulations

---

# CLAUDE.md (한국어)

이 파일은 Claude Code (claude.ai/code)가 이 저장소의 코드를 작업할 때 가이드를 제공합니다.

## 프로젝트 개요

이 저장소는 3D 뷰포트 조작기와 UI 오버레이를 생성하기 위한 `omni.ui.scene` API를 시연하는 Omniverse Kit 확장 예제들을 포함합니다. 네 가지 주요 확장이 포함되어 있습니다:

- **Object Info** (`omni.example.ui_scene.object_info`) - 선택된 prim 위에 3D 정보 팝오버 툴팁을 표시
- **Widget Info** (`omni.example.ui_scene.widget_info`) - 선택된 객체 위에 prim 경로와 스케일 슬라이더가 있는 3D 위젯을 표시
- **Light Manipulator** (`omni.example.ui_scene.light_manipulator`) - RectLight의 너비, 높이, 강도를 제어하는 커스텀 조작기
- **Slider Manipulator** (`omni.example.ui_scene.slider_manipulator`) - 선택된 prim 위에 스케일을 제어하는 커스텀 슬라이더 조작기

## 아키텍처

### 확장 구조
각 확장은 표준 Omniverse Kit 확장 패턴을 따릅니다:
- `config/extension.toml` - 확장 메타데이터 및 종속성
- `omni/example/ui_scene/<extension_name>/` - 메인 Python 모듈
  - `extension.py` - `omni.ext.IExt`를 상속하는 메인 확장 클래스
  - `viewport_scene.py` - `SceneView` 및 뷰포트 통합 관리
  - `*_manipulator.py` - `omni.ui.scene`을 사용한 커스텀 조작기 구현
  - `*_model.py` - 데이터 모델 및 USD 상호작용

### 핵심 구성요소
- **Extension Class**: `omni.ext.IExt`를 상속하며 시작/종료 생명주기를 처리
- **ViewportScene**: 뷰포트 프레임 내에서 `sc.SceneView`를 생성하고 관리
- **Manipulator**: `omni.ui.scene` API를 사용한 커스텀 3D UI 요소
- **Model**: USD 스테이지 상호작용 및 데이터 관리 처리

### 주요 종속성
- `omni.ui.scene` - 핵심 3D UI 프레임워크
- `omni.usd` - USD 스테이지 및 prim 접근
- `omni.kit.viewport.utility` - 뷰포트 윈도우 관리

## 개발 명령어

### 앱 연결
개발을 위해 Omniverse 앱에 연결:
```bash
# Windows
link_app.bat

# Linux
link_app.sh

# 특정 앱 지정
link_app.bat --app code

# 커스텀 경로 지정
link_app.bat --path "C:/Users/bob/AppData/Local/ov/pkg/create-2022.1.3"
```

### 테스트
확장에 대한 테스트 실행:
```bash
# 테스트는 extension.toml [[test]] 섹션에 정의됨
# 테스트 프레임워크와 함께 Kit을 통해 실행 (구체적인 명령은 연결된 앱에 따라 다름)
```

### 확장 로딩
확장은 다음을 통해 로드할 수 있습니다:
1. Extension Manager UI에서 검색 경로 사용: `git://github.com/NVIDIA-Omniverse/kit-extension-sample-ui-scene?branch=main&dir=exts`
2. 앱 연결 후 직접 개발

## 주요 패턴

### 확장 생명주기
```python
class MyExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        viewport_window = get_active_viewport_window()
        self._viewport_scene = ViewportScene(viewport_window, ext_id)
    
    def on_shutdown(self):
        if self._viewport_scene:
            self._viewport_scene.destroy()
```

### 씬 관리
```python
# 뷰포트 프레임 내에서 SceneView 생성
with viewport_window.get_frame(ext_id):
    scene_view = sc.SceneView()
    with scene_view.scene:
        MyManipulator(model=MyModel())
    viewport_window.viewport_api.add_scene_view(scene_view)
```

### USD 통합
확장들은 다음을 통해 USD 스테이지와 상호작용합니다:
- `omni.usd.get_context().get_stage()`
- 선택 변경 콜백
- Prim 속성 수정
- 변환 조작