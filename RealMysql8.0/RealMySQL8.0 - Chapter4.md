---
cssclasses:
  - my_style_width_100
---

> 학습목표
> MySQL엔진과 MySQL서버에서 기본으로 제공되는 InnoDB 스토리지 엔진, 그리고 MyISAM 스토리지 엔진을 구분해서 설펴볼 예정



### 4장을 보며 찾을 의문점
1. 엔진이 무엇일까
2. 왜 mySQL은 다른 DBMS와 독특한 차이가 있다고 이야기하는 걸까
3. ANSI가 중요한 이유는 뭘까?


# 아키텍처

MySQL 서버는 <u>MySQL엔진</u>과 <u>스토리지 엔진</u>으로 구분할 수 있습니다.

스토리지 엔진은 핸들러 API를 만족하면 누구든지 스토리지 엔진을 구현해서 MySQL 서버에 추가해서 사용할 수 있습니다.



## 4.1 MYSQL 엔진 아키텍처

[[MySQL서버 혹은 MySQL]]는 다른 DBMS에 비해 구조가 독특합니다. 이런 독특한 구조 때문에 다른 DBMS에서는 가질 수 없는 엄청난 혜택을 누릴 수 있으며, 반대로 다른 DBMS에서는 문제되지 않을 것들이 가끔 문제가 되기도 한다.
[[MySQL엔진]]
[[엔진이 뭐죠?]]

#### 어떤 문제가 있죠..?
![[Pasted image 20231122213820.png]]



#### MySQL 엔진
[[MySQL엔진]]
MySQL 엔진은 클라이언트로부터의 접속 및 쿼리 요청을 처리하는 커넥션 핸들러와 SQL 파서 및 전처리기 

그래서 MySQL엔진의 의미는 무엇일까요? 
-> 한줄로 요약하기
#### 스토리지 엔진
[[스토리지 엔진]]
MySQL 엔진은 요청된 SQL 문장을 분석하거나 최적화하는 등 DBMS의 두뇌에 해당하는 처리를 수행하고, 실제 데이터를 디스크 스토리지에 저장하거나 디스크 스토리지로부터 데이터를 읽어오는 부분은 스토리지 엔진이 전담합니다.


MySQL 서버에서 MySQL엔진은 하나지만 스토리지 엔진은 여러 개를 동시에 사용할 수 있다.
-> InnoDB로 할건지 MyISAM으로 할지 정하는 것 처럼 그런 것 같은데 왜 이 구조를 허용했지?
-> 데이터베이스 테이블마다 다른 스토리지 엔진을 사용할 수 있음

#### 핸들러 API
[[핸들러 API]]
MySQL 엔진의 쿼리 실행기에서 데이터를 쓰거나 읽어야 할 때는 각 스토리지 엔진에 쓰기 또는 읽기를 요청하는데, 이러한 요청을 핸들러요청이라고 부릅니다.
여기서 사용하는 API를 핸들러 API라고 부릅니다. 



## 4.1.2 MySQL 스레딩 구조

[[MySQL서버 혹은 MySQL]]
MySQL 서버는 프로세스 기반이 아니라 스레드 기반으로 작동한다.
- 포그라운드 스레드
- 백그라운드 스레드
위 두가지로 구분한다.

