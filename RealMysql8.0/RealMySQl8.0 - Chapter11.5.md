
insert 문장이 동시에 실행되는 경우 insert문장 자체보다는 테이블의 구조가 성능에 더 큰 영향을 미칩니다. 
그렇기 때문에 insert문장으로 발생하는 성능과 select의 성능을 동시에 빠르게 만들 수 있는 테이블 구조는 없습니다.
(반정규화)


#  Insert 
 
insert 문장에도 다음과 같은 고급 기능을 지원합니다. 
- insert ignore
- insert on duplicate key update 
> 위 두 기능은 유티크 인덱스, 프라이머리 키에 대해 중복 레코드를 어떻게 처리할지를 결정함


## INSERT IGNORE

insert 문장의 ignore 옵션은 저장하는 레코드의 프라이머리 키나 유니크 인덱스 컬럼의 값이 이미 테이블에 존재하는 레코드와 중복되는 경우, 그리고 저장하는 레코드의 컬럼이 테이블의 컬럼과 호환되지 않는 경우 모두 무시하고 다음 레코드를 처리할 수 있게 해줍니다. 

```

INSERT IGNORE INTO salaries (emp_no, salary, from_date, to_date) 
VALUES  
(10001, 60117, '1986-06-26', '1987-06-26'),
(10001, 62102, '1987-06-26', '1988-06-25'),
(10001, 66074, '1988-06-25', '1989-06-25'),
(10001, 66596, '1989-06-25', '1990-06-25'),
(10001, 66961, '1990-06-25', '1991-06-25');

INSERT IGNORE INTO salaries   SELECT emp_no, (salary+100), '2020-01-01', '2022-01-01'   FROM salaries WHERE to_date>='2020-01-01';

```

![[Pasted image 20240226132231.png]]
![[Pasted image 20240226132335.png]]
결과를 보면 중복되는 레코드의 삽입이 안되는 것을 알 수 있습니다.

또한 insert ingore는 프라이머리 키와 유니크 인덱스를 동시에 가지고 있는 겨우에 두 인덱스 중 하나라도 중복이 발생하는 레코드에 대해서는 insert를 무시합니다.

## insert ... on duplicate key update

insert ... on duplicate key update 문장은 프라이머리 키나 유니크 인덱스의 중복이 발생하면 update 문장의 역할을 수행합니다.

주로 일별로 집계되는 값을 관리할 때 편리하게 사용할 수 있습니다.

![[Pasted image 20240227121506.png]]

daily_statistic 테이블은 (target_date, stat_name) 프라이머리 키 조합으로 생성돼 있습니다. 

그렇기 때문에 stat_name이 최초로 저장되는 경우에는 insert 문장이 실행되고, on duplicate key update 절 이하의 내용은 무시됩니다.

> 자바 Map의 map.put(key, map.getOrDefault(key, default) + increment));

### insert into  group by  on duplicate key update
아래 쿼리는 group by된 결과를 테이블에 insert합니다.
![[Pasted image 20240227122621.png]]

쿼리에서는 group by 결과 건수를 저장하고 있는데 여기서 on Duplicate key update에서 count를 참조하고 있지만 실제로 동작하는 방법은 아닙니다. 

그렇기에 아래와 같이 values() 를 활용해야 합니다
![[Pasted image 20240227122614.png]]

> values의 동작원리
> 
> values는 컬럼명을 인자로 사용하는데, 입력되는 값을 가져 옵니다. 위 쿼리를 예시로 들면 stat_value에 count함수가 들어가는데 키가 중복되는 경우 기존에 값과  더해져서 저장됩니다. 

현재 values는 deprecated 됐으며 아래와 같이 사용하는 것을 권장합니다.
![[Pasted image 20240227123304.png]]

## Load data 명령 주의 사항

Load data 명령은 RDMBMS에서 데이터를 빠르게 적재할 수 있는 방법입니다.
이는 MySQL 서버의 load data 명령을 내부적으로 MySQL 엔진과 스토리지 엔진의 호출 횟수를 최소화하고 스토리지 엔진이 직접 데이터를 적재하기 때문에 일반적인 insert 명령과 비교했을 때 매우 빠릅니다.

