#분류 결과 + 이미지 + 텍스트와 함께 분류 결과에 따라 다른 출력 보여주기
#파일 이름 streamlit_app.py
import streamlit as st
from fastai.vision.all import *
from PIL import Image
import gdown

# Google Drive 파일 ID
file_id = '1g_f6r5fl1h451XookpBeV1AykWiNjcpP'

# Google Drive에서 파일 다운로드 함수
#@st.cache(allow_output_mutation=True)
@st.cache_resource
def load_model_from_drive(file_id):
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model.pkl'
    gdown.download(url, output, quiet=False)

    # Fastai 모델 로드
    learner = load_learner(output)
    return learner

def display_left_content(image, prediction, probs, labels):
    st.write("### 왼쪽: 기존 출력 결과")
    if image is not None:
        st.image(image, caption="업로드된 이미지", use_container_width=True)
    st.write(f"예측된 클래스: {prediction}")
    st.markdown("<h4>클래스별 확률:</h4>", unsafe_allow_html=True)
    for label, prob in zip(labels, probs):
        st.markdown(f"""
            <div style="background-color: #f0f0f0; border-radius: 5px; padding: 5px; margin: 5px 0;">
                <strong style="color: #333;">{label}:</strong>
                <div style="background-color: #d3d3d3; border-radius: 5px; width: 100%; padding: 2px;">
                    <div style="background-color: #4CAF50; width: {prob*100}%; padding: 5px 0; border-radius: 5px; text-align: center; color: white;">
                        {prob:.4f}
                    </div>
                </div>
        """, unsafe_allow_html=True)

def display_right_content(prediction, data):
    st.write("### 오른쪽: 동적 분류 결과")
    cols = st.columns(3)

    # 1st Row - Images
    for i in range(3):
        with cols[i]:
            st.image(data['images'][i], caption=f"이미지: {prediction}", use_container_width=True)
    # 2nd Row - YouTube Videos
    for i in range(3):
        with cols[i]:
            st.video(data['videos'][i])
            st.caption(f"유튜브: {prediction}")
    # 3rd Row - Text
    for i in range(3):
        with cols[i]:
            st.write(data['texts'][i])

# 모델 로드
st.write("모델을 로드 중입니다. 잠시만 기다려주세요...")
learner = load_model_from_drive(file_id)
st.success("모델이 성공적으로 로드되었습니다!")

labels = learner.dls.vocab

# 스타일링을 통해 페이지 마진 줄이기
st.markdown("""
    <style>
    .reportview-container .main .block-container {
        max-width: 90%;
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 분류에 따라 다른 콘텐츠 관리
content_data = {
    labels[0]: {
        'images': [
            "https://i.ibb.co/DDBBT8S/1.jpg",
            "https://i.ibb.co/pv5nnfz/2.jpg",
            "https://i.ibb.co/h9mh8hj/3.jpg"
        ],
        'videos': [
            "https://www.youtube.com/watch?v=Gip8gs4VUPk",
            "https://www.youtube.com/watch?v=_kMmnRJs5t4",
            "https://www.youtube.com/watch?v=bh4eJT-KiSI"
        ],
        'texts': [
            "광일이는 너무 귀여워",
            "광일이가 닮은 동물은 곰이야.",
            "광일이는 원래 베이스를 했다가 드럼으로 바뀌었어."
        ]
    },
    labels[1]: {
        'images': [
            "https://i.ibb.co/Vv0DH2w/6.jpg",
            "https://i.ibb.co/71s10Rx/5.jpg",
            "https://i.ibb.co/qJbGRyZ/4.jpg"
        ],
        'videos': [
            "https://www.youtube.com/watch?v=abdTaW9_j6M",
            "https://www.youtube.com/watch?v=yEAk4QzZ4Vo",
            "https://www.youtube.com/watch?v=yAPyU618qaQ"
        ],
        'texts': [
            "예찬이는 바이올린을 너무 잘해",
            "예찬이는 너무 좋은 맏형이야",
            "예찬이가 닮은 동물은 강아지야"
        ]
    },
    labels[2]: {
        'images': [
            "https://i.ibb.co/F7FmGgQ/9.jpg",
            "https://i.ibb.co/k1hTpHR/8.jpg",
            "https://i.ibb.co/XzfFFT5/7.jpg"
        ],
        'videos': [
            "https://www.youtube.com/watch?v=Tv6UaZ_9XzU",
            "https://www.youtube.com/watch?v=kqGVNHSOuM4",
            "https://www.youtube.com/watch?v=qYeERHUipa4"
        ],
        'texts': [
            "원상이는 베이스를 너무 잘쳐",
            "원상이는 경희대를 나왔어",
            "원상이의 닮은 동물은 너구리야"
        ]
    },
    labels[3]: {
        'images': [
            "https://i.ibb.co/TMM20nG/12.jpg",
            "https://i.ibb.co/PDtLYhN/11.jpg",
            "https://i.ibb.co/vD8HLjd/10.jpg"
        ],
        'videos': [
            "https://www.youtube.com/watch?v=WE2WqQf0wq4",
            "https://www.youtube.com/watch?v=xxtvr690ZJg",
            "https://www.youtube.com/watch?v=qoVnGUZqGio"
        ],
        'texts': [
            "상엽이는 목소리가 좋아",
            "상엽이는 노래를 엄청잘해",
            "상엽이가 닮은 동물은 다람쥐야야"
        ]
    }
}

# 레이아웃 설정
left_column, right_column = st.columns([1, 2])  # 왼쪽과 오른쪽의 비율 조정

# 파일 업로드 컴포넌트 (jpg, png, jpeg, webp, tiff 지원)
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "png", "jpeg", "webp", "tiff"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img = PILImage.create(uploaded_file)
    prediction, _, probs = learner.predict(img)

    with left_column:
        display_left_content(image, prediction, probs, labels)

    with right_column:
        # 분류 결과에 따른 콘텐츠 선택
        data = content_data.get(prediction, {
            'images': ["https://via.placeholder.com/300"] * 3,
            'videos': ["https://www.youtube.com/watch?v=3JZ_D3ELwOQ"] * 3,
            'texts': ["기본 텍스트"] * 3
        })
        display_right_content(prediction, data)

