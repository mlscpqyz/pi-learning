import { createAgentSession, ModelRuntime } from "@earendil-works/pi-coding-agent";

// Read the models and credentials configured for Pi.
const modelRuntime = await ModelRuntime.create();
const model = (await modelRuntime.getAvailable())[0];

if (!model) {
  console.error("没有可用模型。请先在 Pi 中用 /login 配置账号或 API Key。");
  process.exit(1);
}

const { session } = await createAgentSession({ model, modelRuntime });

try {
  // Print each piece of text as the model generates it.
  session.subscribe((event) => {
  if (event.type === "message_update" &&
      event.assistantMessageEvent.type === "text_delta") {
    process.stdout.write(event.assistantMessageEvent.delta);
    return;
  }
  console.log(`📋 [${event.type}]`);
});

await session.prompt("当前目录有哪些文件？");

  console.log(`使用模型：${model.provider}/${model.id}\n`);
  await session.prompt("用一句话介绍你自己。");
  console.log();
} finally {
  session.dispose();
}
