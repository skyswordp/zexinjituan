#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FriendController API 测试脚本
可直接在 VS Code 中运行查看详细的执行日志
日志输出到 C:\Users\DEVTrump\projects\logs
"""

import requests
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Tuple

# 禁用 SSL 警告（测试环境）
requests.packages.urllib3.disable_warnings()

class APITester:
    def __init__(self):
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': '__snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C',
            'Origin': 'https://e68web01.itomtest.com',
            'Referer': 'https://e68web01.itomtest.com/Dynamic',
            'X-Debug-Enabled': 'true'  # ✅ 开启网关层 debug 模式，返回 traceId
        }
        
        # 初始化日志目录
        self.log_dir = r'C:\Users\DEVTrump\projects\logs'
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f"api_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        self.log_content = []  # 日志内容缓冲
        
        self.tests = [
            {'name': '1. getUser', 'url': 'https://e68web01.itomtest.com/api/friend/user/1.0/getUser', 'body': {'id': '488714', 'userId': '488714'}},
            {'name': '2. getMyPraiseCount', 'url': 'https://e68web01.itomtest.com/api/friend/user/1.0/getMyPraiseCount', 'body': {'userId': '488714'}},
            {'name': '3. update', 'url': 'https://e68web01.itomtest.com/api/friend/user/1.0/update', 'body': {'id': '488714', 'nickName': 'test', 'headUrl': 'https://example.com/new.png'}},
            {'name': '4. saveFollow', 'url': 'https://e68web01.itomtest.com/api/friend/user/1.0/saveFollow', 'body': {'userId': '488714', 'beUserId': '100001', 'type': '1'}},
            {'name': '5. readCount', 'url': 'https://e68web01.itomtest.com/api/friend/user/1.0/readCount', 'body': {'type': '1', 'id': '1689288'}},
            {'name': '6. saveShare', 'url': 'https://e68web01.itomtest.com/api/friend/user/1.0/saveShare', 'body': {'userId': 489714, 'circleId': 1689288}},
            {'name': '7. saveChangePraise', 'url': 'https://e68web01.itomtest.com/api/friend/user/1.0/saveChangePraise', 'body': {'userId': 489714, 'praiseType': '1', 'type': '1', 'circleId': 1689288}},
            {'name': '8. getLevel', 'url': 'https://e68web01.itomtest.com/api/friend/levelSetting/1.0/getLevel', 'body': {'account': 'adults123', 'money': 0, 'levelId': '1'}},
            {'name': '9. board-index', 'url': 'https://e68web01.itomtest.com/api/friend/board/index/getByLevel', 'body': {'boardLevel': 1}},
            {'name': '10. board-guess', 'url': 'https://e68web01.itomtest.com/api/friend/board/guess/getByLevel', 'body': {'boardLevel': 1}},
            {'name': '11. getCountList', 'url': 'https://e68web01.itomtest.com/api/friend/circle/1.0/getCountList', 'body': {'time': '1706345600000'}},
            {'name': '12. saveCircle', 'url': 'https://e68web01.itomtest.com/api/friend/circle/1.0/saveCircle', 'body': {'userId': '489714', 'content': 'test'}},
            {'name': '13. pageList-circle', 'url': 'https://e68web01.itomtest.com/api/friend/circle/2.0/pageList', 'body': {'pageNum': 1, 'pageSize': 20}},
            {'name': '14. pageList-index', 'url': 'https://e68web01.itomtest.com/api/friend/indexSetting/1.0/pageList', 'body': {'pageNum': 1, 'pageSize': 20}},
            {'name': '15. pageList-game', 'url': 'https://e68web01.itomtest.com/api/friend/gameSetting/1.0/pageList', 'body': {'pageNum': 1, 'pageSize': 20}},
            {'name': '16. queryTitle', 'url': 'https://e68web01.itomtest.com/api/friend/topic/1.0/queryTitle', 'body': {}},
            {'name': '17. queryDetails', 'url': 'https://e68web01.itomtest.com/api/friend/topic/1.0/queryDetails', 'body': {'topicId': 1, 'pageNum': 1, 'pageSize': 20}},
            {'name': '18. queryTasks', 'url': 'https://e68web01.itomtest.com/api/friend/task/1.0/queryTasks', 'body': {'userId': 489714}},
            {'name': '19. pageList-comments', 'url': 'https://e68web01.itomtest.com/api/friend/circleComments/1.0/pageList', 'body': {'circleId': 1689288, 'pageNum': 1, 'pageSize': 20}},
            {'name': '20. saveComments', 'url': 'https://e68web01.itomtest.com/api/friend/circleComments/1.0/saveComments', 'body': {'circleId': '1689288', 'userId': '489714', 'content': 'test'}},
            {'name': '21. saveReport', 'url': 'https://e68web01.itomtest.com/api/friend/report/1.0/saveReport', 'body': {'id': '1689288', 'userId': '489714', 'type': '1', 'reportReason': 'test'}},
        ]
        
        self.results = []
        self.pass_count = 0
        self.fail_count = 0
    
    def log(self, msg: str):
        """写入日志"""
        self.log_content.append(msg)
    
    def generate_curl_command(self, url: str, body: Dict, headers: Dict) -> str:
        """生成 PowerShell 可执行的 CURL 命令"""
        # PowerShell 格式的 CURL 命令
        curl_cmd = f'curl.exe -X POST "{url}" `\n'
        
        # 添加所有 headers
        for key, value in headers.items():
            # PowerShell 需要转义双引号
            escaped_value = value.replace('"', '\\"')
            curl_cmd += f'  -H "{key}: {escaped_value}" `\n'
        
        # 添加 body（JSON 格式）
        json_body = json.dumps(body, ensure_ascii=False)
        # PowerShell 中单引号不需要转义内部双引号
        curl_cmd += f"  -d '{json_body}' `\n"
        curl_cmd += "  --insecure"
        
        return curl_cmd
    
    def flush_log(self):
        """刷新日志到文件"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.log_content))
    
    def print_header(self):
        """打印测试开始头"""
        header_text = "\n" + "="*80 + f"\n🚀 FriendController API 测试执行 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" + "="*80 + "\n"
        print(header_text)
        self.log(header_text)
    
    def run_test(self, test_idx: int, test: Dict) -> Dict:
        """执行单个测试"""
        name = test['name']
        url = test['url']
        body = test['body']
        
        # 只在控制台显示简要进度
        progress = f"[{test_idx:2d}/{len(self.tests)}] {name} ... "
        print(progress, end='', flush=True)
        
        try:
            start_time = time.time()
            response = requests.post(
                url, 
                json=body, 
                headers=self.headers, 
                timeout=10, 
                verify=False
            )
            elapsed_ms = (time.time() - start_time) * 1000
            
            status_code = response.status_code
            response_text = response.text
            
            # 尝试解析JSON
            try:
                response_json = response.json()
            except:
                response_json = None
            
            # 判断成功/失败：HTTP 200 且 code == "10000"
            if status_code == 200 and response_json and response_json.get('code') == '10000':
                status = "✅ PASS"
                self.pass_count += 1
            else:
                status = "❌ FAIL"
                self.fail_count += 1
            
            # 简要输出到控制台
            print(status)
            
            # 详细信息写入日志
            self.log(f"\n[{test_idx}/{len(self.tests)}] {name}")
            self.log(f"  URL: {url}")
            self.log(f"  状态: {status} | HTTP: {status_code} | 耗时: {elapsed_ms:.1f}ms")
            if response_json:
                self.log(f"  响应码: {response_json.get('code', 'N/A')} | 消息: {response_json.get('message', 'N/A')}")
                # 打印 debug 信息（如果有）
                if '_debug' in response_json:
                    self.log(f"  🔍 Debug: {response_json['_debug']}")
            
            # 生成 PowerShell 可执行的 CURL 命令
            curl_cmd = self.generate_curl_command(url, body, self.headers)
            self.log(f"\n  📋 PowerShell CURL 命令:")
            self.log(f"  {curl_cmd}")
            
            result = {
                'name': name,
                'url': url,
                'body': body,
                'status': 'PASS' if (status_code == 200 and response_json and response_json.get('code') == '10000') else 'FAIL',
                'status_code': status_code,
                'elapsed_ms': elapsed_ms,
                'response': response_json if response_json else response_text,
                'error': None
            }
            
        except Exception as e:
            print(f"❌ FAIL")
            self.fail_count += 1
            
            self.log(f"\n[{test_idx}/{len(self.tests)}] {name}")
            self.log(f"  URL: {url}")
            self.log(f"  状态: ❌ FAIL")
            self.log(f"  错误: {str(e)}")
            
            # 异常时也打印 CURL 命令，方便手动调试
            curl_cmd = self.generate_curl_command(url, body, self.headers)
            self.log(f"\n  📋 PowerShell CURL 命令:")
            self.log(f"  {curl_cmd}")
            
            result = {
                'name': name,
                'url': url,
                'body': body,
                'status': 'FAIL',
                'status_code': None,
                'elapsed_ms': None,
                'response': None,
                'error': str(e)
            }
        
        self.results.append(result)
        return result
    
    def print_summary(self):
        """汇总信息写入日志"""
        summary = "\n" + "="*100 + "\n📊 测试汇总 - 快速预览\n" + "="*100 + "\n"
        summary += f"{'序号':<5} {'API名称':<25} {'状态':<8} {'HTTP':<6} {'响应码':<8} {'耗时':<8}\n"
        summary += "-"*100 + "\n"
        
        for idx, result in enumerate(self.results, 1):
            status_symbol = "✅" if result['status'] == 'PASS' else "❌"
            resp_code = result['response'].get('code', 'N/A') if isinstance(result['response'], dict) else 'N/A'
            time_str = f"{result['elapsed_ms']:.0f}ms" if result['elapsed_ms'] else "N/A"
            
            summary += f"{idx:<5} {result['name']:<25} {status_symbol:<8} {result['status_code'] or 'N/A':<6} {str(resp_code):<8} {time_str:<8}\n"
        
        summary += "-"*100 + "\n"
        summary += f"\n总计: {len(self.tests)} | ✅ 通过: {self.pass_count} | ❌ 失败: {self.fail_count} | 成功率: {self.pass_count/len(self.tests)*100:.1f}%\n"
        
        # 统计耗时
        times = [r['elapsed_ms'] for r in self.results if r['elapsed_ms']]
        if times:
            total_time = sum(times)
            avg_time = total_time / len(times)
            min_time = min(times)
            max_time = max(times)
            summary += f"\n耗时统计: 总计 {total_time:.0f}ms | 平均 {avg_time:.0f}ms | 最快 {min_time:.0f}ms | 最慢 {max_time:.0f}ms\n"
        
        summary += "="*100 + "\n"
        
        self.log(summary)
    
    def print_details(self):
        """详细结果写入日志"""
        details = "\n📋 详细结果 - 逐项展开\n" + "="*100 + "\n"
        
        for idx, result in enumerate(self.results, 1):
            details += f"\n【{idx:2d}】 {result['name']}\n"
            details += "-" * 100 + "\n"
            details += f"URL: {result['url']}\n"
            details += f"状态: {'✅ PASS' if result['status'] == 'PASS' else '❌ FAIL'}\n"
            
            if result['status_code']:
                resp_code = result['response'].get('code', 'N/A') if isinstance(result['response'], dict) else 'N/A'
                resp_msg = result['response'].get('message', 'N/A') if isinstance(result['response'], dict) else 'N/A'
                details += f"HTTP状态码: {result['status_code']} | 响应码: {resp_code} | 消息: {resp_msg}\n"
            
            if result['elapsed_ms']:
                details += f"耗时: {result['elapsed_ms']:.1f}ms\n"
            
            details += f"\n请求参数:\n"
            details += json.dumps(result['body'], indent=2, ensure_ascii=False) + "\n"
            
            # 添加 CURL 命令到详细结果
            curl_cmd = self.generate_curl_command(result['url'], result['body'], self.headers)
            details += f"\nPowerShell CURL 命令（可直接复制执行）:\n"
            details += curl_cmd + "\n\n"
            
            if result['error']:
                details += f"\n错误信息:\n"
                details += result['error'] + "\n"
            else:
                details += f"\n完整响应数据:\n"
                if isinstance(result['response'], dict):
                    details += json.dumps(result['response'], indent=2, ensure_ascii=False) + "\n"
                else:
                    details += str(result['response']) + "\n"
            
            details += "-" * 100 + "\n"
        
        self.log(details)
    
    def run_all(self, show_details=True):
        """执行所有测试"""
        self.print_header()
        
        for idx, test in enumerate(self.tests, 1):
            self.run_test(idx, test)
        
        self.print_summary()
        
        if show_details:
            self.print_details()
        
        # 保存日志到文件
        self.flush_log()
        
        # 打印最终结果提示
        print("\n" + "="*80)
        print(f"✅ 测试完成！日志已保存到:")
        print(f"📄 {self.log_file}")
        print("="*80 + "\n")


def main():
    """主函数"""
    # 设置控制台编码
    import sys
    if sys.stdout.encoding.lower() != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("\n\n")
    print("╔" + "═"*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "🔥 FriendController API 测试工具".center(78) + "║")
    print("║" + "在 VS Code 中直接运行查看详细执行日志".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "═"*78 + "╝")
    
    tester = APITester()
    tester.run_all(show_details=True)
    
    print("\n✨ 测试完成！按 Ctrl+C 退出...\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 测试已中止")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
