트랜잭션의 커밋 처리 시점이 아닌 트랜잭션이 변경한 데이터를 기준으로 병렬 처리 가능 여부를 결정한다.

기존의 잠금 기반 방식에서는 다음과 같이 커밋 처리 시점이 전혀 겹치지 않는 두 트랜잭션은 병렬로 실행될 수 없었다.
