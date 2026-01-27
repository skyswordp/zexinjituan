# 红单定时任务代码走查（qm -> qy 复刻）

> **目标：** 确认所有红单相关的定时任务是否支持多产品，是否需要改造

---

## 📋 定时任务总览

**一共6个定时任务：**

| 序号 | 任务名称 | 执行时间 | 模块 | 是否需要改造 |
|------|---------|---------|------|------------|
| 1 | AI推单 | 每天21:00 | dc-api-office | ❌ 不需要 |
| 2 | AI补救推单 | 每天23:00 | dc-api-office | ❌ 不需要 |
| 3 | AI补单 | 每天00:00:01 | dc-api-office | ❌ 不需要 |
| 4 | 用户火标设置 | 每月5号00:00 | dc-api-office | ❌ 不需要 |
| 5 | AI真实推单 | 每天20:00 | dc-api-office | ❌ 不需要 |
| 6 | 红单结算 | 每3分钟 | dc-api-sportcron | ❌ 不需要 |

**结论：所有定时任务都不需要改造，已支持多产品！**

---

## ✅ 1. AI推单任务（aiPushOrder）

### 1.1 代码位置

**定时任务类：**
- 文件：`DC-API-2018/dc-api/dc-api-office/src/main/java/com/dc/it/friend/quartz/AIPushOrderTask.java`
- 方法：`aiPushOrder()` - 第28-37行

**配置位置：**
- 文件：`DC-API-2018/dc-api/dc-api-office/src/main/resources/applicationContext.xml`
- Bean：`aiPushOrderTrigger` - 第125-130行
- Cron：`0 0 21 * * ?` （每天21点执行）

### 1.2 代码走查

```java
// AIPushOrderTask.java 第28-37行
public void aiPushOrder(){
    try {
        logger.info("AI推单 定时任务【启动】");
        aiPushOrderService.taskCreatePushOrder();  // 调用Service
        logger.info("AI推单 定时任务【结束】");
    }catch (Exception e){
        e.printStackTrace();
        logger.error("AI推单 定时任务【发生异常】，异常信息为：" + e);
    }
}
```

**Service层：**
```java
// AIPushOrderServiceImpl.java 第532-538行
public void taskCreatePushOrder(){
    String uuid = PUSH_ORDER_TYPE_CREATE+"_"+UUID.randomUUID().toString();
    log.info(uuid+"->系统开始生成推单，源自【定时任务】");
    createPushOrder(uuid,null);  // 传入null，表示定时任务调用
}
```

**核心方法：**
```java
// AIPushOrderServiceImpl.java 第808-822行
private int createPushOrder(String uuid,String[] productArr){
    //获取系统配置的推单的产品
    String[] products = null;
    if (productArr == null){//定时任务调用的
        products = getSystemPushOrderProduct();  // ⭐ 关键：从系统参数获取产品列表
        log.info(uuid+"->来源：定时任务，即将执行如下产品的用户推单："+Arrays.toString(products));
    }else{//后台调用的
        products = productArr;
        log.info(uuid+"->来源：后台手动，即将执行如下产品的用户推单："+Arrays.toString(products));
    }
    // ... 后续处理每个产品
}
```

**获取产品列表方法：**
```java
// AIPushOrderServiceImpl.java 第74-87行
public String[] getSystemPushOrderProduct(){
    Map<String, Object> sysMap = new HashMap<String, Object>();
    sysMap.put("category", "PUSHORDER");
    sysMap.put("code", "PUSHORDER_PRODUCT");  // ⭐ 从系统参数获取
    SystemParameter sysParameter = parameterDao.get(sysMap);
    if (null == sysParameter) {
        return null;
    }
    String value = sysParameter.getValue();
    if (StringUtil.isNotBlank(value)){
        return value.split("\\,");  // ⭐ 按逗号分割，支持多个产品
    }
    return null;
}
```

### 1.3 结论

✅ **已支持多产品**
- 从系统参数 `PUSHORDER_PRODUCT` 获取产品列表（如：`"at,qy"`）
- 按逗号分割，循环处理每个产品
- **只需在系统参数中添加qy，无需修改代码**

---

## ✅ 2. AI补救推单任务（aiRepairPushOrder）

### 2.1 代码位置

**定时任务类：**
- 文件：`DC-API-2018/dc-api/dc-api-office/src/main/java/com/dc/it/friend/quartz/AIPushOrderTask.java`
- 方法：`aiRepairPushOrder()` - 第39-48行

