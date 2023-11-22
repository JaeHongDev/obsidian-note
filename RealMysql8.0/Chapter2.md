---
cssclasses:
  - my_style_width_100
---
MySQL 서버는 다양한 형태로 설치할 수 있지만 <u>가능한 리눅스의 RPM이나 운영체제별 인스톨러를 이용하기를 권장한다.</u>
- Tar 또는 Zip으로 압축된 버전
- 리눅스 RPM 설치 버전(운도우 인스톨러 및 macOS 설치 패키지)
- 소스코드 빌드

[[소스코드 설치가 비권장 사항인 이유]]

###  ✅ 버전과 에디션(엔터프라이즈와 커뮤니티) 선택

MySQL 서버의 버전을 선택할 때는 다른 제약 사항이 없습니다. 가능한 최신 버전을 설치하는 것이 좋습니다.(진짜?) [[MySQL 최신 버전을 권장하는 이유?]]
- 서비스를 진행하면서 DBMS를 테스트해갈 수 있다.
	- <u>근데 이거 말고 다른 장점이 없는데?</u>
	- 이게 진짜 장점이라고 생각하기에는 위험 가능성이 있지 않나?
	- <u>아 책에서도 갓 출시된 메이저 버전을 선택하는 것은 위험하다고 말하네</u>
- <u>단 갓 출시된 메이저 버전의 경우 많은 변경이 이루어졌기 때문에 치명적이거나 보완는데 많은 시간이 걸릴 수 있다.</u>


초기 버전의 MySQL 서버는 엔터프라이즈 에디션과 커뮤니티 에디션으로 나뉘어 있기는 했지만 실제 MySQL 서버의 기능에 차이가 있는 것이 아닌 기술적이 차이만 존재했습니다. 하지만 Mysql 5.5 버전부터는 커뮤니티와 엔터프라이즈 에딕션의 기능이 달라지면서 소스코드도 달라졌고, MySQL 엔터프라이즈 에디션의 소스코드는 더이상 공개되지 않습니다.

### 🤔 그러면 엔터프라이즈, 커뮤니티 에디션은 다르다고 봐야하나요?
MySQL 서버의 사용화 전략의 핵심 내용은 엔터프라이즈 에디션과 커뮤니티 에디션 모두 동일합니다. 다만 특정 부가 기능들만 사용 버전인 엔터프라이즈 에디션에 포함되는 방식입니다. 이런 사용화 방식을 [[오픈코어모델]] 이라고 합니다. 
엔터프라이즈 에디션에서 제공되는 기능은 다음과 같습니다.
- Thread Pool
- Enterprise Audit
- Enterprise TDM(Master Key 관리)
- Enterprise Firewall
- Enterprise Monitor
- Enterprise Backup
- MySQL 기술 지원

### MySQL 설치

#### 리눅스 서버의 Yum인스톨러 설치
[[Yum(Yellodog Update Modeified)]]   인스톨러를 이용하려면 MySQL 소프트웨어 리포지터를 등록해야 하는데 이를 이해서 <u>MySqQL 다운로드 페이지에서 RPM 설치 파일을 직접 받아서 설치해야 합니다.</u>

**설치페이지**
https://dev.mysql.com/downloads/repo/yum/

Rpm 설치
```
# wget https://dev.mysql.com/get/mysql80-community-release-fc37-2.noarch.rpm
--2023-10-07 07:23:01--  https://dev.mysql.com/get/mysql80-community-release-fc37-2.noarch.rpm
Resolving dev.mysql.com (dev.mysql.com)... 104.76.87.97, 2600:1410:1000:2ba::2e31, 2600:1410:1000:294::2e31
Connecting to dev.mysql.com (dev.mysql.com)|104.76.87.97|:443... connected.
HTTP request sent, awaiting response... 302 Moved Temporarily
Location: https://repo.mysql.com//mysql80-community-release-fc37-2.noarch.rpm [following]
--2023-10-07 07:23:01--  https://repo.mysql.com//mysql80-community-release-fc37-2.noarch.rpm
Resolving repo.mysql.com (repo.mysql.com)... 23.15.137.78, 2600:1417:a000:69e::1d68, 2600:1417:a000:6a7::1d68
Connecting to repo.mysql.com (repo.mysql.com)|23.15.137.78|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 10524 (10K) [application/x-redhat-package-manager]
Saving to: 'mysql80-community-release-fc37-2.noarch.rpm'

mysql80-community-release-fc37-2.noarch.rpm             100%[=============================================================================================================================>]  10.28K  --.-KB/s    in 0s

2023-10-07 07:23:02 (94.4 MB/s) - 'mysql80-community-release-fc37-2.noarch.rpm' saved [10524/10524]
```

