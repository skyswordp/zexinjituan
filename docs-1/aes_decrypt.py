#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AES 解密工具 - 用于解密 PNG APP 的 requestData
基于 Java DecryptTool.java 实现

使用方法:
    python aes_decrypt.py "加密的requestData字符串"
    
或在代码中调用:
    from aes_decrypt import decrypt
    result = decrypt("xMDluuAuUzRl...")
"""

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import urllib.parse
import sys
import json

# AES 密钥和初始化向量
KEY = "smkldospdosldaaa"
IV = "0000000000000000"


def decrypt(src):
    """
    解密 AES/CBC/PKCS5Padding 加密的数据
    
    Args:
        src (str): URL 编码后的 Base64 加密数据
        
    Returns:
        str: 解密后的 UTF-8 字符串
    """
    try:
        # 1. URL 解码
        decoded = urllib.parse.unquote(src)
        
        # 2. Base64 解码
        encrypted_bytes = base64.b64decode(decoded)
        
        # 3. AES 解密
        key_bytes = KEY.encode('ascii')
        iv_bytes = IV.encode('ascii')
        
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        
        # 4. PKCS5Padding 移除（在 Python 中即为 PKCS7）
        original = unpad(decrypted_bytes, AES.block_size)
        
        # 5. 转换为 UTF-8 字符串
        return original.decode('utf-8')
        
    except Exception as e:
        print(f"解密失败: {e}", file=sys.stderr)
        return None


def decrypt_and_parse_json(src):
    """
    解密并解析 JSON
    
    Args:
        src (str): URL 编码后的 Base64 加密数据
        
    Returns:
        dict: 解析后的 JSON 对象，若失败返回 None
    """
    decrypted = decrypt(src)
    if decrypted is None:
        return None
    
    try:
        return json.loads(decrypted)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}", file=sys.stderr)
        return None


def compare_two_requests():
    """
    对比两个不同域名的 requestData
    """
    print("=" * 80)
    print("【requestData 解密对比】")
    print("=" * 80)
    print()

    # gol8.92friend.net:5656 的 requestData
    gol8_request_data = "xMDluuAuUzRlpbKp1TCNyGZzHT9HhZWIJSRYW6JVVhyiraOBJYHbx3tdb3lq39cw3gXgPjxXKSMVQBh46e8gXl%2BUyS9jz8eImYGG%2BKk4l/TZOASuoQ2W0EM4euaPJuipdHi6XxkvX5gNqa/%2B2Fvth1RURPNpEP9ETT4um1gIqMU5CgsP28tAJh4N4ZxJqWZ7/9fEp1JbEogDn/qCDyBZ1n4vuNNk5v1cYbGP1bpa9t%2BZiG5/3xYiTXSrgNOvieFW9Mo4%2BFDeZUUAsrVR0W%2BtsnfhdQNCITEQ4/f23RyFjONL%2BClfCVPL8FU0K8CfV3URZagRWmYzgPSAY%2ByL8CgLk%2BQKTw%2Bj7x0kduoOgQC/W/C29G2jrlU4SVHa6aUpcL6DiBrEQIcyroKu7/r%2B2mWRwvlir5kmiuEz3gVY7FS9BU5/fc5HLT1gWdoRKAv8237ZX8OYLLW7JQa52BjZ18mke8M/ePdwmXtlxm2IElR9EMni5Kas9UNR9TsFOzAsFXpsVUjiM76zZD2fTYmrYwTJHmJQmHAOEkSDG8w/rphUBrlEJGWvVO9sHzfARWt7WKP9ohUajtVQDRYdRAwTRi12d7RC%2BANQGIQaSXZbLqSvc%2B/Ct7eh%2Bvl2tgD9fOm6tcRP4wmuArAsrufU3EQkfg5s0sJWtwe9tjP6rgZMJw2gyDn9/xRgYrhY33089j9uhZwfQn0W5rTXwUNgiNN1JZ1WQhK2SupIfxMh01r7Z1gGjt0%3D"

    # pt777aiguo.mypengyouquan.com 的 requestData
    pt777_request_data = "iTr578jJwj5dkYOcffTUZpuUYDlyAPg9QD3Vr3f0caY/CdmvzJtWc8IGGkaW8YZPByo8pgRf4yNPba7/1Gzh%2Bt8cSFOwyUaE9kct0ObWgLJHiTwjRGT1kQ1RoxxjdgAWCUFHtHMW8rwvgcpaTkJN7HwOw6ApeHRT9g7ij96doDKpZXuhc1XmQnOk/0ZKrdfhG0wZckuM6hgHYn/IP5AUBdRhmTDQ/U0CCplUvIKayt8oNQaN1SPTQVYX9%2BKIQFUD08IC9bAI8vM7jXS0kmKrVPQGWQE7GBP0OoeU%2BfbPl9Y%2B4TEs4o7aG6jh%2Bd98yTAtCCX%2BHGOmc/sMBa0ERzKABpPTAXBhv2zFC1neTJ5jlWLq1nZu%2BqfD34g7b2AZKkuBjRGCLzd%2BRjXtTUCTGYZqvRuQtmNZbfD/%2BBuRgkMR8HaxtKjAbwFH3pxQUH/qjiLWWsdu76Jz6oSQbYF4dbqdi/W1CsISBUJVpBfMbAv9fvwbmY6jKRgGu4rGAyQI8WvatP7Mr8LQLRak/itxf0N0wStGG0hV1/IRolJ9rNIYExibfwDLmSTGwXdx5KB0dY5NCd66cn5JBH2mjuViDKsG7hZ/RnIC4Loqq/668EUO4rH/RfNWVYXvrz/8FcmJrjTX3iwcmqN3nittczuFOUfDUV7triYlVL/tZYmOTxPxBPxExcoGzqK0hPJ%2BQeIK1p7q9WkoBpUCqBMzQaHr1Nx7v3wjZ4qI9b27AohH9A8DHfE%3D"

    print("【1. GOL8 的 requestData 解密】")
    print("域名: gol8.92friend.net:5656")
    print("-" * 80)
    gol8_decrypted = decrypt(gol8_request_data)
    if gol8_decrypted:
        print(gol8_decrypted)
        try:
            gol8_json = json.loads(gol8_decrypted)
            print("\n【GOL8 - 解析后的 JSON】")
            print(json.dumps(gol8_json, ensure_ascii=False, indent=2))
        except:
            pass
    else:
        print("解密失败！")

    print()
    print("=" * 80)
    print()

    print("【2. PT777 的 requestData 解密】")
    print("域名: pt777aiguo.mypengyouquan.com")
    print("-" * 80)
    pt777_decrypted = decrypt(pt777_request_data)
    if pt777_decrypted:
        print(pt777_decrypted)
        try:
            pt777_json = json.loads(pt777_decrypted)
            print("\n【PT777 - 解析后的 JSON】")
            print(json.dumps(pt777_json, ensure_ascii=False, indent=2))
        except:
            pass
    else:
        print("解密失败！")

    print()
    print("=" * 80)
    print("✓ 解密完成！请对比上面两个 JSON 的差异")
    print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行模式：传入加密字符串
        encrypted_data = sys.argv[1]
        result = decrypt(encrypted_data)
        if result:
            print(result)
            # 尝试解析为 JSON 并美化输出
            try:
                json_obj = json.loads(result)
                print("\n【解析后的 JSON】")
                print(json.dumps(json_obj, ensure_ascii=False, indent=2))
            except:
                pass
    else:
        # 默认模式：对比两个请求
        compare_two_requests()
