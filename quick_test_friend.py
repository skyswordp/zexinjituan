#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动 Friend 微服务测试脚本
================================
最简化版本，直接启动 Friend 服务进行测试

用法：
  python quick_test_friend.py              # 直接测试编译好的 WAR（快速）
  python quick_test_friend.py --rebuild    # 重新编译后测试
  python quick_test_friend.py --port 9090  # 指定端口
"""

import subprocess
import sys
import os
import io
import time
import requests
import argparse
from datetime import datetime
from pathlib import Path

# 修复编码
if sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

WORKSPACE_ROOT = r'C:\Users\DEVTrump\projects'
FRIEND_MODULE = os.path.join(WORKSPACE_ROOT, 'DC-Workspace', 'DC-API-2018', 'dc-api', 'dc-api-friend')
TEST_SCRIPT = os.path.join(WORKSPACE_ROOT, 'test_api_local.py')
TOMCAT_HOME = r'C:\apache-tomcat-8.5.100'
LOG_DIR = os.path.join(WORKSPACE_ROOT, 'logs')

os.makedirs(LOG_DIR, exist_ok=True)

class SimpleLogger:
    def log(self, msg, level=''):
        ts = datetime.now().strftime('%H:%M:%S')
        print(f"[{ts}] {level:>6} {msg}")

logger = SimpleLogger()

def find_war():
    """查找编译好的 WAR 文件"""
    war_file = os.path.join(FRIEND_MODULE, 'target', 'dc-api-friend.war')
    if os.path.exists(war_file):
        logger.log(f"找到 WAR: {war_file}", 'OK')
        return war_file
    logger.log("❌ WAR 文件不存在，请先编译", 'ERROR')
    return None

def rebuild():
    """重新编译 Friend 模块"""
    logger.log("📦 编译 Friend 模块...", 'INFO')
    
    mvn = 'mvn'
    m2_home = os.environ.get('M2_HOME')
    if m2_home:
        mvn = os.path.join(m2_home, 'bin', 'mvn.cmd')
    
    result = subprocess.run(
        [mvn, 'clean', 'package', '-DskipTests', '-q'],
        cwd=FRIEND_MODULE,
        capture_output=True,
        text=True,
        timeout=600
    )
    
    if result.returncode == 0:
        logger.log("✓ 编译成功", 'OK')
        return find_war()
    else:
        logger.log(f"❌ 编译失败: {result.stderr[:200]}", 'ERROR')
        return None

def deploy_and_start(war_file, port=8081):
    """部署 WAR 并启动 Tomcat"""
    logger.log(f"部署到 Tomcat (端口 {port})...", 'INFO')
    
    # 复制 WAR
    webapps_dir = os.path.join(TOMCAT_HOME, 'webapps')
    dest_war = os.path.join(webapps_dir, 'friend.war')
    
    try:
        if os.path.exists(dest_war):
            os.remove(dest_war)
        import shutil
        shutil.copy2(war_file, dest_war)
        logger.log(f"✓ WAR 已部署", 'OK')
    except Exception as e:
        logger.log(f"❌ 部署失败: {e}", 'ERROR')
        return None
    
    # 启动 Tomcat
    catalina = os.path.join(TOMCAT_HOME, 'bin', 'catalina.bat')
    logger.log("🚀 启动 Tomcat...", 'INFO')
    
    try:
        process = subprocess.Popen(
            [catalina, 'run'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        logger.log(f"✓ Tomcat 已启动 (PID: {process.pid})", 'OK')
        return process
    except Exception as e:
        logger.log(f"❌ 启动失败: {e}", 'ERROR')
        return None

def wait_service(port, timeout=120):
    """等待服务就绪"""
    logger.log(f"⏳ 等待服务启动 (最多 {timeout} 秒)...", 'INFO')
    
    start = time.time()
    check_url = f'http://localhost:{port}/'
    
    while time.time() - start < timeout:
        try:
            response = requests.get(check_url, timeout=2)
            if response.status_code in [200, 404, 405]:
                logger.log(f"✓ 服务已就绪", 'OK')
                return True
        except:
            pass
        
        elapsed = int(time.time() - start)
        if elapsed % 10 == 0:
            logger.log(f"等待中... ({elapsed}s)", 'INFO')
        
        time.sleep(1)
    
    logger.log(f"❌ 服务启动超时", 'ERROR')
    return False

def run_tests(port):
    """运行测试"""
    logger.log(f"🧪 运行测试...", 'INFO')
    
    cmd = [
        sys.executable,
        TEST_SCRIPT,
        '--port', str(port),
        '--no-details'
    ]
    
    try:
        result = subprocess.run(cmd, cwd=WORKSPACE_ROOT, timeout=300)
        return result.returncode == 0
    except Exception as e:
        logger.log(f"❌ 测试失败: {e}", 'ERROR')
        return False

def main():
    parser = argparse.ArgumentParser(description='快速启动 Friend 服务测试')
    parser.add_argument('--rebuild', action='store_true', help='重新编译')
    parser.add_argument('--port', type=int, default=8081, help='服务端口')
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("Friend 微服务快速测试")
    print("="*70 + "\n")
    
    # 1. 查找或编译 WAR
    if args.rebuild:
        war_file = rebuild()
    else:
        war_file = find_war()
    
    if not war_file:
        sys.exit(1)
    
    # 2. 启动服务
    process = deploy_and_start(war_file, args.port)
    if not process:
        sys.exit(1)
    
    try:
        # 3. 等待就绪
        if not wait_service(args.port):
            sys.exit(1)
        
        # 4. 运行测试
        if run_tests(args.port):
            logger.log("✅ 测试通过", 'OK')
        else:
            logger.log("⚠️  测试失败，请检查日志", 'WARN')
        
    finally:
        # 5. 停止服务
        logger.log("🛑 停止服务...", 'INFO')
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()
        logger.log("✓ 已停止", 'OK')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已中止")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
