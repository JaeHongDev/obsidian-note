---
cssclasses:
  - my_style_width_100
---
[[플러그인 스토리지 엔진 모델]]
MySql 8.0 부터는 기존의 플러그인 아키텍처를 대처하기 위해 컴포넌트 아키텍처가 지원됩니다. MySQL 서버의 플러그인은ㄷ 다음과 같은 몇 가지 단점이 있는데, 컴포넌트는 이러한 단점들을 보완해서 구현됐다.
- 플러그인은 오직 MYSQL 서버와 인터페이스할 수 있고, 플러그인끼리는 통신할 수 없음
- 플러그인은 MySQL 서버의 변수나 함수를 직접 호출하기 때문에 안전하지 않음
- 플러그인은 상호 의존 관계를 설정할 수 없어서 초기화가 어려움

MySQL 5.7 버전까지는 비밀번호 검증 기능이 플러그인 형태로 제공됐지만 MySQL 8.0의 비밀번호 검증 기능은 컴포넌트로 개선됐다. 
```mysql
mysql> select * from mysql.component;
Empty set (0.00 sec)

mysql> install component 'file://component_validate_password';
Query OK, 0 rows affected (0.04 sec)

mysql> select * from mysql.component;
+--------------+--------------------+------------------------------------+
| component_id | component_group_id | component_urn                      |
+--------------+--------------------+------------------------------------+
|            1 |                  1 | file://component_validate_password |
+--------------+--------------------+------------------------------------+
1 row in set (0.00 sec)
```