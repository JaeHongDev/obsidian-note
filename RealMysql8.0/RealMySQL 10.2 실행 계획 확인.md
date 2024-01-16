---
cssclasses:
  - my_style_width_100
---
# 실행 계획 출력 포맷

MySQL 8.0에서는 Format 옵션을 이용해 실행 계획의 표시 방법을 JSON이나 TREE, 단순 테이블 형태로 선택할 수 있다.

```
EXPLAIN FORMAT=[json | tree] (table의 경우 생략)
```

> 테이블 포맷 형식

![[Pasted image 20240114185415.png]]

> 트리 포맷 형식

![[Pasted image 20240114185729.png]]

> JSON 포맷 형식

![[Pasted image 20240114185900.png]]

EXPLAIN 명령에 사용되는 포맷 옵션별로 개인의 선호도 혹은 표시되는 정보의 차이가 있을 수 있지만 MySQL 옵티마이저가 수집한 실행 계획의 큰 흐름을 보여주는 데는 큰 차이가 없습니다.
-> 보여지는 정보의 차이는 존재하지만 각 실행 계획의 의도를 이해하는데는 크게 상관없다(?)

## 쿼리의 실행 시간 확인

MySQL 8.0.18 버전부터는 쿼리의 실행 계획과 단계별 소요된 시간 정보를 확인할 수 있는 EXPLAIN analyze 기능이 추가됐습니다.  이 기능은 Explain format=tree와 동일한 명령어다.

![[Pasted image 20240114191429.png]]

```mysql
EXPLAIN: 
A -> Table scan on <temporary>  (actual time=4.17..4.2 rows=181 loops=1)
    B -> Aggregate using temporary table  (actual time=4.17..4.17 rows=181 loops=1)
        C -> Nested loop inner join  (cost=667 rows=125) (actual time=0.326..3.37 rows=1066 loops=1)
         D   -> Index lookup on e using ix_firstname (first_name='Matt')  (cost=214 rows=233) (actual time=0.307..0.853 rows=233 loops=1)
         E   -> Filter: ((s.salary > 50000) and (s.from_date <= DATE'1999-01-01') and (s.to_date > DATE'1990-01-01'))  (cost=0.98 rows=0.538) (actual time=0.00658..0.00995 rows=4.58 loops=233)
         F       -> Index lookup on s using PRIMARY (emp_no=e.emp_no)  (cost=0.98 rows=9.68) (actual time=0.00539..0.00771 rows=9.53 loops=233)
```

Tree 포맷의 실행 계획에서 들여쓰기는 호출 순서를 의미하며, 실제 실행 순서는 다음 기준으로 읽으면 됩니다.
 - 들여쓰기가 같은 레벨에서는 상단에 위치한 라인이 먼저
 - 들여쓰기가 다른 레벨에서는 가장 안쪽에 위치한 라인이 먼저

D -> E -> F -> C -> B -> A 순서로 쿼리가 실행됩니다. 

1. employees 테이블에 ix_firstnam 인덱스를 통해 first_name = 'Matt' 조건에 일치하는 레코드를 찾음
2. pk 를 통해 emp_no 와 동일한 레코드를 찾음
3. 조인 조건과 일치하는 건만 가져온 다음
4. 임시 테이블에 결과를 저장하면서 group by 집계를 실행하고
5. 임시 테이블의 결과를 읽어서 결과를 반환함

Explain analyze 명령의 결과에는 단계별로 소요된 시간과레코드 건수, 반복 횟수가 표시됨

- actual time=0.000539..0.000771  테이블에서 일치하는 레코드를 검색하는데 걸린 시간(밀리초)를 의미함, 처음 숫자는 첫 레코드를 가져오는 데 걸린 평균 시간, 두 번째 숫자 값은 마지막 레코드를 가져오는 데 걸린 평균 시간을 의미함
- rows : employees 테이블에서 읽은 emp_no에 일치하는 salaries 테이블의 평균 레코드 건수
- loops: 테이블에서 읽은 emp_no를 이용해 salaries 테이블의 레코드를 찾는 작업이 반복된 횟수 (테이블에서 읽은 레코드의 개수와 동일함)


> 이해를 돕기 위한 추가 설명 
	평균 시간, 평균 레코드 건수 라고 하는 이유는 loops 필드의 값이 1이상이기 떄문입니다. 
	이는 salraies 테이블에서 emp_no 일치 건수를 찾는 작업을 233번 반복해서 실행했는데, 매번 salaries 테이블에서 첫 번째 레코드를 가져오는데 평균 0.007밀리초가 걸렸으며, 마지막 레코드를 읽는데 평균 0.009초가 걸린 것을 의미합니다.