하지만 단점 또한 존재합니다.
1.  저장할 데이터가 많지 않으면 크게 문제가 없지만 데이터가 많은 경우 단일 스레드로 동작하기 때문에 다른 온라인 트랜잭션 쿼리들의 성능에 영향이 갑니다.
2. 마찬가지로 저장할 데이터가 많지 않다면 문제가 없지만 데이터가 많은 경우 단일 트랜잭션에서 발생하는 언둘 로그가 삭제되지 못하고 유지되는데 이는 언두 로그를 디스크로 기록해야 하는 부하를 만들고, 언두 로그로 인한  레코드를 찾는 오버헤드를 만들기도 합니다.


## 성능을 위한 테이블 구조
insert 문장의 성능은 쿼리 문장 자체보다는 구조에 의해 많이 결정됩니다. 
- 대부분 insert 문장은 단일 레코드를 저장하는 형태이므로 insert 문장 자체는 튜닝할 수 있는 부분이 없기 때문입니다. 

### 대량 insert 성능 

수백 수천 건의 레코드를 insert한다면 insert될 레코드들을 프라이머리 키 값 기준으로 미리 정렬해서 insert 문장을 구성하는 것이 성능에 도움이 될 수 있습니다.

> 실제로 테스트 못해봄

Load Data 문장이 레코드를 insert할 때마다 innoDB 스토리지 엔진은 프라이머리 키를 검색해서 레코드가 저장될 위치를 찾습니다. 만약 정렬없이 랜덤하게 덤프된 데이터 파일의 경우에는 각 레코드의 프라이머리 키가 너무 다른 값을 가지는데 이로 인해 innoDB 스토리지 엔진이 레코드를 저장할 때마다 프라이머리 키의 B-Tree에 존재하는 랜덤한 위치의 페이지를 메모리로 읽어와야 하기 때문에 처리가 느립니다.

반면 프라이머리 키로 정렬된 데이터 파일을 적재할 때는 다음에 insert할 레코드의 프라이머리 키 값이 직전에 insert된 값보다 항상 크기 떄문에 메모리에는 프라이머리 키의 마지막 페이지만 적재돼 있으며 새로운 페이지를 메모리로 가져오지 않아도 레코드를 저장할 위치를 찾을 수 있습니다.

### 프라이머리 키 선정

테이블의 프라이머리 키는 insert 성능을 결정하는 가장 중요한 부분입니다. 
- 만약 테이블에 insert되는 레코드가 프라이머리 키의 전체 범위에 대해 프라이머리 키 순서와 무관하게 랜덤하게 저장된다면 MySQL 서버는 레코드를 insert할 때마다 저장될 위치를 찾아야 함


프라이머리 키를 선정할 때 두 가지 요건을 고려해야 합니다.
1. insert 성능
	 - SELECT는 많지 않고 insert가 많은 테이블 
	 - 이 경우 auto increment 패턴의 값을 선택하는 것이 좋습니다. 
	 - 인덱스를 많이 만들지 않는 것이 좋습니다.
1. select 성능
	- SELECT가 빈번하게 실행되는 테이블
	- 이 경우 빈번하게 실행되는 select 쿼리의 조건을 기준으로 프라이머리 키를 선택하는 것이 좋ㅅ브니다.


## Auto-Increment 컬럼
select 보다는 insert에 최적화된 테이블을 생성하기 위해서 두 가지 요소를 갖춰 테이블을 준비해야 합니다.
1. 단조 증가 혹은 단조 감소되는 값으로 프라이머리 키 선정
2. 세컨더리 인덱스 최적화