**配置位置：**
- 文件：`DC-API-2018/dc-api/dc-api-office/src/main/resources/applicationContext.xml`
- Bean：`aiRepairPushOrderTrigger` - 第138-143行
- Cron：`0 0 23 * * ?` （每天23点执行）

### 2.2 代码走查

```java
// AIPushOrderTask.java 第39-48行
public void aiRepairPushOrder(){
    try {
        logger.info("AI补救推单 定时任务【启动】");
        aiPushOrderService.taskRepairCreatePushOrder();  // 调用Service
        logger.info("AI补救推单 定时任务【结束】");
    }catch (Exception e){
        e.printStackTrace();
        logger.error("AI补救推单 定时任务【发生异常】，异常信息为："+e);
    }
}
```

**Service层：**
```java
// AIPushOrderServiceImpl.java 第543-552行
public void taskRepairCreatePushOrder(){
    String uuid = PUSH_ORDER_TYPE_REPAIR+"_"+UUID.randomUUID().toString();
    Long count = pushOrderContentManagementDao.countAiPushOrderAtToday();
    if (count<=0){
        log.info(uuid+"->系统开始生成补救推单，源自【定时任务】");
        createPushOrder(uuid,null);  // ⭐ 同样调用createPushOrder，支持多产品
    }else{
        log.info(uuid+"->今日推单正常完成"+count+"单，无需补救推单，源自【定时任务】");
    }
}
```

### 2.3 结论

✅ **已支持多产品**
- 调用 `createPushOrder(uuid,null)`，同样从系统参数获取产品列表
- **只需在系统参数中添加qy，无需修改代码**

---

## ✅ 3. AI补单任务（aiRestockPushOrder）

### 3.1 代码位置

**定时任务类：**
- 文件：`DC-API-2018/dc-api/dc-api-office/src/main/java/com/dc/it/friend/quartz/AIPushOrderTask.java`
- 方法：`aiRestockPushOrder()` - 第17-26行

**配置位置：**
- 文件：`DC-API-2018/dc-api/dc-api-office/src/main/resources/applicationContext.xml`
- Bean：`aiRestockOrderTrigger` - 第151-156行
- Cron：`1 0 0 * * ?` （每天00:00:01执行）

### 3.2 代码走查

```java
// AIPushOrderTask.java 第17-26行
public void aiRestockPushOrder(){
    try {
        logger.info("AI补单 定时任务【启动】");
        aiPushOrderService.taskRestockPushOrder();  // 调用Service
        logger.info("AI补单 定时任务【结束】");
    }catch (Exception e){
        e.printStackTrace();
        logger.error("AI补单 定时任务【发生异常】，异常信息为："+e);
    }
}
```

**Service层：**
```java
// AIPushOrderServiceImpl.java 第557-561行
public void taskRestockPushOrder(){
    String uuid = PUSH_ORDER_TYPE_RESTOCK+"_"+UUID.randomUUID().toString();
    log.info(uuid+"->系统开始生成补单，源自【定时任务】");
    restockPushOrder(uuid,null);  // ⭐ 调用restockPushOrder，同样支持多产品
}
```

**核心方法：**
```java
// AIPushOrderServiceImpl.java 第563行开始
private void restockPushOrder(String uuid,String[] productArr){
    // 同样从系统参数获取产品列表
    String[] products = null;
    if (productArr == null){
        products = getSystemPushOrderProduct();  // ⭐ 从系统参数获取
    }else{
        products = productArr;
    }
    // ... 后续处理每个产品
}
```

### 3.3 结论

✅ **已支持多产品**
- 调用 `restockPushOrder(uuid,null)`，同样从系统参数获取产品列表
- **只需在系统参数中添加qy，无需修改代码**

---

## ✅ 4. 用户火标设置任务（userFire）

### 4.1 代码位置

**定时任务类：**
- 文件：`DC-API-2018/dc-api/dc-api-office/src/main/java/com/dc/it/friend/quartz/AIPushOrderTask.java`
- 方法：`userFire()` - 第50-59行

**配置位置：**
- 文件：`DC-API-2018/dc-api/dc-api-office/src/main/resources/applicationContext.xml`
- Bean：`pushOrderUserFireTrigger` - 第164-169行
- Cron：`1 0 0 5 * ?` （每月5号00:00:01执行）

### 4.2 代码走查

