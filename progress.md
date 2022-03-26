## 外媒记者信息 爬取进度

### 一、外媒记者信息爬取情况

|  媒体  | 记者列表 | 头像  | 个人详情 | 邮箱  | twitter账号 | twitter推文 | Facebook账号 | 领英账号 |  
|:----:|:----:|:---:|:----:|:---:|:---------:|:---------:|:----------:|:----:|
| KBS  |  有   |  有  |  有   |  有  |    部分     |     有     |     部分     |  -   |
| 朝日新闻 |  有   |  -  |  有   |  -  |     有     |     有     |     -      |  -   |
| voa  |  有   |  有  |  有   |  有  |     -     |     有     |     -      |  -   |
| 读卖新闻 |  有   |  -  |  -   |  -  |     -     |     -     |     -      |  -   |
| CNN  |  有   |  有  |  有   |  -  |    部分     |     有     |     部分     |  -   |
| 路透社  |  有   |  有  |  有   |  有  |     有     |     有     |     有      |  -有  |

1. 记者列表是该网站内所有记者信息的汇总文件，包含记者姓名、职位、公司、头像、社交账号等。

### 二、新闻爬取情况

| 媒体  | 新闻列表 | PDF |  翻译 |
|-----|-----|-----|----|
| kbs |    有 | 有   |  部分 |
| 朝日  |    有 | 有   |   - |
| voa |    有 | 有   |   - |
| 读卖  |    有 | -   |   - |
| 路透社 |    有 | 有   |   - |

1. 新闻列表包括，标题、内容、记者、发布时间、url等信息。
2. PDF为新闻所在页html转换为PDF
3. 翻译功能针对新闻内容进行翻译

### 三、自动化实现情况

|            功能点            | 能否自动化 |
|:-------------------------:|:-----:|
|           文章爬取            |   是   |
|          记者列表爬取           |   是   |
|           文章翻译            |  部分   |
| RocketReach.com<br>需要付费账号 |   是   |
|  Twitter.com<br>个人主页、推文   |   是   |
|       FaceBook.com        |   否   |
|       LinkedIn.com        |   否   |

### 四、24家新闻机构摸排情况

<table>
    <tr>
        <td>媒体</td>
        <td>文章包含<br>记者姓名</td>
        <td>全体记者页面</td>
        <td>个人详情页面</td>
        <td>个人社交账号</td>
        <td>收费</td>
        <td>外协</td>
    <tr>
    <tr>
        <td colspan="8" align="center">已爬取</td>
    <tr>
    <tr>
        <td>KBS</td>
        <td>√</td>
        <td>无</td>
        <td>无</td>
        <td>无</td>
        <td>否</td>
        <td>否</td>
    <tr>
    <tr>
        <td>读卖</td>
        <td>无</td>
        <td>无</td>
        <td>无</td>
        <td>无</td>
        <td>否</td>
        <td>否</td>
    <tr><tr>
        <td>朝日</td>
        <td>√</td>
        <td>√</td>
        <td>无</td>
        <td>无</td>
        <td>是</td>
        <td>是</td>
    <tr><tr>
        <td>VOA</td>
        <td>√</td>
        <td>无</td>
        <td>√</td>
        <td>无</td>
        <td>否</td>
        <td>否</td>
    <tr><tr>
        <td>CNN</td>
        <td>√</td>
        <td>√</td>
        <td>√</td>
        <td>√</td>
        <td>否</td>
        <td>否</td>
    <tr><tr>
        <td>路透社</td>
        <td>√</td>
        <td>√</td>
        <td>√</td>
        <td>√</td>
        <td>否</td>
        <td>否</td>
    <tr><tr>
        <td>韩联社</td>
        <td>√</td>
        <td>无</td>
        <td>无</td>
        <td>√</td>
        <td>否</td>
        <td>否</td>
    <tr><tr>
        <td>美国合众国际社</td>
        <td>√</td>
        <td>无</td>
        <td>√</td>
        <td>无</td>
        <td>否</td>
        <td>否</td>
    <tr><tr>
        <td>NBC</td>
        <td>√</td>
        <td>√</td>
        <td>√</td>
        <td>无</td>
        <td>否</td>
        <td>否</td>
    <tr><tr>
        <td colspan="7" align="center">外协</td>
    <tr><tr>
        <td>华尔街日报</td>
        <td>√</td>
        <td>√</td>
        <td>√</td>
        <td>√</td>
        <td>是</td>
        <td>是</td>
    <tr><tr>
        <td>华盛顿邮报</td>
        <td>√</td>
        <td>√</td>
        <td>√</td>
        <td>无</td>
        <td>是</td>
        <td>是</td>
    <tr><tr>
        <td>环球时报</td>
        <td>√</td>
        <td>无</td>
        <td>无</td>
        <td>无</td>
        <td>是</td>
        <td>是</td>
    <tr><tr>
        <td>德国明镜周刊</td>
        <td>√</td>
        <td>√</td>
        <td>无</td>
        <td>√</td>
        <td>是</td>
        <td>是</td>
    <tr><tr>
        <td>时代周刊</td>
        <td>√</td>
        <td>无</td>
        <td>√</td>
        <td>√</td>
        <td>是</td>
        <td>是</td>
    <tr><tr>
        <td>泰晤士报</td>
        <td>√</td>
        <td>无</td>
        <td>√</td>
        <td>√</td>
        <td>是</td>
        <td>是</td>
    <tr><tr>
        <td>彭博社</td>
        <td>√</td>
        <td>无</td>
        <td>√</td>
        <td>√</td>
        <td>是</td>
        <td>是</td>
    <tr><tr>
        <td colspan="7" align="center"></td>
    <tr>    <tr>
        <td>媒体</td>
        <td>文章包含<br>记者姓名</td>
        <td>全体记者页面</td>
        <td>个人详情页面</td>
        <td>个人社交账号</td>
        <td>收费</td>
        <td>外协</td>
    <tr><tr>
        <td colspan="7" align="center">待爬取</td>
    <tr><tr>
        <td>全国公共广播电台NPR——li</td>
        <td>√</td>
        <td>无</td>
        <td>√</td>
        <td>√</td>
        <td>否</td>
        <td>否</td>
    <tr><tr>
        <td>美联社</td>
        <td>√</td>
        <td>无</td>
        <td>无</td>
        <td>无</td>
        <td>否</td>
        <td>否</td>
    <tr><tr>
        <td>日本广播协会</td>
        <td>无</td>
        <td>无</td>
        <td>无</td>
        <td>无</td>
        <td>否</td>
        <td>否</td>
    <tr><tr>
        <td>共同通讯社</td>
        <td>部分√</td>
        <td>无</td>
        <td>无</td>
        <td>无</td>
        <td>否</td>
        <td>否</td>
    <tr><tr>
        <td>新唐人电视台</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>否</td>
        <td>否</td>
    <tr><tr>
        <td>大纪元</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>否</td>
        <td>否</td>
    <tr><tr>
        <td>对华援助社</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
        <td>否</td>
        <td>否</td>
    <tr>
</table>