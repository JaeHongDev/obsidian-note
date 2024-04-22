
앞서 기록된 바이너리 로그 내용들을 디스크와 동기화하는 fsync시스템 콜이 수행 


sync_binlog옵션에 설정된 값에 따라 디스크가 동기화
- 1: FLUSH 단계에서 넘어온 전체 트랜잭션들에 대해 매번 디스크 동기화 작업 수행

Sync 단계의 대기 큐에 트랝개션들이 많이 쌓이면 쌓일수록 더 효율적이며 아래 두 시스템 변수를 통해 Sync 단계의 실행을 지연시킬 수 있습니다.

- binlog_group_commit_sync_delay
- binlog_group_commit_sync_no_delay_count

