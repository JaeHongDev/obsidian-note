
## ROW 포맷의 문제점
Row 포맷을 사용하는 경우 바이너리 로그에 쿼리로 인해 변경된 데이터들이 전부 저장되기 떄문에 Statement 포맷보다 더 많은 저장 공간과 네트워크 트래픽을 유발할 가능성이 있습니다. 

## 해결책 

ROW포맷의 바이너리 로그 파일 용량을 최소화하기 위해 저장되는 변경 데이터의 컬럼 구성을 제어하는 `binlog_row_image` 시스템 변수를 사용


## 정의
> [!binlog_row_image]
For MySQL row-based replication, this variable determines how row images are written to the binary log.


## 사용
Row 포맷의 바이너리 로그 파일 용량을 최소화하기 위해 `binlog_row_image` 시스템 변수를 활용합니다.

Row 포맷을 사용할 경우 바이너리 로그에는 각 변경 데이터마다 변경 전 레코드와 변경 후 레코드가 함께 저장됩니다. 

`binlog_row_image` 시스템 변수는 각 변경 전후 레코드들에 대해 테이블의 어떤 컬럼들을 기록할 것인지를 결정합니다. 
- full
	- 발생한 레코드의 모든 컬럼들의 값을 바이너리 로그에 기록하는 방식
		- insert: 새롭게 insert된 레코드의 모든 컬럼들만 기록
		- update: 변경 전의 레코드와 변경 후의 레코드 모두 전체 길고
		- delete: 변경 전의 레코드 전체 컬럼들만 바이너리 로그 기록
- noblob
	- full 옵션을 설정한 것과 동일하게 작동하지만 BLOB, TEXT 컬럼에 대해 변경이 발생하지 않은 경우 해당 컬럼들은 기록하지 않음
- minimal
	- 변경 데이터에 대해 꼭 필요한 컬럼들의 값만 바이너리 로그에 기록
		- ![[Pasted image 20240416102733.png]]
	- [[PKE(Primary Key Equivalent)]]

- `binlog_row_image` 변수는 Statemen 포맷을 사용하는 경우 영향을 끼치지 않으며, MIXED 방식을 사용하는 경우 ROW 포맷으로 저장되는 변경 데이터에 한해서만 적용된다. 