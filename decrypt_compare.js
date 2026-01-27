const crypto = require('crypto');

// AES 密钥和偏移量（从 AESUtil.java 中获取）
const KEY = Buffer.from('smkldospdosldaaa', 'utf8');
const OFFSET = Buffer.from('0000000000000000', 'utf8');

function decryptAES(encryptedData) {
    try {
        // URL 解码
        const decoded = decodeURIComponent(encryptedData);

        // Base64 解码
        const encrypted = Buffer.from(decoded, 'base64');

        // AES 解密
        const decipher = crypto.createDecipheriv('aes-128-cbc', KEY, OFFSET);
        let decrypted = decipher.update(encrypted);
        decrypted = Buffer.concat([decrypted, decipher.final()]);

        return decrypted.toString('utf8');
    } catch (e) {
        console.error('解密失败:', e.message);
        return null;
    }
}

function main() {
    console.log('='.repeat(80));
    console.log('【对比测试】gol8 vs pt777 requestData 解密对比');
    console.log('='.repeat(80));
    console.log();

    // gol8.92friend.net:5656 的 requestData
    const gol8RequestData = "xMDluuAuUzRlpbKp1TCNyGZzHT9HhZWIJSRYW6JVVhyiraOBJYHbx3tdb3lq39cw3gXgPjxXKSMVQBh46e8gXl%2BUyS9jz8eImYGG%2BKk4l/TZOASuoQ2W0EM4euaPJuipdHi6XxkvX5gNqa/%2B2Fvth1RURPNpEP9ETT4um1gIqMU5CgsP28tAJh4N4ZxJqWZ7/9fEp1JbEogDn/qCDyBZ1n4vuNNk5v1cYbGP1bpa9t%2BZiG5/3xYiTXSrgNOvieFW9Mo4%2BFDeZUUAsrVR0W%2BtsnfhdQNCITEQ4/f23RyFjONL%2BClfCVPL8FU0K8CfV3URZagRWmYzgPSAY%2ByL8CgLk%2BQKTw%2Bj7x0kduoOgQC/W/C29G2jrlU4SVHa6aUpcL6DiBrEQIcyroKu7/r%2B2mWRwvlir5kmiuEz3gVY7FS9BU5/fc5HLT1gWdoRKAv8237ZX8OYLLW7JQa52BjZ18mke8M/ePdwmXtlxm2IElR9EMni5Kas9UNR9TsFOzAsFXpsVUjiM76zZD2fTYmrYwTJHmJQmHAOEkSDG8w/rphUBrlEJGWvVO9sHzfARWt7WKP9ohUajtVQDRYdRAwTRi12d7RC%2BANQGIQaSXZbLqSvc%2B/Ct7eh%2Bvl2tgD9fOm6tcRP4wmuArAsrufU3EQkfg5s0sJWtwe9tjP6rgZMJw2gyDn9/xRgYrhY33089j9uhZwfQn0W5rTXwUNgiNN1JZ1WQhK2SupIfxMh01r7Z1gGjt0%3D";

    // pt777aiguo.mypengyouquan.com 的 requestData
    const pt777RequestData = "iTr578jJwj5dkYOcffTUZpuUYDlyAPg9QD3Vr3f0caY/CdmvzJtWc8IGGkaW8YZPByo8pgRf4yNPba7/1Gzh%2Bt8cSFOwyUaE9kct0ObWgLJHiTwjRGT1kQ1RoxxjdgAWCUFHtHMW8rwvgcpaTkJN7HwOw6ApeHRT9g7ij96doDKpZXuhc1XmQnOk/0ZKrdfhG0wZckuM6hgHYn/IP5AUBdRhmTDQ/U0CCplUvIKayt8oNQaN1SPTQVYX9%2BKIQFUD08IC9bAI8vM7jXS0kmKrVPQGWQE7GBP0OoeU%2BfbPl9Y%2B4TEs4o7aG6jh%2Bd98yTAtCCX%2BHGOmc/sMBa0ERzKABpPTAXBhv2zFC1neTJ5jlWLq1nZu%2BqfD34g7b2AZKkuBjRGCLzd%2BRjXtTUCTGYZqvRuQtmNZbfD/%2BBuRgkMR8HaxtKjAbwFH3pxQUH/qjiLWWsdu76Jz6oSQbYF4dbqdi/W1CsISBUJVpBfMbAv9fvwbmY6jKRgGu4rGAyQI8WvatP7Mr8LQLRak/itxf0N0wStGG0hV1/IRolJ9rNIYExibfwDLmSTGwXdx5KB0dY5NCd66cn5JBH2mjuViDKsG7hZ/RnIC4Loqq/668EUO4rH/RfNWVYXvrz/8FcmJrjTX3iwcmqN3nittczuFOUfDUV7triYlVL/tZYmOTxPxBPxExcoGzqK0hPJ%2BQeIK1p7q9WkoBpUCqBMzQaHr1Nx7v3wjZ4qI9b27AohH9A8DHfE%3D";

    // 解密 gol8
    console.log('【1. GOL8 请求数据】');
    console.log('域名: gol8.92friend.net:5656');
    console.log('-'.repeat(80));

    const gol8Decrypted = decryptAES(gol8RequestData);
    if (gol8Decrypted) {
        console.log('解密后的 JSON:');
        console.log(gol8Decrypted);
        console.log();
        try {
            const gol8Json = JSON.parse(gol8Decrypted);
            console.log('格式化后的 JSON:');
            console.log(JSON.stringify(gol8Json, null, 2));
        } catch (e) {
            console.log('JSON 解析失败');
        }
    } else {
        console.log('解密失败！');
    }

    console.log();
    console.log('='.repeat(80));
    console.log();

    // 解密 pt777
    console.log('【2. PT777 请求数据】');
    console.log('域名: pt777aiguo.mypengyouquan.com');
    console.log('-'.repeat(80));

    const pt777Decrypted = decryptAES(pt777RequestData);
    if (pt777Decrypted) {
        console.log('解密后的 JSON:');
        console.log(pt777Decrypted);
        console.log();
        try {
            const pt777Json = JSON.parse(pt777Decrypted);
            console.log('格式化后的 JSON:');
            console.log(JSON.stringify(pt777Json, null, 2));
        } catch (e) {
            console.log('JSON 解析失败');
        }
    } else {
        console.log('解密失败！');
    }

    console.log();
    console.log('='.repeat(80));
    console.log();

    // 对比差异
    if (gol8Decrypted && pt777Decrypted) {
        console.log('【3. 差异对比】');
        console.log('='.repeat(80));

        try {
            const gol8Json = JSON.parse(gol8Decrypted);
            const pt777Json = JSON.parse(pt777Decrypted);

            // 对比 sid
            console.log('\n【sid 对比】');
            const gol8Sid = gol8Json.sid || 'null';
            const pt777Sid = pt777Json.sid || 'null';
            console.log(`  gol8:  ${gol8Sid}`);
            console.log(`  pt777: ${pt777Sid}`);
            console.log(`  是否相同: ${gol8Sid === pt777Sid}`);

            // 对比 product
            console.log('\n【product 对比】');
            const gol8Product = gol8Json.product || 'null';
            const pt777Product = pt777Json.product || 'null';
            console.log(`  gol8:  ${gol8Product}`);
            console.log(`  pt777: ${pt777Product}`);
            console.log(`  是否相同: ${gol8Product === pt777Product}`);

            // 对比 data 字段
            console.log('\n【data 字段对比】');
            const gol8Data = gol8Json.data || {};
            const pt777Data = pt777Json.data || {};

            console.log('\n  gol8 data 字段:');
            for (const [key, value] of Object.entries(gol8Data)) {
                console.log(`    ${key}: ${value}`);
            }

            console.log('\n  pt777 data 字段:');
            for (const [key, value] of Object.entries(pt777Data)) {
                console.log(`    ${key}: ${value}`);
            }

            // 找出差异
            console.log('\n【字段差异】');
            const allKeys = new Set([...Object.keys(gol8Data), ...Object.keys(pt777Data)]);
            let hasDiff = false;
            for (const key of Array.from(allKeys).sort()) {
                const gol8Value = gol8Data[key] !== undefined ? gol8Data[key] : '【不存在】';
                const pt777Value = pt777Data[key] !== undefined ? pt777Data[key] : '【不存在】';
                if (gol8Value !== pt777Value) {
                    hasDiff = true;
                    console.log(`  ${key}:`);
                    console.log(`    gol8:  ${gol8Value}`);
                    console.log(`    pt777: ${pt777Value}`);
                }
            }

            if (!hasDiff) {
                console.log('  ✓ 所有字段值相同');
            }

        } catch (e) {
            console.log(`对比失败: ${e.message}`);
        }
    }

    console.log();
    console.log('='.repeat(80));
    console.log('✓ 解密对比完成！');
}

main();
