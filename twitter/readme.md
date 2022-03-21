# Twitter Spider

## 目的
抓取 Twitter 的用户，支持输入批量关键字搜索，抓取每一个用户的所有动态信息

## 破解思路

1. 从最终的获取所有用户的所有动态接口入手，重放接口，测试该接口必须哪些参数。
   - authorization
   - guest_token
   - user_id

2. 分析所有抓到的数据包

3. 列表页翻页分析

翻页分析
```json
{
  "userId": "1324626960434147328",
  "count": 40,
  "cursor": "HBaAgLOh16D1vCkAAA==",
  "includePromotedContent": true,
  "withQuickPromoteEligibilityTweetFields": true,
  "withSuperFollowsUserFields": true,
  "withDownvotePerspective": false,
  "withReactionsMetadata": false,
  "withReactionsPerspective": false,
  "withSuperFollowsTweetFields": true,
  "withVoice": true,
  "withV2Timeline": true,
  "__fs_dont_mention_me_view_api_enabled": false,
  "__fs_interactive_text_enabled": true,
  "__fs_responsive_web_uc_gql_enabled": false
 }
```
翻页的关键是在于上一页一定存在下一页的 cursor 值（正则提取）
Twitter 将返回的列表翻页数值放在了数据中，最后两个 entries 中分别存放了上一页和下一页 cursor 的 hash 值