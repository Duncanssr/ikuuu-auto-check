# GitHub Secrets 变量配置完整教程（含表格说明）
本教程将通过表格清晰展示所有需配置的变量，配合步骤指引，帮助你快速完成敏感信息的安全存储，确保自动签到脚本和清理脚本正常运行。


## 一、前置准备
1. 已创建 GitHub 仓库（如 `ikuuu-auto-check`），并上传了自动签到脚本（`ikuuu_checkin.py`）和工作流配置文件。
2. 准备好以下信息：
   - ikuuu 账号邮箱+密码（如 `lijboy@outlook.com,qwer1234`）；
   - Telegram 机器人令牌（可选，用于接收签到通知）；
   - Telegram 聊天 ID（可选，用于接收签到通知）。


## 二、需配置的变量总览（表格版）
| 变量名称（Name）       | 变量用途                  | 填写格式/示例                          | 是否必选 | 注意事项                                  |
|------------------------|---------------------------|----------------------------------------|----------|-------------------------------------------|
| `ACCOUNTS`             | 存储 ikuuu 账号密码       | 邮箱1,密码1;邮箱2,密码2;邮箱3,密码3    | 是       | 英文逗号分隔邮箱和密码，英文分号分隔多账号 |
| `TELEGRAM_BOT_TOKEN`   | Telegram 机器人身份标识   | 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11 | 否       | 从 `@BotFather` 处获取，格式固定           |
| `TELEGRAM_CHAT_ID`     | 接收通知的 Telegram 聊天ID | 123456789（纯数字）                    | 否       | 从 `@getidsbot` 处获取，无特殊符号        |


## 三、Step 1：进入 GitHub Secrets 配置页
1. 打开你的 GitHub 仓库（示例链接：`https://github.com/Duncanssr/ikuuu-auto-check`）。
2. 点击仓库顶部导航栏的 **Settings**（设置），进入仓库配置页。
3. 在左侧菜单栏中，找到并展开 **Secrets and variables**（密钥和变量），点击子选项 **Actions**，进入工作流专用的 Secrets 配置页。  
   ![进入Secrets页面示意图](https://picsum.photos/id/180/800/400?alt=GitHub仓库设置中Secrets位置)


## 四、Step 2：按表格配置变量（逐个添加）
所有变量均通过 **“新建密钥”** 功能添加，操作逻辑一致，以下按“必选→可选”顺序说明：

### 1. 配置必选变量：`ACCOUNTS`（ikuuu账号密码）
1. 在 Secrets 页面，点击右上角 **New repository secret**（新建仓库密钥）。
2. 按表格要求填写：
   - **Name**：严格填写 `ACCOUNTS`（区分大小写，错写脚本无法读取）；
   - **Secret**：按格式填入账号密码，示例（对应你的账号）：  
     `lijboy@outlook.com,qwer1234;lijboy+cs@outlook.com,qwer1234;MarcelinoLueilwitz@outlook.com,qwer1234`。
3. 点击页面底部 **Add secret**（添加密钥），完成第一个变量配置。


### 2. 配置可选变量：`TELEGRAM_BOT_TOKEN`（Telegram机器人令牌）
1. 再次点击 **New repository secret**。
2. 按表格要求填写：
   - **Name**：严格填写 `TELEGRAM_BOT_TOKEN`；
   - **Secret**：粘贴从 `@BotFather` 获取的令牌（示例：`123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`）。
3. 点击 **Add secret** 保存。


### 3. 配置可选变量：`TELEGRAM_CHAT_ID`（Telegram聊天ID）
1. 再次点击 **New repository secret**。
2. 按表格要求填写：
   - **Name**：严格填写 `TELEGRAM_CHAT_ID`；
   - **Secret**：粘贴从 `@getidsbot` 获取的纯数字ID（示例：`123456789`）。
3. 点击 **Add secret** 保存。


## 五、Step 3：验证变量配置
1. 回到 Secrets 列表页，确认已添加的变量与下表一致：
   | 已添加变量名称         | 状态验证                          |
   |------------------------|-----------------------------------|
   | `ACCOUNTS`             | 显示为 `***`（内容隐藏，正常）    |
   | `TELEGRAM_BOT_TOKEN`   | （若配置）显示为 `***`            |
   | `TELEGRAM_CHAT_ID`     | （若配置）显示为 `***`            |
2. 若需修改变量：点击对应变量名称，进入详情页后点击 **Update secret**，重新填写内容并保存。


## 六、常见问题排查（表格版）
| 问题现象                          | 可能原因                          | 解决方案                                  |
|-----------------------------------|-----------------------------------|-------------------------------------------|
| 脚本提示“未配置任何账号”          | `ACCOUNTS` 变量名称错写（如 `accounts`） | 确认变量名严格为 `ACCOUNTS`（区分大小写） |
| 多账号仅部分签到成功              | `ACCOUNTS` 格式错误（用中文逗号/分号） | 改为英文逗号（`,`）和英文分号（`;`）      |
| 收不到 Telegram 通知              | 机器人令牌/聊天ID填写错误          | 重新从 `@BotFather`/`@getidsbot` 获取并更新 |
| 清理脚本报403错误                 | 变量未配置或权限不足              | 无需额外变量，确保清理脚本中包含 `permissions: {actions: write, contents: read}` |


通过以上步骤，你已完成所有敏感变量的安全配置，脚本将自动读取这些变量运行，无需担心信息泄露。后续添加/修改账号时，只需更新 `ACCOUNTS` 变量即可，无需修改代码。
