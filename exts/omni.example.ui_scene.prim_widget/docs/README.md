# Omni UI Scene Prim Widget Controller

이 확장(extension)은 특정 prim에 대해 프로그래매틱하게 3D 위젯을 제어할 수 있는 기능을 제공합니다. 기존의 선택(selection) 기반 시스템과 달리, prim 경로와 boolean 값을 사용하여 위젯을 켜고 끌 수 있습니다.

## 개요 (Overview)

이 확장은 `omni.example.ui_scene.object_info`를 기반으로 하여 다음과 같은 개선사항을 제공합니다:

- **프로그래매틱 제어**: 마우스 클릭이 아닌 코드를 통한 위젯 제어
- **Prim Path 기반**: 특정 USD prim 경로를 직접 지정
- **외부 API**: 다른 확장이나 스크립트에서 사용 가능한 공개 API
- **상태 관리**: 위젯의 표시/숨김 상태를 추적 및 관리

## 주요 기능 (Key Features)

### 1. 프로그래매틱 위젯 제어 (Programmatic Widget Control)
- USD prim 경로를 직접 지정하여 위젯 표시
- Boolean 값으로 위젯 표시/숨김 제어
- 선택 변경 이벤트에 의존하지 않음

### 2. 외부 API 지원 (External API Support)
- `PrimWidgetController` 클래스를 통한 공개 API
- 다른 확장에서 쉽게 사용 가능
- 명확한 함수 인터페이스 제공

### 3. 상태 추적 (State Tracking)
- 활성 위젯 목록 관리
- 현재 표시된 위젯 정보 제공
- 위젯 표시 상태 쿼리 기능

## 아키텍처 (Architecture)

### 구성 요소 (Components)

1. **PrimWidgetModel**: prim 정보와 위치를 관리하는 모델 클래스
2. **PrimWidgetManipulator**: 3D 위젯을 렌더링하는 manipulator 클래스
3. **PrimWidgetController**: 외부 API를 제공하는 컨트롤러 클래스
4. **ViewportScene**: viewport에 scene을 설정하고 관리
5. **PrimWidgetExtension**: 확장의 메인 클래스

### 데이터 플로우 (Data Flow)

```
External Code → PrimWidgetController → PrimWidgetModel → PrimWidgetManipulator → 3D Viewport
```

## 설치 및 활성화 (Installation & Activation)

1. 확장 디렉토리를 Omniverse Kit의 확장 경로에 복사
2. Extension Manager에서 `Omni UI Scene Prim Widget Controller` 검색
3. 확장 활성화

또는 Extension Manager의 설정에서 확장 검색 경로 추가:
```
git://github.com/your-repo/kit-extension-sample-ui-scene?branch=main&dir=exts
```