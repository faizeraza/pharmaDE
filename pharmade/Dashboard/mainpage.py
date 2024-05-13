import base64
import streamlit as st
from streamlit.components.v1 import html

class MainPage:
    def __init__(self) -> None:
        st.set_page_config(
            page_title="Dashboard",
            page_icon="📊",
            layout="wide",
        )
        st.title("Pharma Dashboard")
    def get_base64(self,bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    def set_background(self,png_file):
        bin_str = self.get_base64(png_file)
        page_bg_img = '''
        <style>
        body {
        background-image: url("data:image/png;base64,%s");
        background-size: ;
        background-attachment: local;
        background-origin: content-box;
        }
        </style>
        ''' % bin_str
        st.markdown(page_bg_img, unsafe_allow_html=True)

    def showschema(self):
        self.set_background(r'C:\Users\Faizan Raza\Desktop\pharmaDE\images\bgimage.JPG')
        st.markdown(
            """
            <style>
            .element-container:has(style){
                display: none;
            }
            #button-after {
                display: none;
            }
            .element-container:has(#button-after) {
                display: none;
            }
            .element-container:has(#button-after) + div button {
                background-color: Green;
                width: 100px;
                height: 20px;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
        started = st.button("Get Start")
        if started:
            st.switch_page(r"C:\Users\Faizan Raza\Desktop\pharmaDE\pharmade\Dashboard\pages\distandcust.py")
        st.image(r'images\final_schema.PNG', caption='Star Schema')

if __name__=="__main__":
    mainpage = MainPage()
    mainpage.showschema()
