---
cssclasses:
  - my_style_width_100
---

핸들러라는 단어는 mySQL 서버의 소스코드로부터 넘어온 표현인데, 이는 우리가 매일 타고 다니는 자동차로 비유하면 이해하기 쉽습니다.
사람이 핸들(운전대)를 이용해 자동차를 운전하듯이, 프로그래밍 언어에서는 어떤 기능을 호출하기 위해 사용하는 운전대와 같은 역할을 하는 객체를 핸들러라고 표현합니다. 
MySQL 서버에서는 MySQL 엔진은 사람 역할을 하고 각 스토리지 엔진은 자동차 역할을 하는데, MySQL엔진이 스토리지 엔진을 조정하기 위해 핸들러라는 것을 사용하게 된다.

MySQL에서 핸들러라는 것은 개념적인 내용으로 완전히 이해하지 못하더라도 크게 문제되지는 않습니다.
<u>다만 MySQL 엔진이 각 스토리지 엔진에게 데이터를 읽어오거나 저장하도록 명령하려면 반드시 핸들러를 통해야 한다는 점만 기억하면 됩니다.</u>

핸들러는 [[MySQL서버 혹은 MySQL]] 의 가장  밑단에서 [[MySQL엔진]]의 요청에 따라 데이터를 디스크로 젖아하고 디스크로부터 읽어 오는 역할을 담당합니다.

핸들러는 결국 스토리지 엔진을 의미하며 MyISAM 테이블을 조작하는 경우에는 핸들러가 MyISAM 스토리지 엔진이 되고, InnoDB 테이블을 조작하는 경우에는 핸들러가 InnoDB 스토리지 엔진이 됩니다.


`Handler_` 로 시작하는 상태 변수는 `MySQL`엔진이 각 스토리지 엔진에게 보낸 명령의 횟수를 의미하는 변수로 이해하면 됩니다.
[[키 캐시 (MyISAM)]] 이나 [[InnoDB]] 와 같이 다른 소토리지 엔진을 사용하는 테이블에 대해 쿼리를 실행하더라도 MySQL의 처리 내용은 대부분 동일하며, 데이터 읽기/쓰기 영역의 처리만 차이가 있습니다. 실질적인 `GORUP BY` 혹은 `Order By` 등의 복잡한 처리는 [[스토리지 엔진]] 영역이 아닌 [[MySQL엔진]] 의 처리 영역인 쿼리 실행기에서 처리됩니다. 

<u>MyISAM 이나 InnoDB 스토리지 엔진 가운데 뭘 사용하든 별 차이가 없는 것 아닌가, 라고 생각할 수 있지만 그렇지 않습니다.</u>

하나의 쿼리 작업은 여러 하위 작업으로 나뉘는데, 각 하위 작업이 [[MySQL엔진]] 영역과 [[스토리지 엔진]] 영역에서 처리되는지 구분할 수 있어야 합니다.
> 책에서는 스토리지 엔진의 개념을 설명하기 위한 것도 있지만 각 단위 작업을 누가 처리하고 MySQL 엔진 영역과 스토리지 엔진 영역의 차이를 설명하는 데 목적이 있습ㄴ다.

아래 명령어를 통해서 어떤 Engine이 있는지 조회할 수 있습니다.
```mysql
mysql> SHOW ENGINES;
ERROR 2006 (HY000): MySQL server has gone away
No connection. Trying to reconnect...
Connection id:    286
Current database: mysql

+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| Engine             | Support | Comment                                                        | Transactions | XA   | Savepoints |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| ndbcluster         | NO      | Clustered, fault-tolerant tables                               | NULL         | NULL | NULL       |
| CSV                | YES     | CSV storage engine                                             | NO           | NO   | NO         |
| ARCHIVE            | YES     | Archive storage engine                                         | NO           | NO   | NO         |
| BLACKHOLE          | YES     | /dev/null storage engine (anything you write to it disappears) | NO           | NO   | NO         |
| ndbinfo            | NO      | MySQL Cluster system information storage engine                | NULL         | NULL | NULL       |
| MRG_MYISAM         | YES     | Collection of identical MyISAM tables                          | NO           | NO   | NO         |
| FEDERATED          | NO      | Federated MySQL storage engine                                 | NULL         | NULL | NULL       |
| MyISAM             | YES     | MyISAM storage engine                                          | NO           | NO   | NO         |
| PERFORMANCE_SCHEMA | YES     | Performance Schema                                             | NO           | NO   | NO         |
| InnoDB             | DEFAULT | Supports transactions, row-level locking, and foreign keys     | YES          | YES  | YES        |
| MEMORY             | YES     | Hash based, stored in memory, useful for temporary tables      | NO           | NO   | NO         |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
11 rows in set (0.03 sec)
```

