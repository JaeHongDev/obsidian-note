뷰는 뷰 ID라는 고유 식별자를 가지며 그룹 멤버가 변경될 때 마다 새로운 뷰 ID값이 생성

```
View ID = [Prefix value]:[Sequence value]
```

- 콜론을 기준으로 첫 번째 부분은 그룹 복제가 초기화될 때 생성
- 두번 째는 단조 증가하는 정숫값으로 1부터 시작하여 그룹에서 멤버가 변경될 떄마다 1씩 증가
![[Pasted image 20240430183025.png]]


