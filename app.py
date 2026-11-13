import streamlit as st
from openai import OpenAI

# 1. 设置网页的标题和图标（女仆特意挑了鲸鱼的图标哦）
st.set_page_config(page_title="AI 评论分析助手", page_icon="🐳")
st.title("🐳 AI 评论分析助手")
st.write("主人，请把评论粘贴到下面的框里，选好要求，剩下的交给我吧～")
# 让用户自己填入 Key，type="password" 会把字符变成小黑点，保护隐私
user_key = st.text_input("请输入您的 DeepSeek API Key（以 sk- 开头）：", type="password")


# 3. 网页上的下拉菜单（选择模板）0
template_options = {
    "默认详细总结": "请帮我总结以下评论的内容：\n1. 用一句话概括大家的总体态度。\n2. 列出大家夸赞的点和吐槽的点。\n3. 摘录一条最有意思的评论。",
    "极简三句话": "请用极其简短的三句话总结以下评论，不要废话。",
    "逻辑推理版": "请帮我分析以下评论，找出其中的逻辑关系和潜在的矛盾点，并给出总结。",
}
selected_template = st.selectbox("请选择总结的风格：", list(template_options.keys()))

# 4. 网页上的文本输入框（代替 comments.txt）
comments_input = st.text_area("请粘贴评论内容（重要提示：请在每一条完整评论之间空一行）：", height=200)

# 5. 网页上的按钮
if st.button("开始分析", type="primary"):
    if not comments_input.strip():
        st.warning("主人，您还没有输入评论哦！")
    elif not user_key.startswith("sk-"):
        st.warning("主人，请先在上方填入正确的 API Key 哦！")
    else:
        # 动态使用用户输入的 Key
        client = OpenAI(api_key=user_key, base_url="https://api.deepseek.com")
        
        with st.spinner('女仆正在努力连接 AI，请主人稍等片刻...'):
            # 组装 Prompt
            # 我们在评论前面加一句强指令，告诉 AI 怎么切分
            prompt = (
                    f"{template_options[selected_template]}\n\n"
                    "【请注意：以下评论以空行作为分隔符，一条完整评论内部可能包含换行，请结合上下文作为整体理解。】\n"
                    f"评论如下：\n{comments_input}"
                )
            try:
                # 发送给 AI
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": prompt}],
                    # 逻辑推理需要更严谨，温度设为 0.1
                    temperature=0.1 if selected_template == "逻辑推理版" else 0.3
                )
                
                # 获取结果并在网页上展示
                summary = response.choices[0].message.content
                st.success("分析完成啦！")
                st.markdown("### 📝 分析结果：")
                st.markdown(summary)
                
            except Exception as e:
                st.error(f"哎呀，出了点问题：{e}")