InnoDB 스토리지 엔진을 사용하는 테이블은 자동으로 프라이머리 키로 클러스터링 됩니다.  
[[RealMySQL8.0 - Chapter8#클러스터링 인덱스]]

![[Pasted image 20240226200314.png]]
위와 같이 자동증가 값을 프라이머리 키로 해시 테이블을 생성하는 것은 MySQL 서버에서 가장 빠른 INSERT를 보장하는 방법입니다.

자동 증가 값의 채번을 위해서는 잠금이 필요한데 이를 AUTO-INC 잠금이라고 합니다.

### AUTO-INC 잠금 
잠금을 사용하는 방식을 변경할 수 있게 innodb_autoinc_lock_mode 시스템 변수를 제공합니다.
총 3가지 모드가 존재하며 다음과 같습니다. 

#### innodb_autoinc_lock_mode = 0
항상 AUTO-INC 잠금을 걸고 한 번에 1씩만 증가된 값을 가져옵니다.  이전 버전과의 호환성을 위하 남겨둠

#### innodb_autoinc_lock_mode = 1
단순히 레코드 한 건씩 insert하는 쿼리에서 Auto-inc 잠금을 사용하지 않고 뮤텍스를 이용해 처리합니다. 

단 하나의 insert 문장에서 여러건의 데이터를 삽입하는 경우 AUTO-INC잠금을 걸고 필요한 만큼의 자동 증가 값을 한꺼번에 가져와서 사용한다.

#### innodb_autoinc_lock_mode = 2
load data나 벌크 insert를 포함한 insert 계열의 문장을 실행할 때 더 이상 AUTO-INC 잠금을 사용하지 않습니다. 
자동 증가 값을 미리 할당받아 처리하는 가장 빠른 방법입니다. 


# UPDATE와 DELETE

## UPDATE ... ORDER BY ... LIMIT N

update와 delete 조건절에 where을 적용해서 삭제하는 경우 많은 데이터를 변경 삭제하게 된다면 다른 커넥션의 쿼리 처리를 방행할 수 있습니다. 
이 때 limit를 이용해 조금씩 잘라서 변경하거나 삭제하는 방법을 사용할 수 있습니다. 

이 방벙은 복제 소스 서버에서 order by ... limit이 포함된 update나 delete 문장을 실행하면 바이너리 로그의 포맷이 statement 기반의 복제에서는 문제가 발생할 수 있습니다. 

![[Pasted image 20240227002620.png]]

이 경우 복제 소스 서버와 레플리카 서버에서 정려된 값의 순서가 다를 수 있기 때문입니다. 물론 프라이머리 키로 정렬하면 문제는 없지만 다른 방식을 사용하는 경우 주의가 필요합니다.

## JOIN UPDATE
두 개 이상의 테이블을 조인해 조인된 결과 레코드를 변경 및 삭제하는 쿼리를 join update라고 합니다. 

일반적으로 join update는 조인되는 모든 테이블에 대해 읽기 참조만 되는 테이블은 읽기 잠금이 걸리고, 컬럼이 변경되는 테이블은 쓰기 잠금이 걸립니다. 그래서 join update 문장이 온라인 트랜잭션 환경에서는 데드락을 유발할 가능성이 있기 떄문에 주의해야 합니다. 

![[Pasted image 20240227002934.png]]

위 쿼리는 tb_test1 테이블과 employees 테이블을 조인 한 다음 employees 테이블의 first_name 컬럼의 값을 tb_test1 테이블의 first_name 컬럼으로 복사하는 join_update문장입니다.

### GROUP BY JOIN UPDATE 
![[Pasted image 20240227003743.png]]

위 쿼리는 부서에 소속된 사원의 수를 저장하기 위한 쿼리입니다. 

하지만 위 쿼리는 실제로 동작하지 않습니다. join update에서는  group by 혹은 Order by 절을 사용할 수 없기 때문입니다. 

그렇기에 서브쿼리를 통한 파생 테이블을 사용해야 합니다. 
![[Pasted image 20240227003914.png]]

위 쿼리는 서브쿼리로 dept_emp 테이블을 dept_no로 그루핑하고, 파생 테이블로 저장했습니다. 
그리고 department테이블고 조인하여 필요한 값을 업데이트 합니다. 

> 일반 테이블과 파생 테이블이 조인될 경우 파생 테이블이 드라이빙 테이블이 됩니다. 
> 
> 물론 옵티마이저가 잘 선택하지만 join_order를 통한 순서를 강제하는 방법도 있습니다. 



## 여러 레코드 update

하나의 update 문장으로 여러 개의 레코드를 없데이트 하는 경우 모든 레코드를 동일한 값으로만 업데이트 할 수 있습니다. 

하지만 8.0 부터 레코드 생성 문법을 이용해  레코드 별로 서로 다른 값을 업데이트 할 수 있습니다. 
![[Pasted image 20240227004052.png]]

`values row(...), row(..)...` 문법을 사용하면 sql 문장 내 임시 테이블을 생성할 수 있습니다. 
2건의 레코드((1,1) 과 2,4를 가지는 임시 테이블을 만들고 조인해서 업데이트를 실행합니다. 

## JOIN DELETE
![[Pasted image 20240227004151.png]]
위 쿼리는 employees와 dept_emp, departments 3개의 테이블을 조인한 다음, 조인이 성공한 레코드에 대해 employees 테이블의 레코드만 삭제하는 쿼리입니다. 

원래 삭제 쿼리는 `delete from table`로 시작하지만 join delete는 어떤 테이블의 데이터를 삭제할지 delete 바로 뒤에 명시한다. 

참고로 하나의 테이블 만 삭제하는 것이 아닌 여러 테이블을 삭제할 수 있다. 
![[Pasted image 20240227004625.png]]



# 문제
###  문제1. 아래 쿼리의 결과를 출력하세요.
```
create table Test1(  
    id int primary key,  
    name varchar(10),  
    unique index(name)  
);  
  
  
insert ignore into Test1(id,name) value (1, '테스트1');  
insert ignore into Test1(id,name) value (2, '테스트1');  
insert ignore into Test1(id,name) value (3, '테스트2');  
insert ignore into Test1(id,name) value (4, '테스트4');  
  
select count(*) as result from Test1;
```

### 문제2. insert on duplicate key update와 replace의 차이점을 설명해주세요
replace는 삭제 후 insert의 조합으로 작동하지만
insert on duplicate key update는 중복된 프라이머리 키 혹은 유니크 인덱스의 경우 업데이트가 실행됩니다. 

### 문제3. 프라이머리키를 UUID와 A.I 둘중에서 무엇을 고르는게 좋을까요?

uuid의 장점
- uuid를 사용하면 데이터의 세그먼트를 포함하는 여러 데이터베이스가 있는 경우 id가 어느 데이터베이스에 존재하던 고유하다는 것을 알 수 있습니다. 
- 삽입 전에 pk를 알 수 있기 때문에 외래 키로 사용하여 하위 레코드를 삽입하기 전에 pk를 알아야 하는 트랜잭션 논리를 단순화 할 수 있습니ㅏ. 
- 보안에 이점이 있습니다.



AutoIncrement를 사용하게 될 경우 엔티티의 id로 사용하는 경우 id가 단순 숫자값이기 때문에 외부에서 쉽게 가져갈 수 있습니다.

API를 통해 유저의 개인정보를 조회할 때, 만약 보안 기능이 제대로 작동하지 않는다면 타인의 데이터를 쉽게 빼갈 수 있겠네요

보안적인 문제로 외부에서 서비스의 규모를 추정할 수 있습니다.
- Auto incrmenet id를 사용하면 새로운 데이터가 생성될 때 그 id가 그동안 쌓인 데이터의 양이 됩니다.

보안적인 부분이 아니더라도 디비 마이그레이션의 경우 ai 지원여부에 따라 골치아플 수 있음


UUID를 pk로 사용할 경우 다음과 같은 문제가 발생합니다. 
- pk는 클러스터링 인덱스로 사용되는데 UUID로 자주용되는 v4는 랜덤값이기 때문에 insert가 많아지면 저장된 데이터 sorting으로 인한 오버헤드가 발생하여 성능 저하가 발생할 수 있음
- ![[Pasted image 20240227164410.png]]
- 이를 대비하기 위해 pk와 uuid를 가지는 방법도 있습니다. 
- uuid 크기 줄이기(유튜브) https://github.com/gpslab/base64uid


정리하면 둘 중에 무엇을 선택하던 크게 중요하지 않습니다. 
다만 서비스 규모가  작다면 a.i를 사용하는 것이 단순하게 개발할 수 있으며 만약 규모를 확장하거나 보안이 필요하다면 uuid를 사용하는 것이 더 나은 방법일 수 있습니다.




https://enterprisecraftsmanship.com/posts/entity-identity-vs-database-primary-key/
https://devs0n.tistory.com/87
https://tomharrisonjr.com/uuid-or-guid-as-primary-keys-be-careful-7b2aa3dcb439
https://www.outsystems.com/forums/discussion/76850/what-are-the-pros-cons-of-uuid-vs-auto-increment-serial-for-the-primary-key/