
import streamlit as st
from streamlit_extras.stylable_container import stylable_container 
import pandas as pd
import numpy as np
from MusicRecommend import find_similar_songs

# CSS 파일 경로
css_path1 = "/content/drive/MyDrive/style.css"
css_path2 = "/content/drive/MyDrive/normalize.css"

#노래 파일 경로
songs_data = pd.read_csv('/content/drive/MyDrive/total_melon_emotion.csv')

# CSS 파일을 읽어오는 함수
def load_css(file_path):
    with open(file_path, 'r') as file:
        css_content = file.read()
    return css_content

# CSS 파일 내용을 읽어옴
css_content1 = load_css(css_path1)
css_content2 = load_css(css_path2)

st.markdown(
    f"<style>{css_content1}{css_content2}</style>",
    unsafe_allow_html=True
)

def Header():
    with stylable_container(
        key="logo",
        css_styles="""
            {
                line-height:60px;
                height: 60px !important;

                position: relative;
                border-bottom: 1px solid #555152 !important;

                flex-direction:row !important;
                justify-content: space-between !important;
                align-items: center !important;

            }
            .element-container st-emotion-cache-engr8z div > div > div {
                width: 50%;
            }
            div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.logo) > div:first-child {
                display:none;
            }
            div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.logo) [data-stale="false"] {
                width: 50% !important;
            }
            div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.logo) img{
                margin-left:20px;
            }

            div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.logo) [data-stale="false"]:has([data-testid="stText"]) .st-emotion-cache-y4bq5x {
                width:100% !important;
                justify-content: end;
                padding-right:20px;
            }
            div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.logo) [data-testid="stText"] {
                font-size: 12px !important;

            }
            """,
    ):
        st.image('/content/drive/MyDrive/img/tit.svg', width=180)
        st.text("감정일기 플레이리스트")


Header()

# ------------------Header 영역------------------------------

disable_enter_key_script = """
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const textarea = document.querySelector('textarea');
        textarea.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
            }
        });
    });
</script>
"""

st.markdown(disable_enter_key_script, unsafe_allow_html=True)


# 사용자에게 텍스트 입력 받기
user_input = ""