Yum 리포지터리 등록
```
# rpm -Uvh mysql80-community-release-fc37-2.noarch.rpm
rpm: RPM should not be used directly install RPM packages, use Alien instead!
rpm: However assuming you know what you are doing...
warning: mysql80-community-release-fc37-2.noarch.rpm: Header V4 RSA/SHA256 Signature, key ID 3a79bd29: NOKEY
Verifying...                          ################################# [100%]
Preparing...                          ################################# [100%]
Updating / installing...
   1:mysql80-community-release-fc37-2 ################################# [100%]
```

설치정보 확인
```
# ls -al -alh /etc/yum.repos.d/*mysql*
-rw-r--r-- 1 root root 1.3K Jul 10 13:39 /etc/yum.repos.d/mysql-community-debuginfo.repo
-rw-r--r-- 1 root root 1.2K Jul 10 13:39 /etc/yum.repos.d/mysql-community-source.repo
-rw-r--r-- 1 root root 1.1K Jul 10 13:39 /etc/yum.repos.d/mysql-community.repo
```

Yum 인스톨러 명령을 이용한 버전별 설치 가능한 MySQl 소프트웨어 목록 확인


### macOS용 DMG 패키지 설치
macOS에서 인스톨러로 설치하려면 설치에 필요한 DMG 패키지 파일들을 직접 다운로드해야 합니다.

https://dev.mysql.com/downloads/mysql/


MySQL 서버를 사설 네트워크에서만 사용한다면 `Use Legacy Password Encryption`을 선택해도 괜찮지만 MySQL 서버에 접속하게 된다면 `Use Strong Password Encryption`을 선택하자.

> 갑자기 든 생각인데 MySQL은 패스워드를 어떻게 관리하는거지?

MySQL 서버를 설치할 때 기본 설정으로 설치하면 데이터 디렉터리와 로그 파일들을 `usr/local/mysql` 디렉터리 하위에 생성하고 관리자 모드로 MySQL 서버 프로세스를 기동하기 때문에 관리자 계정에 대한 비밀번호 설정이 필요합니다.

```shell
ps -ef | grep mysqld
   74 10994     1   0  4:43PM ??         0:01.72 /usr/local/mysql/bin/mysqld --user=_mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data --plugin-dir=/usr/local/mysql/lib/plugin --log-error=/usr/local/mysql/data/mysqld.local.err --pid-file=/usr/local/mysql/data/mysqld.local.pid --keyring-file-data=/usr/local/mysql/keyring/keyring --early-plugin-load=keyring_file=keyring_file.so
  501 11203 11024   0  4:46PM ttys000    0:00.00 grep mysqld
  
```

MySQL 서버가 설치된 디렉터리는 `/usr/local/mysql` 이며, 하위의 각 디렉터리는 다음과 같습니다. 
- `bin` : MySQL 서버와 클라이언트 프로그램, 유틸리티를 위한 디렉터리
- `data` : 로그 파일과 데이터 파이들이 저장되는 디렉터리
- `include` : C/C++ 헤더 파일들이 저장된 디렉터리
- `lib`: 라이브러리 파일들이 저장된 디렉터리
- `share`: 다양한 지원 파일들이 저장돼 있으며, 에러 메시지나 샘플 설정 파일 (`my.cnf`)이 있는 디렉터리

MacOS에 설치된 MySQL 서버의 설정 파일(my.cnf) 등록 및 시작과 종료는 모두 `시스템 환경 설정`의 최하단에 있는 MySQL을 클릭하면 실행되는 MySQL 관리 프로그램에서 수행할 수 있다.

![[Pasted image 20231007172759.png]]

