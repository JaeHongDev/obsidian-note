---
cssclasses:
  - my_style_width_100
---
#mysql 에서 사용자 계정을 생성하는 경우 다른 DBMS와 몇 가지 차이점이 있습니다. (사실 DBMS마다 조금씩 다름)
- MySQL 사용자 계정은 단순히 아이디뿐 아니라 해당 사용자가 어느 IP에서 접속하는지 확인합니다.
- 권한을 묶어서 관리하는 (Role)의 개념이 도입됐기 때문에 여러 권한을 묶은 세트(Role)을 부여하는 것 또한 가능합니다. 
- <u>사용자의 접속 지점(클라이언트가 실행된 호스트명이나 도메인 또는 IP)도 계정의 일부가 된다.</u>

## 사용자 식별

mysql의 사용자 식별 방법은 몇 가지 특징이 있습니다.
- <u>사용자의 접속 집점(클라이언트가 실행된 호스트명이나 도메인 또는 IP)도 계정의 일부가 된다.</u>
- 아이디와 호스트를 함께 명시해야 합니다.
-  백틱 혹은 홑따옴표로 아이디와 IP주소를 감쌀 수 있음


###  예제1
- 아래 사용자 계정은 MySQL 서버가 기동 중인 로컬 호스트에서 `svc_id` 라는 아이디로 접속할 때만 사용할 수 있습니다.
```mysql
'svc_id'@127.0.0.1
```

### 상황2
만약 모든 컴퓨터에서 접속이 가능한 사용자를 생성하고 싶다면 ip주소를 `%` 문자로 대체하면 됩니다.
```mysql
'svc_id'@'%' #password abc
```

### 상황3
아래와 같은 계정 상태에서 패스워드가 다른 경우 어떤 계정으로 접근이 가능할까?
```mysql
'svc_id'@192.168.0.10 #password 123
'svc_id'@'%' #password abc
```

- MySQL에서 권한이나 계정 정보에 대해서 가장 작은 것을 항상 먼저 선택합니다.
	-  위 두 계정 정보 가운데 `%` 는 더 넓은 범위를 포함하고 있기 때문에  `192.168.0.10` 호스트의 비밀번호에 해당 하는 정보를 선택한다.
	- 그렇기에  `'svc_id'@192.168.0.10 #password abc` 로 접근하는 경우 비밀번호가 일치하지 않는다.
		- <u>종종 생기는 상황</u>


## 사용자 계정 관리

### 시스템 계정과 일반 계정
MySQL 8.0는  기준이 되는 것은 `SYSTEM_USER` 권한 가지고 있느냐에 따라 계정이 구분됩니다.
- 시스템 계정
	- 데이터베이스 서버 관리자를 위한 계정
	- 다른 시스템 계정과 일반 계정을 관리 할 수 있음
	- 다른 세션(Connection) 또는 그 세션에서 실행 중인 쿼리를 강제 종료	
	 - 스토어드 프로그램 생성 시 DEFINER를 사용자로 설정
- 일반 계정
	- 일반 운영 프로그램, 개발자를 위한 계정
	 - 계정 관리가 불가능

[[데이터베이스 계정과 사용자]]

예외적으로 내장된 계정
- `root@localhost`
- `mysql.sys@localhost` : 기본으로 내장된 sys스키마의 객체 (VIEW, Function, 프로시저)를 정의하는 계정
- `mysql.session@localhost` : MySQL 플러그인 서버로 접근할 때 사용되는 계정
 - `mysql.infoschema@localhost`: information_schema 정의된 View의 DEFINER로 사용되는 계정
<u>참고로 root를 제외한 계정은 잠겨 있는 상태이며 의도적으로 계정을 풀지 않는 한 악의적인 용도로 사용할 수 없습니다.</u>

```mysql
mysql> select user, host, account_locked from mysql.user where user like 'mysql.%';
+------------------+-----------+----------------+
| user             | host      | account_locked |
+------------------+-----------+----------------+
| mysql.infoschema | localhost | Y              |
| mysql.session    | localhost | Y              |
| mysql.sys        | localhost | Y              |
+------------------+-----------+----------------+
3 rows in set (0.03 sec)
ㅐ```


