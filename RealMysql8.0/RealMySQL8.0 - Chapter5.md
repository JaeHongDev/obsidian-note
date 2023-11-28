---
cssclasses:
  - my_style_width_100
---


[[트랜잭션]]

### 잠금과 트랜잭션의 차이점
잠금은 동시성을 제어하기 위한 기능이고 트랜잭션은 데이터의 정합성을 보장하기 위한 기능입니다. 

트랜잭션은 데이터의 정합성을 보장하기 위한 기능입니다.

하나의 회원 정보 레코드를 여러 커넥션에서 동시에 변경하려고 하는데 잠금이 없다면 하나의 데이터를 여러 커넥션에서 동시에 변경할 수 있게 됩니다.

결과적으로 해당 레코드의 값은 예측할 수 없는 상태가 되는데 잠근은 여러 커넥션에서 동시에 동일한 자원을 요청할 경우 순서대로 한 시점에는 하나의 커넥션만 변경할 수 있게 해주는 역할을 합니다.

[[격리 수준]]



# 트랜잭션
[[트랜잭션]]

## 5.1.1 MySQL에서의 트랜잭션
트랜잭션은 꼭 여러 개의 변경 작업을 수행하는 쿼리가 조합됐을 때만 의미 있는 개념은 아닙니다.
-> 왜?
->트랜잭션은 하나의 논리적인 작업 셋에 하나의 쿼리가 있든 두 개 이상의 쿼리가 있든 관계없이 논리적인 작업 셋 자체가 100% 적용되거나 아무것도 적용되지 않아야 함을 보장해 주는 것이다.

간단한 예제로 트랜잭션 관점에서 [[InnoDB]]테이블과 [[키 캐시 (MyISAM)]] 테이블의 차이를 살펴보면 다음과 같습니다.

```mysql
mysql> create table tab_myisam (fdpk int not null, primary key (fdpk)) engine=myisam;
Query OK, 0 rows affected (0.01 sec)

mysql> insert into tab_myisam (fdpk) values(3);
Query OK, 1 row affected (0.00 sec)

mysql> create table tab_innodb (fdpk int not null, primary key (fdpk)) engine=innodb;
Query OK, 0 rows affected (0.02 sec)

mysql> insert into tab_innodb (fdpk) values (3);
Query OK, 1 row affected (0.00 sec)

mysql> set autocommit=on;
Query OK, 0 rows affected (0.00 sec)

mysql> insert into tab_myisam (fdpk) values (1), (2), (3);
ERROR 1062 (23000): Duplicate entry '3' for key 'tab_myisam.PRIMARY'
mysql> inser into tab_innodb (fdpk) values (1),(2),(3);
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'inser into tab_innodb (fdpk) values (1),(2),(3)' at line 1

mysql> select * from tab_myisam;
+------+
| fdpk |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)

mysql> select * from tab_innodb;
+------+
| fdpk |
+------+
|    3 |
+------+
1 row in set (0.00 sec)
```

auto-commit 모드에서 실행 시킨 결과는 놀랍게도 둘 사이의 차이가 있다. 

두 insert 문장 모두 실패한다. 하지만 결과는 다른데 [[키 캐시 (MyISAM)]]경우 1과 2는 insert된 상태로 남아 있는 것을 확인할 수 있다.
1,2를 저장하고 3(중복)을 저장할 때 3을 제외한 나머지 값은 저장하고 쿼리 실행을 종료해 버린다. 

[[InnoDB]]는 쿼리 중 일부라도 오류가 발생하면 전체를 원 상태로 만든다는 트랜잭션의 원칙대로 insert문장을 실행하기 전 상태 그대로 복구했다. 
[[키 캐시 (MyISAM)]]은 이런 현상을 `부분 업데이트`라고 표현하며 테이블 데이터의 정합성을 맞추는데 상당히 어려운 문제를 만들어 낸다.
## 5.1.2 주의 사항

[[트랜잭션]] 또한 DBMS의 커넥션과 동일하게 꼭 필요한 최소의 코드에만 적용하는 것이 좋습니다. 이는 프로그램 코드에서 <u>트랜잭션의 범위를 최소화하라는 의미입니다. </u>

1. 처리 시작
	1. => 데이터베이스 커넥션 생성
	2. => 트랜잭션 시작
2. 사용자의 로그인 여부 확인
3. 사용자의 글쓰기 내용의 오류 여부 확인
4. 첨부로 업로드된 파일 확인 및 저장
5. 사용자의 입력 내용을 DBMS에 저장
6. 첨부파일 정보를 DBMS에 저장
7. 저장된 내용 또는 기타 정보를 DBMS에서 조회
8. 게시물 등록에 대한 알림 메일 발송
9. 알림 메일 발송 이력을 DBMS에 저장
	1. <= 트랜잭션 종료(COMMIT)
	2. <= 데이터베이스 커넥션 반납
10. 처리 완료

위 처리 절차 중 DMBS의 트랜잭션 처리에 좋지 않은 영향을 미치는 부분을 나눠서 살펴보면 다음과 같습니다.
- 실제로 많은 개발자가 데이터베이스의 커넥션을 생성하는 코드를 1번과 2번 사이에 구현하며 그와 동시에 START TRANSACTION 명령으로 트랜잭션을 시작한다. 그리고 9번과 10번 사이에서 트랜잭션을 COMMIT하고 커넥션을 종료한다. 실제로 DBMS에 데이터를 저장하는 작업은 5번부터 시작된다는 것을 알 수 있다. 
1. 커넥션을 소유하는 시간이 길다
2. 메일 전송이나 FTP 파일 전송 작업 혹은 네트워크를 통해 원격 서버와 통신하는 작업은 DBMS 트랜잭션 내에서 제거하는 것이 좋다.
3. DMBS 작업을 분리할 수 있다면 분리하는 것이 좋다. 