MySQL 서버에서 실행 중인 스레드의 목록은 `performance_schema` 데이터베이스의 threads 테이블을 통해 확인할 수 있습니다.
```mysql

Database changed
mysql> SELECT thread_id, name, type, processlist_user, processlist_host  FROM  performance_schema, threads ORDER BY type, thread_id;
ERROR 1146 (42S02): Table 'mysql.performance_schema' doesn't exist
mysql> SELECT thread_id, name, type, processlist_user, processlist_host  FROM  performance_schema.threads ORDER BY type, thread_id;
+-----------+---------------------------------------------+------------+------------------+------------------+
| thread_id | name                                        | type       | processlist_user | processlist_host |
+-----------+---------------------------------------------+------------+------------------+------------------+
|         1 | thread/sql/main                             | BACKGROUND | NULL             | NULL             |
|         2 | thread/mysys/thread_timer_notifier          | BACKGROUND | NULL             | NULL             |
|         4 | thread/innodb/io_ibuf_thread                | BACKGROUND | NULL             | NULL             |
|         5 | thread/innodb/io_read_thread                | BACKGROUND | NULL             | NULL             |
|         6 | thread/innodb/io_read_thread                | BACKGROUND | NULL             | NULL             |
|         7 | thread/innodb/io_read_thread                | BACKGROUND | NULL             | NULL             |
|         8 | thread/innodb/io_read_thread                | BACKGROUND | NULL             | NULL             |
|         9 | thread/innodb/io_write_thread               | BACKGROUND | NULL             | NULL             |
|        10 | thread/innodb/io_write_thread               | BACKGROUND | NULL             | NULL             |
|        11 | thread/innodb/io_write_thread               | BACKGROUND | NULL             | NULL             |
|        12 | thread/innodb/io_write_thread               | BACKGROUND | NULL             | NULL             |
|        13 | thread/innodb/page_flush_coordinator_thread | BACKGROUND | NULL             | NULL             |
|        14 | thread/innodb/log_checkpointer_thread       | BACKGROUND | NULL             | NULL             |
|        15 | thread/innodb/log_flush_notifier_thread     | BACKGROUND | NULL             | NULL             |
|        16 | thread/innodb/log_flusher_thread            | BACKGROUND | NULL             | NULL             |
|        17 | thread/innodb/log_write_notifier_thread     | BACKGROUND | NULL             | NULL             |
|        18 | thread/innodb/log_writer_thread             | BACKGROUND | NULL             | NULL             |
|        19 | thread/innodb/log_files_governor_thread     | BACKGROUND | NULL             | NULL             |
|        24 | thread/innodb/srv_lock_timeout_thread       | BACKGROUND | NULL             | NULL             |
|        25 | thread/innodb/srv_error_monitor_thread      | BACKGROUND | NULL             | NULL             |
|        26 | thread/innodb/srv_monitor_thread            | BACKGROUND | NULL             | NULL             |
|        27 | thread/innodb/buf_resize_thread             | BACKGROUND | NULL             | NULL             |
|        28 | thread/innodb/srv_master_thread             | BACKGROUND | NULL             | NULL             |
|        29 | thread/innodb/dict_stats_thread             | BACKGROUND | NULL             | NULL             |
|        30 | thread/innodb/fts_optimize_thread           | BACKGROUND | NULL             | NULL             |
|        33 | thread/mysqlx/acceptor_network              | BACKGROUND | NULL             | NULL             |
|        37 | thread/innodb/buf_dump_thread               | BACKGROUND | NULL             | NULL             |
|        38 | thread/innodb/clone_gtid_thread             | BACKGROUND | NULL             | NULL             |
|        39 | thread/innodb/srv_purge_thread              | BACKGROUND | NULL             | NULL             |
|        40 | thread/innodb/srv_worker_thread             | BACKGROUND | NULL             | NULL             |
|        41 | thread/innodb/srv_worker_thread             | BACKGROUND | NULL             | NULL             |
|        42 | thread/innodb/srv_worker_thread             | BACKGROUND | NULL             | NULL             |
|        44 | thread/sql/signal_handler                   | BACKGROUND | NULL             | NULL             |
|        45 | thread/mysqlx/acceptor_network              | BACKGROUND | NULL             | NULL             |
|        65 | thread/mysqlx/worker                        | BACKGROUND | NULL             | NULL             |
|       277 | thread/mysqlx/worker                        | BACKGROUND | NULL             | NULL             |
|        43 | thread/sql/event_scheduler                  | FOREGROUND | event_scheduler  | localhost        |
|        47 | thread/sql/compress_gtid_table              | FOREGROUND | NULL             | NULL             |
|       281 | thread/sql/one_connection                   | FOREGROUND | root             | localhost        |
+-----------+---------------------------------------------+------------+------------------+------------------+
39 rows in set (0.01 sec)
```

밑에 3개만 포그라운드 스레드고 나머지는 백그라운드 스레드입니다. 
- `thread/sql'/one_connection` 스레드만 실제 사용자의 요청을 처리하는 포그라운드 스레드 입니다.
-  백그라운드 스레드의 개수는 MySQL 서버의 설정 내용에 따라 가변적이다 -> 이말이 무슨 말이지?
- 동일한 이름의 스레드가 2개 이상씩 보이는 것은 MySQL 서버의 설정 내용에 의해 여러 스레드가 동일 작업을 병렬로 처리하는 경우다.
#### 참고
여기서 소개하는 스레드 모델은 MySQL 서버가 전통적으로 가지고 있던 스레드 모델입니다. MySQL 커뮤니티 에디션에서 사용되는 모델로 MySQL 엔터프라이즈 에디션과 Percona MySQL 서버에서는 전통적인 스레드 모델 뿐 아니라 스레드 풀 모델을 사용할 수도 있습니다.


