# 账号密码汇总

> **快速查找索引**
> - [测试库连接](#测试库pubdbdev)
> - [生产库连接](#生产库)
> - [QY相关系统](#qy相关系统)
> - [游戏相关系统](#游戏相关系统)
> - [中心钱包](#中心钱包)
> - [其他系统](#其他系统入口)

---

## QY相关系统

### QY财务后台（生产）
- 地址：https://eqcnqy240.h955brevn34565bv012uadfrfb23fubt6-qy.com/
- 账号：boots
- 密码：boots@2024!

### QY预上线
- 地址：https://qyweb01.itomtest.com/

---

## 游戏相关系统

### API-Game（游戏配置，游戏开关）
- 地址：http://eq.dc-office.com/
- 账号：boots
- 密码：123123

### Game Office（单一钱包、优惠钱包）
- **第一套**：https://javalangnullpointerexception.com/#/login
- **第二套**：https://second.javalangnullpointerexception.com/
- 账号：admin
- 密码：a123a123

---

## 中心钱包

### 中心钱包第一套（生产）
- 连接信息：
  ```
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 190.92.232.31)(PORT = 1541))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SID = gcenterprd)
    )
  )
  ```
- 只读账户：gcenter_read / IH238dhi14
- 生产用户名：gcenter（查询表时需要带上 `gcenter.<表名>`）

### 中心钱包第二套（生产）
- 连接信息：
  ```
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 190.92.232.31)(PORT = 1551))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = gcenterprd2)
    )
  )
  ```
- 只读账户：gcenter_read / IH238dhi14
- 生产用户名：gcenter（查询表时需要带上 `gcenter.<表名>`）

---

## 测试库（pubdbdev）

### 连接信息（已迁移 - 2025-12-01）
- **新地址**：
  ```
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 119.13.81.81)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = pubdbdev)
    )
  )
  ```
- **旧地址**（已迁移，仅供参考）：
  - HOST: 119.8.59.243
  - PORT: 1521
  - SERVICE_NAME: pubdbdev
  - JDBC: `jdbc:oracle:thin:@119.8.59.243:1521:pubdbdev`

### 账号密码
- **联系人**：IT Jeremiah（Oracle 数据问题可找他）
- **API Game 用户**：pubdb / CiuXZ482PZwx
- **中心钱包用户**：ptnew / 1q2w3e4r5t
- **PNG 用户**：pngdev / EO97nh12gloi

---

## 生产库

### API-Office 生产库
- 连接信息：
  ```
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 190.92.232.31)(PORT = 1561))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = pubdb)
    )
  )
  ```
- 只读用户：rdpubdb / E4592gce
- 查询表时需加用户前缀：`pubdb.<table_name>`

### PNG 库
- 连接信息：
  - HOST: 190.92.232.31
  - PORT: 1531
  - PROTOCOL: TCP
  - SERVER: DEDICATED
  - SERVICE_NAME: pngp
- 只读用户/密码：pngrd / Uc456aacgl（查询表需加用户名 `pngdev.<table_name>`）

---

## OceanBase

### 连接信息
- 域名：t75oc3qekhjog.aws-ap-east-1-internet.oceanbase.cloud
- 端口：1521
- 用户：NWALLET
- 密码：Wallet123$%^
- SSL证书：需要 `ca.pem` 文件
- 连接命令：
  ```bash
  obclient -h t75oc3qekhjog.aws-ap-east-1-internet.oceanbase.cloud -P 1521 -u NWALLET --ssl-ca=<path>/ca.pem -p 'Wallet123$%^'
  ```

---

## 本地开发

### Game Office 前端项目
- 项目路径：`C:\project\dc\dc_gc_office`
- 启动命令：
  ```bash
  cd C:\project\dc\dc_gc_office
  npm run dev
  ```

---

## 其他系统入口

## VPN（dev openvpn）
- 地址：https://18.166.253.125:943/
- 账号：trump
- 密码：Wh456&*(QQaz

## 测试库（pubdbdev）
- 联系人：IT Jeremiah（Oracle 数据问题可找他）
- 连接信息（已迁移 - 2025-12-01）：
  - HOST: 119.13.81.81
  - PORT: 1521
  - PROTOCOL: TCP
  - SERVER: DEDICATED
  - SERVICE_NAME: pubdbdev
- game api 用户/密码：pubdb / CiuXZ482PZwx
- PNG 用户/密码：pngdev / EO97nh12gloi

## 生成库
### PNG 库
- 连接信息：
  - HOST: 190.92.232.31
  - PORT: 1531
  - PROTOCOL: TCP
  - SERVER: DEDICATED
  - SERVICE_NAME: pngp
- 只读用户/密码：pngrd / Uc456aacgl（查询表需加用户名 pngdev.<table_name>）

### GAMEAPI 库
- 连接信息：
  - HOST: 190.92.232.31
  - PORT: 1561
  - PROTOCOL: TCP
  - SERVER: DEDICATED
  - SERVICE_NAME: pubdb
- 只读用户/密码：rdpubdb / E4592gce（查询表需加用户前缀 pubdb.<table_name>）

## 系统入口
### 禅道
- 地址：http://office.dc-process.com/zentao/user-login.html
- 账号：Trump
- 密码：Aa123456

### OA 打卡（Power Apps）
- 地址：OA_Punch_In_online - Power Apps
- 说明：可以备存到浏览器书签
- 链接：https://apps.powerapps.com/play/e/c7c4b750-7570-ebc0-b9b3-ec67e0052290/a/661f3032-5821-40f7-b31b-847704eeb9de?tenantId=95e36529-e288-425d-8be7-6167132dad43&source=teamsopenwebsite&hint=0440c872-45d9-4d40-989f-51ea7820db14&sourcetime=1759731839778

## GitLab
- 地址：https://git.easydevops.net/
- 账号：trump
- 密码：1q2w3e4r5t@.
- token（身份验证，请妥善保存）：glpat-VDecDiYzxJ6emrWxKbM2yG86MQp1OmI5CA.01.0y07d65u3
- token 用法：
```
git clone http://trump:glpat-VDecDiYzxJ6emrWxKbM2yG86MQp1OmI5CA.01.0y07d65u3@git.easydevops.net/B2C_DC/public/png.git
```

## Kibana
- 地址：https://kibana.easydevops.net/
- 账号：trump
- 密码：1q2w3e4r5t@.

## 其他
- 链接：http://159.138.156.199/ui/#/profile/improvement

## CRM 测试登录
- 地址：https://eqqycrm.wotingshuoyumingyuechangyuehao2333heheda.com/#/login
- 账号：c_cest
- 密码：cest123

## 平台域名/账号
- QY：eqqycrm.wotingshuoyumingyuechangyuehao2333heheda.com
- L8：eqlong8crm.wotingshuoyumingyuechangyuehao2333heheda.com
- AT：eqpt777crm.wotingshuoyumingyuechangyuehao2333heheda.com
- LH：eqe68crm.wotingshuoyumingyuechangyuehao2333heheda.com
- QYH：http://equlecrm.wotingshuoyumingyuechangyuehao2333heheda.com/
- RB：aws5crm.qweurnzxv1834mnvb-rb88.com
- 账号/密码：与财务后台一致；如缺账号密码请找 SRE 获取。
- 通用账号：boots / boots@2024!
- 若链接/账号缺失或有问题可直接找 SRE（运维管理所有服务器）。
- 更新 PNG 项目需提前告知，以便同步服务器分布信息。
- 后台登录示例：
  - 地址：https://portal2.owadmin999.com/46abi23?Language=cs
  - 账号：ctadmin
  - 密码：g0ds@feus2025!
  - 地址：https://www.agback.support/backend/
  - 账号：ctadmin
  - 密码：123456

## 参考文档
- 测试服务说明：https://git.easydevops.net/it/sre/production-docs-detail/-/blob/master/service-info/test-service/new-test-service.md
- WebOffice 服务说明：https://git.easydevops.net/it/sre/production-docs-detail/-/blob/master/service-info/product-service/weboffice.md
- CRM 服务说明：https://git.easydevops.net/it/sre/production-docs-detail/-/blob/master/service-info/product-service/crm.md
- 生产文档目录：https://git.easydevops.net/it/sre/production-docs-detail/
- 若无法访问上述链接，请联系 Mimi 协助开通

## PNG 线上配置片段（参考）
- init.properties
```
# 数据库配置
datasource.type = mysql
datasource.driverClassName = oracle.jdbc.driver.OracleDriver
datasource.url = ENC(474ZglxU4VUfFYyUQMIBw35HtQW/+GTrUS9KvMbE3w71pufijh/ERrGvWze7kZQ7C1VzZiU68G5R3AWozcuv+A==)
datasource.username = ENC(RTHLpDWr1fl8gbJ8uPs7vw==)
datasource.password = ENC(/q1j8TikvZZ8XBuhKIBSeQVXqUuTsz9R)
datasource.maxActive = 8000
datasource.maxIdle = 1000
datasource.maxWait = 120000
datasource.whenExhaustedAction = 1
datasource.validationQuery = select 1 from dual
datasource.timeBetweenEvictionRunsMillis = 100000
datasource.testWhileIdle = true
datasource.testOnBorrow = false
datasource.testOnReturn = false
datasource.removeAbandoned = true
datasource.removeAbandonedTimeout = 180
datasource.logAbandoned = true
hibernate.dialect = org.hibernate.dialect.OracleDialect
hibernate.jdbc.batch_size = 25
hibernate.jdbc.fetch_size = 50
hibernate.show_sql = false
hibernate.connection.release_mode = after_transaction
```

- log4j.properties
```
log4j.rootLogger = INFO,A1,stdout
#log4j.rootLogger=WARN, stdout, logfile
log4j.appender.stdout = org.apache.log4j.ConsoleAppender
log4j.appender.stdout.layout = org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern = %d %p [%c] - %m%n
log4j.logger.net.sf.json.xml.XMLSerializer = OFF
log4j.appender.A1 = org.apache.log4j.DailyRollingFileAppender
log4j.appender.A1.File = ${catalina.base}/logs/elf_office.log
log4j.appender.A1.DatePattern = '.'yyyy-MM-dd
log4j.appender.A1.Append = true
log4j.appender.A1.layout = org.apache.log4j.PatternLayout
log4j.appender.A1.layout.ConversionPattern = %d %5p (%c:%L) %n %m%n
```

- config.properties
```
# netpay::被授权的多个IP地址，用英文逗号分隔
netpay_services_ip = 127.0.0.1,202.66.33.213,152.101.114.206,202.66.33.239
netpay_hidden_value = bc50562c65f97258ee83be28e0d6dba8
mackey = 7dc4b594a1ee58d25af85212de821793
# 以下三项，值为0时表示不做限制
cashin_count = 3
cashin_amount = 0
cashin_totalAmount = 0
# 每日提款次数
CashoutTodayCount = 100000
# 每日提款额度
CashoutTodayAmount = 380000
# ea_bbs 用户信息同步地址
ea_bbs_register = http://bbs.e68ph.net/member.php
ea_bbs_ip = 27.126.190.25
ea_bbs_port = 3306
ea_bbs_databases = e68ph
ea_bbs_user = e68ph
ea_bbs_password = jDkKGJKmjwDkruKTGWJPzKm
# ea_bbs 用户密码更新地址
bbs_modifyPassword_url = http://bbs.e68ph.net/logging.do
#ptwebservice
PHP_PT_SERVICE = http://172.23.2.120:6886/goldenrose
InternalAgent = 'a_e68cs1', 'a_e68cs2', 'a_e68cs3', 'a_e68cs4', 'a_e68cs5','a_kiki','a_lode','a_test05','a_test012','a_test013','a_judy','a_jennies','a_zoe01','a_eva01','a_kiki','a_kelly','a_doris','a_tina','a_rachel','a_helen','a_yoyo','a_judy02','a_jennies02','a_doris02','a_kelly02','a_rachel02','a_helen02','a_tina02'
#秒付宝商户号
MFBClientNo = e68mfb888JQK
#upgrade url
AUTO_UPGRADE_URL = http://59.188.218.53:6789/betRecord.ssl
#JC接口地址
JC_Services = http://192.168.0.201:9991/secure/
#EA中转链接
EA_GAME_URL = http://59.188.218.54:1200/
onegame.url = http://onegame-wallet.production-onegame.svc.cluster.local:8080/
twogame.url = http://twogame-wallet.production-twogame.svc.cluster.local:8080/
```

- applicationContext-quartz.xml
```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:aop="http://www.springframework.org/schema/aop"
      xmlns:tx="http://www.springframework.org/schema/tx"
      xsi:schemaLocation="
http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-2.5.xsd
http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-2.5.xsd
http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-2.5.xsd">
<bean
        class="org.springframework.scheduling.quartz.SchedulerFactoryBean">
<property name="triggers">
<list>
</list>
</property>
</bean>
</beans>
```

## CRM 线上配置片段（参考）
- application-dev.yml
```
mysql:
  spring:
    datasource:
      type: com.alibaba.druid.pool.DruidDataSource
      driverClassName: com.mysql.jdbc.Driver
      druid:
        master: #主数据源
          url: ENC(0qXtzB4GoUtbImLmB/yDRJ+Q/8Mjhw69Vbq1Onp7xB7RniO1ogVGX32N/EkGeh1Ar85qLwo5rE8qtfuqW0Lq3V8J+MybrVHjLrVuOMKjoD93Mye3ue/1xrC/I6pdNCXnivQFvgW2Gz/Lo5uPYmERAr6dymwdM0GSUOJmU0rg2Dg=)
          username: ENC(2Nrm6zWnW6NhfSHhQJLjzJipJlb8tESC)
          password: ENC(0GHyZeV0cw2ohDDwUPX8iYph0M5/OjUlYnlDvoA35V2mVuJv3Ec8ed4uZj92HsYeE1vWdmPQc3c=)
        slave: #从数据源
          url: ENC(/yq7kNI6fqGHTZKNtk+DksmnRWTKWzRYxG155NPOgTUVZokEcPCQ7K8qlGc1Xws9k6UCxiP27qhDbBAN5mpxCx/A6Q+nI2lAMka0wMCPc1y9L7EdT9sBcl5ykKG7DyEliqz5Z+mkp0XpyXweNg9Dv2A3grezQU9CuzbHLTy36r7htMxVzXNdow==)
          username: ENC(DYjaiwN7dEv1h+to+nneqA==)
          password: ENC(0wZ3bvNSYrttWG4vmpWYq9CZaAAKt0u9)
        initial-size: 5
        max-active: 100
        min-idle: 10
        max-wait: 60000
        pool-prepared-statements: true
        max-pool-prepared-statement-per-connection-size: 20
        time-between-eviction-runs-millis: 30000
        min-evictable-idle-time-millis: 120000
        validation-query: SELECT 1 FROM DUAL
        test-while-idle: true
        test-on-borrow: false
        test-on-return: false
        stat-view-servlet:
          enabled: false
oracle:
  spring:
      datasource:
          type: com.alibaba.druid.pool.DruidDataSource
          driverClassName: oracle.jdbc.driver.OracleDriver
          druid:
              pubmaster:  #数据源1
                  url: ENC(01NhRgOmgneRTMHwjcX/MUSY6JrXQoj5axnRP5Oj8fDaLU5VZFvNcG6cqsxUDka0D1eLz6WbD2Vln7/n+wfhpK8tZ2FH5/GQLIrhZFMne0YzHF210v8mu0rmv5VMOica8eJ+vZekd2zDB52KbNrZsYF/uxQLEiD7YmwPVtGo9MHJrhpVCg0/Yfmo+8lhYkI4l8f0gTr/KsjrFOGMzVXcRte0FHm1cLdqJYO1TdNDiafpnQqgwEwJzw==)
                  username: ENC(NZG+7aI/HGLcQPEGnFNUSQ==)
                  password: ENC(Ihh0GuOgTeARPgAl88YLX8vE9aSwPJ4y)
              # pubslave:  #数据源1
                  # url: jdbc:oracle:thin:@47.244.139.19:1521:pubdbdev
                  # username: pubdb
                  # password: CiuXZ482PZwx
              initial-size: 10
              max-active: 100
              min-idle: 10
              max-wait: 60000
              pool-prepared-statements: true
              max-pool-prepared-statement-per-connection-size: 20
              time-between-eviction-runs-millis: 60000
              min-evictable-idle-time-millis: 300000
              validation-query: SELECT 1 FROM DUAL
              test-while-idle: true
              test-on-borrow: false
              test-on-return: false
              stat-view-servlet:
                  enabled: false
#大数据数据源
bigdata:
  datasource:
    impala:
      driverClassName: org.apache.hive.jdbc.HiveDriver
      url: ENC(Nl09vV8ZOgG1StobLBEUH3WWyizb1sI5FfSDxvnU+XBdS2TnEgGyHb4oRawLY3vS)
      username: ENC(jrE+OLMDCbxtRI8bzkEuWA==)
      password: ENC(3ipUJqlU2JR4uQn2pwKAMCamoiAd3gwU)
      initialPoolSize: 5
      maxIdleTime: 5000
      minPoolSize: 5
      acquireIncrement: 5
      maxPoolSize: 30
      idleConnectionTestPeriod: 1000
oraclebigdata:
  spring:
    datasource:
      type: com.alibaba.druid.pool.DruidDataSource
      driverClassName: oracle.jdbc.OracleDriver
      druid:
        pubmasterbigdata:  #数据源1
          url: ENC(J5B1ODzfybIA2jgBPewZ/fPH9yfBGpHn4swVBi9ZQKWmRZVwT+qjEPpi9FIQvPdquLeM0H4aDFZQUrCZmQKWNNXF4nnJc6xL)
          username: ENC(WIAgL+YlFRq9eNZFFN84TA==)
          password: ENC(13Q6eZEZLErq52PhrZBpo6SmqGNNM1XW)
        initial-size: 10
        max-active: 100
        min-idle: 10
        max-wait: 60000
        pool-prepared-statements: true
        max-pool-prepared-statement-per-connection-size: 20
        time-between-eviction-runs-millis: 60000
        min-evictable-idle-time-millis: 300000
        validation-query: SELECT 1 FROM DUAL
        test-while-idle: true
        test-on-borrow: false
        test-on-return: false
        stat-view-servlet:
          enabled: false
```

- application.yml
```
# Tomcat
server:
  tomcat:
    uri-encoding: UTF-8
    max-threads: 1000
    min-spare-threads: 30
  port: 8080
  connection-timeout: 6000000
  servlet:
    context-path: /

spring:
  # 环境 dev|test|prod
  profiles:
    active: dev
  jackson:
    time-zone: GMT+8
    date-format: yyyy-MM-dd HH:mm:ss
  servlet:
    multipart:
      max-file-size: 20MB
      max-request-size: 20MB
      enabled: true
  mvc:
    throw-exception-if-no-handler-found: true
    static-path-pattern: /static/**
  resources:
    add-mappings: false
  cache:
    ehcache:
      config: classpath:ehcache.xml

jasypt:
  encryptor:
    password: ComoneBaby

pagehelper:
  reasonable: true

crm:
# 产品名称:qy,l8,at,e68,ufa,ule,zb,qfa
  product: qy
# 定时任务
scheduler:
  crm:
    task: true
    labelauto: true
    noticedata: true
    notice: true
    dataintegration: true
    info: true
    usersBehavior: true
  risk:
    creditlevelusers: true
    processBlackInfo: true
    armScheduler: true
  bi:
    dataCollect: true
  #客户分析-生成任务下会员 定时任务
  customer:
    taskUser: false
    taskName: true
    userMaintain: true
# crm域名
crmUrl:
  qy: http://qy-crmfd.production-qy.svc.cluster.local
  lh: http://e68-crmfd.production-e68.svc.cluster.local
  at: http://pt777-crmfd.production-pt777.svc.cluster.local
  yl: http://long8-crmfd.production-long8.svc.cluster.local
  tq: http://sportone-crmfd.production-sportone.svc.cluster.local
  ued: http://ued-crmfd.production-ued.svc.cluster.local
  jxf: http://jxf-crmfd.production-jxf.svc.cluster.local
  rb88: http://rb88-crmfd.production-rb88.svc.cluster.local
  middUrl: http://qy-midd.production-qy.svc.cluster.local:8080/
  gameApiUrl: http://api-game.production-api.svc.cluster.local:8080
```

---

## 常用SQL语句

### 表结构修改

#### B_CAROUSEL_MAP_CONFIG 表 - 添加APP专用跳转链接字段
```sql
ALTER TABLE B_CAROUSEL_MAP_CONFIG ADD (JUMP_LINK_APP VARCHAR2(200 BYTE) VISIBLE);
COMMENT ON COLUMN B_CAROUSEL_MAP_CONFIG.JUMP_LINK_APP IS '跳转链接-APP专用';
```

#### B_CAROUSEL_MAP_CONFIG 表 - 添加黑夜版图片字段
```sql
ALTER TABLE B_CAROUSEL_MAP_CONFIG ADD (IMAGE_URL_NIGHT VARCHAR2(100 BYTE) VISIBLE);
COMMENT ON COLUMN B_CAROUSEL_MAP_CONFIG.IMAGE_URL IS '轮播图图片地址-白天版';
COMMENT ON COLUMN B_CAROUSEL_MAP_CONFIG.IMAGE_URL_NIGHT IS '轮播图图片地址-黑夜版';
```
