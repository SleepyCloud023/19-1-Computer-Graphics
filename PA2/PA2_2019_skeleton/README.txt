2015004075 김태형
SimpleScene.py 파일만 수정하였습니다

추가한 함수:

def pOnSplineAtTime(control_points, time) 
: 컨트롤포인트배열(사이즈 6), 시간값을 받아 4개의 점으로 캣멀롬 곡선을 구성하고 시간에 맞는 곡선위의 점의 3차원 좌표를 반환합니다.
def grdOnSplineAtTime(control_points, time)
: 컨트롤포인트배열(사이즈 6), 시간값을 받아 4개의 점으로 캣멀롬 곡선을 구성하고 시간에 맞는 곡선위의 점에서의 접선 gradient를 반환합니다.
def myRotate(gradient):
: gradient를 받아 (0,0,1) -> (gradient) 로 로컬 축 변환해주는 행렬을 반환합니다.