GTID 모드를 전환할 때 사용되는 시스템 변수는 
- [[enforce_gtid_consistency]]
- [[gtid_mode]]
입니다. 



Non-GTID 기반 복제에서 다음과 같은 순서로 전환 작업이 진행됩니다. 
1. 각 서버에서 `enforce_gtid_consistency` 시스템 변수 값을 WARN으로 변경 
	- 설정 변경 후 서버의 동작 모니터링 문제가 없으면 다음 단계로 넘어감
2. 각 서버에서 `enforce_gtid_consistency` 시스템 변수 값을 ON으로 변경
3. 각 서버에서 `gtid_mode` 시스템 변수 값을 `off_permissive`로 변경
	- off_permissive로 변경하면 레플리카 서버에서만 복제 시 익명 트랜잭션, GTID 트랜잭션 처리
4. 각 서버에서 `gtid_mode` 시스템 변수 값을 `on_permissive`로 변경
5. 잔여 트랜잭션 확인
	1. `SHOW GLOBAL STATUS LIKE 'Ongoing_anoymous_transaction_count`
6. 각 서버에서 `git_mode` 시스템 변수 값을 ON으로 변경
7. `my.cnf` 파일 변경
8. GTID 기반 복제를 사용하도록 복제 설정 변경

