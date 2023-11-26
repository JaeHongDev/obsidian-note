---
cssclasses:
  - my_style_width_100
---

일반적으로 레코드 레벨의 트랜잭션을 지원하는 DBMS가 제공하는 기능이며, MVCC의 가장 큰 목적은 잠금을 사용하지 않는 일관된 읽기를 제공하는 데 있습니다.
-> 레코드를 잠그지 않고 일관된 읽기를 제공하는 목적을 가지고 있다. 

[[InnoDB]]는 [[언두 로그]] 이용해 이 기능을 구현합니다.

여기서 멀티 버전은 하나의 레코드에 대해 여러 개의 버전이 동시에 관리된다는 의미입니다.


이해를 위해 [[격리 수준]] 이 READ_COMMITTED 인 [[MySQL서버 혹은 MySQL]] 에서 [[InnoDB]] 를 사용하는 테이블의 데이터 변경을 어떻게 처리하는지 보면 다음과 같습니다.
```mysql
mysql> create table member (
    ->  m_id int not null,
    ->  m_name varchar(20) not null,
    ->  m_area varchar(100) not null,
    ->  primary key (m_id),
    ->  index ix_area (m_area)
    -> );
mysql> insert into member (m_id, m_name,m_area) values (12, '홍길동', '서울');
mysql> commit;
```

```mysql
update member set m_area='경기' where m_id=12;
```

![[Pasted image 20231125133455.png]]

Update문장이 실행되면 커밋 실행 여부와 관계없이 InnoDB의 버퍼 풀은 새로운 값인 '경기'로 업데이트 된다. 그리고 디스크의 데이터 파일에는 체크포인트나 InnoDB의 write스레드에 의해 새로운 값으로 업데이트돼 있을 수도 있고 아닐 수도 있다.
<u>InnoDB가 ACID를 보장하기 때문에 일반적으로는 InnoDB의 버퍼 풀과 데이터 파일은 동일한 상태라고 가정해도 무방합니다</u>

#### 아직 COMMIT이나 ROLLBACK이 되지 않은 상태에서 다른 사용자가 다음 같은 쿼리로 작업 중인 레코드를 조회하면 어디에 있는 데이터를 조회할 까?
MySQL 서버의 시스템 변수(`transaction_isolation`)에 설정된 격리 수준에 따라 다름

격리 수준이 READ_UNCOMMITTED 인 경우에는 [[InnoDB 버퍼 풀]]이 현재 가지고 있는 변경된 데이터를 읽어서 반환합니다. 즉 데이터가 커밋됐든 아니든 변경된 상태의 데이터를 반환합니다.
그렇지 않고 READ_COMMITTED나 그 이상의 [[격리 수준]]인 경우에는 아직 커밋되지 않았기 때문에 [[InnoDB 버퍼 풀]]이나 데이터 파일에 있는 내용 대신 변경되기 이전의 내용을 보관하고 있는 언두 영역의 데이터를 반환합니다.

현재 상태에서 COMMIT 명령을 실행하면 InnoDB는 더 이상의 변경 작업 없이 지금의 상태를 영구적인 데이터로 만들어 버립니다. 하지만 롤백을 실행하면 InnoDB는 언두 영역에 있는 백업된 데이터를 [[InnoDB 버퍼 풀]] 로 다시 복구하고, 언두 영역의 내용을 삭제해 버립니다. 언두 영역의 백업 데이터가 항상 바로 삭제되는 것이 아닌 언두 영역을 필요로 하는 트랜잭션이 더는 없을 때 비로소 삭제됩니다.