### 포그라운드 스레드 (클라이언트 스레드)
[[포그라운드 스레드]]
- 포그라운드 스레드는 최소한 MySQL 서버에 접속된 클라이언트의 수만큼 존재한다.
- 각 클라이언트 사용자가 요청하는 쿼리 문장을 처리한다.

클라이언트 사용자가 작업을 마치고 커넥션을 종료하면 해당 커넥션을 담당하던 스레드는 다시 스레드 캐시로 되돌아간다.
-> 무슨 의미로 받아들이는게 좋을까..?

- 포그라운드 스레드는 데이터를 MySQL의 데이터 버퍼나 캐시로부터 가져오며, 버퍼나 캐시에 없는 경우에는 직접 디스크의 데이터나 인덱스 파일로부터 데이터를 읽어와서 작업을 처리한다.
- MyISAM 테이블은 디스크 쓰기 작업까지 포그라운드 스레드가 처리하지만 InnoDB 테이블은 데이터 버퍼나 캐시까지만 포그라운드 스레드가 처리하고, 나머지 버포로부터 디스크까지 기록하는 작업은 백그라운드 스레드가 처리한다.

> MySQL에서 사용자 스레드와 포그라운드 스레드는 똑같은 의미라고 사용된다. 클라이언트가 MySQL 서버에 접속하게 되면 MySQL 서버는 그 클라잉너트의 요청을 처리해 줄 스레드를 생성해 그 클라이언트에게 할당한다. 이 스레드는 DBMS의 앞단에서 사용자(클라이언트)와 통신하기 때문에 포그라운드 스레드라고 하며, 사용자가 요청한 작업을 처리하기 때문에 사용자 스레드라고도 한다.


### 백그라운드 스레드
[[백그라운드 스레드]]
MyISAM의 경우에는 별로 해당 사항이 없는 부분이지만 InnoDB는 다음과 같이 여러 가지 작업이 백그라운드로 처리된다.
- 인서트 버퍼(Insert Buffer)를 병합하는 스레드
- 로그를 디스크로 기록하는 스레드
- InnoDB 버퍼 풀의 데이터를 디스크에 기록하는 스레드
- 데이터를 버퍼로 읽어 오는 스레드
- 잠금이나 데드락을 모니터링하는 스레드



## 4.1.3 메모리 할당 구조
[[MySQL서버 혹은 MySQL]]
MySQL에서 사용되는 메모리 공간은 크게 다음과 같이 분리할 수 있습니다.
- [[글로벌 메모리 영역]]
- [[로컬 메모리 영역]]

글로벌 메모리 영역의 모든 메모리 공간은 <u>MySQL 서버가 시작되면서 운영체제로부터 할당됩니다.</u>
운영체제의 종류에 따라 다르겠지만 요청된 메모리 공간을 100% 할당해줄 수도 있고, 그 공간만큼 예약해두고 필요할 때 조금씩 할당해주는 경우도 있다.



### 글로벌 메모리 영역
일반적으로 클라이언트 스레드의 수와 무관하게 하나의 메모리 공간만 할당된다. 단 필요에 따라 2개 이상의 메모리 공간을 할당받을 수도 있지만 클라이언트의 스레드 수와 무관하며, 생성도니 글로벌 영역이 N개라 하더라도 모든 스레드에 의해 공유된다.
대표적으로 글로벌 메로리 영역은 다음과 같다.
- 테이블 캐시
- InnoDB 버퍼 풀
- InnoDB 어댑티브 해시 인덱스
- InnoDB 리두 로그 버퍼

#### 로컬 메모리 영역
세션 메모리 영역이라고도 표현하며 MySQL 서버상에 존재하는 클라이언트 스레드가 쿼리를 처리하는데 사용하는 메모리 영역이다. 
대표적으로 <u>커넥션 버퍼</u>와 <u>정렬 버퍼</u> 등이 있다.

<u>MySQL 서버에 접속하면 MySQL 서버에서는 클라이언트 커넥션으로부터의 요청을 처리하기 위해 스레드를 하나씩 할당하게 되는데, 클라리언트 스레드가 사용하는 메모리 공간이라고 해서 클라이언트 메모리 영역이라고도 한다. </u>

로컬 메모리는 각 클라리언트 스레드별로 독립적으로 할당되며 절대 공유되어 사용되지 않는다는 특징이 있다. 


## 4.1.4 플러그인 스토리지 엔진 모델
[[플러그인 스토리지 엔진 모델]]
MySQL의 독특한 구조 중 대표적인 것이 <u>플러그인 모델이다</u>. 플러그인에서 사용할 수 있는 것이 스토리지 엔진만 있는 것은 아니다. 
- 전문 검색 엔진을 위한 검색어 파서 -> 플러그인 형태로 개발해서 사용 가능
- 사용자 인증을 위한 Native Authentication, Caching SHA-2 Authentication등도 모두 플러그인으로 구현되어 제공된다.

