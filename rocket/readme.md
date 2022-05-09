# 使用教程

## 1. 访问 http://101.35.230.198:5000/

#### （1） 选择 Run Spider

#### （2） 选择 Scrapyd serve 为 43.135.68.41:6800

#### （3） 选择 project 为 rocket

#### （4） 选择 _version 为 default: the latest version

#### （5） 选中 settings & arguments

- USER_AGENT  **Mozilla/5.0**
- ROBOTSTXT_OBEY **False**
- COOKIES_ENABLED **False**
- CONCURRENT_REQUESTS **5**
- DOWNLOAD_DELAY **1**

**设置 additional 参数如下，参数根据情况调整**

```text
-d setting=CLOSESPIDER_TIMEOUT=60
-d setting=CLOSESPIDER_PAGECOUNT=10
-d start=0
-d size=2
-d key=a4f232k9333d66b17f359eec8b1e4b89de31df6
-d query={"employer": ["state.gov"], "current_title": ["Secretary"]}
```

#### （6） 点击 Check CMD

#### （7） 点击运行

#### （8） 访问 http://43.135.68.41:8888/1895165

#### （9） 在【文件】 /data/ftp/csv 下获取数据爬取结果