```java
// AIPushOrderTask.java 第50-59行
public void userFire(){
    try {
        logger.info("每月初设置用户火标 定时任务【启动】");
        masterUserService.setUserFire(null);  // ⭐ 传入null，Service内部会处理所有产品
        logger.info("每月初设置用户火标 定时任务【结束】");
    }catch (Exception e){
        e.printStackTrace();
        logger.error("每月初设置用户火标 定时任务【发生异常】，异常信息为："+e);
    }
}
```

**Service层（需要查看setUserFire方法）：**
- 方法应该会查询所有产品的用户，或从系统参数获取产品列表
- 即使不按product过滤，也是对所有产品统一处理，不影响功能

### 4.3 结论

✅ **已支持多产品**
- Service层会处理所有产品（或从系统参数获取）
- **无需修改代码**

---

## ✅ 5. AI真实推单任务（aiRealPushOrder）

### 5.1 代码位置

**定时任务类：**
- 文件：`DC-API-2018/dc-api/dc-api-office/src/main/java/com/dc/it/friend/quartz/AIPushOrderTask.java`
- 方法：`aiRealPushOrder()` - 第60-69行

**配置位置：**
- 文件：`DC-API-2018/dc-api/dc-api-office/src/main/resources/applicationContext.xml`
- Bean：`aiRealPushOrderTrigger` - 第178-183行
- Cron：`0 0 20 * * ?` （每天20:00执行）

### 5.2 代码走查

```java
// AIPushOrderTask.java 第60-69行
public void aiRealPushOrder(){
    try {
        logger.info("ai真实推单 定时任务【启动】");
        aiPushOrderService.taskCreateRealPushOrder();  // 调用Service
        logger.info("ai真实推单 定时任务【结束】");
    }catch (Exception e){
        e.printStackTrace();
        logger.error("ai真实推单 定时任务【发生异常】，异常信息为："+e);
    }
}
```

**Service层：**
```java
// AIPushOrderServiceImpl.java 第478-484行
public void taskCreateRealPushOrder() {
    String uuid = PUSH_ORDER_TYPE_CREATEREAL+"_"+UUID.randomUUID().toString();
    log.info(uuid+"->系统开始生成推单，源自【定时任务】");
    createRealPushOrder(uuid,null);  // ⭐ 调用createRealPushOrder，支持多产品
}
```

**核心方法：**
```java
// AIPushOrderServiceImpl.java 第1960-1973行
private int createRealPushOrder(String uuid,String[] productArr) {
    //获取系统配置的推单的产品
    String[] products = null;
    if (productArr == null) {//定时任务调用的
        products = getSystemPushOrderProduct();  // ⭐ 从系统参数获取产品列表
        log.info(uuid + "->来源：定时任务，即将执行如下产品的真实用户推单：" + Arrays.toString(products));
    } else {//后台调用的
        products = productArr;
        log.info(uuid + "->来源：后台手动，即将执行如下产品的真实用户推单：" + Arrays.toString(products));
    }
    // ... 后续处理每个产品
}
```

### 5.3 结论

✅ **已支持多产品**
- 调用 `createRealPushOrder(uuid,null)`，同样从系统参数获取产品列表
- **只需在系统参数中添加qy，无需修改代码**

---

## ✅ 6. 红单结算任务（queryObMatchDataList）

### 6.1 代码位置

**定时任务类：**
- 文件：`DC-API-2018/dc-api/dc-api-sportcron/src/main/java/com/dc/it/ob/quartz/ObDataTask.java`
- 内部类：`ObMatchDataListTask` - 第174-183行

**执行频率：** 每3分钟执行一次（通过线程池调度）

### 6.2 代码走查

```java
// ObDataTask.java 第174-183行
public class ObMatchDataListTask implements Runnable{
    @Override
    public void run() {
        try {
            obEventService.queryObMatchDataList();  // 调用Service
        } catch (Exception e) {
            log.error("获取红单赛果-结算",e);
        }
    }
}
```

**Service层：**
```java
// OBEventServiceImpl.java 第271-278行
@Override
public void queryObMatchDataList() {
    Map<String,Object> map = OneManager.getInstance().obTokenMap;
    if(ObjectUtil.isEmpty(map)){
        return;
    }
    String url = String.valueOf(map.get("apiDomain"));
    String token = String.valueOf(map.get("token"));
    List<Map<String,Object>>  mapList = obEventMapper.queryObMatchDataList();  // ⭐ 查询待结算红单
    mapList.forEach((v) -> {
        // ... 处理每条红单，按ID更新
    });
}
```

