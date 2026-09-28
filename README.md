# Pi Agent 学习项目

按章节保存 Pi SDK 的练习代码。项目使用 Node.js、TypeScript 和 `@earendil-works/pi-coding-agent`。

## 运行

先安装依赖，并通过 Pi 的 `/login` 配置自己的模型账号或 API Key。凭据保存在本机，不要提交到仓库。

```powershell
npm install
npx tsx L01-env/01-hello.ts
npx tsx L04-prompt/04a-replace-prompt.ts
```

`L04-prompt/04a-replace-prompt.ts` 用 `systemPromptOverride` 替换默认编程助手人设，并清空追加规则。要改成自己的智能体，修改这个文件中 `systemPromptOverride` 返回的文字即可。
