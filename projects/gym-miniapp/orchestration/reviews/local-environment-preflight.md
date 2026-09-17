# 本地环境只读检查

Checked: 2026-09-16
Purpose: 为 CP0 提供现有环境证据，不代替技术选型和安全门禁。

- 目标 /Users/orderly_ray/Projects/gym-miniapp 不存在；未建项或写入源码。
- Node 路径 /Users/orderly_ray/.nvm/versions/node/v24.18.0/bin/node；执行版本 v24.18.0。
- 内置 node:sqlite 可加载，内存数据库 select sqlite_version() 返回 3.53.1；关闭成功。仅验证本机可用性，不证明事务/并发/生产部署适用性。
- Python /usr/bin/python3 版本 3.9.6。
- Git /usr/bin/git 版本 2.39.5 (Apple Git-154)。
- /Applications/wechatwebdevtools.app 存在，未打开工程或编译；Info.plist 的 CFBundleShortVersionString 返回36.6.0，此为应用包元数据，不能直接作为微信开发者工具产品版本或基础库版本证据。

没有安装依赖、创建数据库文件、下载第三方代码、读取凭证或执行预览上传。CP0仍需核对实际开发工具版本、基础库、账号能力、所选运行时/数据库文档与测试方式，并遵守本项目安全门禁。