MySQL에서 쿼리가 실행되는 과정을 보면 거의 대부분의 작업이 MySQL엔진에서 처리되고, 마지막 데이터 읽기.쓰기 작업만 스토리지 엔진에 의해 처리된다.
-> 새로운 용도의 스토리지 엔진을 만든다 하더라도 DBMS의 전체 기능이 아닌 일부분의 기능만 수행하는 엔진을 작성하는 것임

- SQL 파서
- SQL 옵티마이저
- SQL 실행기
- 데이터 읽기/쓰기 (스토리지 엔진의 처리 영역) 
- 디스크

## 4.1.5 컴포넌트
[[MySQL 컴포넌트]]

## 4.1.6 쿼리 실행 구조 

[[MySQL 쿼리 실행 구조]]

### 쿼리 파서
쿼리 파서는 사용자 요청으로 들어온 쿼리 문장을 토큰으로 분리해 트리 형태의 구조를 만들어 내는 작업을 의미합니다. 쿼리 문장의 기본 문법 오류는 이 과정에서 발견되고 사용자에게 오류 메시지를 전달합니다.

### 전처리기
파서 과정에서 만들어진 파서 트리를 기반으로 쿼리 문장에 구조적인 문제점이 있는지 확인합니다. 각 토큰을 테이블 이름이나 칼럼 이름, 또는 내장 함수와 같은 개체를 매핑해 해당 객체의 존재 여부와 객체의 접근 권한 등을 이 과정에서 수행합니다. 


- 개체 ? 객체

### 옵티마이저
옵티마어지란 <u>사용자의 요청으로 들어온 쿼리 문장을 저렴한 비용으로 가장 빠르게 처리할지를 결정하는 역할을 담당합니다.</u>

이 책에서 
- 옵티마이저개 선택하는 내용을 설명
- 옵티마이저가 더 나은 서택을 할 수 있게 유도하는 방법을 설명

### 실행 엔진
실행 엔진은 만들어진 계획대로 각 핸들러에게 요청해서 받은 결과를 또 다른 핸들러 요청의 입력으로 연결하는 역할을 수행한다.

### 핸들러
핸들러는 <u>MySQL 서버의 가장 밑단에서 MySQL 실행 엔진의 요청에 따라 데이터를 디스크로 저장하고 디스크로부터 읽어 오는 역할을 담당한다. 핸들러는 결국 스토리지 엔진을 의미한다.</u>

- MyISAM 테이블을 조작하는 경우 MyISAM 스토리지 엔진이 핸들러
- InnoDB 테이블을 조작하는 경우 InnoDB 스토리지 엔진이 핸들러

## 4.1.7 복제
[[복제 (MySQL)]]
지금은 중요하지 않음 

## 4.1.8 쿼리 캐시
MySQL 8.0에서 부터 해당 기능은 완전히 제거되고 관련 시스템 변수도 모두 제거 됐다.
[[쿼리 캐시 (MySQL)]]
## 4.1.9 스레드 풀
[[스레드 풀(MySQL)]]

MySQL 서버 엔터프라이즈 에디션은 스레드 풀 기능을 제공하지만 MySQL 커뮤니티은 지원하지 않는다.


스레드 풀은 내부적으로 사용자의 요청을 처리하는 스레드 개수를 줄여소 동시 처리되는 요청이 많다 하더라도 MySQL 서버의 CPU가 제한된 개수의 스레드 처리에만 집중할 수 있게 해서 서버의 자원 소모를 줄이는 것이 목적이다.

`Percona Server` 의 스레드 풀은 기본적으로 CPU 코어의 개수만큼 스레드 그룹을 생성하는데, 스레드 그룹의 개수는 `thread_pool_size` 시스템 변수를 변경해서 조정할 수 있다. 하지만 일반적으로 CPU코어의 개수와 맞추는 것이 CPU 프로세서 친화도를 높이는 데 좋다.


## 4.1.10 트랜잭션 지원 메타 데이터
[[트랜잭션 지원 메타데이터]]
데이터베이스 서버에서 테이블의 구조 정보와 스토어드 프로그램 등의 정보를 데이터 딕셔너리 혹은 메타데이터라고 합니다.


# 4.2 InnoDB 스토리지 엔진 아키텍처
[[스토리지 엔진]]
[[InnoDB]]