### 계정 생성
MySQL 5.7 버전까지 `GRANT` 명령으로 권한의 부여와 동시에 계정 생성이 가능했지만 8.0부터 구분해서 실행하도록 변경되었습니다.
- `CREATE USER` : 계정 생성
	- 계정의 인증 방식과 비밀번호
	- 비밀번호 관련 옵션 (비밀번호 유효 기간, 비밀번호 이력 개수, 비밀번호 재사용 불과 기간)
	- 기본 역할(Role)
	- [[SSL]] 옵션
	- 계정 잠금 여부
- `GRANT` : 권한 부여

책의 예시로 사용자를 생성하는 명령어는 다음과 같습니다
```mysql
CREATE USER 'user'@'%'
	IDENTIFIED WITH 'mysql_native_password' BY 'password' 
	REQUIRED NONE
	PASSWORD EXPIRE INTERVAL 30 DAY
	ACCOUNT UNLOCK
	PASSWORD HISTORY DEFAULT
	PASSWORD REUSE INTERVAL DEFAULT
	PASSWORD REQUIRE CURRENT DEFAULT
```

### IDENTIFIED WITH
사용자의 인증 방식과 비밀번호를 설정하는 구문이며 다음과 같은 특징을 가지고 있습니다.
-  IDENTIFIED WITH 뒤에는 <u>반드시 인증 방식을 명시해야 합니다</u>. 
	- [[Native Authentication]]
	- [[Caching SHA-2 Authentication]]  
	- [[PAM Authentication]]
	 - [[LDAP Authentication]]

MySQL 5.7버전까지 Native Authentication이 기본 인증 방식으로 사용됐지만 MySQL 8.0 부터 Caching SHA-2 Authentication으로 변경됐습니다. 
<u>단 호환성을 위해서 이전 인증 방식을 사용할 수 있도록 설정할 수 있습니다</u>
```mysql
SET GLOBAL default_authentication_plugin="mysql_native_password"
```

```mysql
mysql> SHOW GLOBAL VARIABLES LIKE 'default_authentication_plugin';
+-------------------------------+-----------------------+
| Variable_name                 | Value                 |
+-------------------------------+-----------------------+
| default_authentication_plugin | caching_sha2_password |
+-------------------------------+-----------------------+
```

### REQUIRE
MySQL 서버에 접속할 때 암호화된 SSL/TLS 채널을 사용할지 여부를 설정합니다. 
- 별도의 설정하지 않으면 비암호화 채널로 연결하게 됩니다.
- Require 옵션을 [[SSL]] 로 설정하지 않았다고 하더라도 [[Caching SHA-2 Authentication]] 인증 방식을 사용하면 암호화된 채널만으로 `MySQL` 서버에 접속할 수 있게 됩니다.
###### 여기서 암호화된 채널이 무엇을 의미하죠?


### PASSWORD EXPIRE
- 비밀번호의 유효기간을 설정하는 옵션
	- `PASSWORD EXPIRE` : 계정 생성과 동시에 비밀번호의 만료 처리
	- `PASSWORD EXPIRE NEVER`: 계정 비밀번호의 만료 기간 없음
	- `PASSWORD EXPIRE DEFAULT` : `default_password_lifetime` 시스템 변수에 저장된 기간으로 비밀번호의 유효기간 설정
	- `PASSWORD EXIPRE INTERVAL n DAY` 비밀번호 유효 기간을 오늘부터 n일자로 생성
- 별도로 명시하지 않는 경우 `default_password_lifetime` 시스템 변수에 유효기간으로 설정
```mysql
mysql> show global variables like 'default_password_lifetime';
+---------------------------+-------+
| Variable_name             | Value |
+---------------------------+-------+
| default_password_lifetime | 0     |
+---------------------------+-------ㅏ+
```
- 개발자나 데이터베이스 관리자의 비밀번호는 유효기간을 설정하는 것이 보안상 안전
- <u>단 응용 프로그램 접속용 계정에 유효 기간을 설정하는 것은 위험할 수 있음</u>


### PASSWORD HISTORY
- 한 번 사용했던 비밀번호를 재사용하지 못하게 설정하는 옵션
	- `PASSWORD HISTORY DEFAULT`: password_history 시스템 변수에 저장된 개수만큼 비밀번호의 이력을 저장, 저장된 이력에 남아있는 비밀번호 재사용 불가
	- `PASSWORD HISTORY n`: 비밀번호 이력을 N개 까지 저장하며, 저장된 이력에 남아있는 비밀번호는 재사용 불가

```mysql
mysql> select * from mysql.password_history;
Empty set (0.00 sec)
```

