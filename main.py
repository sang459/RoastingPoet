import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import \
    ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI

st.set_page_config("RoastingPoet", layout="wide")

# 페이지 새로 로딩될때마다 바뀌는 변수들은 st.session_state["변수명"] 이런식으로 저장해줘야함
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []

# 유저인풋 받는 함수
def get_text():
    """
    Get the user input text.
    Returns:
        (str): The text entered by the user
    """
    input_text = st.text_input(
        "You: ",
        st.session_state["input"],
        key="input",
        placeholder="Type in and press enter",
        label_visibility="hidden",
    )
    return input_text

# 초기화(나도 이해 못함 아직)
def new_chat():
    """
    Clears session state and starts a new chat.
    """
    save = []
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state.entity_memory.store = {} 
    st.session_state.entity_memory.buffer.clear()

    # entity memory라는건  memory 중에서도 {'Sarah': '주인공, 여자, ...', 'Mr.Thompson': '집사, 수상한 움직임'} 
    # 이런 식으로 기억할 내용을 저장하는 방식. langchain의 기능임

# Set up the Streamlit app layout
st.title("💡 A Wise Robot Says...")

st.markdown(
        """ 
        ```
        Share your worries, your questions so dear,
        With a wise robot, who's always near.
        Type in your troubles, let them take flight,
        Press enter and watch, as wisdom ignites.
        ```
        
        """
    )

# API 키 입력받기
API_O = st.secrets["API_KEY"]


    # Large Language Model은 OpenAI 쓸거임
llm = ChatOpenAI(temperature=0.8, openai_api_key=API_O, model_name="gpt-3.5-turbo", verbose=False)

    # Create a ConversationEntityMemory object if not already created
if "entity_memory" not in st.session_state:
    st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=1)

    # Create the ConversationChain object with the specified configuration
Conversation = ConversationChain(
        llm=llm,
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=st.session_state.entity_memory,
    )


user_input = get_text()
if user_input:
    output = Conversation.run(input=user_input+" (INSTRUCTION: You are RoastingPoet. People ask you for advice, but they get roasted instead. Instead of just replying, I want you to brutally roast them in a poem. I mean BRUTALLY. And also put '\n' in front of capital letters.)")
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)


with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        st.success(st.session_state["generated"][i], icon="✒️")
        st.info(st.session_state["past"][i], icon="😭")

st.markdown(
    """ 
        > :black[*powered by -  [LangChain]('https://langchain.readthedocs.io/en/latest/modules/memory.html#memory') + 
        [OpenAI]('https://platform.openai.com/docs/models/gpt-3-5') + 
        [Streamlit]('https://streamlit.io') + [DataButton](https://www.databutton.io/)*]
        """
)