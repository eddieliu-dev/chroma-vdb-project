This repository is for a chroma vector database project:
1. Ollama平台搭建+OpenWebUI 构建私有平台
   https://github.com/ollama/ollama 
   选模型：hugging face-embedding模型（bge格式）
2. 实现chroma增删改查CRUD能力 复杂一些：读documents。。。
   ID（uuid），标题，标签，全文，创建人（随机字符串等），创建时间（随机生成）
   标题，标签：大模型prompt提取