위 화면에서 서버를 실행하고 종료할 수 있다. 다른 방법으로 터미널에서도 다음과 같은 명령어를 통해서 실행, 종료가 가능하다.

```shell
### MySQL 서버 시작
sudo /usr/local/mysql/support-files/mysql.server start
Password:
Starting MySQL
.Logging to '/usr/local/mysql/data/dev.local.err'.
.............................................

### MySQL 서버 종료
sudo /usr/local/mysql/support-files/mysql.server stop
Password:
 ERROR! MySQL server PID file could not be found!
```


## MySQL 서버의 시작과 종료

### 설정 파일 및 데이터 파일 준비

리눅스 서버에서 Yum 인스톨러는 RPM을 이용해서 MySQL 서버를 설치하면 MySQL 서버에 필요한 프로그램들과 디렉터리들은 일부 준비되지만 트랜잭션 로그 파일과 시스템 테이블이 준비되지 않았기 때문에 MySQL 서버를 실행시킬 수 없습니다. 이때 MySQL 서버가 설치되면 `/etc/my.cnf` 설정 파일이 준비되는데, 3 ~ 4개의 아주 기본적인 설정만 등록돼있습니다.

<u>테스트용도로는 충분하지만 일반 서비스용으로 MySQL 서버를 설치한다면 충분한 설치 준비가 필요합니다.</u>

(내용이 더 있는데 리눅스 환경이라서 테스트를 못해봄 나중에 오라클 리눅스로 직접 시도해볼 예정)

### 시작과 종료
유닉스 계열 운영체제에서 RPM 패키지로 MySQL을 설치했다면 자동으로 `/usr/lib/systemd/system/mysqld.service` 파일이 생성되고, `systemctl` 유틸리티를 이용해 MySQL을 기동하거나 종료하는 것이 가능합니다.

> 주의
> 이전 예제ㅇ

(마찬가지로 리눅스 환경으로 테스트해서 확인해볼 내용)


### 서버 연결 테스트
MySQL 서버에 접속하는 방법은 MySQL 서버 프로그램와 함께 설치된 MySQL 기본 클라언트 프로그램인 mysql을 실행하면 된다.
```shell
mysql -uroot -p --host=localhost --socket=/tmp/mysql.sock // 1
mysql -uroot -p --host=127.0.0.1 --port=3306 // 2
mysql -uroot -p  // 3
```

- 첫 번째 예제는 MySQL 소켓 파일을 이용해 접소하는 예제입니다. 
- 두 번째 예제는 TCP/IP를 통해 127.0.0.1(로컬호스트)로 예제입니다.
	- <u> TCP/IP를 통해 접근하는 경우에는 포트를 명시하는 것이 일반적입니다.</u>
	- 보통 원격 mysql 서버에 접근할 때 주로 사용하는 방법입니다.
- 세 번째 예젠는 별도의 호스트 주소와 포트를 명시하지 않는 방법입니다
	- 기본값으로 호스트는 localhost가 되며 소캣 파일을 사용하게 되는데 소캣 파일의 위치는 MySQL 설정 파일에서 읽어서 사용합니다. 

여기서 localhost로 명시하는 것과 127.0.0.1로 명시하는 것은 의미가 다르다. --host=localhost 옵션을 사용하는 경우 MySQL 클라이언트 프로그램은 항상 소켓 파일을통해 MySQL 서버에 접속하게 되는데, 이는 `Unix domain socket` 을 이용하는 방식으로 TCP/IP를 통한 통신이 아닌 유닉스의 프로세스 간 통신의 일종입니다. 
하지만 127.0.0.1을 사용하는 경우네는 가지 서버를 가리키는 루프백 IP이기는 하지만 TCP/IP 통신 방식을 사용하는 것입니다.


MySQL 서버에 접속했다면 `SHOW DATABASES` 명령으로 데이터베이스의 목록을 확인할 수 있습니다.

```mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 26
Server version: 8.0.34 MySQL Community Server - GPL

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.00 sec)
```

MySQL서버에 직접 로그인하지 않고 원격 서버에서 MySQL 서버의 접속 가능 여부만 확인하는 방법이 존재합니다. 
- telent
- NetCat
위 명령을 이용해서 원격지 MySQL 서버가 응답 가능한 상태인지 확인해볼 수 있습니다.

