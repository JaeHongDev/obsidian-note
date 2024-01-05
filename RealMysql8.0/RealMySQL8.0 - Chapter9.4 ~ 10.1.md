---
cssclasses:
  - my_style_width_100
---
# 쿼리 힌트 

> 💡 옵티마이저 힌트가 필요한 이유
> MySQL 서버는 우리가 서비스하는 비즈니스를 100% 이해하지 못합니다. 그렇기에 서비스 개발자나 DBA보다 MySQL 서버가 부족한 실행 계획을 수립할 때가 있는데 이때 옵티마이저에게 쿼리의 실행 계획을 어떻게 수립해야 할지 알려줘야합니다.
> 
> 🗒 결국 힌트는 옵티마이저에게 우리가 원하는 실행 계획의 의도를 명확하게 파악하도록 하기 위함이다.
>  > 어떤 경우에 힌트가 실패할까? (이전에 살펴본 프라이머리키 선호 방식이 있겠다)

MySQL 서버에서 사용 가능한 쿼리 힌트는 2가지가 있습니다.
1. 인덱스 힌트
2. 옵티마이저 힌트


## 인덱스 힌트

> 인덱스 힌트가 뭐지? (책에서 설명이 없는데..?)
> 없어서 공식문서에서 가져옴

Index hints give the optimizer information about how to choose indexes during query processing.

### 🤔 인덱스 힌트의 적용 범위
> index hints apply to [`SELECT`](https://dev.mysql.com/doc/refman/8.0/en/select.html "13.2.13 SELECT Statement") and [`UPDATE`](https://dev.mysql.com/doc/refman/8.0/en/update.html "13.2.17 UPDATE Statement") statements. They also work with multi-table [`DELETE`](https://dev.mysql.com/doc/refman/8.0/en/delete.html "13.2.2 DELETE Statement") statements, but not with single-table `DELETE`, as shown later in this section

책에서 인덱스 힌트는 SELECT, UPDATE에서만 사용가능하다고 한다.
하지만 공식문서에서는 다중 테이블 delete에서도 동작 가능하다고 설명한다.
어떤게 맞는지 책을 보면서 찾아보자


### STRAIGHT_JOIN

STRAIGHT_JOIN는 여러 개의 테이블이 조인될 떄 조인 순서를 고정하는 역할을 합니다. 일반적으로 드라이빙 테이블과 드리븐 테이블을 결정하는 것은 옵티마이저의 역할입니다.
테이블의 레코드 수를 기준으로 적은 테이블은 드라이빙 테이블, 반대는 드리븐테이블로 결정됩니다.
![[Pasted image 20240104202650.png]]
참고로 STRAIGHT_JOIN을 사용하기 위한 기준이 있다.
1. 임시 테이블과 일반 테이블의 조인
	- 일반적으로 임시 테이블을 드라이빙 테이블로 선정하는 것이 좋습니다.
	- 만약 일반 테이블에 인덱스가 없는 경우 레코드가 적은 쪽을 선택하는 것이 좋습니다 (이러면 옵티마이저가 해주는 것 아닌가?) 
2. 임시 테이블끼리 조인
	 - 임시테이블은 인덱스가 없기 때문에 어느 테이블을 먼저 드라이빙으로 읽어도 무관하기에 크기가 작은 테이블을 드라이빙 테이블로 선택해주는 것이 좋습니다.
3. 일반 테이블끼리 조인
	- 양쪽 테이블 모두 조인 컬럼에 인덱스가 있거나 양쪽 테이블 모두 조인 컬럼에 인덱스가 없는 경우에는 레코드 건수가 적은 테이블을 드라이빙으로 선택해주는 것이 좋으며, 그 이외에는 조인 컬럼에 인덱스가 없는 테이블을 드라이빙으로 선택하는 것이 좋습니다. 

### USE INDEX / FORCE INDEX / IGNORE INDEX

위 세종류의 인덱스 힌트는 조인의 순서를 변경하는 것 다음으로 자주 사용됩니다. 
사용하는 방법은 인덱스를 가지는 테이블 뒤에 힌트를 명시하는 것입니다.

#### 왜 사용하나요?
대부분의 경우 옵티마이저는 어떤 인덱스를 선택할지 잘 고르지만 3~4개 이상의 컬럼을 포함하는 비슷한 인덱스가 여러개 존재할 때 실수를 한다. 

#### 어떤 종류가 있나요?
1. `USE INDEX`
2. `FORCE INDEX`
3. `IGNORE INDEX`

##### USE INDEX
가장 자주 사용하는 인덱스 힌트입니다. 옵티마이저에게 특정 테이블의 인덱스를 사용하도록 권장하는 정도입니다.

##### FORCE INDEX
USE INDEX 보다 옵티마이저에게 미치는 영향이 더 큰 인덱스 힌트입니다.
> ⚠ (주의)
> 단 USE INDEX로도 줄 수 없는 경우에는 FORCE INDEX도 적용이 안됩니다.
 
##### IGNORE INDEX
두 인덱스 힌트와 다르게 옵티마이저가 해당 인덱스를 사용할 수 없도록 합니다.



> "가장 훌륭한 최적화는 그 쿼리를 서비스에서 없애 버리거나 튜닝할 필요가 없게 데이터를 최소화하는 것"
> -> 검색할 데이터의 크기를 줄이는  것
> ex) 카카오톡 같은 서비스를 예시로 볼 수 있음 채팅 같은 데이터는 크기가 큰데 서버에서 저장하는 데이터의 크기를 3일로 제한 해버리고 나머지 데이터는 로그로 저장하는 방식
# 부록

### 2가지 형태의 옵티마이저 힌트
```
/*! */
/*+ */
```
https://dev.mysql.com/doc/refman/8.0/en/optimizer-hints.html


370p를 보면 `여전히 MySQL 서버는 우리가 서비스하는 비즈니스를 100% 이해하지는 못한다. 그래서 서비스 개발자나 DBA 보다 MySQL 서버가 부족한 실행 계획을 수립할 때가 있을 수 있다` 에서 어떤 상황에서 주로 MySQL 서버의 옵티마이저가 실행 계획 수립 실패예시입니다.

https://medium.com/daangn/mysql-optimizer-error-e438aa02e622



