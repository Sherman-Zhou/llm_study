from enhanced_ds_agent import EnhancedDeepSeekAgent
class MemoryDeepSeekAgent(EnhancedDeepSeekAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.memory = {}
        self.local_commands.update({
            "记住": self._remember_info,
            "我知道": self._recall_info
        })
    
    def _remember_info(self) -> str:
        """记住用户提供的信息"""
        parts = self.conversation_history[-1]["content"].split("记住", 1)
        if len(parts) > 1:
            info = parts[1].split("是", 1)
            if len(info) == 2:
                key = info[0].strip()
                value = info[1].strip()
                self.memory[key] = value
                return f"好的，我已经记住 {key} 是 {value}"
        return "请使用'记住[什么]是[内容]'的格式"
    
    def _recall_info(self) -> str:
        """回忆记住的信息"""
        parts = self.conversation_history[-1]["content"].split("我知道", 1)
        if len(parts) > 1:
            key = parts[1].strip()
            if key in self.memory:
                return f"你之前告诉我 {key} 是 {self.memory[key]}"
            return f"我不知道 {key} 的信息"
        return "请使用'我知道[什么]'的格式"
    
    def chat(self, user_input: str) -> str:
        # 添加到对话历史
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # 检查是否是本地命令
        command = user_input.strip().lower()
        for cmd in self.local_commands:
            if cmd in command:
                response = self.local_commands[cmd]()
                self.conversation_history.append({"role": "assistant", "content": response})
                return response
        
        # 检查是否有记忆可以添加到上下文
        context = self._add_memory_to_context(user_input)
        
        # 调用API
        response = self._call_api(context)
        
        # 添加助手回复到对话历史
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def _add_memory_to_context(self, user_input: str) -> List[Dict]:
        """将相关记忆添加到上下文中"""
        context = self.conversation_history.copy()
        
        # 简单查找相关记忆
        for key, value in self.memory.items():
            if key.lower() in user_input.lower():
                context.insert(-1, {
                    "role": "system",
                    "content": f"用户之前告诉你: {key} 是 {value}"
                })
        
        return context

# 使用记忆版Agent
if __name__ == "__main__":
    # 替换为你的实际API密钥
    API_KEY = "your_api_key_here"
    
    agent = MemoryDeepSeekAgent(API_KEY)
    
    print("记忆版 DeepSeek Agent 已启动，输入'帮助'查看可用命令\n")
    
    while True:
        user_input = input("你: ")
        
        if user_input.lower() in ["退出", "exit", "quit", "bye", "再见"]:
            print("助手: 再见！")
            break
            
        response = agent.chat(user_input)
        print("助手:", response)