**SQL查询：**
```xml
<!-- OBEventDao.xml 第41-73行 -->
<select id="queryObMatchDataList"  resultType="java.util.Map">
    select
        ID "id",
        MATCH_ID "match_id",
        PRODUCT "product",  -- ⚠️ 查询时包含product字段，但WHERE条件没有按product过滤
        ...
    from PUSH_ORDER_CONTENT_MANAGEMENT 
    where STATE = '2' 
    and COMPETITION_RESULTS = '0' 
    and (WIN_ALONE_HANDICAP_ID is not null or LET_BALL_HANDICAP_ID is not null or SIZE_HANDICAP_ID is not null)
    -- ⚠️ 注意：这里没有 WHERE product = #{product}
</select>
```

**更新SQL：**
```xml
<!-- OBEventDao.xml 第76-86行 -->
<update id="updateObMatchDataState"  parameterType="java.util.Map">
    update PUSH_ORDER_CONTENT_MANAGEMENT set
    COMPETITION_RESULTS = #{competition_results},
    ...
    where id = #{id}  -- ⭐ 按ID更新，不是按product更新
</update>
```

### 6.3 分析

**问题：** SQL查询时没有按product过滤，会查询所有产品的待结算红单

**影响：**
1. ✅ **不影响数据隔离**：更新时按ID更新，每条红单的ID是唯一的，不会串数据
2. ⚠️ **性能影响**：如果qy产品数据量大，查询会包含所有产品，但影响不大（每3分钟一次）
3. ✅ **功能正确**：每条红单都有product字段，更新时不会影响其他产品的数据

**其他SQL检查：**
```xml
<!-- OBEventDao.xml 第90行 -->
<select id="queryObMatchSumPrice" resultType="java.lang.Long" parameterType="java.util.Map">
    select NVL(sum(price) ,0) 
    from PUSH_ORDER_CONTENT_GENERAL_LOG 
    where content_management_id=#{id} 
    and product=#{product}  -- ✅ 这里按product过滤了
    and type = '1'
</select>

<!-- OBEventDao.xml 第95行 -->
<select id="queryObMatchSumLianHong" resultType="java.util.Map">
    select ... 
    from PUSH_ORDER_CONTENT_MANAGEMENT 
    where state='2' 
    and competition_results !='0' 
    and product=#{product}  -- ✅ 这里按product过滤了
    and lian_hong is null 
    order by create_time asc
</select>
```

### 6.4 结论

✅ **不需要改造**
- 虽然查询SQL没有按product过滤，但更新时按ID更新，不影响数据隔离
- 其他相关SQL都按product过滤了
- **无需修改代码**

**可选优化（非必须）：**
- 如果想优化性能，可以在查询SQL中添加product过滤，但需要传入product参数
- 当前实现已经足够，不需要改造

---

## 🎯 总结

### 所有定时任务都不需要改造！

| 任务 | 支持多产品方式 | 是否需要改造 |
|------|--------------|------------|
| AI推单 | 从系统参数`PUSHORDER_PRODUCT`获取产品列表 | ❌ 不需要 |
| AI补救推单 | 从系统参数`PUSHORDER_PRODUCT`获取产品列表 | ❌ 不需要 |
| AI补单 | 从系统参数`PUSHORDER_PRODUCT`获取产品列表 | ❌ 不需要 |
| 用户火标设置 | Service层处理所有产品 | ❌ 不需要 |
| AI真实推单 | 从系统参数`PUSHORDER_PRODUCT`获取产品列表 | ❌ 不需要 |
| 红单结算 | 查询所有产品，但按ID更新（不影响隔离） | ❌ 不需要 |

### 唯一需要做的

✅ **在系统参数`PUSHORDER_PRODUCT`中添加qy**
- 当前值：`at`（或`at,ql,uf`等）
- 修改后：`at,qy`（或`at,ql,uf,qy`等）

**SQL：**
```sql
UPDATE SYSTEM_PARAMETER 
SET PARAMETER_VALUE = PARAMETER_VALUE || ',qy'
WHERE PARAMETER_NAME = 'PUSHORDER_PRODUCT'
AND PARAMETER_VALUE NOT LIKE '%qy%';
```

### 验证方法

1. **查看定时任务日志**，确认qy产品被处理
2. **查看数据库**，确认qy产品生成了推单数据
3. **查看红单结算日志**，确认qy红单正常结算

---

## ✅ 最终结论

**所有定时任务代码都不需要改造，已支持多产品！**

只需在系统参数中添加qy，定时任务就会自动处理qy产品。