### PASSWORD REUSE INTERVAL
- 한 번 사용했던 비밀번호의 재사용 금지 기간을 설정
	- `PASSWORD REUSE INTERVAL DEFAULT` : `password_reuse_interval` 변수에 저장된 기간으로 설정 ( 기본값 )
	- `PASSWORD REUSE INTERFVA n DAY` : n일자 이후에 비밀번호 재사용 할 수 있도록 설정
```mysql
mysql> show global variables like 'password_reuse%';
+-------------------------+-------+
| Variable_name           | Value |
+-------------------------+-------+
| password_reuse_interval | 0     |
+-------------------------+-------+
1 row in set (0.00 sec)
```

### PASSWORD REQUIRE
- 비밀번호가 만료되어 새로운 비밀번호를 변경할 때 현재 비밀번호를 필요로 할지 말지를 결정하는 옵션
	- `PASSWORD REQUIRE CURRENT` : 현재 비밀번호를 먼저 입력하도록 설정
	- `PASSWORD REQUIRE OPTIONAL` : 현재 비밀번호 입력하지 않아도 되도록 설정
	- `PASSWORD REQUIRE DEFAULT` : `password_require_current` : 시스템 변수의 값으로 설정

### ACCOUNT LOCK/UNLOCK
- 계정 생성 혹은 `ALTER USER` 명령을 사용해 계정 정보를 변경할 수 없도록 잠글지 여부를 정함
	- `ACCOUNT LOCK`: 계정을 사용하지 못하게 잠금
	- `ACCOUNT UNLOCK`: 잠긴 계정을 다시 사용 가능 상태로 잠금 해제

## 비밀번호 관리

### 고수준 비밀번호

MySQL 서버의 비밀번호는 유효기간이나 이력 관리를 통한 재사용 금지 기능뿐만 아니라 비밀번호를 쉽게 유추할 수 있는 단어들이 사용되지 않게 글자의 조합을 강제하거나 금칙어로 설정하는 기능도 있습니다.


MySQL 서버에서 비밀번호의 유효성 체크 규칙을 적용하려면 validate_password 컴포넌트를 이용하면 되는데 다음과 같이 `validate_component` 는 내장돼 있기 때문에 `install component` 를 통해서 설치 가능하다. 
```mysql
mysql> install component 'file://component_validate_password';
mysql> select * from mysql.component;
+--------------+--------------------+------------------------------------+
| component_id | component_group_id | component_urn                      |
+--------------+--------------------+------------------------------------+
|            1 |                  1 | file://component_validate_password |
+--------------+--------------------+------------------------------------+
```
`validate_password` 컴포넌트에서 제공하는 시스템 변수를 확인할 수 있습니다.
```mysql
mysql> show global variables like 'validate_password%';
+-------------------------------------------------+--------+                
| Variable_name                                   | Value  |
+-------------------------------------------------+--------+
| validate_password.changed_characters_percentage | 0      |
| validate_password.check_user_name               | ON     |
| validate_password.dictionary_file               |        |
| validate_password.length                        | 8      |
| validate_password.mixed_case_count              | 1      |
| validate_password.number_count                  | 1      |
| validate_password.policy                        | MEDIUM |
| validate_password.special_char_count            | 1      |
+-------------------------------------------------+--------+
8 rows in set (0.00 sec)
```

비밀번호 정책은 크게 다음 3가지에서 선택할 수 있습니다.
- LOW: 비밀번호의 길이만 검증
- MEDUM : 기본값이며, 비밀번호의 길이를 검증, 숫자, 대소문자, 특수문자의 배합
- STRONG: MEDIUM과 금칙어의 포함여부

금칙어 파일 같은 경우 한 줄에 하나씩 기록한 텍스트 파일을 작성하면 됩니다.
혹은 시스템 변수에 직접 추가할 수 있습니다.
```
set global validate_password.dictionary_file = 'prohibitive_word.data';
set glboal vaidate_password.policy='STRONG';
```

