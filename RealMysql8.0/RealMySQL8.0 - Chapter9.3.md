---
cssclasses:
  - my_style_width_100
---

# 고급 최적화
MySQL 서버의 옵티마이저가 실행 계획을 수립할 때 통계 정보와 옵티마이저 옵션을 결합해서 최적의 실행 계획을 수립합니다.
이 때 옵티마이저 옵션은 
- 옵티마이저 옵션
- 옵티마이저 스위치
두 가지로 구분할 수 있습니다.

여기서 옵티마이저 옵션은 조인이 많이 사용되는 서비스에서 꼭 알아야 하는 옵션입니다.
## 옵티마이저 스위치 옵션
- 옵티마이저 스위치는 MySQL 5.5버전부터 지원되기 시작했습니다.
- 옵티마이저 스위치 옵션은 `optimzer_switch` 시스템 변수를 이용해서 제어하는데, `optimizer_switch` 시스템 변수에는 여러 개의 옵션을 세트로 묶어서 설정하는 방식으로 사용합니다.
- `optimizer_switch` 시스템 변수에 설정할 수 있는 최적화 옵션은 다음과 같습니다.
```
`atched_key_access={on|off}`
`block_nested_loop={on|off}`
`condition_fanout_filter={on|off}`
`derived_condition_pushdown={on|off}`
`derived_merge={on|off}`
`duplicateweedout={on|off}`
`engine_condition_pushdown={on|off}`
`firstmatch={on|off}`
`hash_join={on|off}`
`index_condition_pushdown={on|off}`
`index_merge={on|off}`
`index_merge_intersection={on|off}`
`index_merge_sort_union={on|off}`
`index_merge_union={on|off}`
`loosescan={on|off}`
`materialization={on|off}`
`mrr={on|off}`
`mrr_cost_based={on|off}`
`prefer_ordering_index={on|off}`
`semijoin={on|off}`
`skip_scan={on|off}`
`subquery_materialization_cost_based={on|off}`
`subquery_to_derived={on|off}`
`use_index_extensions={on|off}`
`use_invisible_indexes={on|off}`
```
- 각각의 옵티마이저 스위치 옵션은 default, on, off 중에서 하나를 설정할 수 있는데, on으로 설정되면 해당 옵션을 활성화하고, off를 설정하면 해당 옵션을 비활성화한다.
- 그리고 default를 설정하면 기본값이 적용된다.
- 옵티마이저 스위치 옵션은 글로벌과 세션별 모두 설정할 수 있는 시스템 변수이므로 MySQL 서버 전체적으로 또는 현재 커넥션에 대해서만 다음과 같이 설정할 수 있다.
```mysql
// MySQL 서버 전체적으로 옵티마이저 스위치 설정
set global optimizer_switch='index_merge=on,index_merge_union=on,...'; 

// 현재 커넥션의 옽비마이저 스위치만 설정
set session optimizer_switch='index_merge=on,index_merge_union=on,...';
```
- 또한 다음과 같이 "SET_VAR" 옵티마이저 힌트를 이용해 현재 쿼리에만 설정할 수 있습니다.
```mysql
select /*+ SET_VAR(optimizer_switch='condition_fanout_filter=off'*/ 
 from ...
```

### MRR 배치 키 인덱스 (mrr & batched_key_access)
MRR은 `Multi-Range Read` 를 줄여서 부르는 이름이고 메뉴얼에서는 `DS-MMR(Disk Sweep Multi-Range Read`라고 합니다. 

MySQL 서버는 조인 대상 테이블 중 하나로부터 레코드를 읽어서 조인 버퍼에 버퍼링하는 것을 MRR이라고 합니다.
구체적으로 드라이빙 테이블의 레코드를 읽어서 드린 테이블과의 조인을 즉시 실행하지 않고 조인 대상을 버퍼링합니다. 
조인 버퍼에 레코드가 가득 차면 MySQL엔진은 버퍼링된 레코드를 스토리지 엔진으로 한 번에 요청하고 스토리지 엔진은 읽어야 할 레코드드들을 데이터 페이지에 정렬된 순서로 접근해서 디스크의 데이터 페이지 읽기를 최소화 할 수 있습니다.

MMR을 응용해서 실행되는 조인 방식을 `BKA(Batched Key ACCESS)` 라고 합니다.
기본 설정은 비활성화 인데 이는 쿼리의 특성에 따라 도움을 받을 수 있지만, BKA 조인을 사용하게 되면 부가적인 정렬 작업이 필요해지면서 오히려 성능에 안 좋은 영향을 미칠 수 있기 때문입니다.

### 블록 네스티드 루프 조인(block_nested_ loop)
MySQL 서버에서 사용되는 대부분의 조인은 네스티드 루프 조인인데, 조인의 연결 조건이 되는 컬럼에 모두 인덱스가 있는 경우 사용되는 조인 방식입니다.
아래 예제에서는 employees 테이블에서 first_name 조건에 일치하는 레코드 1건을 찾아서 salaries 테이블의 일치하는 레코드를 찾는 형태의 조인입니다.
![[Pasted image 20231223002401.png]]
- 이러한 형태의 조인은 프로그래밍 언어에서 중첩된 반복 명령을 사용하는 것처럼 작동한다고 해서 네스티드 루프 조인이라고 합니다.
- 네스티드 루프 조인은 레코드를 읽어서 다른 버퍼 공간에 저장하지 않고 즉시 드리븐 테이블의 레코드를 찾아서 반환합니다.
- 네스티드 루프 조인과 블록 네스티드 루프 조인의 가장 큰 차이는 조인 버퍼(join_buffer_size 시스템 설정으로 조정되는 조인을 위한 버퍼)가 사용되는지 여부와 조인에서 드라이빙 테이블과 드린 테이블이 어떤 순서로 조인되느냐 입니다.
- 조인 알고리즘에서 "Block" 이라는 단어가 사용되면 조인용으로 별도의 버퍼가 사용됐다는 것을 의미하는데, 조인 쿼리의 실행 계획에서 Extra컬럼에 Using Join Buffer라는 문구가 표시되면 그 실행 계획은 조인 버퍼를 사용한다는 것을 의미합니다.
- 조인은 드라이빙 테이블에서 일치하는 레코드의 건수만큼 드리븐 테이블을 검색하면서 처리됩니다.
- 즉 드라이빙 테이블은 한 번에 쭉 읽지만, 드리븐 테이블을 여러 번 읽는다는 것을 의미합니다.
- 예를 들어 드라이빙 테이블에서 일치하는 레코드가 1,000건이었는데, 드리븐 테이블의 조인 조건이 인덱스를 이용할 수 없었다면 드리븐 테이블에서 연결되는 레코드를 찾기 위해 1000번의 풀 테이블 스캔을 해야 합니다. 
- 그래서 드리븐 테이블을 검색할 때 인덱스를 사용할 수 없는 쿼리는 상당히 느려지며, 옵티마이저는 최대한 드리븐 테이블의 검색이 인덱스를 사용할 수 있게 실행 계획을 수립합니다
- 