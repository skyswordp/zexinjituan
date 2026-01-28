# FriendController API 完整测试报告

**生成时间**: 2026-01-28 20:29:50
**测试环境**: https://e68web01.itomtest.com
**测试用户**: adults123 (userId: 488714)
**测试结果**: PASS 21/21 ✅

---

## 测试汇总

| # | 接口 | 状态 | 耗时(ms) |
|---|---|---|---|
| 1 | getUser | [OK] | 266 |
| 2 | getMyPraiseCount | [OK] | 93 |
| 3 | update | [OK] | 452 |
| 4 | saveFollow | [OK] | 88 |
| 5 | readCount | [OK] | 88 |
| 6 | saveShare | [OK] | 98 |
| 7 | saveChangePraise | [OK] | 376 |
| 8 | getLevel | [OK] | 89 |
| 9 | board-index | [OK] | 82 |
| 10 | board-guess | [OK] | 90 |
| 11 | getCountList | [OK] | 94 |
| 12 | saveCircle | [OK] | 89 |
| 13 | pageList-circle | [OK] | 701 |
| 14 | pageList-index | [OK] | 315 |
| 15 | pageList-game | [OK] | 174 |
| 16 | queryTitle | [OK] | 268 |
| 17 | queryDetails | [OK] | 135 |
| 18 | queryTasks | [OK] | 252 |
| 19 | pageList-comments | [OK] | 277 |
| 20 | saveComments | [OK] | 96 |
| 21 | saveReport | [OK] | 85 |

---

## 完整接口 CURL 命令 (可直接复制粘贴执行)

### 1. getUser
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/user/1.0/getUser' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"id":"488714","userId":"488714"}'
```

### 2. getMyPraiseCount
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/user/1.0/getMyPraiseCount' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"userId":"488714"}'
```

### 3. update
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/user/1.0/update' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"id":"488714","nickName":"test","headUrl":"https://example.com/new.png"}'
```

### 4. saveFollow
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/user/1.0/saveFollow' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"userId":"488714","beUserId":100001,"type":"1"}'
```

### 5. readCount
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/user/1.0/readCount' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"type":"1","id":1689288}'
```

### 6. saveShare
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/user/1.0/saveShare' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"userId":489714,"circleId":1689288}'
```

### 7. saveChangePraise
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/user/1.0/saveChangePraise' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"userId":489714,"praiseType":"1","type":"1","circleId":1689288}'
```

### 8. getLevel
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/levelSetting/1.0/getLevel' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"account":"adults123","money":0,"levelId":"1"}'
```

### 9. board-index
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/board/index/getByLevel' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"boardLevel":1}'
```

### 10. board-guess
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/board/guess/getByLevel' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"boardLevel":1}'
```

### 11. getCountList
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/circle/1.0/getCountList' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"time":"1706345600000"}'
```

### 12. saveCircle
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/circle/1.0/saveCircle' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"userId":489714,"content":"test"}'
```

### 13. pageList-circle
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/circle/2.0/pageList' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"pageNum":1,"pageSize":20}'
```

### 14. pageList-index
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/indexSetting/1.0/pageList' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"pageNum":1,"pageSize":20}'
```

### 15. pageList-game
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/gameSetting/1.0/pageList' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"pageNum":1,"pageSize":20}'
```

### 16. queryTitle
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/topic/1.0/queryTitle' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{}'
```

### 17. queryDetails
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/topic/1.0/queryDetails' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"topicId":1,"pageNum":1,"pageSize":20}'
```

### 18. queryTasks
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/task/1.0/queryTasks' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"userId":489714}'
```

### 19. pageList-comments
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/circleComments/1.0/pageList' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"circleId":1689288,"pageNum":1,"pageSize":20}'
```

### 20. saveComments
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/circleComments/1.0/saveComments' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"circleId":1689288,"userId":489714,"content":"test"}'
```

### 21. saveReport
```bash
curl -X POST 'https://e68web01.itomtest.com/api/friend/report/1.0/saveReport' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Content-Type: application/json;charset=UTF-8' \
  -H 'Cookie: __snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C' \
  -H 'Origin: https://e68web01.itomtest.com' \
  -H 'Referer: https://e68web01.itomtest.com/Dynamic' \
  -d '{"reportName":"adults123","beReportName":"user2","fCircleId":1689288,"content":"test","reportReason":"test"}'
```

---

## 使用说明

1. 打开终端 (Mac/Linux 使用 Terminal，Windows 使用 PowerShell 或 Git Bash)
2. 选择上面任何一个代码块，复制CURL命令
3. 粘贴到终端按Enter执行即可
4. 可获取完整的API响应数据进行验证

**所有接口均已通过测试，响应码均为 HTTP 200 成功！**

