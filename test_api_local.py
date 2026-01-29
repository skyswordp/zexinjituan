#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FriendController API 本地开发测试脚本
========================================
用途：本地开发环境中直接测试 Friend 模块接口

支持两种模式：
1. 远程测试：连接到 e68web01.itomtest.com（需要 VPN）
2. 本地测试：连接到 http://localhost:8081（本地开发）

用法：
  python test_api_local.py                    # 默认连接本地
  python test_api_local.py --remote           # 连接远程测试环境
  python test_api_local.py --url http://127.0.0.1:8081   # 指定 URL

特点：
  - 完全兼容 test_api.py 的测试用例
  - 自动转换 URL 和 Headers
  - 详细的日志输出和错误诊断
  - 兼容本地 H2 数据库和生产 Oracle 数据库
"""

import requests
import json
import time
import os
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# 禁用 SSL 警告（测试环境）
requests.packages.urllib3.disable_warnings()

class Colors:
    """ANSI 颜色代码"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class APITester:
    def __init__(self, base_url: str, mode: str = 'local'):
        self.base_url = base_url.rstrip('/')
        self.mode = mode  # 'local' 或 'remote'
        
        # 根据模式设置 Headers
        if mode == 'local':
            self.headers = {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json;charset=UTF-8',
            }
        else:
            # 远程环境需要保持原有的 Cookie 和 Referer
            self.headers = {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json;charset=UTF-8',
                'Cookie': '__snaker__id=jvOJbjKJWgJZ7mEl; JSESSIONID=E85595B704A736F259DBA0CAC72DCF0C',
                'Origin': 'https://e68web01.itomtest.com',
                'Referer': 'https://e68web01.itomtest.com/Dynamic'
            }
        
        # 初始化日志目录
        self.log_dir = r'C:\Users\DEVTrump\projects\logs'
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f"api_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        self.log_content = []
        self.results = []
        self.pass_count = 0
        self.fail_count = 0
        
        # 测试用例（原始）
        self._init_tests()
    
    def _init_tests(self):
        """初始化测试用例"""
        # 这些是原始的远程 URL，将在 run_test 时转换为本地 URL
        self.tests = [
            {'name': '1. getUser', 'path': '/api/friend/user/1.0/getUser', 'body': {'id': '488714', 'userId': '488714'}},
            {'name': '2. getMyPraiseCount', 'path': '/api/friend/user/1.0/getMyPraiseCount', 'body': {'userId': '488714'}},
            {'name': '3. update', 'path': '/api/friend/user/1.0/update', 'body': {'id': '488714', 'nickName': 'test', 'headUrl': 'https://example.com/new.png'}},
            {'name': '4. saveFollow', 'path': '/api/friend/user/1.0/saveFollow', 'body': {'userId': '488714', 'beUserId': 100001, 'type': '1'}},
            {'name': '5. readCount', 'path': '/api/friend/user/1.0/readCount', 'body': {'type': '1', 'id': 1689288}},
            {'name': '6. saveShare', 'path': '/api/friend/user/1.0/saveShare', 'body': {'userId': 489714, 'circleId': 1689288}},
            {'name': '7. saveChangePraise', 'path': '/api/friend/user/1.0/saveChangePraise', 'body': {'userId': 489714, 'praiseType': '1', 'type': '1', 'circleId': 1689288}},
            {'name': '8. getLevel', 'path': '/api/friend/levelSetting/1.0/getLevel', 'body': {'account': 'adults123', 'money': 0, 'levelId': '1'}},
            {'name': '9. board-index', 'path': '/api/friend/board/index/getByLevel', 'body': {'boardLevel': 1}},
            {'name': '10. board-guess', 'path': '/api/friend/board/guess/getByLevel', 'body': {'boardLevel': 1}},
            {'name': '11. getCountList', 'path': '/api/friend/circle/1.0/getCountList', 'body': {'time': '1706345600000'}},
            {'name': '12. saveCircle', 'path': '/api/friend/circle/1.0/saveCircle', 'body': {'userId': 489714, 'content': 'test'}},
            {'name': '13. pageList-circle', 'path': '/api/friend/circle/2.0/pageList', 'body': {'pageNum': 1, 'pageSize': 20}},
            {'name': '14. pageList-index', 'path': '/api/friend/indexSetting/1.0/pageList', 'body': {'pageNum': 1, 'pageSize': 20}},
            {'name': '15. pageList-game', 'path': '/api/friend/gameSetting/1.0/pageList', 'body': {'pageNum': 1, 'pageSize': 20}},
            {'name': '16. queryTitle', 'path': '/api/friend/topic/1.0/queryTitle', 'body': {}},
            {'name': '17. queryDetails', 'path': '/api/friend/topic/1.0/queryDetails', 'body': {'topicId': 1, 'pageNum': 1, 'pageSize': 20}},
            {'name': '18. queryTasks', 'path': '/api/friend/task/1.0/queryTasks', 'body': {'userId': 489714}},
            {'name': '19. pageList-comments', 'path': '/api/friend/circleComments/1.0/pageList', 'body': {'circleId': 1689288, 'pageNum': 1, 'pageSize': 20}},
            {'name': '20. saveComments', 'path': '/api/friend/circleComments/1.0/saveComments', 'body': {'circleId': 1689288, 'userId': 489714, 'content': 'test'}},
            {'name': '21. saveReport', 'path': '/api/friend/report/1.0/saveReport', 'body': {'reportName': 'adults123', 'beReportName': 'user2', 'fCircleId': 1689288, 'content': 'test', 'reportReason': 'test'}},
        ]
    
    def log(self, msg: str):
        """记录日志"""
        self.log_content.append(msg)
    
    def flush_log(self):
        """刷新日志到文件"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.log_content))
    
    def print_header(self):
        """打印测试开始头"""
        header_text = "\n" + "="*80
        header_text += f"\n🚀 FriendController API 测试执行"
        header_text += f"\n📍 模式: {self.mode.upper()} | 地址: {self.base_url}"
        header_text += f"\n⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        header_text += "\n" + "="*80 + "\n"
        print(header_text)
        self.log(header_text)
    
    def run_test(self, test_idx: int, test: Dict) -> Dict:
        """执行单个测试"""
        name = test['name']
        path = test['path']
        url = self.base_url + path
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
            
            # 尝试解析 JSON
            try:
                response_json = response.json()
            except:
                response_json = None
            
            # 判断成功/失败：HTTP 200 且 code == "10000" 或包含数据
            success = status_code == 200 and (
                (response_json and response_json.get('code') == '10000') or
                (response_json and 'data' in response_json)
            )
            
            status_symbol = "✅" if success else "❌"
            self.pass_count += success
            self.fail_count += not success
            
            # 简要输出到控制台
            print(f"{status_symbol} {status_code}")
            
            # 详细信息写入日志
            self.log(f"\n[{test_idx}/{len(self.tests)}] {name}")
            self.log(f"  URL: {url}")
            self.log(f"  状态: {status_symbol} | HTTP: {status_code} | 耗时: {elapsed_ms:.1f}ms")
            if response_json:
                self.log(f"  响应码: {response_json.get('code', 'N/A')} | 消息: {response_json.get('message', 'N/A')}")
            
            result = {
                'name': name,
                'path': path,
                'url': url,
                'body': body,
                'status': 'PASS' if success else 'FAIL',
                'status_code': status_code,
                'elapsed_ms': elapsed_ms,
                'response': response_json if response_json else response_text,
                'error': None
            }
            
        except requests.exceptions.ConnectionError as e:
            print(f"❌ 连接失败")
            self.fail_count += 1
            self.log(f"\n[{test_idx}/{len(self.tests)}] {name}")
            self.log(f"  URL: {url}")
            self.log(f"  状态: ❌ 连接失败")
            self.log(f"  错误: 无法连接到服务器")
            self.log(f"  详情: {str(e)}")
            
            result = {
                'name': name,
                'path': path,
                'url': url,
                'body': body,
                'status': 'FAIL',
                'status_code': None,
                'elapsed_ms': None,
                'response': None,
                'error': f"Connection Error: {str(e)}"
            }
            
        except Exception as e:
            print(f"❌ 错误")
            self.fail_count += 1
            self.log(f"\n[{test_idx}/{len(self.tests)}] {name}")
            self.log(f"  URL: {url}")
            self.log(f"  状态: ❌ 错误")
            self.log(f"  错误: {str(e)}")
            
            result = {
                'name': name,
                'path': path,
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
        summary = "\n" + "="*100 + "\n📊 测试汇总\n" + "="*100 + "\n"
        summary += f"{'序号':<5} {'API名称':<25} {'状态':<8} {'HTTP':<6} {'响应码':<8} {'耗时':<8}\n"
        summary += "-"*100 + "\n"
        
        for idx, result in enumerate(self.results, 1):
            status_symbol = "✅" if result['status'] == 'PASS' else "❌"
            resp_code = result['response'].get('code', 'N/A') if isinstance(result['response'], dict) else 'N/A'
            time_str = f"{result['elapsed_ms']:.0f}ms" if result['elapsed_ms'] else "N/A"
            http_code = str(result['status_code']) if result['status_code'] else 'N/A'
            
            summary += f"{idx:<5} {result['name']:<25} {status_symbol:<8} {http_code:<6} {str(resp_code):<8} {time_str:<8}\n"
        
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
        print("\n" + summary)
    
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
            
            if result['error']:
                details += f"\n错误信息:\n"
                details += result['error'] + "\n"
            else:
                if result['response']:
                    details += f"\n完整响应数据:\n"
                    if isinstance(result['response'], dict):
                        details += json.dumps(result['response'], indent=2, ensure_ascii=False) + "\n"
                    else:
                        details += str(result['response']) + "\n"
            
            details += "-" * 100 + "\n"
        
        self.log(details)
    
    def run_all(self, show_details: bool = True):
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
        print(f"✅ 测试完成！详细日志已保存到:")
        print(f"📄 {self.log_file}")
        print("="*80 + "\n")
        
        return self.pass_count == len(self.tests)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='FriendController API 本地开发测试脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：
  python test_api_local.py                      # 本地模式（localhost:8081）
  python test_api_local.py --remote             # 远程模式（e68web01.itomtest.com）
  python test_api_local.py --url http://192.168.1.100:8081   # 自定义 URL
        """
    )
    parser.add_argument(
        '--remote',
        action='store_true',
        help='连接到远程测试环境（e68web01.itomtest.com）'
    )
    parser.add_argument(
        '--url',
        type=str,
        help='自定义基础 URL（默认 http://localhost:8081）'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8081,
        help='本地端口（仅在 --remote 未指定时使用，默认 8081）'
    )
    parser.add_argument(
        '--no-details',
        action='store_true',
        help='不显示详细结果'
    )
    
    args = parser.parse_args()
    
    # 确定模式和 URL
    if args.remote:
        base_url = 'https://e68web01.itomtest.com'
        mode = 'remote'
    elif args.url:
        base_url = args.url
        mode = 'custom'
    else:
        base_url = f'http://localhost:{args.port}'
        mode = 'local'
    
    # 打印启动信息
    print("\n")
    print("╔" + "═"*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "🎯 FriendController API 本地开发测试".center(78) + "║")
    print("║" + f"模式: {mode.upper()} | 地址: {base_url}".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "═"*78 + "╝")
    print()
    
    # 检查连接
    print(f"⏳ 检查连接 {base_url} ...")
    try:
        response = requests.get(base_url, timeout=3, verify=False)
        print(f"✅ 连接成功\n")
    except requests.exceptions.ConnectionError:
        print(f"❌ 连接失败！无法连接到 {base_url}")
        print(f"⚠️  请确认:")
        print(f"   1. 服务已启动")
        print(f"   2. URL 正确: {base_url}")
        print(f"   3. 网络连接正常")
        sys.exit(1)
    except Exception as e:
        print(f"⚠️  连接检查失败: {e}\n")
    
    # 运行测试
    tester = APITester(base_url, mode=mode)
    success = tester.run_all(show_details=not args.no_details)
    
    print("\n✨ 测试完成！按 Ctrl+C 退出...\n")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 测试已中止")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
