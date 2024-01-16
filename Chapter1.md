---
cssclasses:
  - my_style_width_100
---

논리 게이트

게이트 - 물리적으로는 다양한 소재와 제작 기술로 구현되지만, 논리적 작동 방식은 모든 컴퓨터에서 동일하다. 

논리 게이트 - 개인용 컴퓨터, 휴대전화 또는 네트워크 라우터 같은 디지털 기기는 모든 정보를 저장하고 처리하도록 설게된 칩들을 탑재한다. 이 칩들은 모양과 형태가 다르긴 하지만 동일한 구성 요소인 기초 논리 게이트로 만들어진다.

Nand  - 기초적인 논리 게이트

배경 절 - 과제들을 수행하는 데 필요한 지식들을 배움
명세 절 - 칩의 기능을 정의, 칩이 제공해야 하는 다양한 기능을 나열
구현 절 - 칩을 어떻게 실제로 구현할지에 대한 힌트 및 가이드 라인
정리 절 - 논의에서 빠진 주요 주제들에 대해 언급
프로젝트 절 - 책에서 제공하는 하드웨어 시뮬레이터를 활용하여 개인용 컴퓨터에 들어갈 칩들을 만듦 


# 배경
불 게이트 

불 게이트는 불 함수를 물리적으로 구현한 것

불 대수 - 참/거짓, 1/0, 예/아니오, 켜짐/꺼짐 같은 불 값을 다루는 대수학 (책에서는 0과 1)

불 함수는 2진수를 입력받아 2진수를 출력하는 함수

불 함수를 정의하고 분석하는 것이 컴퓨터 아키텍처를 구축하는 첫 단계

진리표 - 불 함수를 에시로 들었을 때 입력값(이진수)들과 결과값(이진수)들을 나란히 쓰는 것을 의미

앞부분 세 열은 함수 입력값이 될 수 있는 모든 2진 값 조합을 나타낸다.
마지막 열은 2^n개의 튜플 V1....Vn(n = 3)에 대한 함수 값 f(V1....Vn)이다.

```
x y z f(x,y,z)
0 0 0 0
0 0 1 0
0 1 0 1
0 1 1 0
1 0 0 0
1 0 1 0
1 1 0 1
1 1 1 0
```

불 표현식 
- 불 함수는 진리표 말고도 입력값에 대한 불 연산으로도 표현 가능하다. 
- 자주 사용하는 불 연산은 
	- And (x = 1, y = 1, 1)
	- Or (x or y is 1, 1)
	- Not (Not x , x is 0, 1)
- 위 진리표에 정의된 함수 $$f(x, y, z)=(x+y) \neg z $$는 위 수식으로 표현할 수 있습니다.
 
정준 표현 - 모든 불 함수는 정준 표현이라는 불 표현식으로 표현 가능하다.
-  함수의 진리표에서 함수 값이 1인 행들을 보면 각 행의 입력값에 대해 리터럴(변수, 변수의 부정값)을 And 연산으로 묶어 하나의 항으로 구성할 수 있다.
```
x = 0, y = 1, z = 0

```
$$\neg xy\neg z$$
```
f(x, y, z) = 1인 조건을 보면
x y z
0 0 1
0 1 0
1 1 0
이렇게 세 조건이 있습니다.
```
위 세 조건을 각각 수식으로 표현하면 
$$\neg xy\neg z$$
$$\neg x \neg yz$$
$$xy\neg z$$
위와 같습니다. 

즉 불 함수로 다시 표현하면 아래와 같이 표현가능합니다.
$$
f(x,y,z) = \neg xy\neg z + x\neg y\neg z + \neg x \neg yz
$$

즉 위와 같은 표현식을 정준 표현식이라고 부릅니다.

2- 입력 불 함수 

n개의 2진 변수에 대해 정의되는 불 함수의 수는 $$2^{2^n}$$ 개임을 알 수 있습니다.
![[Pasted image 20240108181711.png]]
두 변수에 대한 16개의 불 함수 예시가 나열되어 있는데, 이 함수들은 오른쪽 4개 열에 열거된, 4개의 2진 값 조합마다 가능한 모든 결괏값들에 따라 체계적으로 결정됩니다.