플러그인 위치
```shell
/usr/local/mysql/lib/plugin

total 32560
drwxr-xr-x  43 root  wheel     1376 Oct  7 16:42 .
drwxr-xr-x  21 root  wheel      672 Oct  7 16:42 ..
-rwxr-xr-x   1 root  wheel    76240 Jun 22 22:39 adt_null.so
-rwxr-xr-x   1 root  wheel   101696 Jun 22 22:39 authentication_fido_client.so
-rwxr-xr-x   1 root  wheel   102016 Jun 22 22:39 authentication_ldap_sasl_client.so
-rwxr-xr-x   1 root  wheel  6951984 Jun 22 22:39 authentication_oci_client.so
-rwxr-xr-x   1 root  wheel    76992 Jun 22 22:39 component_audit_api_message_emit.so
-rwxr-xr-x   1 root  wheel  1510016 Jun 22 22:39 component_keyring_file.so
-rwxr-xr-x   1 root  wheel    91504 Jun 22 22:39 component_log_filter_dragnet.so
-rwxr-xr-x   1 root  wheel    98800 Jun 22 22:39 component_log_sink_json.so
-rwxr-xr-x   1 root  wheel    74576 Jun 22 22:39 component_log_sink_syseventlog.so
-rwxr-xr-x   1 root  wheel   100144 Jun 22 22:39 component_mysqlbackup.so
-rwxr-xr-x   1 root  wheel    72256 Jun 22 22:39 component_query_attributes.so
-rwxr-xr-x   1 root  wheel   113472 Jun 22 22:39 component_reference_cache.so
-rwxr-xr-x   1 root  wheel   123072 Jun 22 22:39 component_validate_password.so
-rwxr-xr-x   1 root  wheel   123472 Jun 22 22:39 connection_control.so
-rwxr-xr-x   1 root  wheel   179712 Jun 22 22:39 ddl_rewriter.so
drwxr-xr-x  39 root  wheel     1248 Oct  7 16:42 debug
-rwxr-xr-x   1 root  wheel  3145232 Jun 22 22:39 group_replication.so
-rwxr-xr-x   1 root  wheel    94880 Jun 22 22:39 ha_example.so
-rwxr-xr-x   1 root  wheel    93072 Jun 22 22:39 ha_mock.so
-rwxr-xr-x   1 root  wheel   159040 Jun 22 22:39 innodb_engine.so
-rwxr-xr-x   1 root  wheel   195008 Jun 22 22:39 keyring_file.so
-rwxr-xr-x   1 root  wheel    76512 Jun 22 22:39 keyring_udf.so
lrwxr-xr-x   1 root  wheel       27 Oct  7 16:42 libcrypto.3.dylib -> ../../lib/libcrypto.3.dylib
lrwxr-xr-x   1 root  wheel       26 Oct  7 16:42 libfido2.1.dylib -> ../../lib/libfido2.1.dylib
-rwxr-xr-x   1 root  wheel   315552 Jun 22 22:39 libmemcached.so
-rwxr-xr-x   1 root  wheel  1362416 Jun 22 22:39 libpluginmecab.so
lrwxr-xr-x   1 root  wheel       39 Oct  7 16:42 libprotobuf-lite.3.19.4.dylib -> ../../lib/libprotobuf-lite.3.19.4.dylib
lrwxr-xr-x   1 root  wheel       34 Oct  7 16:42 libprotobuf.3.19.4.dylib -> ../../lib/libprotobuf.3.19.4.dylib
lrwxr-xr-x   1 root  wheel       24 Oct  7 16:42 libssl.3.dylib -> ../../lib/libssl.3.dylib
-rwxr-xr-x   1 root  wheel    53520 Jun 22 22:39 locking_service.so
-rwxr-xr-x   1 root  wheel    54448 Jun 22 22:39 mypluglib.so
-rwxr-xr-x   1 root  wheel   239152 Jun 22 22:39 mysql_clone.so
-rwxr-xr-x   1 root  wheel    53424 Jun 22 22:39 mysql_no_login.so
-rwxr-xr-x   1 root  wheel    70400 Jun 22 22:39 rewrite_example.so
-rwxr-xr-x   1 root  wheel   121824 Jun 22 22:39 rewriter.so
-rwxr-xr-x   1 root  wheel   175488 Jun 22 22:39 semisync_master.so
-rwxr-xr-x   1 root  wheel   102720 Jun 22 22:39 semisync_replica.so
-rwxr-xr-x   1 root  wheel   102976 Jun 22 22:39 semisync_slave.so
-rwxr-xr-x   1 root  wheel   175248 Jun 22 22:39 semisync_source.so
-rwxr-xr-x   1 root  wheel   100208 Jun 22 22:39 validate_password.so
-rwxr-xr-x   1 root  wheel   110000 Jun 22 22:39 version_token.so
```


