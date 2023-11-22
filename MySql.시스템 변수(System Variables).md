---
cssclasses:
  - my_style_width_100
---

MySQL 서버가 기동하면서 설정 파일의 내용을 읽어 메모리나 작동 방식을 초기화하고, 접속된 사용자를 제어하기 위해 별도로 저장해 둔 값


아래 명령어로 시스템 변수를 조회할 수 있습니다.
```shell
SHOW GLOBAL VARIABLES;
SHOW VARIABLES;
```

| Name                        | CMD-LINE | Option File | System Var | Var Scope | Dynamic |
| --------------------------- | -------- | ----------- | ---------- | --------- | ------- |
| activate_all_roles_on_login | Yes      | Yes         | Yes        | Global    | Yes     |
| admin_address               | Yes      | Yes         | Yes        | Global    | No      |
| admin_port                  | Yes      | Yes         | Yes        | Global    | No      |
| sql_log_btn                 |          |             | Yes        | Session   | Yes     |
| time_zone                   |          |             | Yes        | Both      | Yes     |

시스템 변수는 5가지 속성을 가지며 다음과 같습니다.
- `Cmd-Line` : MySQL 서버의 명령행 인자로 설정될 수 있는지 여부를 나타냅니다. Yes이면 명령행 인자로 이 시스템 변수의 값을 변경하는 것이 가능합니다.  (비어있으면 No인건가? 왜 빈칸이지)
- `Option File` : MySQL의 설정 파일인 [[my.cnf]] 로 제어할 수 있는지 여부를 나타낸다. 
- `System Var` : 시스템 변수인지 아닌지 나타냅니다.
- `Var Scope`: 시스템 변수의 적용 범위를 나타냅니다. 
	- `Global`: 서버 전체
	- `Session` : 세션
	- `Dynamic`: 시스템 변수가 동적인지 정적인지 구분 

