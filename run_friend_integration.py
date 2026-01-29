#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Friend 模块一体化启动脚本
=================================
功能：一条龙式启动和测试 dc-api-friend 模块
  1. 检查依赖和环境
  2. 自动编译 dc-api-friend 模块
  3. 启动 dc-api-friend 服务
  4. 等待服务就绪（检查健康检查接口）
  5. 运行 test_api.py 测试
  6. 收集和展示测试结果及错误日志

用法：
  python3 run_friend_integration.py [--skip-build] [--friend-port=8081]

参数：
  --skip-build        跳过编译步骤
  --friend-port       Friend 服务端口（默认 8081）
  --gateway-port      网关服务端口（默认 8080）
  --test-url          指定测试 API 的基础 URL（默认 http://localhost:8080）
"""

import subprocess
import sys
import os
import io
import time
import json
import requests
import argparse
import threading
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, Dict, List

# 修复编码
if sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding.lower() not in ('utf-8', 'utf8'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 配置
WORKSPACE_ROOT = r'C:\Users\DEVTrump\projects'
DC_WORKSPACE = os.path.join(WORKSPACE_ROOT, 'DC-Workspace', 'DC-API-2018')
DC_PARENT_PATH = os.path.join(WORKSPACE_ROOT, 'dc-parent')  # dc-api-web 所在路径
DC_API_WEB_PATH = os.path.join(DC_PARENT_PATH, 'dc-api-web')  # 网关服务路径
FRIEND_MODULE_PATH = os.path.join(DC_WORKSPACE, 'dc-api', 'dc-api-friend')  # Friend 微服务路径
TEST_SCRIPT = os.path.join(WORKSPACE_ROOT, 'docs-1', 'FriendController', 'test_api.py')
LOG_DIR = os.path.join(WORKSPACE_ROOT, 'logs')
INTEGRATION_LOG_FILE = os.path.join(LOG_DIR, f'integration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

# 确保日志目录存在
os.makedirs(LOG_DIR, exist_ok=True)

class Colors:
    """终端颜色"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def disable():
        Colors.HEADER = Colors.BLUE = Colors.CYAN = Colors.GREEN = Colors.YELLOW = Colors.RED = Colors.ENDC = Colors.BOLD = ''

