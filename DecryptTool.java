import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;
import java.net.URLDecoder;

public class DecryptTool {

    private static final String KEY = "smkldospdosldaaa";
    private static final String OFFSET = "0000000000000000";

    public static String decrypt(String src) {
        try {
            // URL 解码
            String decoded = URLDecoder.decode(src, "UTF-8");

            // AES 解密
            Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
            byte[] raw = KEY.getBytes("ASCII");
            SecretKeySpec skeySpec = new SecretKeySpec(raw, "AES");
            IvParameterSpec iv = new IvParameterSpec(OFFSET.getBytes());
            cipher.init(Cipher.DECRYPT_MODE, skeySpec, iv);

            byte[] encrypted1 = Base64.getDecoder().decode(decoded);
            byte[] original = cipher.doFinal(encrypted1);

            return new String(original, "utf-8");
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public static void main(String[] args) {
        System.out.println("================================================================================");
        System.out.println("【requestData 解密对比】");
        System.out.println("================================================================================");
        System.out.println();

        // gol8.92friend.net:5656 的 requestData
        String gol8RequestData = "xMDluuAuUzRlpbKp1TCNyGZzHT9HhZWIJSRYW6JVVhyiraOBJYHbx3tdb3lq39cw3gXgPjxXKSMVQBh46e8gXl%2BUyS9jz8eImYGG%2BKk4l/TZOASuoQ2W0EM4euaPJuipdHi6XxkvX5gNqa/%2B2Fvth1RURPNpEP9ETT4um1gIqMU5CgsP28tAJh4N4ZxJqWZ7/9fEp1JbEogDn/qCDyBZ1n4vuNNk5v1cYbGP1bpa9t%2BZiG5/3xYiTXSrgNOvieFW9Mo4%2BFDeZUUAsrVR0W%2BtsnfhdQNCITEQ4/f23RyFjONL%2BClfCVPL8FU0K8CfV3URZagRWmYzgPSAY%2ByL8CgLk%2BQKTw%2Bj7x0kduoOgQC/W/C29G2jrlU4SVHa6aUpcL6DiBrEQIcyroKu7/r%2B2mWRwvlir5kmiuEz3gVY7FS9BU5/fc5HLT1gWdoRKAv8237ZX8OYLLW7JQa52BjZ18mke8M/ePdwmXtlxm2IElR9EMni5Kas9UNR9TsFOzAsFXpsVUjiM76zZD2fTYmrYwTJHmJQmHAOEkSDG8w/rphUBrlEJGWvVO9sHzfARWt7WKP9ohUajtVQDRYdRAwTRi12d7RC%2BANQGIQaSXZbLqSvc%2B/Ct7eh%2Bvl2tgD9fOm6tcRP4wmuArAsrufU3EQkfg5s0sJWtwe9tjP6rgZMJw2gyDn9/xRgYrhY33089j9uhZwfQn0W5rTXwUNgiNN1JZ1WQhK2SupIfxMh01r7Z1gGjt0%3D";

        // pt777aiguo.mypengyouquan.com 的 requestData
        String pt777RequestData = "iTr578jJwj5dkYOcffTUZpuUYDlyAPg9QD3Vr3f0caY/CdmvzJtWc8IGGkaW8YZPByo8pgRf4yNPba7/1Gzh%2Bt8cSFOwyUaE9kct0ObWgLJHiTwjRGT1kQ1RoxxjdgAWCUFHtHMW8rwvgcpaTkJN7HwOw6ApeHRT9g7ij96doDKpZXuhc1XmQnOk/0ZKrdfhG0wZckuM6hgHYn/IP5AUBdRhmTDQ/U0CCplUvIKayt8oNQaN1SPTQVYX9%2BKIQFUD08IC9bAI8vM7jXS0kmKrVPQGWQE7GBP0OoeU%2BfbPl9Y%2B4TEs4o7aG6jh%2Bd98yTAtCCX%2BHGOmc/sMBa0ERzKABpPTAXBhv2zFC1neTJ5jlWLq1nZu%2BqfD34g7b2AZKkuBjRGCLzd%2BRjXtTUCTGYZqvRuQtmNZbfD/%2BBuRgkMR8HaxtKjAbwFH3pxQUH/qjiLWWsdu76Jz6oSQbYF4dbqdi/W1CsISBUJVpBfMbAv9fvwbmY6jKRgGu4rGAyQI8WvatP7Mr8LQLRak/itxf0N0wStGG0hV1/IRolJ9rNIYExibfwDLmSTGwXdx5KB0dY5NCd66cn5JBH2mjuViDKsG7hZ/RnIC4Loqq/668EUO4rH/RfNWVYXvrz/8FcmJrjTX3iwcmqN3nittczuFOUfDUV7triYlVL/tZYmOTxPxBPxExcoGzqK0hPJ%2BQeIK1p7q9WkoBpUCqBMzQaHr1Nx7v3wjZ4qI9b27AohH9A8DHfE%3D";

        System.out.println("【1. GOL8 的 requestData 解密】");
        System.out.println("域名: gol8.92friend.net:5656");
        System.out.println("--------------------------------------------------------------------------------");
        String gol8Decrypted = decrypt(gol8RequestData);
        if (gol8Decrypted != null) {
            System.out.println(gol8Decrypted);
        } else {
            System.out.println("解密失败！");
        }

        System.out.println();
        System.out.println("================================================================================");
        System.out.println();

        System.out.println("【2. PT777 的 requestData 解密】");
        System.out.println("域名: pt777aiguo.mypengyouquan.com");
        System.out.println("--------------------------------------------------------------------------------");
        String pt777Decrypted = decrypt(pt777RequestData);
        if (pt777Decrypted != null) {
            System.out.println(pt777Decrypted);
        } else {
            System.out.println("解密失败！");
        }

        System.out.println();
        System.out.println("================================================================================");
        System.out.println("✓ 解密完成！请对比上面两个 JSON 的差异");
        System.out.println("================================================================================");
    }
}