> ⚠ 주의
> Explain Analyze는 실제 쿼리를 실행하고 사용된 실행 계획이기 때문에 실행시간이 오래 걸리는 쿼리의 경우 가급적 사용하는 것을 자제하는 것이 좋습니다.
> 그렇기에 먼저 Explain으로 쿼리 실행 계획을 보고 튜닝한 다음 실행하는 것을 추천합니다

### 🤔 왜 F가 제일 먼저 실행되는게 아닌가요?


# 실행 계획 분석

EXPLAIN 포맷이 tree든 json보다는 실행 계획이 어떤 접근 방법을 사용해서 어떤 최적화를 수행하는지, 그리고 어떤 인덱스를 사용하는지 등을 이해하는 것이 더 중요합니다.
기존 테이블 포맷이 바뀌든 아니든 실행계획을 이해할 수 있다면 포맷이 바뀌어도 어렵지 않게 실행 계획을 이해할 수 있기 때문입니다.
![[Pasted image 20240115002446.png]]

실행 계획의 결과를 보면 위쪽에서 부터 아래쪽으로 실행되는 쿼리의 순서입니다. 출력된 실행 계획에서 위쪽 결과일수록 쿼리의 바깥 부분이거나 먼저 접근한 테이블이고, 아래쪽에 출력된 결과일수록 쿼리의 안쪽 부분 또는 나중에 접근한 테이블에 해당합니다.

> ⚠ 주의
> 상관 서브쿼리 혹은 UNION의 경우 실행 순서대로 표시되지 않을 수 있습니다.

## id 컬럼

아래의 쿼리처럼 하나의 select쿼리는 1개 이상의 서브 select 문장을 포함할 수 있습니다.
```mysql
select ...
from (select ... from tb_test1) tb1, tb_test2 tb2 
 where tb1.id = tb2.id
```
위 쿼리를 다시 아래의 쿼리 처럼 나눠서 생각할 수 있습니다.
```
select ... from tb_test1
select ... from tb_test2 where tb1.id = tb2.id
```
이렇게 select 키워드로 구분한 것을 단위 쿼리 라고 표현합니다.

실행 계획에서 가장 왼쪽에 표시되는 id 컬럼은 단위 select 쿼리별로 부여되는 식별자 값으로 위 쿼리는 실행 계획에서 최소 2개의 id값이 표시됩니다.
하나의 쿼리안에 여러개의 테이블을 조인하면 조인되는 테이블의 개수만큼 실행 계획 레코드가 출력되지만 같은 id값이 부여됩니다.

![[Pasted image 20240115003448.png]]

위 예시쿼리를 보면 employees와 salaraies를 조인하는 쿼리로 실제 같은 id값이 부여되는 것을 알 수 있다.
![[Pasted image 20240115003710.png]]

위 쿼리 예시를 보면 조인을 하지 않는 서로 다른 세가지 종류의 쿼리 실행 계횡르 보면 각각의 id값이 다른 것을 알 수 있습니다.

> ⚠ 중요
> 
> 여기서 id값이 순서대로 정렬된 것이 아닌데 이는 id값이 쿼리의 실행 순서를 의미하는 것은 아니다. 단순히 쿼리의 식별값을 의미하기 때문이다.

![[Pasted image 20240115004045.png]]

이전 쿼리 예시를 보면 실행 게획의 출력 순서대로 먼저 실행되는 순서로 나열된다고 이야기 했습니다.  하지만 위 쿼리는 employees 테이블을 먼저 읽고, 그 결과를 이용해 dept_emp 테이블을 읽는 순서로 실행됩니다.

```mysql
-> Filter: (de.dept_no = (select #2))  (cost=4048 rows=33114)  
    -> Table scan on de  (cost=4048 rows=331143)  
    -> Select #2 (subquery in condition; run only once)  
        -> Limit: 1 row(s)  (cost=1.2 rows=1)  
            -> Covering index lookup on e using ix_lastname_firstname (last_name='Facello', first_name='Georgi')  (cost=1.2 rows=2)
```

> run only once 에 대한 설명 없으면 다시 찾기

위 설명처럼 쿼리 실행 순서가 혼란스러운 경우 format=tree로 변경해서 보면 더 정확하게 알 수 있는데 여기서 `SELECT #2`부분이 가장 안쪽 depth인 것을 알 수 있습니다. 즉 이 쿼리는 employees 테이블이 가장 먼저 조회되고, 그 결과를 이용해 dept_emp 테입르을 조회합니다.


## select_type 컬럼

