# 변경 로그 (Changelog)

## [1.0.0] - 2025-01-14

### 추가됨 (Added)
- 프로그래매틱 prim 위젯 제어 기능
- `PrimWidgetController` 공개 API 클래스
- Prim 경로 기반 위젯 표시/숨김 기능
- Boolean 토글 방식의 위젯 제어
- 위젯 상태 추적 및 관리 기능
- 외부 확장에서 사용 가능한 API 인터페이스
- 다중 prim 위젯 상태 관리
- 실시간 prim 정보 업데이트 (경로, 재질 정보)

### 기능 (Features)
- `show_widget()`: 특정 prim에 위젯 표시
- `hide_widget()`: 위젯 숨김 기능
- `toggle_widget()`: 위젯 표시 상태 토글
- `is_widget_visible()`: 위젯 표시 상태 확인
- `get_current_prim_path()`: 현재 표시된 위젯의 prim 경로 조회
- `get_active_widgets()`: 활성 위젯 목록 조회
- `clear_all_widgets()`: 모든 위젯 상태 초기화

### 개선사항 (Improvements)
- 선택(selection) 의존성 제거
- USD 무대(stage) 변경에 대한 실시간 반응
- 메모리 효율적인 리소스 관리
- 예외 처리 및 에러 메시지 개선

### 기술적 세부사항 (Technical Details)
- `omni.ui.scene` API 기반 3D 위젯 렌더링
- `UsdGeom.Imageable` prim 타입 지원
- 실시간 바운딩 박스 계산
- 카메라 방향 자동 조정 (billboard 효과)
- USD Notice 시스템을 통한 prim 변경 감지

### 호환성 (Compatibility)
- Omniverse Kit 103.1+ 지원
- Python 3.7+ 호환
- USD 21.08+ 필요
- `omni.usd`, `omni.ui.scene`, `omni.kit.viewport.utility` 의존성