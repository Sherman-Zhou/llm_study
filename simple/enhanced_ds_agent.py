from simple_ds_agent import DeepSeekAPIAgent
class EnhancedDeepSeekAgent(DeepSeekAPIAgent):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.local_commands = {
            "帮助": self._show_help,
            "清空历史": self.reset_conversation,
            "时间": self._get_current_time
        }
    
    def _show_help(self) -> str:
        """显示帮助信息"""
        help_text = """我可以帮你做以下事情:
- 普通聊天对话
- 特殊命令:
  * 帮助: 显示此帮助信息
  * 清空历史: 重置对话
  * 时间: 显示当前时间
其他问题我会调用 DeepSeek API 来回答"""
        return help_text
    
    def _get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return f"当前时间是: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    def chat(self, user_input: str) -> str:
        """
        增强版对话处理
        """
        # 检查是否是本地命令
        command = user_input.strip().lower()
        for cmd in self.local_commands:
            if cmd in command:
                return self.local_commands[cmd]()
        
        # 不是本地命令则调用API
        return super().chat(user_input)

# 使用增强版Agent
if __name__ == "__main__":
    # 替换为你的实际API密钥
    API_KEY = "your_api_key_here"
    
    agent = EnhancedDeepSeekAgent(API_KEY)
    
    print("增强版 DeepSeek Agent 已启动，输入'帮助'查看可用命令\n")
    
    while True:
        user_input = input("你: ")
        
        if user_input.lower() in ["退出", "exit", "quit", "bye", "再见"]:
            print("助手: 再见！")
            break
            
        response = agent.chat(user_input)
        print("助手:", response)