1. 처리 시작
2. 사용자의 로그인 여부 확인
3. 사용자의 글쓰기 내용의 오류 여부 확인
4. 첨부로 업로드된 파일 확인 및 저장
	1. => 데이터베이스 커넥션 생성
	2. => 트랜잭션 시작
5. 사용자의 입력 내용을 DBMS에 저장
6. 첨부파일 정보를 DBMS에 저장
	1. <= 트랜잭션 종료(COMMIT)
7. 저장된 내용 또는 기타 정보를 DBMS에서 조회
8. 게시물 등록에 대한 알림 메일 발송
9. 알림 메일 발송 이력을 DBMS에 저장
	1. <= 트랜잭션 종료(COMMIT)
	2. <= 데이터베이스 커넥션 반납
10. 처리 완료



# 5.2 MySQL 엔진의 자믐


MySQL에서 사용되는 잠금은 크게 다음 레벨로 나눌 수 있다.
- [[스토리지 엔진]]레벨
- [[MySQL엔진]]레벨

<u>MySQL엔진은 MySQL 서버에서 스토리지 엔진을 제외한 나머지 부분으로 이해하면 된다.</u> 
MySQL엔진 레벨은 잠금은 모든 스토리지 엔진에 영향을 미치지만, 스토리지 엔진 레벨의 잠금은 스토리지 엔진 간 상호 영향을 미치지 않는다.

MySQL 엔진에서는 테이블 데이터 동기화를 위한 테이블 락 이외에도
- [[메타데이터 락]]
- [[네임드 락]]
을 제공한다. 

## 5.2.1 글로벌 락
[[글로벌 락]]

## 5.2.2 테이블 락
[[테이블 락]]
### 5.2.3 네임드 락 
[[네임드 락]]
### 5.2.4 메타데이터 락
메타데이터 락은 데이터베이스 객체의 이름이나 구조를 변경하는 경우에 획득하는 잠금입니다.
```
RENAME TABLE TAB_A TO TAB_B
```
위 내용처럼 테이블의 이름을 변경하는 경우 자동으로 획득하는 잠금입니다. 

하나의 RENAME TABLE 명령문에 두 개의 RENAME 작업을 한꺼번에 실행하면 실제 애플리케이션에서는 Table not found rank 같은 상황을 발생 시키지 않고 적용하는 것이 가능하다. 


메타 데이터 잠금과 InnoDB의 트랜잭션을 동시에 사용해야 하는 경우도 있습니다. 예를 들어 다음과 같은 구조의 INSERT만 실행되는 로그 테이블을 보면 해당 테이블은 웹 서버의 액셋ㅡ 로그를 저장만 하기 때문에 UPDATE와 DELETE가 없습니다. 
```mysql
CREATE TABLE ACCESS_LOG (
  id bigint not null auto_incrmenet,
  client_ip int unsigned, 
  access_dttm timestamp,
  primary key(id)
)
```

테이블 구조를 변경해야 하는 상황이 발생했을때 MySQL 서버의 Online DDL을 이용해서 변경할 수 있지만 단일 스레드로 작동하기 때문에 상당히 많은 시간이 소모도니다.
이때는 새로운 구조의 테이블을 생성하고 먼저 최근(1시간 직전 또는 하루 전)의 데이터까지는 프라이머리 키인 id값을 범위별로 나눠서 여러 개의 스레드로 빠르게 복사한다.

(이거 다시 보기)

# 5.3 InnoDB 스토리지 엔진 잠금
[[InnoDB]] 스토리지 엔진은 MySQL에서 제공하는 잠금과는 별개로 스토리지 엔진 내부에서 레코드 기반의 잠금 방식을 탑재하고 있습니다.
- [[키 캐시 (MyISAM)]]보다 뛰어난 동시성 처리를 제공함
- 이원화된 잠금 처리 탓에 [[InnoDB]] 스토리지 엔진에서 사용되는 잠금에 대한 정보는 MySQL 명령어를 이용해 접근하기 상당히 어려웠다.
- 최근 버전에서 [[InnoDB]]의 [[트랜잭션]]과 잠금, 그리고 잠금 대기 중인 트랜잭션의 목록을 조회할 수 있는 방법이 도입됐다. 

## InnoDB 스토리지 엔진의 잠금

InnoDB 스토리지 엔진은 레코드 기반의 잠금 기능을 제공하며, 잠금 정보가 상당히 작은 공간으로 관리되기 때문에 레코드 락이 페이지 락으로, 또는 테이블 락으로 레벨업되는 경우는 없다.
일반 상용 DBMS와는 조금 다르게 [[InnoDB]] 스토리지 엔진에서는 레코드 락뿐 아니라 레코드와 레콛 사이듸 간격을 잠그는 [[갭 락 (GAP LOCK)]]이 존재합니다.
![[Pasted image 20231127145834.png]]

[[레코드 락(Record Lock, Record only lock)]]
[[갭 락 (GAP LOCK)]]
[[넥스트 키 락(Next Key Lock)]]
[[자동 증가 락]]


## 5.3.2 인덱스와 잠금



