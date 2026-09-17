# 微信登录原始来源复核

Checked: 2026-09-16
Reviewer: 小程序指挥者
Source: https://developers.weixin.qq.com/miniprogram/dev/server/API/user-login/api_code2session

网页读取工具失败、Firecrawl额度不足；使用 HTTPS 读取官方页面成功，并解析实际正文。

直接支持：wx.login 临时 code 交由开发者服务器调用 code2Session；请求包含 appid、secret、js_code、grant_type；响应包括 openid 和 session_key，UnionID 有条件返回。官方列出无效 code、风险拦截、频率限制等失败状态。

产品推断：此过程建立微信身份，未核查本店会员资格。因此本店会员绑定必须另有经授权的馆方核验，失败不能回退为假登录。此页不证明任何真实 AppID 已可用，也不证明本项目已完成真实登录测试。

此复核只支持研究中的微信身份分层；完整研究验收仍须读取 PM 最终证据与结果。
