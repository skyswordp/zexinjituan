# CRM 系统访问地址汇总

## 各产品 CRM 登录地址

### QY 项目
- **AWS5 环境**: https://eqqycrm.wotingshuoyumingyuechangyuehao2333heheda.com
- **AWS6 环境**: https://sgqycrm.wotingshuoyumingyuechangyuehao2333heheda.com
- **内部解析源**:
  - AWS5: qy-crm-5.prod-all-env.com
  - AWS6: qy-crm-6.prod-all-env.com

### RB88 项目
- **AWS5 环境**: https://aws5crm.qweurnzxv1834mnvb-rb88.com
- **AWS6 环境**: https://aws6crm.qweurnzxv1834mnvb-rb88.com
- **内部解析源**:
  - AWS5: rb88-crm-5.prod-all-env.com
  - AWS6: rb88-crm-6.prod-all-env.com

### E68 项目
- **AWS5 环境**: https://eqe68crm.wotingshuoyumingyuechangyuehao2333heheda.com
- **AWS6 环境**: https://sge68crm.wotingshuoyumingyuechangyuehao2333heheda.com

### Long8 项目
- **AWS5 环境**: https://eqlong8crm.wotingshuoyumingyuechangyuehao2333heheda.com
- **AWS6 环境**: https://sglong8crm.wotingshuoyumingyuechangyuehao2333heheda.com

### PT777 项目
- **AWS5 环境**: https://eqpt777crm.wotingshuoyumingyuechangyuehao2333heheda.com
- **AWS6 环境**: https://sgpt777crm.wotingshuoyumingyuechangyuehao2333heheda.com

### SportOne (TQ) 项目
- **AWS5 环境**: https://awshkcrm.p68eqjobsnr90wndpoeo4l1x-tq.com
- **AWS6 环境**: https://awsjpcrm.p68eqjobsnr90wndpoeo4l1x-tq.com

### UED 项目
- **AWS5 环境**: https://awshkcrm.wqnfuidshjoicjdsaiou023hchds98au-ued.com
- **AWS6 环境**: https://awsjpcrm.wqnfuidshjoicjdsaiou023hchds98au-ued.com

### JXF 项目
- **AWS5 环境**: https://aws5crm.xzcvbqweoiru1298lkjh-jxf.com
- **AWS6 环境**: https://aws6crm.xzcvbqweoiru1298lkjh-jxf.com

## CRM 系统说明

### 功能概述
CRM 是原来给电销使用的后台系统,后来作为大数据分析使用的后台,主要功能包括:
- 提案分析
- 数据综合分析
- 存款通道分析
- 存提分析
- 系统洗码分析
- 登录存款数分析
- 客服转用维护
- 额度审核
- 等其他大数据分析功能

### 技术架构
- **前端**: crm_frontend (静态资源)
- **后端**: crm_backend
- **容器服务名称**: {product}-crmfd (前端) / {product}-crmbd (后端)
- **负责人**: Dev Nice

### 环境说明
- **AWS5**: 香港 AWS 环境 (前缀: eqqy/aws5)
- **AWS6**: 日本 AWS 环境 (前缀: sgqy/aws6)

### 注意事项
1. CRM 定时器会影响汇报机器人发送数据
2. 只需一个容器启动计划任务即可
3. 各产品 CRM 系统数据相互独立
4. 访问 CRM 系统需要对应产品的账号权限

## 参考文档
- 详细配置信息请参考: `production-docs-detail/service-info/product-service/crm.md`
- 产品服务信息请参考各产品对应的 md 文件 (如 `qy.md`, `rb88.md`)
