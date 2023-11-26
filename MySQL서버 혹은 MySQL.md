---
cssclasses:
  - my_style_width_100
---

### MySQL 개념

MySQL 서버는 MySQL 엔진과 스토리지 엔진을 합친 것을 의미합니다.
(MySQL이라고 부르기도 합니다)

RealMySQL에서는 쿼리 파서나 옵티마이저 등과 같은 기능을 스토리지 엔진과 구분하고자 MySQL 엔진과 스토리지 엔진으로 구분했습니다.



### MySQL 스레딩 구조
MySQL 서버는 프로세스 기반이 아니라 스레드 기반으로 작동하며 다음과 같이 구분합니다.
- [[포그라운드 스레드]]
- [[백그라운드 스레드]]


```mysql
select thread_id, name, type, processlist_user, processlist_host from
 performance_schema.threads order by type, thread_id;
```

```mysql
thread_id	name	type	processlist_user	processlist_host
1	thread/sql/main	BACKGROUND	NULL	NULL
2	thread/mysys/thread_timer_notifier	BACKGROUND	NULL	NULL
4	thread/innodb/io_ibuf_thread	BACKGROUND	NULL	NULL
5	thread/innodb/io_read_thread	BACKGROUND	NULL	NULL
6	thread/innodb/io_read_thread	BACKGROUND	NULL	NULL
7	thread/innodb/io_read_thread	BACKGROUND	NULL	NULL
8	thread/innodb/io_read_thread	BACKGROUND	NULL	NULL
9	thread/innodb/io_write_thread	BACKGROUND	NULL	NULL
10	thread/innodb/io_write_thread	BACKGROUND	NULL	NULL
11	thread/innodb/io_write_thread	BACKGROUND	NULL	NULL
12	thread/innodb/io_write_thread	BACKGROUND	NULL	NULL
13	thread/innodb/page_flush_coordinator_thread	BACKGROUND	NULL	NULL
14	thread/innodb/log_checkpointer_thread	BACKGROUND	NULL	NULL
15	thread/innodb/log_flush_notifier_thread	BACKGROUND	NULL	NULL
16	thread/innodb/log_flusher_thread	BACKGROUND	NULL	NULL
17	thread/innodb/log_write_notifier_thread	BACKGROUND	NULL	NULL
18	thread/innodb/log_writer_thread	BACKGROUND	NULL	NULL
19	thread/innodb/log_files_governor_thread	BACKGROUND	NULL	NULL
24	thread/innodb/srv_lock_timeout_thread	BACKGROUND	NULL	NULL
25	thread/innodb/srv_error_monitor_thread	BACKGROUND	NULL	NULL
26	thread/innodb/srv_monitor_thread	BACKGROUND	NULL	NULL
27	thread/innodb/buf_resize_thread	BACKGROUND	NULL	NULL
28	thread/innodb/srv_master_thread	BACKGROUND	NULL	NULL
29	thread/innodb/dict_stats_thread	BACKGROUND	NULL	NULL
30	thread/innodb/fts_optimize_thread	BACKGROUND	NULL	NULL
33	thread/mysqlx/acceptor_network	BACKGROUND	NULL	NULL
37	thread/innodb/buf_dump_thread	BACKGROUND	NULL	NULL
38	thread/innodb/clone_gtid_thread	BACKGROUND	NULL	NULL
39	thread/innodb/srv_purge_thread	BACKGROUND	NULL	NULL
40	thread/innodb/srv_worker_thread	BACKGROUND	NULL	NULL
41	thread/innodb/srv_worker_thread	BACKGROUND	NULL	NULL
42	thread/innodb/srv_worker_thread	BACKGROUND	NULL	NULL
44	thread/sql/signal_handler	BACKGROUND	NULL	NULL
45	thread/mysqlx/acceptor_network	BACKGROUND	NULL	NULL
284	thread/mysqlx/worker	BACKGROUND	NULL	NULL
298	thread/mysqlx/worker	BACKGROUND	NULL	NULL
43	thread/sql/event_scheduler	FOREGROUND	event_scheduler	localhost
47	thread/sql/compress_gtid_table	FOREGROUND	NULL	NULL
310	thread/sql/one_connection	FOREGROUND	root	localhost
315	thread/sql/one_connection	FOREGROUND	root	localhost
```


### 메모리 할당 및 사용 구조

MySQL에서 사용되는 메모리 공간은 다음과 같이 구분합니다.
- [[글로벌 메모리 영역]]
- [[로컬 메모리 영역]]

운영체제의 종류에 따라 다르겠지만 요청된 메모리 공간을 100% 할당해줄 수도 있고, 그 공간만큼 예약해두고 필요할 때 조금씩 할당해주는 경우도 있다. 각 운영체제의 메모리 할당 방식은 상당히 복잡하며, MySQL 서버가 사용하는 정확한 메모리의 양을 측정하는 것 또한 쉽지 않다. 
그렇기에 <u>그냥 단순하게 MySQL의 시스템 변수로 설정해 둔 만큼 운영체제로부터 메모리를 할당받는다고 생각해도 된다.</u>



### 관련 사항
[[MySQL 명령어 꿀팁]]