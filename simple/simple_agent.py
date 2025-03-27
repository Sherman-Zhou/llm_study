class SimpleAgent:
    def __init__(self):
        # 简单的知识库
        self.knowledge_base = {
            "你好": "你好！我是你的智能助手。",
            "你是谁": "我是一个简单的Python智能助手。",
            "再见": "再见，祝你有个愉快的一天！",
            "计算": "我可以帮你做简单计算，请告诉我算式。",
            "默认": "我不太明白你的意思，能再说清楚些吗？"
        }
        
        # 对话历史
        self.conversation_history = []
    
    def respond(self, user_input):
        """处理用户输入并返回响应"""
        # 将用户输入添加到对话历史
        self.conversation_history.append(f"用户: {user_input}")
        
        # 简单的意图识别
        response = self._understand_input(user_input)
        
        # 将响应添加到对话历史
        self.conversation_history.append(f"助手: {response}")
        
        return response
    
    def _understand_input(self, text):
        """简单的意图理解"""
        text = text.lower().strip()
        
        # 检查问候
        if any(word in text for word in ["你好", "嗨", "hello", "hi"]):
            return self.knowledge_base["你好"]
        
        # 检查询问身份
        elif any(word in text for word in ["你是谁", "你叫什么"]):
            return self.knowledge_base["你是谁"]
        
        # 检查告别
        elif any(word in text for word in ["再见", "拜拜", "exit", "quit"]):
            return self.knowledge_base["再见"]
        
        # 检查计算请求
        elif "计算" in text or "算" in text:
            return self._handle_calculation(text)
        
        # 默认回复
        else:
            return self.knowledge_base["默认"]
    
    def _handle_calculation(self, text):
        """处理简单计算"""
        # 尝试提取数字和运算符
        try:
            # 简单的提取方法 - 实际应用需要更健壮的实现
            parts = text.split()
            for part in parts:
                if part.isdigit() or part in '+-*/':
                    # 非常简单的安全计算
                    if '+' in text:
                        nums = text.split('+')
                        result = int(nums[0]) + int(nums[1])
                    elif '-' in text:
                        nums = text.split('-')
                        result = int(nums[0]) - int(nums[1])
                    elif '*' in text:
                        nums = text.split('*')
                        result = int(nums[0]) * int(nums[1])
                    elif '/' in text:
                        nums = text.split('/')
                        result = int(nums[0]) / int(nums[1])
                    else:
                        return "请告诉我具体的计算式，比如'计算3+5'"
                    
                    return f"计算结果是: {result}"
        except:
            return "抱歉，我无法理解这个计算"
        
        return self.knowledge_base["计算"]

# 使用示例
if __name__ == "__main__":
    agent = SimpleAgent()
    
    print("简单对话Agent已启动，输入'退出'结束对话")
    
    while True:
        user_input = input("你: ")
        
        if user_input.lower() in ["退出", "exit", "quit", "bye", "再见"]:
            print(agent.respond(user_input))
            break
            
        response = agent.respond(user_input)
        print("助手:", response)