```shell
nc localhost 3306
J
8.0.34(3mP\�ElU(KsS!caching_sha2_password
```
자가 깨져 정확한 내용을 알 수 없지만 Telnet과 Netcat 프로그램이 출력한 내용에서 MySQL 서버의 버전 정보를 정상적으로 보내준 것을 알 수 있다. 이렇게 해서 서버가 보내준 메시지를 ㅜㄹ력한다면 네트워크 수준의 연결은 정상적임을 알 수 있다.

#### -uroot 와 -u root 의 차이점은 뭐지?
gpt말로는 -uroot나 -u root가 동일한 명령어라고 하는데 왜죠..? -u옵션만 그런건가..? 나중에 사용자 생성하고 난다음에 테스트 해봐야징


## MySQL 서버 업그레이드

MySQL 서버를 업그레이드하는 두 가지 방법이 있습니다.
1. MySQL 서버의 데이터 파일을 그대로 두고 업그레이드 하는 방법
2. `mysqldump` 도구 등을 이용해 MySQL 서버의 데이터를 SQL 문장이나 텍스트 파일로 덤프한 후, 새로 업그레이드된 버전의 MySQL 서버에서 덤프된 데이터를 적재하는 방법

1번 방벙을 [[인플레이스 업그레이드(IN-PLACE-UPGRADE)]] 라고 하며 2번 방법을 [[논리적 업그레드(Logical Upgrade)]] 라고 합니다.

### 인플레이스 업그레이드 제약사항

업그레이드에는 두 가지를 생각해볼 수 있습니다.
- 마이너(패치) 버전 간 업그레이드
- 메이저 (패치) 버전 간 업그레이드

동일 메이저 버전에서 마이너 버전 간 업그레이드는 대부분 데이터 파일의 변경 없이 진행되며, 많은 경우 여러 버전을 건너뛰어서 업그레이드 하는 것도 허용합니다.
하지만 메이저 버전 간 업그레이드는 대부분 크고 작은 데이터 파일의 변경이 필요하기 때문에 반드시 직전 버전에서만  업그레이드가 허용됩니다.
- MySQL 5.5 -> MySQL 5.6은 가능
- MySQL 5.5 -> MySQL 5.7, 8.0 은 불 가능
	- 메이저 버전 업그레이드는 데이터 파일의 패치가 필요한데, MySQL 8.0 서버 프로그램은 직전 메이저 버전은 MYSQL 5.7 버전에서 사용하던 데이터 파일과 로그 포맷만 인식하도록 구현되기 때문이다.
	 - 즉 직전 버전만 데이터 파일과 로그 포맷만 인식함
- 만약 MySQL 5.1 에서 8.0으로 가려면 다음과 같은 단계를 건너야 함
	- 5.1 -> 5.5 -> 5.6 -> 5.7 -> 8.0
	- 상당히 번거로운 과정이기에 두 단계 이상을 합 번에 업그레이드 한다면 `mysqldump` 프로그램 MySQL 서버에서 데이터를 백업받은 후 새로 구축된 MySQL 8.0 서버에 데이터를 적재하는 [[논리적 업그레드(Logical Upgrade)]] 가 더 나은 방법일 수 있습니다.

추가적으로 주의해야 할 점은 버전 업그레이드가 특정 마이너 버전에서만 가능한 경우가 있습니다.
- 예를 들어 MySQL 5.7.8 버전을 사용 중이면 MySQL 서버 8.0 버전으로 바로 업그레이드 할 수 없습니다.
- 이는 5.7.8 버전이 [[GA버전]]이 아니기 때문입니다. 

### MySQL 8.0 업그레이드 시 고려사항

MySQL 8.0에서 상당히 많은 기능들이 개선되거나 변경됐습니다. 변경후 MySQL 8.0 에서는 사용할 수 없는 기능들이 있습니다.
- `사용자 인증 방식 변경` : MySQL 8.0 버전부터는 [[Caching SHA-2 Authentication]] 인증 방식이 기본 인증 방식으로 바뀌었습니다. MySQL 5.7에 존재했던 사용자 계정은 여전히 Native Authentication 인증 방식을 사용합니다. 
	- 단 Native Authentication 인증 방식을 사용하고자 한다면 MySQL 서버를 시작할 때  다음 ```--default-authentication-plugin=mysql_native_password``` 파라미터를 활성화 해야 합니다.
