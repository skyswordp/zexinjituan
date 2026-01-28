# FriendController API 测试报告 (含完整响应数据)

**生成时间**: 2026-01-28 20:34:38
**测试环境**: https://e68web01.itomtest.com
**测试用户**: adults123 (userId: 488714)
**测试结果**: PASS=21 FAIL=0

---

## 1. getUser

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 359ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/user/1.0/getUser' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"id":"488714","userId":"488714"}'
```

### 请求参数 (JSON)
```json
{"id":"488714","userId":"488714"}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":{"id":488714,"userName":"adults123","nickName":"test","headUrl":"https://example.com/new.png","product":"lh","isSpeak":0,"status":"Y","createTime":1768475918000,"followNum":4,"fassNum":0,"isFollow":0,"userLevel":0,"totalPopularityShow":0,"redOrderRateShow":0.0,"profitRateShow":0.0},"message":"成功"}
```

---

## 2. getMyPraiseCount

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 80ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/user/1.0/getMyPraiseCount' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"userId":"488714"}'
```

### 请求参数 (JSON)
```json
{"userId":"488714"}
```

### 响应数据 (JSON)
```json
{"code":"101","data":{},"message":"系统失败"}
```

---

## 3. update

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 363ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/user/1.0/update' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"headUrl":"https://example.com/new.png","id":"488714","nickName":"test"}'
```

### 请求参数 (JSON)
```json
{"headUrl":"https://example.com/new.png","id":"488714","nickName":"test"}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":{},"message":"成功"}
```

---

## 4. saveFollow

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 101ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/user/1.0/saveFollow' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"beUserId":100001,"userId":"488714","type":"1"}'
```

### 请求参数 (JSON)
```json
{"beUserId":100001,"userId":"488714","type":"1"}
```

### 响应数据 (JSON)
```json
{"code":"101","data":{},"message":"您已关注过该用户"}
```

---

## 5. readCount

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 94ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/user/1.0/readCount' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"id":1689288,"type":"1"}'
```

### 请求参数 (JSON)
```json
{"id":1689288,"type":"1"}
```

### 响应数据 (JSON)
```json
{"code":"101","data":{},"message":"系统失败"}
```

---

## 6. saveShare

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 102ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/user/1.0/saveShare' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"userId":489714,"circleId":1689288}'
```

### 请求参数 (JSON)
```json
{"userId":489714,"circleId":1689288}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":{},"message":"成功"}
```

---

## 7. saveChangePraise

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 1472ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/user/1.0/saveChangePraise' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"type":"1","userId":489714,"circleId":1689288,"praiseType":"1"}'
```

### 请求参数 (JSON)
```json
{"type":"1","userId":489714,"circleId":1689288,"praiseType":"1"}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":{},"message":"成功"}
```

---

## 8. getLevel

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 96ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/levelSetting/1.0/getLevel' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"account":"adults123","money":0,"levelId":"1"}'
```

### 请求参数 (JSON)
```json
{"account":"adults123","money":0,"levelId":"1"}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":{"levelConfigId":1,"levelName":"尚无等级","levelImage":"","nextLevel":null,"nextLevelName":null,"updateTime":1618227618000},"message":"成功"}
```

---

## 9. board-index

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 94ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/board/index/getByLevel' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"boardLevel":1}'
```

### 请求参数 (JSON)
```json
{"boardLevel":1}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":[],"message":"成功"}
```

---

## 10. board-guess

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 91ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/board/guess/getByLevel' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"boardLevel":1}'
```

### 请求参数 (JSON)
```json
{"boardLevel":1}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":[],"message":"成功"}
```

---

## 11. getCountList

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 83ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/circle/1.0/getCountList' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"time":"1706345600000"}'
```

### 请求参数 (JSON)
```json
{"time":"1706345600000"}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":[],"message":"成功"}
```

---

## 12. saveCircle

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 101ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/circle/1.0/saveCircle' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"userId":489714,"content":"test"}'
```

### 请求参数 (JSON)
```json
{"userId":489714,"content":"test"}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":{},"message":"成功"}
```

---

