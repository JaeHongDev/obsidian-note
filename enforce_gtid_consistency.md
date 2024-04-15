## 정의
`enforce_gtid_consistency` 시스템 변수는 GTID 기반 복제에서 소스 서버와 레플리카 서버 간의 데이터 일관성을 해칠 수 있는 쿼리들이 MySQL 서버에서 실행되는 것을 허용할지를 제어하는 시스템 변수입니다. 


enforce_gtid_consistency옵션을 사용할 떄 아래 패턴의 쿼리들은 사용을 금지합니다.
- `트랜잭션을 지원하는 테이블과 지원하지 않는 테이블을 함께 변경하는 쿼리, 트랜잭션`
- `CREATE TABLE ...SELECT ... 구문`
- `트랜잭션 내에서 CREATE TEMPORARY TABLE, DROP TEMPORARY TABLE 구문 사용`

사용을 금지 하는 이유는 소스 서버에서 레플리카 서버로 복제되어 적용될 때 단일 트랜잭션으로 처리되지 않을 수도 있습니다. 


## 값
항상 ON을 사용하는 것을 권장
![[Pasted image 20240409134107.png]]