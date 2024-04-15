
GTID기반 복제는 다음과 같은 제약 사항이 있습니다. 

1. GTID가 활성화된 MySQL 서버에서는 `enforce_gtid_cosistency=on` 옵션으로 인해 GTID 일관성을 해칠 수 있는 일부 유형의 쿼리들은 실행할 수 없습니다. 
2. GTID 기반 복제가 설정된 레플리카 서버에서는 `sql_slave_skip_counter` 시스템 변수를 사용해 복제된 트랜잭션을 건너뛸 수 없습니다. 
3. GTID 기반 복제에서 `CHANGE REPLICATION SOURCE TO`구문의 `IGNORE_SERVER_IDS` 옵션은 더 이상 사용되지 않습니다. 