-  `MySQL 8.0 과의 호환성 체크` : MySQL 8.0 업그레이드 전에 MySQL 5.7 버전에서 손상된 [[FRM(MySQL)]] 파일이나 호환되지 않는 데이터 타입 또는 함수가 있는 mysqlcheck 유틸리티를 통해 확인하는 것을 권장합니다.
- [[외래키(Foreign Key)]] 이름의 길이: MySQL 8.0에서는 [[외래키(Foreign Key)]] 의 이름이 64글자로 제한됩니다.
- Group By에 사용된 정렬 옵션: MySQL 5.x에서 GROUP BY 절의 컬럼 뒤에 'ASC' 나 'DESC'를 사용한다면 제거해야합니다.
- 파티션을 위한 공용 테이블스페이스: MySQL 8.x에서는 파티션의 각 테이블스페이스를 공용 테이블스페이스에 저장할 수 없다.

```mysql
# 이거 왜 됌?
mysql> select version();
+-----------+
| version() |
+-----------+
| 8.0.34    |
+-----------+
1 row in set (0.00 sec)

mysql> SELECT id1 FROM t3 group by id1 order by id1 desc
    -> ;
+-------------------------------------------------------------------+
| id1                                                               |
+-------------------------------------------------------------------+
| aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa |
+-------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### MySQL 업그레이드 체크

```shell
linux> mysqlcheck -u root -p --all-databases --check-update

mysql.columns_priv                                 Table is already up to date
mysql.component                                    Table is already up to date
mysql.db                                           Table is already up to date
mysql.default_roles                                Table is already up to date
mysql.engine_cost                                  Table is already up to date
mysql.func                                         Table is already up to date
mysql.general_log                                  Table is already up to date
mysql.global_grants                                Table is already up to date
mysql.gtid_executed                                Table is already up to date
mysql.help_category                                Table is already up to date
mysql.help_keyword                                 Table is already up to date
mysql.help_relation                                Table is already up to date
mysql.help_topic                                   Table is already up to date
mysql.innodb_index_stats                           Table is already up to date
mysql.innodb_table_stats                           Table is already up to date
mysql.ndb_binlog_index                             Table is already up to date
mysql.password_history                             Table is already up to date
mysql.plugin                                       Table is already up to date
mysql.procs_priv                                   Table is already up to date
mysql.proxies_priv                                 Table is already up to date
mysql.replication_asynchronous_connection_failover Table is already up to date
mysql.replication_asynchronous_connection_failover_managed Table is already up to date
mysql.replication_group_configuration_version      Table is already up to date
mysql.replication_group_member_actions             Table is already up to date
mysql.role_edges                                   Table is already up to date
mysql.server_cost                                  Table is already up to date
mysql.servers                                      Table is already up to date
mysql.slave_master_info                            Table is already up to date
mysql.slave_relay_log_info                         Table is already up to date
mysql.slave_worker_info                            Table is already up to date
mysql.slow_log                                     Table is already up to date
mysql.tables_priv                                  Table is already up to date
mysql.time_zone                                    Table is already up to date
mysql.time_zone_leap_second                        Table is already up to date
mysql.time_zone_name                               Table is already up to date
mysql.time_zone_transition                         Table is already up to date
mysql.time_zone_transition_type                    Table is already up to date
mysql.user                                         Table is already up to date
sample.t1                                          Table is already up to date
sample.t2                                          Table is already up to date
sample.t3                                          Table is already up to date
sys.sys_config                                     Table is already up to date
```

### MySQL 8.0 업그레이드
MySQL 5.7에서 8.0으로 업그레이드 하는 과정은 단순하지는 않습니다. 사용자의 눈에 보이는 것은 차이가 없지만 MySQL 서버가 내부적으로 진행하는 업그레이드 과정은 상당히 복잡합니다. 
- `데이터 딕셔너리 업그레이드`: MySQL 5.7 버전까지는 데이터 딕셔너리 정보가 [[FRM(MySQL)]] 확장자를 가진 파일로 별도로 보관됐었는데 8.0부터 딕셔너리 정보가 트랜잭션이 지원되는 InnoDB 시스템 테이블로 저장한다.
- `서버 업그레이드` MySQL 서버의 시스템 데이터베이스의 테이블 구조를 MySQL 8.0 버전에 맞게 변경한다.

(참고)
지금까지 MySQL 서버의 버전을 업그레이드하고도 mysql_upgrade 유틸리티를 실행하지 않아서 이런 저런 이슈가 발생했다. 하지만 이제부터 MySQL 서버가 업그레이드됐다면 MySQL 서버 프로그램이(mysqld) 가 시작되면서 자동으로 필요한 작업을 수행하기 때문에 사용자 실수를 더 줄일 수 있습니다.

## 서버 설정

MySQL 서버는 단 하나의 설정 파일을 사용한다.
- my.cnf: 리눅스를 포함한 유닉스 계열에서 사용
- my.imi: 윈도우 계열에서 사용

MySQL 서버는 지정한 여러 개의 디렉터리를 순차적으로 탐색하면서 처음 발견된 my.cnf 파일을 사용한다.
```shell
mysqld --verbose --help
mysqld  Ver 8.0.23 for osx10.15 on x86_64 (Homebrew)
Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Starts the MySQL database server.

