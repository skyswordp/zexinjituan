#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import urllib.parse
import json

# AES 密钥和偏移量（从 AESUtil.java 中获取）
KEY = b"smkldospdosldaaa"  # 16 bytes
OFFSET = b"0000000000000000"  # 16 bytes

def decrypt_aes(encrypted_data):
    """
    解密 AES 加密的数据
    """
    try:
        # URL 解码
        decoded = urllib.parse.unquote(encrypted_data)

        # Base64 解码
        encrypted_bytes = base64.b64decode(decoded)

        # AES 解密
        cipher = AES.new(KEY, AES.MODE_CBC, OFFSET)
        decrypted = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)

        # 转换为字符串
        result = decrypted.decode('utf-8')
        return result
    except Exception as e:
        print(f"解密失败: {e}")
        return None

def main():
    print("=" * 80)
    print("【对比测试】gol8 vs pt777 requestData 解密对比")
    print("=" * 80)
    print()

    # gol8.92friend.net:5656 的 requestData
    gol8_request_data = "xMDluuAuUzRlpbKp1TCNyGZzHT9HhZWIJSRYW6JVVhyiraOBJYHbx3tdb3lq39cw3gXgPjxXKSMVQBh46e8gXl%2BUyS9jz8eImYGG%2BKk4l/TZOASuoQ2W0EM4euaPJuipdHi6XxkvX5gNqa/%2B2Fvth1RURPNpEP9ETT4um1gIqMU5CgsP28tAJh4N4ZxJqWZ7/9fEp1JbEogDn/qCDyBZ1n4vuNNk5v1cYbGP1bpa9t%2BZiG5/3xYiTXSrgNOvieFW9Mo4%2BFDeZUUAsrVR0W%2BtsnfhdQNCITEQ4/f23RyFjONL%2BClfCVPL8FU0K8CfV3URZagRWmYzgPSAY%2ByL8CgLk%2BQKTw%2Bj7x0kduoOgQC/W/C29G2jrlU4SVHa6aUpcL6DiBrEQIcyroKu7/r%2B2mWRwvlir5kmiuEz3gVY7FS9BU5/fc5HLT1gWdoRKAv8237ZX8OYLLW7JQa52BjZ18mke8M/ePdwmXtlxm2IElR9EMni5Kas9UNR9TsFOzAsFXpsVUjiM76zZD2fTYmrYwTJHmJQmHAOEkSDG8w/rphUBrlEJGWvVO9sHzfARWt7WKP9ohUajtVQDRYdRAwTRi12d7RC%2BANQGIQaSXZbLqSvc%2B/Ct7eh%2Bvl2tgD9fOm6tcRP4wmuArAsrufU3EQkfg5s0sJWtwe9tjP6rgZMJw2gyDn9/xRgYrhY33089j9uhZwfQn0W5rTXwUNgiNN1JZ1WQhK2SupIfxMh01r7Z1gGjt0%3D"

    # pt777aiguo.mypengyouquan.com 的 requestData
    pt777_request_data = "iTr578jJwj5dkYOcffTUZpuUYDlyAPg9QD3Vr3f0caY/CdmvzJtWc8IGGkaW8YZPByo8pgRf4yNPba7/1Gzh%2Bt8cSFOwyUaE9kct0ObWgLJHiTwjRGT1kQ1RoxxjdgAWCUFHtHMW8rwvgcpaTkJN7HwOw6ApeHRT9g7ij96doDKpZXuhc1XmQnOk/0ZKrdfhG0wZckuM6hgHYn/IP5AUBdRhmTDQ/U0CCplUvIKayt8oNQaN1SPTQVYX9%2BKIQFUD08IC9bAI8vM7jXS0kmKrVPQGWQE7GBP0OoeU%2BfbPl9Y%2B4TEs4o7aG6jh%2Bd98yTAtCCX%2BHGOmc/sMBa0ERzKABpPTAXBhv2zFC1neTJ5jlWLq1nZu%2BqfD34g7b2AZKkuBjRGCLzd%2BRjXtTUCTGYZqvRuQtmNZbfD/%2BBuRgkMR8HaxtKjAbwFH3pxQUH/qjiLWWsdu76Jz6oSQbYF4dbqdi/W1CsISBUJVpBfMbAv9fvwbmY6jKRgGu4rGAyQI8WvatP7Mr8LQLRak/itxf0N0wStGG0hV1/IRolJ9rNIYExibfwDLmSTGwXdx5KB0dY5NCd66cn5JBH2mjuViDKsG7hZ/RnIC4Loqq/668EUO4rH/RfNWVYXvrz/8FcmJrjTX3iwcmqN3nittczuFOUfDUV7triYlVL/tZYmOTxPxBPxExcoGzqK0hPJ%2BQeIK1p7q9WkoBpUCqBMzQaHr1Nx7v3wjZ4qI9b27AohH9A8DHfE%3D"

    # 解密 gol8
    print("【1. GOL8 请求数据】")
    print("域名: gol8.92friend.net:5656")
    print("-" * 80)

    gol8_decrypted = decrypt_aes(gol8_request_data)
    if gol8_decrypted:
        print("解密后的 JSON:")
        print(gol8_decrypted)
        print()
        try:
            gol8_json = json.loads(gol8_decrypted)
            print("格式化后的 JSON:")
            print(json.dumps(gol8_json, indent=2, ensure_ascii=False))
        except:
            print("JSON 解析失败")
    else:
        print("解密失败！")

    print()
    print("=" * 80)
    print()

    # 解密 pt777
    print("【2. PT777 请求数据】")
    print("域名: pt777aiguo.mypengyouquan.com")
    print("-" * 80)

    pt777_decrypted = decrypt_aes(pt777_request_data)
    if pt777_decrypted:
        print("解密后的 JSON:")
        print(pt777_decrypted)
        print()
        try:
            pt777_json = json.loads(pt777_decrypted)
            print("格式化后的 JSON:")
            print(json.dumps(pt777_json, indent=2, ensure_ascii=False))
        except:
            print("JSON 解析失败")
    else:
        print("解密失败！")

    print()
    print("=" * 80)
    print()

    # 对比差异
    if gol8_decrypted and pt777_decrypted:
        print("【3. 差异对比】")
        print("=" * 80)

        try:
            gol8_json = json.loads(gol8_decrypted)
            pt777_json = json.loads(pt777_decrypted)

            # 对比 sid
            print("\n【sid 对比】")
            gol8_sid = gol8_json.get("sid", "null")
            pt777_sid = pt777_json.get("sid", "null")
            print(f"  gol8:  {gol8_sid}")
            print(f"  pt777: {pt777_sid}")
            print(f"  是否相同: {gol8_sid == pt777_sid}")

            # 对比 product
            print("\n【product 对比】")
            gol8_product = gol8_json.get("product", "null")
            pt777_product = pt777_json.get("product", "null")
            print(f"  gol8:  {gol8_product}")
            print(f"  pt777: {pt777_product}")
            print(f"  是否相同: {gol8_product == pt777_product}")

            # 对比 data 字段
            print("\n【data 字段对比】")
            gol8_data = gol8_json.get("data", {})
            pt777_data = pt777_json.get("data", {})

            print("\n  gol8 data 字段:")
            for key, value in gol8_data.items():
                print(f"    {key}: {value}")

            print("\n  pt777 data 字段:")
            for key, value in pt777_data.items():
                print(f"    {key}: {value}")

            # 找出差异
            print("\n【字段差异】")
            all_keys = set(gol8_data.keys()) | set(pt777_data.keys())
            has_diff = False
            for key in sorted(all_keys):
                gol8_value = gol8_data.get(key, "【不存在】")
                pt777_value = pt777_data.get(key, "【不存在】")
                if gol8_value != pt777_value:
                    has_diff = True
                    print(f"  {key}:")
                    print(f"    gol8:  {gol8_value}")
                    print(f"    pt777: {pt777_value}")

            if not has_diff:
                print("  ✓ 所有字段值相同")

        except Exception as e:
            print(f"对比失败: {e}")

    print()
    print("=" * 80)
    print("✓ 解密对比完成！")

if __name__ == "__main__":
    main()
