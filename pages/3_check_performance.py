import streamlit as st
from topicrec.tokenizer import CustomTokenizer
st.set_page_config(page_title="입력 데이터에 대한 주제 추천")
st.title("주제 추천 솔루션")

st.session_state["checked"] = 0

### PERFORMANCE CHECK ###
st.subheader("본 모델의 성능")
if "model" in st.session_state:
    model = st.session_state["model"]
    data_type = st.session_state["data_type"]
    print("data_type", data_type)
    if data_type == "news":
        data_path = st.session_state["data_path"]
    elif data_type == "patent":
        data_path = st.session_state["test_data_path"]
    inv_org_mappings = st.session_state["inv_org_mappings"]
else:
    print("data_type has no value")

if st.button("성능 확인"):
    ### LOAD DATA ###
    from topicrec.dataset import fetch_data
    @st.cache_data
    def wrap_fetch_data(rootdir, data_type, train_yn=False):
        return fetch_data(rootdir, data_type, train_yn=False)

    test_docs, y_true = wrap_fetch_data(data_path, data_type, False)

    ### TEST DATA INFERENCE ###
    from tqdm import tqdm
    from sklearn.metrics import accuracy_score
    y_preds = []
    checked = st.session_state["checked"]
    if checked == 0:
        with st.spinner("Waiting. . ."):
            for dt_test in tqdm(test_docs):
                if data_type == "news":
                    y_pred, _ = model.transform(dt_test)
                    y_pred = y_pred[0]
                elif data_type == "patent":
                    y_pred, _ = model.transform(dt_test)
                    y_pred = inv_org_mappings[y_pred[0]]
                y_preds.append(y_pred)
            checked = 1
            st.session_state["checked"] = checked
            st.session_state["y_preds"] = y_preds
    else:
        y_preds = st.session_state["y_preds"]

    acc = accuracy_score(y_true, y_preds)
    st.write("accuracy : ", acc)