Usage: mysqld [OPTIONS]

Default options are read from the following files in the given order:
/etc/my.cnf /etc/mysql/my.cnf /usr/local/etc/my.cnf ~/.my.cnf
```
MySQL  서버나 클라이언트 프로그램이 my.cnf 파일을 찾는 순서는 다음과 같다. [[my.cnf]]
1. /etc/my.cnf
2. /etc/mysql/my.cnf
3. /usr/etc/my.cnf
4. ~/.my.cnf 

실제로 MySQL 서버는 단 하나의 설정 파일만 사용하지만 설정 파일이 위치한 디렉터리는 여러 곳일 수 있다. <u>즉 하나만 사용하지만 어느 파일을 실행했는지 쉽게 알 수 없는 문제점이 있다.  그렇기 때문에 `mysqld --verbose --help` 명령어로 어떤 파일을 먼저 찾는지 확인하는 것도 하나의 방법이다.</u>

참고로 주로 MySQL 서버 파일은 주로 1,2번을 사용하는데 하나의 장비에 2개 이상의 MySQL 서버를 실행하는 경우 1번과 2번은 충돌이 발생할 수 있으므로 공유된 디렉터리가 아닌 별도의 디렉터리에 설정 파일을 준비하고 MySQL 서버를 실행하는 경우 1,2번은 충돌이 발생할 수 있으므로 공유된 디렉터리가 아닌 별도 디렉터리에 설정 파일을 준비하고 실행 스크립트를 변경하는 방법을 사용한다. 단 그렇게 실행하는 형태로 준비되는 경우는 없다.  
(<u> MySQL 버전 업그레이드 하면서 데이터를 dump 하는 경우가 있지 않을까 싶습니다. </u>)

### 설정 파일의 구성

MySQL 설정 파일은 하나의 [[my.cnf]] 파일에 여러개의 설정 그룹을 담을 수 있으며, 대체로 실행 프로그램 이름을 그룹명으로 사용한다
```shell
# Default Homebrew MySQL server config
[mysqld] -> mysqld 그룹에 적용되는 설정
# Only allow connections from localhost
bind-address = 127.0.0.1
mysqlx-bind-address = 127.0.0.1

