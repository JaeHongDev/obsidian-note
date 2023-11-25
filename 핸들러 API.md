---
cssclasses:
  - my_style_width_100
---
MySQL 엔진의 쿼리 실행기에서 데이터를 쓰거나 읽어야 할 때는 각 스토리지 엔진에 쓰기 또는 읽기를 요청하는데, 이러한 요청을 핸들러요청이라고 부릅니다.
여기서 사용하는 API를 핸들러 API라고 부릅니다. 


MySQL 엔진의 쿼리 실행기에서 데이터를 쓰거나 읽어야 할 때는 각 [[스토리지 엔진]]에 쓰기 또는 읽기를 요청하는데, 이러한 요청을 핸들러 요청이라고 하며, 여기서 사용되는 API를 핸들러 API라고 합니다.

> 요청하는 행위를 핸들러 요청이라고 하며, 실제로 사용하는 기능을 핸들러 API라고 하는듯

[[InnoDB]] [[스토리지 엔진]] 또한 이 핸들러 API를 이용해 MySQL 엔진과 데이터를 주고받습니다. 
핸들러 API를 통해 얼마나 많은 데이터(레코드)작업이 있었는지는 아래 명령어를 통해서 확인 가능합니다.
```mysql
mysql> show global status like 'Handler%';
+----------------------------+-------+
| Variable_name              | Value |
+----------------------------+-------+
| Handler_commit             | 669   |
| Handler_delete             | 8     |
| Handler_discover           | 0     |
| Handler_external_lock      | 7347  |
| Handler_mrr_init           | 0     |
| Handler_prepare            | 16    |
| Handler_read_first         | 56    |
| Handler_read_key           | 2295  |
| Handler_read_last          | 0     |
| Handler_read_next          | 4641  |
| Handler_read_prev          | 0     |
| Handler_read_rnd           | 0     |
| Handler_read_rnd_next      | 224   |
| Handler_rollback           | 0     |
| Handler_savepoint          | 0     |
| Handler_savepoint_rollback | 0     |
| Handler_update             | 357   |
| Handler_write              | 41    |
+----------------------------+-------+
18 rows in set (0.03 sec)
```