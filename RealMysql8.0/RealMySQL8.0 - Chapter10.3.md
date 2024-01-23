---
cssclasses:
  - my_style_width_100
aliases:
---
## rows

MySQL 실행 계획의 rows 컬럼값은 실행 계획의 효율성 판단을 위해 예측했던 레코드 건수를 보여준다. 

rows 컬럼은 몇 가지 주의 할 점이 있습니다.
1.  각 스토리지 엔진별로 가지고 있는 통계 정보를 참조해 MySQL 옵티마이저가 산출한 예상값으로 정확하지 않습니다. 
2.  표시되는 값은 반환하는 레코드의 예측치가 아닌 ==쿼리를 처리하기 위해 얼마나 많은 레코드를 읽고 체크해야 하는지를 의미합니다== 
3.  실행 계획의 rows 컬럼에 출력되는 값과 실제 쿼리 결과 반환된 레코드 건수는 일치하지 않는 경우가 많습니다. 


![[Pasted image 20240120195037.png]]
위 쿼리는 `from_date >= 1985-01-01` 조건을 만족하는 레코드를 검색하는 쿼리입니다.

해당 쿼리는 ix_fromdate 인덱스를 이용해 처리할 수 있지만 풀 테이블 스캔을 선택했습니다.
![[Pasted image 20240120195242.png]]

이는 전체 테이블 레코드의 건수는 33만건이고 실행 계획에서 나온 결과와 비교했을 때 거의 차이가 없는 것을 알 수 있습니다.
결국 인덱스를 사용하는 것 보다 풀테이블 스캔을 활용하는 것이 더 낫다고 옵티마이저가 선택한 것입니다.

![[Pasted image 20240120195526.png]]
![[Pasted image 20240120201259.png]]
위 쿼리 실행 계획을 보면 MySQL 옵티마이저는 대략 292건의 레코드만 읽고 체크해 보면 원하는 결과를 가져올 수 있을 것으로 예측했습니다.  더 나아가 이전 쿼리와 달리 풀 테이블 스캔이 아닌 range로 인덱스 스캔을 사용했다는 것 또한 알 수 있습니다.

이는 옵티마이저가 from_date 컬럼의 값이 위 조건을 만족하는 경우를 292건만 존재할 것으로 예측했고, 전체 테이블 건수와 비교하면 8.8% 밖에 되지 않습니다. 

최종적으로 옵티마이저는 ix_fromdate 인덱스를 range 방식으로 처리한 것입니다.


### 정리
결국 row 컬럼은 옵티마이저가 해당 테이블의 실행 계획의 효율성 판단을 위해 예측치며 표현된 값은 쿼리를 처리하기 위해 얼마나 많은 레코드를 읽고 체크해야 하는지를 의미합니다.


## filtered 컬럼

옵티마이저는 각 테이블에서 일치하는 레코드 개수를 가능하면 정확히 파악해야 좀더 효율적인 실행 계획을 수립할 수 있습니다.

대부분의 쿼리에서 where절에 사용되는 조건이 모두 인덱스를 사용할 수 있는 것은 아닙니다.

특히 조인이 사용되는 경우에는 where절에서 인덱스를 사용할 수 있는 조건도 중요하지만 인덱스를 사용하지 못하는 조건에 일치하는 레코드 건수를 파악하는 것도 매우 중요합니다.

> 책 예시 실행 결과가 다름

![[Pasted image 20240120205346.png]]

### 정리
filtered 컬럼의 값은 필터링되어 버려지는 레코드의 비율이 아닌 필터링되고 남은 레코드의 비율을 의미한다.

# Extra 컬럼

Extra 컬럼에는 주로 내부적인 처리 알고리즘을 표현합니다.

- const row not found
- Deleting all rows
- Distinct
- FirstMatch
- etc...


## const row not found
쿼리의 실행 계획에서 const 접근 방법으로 테이블을 읽었지만 실제로 해당 테이블에 레코드가 1건도 존재하지 않는 경우 Extra컬럼에 이 내용이 표시됩니다.

(재현x)

## Deleting all rows

MyISAM 스토리지 엔진과 같이 스토리지 엔진의  핸들러 차원에서 테이블의 모든 레코드들 삭제하는 기능을 제공하는 스토리지 엔진 테이블인 경우 Delete 쿼리 호출 시 처리된다. 

## Distinct

![[Pasted image 20240121183724.png]]
위 쿼리는 사원이 존재하는 부서번호 목록을 가져오도록 하는 쿼리입니다.
![[Pasted image 20240121183949.png]]

단순하게dept_emp 테이블을 읽을 때 row를 읽지 않고 무시했다는 의미입니다.

