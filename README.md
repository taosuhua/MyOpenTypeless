<p align="center">
  <strong>中文</strong> | <a href="README_EN.md">English</a> | <a href="README_ja.md">日本語</a> | <a href="README_ko.md">한국어</a>
</p>

<p align="center">
  <img src="src-tauri/icons/128x128@2x.png" width="128" height="128" alt="OpenTypeless Logo" />
</p>

<h1 align="center">OpenTypeless</h1>

<p align="center">
  开源桌面端 AI 语音输入工具。自然说话，在任意应用中获得润色后的文本。
</p>

<p align="center">
  无论你在写邮件、写代码、聊天还是做笔记 — 只需按下热键，<br/>
  说出你的想法，OpenTypeless 会用 AI 转录并润色你的语音，<br/>
  然后直接输入到你正在使用的任何应用中。
</p>

---

## 安装与配置指南

### 方式一：使用本地 Whisper（推荐，免费且隐私）

本方式使用本地 GPU 加速的 Whisper 模型，无需 API 密钥，完全免费，且语音数据不会上传到任何服务器。

#### 1. 安装 Python

从 [Python 官网](https://www.python.org/downloads/) 下载 Python 3.11 或更高版本。

安装时**务必勾选** "Add Python to PATH"。

#### 2. 安装 faster-whisper-server

打开命令提示符或 PowerShell，运行：

```bash
pip install faster-whisper-server
```

#### 3. 安装 Qwen3-ASR（可选，另一个本地模型）

Qwen3-ASR 是阿里巴巴开发的语音识别模型，转录速度更快：

```bash
pip install qwen-asr
```

模型会在首次使用时自动下载（约 4.7GB）。

#### 4. 安装 CUDA（可选，用于 GPU 加速）

如果你有 NVIDIA 显卡，安装 CUDA Toolkit 可大幅提升转录速度：

- 从 [NVIDIA CUDA Downloads](https://developer.nvidia.com/cuda-downloads) 下载 CUDA 12.x 版本
- 安装到默认位置即可

**注意**：GTX 1660 Ti 及以上显卡支持 CUDA。若无显卡或不安装 CUDA，程序会自动使用 CPU 模式（速度较慢）。

#### 5. 安装 OpenTypeless

下载并运行安装包：
- Windows: `OpenTypeless_0.1.0_x64-setup.exe`（NSIS 安装包）
- 或 `OpenTypeless_0.1.0_x64_en-US.msi`

#### 6. 配置本地语音识别

打开 OpenTypeless，进入设置：

1. **语音识别（STT）设置**：
   - 选择 `Local Whisper (本地)` 或 `Local Qwen3-ASR (本地)`
   - 无需填写 API 密钥

**两个本地模型的对比**：

| 模型 | 显存占用 | 转录速度 | 中文效果 |
|------|----------|----------|----------|
| Local Whisper (medium) | ~2GB | ~1.9秒 | 良好 |
| Local Qwen3-ASR (1.7B) | ~4GB | ~0.9秒 | 优秀 |

**注意**：由于显存限制，GTX 1660 Ti（6GB）只能同时运行一个本地模型。如果需要切换，请关闭另一个服务。

2. **AI 润色（LLM）设置**：
   - 选择任意 LLM 服务商（如 OpenRouter、DeepSeek 等）
   - 输入对应的 API 密钥
   - 或选择 `OpenTypeless Cloud` 使用云端服务

3. **通用设置**：
   - 设置热键（默认 `Ctrl+/`）
   - 选择输出模式：键盘模拟或剪贴板

#### 7. 开始使用

- 按下热键开始录音
- 说话（支持中英文混合）
- 松开热键，等待转录和润色
- 文本自动输入到当前应用

---

### 方式二：使用云端 STT 服务

如果不想本地部署，可选择以下云端语音识别服务商：

| 服务商 | 特点 | 获取 API 密钥 |
|--------|------|---------------|
| Groq Whisper | 免费，速度快 | [Groq Console](https://console.groq.com/) |
| GLM-ASR（智谱） | 中文效果好 | [智谱开放平台](https://open.bigmodel.cn/) |
| Deepgram | 高准确率 | [Deepgram](https://console.deepgram.com/) |
| SiliconFlow（硅基流动） | 国内访问快 | [SiliconFlow](https://cloud.siliconflow.cn/) |
| OpenAI Whisper | 稳定可靠 | [OpenAI](https://platform.openai.com/) |

配置方法：在设置中选择对应服务商，输入 API 密钥即可。

---

### AI 润色服务商选择

| 服务商 | 推荐模型 | 特点 | 获取 API 密钥 |
|--------|----------|------|---------------|
| OpenRouter | `google/gemini-2.5-flash` | 免费，速度快 | [OpenRouter](https://openrouter.ai/) |
| DeepSeek | `deepseek-chat` | 中文效果好，便宜 | [DeepSeek](https://platform.deepseek.com/) |
| 智谱（Zhipu） | `glm-4-flash` | 中文效果好 | [智谱开放平台](https://open.bigmodel.cn/) |
| OpenAI | `gpt-4o-mini` | 稳定可靠 | [OpenAI](https://platform.openai.com/) |

---

## 功能特性

- 🎙️ 全局热键录音，支持按住和切换两种模式
- 💊 浮动胶囊悬浮窗，随时可见录音状态
- 🗣️ 多种语音识别服务商：本地 Whisper、Groq、智谱、Deepgram 等
- 🤖 多种大模型润色文本：DeepSeek、智谱、OpenAI、Gemini 等
- ⚡ 流式输出，边生成边打字
- ⌨️ 支持键盘模拟和剪贴板两种输出方式
- 🌐 翻译模式：说中文，输出英文（或其他语言）
- 📖 自定义词典，提升专业术语识别率
- 🔍 自动识别当前应用，适配不同场景
- 📜 本地历史记录，支持全文搜索
- 🌗 深色 / 浅色 / 跟随系统主题
- 🚀 开机自启

---

## 常见问题

### 为什么输出是繁体中文？

请确保在设置中选择了"简体中文"作为目标语言。如果仍有问题，请检查 LLM 服务商的模型是否正确配置。

### 转录速度慢怎么办？

1. 确保已安装 CUDA 并正确配置
2. 检查 GPU 是否被正确使用（任务管理器中查看 GPU 使用率）
3. 如果使用 CPU，转录速度会较慢（约 5-7 秒）
4. GPU 加速下，转录速度约 1-2 秒

### 在新电脑上如何部署？

1. 安装 Python 3.11+（勾选 "Add Python to PATH")
2. `pip install faster-whisper-server`
3. 安装 CUDA（可选，用于 GPU 加速）
4. 安装 OpenTypeless

程序会自动检测 Python 和 CUDA 路径，无需手动配置。

### 可以完全离线使用吗？

可以。使用本地 Whisper + 本地 LLM（如 Ollama），程序可完全离线运行。

---

## 从源码构建

```bash
# 安装依赖
npm install

# 开发模式运行
npm run tauri dev

# 构建生产版本
npm run tauri build
```

构建产物位于 `src-tauri/target/release/bundle/`。

---

## 许可证

[MIT](LICENSE)