select_type 컬럼은 단위 쿼리가 어떤 유형인지 표시되는 컬럼으로 총 12개의 유형이 있습니다.
- SIMPLE
- PRIMARY
- UNION
- DEPENDENT UNION
- UNION RESULT
- SUBQUERY
- DEPENDENT SUBQUERY
- DERIVED 
- DEPENDENT DERIVED
- UNCACHEABLE SUBQUERY
- UNCACHEABLE UNION
- MATERIALIZED

### SIMPLE 
UNION이나 서브쿼리를 사용하지 않는 단순한 SELECT 쿼리인 경우 해당 쿼리 문장의 select_type은 simple로 표시된다.
일반적으로 제일 바깥 select 쿼리의 select_type이 simple로 표시됩니다.

Simple [`SELECT`](https://dev.mysql.com/doc/refman/8.0/en/select.html "13.2.13 SELECT Statement") (not using [`UNION`](https://dev.mysql.com/doc/refman/8.0/en/union.html "13.2.18 UNION Clause") or subqueries)


### PRIMARY
UNION 혹은 서브쿼리를 가지는 SELECT 쿼리의 실행 계획에서 가장 바깥쪽에 있는 단위 쿼리는 select_type이 primary로 표시됩니다.
SIMPLE 유형과 동일하게 하나만 존재합니다.


### UNION 

UNION으로 결합하는 단위 SELECT 쿼리 가운데 첫 번째를 제외한 두 번째 이후 단위 SELECT 쿼리의 select_type이 UNION으로 표시됩니다.

![[Pasted image 20240115011243.png]]

실행 결과를 보면 맨 처음은 PRIMARY로 union 혹은 서브쿼리를 포함한 가장 바깥쪽에 있기 때문에 primary로 표시됩니다.
두 번째 실행 결과는 3~4번째 실행 결과를 저장하는 임시 테이블(derivied)이 select_type으로 표시됩니다.
이후 3~4번째 쿼리는 UBION으로 표시됩니다.

### DEPENDENT UNION

DEPENDENT UNION select type 또한  UNION select type와 같이 union, union all 로 집합을 결합하는 쿼리에서 표시됩니다.
여기서 DEPENDENT 는 union, union all로 결합된 단일 쿼리가 외부 쿼리에 의해 영향을 받는 것을 의미합니다.

![[Pasted image 20240115013745.png]]

위 쿼리를 보면 서브쿼리가 먼저 실행될 것 처럼 보인다. 하지만 옵티마이저는  IN 내부의 서브쿼리를 먼저 처리하지 않고, 외부의 employees 테이블을 먼저 읽은 다음 서브쿼리를 실행하는데 이때 employees 테이블의 컬럼값이 서브쿼리에 영향을 준다.

```
-> Filter: <in_optimizer>(e1.emp_no,<exists>(select #2))  (cost=30224 rows=299920) (actual time=6.32..2295 rows=233 loops=1)  
    -> Table scan on e1  (cost=30224 rows=299920) (actual time=0.0662..190 rows=300024 loops=1)  
    -> Select #2 (subquery in condition; dependent)  
        -> Limit: 1 row(s)  (cost=3.02..3.02 rows=0.1) (actual time=0.00625..0.00625 rows=777e-6 loops=300024)  
            -> Table scan on <union temporary>  (cost=3.02..3.02 rows=0.1) (actual time=0.00596..0.00596 rows=777e-6 loops=300024)  
                -> Union materialize with deduplication  (cost=0.52..0.52 rows=0.1) (actual time=0.00551..0.00551 rows=777e-6 loops=300024)  
                    -> Limit table size: 1 unique row(s)  
                        -> Limit: 1 row(s)  (cost=0.255 rows=0.05) (actual time=0.00249..0.00249 rows=777e-6 loops=300024)  
                            -> Filter: (e2.first_name = 'Matt')  (cost=0.255 rows=0.05) (actual time=0.00222..0.00222 rows=777e-6 loops=300024)  
                                -> Single-row index lookup on e2 using PRIMARY (emp_no=<cache>(e1.emp_no))  (cost=0.255 rows=1) (actual time=0.00174..0.0018 rows=1 loops=300024)  
                    -> Limit table size: 1 unique row(s)  
                        -> Limit: 1 row(s)  (cost=0.255 rows=0.05) (actual time=0.00252..0.00252 rows=0 loops=299791)  
                            -> Filter: (e3.last_name = 'Matt')  (cost=0.255 rows=0.05) (actual time=0.00225..0.00225 rows=0 loops=299791)  
                                -> Single-row index lookup on e3 using PRIMARY (emp_no=<cache>(e1.emp_no))  (cost=0.255 rows=1) (actual time=0.00179..0.00185 rows=1 loops=299791)
```

결국 실제로 외부 쿼리가 내부 쿼리에 영향을 주는 서브쿼리가 아닌 것 처럼 보이지만 employees 테이블을 먼저 스캔한 다음 내부적으로 UNION에 사용된 select 쿼리의 where 조건에 e2.emp_no = e1.emp_no와 같은 조건이 자동으로 추가되어 실행된다.

그렇기에 외부에 정의된 employees 테이블의 emp_no 컬럼이 서브 쿼리에 사용되기 때문에 dependent union이 select_type에 표시된 것이다 

```
SELECT 
  e1.emp_no AS emp_no,
  e1.birth_date AS birth_date,
  e1.first_name AS first_name,
  e1.last_name AS last_name,
  e1.gender AS gender,
  e1.hire_date AS hire_date
FROM 
  employees.employees e1
WHERE 
  e1.emp_no IN (
    SELECT 
      e2.emp_no 
    FROM 
      employees.employees e2 
    WHERE 
      (e2.first_name = 'Matt' AND e1.emp_no = e2.emp_no)
    UNION
    SELECT 
      e3.emp_no 
    FROM 
      employees.employees e3 
    WHERE 
      (e3.last_name = 'Matt' AND e1.emp_no = e3.emp_no)
  );

```
show warnings 명령어로 조회한 실제 쿼리에서 방금 이야기 했던 조건이 추가된 것을 확인할 수 있습니다.


### UNION RESULT
UNION RESULT는 UNION 결과를 담아두는 테이블입니다.
8.0 이전에는 UNION ALL의 경우 임시테이블을 사용했지만 현재는 사용하지 않도록 개선했습니다. 하지만 여전히 (UNION, UNION DISTINCT) 임시 테이블에 결과를 버퍼링하며 실행 계획상에 이 임시 테이블을 가리키는 라인의 select_type이 union result인 것을 알 수 있습니다.
참고로 UNION RESULT는 실제 쿼리에서 단위 쿼리가 아니기 때문에 별도의 id값은 부여되지 않습니다.

만약 UNION DISTINCT가 아닌 UNION ALL을 사용하면 UNION RESULT를 하지 않는 것을 알 수 있습니다.

#### 🤔 UNION RESULT  버그 의심
![[Pasted image 20240115021527.png]]

책에서 제공하는 예시를 보면 id가 3인 것을 알 수 있습니다. 

> The [`SELECT`](https://dev.mysql.com/doc/refman/8.0/en/select.html "13.2.13 SELECT Statement") identifier. This is the sequential number of the [`SELECT`](https://dev.mysql.com/doc/refman/8.0/en/select.html "13.2.13 SELECT Statement") within the query.
  The value can be `NULL` if the row refers to the union result of other rows. In this case, the `table` column shows a value like ``<union_`M`_,_`N`_>`` to indicate that the row refers to the union of the rows with `id` values of _`M`_ and _`N`_.

MySQL 공식문서에 따르면 id 컬럼이 null인 경우 table 컬럼에 <union_m, n> 형식으로 표기된다고 명시돼 있습니다.
하지만 id는 3으로 표현돼 있습니다. 

```mysql
-- 첫 번째 쿼리
SELECT
  e1.emp_no AS emp_no
FROM
  employees.salaries e1
WHERE
  e1.salary > 100000
UNION
-- 두 번째 쿼리
SELECT
  e2.emp_no AS emp_no
FROM
  employees.dept_emp e2
WHERE
  e2.from_date > DATE '2000-01-01';

```

show warnings 의 결과에서도 id가 3인 결과를 사용하지 않는 것으로 알 수 있습니다.

### SUBQUERY

일반적으로 서브쿼리라고 하면 여러 가지를 통틀어서 이야기할 때가 많은데 select_ ype의 <u>subquery는 from 절 이외에서 사용되는 서브쿼리만을 의미합니다. </u>
![[Pasted image 20240115023919.png]]

MySQL 서버의 실행 계획에서 FROM 절에 사용된 서브쿼리는 select_type이 DERIVED로 표시되고, 그 밖의 위치에서 사용된 서브쿼리는 전부 SUBQUERY로 표시된다. 

#### 서브쿼리의 다른 이름
서브쿼리는 사용하는 위치에 따라 각기 다른 이름을 가집니다.
- 중첩된 쿼리 (Nested Query) : Select되는 컬럼에 사용된 서브쿼리를 네스티드 쿼리라고 합니다.
- 서브쿼리: WHERE 절에 사용된 경우에는 일반적으로 서브쿼리라고 합니다.
- 파생테이블: FROM 절에 사용된 서브쿼리를 MySQL에서는 파생 테이블이라고 하며, 일반적으로 RDBMS에서는 인라인 뷰 혹은 서브 셀렉트라고 부릅니다.
서브쿼리가 반환하는 값의 특성에 따라 다음과 같이 구분합니다.
- 스칼라 서브쿼리: 하나의 값만 반환하는 쿼리
- 로우 서브쿼리: 컬럼의 개수와 관계없이 하나의 레코드만 반환하는 쿼리


### DEPENDENT SUBQUERY
서브쿼리가 바깥쪽 select 쿼리에서 정의된 컬럼을 사용하는 경우 select_type에 dependent_subquery라고 표시됩니다.
![[Pasted image 20240115024414.png]]

위 쿼리는 안쪽의 서브쿼리 결과가 바깥쪽 select 쿼리의 컬럼에 의존적이기 때문에 dependent라는 키워드가 붙습니다.
또한 dependent union과 같이 dependent subquery 또한 외부 쿼리가 먼저 수행된 후 내부 쿼리가 실행돼야 하므로 일반 서브쿼리보다는 처리속도가 느립니다.


### DERIVED

DERIVED는 단위 select 쿼리의 실행 결과로 메모리나 디스크에 임시 테이블을 생성하는 것을 의미합니다.
select_type이 deverived 인 경우에 생성되는 임시 테이블을 파생 테이블이라고 부릅니다. 또한 MySQL 5.5 버전까지는 파생 테이블에는 인덱스가 없기 때문에 다른 테이블과 조인할 때 성능상 불리할 때가 많습니다.
그러나 MySQL5.6 버전 부터는 옵티마이저 옵션에 따라 쿼리의 특성에 맞게 임시 테이블에도 인덱스를 추가해서 만들 수 있게 최적화 됐습니다.

![[Pasted image 20240115030940.png]]

> ⚠ 주의점
> 
> 위 쿼리는 서브쿼리를 제거하고 조인으로 처리할 수 있는 형태입니다.
> 
> MySQL 서버가 업그레이드 되면서 파생테이블에 대한 최적화가 진행되었지만 한계가 있기에  최적화된 쿼리를 작성해야한다.

### DEPENDENT DERIVED
MySQL 8.0 이전 버전에서 FROM 절의 서브쿼리는 외부 컬럼을 사용할 수 없었는데, MySQL 8.0 버전부터 래터럴 조인 기능이 추가되면서 FROM 절의 서브쿼리에서도 외부 컬럼을 참조할 수 있게 됐습니다.
![[Pasted image 20240115031832.png]]

> 래터럴 조인에 대한 자세한 이야기는 11절에서 확인

### UNCACHEDABLE SUBQUERY

하나의 쿼리 문장에 서브쿼리가 하나만 있더라도 실제 그 서브쿼리가 한 번만 실행되는 것은 아닙니다. 
간혹 조건이 똑같은 서브쿼리가 실행될 때가 있는데 이런 상황에서 MySQL에서는 이전 실행 결과를 그대로 사용할 수 있게 서브쿼리의 결과를 내부적인 캐시 공간에 담아둡니다. ( 쿼리 캐시 혹은 파생 테이블과는 관련없는 기능)

![[Pasted image 20240115032327.png]]
서브쿼리는 바깥쪽의 영향을 받지 않으므로 처음 한 번만 실행해서 그 결과를 캐시하고 필요할 때 결과를 이용합니다. 
위 그림은 select_type이 서브쿼리인 경우 캐시를 사용하는 방법입니다. 쿼리 실행 결과가 처음 한 번만 생성되고 이후 해당 캐시값을 사용합니다.

DEPENDENT SUBQUERY는 의존하는 바깥쪽 쿼리의 컬럼의 값 단위로 캐시해두고 상합니다.
서브쿼리의 캐시와 다른 점은 딱 한 번만 캐시되는 것이 아닌 외부 쿼리의 값 단위로 캐시가 만들어지는 방식으로 처리됩니다.
둘의 차이점은 이 캐시를 사용할 수 있느냐 없느냐에 따라 차이가 있습니다.

만약 서브쿼리의 요소로 인해 캐시할 수 없는 경우에는 UNCACHEABLE SUBQUERY로 표시됩니다.
- 사용자 변수가 서브쿼리에 사용된 경우
- NOT_DETERMINSTIC 속성의 스토어드 루틴이 서브쿼리 내 사용된 경우
- UUID혹은 RAND와 같이 결괏값이 호출할 댸마다 달라지느 함수가 서브쿼리에 사용된 경우

아래 쿼리는 사용자 변수가 사용된 쿼리로 캐시를 사용할 수 없는 쿼리다. 
![[Pasted image 20240115032940.png]]



## table 컬럼

MySQL 서버의 실행 계획은 단위 SELECT 쿼리 기준이  아닌 테이블 기준으로 표시됩니다.

 ![[Pasted image 20240115161440.png]]

 처음 쿼리는 테이블이 존재하지 않으며 두 번째 쿼리는 DUAL이라는 테이블이 사용됐습니다. 실제 DUAL이라는 테이블은 없지만 쿼리는 오류를 발생시키지 않습니다.
옵티마이저는 from dual 부분을 제거하고 처음 쿼리처럼 처리하는데 show warnings를 보면 그 결과를 확인할 수 있습니다.

처음 쿼리와 두 번째 쿼리의 실행 계획을 보면 table이 null인 것을 알 수 있습니다. 이는 별도의 테이블을 사용하지 않는 select 쿼리인 경우에 table 컬럼이 null로 표시됩니다.
![[Pasted image 20240115162024.png]]\

만약 table 컬럼이  `< >` 로 둘러싸인 이름의 경우에는 임시테이블을 사용하는 것을 의미합니다. `< >` 로 표시되는 숫자는 단위 select 쿼리의 id 값을 지칭합니다. 
![[Pasted image 20240115030940.png]]

단위 select 쿼리의 id 값이 2인 실행계획으로 부터 만들어진 파생 테이블을 가리킵니다. 

```mysql
-> Nested loop inner join  (cost=215795 rows=310787) (actual time=218..930 rows=300024 loops=1)  
    -> Table scan on tb  (cost=98043..101930 rows=310787) (actual time=218..283 rows=300024 loops=1)  
        -> Materialize  (cost=98043..98043 rows=310787) (actual time=218..218 rows=300024 loops=1)  
            -> Group (no aggregates)  (cost=66964 rows=310787) (actual time=0.0401..181 rows=300024 loops=1)  
                -> Covering index scan on de using ix_empno_fromdate  (cost=33850 rows=331143) (actual time=0.0363..102 rows=331603 loops=1)  
    -> Single-row index lookup on e using PRIMARY (emp_no=tb.emp_no)  (cost=0.25 rows=1) (actual time=0.00177..0.00183 rows=1 loops=300024)
```

## partitions 컬럼

MySQL 5.7 버전까지는 옵티마이저가 사용하는 파티션들의 목록은 Explain Parition 명령을 이용해 확인 가능했으며 현재는 Explain 명령으로 파티션 관련 실행 게획까지 모두 확인할 수 있게 변경됐습니다.

(이부분은 이후 RealMySQL8.0 2권보고 확인해볼 예정)

## type 컬럼

쿼리의 실행 계획에서 type 이후의 컬럼은 MySQL 서버가 각 테이블의 레코드를 인덱스를 사용하거나, 테이블을 처음부터 끝까지 읽는 풀 테이블 스캔으로 읽었는지를 나타냅니다. 

MySQL에서는 하나의 테이블로부터 레코드를 읽는 작업도 조인처럼 처리합니다. 그래서 메뉴얼에서는 type 컬럼을 조인 타입으로 소개합니다.
그렇기에 type 컬럼은 조인 여부를 생각하는 것이 아닌 각 테이블의 접근 방법으로 해석하면 됩니다.

실행 계획의 type 컬럼에 표시될 수 있는 값은 다음과 같습니다.
- system
- const
- eq_ref
- ref
- fulltext
- ref_or_null
- unique_subquery
- index_subquery
- range
- index_merge
- index
- all

all 을 제외한 나머지는 모두 인덱스를 사용한 접근 방법이며 all은 인덱스를 사용하지 않고 ,테이블을 처음부터 끝까지 읽어서 레코드를 가져오는 풀 테이블 스캔 접근 방법을 의미한다. 
참고로 위 순서는 각 접근 방법 중 성능이 빠른 순서로 나열된 것입니다.


### SYSTEM
레코드가 1건만 존재하는 테이블 혹은 한 건도 존재하지 않는 테이블을 참조하는 형태의 접근 방법을 system이라고 합니다.
주로 MyISAM 혹은 MEMORY 테이블에서만 사용되는 접근 방법입니다.

### const

테이블의 레코드 건수와 관계없이 쿼리가 프라이머리 키나 유니크 키 컬럼을 이용한 where 조건절을 가지고 있으며, 반드시 1건을 반환하는 쿼리의 처리 방식을 const라고 합니다.
![[Pasted image 20240115211156.png]]

> ⚠ 주의
> 
> 만약 다중 컬럼으로 구성된 프라이머리 카 혹은 유니크 키 중에서 인덱스의 일부 컬럼만 조건으로 사용할 떄는 const타입의 접근 방법을 사용할 수 없습니다.

### eq_ref
eq_ref 접근 방법은 여러 테이블이 조인되는 쿼리의 실행 계획에서만 표시됩니다. 
조인에서 처음 읽은 테이블의 컬럼값을, 그다음 읽어야 할 테이블의 프라이머리 키나 유니크 키 컬럼의 검색 조건에 사용할 떄를 가리켜 eq_ref라고 합니다.
![[Pasted image 20240115211818.png]]

만약 유니크 키로 검색할 때 그 유니크 인덱스가 not null이 아닌 경우 혹은 다중 컬럼으로 만들어진 프라이머리키나 유니크 인덱스를 사용할 때 모든 컬럼이 비교 조건에 사용돼지 않는다면 eq_ref접근 방법을 사용할 수 없습니다.

정리하면 조인에서 두 번째 이후에 읽는 테이블에서 반드시 1건만 존재한다는 보장이 있어야 사용할 수 있는 접근 방법입니다.


### ref
ref 접근 방법은 eq_ref와 달리 조인의 순서와 관계없이 사용되며, 프라이머리 키 혹은 유니크 키 등의 제약조건도 없습니다.
단순히 동등조건을 사용하는 경우에 적용되는 타입으로 여타 다른 조건보다는 빠른 레코드 조회 방법중 하나입니다.

이전까지 살펴본 ref, eq_ref, const는 좋은 접근 방법으로 인덱스의 분포도가 나쁘지 않다면 성능상의 문제를 일으키지 않는 접근 방법입니다.


### fulltext

fulltext 접근 방법은 MySQL 서버의 전문 검색 인덱스를 사용해 레코드를 읽는 접근 방법입니다.

이부분은 전문 검색을 사용할 때가 아니면 볼일이 거의 없기 때문에 책의 예시 (440p)를 참고하자.

### ref_or_null

이 접근 방법은 ref 접근 방법과 같은데, null 비교가 추가된 형태입니다. 
![[Pasted image 20240115212745.png]]

실제로 많이 활용되지 않지만, 나쁘지 않은 접근 방법 입니다.

### unique_subquery

where 조건절에서 사용될 수 있는 IN형태(subquery)의 쿼리를 위한 접근 방법입니다. 
unique_subquery 이름 그대로 서브쿼리에서 중복되지 않는 유니크한 값만 반환할 때 이 접근 방법을 사용합니다.
![[Pasted image 20240115213009.png]]

실제 실행 계획에서는 unique_subquery가 보이지 않는다 이는  IN(subquery) 형태의 세미조인을 최적화 했기 때문에 다르게 보이는 것으로 semijoin 옵션을 끄게 될 경우 아래와 같이 보인다.
![[Pasted image 20240115213551.png]]

책 예시랑 다른데..?


### index_subquery

IN 연산자 특성상 IN (서브쿼리) 혹은 IN(상수 나열) 형태의 조건은 괄호 안에 있는 값의 목록에서 종복된 값이 먼저 제거돼야 합니다.

union_subquery 접근 방법은 IN(subquery) 조건의 서브쿼리가 중복된 값을 만들어내지 않는다는 보장이 있으므로 별도의 중복을 제거할 필요가 없다. 
하지만 in 서브쿼리에서 중복된 값이 발생할 수 있는데 이때 index_subquery 접근 방법이 사용된다.

### range
range는 인덱스 레인지 스캔 형태의 접근 방법입니다. range는 인덱스를 하나의 값이 아니라 범위 검색하는 경우를 의미하는데 
- <, >
- is null
- between
- in
- like
등의 연산자를 이용해 인덱스를 검색할 때 사용됩니다.
range 접근 방법이 앞서 설명한 쿼리보다 성능은 떨어지지만 나쁘지 않은 쿼리이다. 
![[Pasted image 20240115234617.png]]


### index_merge 
index_merge 접근 방법은 2개 이상의 인덱스를 이용해 각각의 검색 결과를 만들어낸 후, 그 결과를 병합해서 처리하는 방식입니다.

index_merge는 
- 여러 인덱스를 읽어야 하므로 일반적으로 Range 접근 방법보다 효율성이 떨어진다.
- 전문 검색 인덱스를 사용하는 쿼리에서는 index_merge가 작동하지 않는다.
- 해당 접근 방법으로 처리도니 결과는 항상 2개 이상의 집합이 되기 때문에 그 두 집합의 교집합이나 합집합 또는 중복 제거와 같은 부가적인 작업이 더 필요하다.
이런 특징 때문에 이름만큼 효율적으로 동작하는 것은 아닙니다. 

![[Pasted image 20240115235417.png]]



### index 

index 접근 방식은 인덱스를 처음부터 끝까지 읽는 인덱스 풀 스캔을 의미합니다. 이는 range 접근 방법과 같이 효율적으로 인덱스의 필요한 부분만 읽는 것을 의미하는 것은 아닙니다.
이 방법은 처음부터 끝까지 읽는 풀 테이블 스캔 방식과 비교했을 때 비교하는 레코드 건수는 같지만 일반적으로 데이터 파일 전체보다 크기가 작으므로 인덱스 풀 스캔시 풀 테이블 스캔보다 빠르게 처리되며, 쿼리의 내용에 따라 정렬된 인덱스의 장점을 이용할 수 있으므로 훨씬 효율적입니다.

아래 조건을 만족하는 경우 Index 접근 방식을 이용합니다.
1. range나 const,ref 같은 접근 방법으로 인덱스를 사용하지 못하는 경우
2. 인덱스에 포함된 컬럼만으로 처리할 수 있는 쿼리인 경우
3. 인덱스를 이용해 정렬이나 그루핑 작업이 가능한 경우

![[Pasted image 20240115235929.png]]

### ALL

마지막으로 흔히 알고있는 풀 테이블 스캔을 의미하는 접근 방법입니다. 
테이블을 처음부터 끝까지 읽어 불필요한 레코드를 제거하고 반환하기에 가장 마지막에 선택해야하는 비효율적인 방법입니다.

InnoDB는 리드 어헤드라고 부르는 작업을 통해 한 번에 여러 페이지를 읽어서 처리할 수 있습니다. 

> ℹ 참고
> 일반적으로 index와 all 접근 방법은 작업 범위를 제한하는 조건이 아니므로 빠른 응답을 사용자에게 보내야 하는 웹 서비스 등과 같은 온라인 트랜잭션 처리 환경에는 적합하지 않습니다.


## possible_keys 컬럼

단순하게 사용될법했던 인덱스의 목록입니다. 

![[Pasted image 20240116000549.png]]
해당 쿼리에서 emp_no 즉 pk만 인덱스를 활용할 수 있고 first_name을 활용할 수 있습니다. 

즉 단순하게 쿼리 인덱스를 사용 가능한 목록이기 때문에 무시해도 크게 문제되지 않습니다.


## key 컬럼
key 컬럼에 표시되는 인덱스는 최종 선택된 실행 계획에서 사용하는 인덱스를 의미합니다.
그렇기에 쿼리를 튜닝할 때는 key 컬럼에 의도했던 인덱스가 표시되는지 확인하는 것이 중요하다. 

## KEY_LEN 컬럼
key_ken 컬럼은 같은 쿼리를 처리하기 위해 다중 컬럼으로 구성된 인덱스에서 몇 개의 컬럼까지 사용했는지 알려주는 역할을 합니다.
더 정확하게는 몇 바이트까지 사용했는지 알려주는 지표입ㅈ니다.

![[Pasted image 20240116000907.png]]
현재 char(4)인 dept_no 컬럼을 사용했다. 이는 실행 결과에서 16바이트와는 조금 거리가 있는다. mysql에서 utf8mb4문자를 위해 메모리 공간을 1당 4바이트로 계산하기 때문에 16바이트로 표시된 것입니다.

![[Pasted image 20240116001158.png]]
추가로 날짜가 인덱스에 들어갈 경우 4로 표시된다. 원래 MySQL은 날짜의 경우 3바이트를 사용하는데 이는 null을 포함하기 때문이다. 그렇기에 3+1로 4바이트를 사용하는 것입니다.

## ref 컬럼

접근 방법이 ref면 참조 조건으로 어떤 값이 제공됐는지 보여준다. 만약 상숫값을 지정했다면 ref 칼럼의 값은 const로 표시되고, 다른 테이블의 컬럼값이면 그 테이블명과 칼럼값이 표시된다.


간혹 쿼리의 실행 계획에서 ref 컬럼의 값이 func라고 표시될 때가 있습니다. 이는 Function의 줄임말로 콜레이션 변환이나 값 자체의 연산을 겨처서 참조됐다는 것을 의미합니다.

![[Pasted image 20240116110823.png]]

employees테이블에서 dept_emp를 읽을 때 emp_no 값에서 1을 뺀 값으로 조인하기 때문에 func라고 표기됩니다.