Support 컬럼에 표시될 수 있는 값은 다음 4자가 있습니다.
- Yes: MySQL 서버(mysqld)에 해당 스토리지 엔진이 포함돼 있고, 사용 가능으로 활성화된 상태임
- DEFAULT: Yes와 동일한 상태지만 필수 스토리지 엔진을 의미함
	- 이 스토리지 엔진이 없으면 MySQL이 시작되지 않을 수도 있음
- No: 현재 MySQL 서버에 포함되지 않았음을 의미함
- DISABLED: 현재 MySQL 서버에는 포함됐지만 파라미터에 의해 비활성화된 상태임

[[MySQL서버 혹은 MySQL]]에 포함되지 않은 스토리지 엔진을 사용하려면 MySQL 서버를 다시 빌드(컴파일)해야 합니다.
하지만 MySQL 서버가 적절히 준비만 돼 있다면 플러그인 형태로 빌드된 [[스토리지 엔진]]라이브러리를 다운로드해서 끼워 넣기만 하면 사용할 수 있습니다. 
-> 적절하다의 기준은..?j

또한 플러그인 형태의 스토리지 엔진은 손쉽게 업그레이드 할 수 있습니다.  스토리지 엔진뿐만 아니라 모든 플러그인의 내용은 다음과 같이 확인할 수 있습니다.

```mysql
mysql> show plugins;
+----------------------------------+----------+--------------------+-----------------+---------+
| Name                             | Status   | Type               | Library         | License |
+----------------------------------+----------+--------------------+-----------------+---------+
| keyring_file                     | ACTIVE   | KEYRING            | keyring_file.so | GPL     |
| binlog                           | ACTIVE   | STORAGE ENGINE     | NULL            | GPL     |
| mysql_native_password            | ACTIVE   | AUTHENTICATION     | NULL            | GPL     |
| sha256_password                  | ACTIVE   | AUTHENTICATION     | NULL            | GPL     |
| caching_sha2_password            | ACTIVE   | AUTHENTICATION     | NULL            | GPL     |
| sha2_cache_cleaner               | ACTIVE   | AUDIT              | NULL            | GPL     |
| daemon_keyring_proxy_plugin      | ACTIVE   | DAEMON             | NULL            | GPL     |
| CSV                              | ACTIVE   | STORAGE ENGINE     | NULL            | GPL     |
| MEMORY                           | ACTIVE   | STORAGE ENGINE     | NULL            | GPL     |
| InnoDB                           | ACTIVE   | STORAGE ENGINE     | NULL            | GPL     |
| INNODB_TRX                       | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_CMP                       | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_CMP_RESET                 | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_CMPMEM                    | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_CMPMEM_RESET              | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_CMP_PER_INDEX             | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_CMP_PER_INDEX_RESET       | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_BUFFER_PAGE               | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_BUFFER_PAGE_LRU           | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_BUFFER_POOL_STATS         | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_TEMP_TABLE_INFO           | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_METRICS                   | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_FT_DEFAULT_STOPWORD       | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_FT_DELETED                | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_FT_BEING_DELETED          | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_FT_CONFIG                 | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_FT_INDEX_CACHE            | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_FT_INDEX_TABLE            | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_TABLES                    | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_TABLESTATS                | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_INDEXES                   | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_TABLESPACES               | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_COLUMNS                   | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_VIRTUAL                   | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_CACHED_INDEXES            | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| INNODB_SESSION_TEMP_TABLESPACES  | ACTIVE   | INFORMATION SCHEMA | NULL            | GPL     |
| MyISAM                           | ACTIVE   | STORAGE ENGINE     | NULL            | GPL     |
| MRG_MYISAM                       | ACTIVE   | STORAGE ENGINE     | NULL            | GPL     |
| PERFORMANCE_SCHEMA               | ACTIVE   | STORAGE ENGINE     | NULL            | GPL     |
| TempTable                        | ACTIVE   | STORAGE ENGINE     | NULL            | GPL     |
| ARCHIVE                          | ACTIVE   | STORAGE ENGINE     | NULL            | GPL     |
| BLACKHOLE                        | ACTIVE   | STORAGE ENGINE     | NULL            | GPL     |
| FEDERATED                        | DISABLED | STORAGE ENGINE     | NULL            | GPL     |
| ndbcluster                       | DISABLED | STORAGE ENGINE     | NULL            | GPL     |
| ndbinfo                          | DISABLED | STORAGE ENGINE     | NULL            | GPL     |
| ndb_transid_mysql_connection_map | DISABLED | INFORMATION SCHEMA | NULL            | GPL     |
| ngram                            | ACTIVE   | FTPARSER           | NULL            | GPL     |
| mysqlx_cache_cleaner             | ACTIVE   | AUDIT              | NULL            | GPL     |
| mysqlx                           | ACTIVE   | DAEMON             | NULL            | GPL     |
+----------------------------------+----------+--------------------+-----------------+---------+
49 rows in set (0.00 sec)
```