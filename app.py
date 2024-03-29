from fastai.vision.all import *
# from fastai.vision.core import PILImage
# from fastai.learner import load_learner
import streamlit as st
import requests
import os

@st.cache(allow_output_mutation=True)
def get_learner(file_name='export.pkl'):
    learn = load_learner(file_name)
    return learn


def download_files(URL):
    with open("export.pkl", "wb") as model:
        r = requests.get(URL)
        model.write(r.content)
    try:
        assert(os.path.getsize("export.pkl") > 15000)
        st.success('Model is ready! Go ahead to the next stage')
    except:
        st.warning("There is something wrong!")


def write():
    pl = st.empty()
    pl.markdown('''
    <html>
    <body style="background-color:#216D6D;">
    <h1 align="center" style="color:white;">Image Classifier</h1>
    </body>
    </html>
    ''',unsafe_allow_html=True)
    if (not os.path.isfile('export.pkl') or os.path.getsize("export.pkl") < 15000):
        ph = st.empty()
        ph2 = st.empty()
        ph3 = st.empty()
        # ph.warning('Please download the model file')
        URL = ph3.text_input('Please paste URL(direct download link) to your image classifier model','')
        if ph2.button('Get your model'):
            ph.empty()
            ph3.empty()
            ph2.info('Please wait a moment...')
            try:
                download_files(URL)
                # ph2.text('Model is ready!')
                st.button("Next Stage")
            except Exception as e:
                st.error('Not a correct URL!')
                print(str(e))

    else:
        st.success("Model is ready")

        img_data = st.file_uploader('Please upload your image',type=['jpg','jpeg','png','gif'])
        if img_data == None:
                st.warning('Checking data...')
        else:
            st.image(img_data,width=180,use_column_width=False)
            check = st.button('Predict')
            if check:
                file_name = 'export.pkl'
                learn = get_learner(file_name)
                img = PILImage.create(img_data)
                result = learn.predict(img)
                pred,pred_idx,probs = result
                prob_value = f'{probs[pred_idx]:.04f}'
                st.write('Result: '+pred.capitalize())
                st.write('Probablitiy: '+prob_value)


if __name__ == "__main__":
    write()

    