```
<u>일반적으로 중복된 설정이 나열되는 경우는 없지만 socket이나 port같은 설정은 모든 프로그램에 공통으로 필요한 설정값같은 경우에 주로 사용합니다.</u>


### MySQL 시스템 변수의 특징 

MySQL 서버는 기동하면서 설정 파일의 내용을 읽어 메모리나 작동 방식을 초기화하고, 접속도니 사용자를 제어하기 위해 이러한 값을 별도로 저장해 둔다.
이렇게 저장된 값을 [[MySql.시스템 변수(System Variables)]] 라고 합니다.
아래 명령어로 현재 [[MySql.시스템 변수(System Variables)]] 를 확인할 수 있습니다.
```shell
SHOW GLOBAL VARIABLES;
SHOW VARIABLES;
```

시스템 변수 값이 어떻게 MySQL 서버와 클라이언트에 영향을 미치는지 판단하려면 각 변수가 글로벌 변수인지 세션 변수인지 구분할 수 있어야 합니다.

### 글로벌 변수와 세션 변수

MySQL의 시스템 변수는 적용 범위에 따라 글로벌 변수와 세션 변수로 나뉩니다. <u>글로벌로 적용 될 수 있으며, 세션에도 적용가능한 경우에는 `Both` 로 표기합니다</u>

- 글로벌 범위의 시스템 변수는 하나의 MySQL 서버 인스턴스에서 전체적으로 영향을 미치는 시스템 변수를 의미하며, 주로 MySQL 서버 자체 관련된 설정입니다.
	- MySQL 서버에서 단 하나만 존재하는 `InnoDB`버퍼 풀 크기  또는 키 캐시 크기가 가장 대표적인 글로벌 영역의 시스템 변수입니다.
- 세션 범위의 시스템 변수는 MySQL 클라이언트가 MySQL 서버에 접속할 때 기본적으로 부여하는 옵션의 기본값을 제어하는데 사용된다. 
	- autocommit을 ON으로 설정하면 해당 서버에 접속하는 모든 커넥션은 기본으로 자동 커밋 모드로 시작되지만 각 커넥션에서 autocommit 변수의 값을 OFF로 변경해 자동 커밋모드를 ㅂ활성화 할 수 있습니다. 
	- 이러한 세션 변수는 커넥션별로 설정값을 서로 다르게 지정할 수 있지만 한번 연결된 커넥션의 세션 변수는 서버에서 강제로 변경할 수 없습니다.
- 세션 범위의 시스템 변수 가운데 [[my.cnf]] 에 명시해 초기화 할 수 있으며 대부분 `Both` 로 명시돼 있습니다. 
	- Session이라고 명시된 시스템 변수만 MySQL 서버의 설정 파일에 초깃값을 명시할 수 없으며 커넥션이 만들어지는 순간부터 해당 커넥션에만 유효합니다. 
	- Both로 명시된 시스템 변수는 서버가 기억해둔 다음 실제 클라이언와 커넥션이 실행되는 순간에 해당 커넥션의 기본값으로 사용됩니다. 

### 정적 변수와 동적 변수
MySQL 서버의 시스템 변수는 MySQL 서버가 기동중인 상태에서 변경 가능한지에 따라 다음과 같이 구분 됩니다.
- 동적 변수
	-  이미 가동 중인 MySQL 서버의 메모리에 있는 MySQL 서버의 시스템 변수를 변경
- 정적 변수
	- MySQL 시스템 변수는 디스크에 저장돼 있는 [[my.cnf]] 파일을 변경하는 경우와

디스크에 저장된  설정 파일의 내용은 변경하더라도 MySQ 서버가 재시작하기 전에는 적용되지 않습니다. 단 `SHOW` 명령으로 MySQL 서버에 적용된 변숫값을 확인하거나 `SET` 명령을 이용해 값을 변경할 수 있습니다.
```
mysql -uroot -p
mysql> show global variables like '%max_connections%';
+------------------------+-------+
| Variable_name          | Value |
+------------------------+-------+
| max_connections        | 151   |
| mysqlx_max_connections | 100   |
+------------------------+-------+
2 rows in set (0.00 sec)

mysql> set global max_connections=500;
Query OK, 0 rows affected (0.00 sec)

mysql> show global variables like '%max_connections%';
+------------------------+-------+
| Variable_name          | Value |
+------------------------+-------+
| max_connections        | 500   |
| mysqlx_max_connections | 100   |
+------------------------+-------+
2 rows in set (0.00 sec)
```

주의할 점은 SET 명령어를 통해 변경되는 시스템 변숫값으 MySQL의 [[my.cnf]] 파일에 반영하는 것이 아니며 MySQL 인스턴스에서만 유효하다.
영구 적용을 이해서는 `SET PERSIST` 명령어를 사용하면 된다.

시스템 변수의 범위가 `Both` 인 경우에는 글로벌 시스템 변수의 값을 변경해도 이미 존재하는 세션 변숫값은 변경되지 않고 유지된다.
```mysql
mysql> show global variables like 'join_buffer_size';
+------------------+--------+
| Variable_name    | Value  |
+------------------+--------+
| join_buffer_size | 262144 |
+------------------+--------+
1 row in set (0.00 sec)

