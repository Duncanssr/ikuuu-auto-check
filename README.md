👌 明白啦，你是要我基于这个 **ikuuu 自动签到脚本**，写一个完整的 **README 使用教程**。

我帮你整理好一份标准的开源项目说明文档：

---

# 📌 ikuuu-auto-check

一个基于 **Python + GitHub Actions** 的自动签到工具，支持多账号，并可通过 Telegram Bot 发送签到结果通知。

---

## ✨ 功能特性

* [x] 支持多账号签到（用分号 `;` 分隔）
* [x] 自动登录并签到 ikuuu
* [x] 支持 Telegram 推送签到结果
* [x] 可通过 GitHub Actions 定时执行，无需服务器

---

## 📦 部署方式

### 1. Fork 本仓库

点击右上角 **Fork**，将本仓库复制到自己的 GitHub 账户下。

---

### 2. 配置 Secrets

进入你 Fork 后的仓库 → **Settings → Secrets and variables → Actions → New repository secret**，添加以下参数：

| 名称                   | 示例值                                                         | 说明                            |
| -------------------- | ----------------------------------------------------------- | ----------------------------- |
| `ACCOUNTS`           | `email1@example.com,password1;email2@example.com,password2` | 多账号用 `;` 分隔，账号密码之间用 `,` 分隔    |
| `TELEGRAM_BOT_TOKEN` | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`                 | （可选）你的 Telegram Bot Token     |
| `TELEGRAM_CHAT_ID`   | `123456789`                                                 | （可选）你的 Telegram 用户/群组 Chat ID |

📌 如果不配置 Telegram 参数，则只会在 GitHub Actions 日志中显示签到结果。

---

### 3. 启用 GitHub Actions

1. 进入仓库 → 点击 **Actions**
2. 找到 `ikuuu_checkin` 工作流
3. 点击 **Enable workflow**

---

### 4. 设置定时任务（可选）

项目默认可以手动运行，你也可以设置 **自动执行**。

编辑 `.github/workflows/ikuuu_checkin.yml`，添加一个 `schedule` 定时任务，例如每天北京时间早上 8 点运行：

```yaml
on:
  workflow_dispatch:
  schedule:
    - cron: "0 0 * * *"   # UTC 0点，对应北京时间 8点
```

---

## ▶️ 手动运行

进入仓库 → Actions → 选择 `ikuuu_checkin` → 点击 **Run workflow** 即可手动触发签到。

---

## 📜 日志查看

签到完成后，可以在 **Actions 日志** 或 Telegram Bot（如果配置了）中查看签到结果。

日志示例：

```
📅 执行时间: 2025-09-05 08:00:01
🌐 地址: https://ikuuu.org

📋 账号信息:
  账号 1: test@example.com
  密码 1: te****23

🎉 签到结果 🎉
  账号 1: ✅ 签到成功，获得 123MB 流量
```

---

## ⚠️ 注意事项

1. 账号密码不要带分号 `;` 或逗号 `,`，否则会解析错误。
2. 如果频繁失败，可能是因为 **IP 风控** 或 **账号异常**，建议手动登录一次确认。
3. GitHub Actions 有运行时长限制，请尽量不要配置过多账号。

---

## 🛠️ 技术栈

* Python 3
* requests
* GitHub Actions

---

你要不要我帮你顺便写一个 `.github/workflows/ikuuu_checkin.yml`，这样 README 里的步骤就是完整可跑的？