## FirstMatch
세미 조인의 여러 최적화 중에 FirstMatch 전략이 사용되면 Extra 컬럼에 FirstMatch 메시지를 출력합니다. 
[[RealMySQL8.0 - Chapter9.3#퍼스트 매치 (firstmatch)]]

## Full scan on Null Key

![[Pasted image 20240121185749.png]]
(오타 ㅎㄷㄷ)

단순하게  "col1 in (select col2 from ... )" 쿼리에서 col1 null인 경우 해당합니다.

## Impossible Having

![[Pasted image 20240121190456.png]]

쿼리에 사용된 Having절의 조건을 만족하는 레코드가 없을 때 실행 계힉의 Extra컬럼에는 IMpossible Havning 키워드가 표시됩니다.


## Impossible Where
Impossible Having과 동일하며 where 조건이 항상 false가 될 수밖에 없는 경우 Impossible Where가 표시됩니다. 

## LooseScan
세미 조인 최적화 중에서 LooseScan 최적화 전략이 사용되면 실행 계획의 Extra 컬럼에 LooseScan이 표시됩니다.
[[RealMySQL8.0 - Chapter9.3#루스 스캔]]

## No Matching min/max row 

Impossible where에 더해 min,max를 사용하는 경우 No matching min/max row 라는 메시지가 출력됩니다.
![[Pasted image 20240121194541.png]]



## no matching row in const table
const 방식으로 접근할 때 일치하는 레코드가 없다면 no matching row in const table 메시지가 표시됩니다.
![[Pasted image 20240121182604.png]]*


## no matching rows after partition pruning
No matching rows after partition pruning 메시지는 파티션된 테이블에 대한 update 또는 delete 명령의 실행 계획에서 표 시될 수 있는데, 해당 파티션에서 update하거나, delete할 대상 레코드가 없을 때 표시됩니다.


## no table used
말 그대로 쿼리에서 테이블이 존재하지 않는 경우 표시되는 메시지 입니다.

## Not exists

안티 조인 혹은 아우터 조인에서 on 절이 아닌 where 절의 컬럼이 null 인 경우 해당됩니다.
![[Pasted image 20240121195428.png]]-


## Plain isn't ready yet

아래 방식을 이용해서 Explain for connection 명령을 실행했을 때 Extra 컬럼에 Plain is not read yet이라는 메시지가 표시되는데 이는 커넥션에서 아직 쿼리의 실행 게획을 수립하지 못한 상태에서 Expalin for connection 명령이 실행된 것을 의미합니다.
![[화면 기록 2024-01-21 오후 8.03.22.mov]]


## Range checked for each record(index map: N)
![[Pasted image 20240123012038.png]]

조인 조건에 상수가 없고 둘 다 변수인 경우 MySQL 옵티마이저는 어느 테이블을 읽어야 효율적인지 판단할 수 없습니다. 
매 레코드를 읽을 때 마다 계산 기준이 바뀌기 떄문입니다.

Extra 컬럼에 표시된 값의 의미는 레코드마다 인덱스 레인지 스캔을 체크한다의 의미입니다.

여기서 (index map : 0x1) 은 사용할지 말지를 판단하는 후보 인덱스의 순번을 의미합니다.

![[Pasted image 20240123012424.png]]

즉 0x1 는 첫 번째 인덱스를 사용하는 것을 의미하고 0x2는 ix_hiredate 두 번째 인덱스를 후보 인덱스로 둔다는 의미입니다. 
> 0x2 -> 0010임 
> 여기서 비트맵 규칙에 따라 2번 째 위치한 인덱스를 후보군으로 두는 것입니다. 


## Recursive 

![[Pasted image 20240123012936.png]]

Mysql 8.0 부터는 CTE를 이용해 재귀 쿼리를 작성할 수 있게 됐습니다. 

위 쿼리의 WIT 절에서 발생하는 작업은 다음과 같습니다. 
1. n이라는 컬럼을 가진 cte라는 이름의 내부 임시테이블을 생성
2. n 컬럼의 값이 1부터 5까지 1씩 증가하게 해서 레코드 5건을 만들어서 cte 내부 임시 테이블에 저장

쿼리 실행 계획을 보면 Extra 컬럼에 Recursive 값이 표시됨


## Rematerialize

MySQL 8.0 버전부터는 래터럴 조인 기능이 추가됐습니다.
래터럴 조인 과정에서 테이블은 선행 테이블의 레코드별로 서브쿼리를 실행해서 그 결과를 임시 테이블에 저장하는데 이 과정을 Rematerializing 이라고 합니다.

![[Pasted image 20240123013410.png]]

employees 테이블의 레코드마다 slararies 테이블에서 emp_no가 일치하는 레코드 중에서 from_date 컬럼의 역순으로 2건만 가져와 임시 테이블을 derived2로 저장했습니다.
그리고 employees 테이블과 derived2 테이블을 조인한다. 여기서 derived2 임시 테이블은 employees 테이블의 레코드마다 새로 내부 임시 테이블이 생성된다.


## Select table optimized away

min 혹은 max 만 select 절에 사용되거나 group by로 min, max를 조회하는 쿼리가 인덱스를 오름차순 혹은 내림차순으로 1건만 읽는 형태의 최적화가 적용된다면, Extra 컬럼에 `Select table s optimizeda away` 가 표시.

![[Pasted image 20240123013724.png]]
간단하게 정렬된 레코드에서 처음과 마지막 레코드를 읽어서 가져오는 최적화를 의미함. 
> 단순하게 min 혹은 max만 사용해도 동일하게 표시됩니다. 

## Start temporary, End temporary 

세미 조인 최적화 중에서 Duplicate Weed-out 최적화 전략이 사용되면 mySQL 옵티마이저는 Extra 컬럼에 Start emporary 혹은 End temporary 문구를 표시합니다. 

Duplicate Weed-Out 최적화 전략은 불필요한 중복 레코드를 제거하기 위해 내부 임시테이블을 사용하는데 테이블을 식별할 수 있게 조인의 첫 번째 테이블에 Start temporary문구를 보여주고 조인이 끝나는 부분에 End Temporary문구를 보여줍니다. 


## Unique row not found
두 개의 테이블이 각각 유니크 컬럼으로 아우터 조인을 수행하는 쿼리에서 아우터 테이블에 일치하는 레코드가 존재하지 않을 때 Extra 컬럼에 해당 코멘트가 표시됩니다.


## Using filesort

order by를 처리하기 위해 인덱스를 이용하지 못할 때 서버가 조회된 레코드를 다시 한번 정렬해야 합니다. 이 때 Extra 컬럼에는 Using filesort 코멘트가 표시되며, 조회된 레코드를 정렬용 메모리 버퍼에 복사해 퀵 소트 혹은 힙 소트 알고리즘을 이용해 정렬을 수행합니다.

![[Pasted image 20240123015648.png]]


## Using index(커버링 인덱스)

데이터 파일을 전혀 읽지 않고 인덱스만 읽어서 쿼리를 모두 처리할 수 있을 때 Extra 컬럼에 Using index가 표시됩니다.

인덱스를 이용해 처리하는 쿼리에서 가장 큰 부하를 차지하는 부분은 인덱스 검색에서 일치하는 키 값들의 레코드를 읽기 위해 데이터파일을 검색하는 작업임

![[Pasted image 20240123120704.png]]

Using Index는 인덱스만으로 쿼리를 수행할 수 있을 때 표시됩니다.
이렇게 인덱스만으로 처리되는 것을 커버링 인덱스라고 합니다.

## Using index condition

MySQL 옵티마이저가 인덱스 컨디션 푸시다운 최적화를 사용하면 Extra 컬럼에 Using index condition 메시지가 표시됩니다.
![[Pasted image 20240123121105.png]]

[[RealMySQL8.0 - Chapter9.3#인덱스 컨디션 푸시다운 (index_condition_pushdown)]]


## Using index for group-by

group by 처리를 위해 MySQL 서버는 그루핑 기준 컬럼을 이용해 정렬 작업을 수행하고 다시 정렬된 결과를 그루핑하는 형태의 작업을 필요로 한다.

만약 인덱스를 이용한다면 정렬 없이 그루핑만 수행되기 때문에 효율적이고 빠르게 처리된다. 이런 경우 Extra 컬럼에 Using index for gorup by 메시지가 표시된다.

### 타이트 인덱스 스캔을 통한 Group By 처리

인덱스를 이용해 Group by 절을 처리할 수 있더라도, avg, sum, count 처럼 조회하려는 값이 모든 인덱스를 다 읽어야 할 떄는 필요한 레코드만 듬성듬성 읽을 수가 없습니다. 이러한 쿼리의 경우에는 인덱스를 사용화지만 루스 인덱스 스캔이라고 하지 않는다. 
또한 실행 계획에서도 Using index for group by 가 표시되지 않는다.
![[Pasted image 20240123122132.png]]


### 루스 인덱스 스캔을 통한 group by 처리

단일 컬럼으로 구성된 인덱스에서는 그루핑 컬럼 말고는 아무것도 조회하지 않는 쿼리에서 루스 인덱스 스캔을 사용할 수 있습니다.
![[Pasted image 20240123123735.png]]

참고로 group by에서 인덱스를 사용하려면 우선 group by 조건에서 인덱스를 사용할 수 있는 요건이 갖춰져야 한다. 
또한 where절에서 사용하는 인덱스에 의해서도 group by절의 인덱스 사용 여부가 영향을 받는다.

- where 조건절이 없는 경우
- where 조건절이 있지만 검색을 위해 인덱스를 사용하지 못하는 경우
- where 절의 조건이 있고 검색을 위해 인덱스를 사용하는 경우


where 절의 조건이 검색을 위해 인덱스를 이용하고 group by가 같은 인덱스를 사용할 수 있는 쿼리라도 루스 인덱스 스캔을 사용하지 않을 수 있습니다.

![[Pasted image 20240123124151.png]]
위 쿼리 같은 경우 정해진 범위 내 모든 레코드를 읽는 것이 루스 인덱스 스캔을 사용하는 것 보다 매우 빠르게 처리될 수 있기 때문에 using index for gorup by가 사라진 것을 알 수 있습니다 

## Using index for skip scan

MySQL 옵티마이저가 인덱스 스킵 스캔 최적화를 사용하면 Extra 컬럼에 Using index for skip scan 메시지를 표시함


## Using join buffer(Blog Nested Loop, Batched Key access, hash join)

조인이 수행될 때 드리븐 테이블의 조인 컬럼에 적절한 인덱스가 없다면 MySQL 서버는 블록 네스티드 루프 조인 혹은 해시 조인을 사용합니다.
이 때 실행 계획은 Using join buffer라는 메시지가 표시됩니다.
![[Pasted image 20240123124758.png]]
카테시안 조인을 예시로 들면 항상 조인 버퍼를 사용한다.


## Using MMR

(실행 결과 재현 x)
![[Pasted image 20240123125723.png]]

MySQL 서버는 MMR이라는 최적화를 도입했는데 이는 MySQL 엔진이 여러 개의 키 값을 한 번에 스토리지 엔진으로 전달하고, 스토리지 엔진은 넘겨받은 키 값들을 정렬해서 최소한의 페이지 접근만으로 필요한 레코드를 읽을 수 있게 최적화 한 것입니다.
[[RealMySQL8.0 - Chapter9.3#MRR 배치 키 인덱스 (mrr & batched_key_access)]]


## Usingj sort_union, Using union, Using intersect

쿼리가 index_merge 접근 방법으로 실행되는 경우에는 2개 이상의 인덱스가 동시에 사용될 수 있는데 이때 Extra 컬럼에는 아래 3개 중 하나의 메시지가 선택적으로 출력됩니다.
- Using intersect : and 조건
- Using union: or 조건
- Using sort_union: or 조건 이후 정렬 이후 레코드 읽기
## Using temporary

MySQL 서버에서 쿼리를 처리하는 동안 중간 결과를 담아 두기 위해 임시 테이블을 사용합니다. 이 때 Extra 컬럼에 Using temporary 키워드가 표시되면 임시테이블을 사용한 것입니다.

하지만 사용된 임시 테이블이 메모리인지 디스크인지느 실행 계획만으로 판단할 수 없습니다.
> 임시 테이블이나 버퍼가 메모리에 저장됐는지 확인하는 방법은 MySQl 서버의 상태 변숫값으로 확인할 수 있습니다.


## Using where


MySQL 서버는 MySQL 엔진과 스토리지 엔진 두 레이어로 나눠지는데 스토리지 엔진은 디스크나 메모리상에서 필요한 레코드를 읽거나 저장하는 역할을 하며 MySQL 엔진은 스토리지 엔진으로부터 받은 레코드를 가공 또는 연산하는 작업을 수행합니다 

MySQL엔진 레이어에서 별도의 가공을 해서 필터링 작업을 처리한 경우에만. Extra 컬럼에 Using where 코멘트가 표시됩니다.

![[Pasted image 20240123130804.png]]

emp_no 조건을 만족하는 것은  100건이지만 두 조건을 만족하는 레코드는 37건이다. 이는 스토리지 엔진에서 100개를 읽고 MySQL엔진에 넘겨줬지만 MySQL 엔진은 그중에서 63건의 레코드를 그냥 읽고 필터링해서 버렸다는 의미이다. 여기서 Using where는 63건의 레코드를 버리는 처리를 의미합니다.

## Zero limit
```
mysql> explain select * from employees limit 0;
Empty set (0.00 sec)
```