def Section_con():
    left, right = st.columns([0.28, 0.72])
    playlist_wrap = False

    with left:
        with stylable_container(
            key="write",
            css_styles="""
                {
                    height: 100% !important;
                    text-align: left !important;
                    padding: 30px 20px 20px 20px;
                    border-right: 1px solid #555152 !important;

                    gap:0 !important;
                }

                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.write) .st-emotion-cache-1kyxreq {
                    width:unset !important
                }

                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.write) [data-testid="stText"] {
                    line-height: 1.2 !important;
                    font-weight: bold !important;
                    text-align: left !important;
                    font-size: 1.1rem !important;
                    white-space: unset;
                    margin-bottom: 5px;
                }

                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.write) [data-stale="false"] {
                    width:100% !important;

                    height:auto;
                }
                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.write) img {
                    width:100% !important;

                    height:auto;
                    margin-bottom: 20px;
                }
                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.write) .stTextLabelWrapper{
                    width:100% !important;

                }
                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.write) .stTextArea {
                    width:100% !important;
                    border-top: 1px solid #aaa;
                    margin-top: 20px;
                }

                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.write) textarea {
                    background: #FFFDF9;
                    font-family: "UhBeemysen" !important;
                    font-size: 20px;
                    line-height: normal;
                }

                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.write) textarea::placeholder {
                    color: #AAA;
                }

                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.write) .stTextArea [data-baseweb="textarea"] {
                    border:none !important;
                    border-radius: 0
                }

                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.write) [data-testid="stButton"] {
                    width: unset !important;
                    text-align: center;
                    margin-top: 30px;
                }

                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.write) button {
                    width: 150px;
                    height: 40px;
                    border-radius: 20px;

                }
                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.write) button p {
                    color: #FFF !important;
                    font-size: 16px;
                }

                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.write) .stTextArea [data-testid="InputInstructions"] {
                    display:none !important;
                }
                """,
        ):
            st.image('/content/drive/MyDrive/img/cake.png', width=360)
            st.text("당신의 오늘의 일기를 입력해주세요.")
            st.text("오늘 무슨 일이 있었고 어떤 감정을 느끼셨나요?")

            # 사용자에게 텍스트 입력 받기
            user_input = st.text_area("",height=200, placeholder="원하는 텍스트를 입력하세요:")
            # st.write("입력된 텍스트:", user_input)

            # 버튼을 만들어서 버튼이 눌리면 동작하도록 함
            if st.button("일기 기록하기"):
                #노래 파일 경로
                playlist = find_similar_songs(user_input,songs_data)
                playlist_wrap = True
                

    with right:
        with stylable_container(
            key="song",
            css_styles="""
                {
                    width: 100% !important;
                    margin-bottom: 30px;
                }

                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.song) [data-testid="stText"] {
                    font-size: 24px;
                    font-weight: 700 !important;

                    width: 100% !important;
                    height:100px;
                    line-height:100px;

                    border-bottom: 1px solid #555152 !important;

                    padding-left:1em;
                }

                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.song) [data-testid="stImage"] img {
                    width:100%;
                    height: auto;
                }
            """
        ):
            st.text("나만의 감정일기 노래리스트 만들기")

        # st.markdown에 링크를 추가하는 함수
        def create_link(tit):
            return f'<a href="https://www.youtube.com/results?search_query={tit}" target="_blank">{tit}</a>'


        if playlist_wrap:
            em, list0, list1, list2, em = st.columns([0.1,1.0,1.0,1.0,0.1])

            for i in range(3):
                with locals()[f"list{i}"]:
                    with stylable_container(
                    key=f"playlist{i}",
                    css_styles=f"""
                        {{
                            padding: 0 10px !important;
                        }}

                        div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.playlist{i}) [data-stale="false"]:nth-child(4) .stMarkdown {{
                            width:100% !important;  
                        }}

                        div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.playlist{i}) [data-stale="false"]:nth-child(4) a {{
                            white-space: pre-wrap;
                            font-size: 16px;
                            font-weight: 700 !important;
                            line-height:1.3;
                            height: 42px;

                            text-overflow:ellipsis;
                            overflow:hidden;
                            display: -webkit-box !important;
                            -webkit-line-clamp: 2;
                            -webkit-box-orient: vertical;
                            
                            text-decoration: none;

                            margin-bottom: 20px;
                            margin-top: -10px !important;
                        }}

                        div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.playlist{i}) [data-stale="false"]:nth-child(3) [data-testid="stText"] {{
                            font-size: 12px;
                            margin-top:10px;
                        }}

                        div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.playlist{i}) [data-stale="false"]  {{
                            width:100% !important;    
                        }}

                        div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.playlist{i}) [data-stale="false"]:nth-child(2) div {{
                            width:100% !important; 
                        }}

                        div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.playlist{i}) [data-stale="false"] .stTextLabelWrapper {{
                            width:100% !important;    
                        }}

                        div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.playlist{i}) [data-stale="false"]  {{
                            width:100% !important;    
                        }}
                    """
                    ):
                        st.image(playlist[i]["img"])
                        # st.text(playlist[i]["genre"])
                        # st.markdown 링크를 추가
                        st.text(playlist[i]["singer"])
                        st.markdown(create_link(playlist[i]["title"]), unsafe_allow_html=True)
        else:
            with stylable_container(
            key=f"nolist",
            css_styles="""
                {
                     margin-top: 150px;
                }

                div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.nolist) p {
                    color: #AAA !important;
                    font-size: 20px;
                    text-align:center;
                    line-height:1.5;
                }
            """
            ):
                st.markdown("<p>일기를 기록하고 나만의 감성이 담긴 <br> 플레이리스트를 추천받으세요.</p>", unsafe_allow_html=True)

Section_con()