### 이중 비밀번호
많은 응용 프로그램 서버들이 공용으로 데이터베이스 서버를 사용하기 때문에 데이터베이스 서버의 계정 정보는 응용 프로그램 서버로 부터 공용으로 사용됩니다. <u> 이런 특성으로 인해 데이터베이스 서버의 계정 정보는 쉽게 변경하기 어려우며, 데이터베이스 계정 비밀번호를 실행 중인 상태에서 변경이 불가능했습니다. </u> 
- 처음 설정한 상태로 몇 년동안 사용되는 경우
- 데이터베이스의 비밀번호를 주기적으로 변경해야 하지만 서비스를 모두 멈추지 않고서는 변경하기 어려웠다.

이를 해결하기 위해 MySQL 8.0 부터 계정의 비밀번호를 2개의 값을 동시에 사용할 수 있는 기능을 추가함
- 이중 비밀번호지만 둘 중 하나만 맞아도 상관없음

MySQL 서버의 이중 비밀번호 기능은 하나의 계정에 대해 2개의 비밀번호를 동시에 설정한다.
- 각각 프라이머리와 세컨더리로 구분
- 최근에 설정된 비밀번호가 프라이머리
- 이전 비밀번호가 세컨더리
- 변경하려면 `CURRENT PASSWORD` 옵션 추가

```mysql
ALTER USER 'root@localhost' IDENTIFIED BY 'old_password'; # root 계정의 프라이머리 비밀번호가 old_password
ALTER USER 'root@localhost' IDENTIFIED BY 'new_password' RETAIN CURRENT PASSWORD; # old_password가 세컨더리에 등록 new_password가 프라이머리로 등록
ALTER USER 'root@localhost' DISCARD OLD PASSWORD
```
이 방법으로 모든 애플리케이션이 프라이머리 비밀번호로 전환되면 세컨드리 비밀번호는 삭제합니다.


## 권한

MySQL 5.7 버전까지 권한은 Global권한과 객체 단위의 권한으로 구분됐습니다. 
- 데이터베이스나 테이블 이외의 객체에 적요되는 권한을 글로벌(Global) 권한
	- GRANT 명령어로 권한을 부여할 때 명시X
- 데이터베이스나 테이블을 제어하는데 필요한 권한을 객체 권한
	- GRANT 명령어로 권한을 부여할 때 반드시 특정 객체를 명시
 - 예외적으로 ALL은 글로벌과 객체 권한 두 가지 용도로 사용 하는데, 특정 객체에 ALL권한이 부여되면 해당 객체에 적용될 수 있는 모든 객체 권한을 부여하며, 글로벌로 ALL이 사용되면 글로벌 수준에서 가능한 모든 권한을 부여함
	- 실무 경험이 없다보니 왜 그런 차이가 있는지 궁금함
- MySQL 8.0 버전부터 5.7버전의 권한에 동적 권한이 더 추가 됌
- 5.7 이전 버전을 정적 권한이라고 부름


## 역할 
MySQL 8.0 버전 부터는 권한을 묶어서 역할(Role)을 사용할 수 있게 됐습니다. 실제 MySQL 서버 내부적으로 역할(ROLE)은 계정과 같은 보습을 하고 있습니다. 
```mysql
CREATE ROLE
 role_emp_read,
 role_emp_write;
```
`CREATE_ROLE` 명령에서는 빈 껍데기만 있는 역할을 정의한 것이며 GRANT 명령으로 각 역할에 대해 실질적인 권한을 부여할 수 있습니다.
```
mysql> GRANT SELECT ON employees.* TO role_emp_read;
Query OK, 0 rows affected (0.00 sec)

mysql> GRANT INSERT, UPDATE, DELETE ON employees.* TO role_emp_write;
Query OK, 0 rows affected (0.01 sec)
```
employees DB의 모든 테이블에 select 권한만 부여하거나
employees DB의 모든 테이블에 CUD 권한을 부여할 수 있습니다.

역할은 그 자체로 사용될 수 없고 계정에 부여해야 하므로 다음과 같은 방식으로 사용자를 생성할 수 있습니다.
```mysql
mysql> CREATE USER reader@'127.0.0.1' IDENTIFIED BY 'Qwer!234';
Query OK, 0 rows affected (0.01 sec)

mysql> CREATE USER writer@'127.0.0.1' IDENTIFIED BY 'Qwer!234';
Query OK, 0 rows affected (0.00 sec)

```

```mysql
mysql -h127.0.0.1 -ureader -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 43
Server version: 8.0.34 MySQL Community Server - GPL

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show tables;
ERROR 1046 (3D000): No database selected
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| performance_schema |
+--------------------+
2 rows in set (0.01 sec)
```