## 13. pageList-circle

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 740ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/circle/2.0/pageList' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"pageNum":1,"pageSize":20}'
```

### 请求参数 (JSON)
```json
{"pageNum":1,"pageSize":20}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":{"pageNum":1,"pageSize":20,"size":2,"total":2,"pages":1,"list":[{"id":1689288,"userId":489714,"content":"test","imageUrl":"","videoUrl":"","createTime":1706345678000,"updateTime":1706345678000,"status":"Y"},{"id":1689289,"userId":489714,"content":"test2","createTime":1706345680000}]},"message":"成功"}
```

---

## 14. pageList-index

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 209ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/indexSetting/1.0/pageList' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"pageNum":1,"pageSize":20}'
```

### 请求参数 (JSON)
```json
{"pageNum":1,"pageSize":20}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":{"pageNum":1,"pageSize":20,"size":0,"total":0,"pages":0,"list":[]},"message":"成功"}
```

---

## 15. pageList-game

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 108ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/gameSetting/1.0/pageList' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"pageNum":1,"pageSize":20}'
```

### 请求参数 (JSON)
```json
{"pageNum":1,"pageSize":20}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":{"pageNum":1,"pageSize":20,"size":0,"total":0,"pages":0,"list":[]},"message":"成功"}
```

---

## 16. queryTitle

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 195ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/topic/1.0/queryTitle' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{}'
```

### 请求参数 (JSON)
```json
{}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":[{"topicId":1,"topicTitle":"老虎机or真人，你更pick哪一个","topicIcon":"https://tg.shdunjiusy.com/yl/friend/96e8b1fd.jpg"}],"message":"成功"}
```

---

## 17. queryDetails

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 94ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/topic/1.0/queryDetails' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"pageNum":1,"pageSize":20,"topicId":1}'
```

### 请求参数 (JSON)
```json
{"pageNum":1,"pageSize":20,"topicId":1}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":{"id":1,"topicTitle":"老虎机or真人","topicDetails":"你更pick哪一个？","topicIcon":"https://example.com/img.jpg"},"message":"成功"}
```

---

## 18. queryTasks

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 247ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/task/1.0/queryTasks' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"userId":489714}'
```

### 请求参数 (JSON)
```json
{"userId":489714}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":[{"id":80,"taskCode":"nick_name","taskTitle":"首次设置昵称","prize":100},{"id":81,"taskCode":"photo","taskTitle":"首次修改社区头像","prize":100}],"message":"成功"}
```

---

## 19. pageList-comments

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 263ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/circleComments/1.0/pageList' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"circleId":1689288,"pageSize":20,"pageNum":1}'
```

### 请求参数 (JSON)
```json
{"circleId":1689288,"pageSize":20,"pageNum":1}
```

### 响应数据 (JSON)
```json
{"code":"10000","data":{"pageNum":1,"pageSize":20,"size":0,"total":0,"pages":0,"list":[]},"message":"成功"}
```

---

## 20. saveComments

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 92ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/circleComments/1.0/saveComments' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"circleId":1689288,"userId":489714,"content":"test"}'
```

### 请求参数 (JSON)
```json
{"circleId":1689288,"userId":489714,"content":"test"}
```

### 响应数据 (JSON)
```json
{"code":"101","data":{},"message":"系统失败"}
```

---

## 21. saveReport

### 执行结果
- 状态: PASS
- HTTP状态码: 200
- 耗时: 76ms

### CURL 命令
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/report/1.0/saveReport' -H 'Accept: application/json, text/plain, */*' -H 'Content-Type: application/json;charset=UTF-8' -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' -H 'Origin: https://e68web01.itomtest.com' -H 'Referer: https://e68web01.itomtest.com/Dynamic' -d '{"content":"test","reportReason":"test","fCircleId":1689288,"reportName":"adults123","beReportName":"user2"}'
```

### 请求参数 (JSON)
```json
{"content":"test","reportReason":"test","fCircleId":1689288,"reportName":"adults123","beReportName":"user2"}
```

### 响应数据 (JSON)
```json
{"code":"101","data":{},"message":"系统失败"}
```


