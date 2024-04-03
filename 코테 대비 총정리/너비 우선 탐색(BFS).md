

## 그래프 탐색
- 주로 최단 경로를 찾는 다익스트라 알고리즘에 매우 유용하게 사용된다. 
```
BFS(G, start_v) 
	let Q be a queue
	label start_v as discovered
	Q.enqueue(start_v)
	while Q is not empty do
		v := Q.dequeue()
		for all edges from v to w in G.adjancentEdges(v) do
			if w is not labeled as discovered then
				label w as discovered 
				w.parent := v
				Q.enqueue(w)
```
- 위 수도코드를 자바코드로 표현하면 다음과 같습니다 
- ![[Pasted image 20240403173513.png]]

> ⚠ 주의
> BFS를 재귀로 풀이할 수 없다.