mysql> show variables like 'join_buffer_size';
+------------------+--------+
| Variable_name    | Value  |
+------------------+--------+
| join_buffer_size | 262144 |
+------------------+--------+
1 row in set (0.02 sec)

mysql> set global join_buffer_size=524288;
Query OK, 0 rows affected (0.01 sec)

+------------------+--------+
| Variable_name    | Value  |
+------------------+--------+
| join_buffer_size | 524288 |
+------------------+--------+
1 row in set (0.00 sec)

mysql> show variables like 'join_buffer_size';
+------------------+--------+
| Variable_name    | Value  |
+------------------+--------+
| join_buffer_size | 262144 |
+------------------+--------+
1 row in set (0.01 sec)
```

### SET PERSIST
MySQL 서버의 시스템 변수는 동적 변수와 정적 변수로 구분되는데 동적 변수의 경우 MySQL 서버에서 `SET GLOBAL` 명령으로 변경하면 즉시 MySQ 서버에 반영되는 것을 확인했습니다.

하지만 실제 [[my.cnf]] 파일에 저장되는 것이 아닌 MySQL 서버의 인스턴스에서 유효하기 때문에 `SET PERSIST` 명령어를 통해 실제로 반영할 수 있습니다.
- 단 `my.cnf` 파일에 저장되는 것이 아닌 별도의 설정 파일(mysqld-auto.cnf) 파일에 변경 내용을 기록하며 서버 실행시 두 파일을 읽어 드린 다음 메모리에 저장합니다 .
- 세션 변수에는 적용되지 않음

다음 재시작 할 떄 적용하고자 하면 `PERSIST_ONLY` 를 적용하면 됩니다.

```mysql
mysql> SET PERSIST_ONLY max_connections=5000;
Query OK, 0 rows affected (0.00 sec)

mysql> show global variables like 'max_connections';
+-----------------+-------+
| Variable_name   | Value |
+-----------------+-------+
| max_connections | 500   |
+-----------------+-------+
1 row in set (0.00 sec)
```

`sudo cat data/mysqld-auto.cnf`
```json
{
  "Version": 2,
  "mysql_dynamic_parse_early_variables": {
    "max_connections": {
      "Value": "5000",
      "Metadata": {
        "Host": "localhost",
        "User": "root",
        "Timestamp": 1696852117085036
      }
    }
  }
}   
```
mysqld-auto.cnf파일에는 다음과 같은 정보가 저장됩니다.
- JSON 포맷으로 정의
- 파일에는 변경된 시스템 변수의이름과 설정값,
- 언제 누구에 의해 시스템 변수가 변경됐는지 등의 정보

```
1696852117085036
**GMT**: 2023년 October 9일 Monday AM 11:48:37.085  
**Your time zone**: 2023년 10월 9일 월요일 오후 8:48:37.085 [GMT+09:00](https://www.epochconverter.com/timezones?q=1696852117085036 "convert to other time zones")  
```

직접 테이블을 통해 참조 할 수 있습니다. 
```mysql
mysql> SELECT a.variable_name, b.variable_value,
    -> a.set_time, a.set_user,a.set_host
    ->  FROM performance_schema.variables_info a
    ->  INNER JOIN performance_schema.persisted_variables b
    ->   ON a.variable_name = b.variable_name
    ->  where b.variable_name like 'max_connections'\G
*************************** 1. row ***************************
 variable_name: max_connections
variable_value: 5000
      set_time: 2023-10-09 19:48:58.076335
      set_user: root
      set_host: localhost
1 row in set (0.01 sec)
```

<u>여기서 만약 mysqld-auto.cnf 파일을 직접 수정하는 경우 오류가 발생하면 MySQL 서버가 시작되지 못할 수 있기 때문에 직접 명령어를 사용하는 것을 권장합니다.</u>