class Logger:
    """日志管理"""
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.messages: List[str] = []
        self._write_header()
    
    def _write_header(self):
        header = f"\n{'='*80}\nFriend 模块集成测试 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*80}\n"
        self.log(header)
    
    def log(self, msg: str, level: str = 'INFO', color: str = ''):
        """记录日志"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        formatted_msg = f"[{timestamp}] [{level}] {msg}"
        
        # 终端输出
        if color:
            print(f"{color}{formatted_msg}{Colors.ENDC}")
        else:
            print(formatted_msg)
        
        # 文件输出
        self.messages.append(formatted_msg)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(formatted_msg + '\n')
    
    def info(self, msg: str):
        self.log(msg, 'INFO', Colors.CYAN)
    
    def success(self, msg: str):
        self.log(msg, 'SUCCESS', Colors.GREEN)
    
    def warning(self, msg: str):
        self.log(msg, 'WARN', Colors.YELLOW)
    
    def error(self, msg: str):
        self.log(msg, 'ERROR', Colors.RED)
    
    def debug(self, msg: str):
        self.log(msg, 'DEBUG', Colors.BLUE)

logger = Logger(INTEGRATION_LOG_FILE)

def check_prerequisites() -> bool:
    """检查先决条件"""
    logger.info("🔍 检查先决条件...")
    
    checks = [
        ('Java 环境', lambda: _check_command('java -version')),
        ('Maven 环境', lambda: _check_command('mvn -version')),
        ('Python 环境', lambda: _check_command('python --version')),
        ('Git 环境', lambda: _check_command('git --version')),
    ]
    
    all_ok = True
    for name, check_fn in checks:
        if check_fn():
            logger.success(f"✓ {name} 已安装")
        else:
            logger.error(f"✗ {name} 未安装或不可用")
            all_ok = False
    
    return all_ok

def _check_command(cmd: str) -> bool:
    """检查命令是否可用"""
    try:
        parts = cmd.split()
        # 对于 mvn，也尝试从 M2_HOME 环境变量查找
        if parts[0] == 'mvn':
            m2_home = os.environ.get('M2_HOME')
            maven_home = os.environ.get('MAVEN_HOME')
            maven_path = None
            
            if m2_home:
                maven_path = os.path.join(m2_home, 'bin', 'mvn.cmd')
            elif maven_home:
                maven_path = os.path.join(maven_home, 'bin', 'mvn.cmd')
            
            if maven_path and os.path.exists(maven_path):
                return True
            
            # 尝试标准命令
            try:
                subprocess.run(parts, capture_output=True, timeout=5)
                return True
            except Exception:
                return False
        
        subprocess.run(parts, capture_output=True, timeout=5)
        return True
    except Exception:
        return False

def _get_maven_cmd() -> str:
    """获取 Maven 命令"""
    # 首先尝试环境变量
    m2_home = os.environ.get('M2_HOME')
    maven_home = os.environ.get('MAVEN_HOME')
    
    if m2_home:
        maven_cmd = os.path.join(m2_home, 'bin', 'mvn.cmd')
        if os.path.exists(maven_cmd):
            return maven_cmd
    
    if maven_home:
        maven_cmd = os.path.join(maven_home, 'bin', 'mvn.cmd')
        if os.path.exists(maven_cmd):
            return maven_cmd
    
    # 否则尝试 PATH 中的 mvn
    return 'mvn'

def build_friend_module(skip_build: bool = False) -> bool:
    """编译 dc-api-friend 模块"""
    if skip_build:
        logger.warning("⊘ 跳过编译步骤")
        return True
    
    logger.info("📦 开始编译 dc-api-friend 模块和 dc-api-web 网关...")
    logger.debug(f"Friend 模块路径: {FRIEND_MODULE_PATH}")
    logger.debug(f"网关服务路径: {DC_API_WEB_PATH}")
    
    # 检查路径
    if not os.path.exists(FRIEND_MODULE_PATH):
        logger.error(f"✗ Friend 模块路径不存在: {FRIEND_MODULE_PATH}")
        return False
    
    if not os.path.exists(DC_API_WEB_PATH):
        logger.error(f"✗ 网关服务路径不存在: {DC_API_WEB_PATH}")
        return False
    
    try:
        # 获取 Maven 命令
        mvn_cmd = _get_maven_cmd()
        
        # 1. 先编译父模块（如果需要）
        logger.debug("编译 dc-parent 父模块...")
        parent_result = subprocess.run(
            [mvn_cmd, 'clean', 'install', '-DskipTests', '-q'],
            cwd=DC_PARENT_PATH,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if parent_result.returncode != 0:
            logger.warning(f"⚠ 父模块编译有警告:\n{parent_result.stderr[:500]}")
        
        # 2. 编译 dc-api-web 网关
        logger.debug("编译 dc-api-web 网关...")
        web_result = subprocess.run(
            [mvn_cmd, 'clean', 'package', '-DskipTests', '-q'],
            cwd=DC_API_WEB_PATH,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if web_result.returncode != 0:
            logger.warning(f"⚠ dc-api-web 编译失败:\n{web_result.stderr[:500]}")
            # 不中断，继续编译 Friend
        else:
            logger.success("✓ dc-api-web 网关编译成功")
        
        # 3. 编译整个 DC-API-2018 项目
        logger.debug("编译 DC-API-2018 整体项目...")
        dc_result = subprocess.run(
            [mvn_cmd, 'clean', 'install', '-DskipTests', '-q'],
            cwd=DC_WORKSPACE,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if dc_result.returncode != 0:
            logger.warning(f"⚠ DC-API-2018 编译有警告:\n{dc_result.stderr[:500]}")
        
        # 4. 编译 Friend 模块
        logger.debug("编译 Friend 模块...")
        build_result = subprocess.run(
            [mvn_cmd, 'clean', 'package', '-DskipTests', '-q'],
            cwd=FRIEND_MODULE_PATH,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if build_result.returncode == 0:
            logger.success("✓ Friend 模块编译成功")
            return True
        else:
            logger.error(f"✗ Friend 模块编译失败:\n{build_result.stderr[:500]}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("✗ 编译超时（超过 10 分钟）")
        return False
    except Exception as e:
        logger.error(f"✗ 编译异常: {str(e)}")
        return False

def find_jar_file(module_path: str) -> Optional[str]:
    """查找 JAR 文件（或 WAR 文件）"""
    target_dir = os.path.join(module_path, 'target')
    
    if not os.path.exists(target_dir):
        logger.error(f"✗ target 目录不存在: {target_dir}")
        return None
    
    # 先查找 JAR
    jar_files = list(Path(target_dir).glob('*.jar'))
    jar_files = [j for j in jar_files if 'sources' not in str(j) and 'javadoc' not in str(j)]
    
    # 如果没有 JAR，查找 WAR
    if not jar_files:
        war_files = list(Path(target_dir).glob('*.war'))
        war_files = [w for w in war_files if 'sources' not in str(w) and 'javadoc' not in str(w)]
        if war_files:
            war_file = max(war_files, key=lambda x: x.stat().st_size)
            logger.debug(f"找到 WAR 文件: {war_file}")
            return str(war_file)
    
    if not jar_files:
        logger.error(f"✗ 未找到 JAR 或 WAR 文件在: {target_dir}")
        return None
    
    # 选择最大的 JAR（通常是带依赖的 JAR）
    jar_file = max(jar_files, key=lambda x: x.stat().st_size)
    logger.debug(f"找到 JAR 文件: {jar_file}")
    return str(jar_file)

def start_friend_service(jar_file: str, port: int = 8081) -> Tuple[Optional[subprocess.Popen], int]:
    """启动 Friend 服务"""
    
    # 判断是 JAR 还是 WAR
    if jar_file.endswith('.war'):
        return _deploy_war_to_tomcat(jar_file, port)
    else:
        return _start_jar_service(jar_file, port)

def _start_jar_service(jar_file: str, port: int = 8081) -> Tuple[Optional[subprocess.Popen], int]:
    """启动 JAR 服务"""
    logger.info(f"🚀 启动 Friend 微服务 (JAR 模式, 端口: {port})...")
    
    if not os.path.exists(jar_file):
        logger.error(f"✗ JAR 文件不存在: {jar_file}")
        return None, 0
    
    # 使用 -local profile 启动（开发模式 H2 数据库）
    cmd = [
        'java',
        '-Dspring.profiles.active=local',
        '-Dserver.port=' + str(port),
        '-jar',
        jar_file
    ]
    
    logger.debug(f"启动命令: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        logger.success(f"✓ Friend 微服务进程已启动 (PID: {process.pid})")
        return process, process.pid
        
    except Exception as e:
        logger.error(f"✗ 启动 Friend 服务失败: {str(e)}")
        return None, 0

def _deploy_war_to_tomcat(war_file: str, port: int = 8081) -> Tuple[Optional[subprocess.Popen], int]:
    """部署 WAR 到 Tomcat"""
    logger.info(f"🚀 部署 Friend 微服务 (WAR 模式, Tomcat 端口: {port})...")
    
    if not os.path.exists(war_file):
        logger.error(f"✗ WAR 文件不存在: {war_file}")
        return None, 0
    
    tomcat_home = r'C:\apache-tomcat-8.5.100'
    
    if not os.path.exists(tomcat_home):
        logger.error(f"✗ Tomcat 未找到: {tomcat_home}")
        logger.info("💡 提示: 检查 Tomcat 安装路径，或使用 --no-gateway 跳过此步骤")
        return None, 0
    
    # 检查 Tomcat 是否在运行
    try:
        response = requests.get(f'http://localhost:{port}', timeout=2)
        logger.warning(f"⚠️  Tomcat 已在运行 (端口 {port})")
        return None, 0
    except requests.exceptions.RequestException:
        pass
    
    logger.debug(f"部署 WAR 到 Tomcat: {tomcat_home}")
    logger.debug(f"WAR 文件: {war_file}")
    
    # 将 WAR 复制到 Tomcat webapps
    import shutil
    webapps_dir = os.path.join(tomcat_home, 'webapps')
    app_name = 'friend'
    dest_war = os.path.join(webapps_dir, f'{app_name}.war')
    
    try:
        if os.path.exists(dest_war):
            os.remove(dest_war)
        
        shutil.copy2(war_file, dest_war)
        logger.debug(f"✓ WAR 已复制到: {dest_war}")
        
    except Exception as e:
        logger.error(f"✗ 部署失败: {str(e)}")
        return None, 0
    
    # 启动 Tomcat
    catalina_script = os.path.join(tomcat_home, 'bin', 'catalina.bat')
    
    if not os.path.exists(catalina_script):
        logger.error(f"✗ Tomcat 启动脚本不存在: {catalina_script}")
        return None, 0
    
    try:
        # 在后台启动 Tomcat
        cmd = [catalina_script, 'run']
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        logger.success(f"✓ Tomcat 进程已启动 (PID: {process.pid})")
        logger.debug("⏳ 等待 WAR 部署和应用启动，这可能需要 30-60 秒...")
        return process, process.pid
        
    except Exception as e:
        logger.error(f"✗ 启动 Tomcat 失败: {str(e)}")
        return None, 0

def find_web_jar_file(module_path: str) -> Optional[str]:
    """查找 dc-api-web 的 JAR 文件"""
    target_dir = os.path.join(module_path, 'target')
    
    if not os.path.exists(target_dir):
        logger.error(f"✗ target 目录不存在: {target_dir}")
        return None
    
    jar_files = list(Path(target_dir).glob('*.jar'))
    jar_files = [j for j in jar_files if 'sources' not in str(j) and 'javadoc' not in str(j)]
    
    if not jar_files:
        logger.error(f"✗ 未找到 JAR 文件在: {target_dir}")
        return None
    
    # 选择最大的 JAR（通常是带依赖的 JAR）
    jar_file = max(jar_files, key=lambda x: x.stat().st_size)
    logger.debug(f"找到 dc-api-web JAR 文件: {jar_file}")
    return str(jar_file)

def start_web_gateway(jar_file: str, port: int = 8080, friend_url: str = 'http://localhost:8081') -> Tuple[Optional[subprocess.Popen], int]:
    """启动 dc-api-web 网关服务"""
    logger.info(f"🚀 启动 dc-api-web 网关服务 (端口: {port})...")
    logger.debug(f"转发到 Friend 服务: {friend_url}")
    
    if not os.path.exists(jar_file):
        logger.error(f"✗ JAR 文件不存在: {jar_file}")
        return None, 0
    
    # 网关服务配置
    cmd = [
        'java',
        '-Dserver.port=' + str(port),
        '-Dapi.friend.url=' + friend_url,  # 转发地址
        '-jar',
        jar_file
    ]
    
    logger.debug(f"启动命令: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        logger.success(f"✓ dc-api-web 网关进程已启动 (PID: {process.pid})")
        return process, process.pid
        
    except Exception as e:
        logger.error(f"✗ 启动 dc-api-web 网关失败: {str(e)}")
        return None, 0

def wait_for_service(port: int, max_wait: int = 120, interval: int = 5, service_name: str = "服务") -> bool:
    """等待服务就绪"""
    logger.info(f"⏳ 等待 {service_name}启动 (最多 {max_wait} 秒)...")
    
    health_url = f'http://localhost:{port}/actuator/health'
    start_time = time.time()
    last_log_time = 0
    
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(health_url, timeout=3)
            if response.status_code == 200:
                logger.success(f"✓ {service_name}已启动就绪")
                return True
        except requests.exceptions.RequestException:
            pass
        
        # 如果没有 /actuator/health，尝试简单的 ping
        try:
            response = requests.get(f'http://localhost:{port}/', timeout=3)
            if response.status_code in [200, 404, 405]:  # 任何响应都说明服务在运行
                logger.success(f"✓ {service_name}已启动就绪")
                return True
        except requests.exceptions.RequestException:
            pass
        
        elapsed = int(time.time() - start_time)
        
        # 每 15 秒输出一次进度
        if elapsed - last_log_time >= 15 or elapsed == interval:
            logger.debug(f"等待中... ({elapsed}s/{max_wait}s)")
            last_log_time = elapsed
            
            # 如果是 Tomcat (端口通常是 8080 或 8081)，尝试检查日志
            if port in [8080, 8081, 8082]:
                _check_tomcat_logs()
        
        time.sleep(interval)
    
    logger.error(f"✗ {service_name}启动超时 ({max_wait}s)")
    
    # 最后尝试查看 Tomcat 日志
    if port in [8080, 8081, 8082]:
        logger.warning("尝试查看 Tomcat 日志以诊断问题...")
        _check_tomcat_logs()
    
    return False

def _check_tomcat_logs():
    """检查 Tomcat 日志，诊断问题"""
    tomcat_home = r'C:\apache-tomcat-8.5.100'
    log_dir = os.path.join(tomcat_home, 'logs')
    
    if not os.path.exists(log_dir):
        return
    
    # 查找最新的 catalina 日志
    catalina_logs = []
    for f in os.listdir(log_dir):
        if f.startswith('catalina') and f.endswith('.log'):
            catalina_logs.append(os.path.join(log_dir, f))
    
    if catalina_logs:
        latest_log = max(catalina_logs, key=os.path.getmtime)
        try:
            with open(latest_log, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()[-20:]  # 最后 20 行
                logger.debug("最近的 Tomcat 日志:")
                for line in lines:
                    if 'ERROR' in line or '严重' in line or 'Exception' in line:
                        logger.error(f"  {line.strip()}")
                    elif 'WARN' in line or '警告' in line:
                        logger.warning(f"  {line.strip()}")
        except Exception as e:
            logger.debug(f"无法读取日志: {e}")

def run_tests(test_url: str) -> bool:
    """运行测试脚本"""
    logger.info(f"🧪 运行测试脚本: {TEST_SCRIPT}")
    logger.debug(f"测试 URL: {test_url}")
    
    if not os.path.exists(TEST_SCRIPT):
        logger.error(f"✗ 测试脚本不存在: {TEST_SCRIPT}")
        return False
    
    # 修改测试脚本中的 API 地址为本地地址（如果需要）
    # 这里假设 test_api.py 已经配置好了基础 URL
    
    try:
        # 在新的 Python 进程中运行测试
        result = subprocess.run(
            [sys.executable, TEST_SCRIPT],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=os.path.dirname(TEST_SCRIPT)
        )
        
        logger.info("📋 测试输出:")
        print("\n" + result.stdout)
        
        if result.stderr:
            logger.warning("测试错误输出:")
            print(result.stderr)
        
        if result.returncode == 0:
            logger.success("✓ 测试通过")
            return True
        else:
            logger.error(f"✗ 测试失败 (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("✗ 测试超时")
        return False
    except Exception as e:
        logger.error(f"✗ 测试异常: {str(e)}")
        return False

def collect_service_logs(process: subprocess.Popen, log_file: str):
    """收集服务日志"""
    logger.debug("开始收集服务日志...")
    
    try:
        stdout, stderr = process.communicate(timeout=1)
    except subprocess.TimeoutExpired:
        # 进程仍在运行，获取当前输出
        try:
            stdout, stderr = process.communicate(timeout=1)
        except subprocess.TimeoutExpired:
            logger.debug("服务仍在运行，未能收集完整日志")
            return
    
    if stdout:
        logger.debug("服务标准输出:")
        print(stdout[:2000])  # 只显示前 2000 字符
    
    if stderr:
        logger.debug("服务错误输出:")
        print(stderr[:2000])

def cleanup(process: Optional[subprocess.Popen]):
    """清理资源"""
    if process:
        logger.info("🛑 停止 Friend 服务...")
        try:
            process.terminate()
            process.wait(timeout=5)
            logger.success("✓ 服务已停止")
        except subprocess.TimeoutExpired:
            logger.warning("⚠ 服务未及时停止，强制杀死...")
            process.kill()

def main():
    parser = argparse.ArgumentParser(description='Friend 模块一体化启动和测试脚本')
    parser.add_argument('--skip-build', action='store_true', help='跳过编译步骤')
    parser.add_argument('--friend-port', type=int, default=8081, help='Friend 服务端口 (默认 8081)')
    parser.add_argument('--gateway-port', type=int, default=8080, help='网关服务端口 (默认 8080)')
    parser.add_argument('--test-url', type=str, help='测试 API 基础 URL (默认 http://localhost:GATEWAY_PORT)')
    parser.add_argument('--no-color', action='store_true', help='禁用彩色输出')
    parser.add_argument('--no-gateway', action='store_true', help='不启动网关，直接测试 Friend 服务')
    
    args = parser.parse_args()
    
    if args.no_color:
        Colors.disable()
    
    logger.info(f"{'='*80}")
    logger.info("🎯 Friend 模块一体化启动和测试")
    logger.info(f"{'='*80}")
    logger.info(f"工作空间: {WORKSPACE_ROOT}")
    logger.info(f"网关服务: {DC_API_WEB_PATH}")
    logger.info(f"Friend 微服务: {FRIEND_MODULE_PATH}")
    logger.info(f"测试脚本: {TEST_SCRIPT}")
    logger.info(f"日志文件: {INTEGRATION_LOG_FILE}")
    
    if args.no_gateway:
        logger.warning("⚠️  将跳过网关，直接测试 Friend 服务（非完整链路）")
    else:
        logger.info("✓ 启用完整网关链路: test_api → FriendController (网关) → Friend 微服务")
    
    logger.info(f"{'='*80}\n")
    
    # 1. 检查先决条件
    if not check_prerequisites():
        logger.error("❌ 先决条件检查失败，请安装必要的工具")
        sys.exit(1)
    
    # 2. 编译模块
    if not build_friend_module(skip_build=args.skip_build):
        logger.error("❌ 编译失败")
        sys.exit(1)
    
    processes = []
    
    try:
        # 3. 启动 Friend 微服务
        friend_jar = find_jar_file(FRIEND_MODULE_PATH)
        if not friend_jar:
            logger.error("❌ 未找到 Friend 模块的 JAR 文件")
            sys.exit(1)
        
        friend_process, friend_pid = start_friend_service(friend_jar, port=args.friend_port)
        if not friend_process:
            logger.error("❌ 启动 Friend 微服务失败")
            sys.exit(1)
        processes.append(("Friend", friend_process))
        
        # 等待 Friend 服务启动
        if not wait_for_service(args.friend_port, service_name="Friend微服务"):
            logger.error("❌ Friend 微服务启动失败或超时")
            sys.exit(1)
        
        # 4. 启动网关服务（可选）
        if not args.no_gateway:
            web_jar = find_web_jar_file(DC_API_WEB_PATH)
            if not web_jar:
                logger.warning("⚠️  未找到 dc-api-web 的 JAR 文件，尝试编译...")
                # 尝试单独编译
                result = subprocess.run(
                    ['mvn', 'clean', 'package', '-DskipTests', '-q'],
                    cwd=DC_API_WEB_PATH,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode == 0:
                    web_jar = find_web_jar_file(DC_API_WEB_PATH)
            
            if web_jar:
                friend_service_url = f'http://localhost:{args.friend_port}'
                gateway_process, gateway_pid = start_web_gateway(
                    web_jar, 
                    port=args.gateway_port,
                    friend_url=friend_service_url
                )
                if gateway_process:
                    processes.append(("Gateway", gateway_process))
                    
                    # 等待网关启动
                    if not wait_for_service(args.gateway_port, service_name="网关服务"):
                        logger.error("❌ 网关服务启动失败或超时")
                        sys.exit(1)
                    
                    test_url = args.test_url or f'http://localhost:{args.gateway_port}'
                    logger.success(f"✓ 完整链路就绪: test_api → {test_url} (网关) → {friend_service_url} (Friend 微服务)")
                else:
                    logger.warning("⚠️  启动网关失败，将直接测试 Friend 服务")
                    test_url = f'http://localhost:{args.friend_port}'
            else:
                logger.warning("⚠️  找不到 dc-api-web JAR，将直接测试 Friend 服务")
                test_url = f'http://localhost:{args.friend_port}'
        else:
            test_url = args.test_url or f'http://localhost:{args.friend_port}'
        
        # 5. 运行测试
        test_success = run_tests(test_url)
        
        # 最终统计
        logger.info(f"\n{'='*80}")
        if test_success:
            logger.success("✅ 全部测试通过")
        else:
            logger.warning("⚠️ 部分测试失败，请检查日志")
        logger.info(f"{'='*80}\n")
        
        sys.exit(0 if test_success else 1)
        
    finally:
        # 清理所有启动的进程
        for service_name, process in reversed(processes):
            logger.info(f"🛑 停止 {service_name} 服务...")
            try:
                process.terminate()
                process.wait(timeout=5)
                logger.success(f"✓ {service_name} 已停止")
            except subprocess.TimeoutExpired:
                logger.warning(f"⚠ {service_name} 未及时停止，强制杀死...")
                process.kill()
        
        logger.info(f"\n📄 详细日志已保存到: {INTEGRATION_LOG_FILE}")

if __name__ == '__main__':
    main()
