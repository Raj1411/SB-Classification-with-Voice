import pandas as pd
import streamlit as st
from time import sleep
import base64
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events



x=[]
txtdumpfile=open("./text.txt",'a+')
# engine=pyttsx3.init()
st.write("""# Swiss Beauty Product Classification """)
voicerate=120
# listener=sr.Recognizer()
if st.checkbox('Start'):
    st.subheader('Bobo is ready to listen...')
    try:
        stt_button = Button(label="Speak", width=100)

        stt_button.js_on_event("button_click", CustomJS(code="""
            var recognition = new webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = false;
        
            recognition.onresult = function (e) {
                var value = "";
                for (var i = e.resultIndex; i < e.results.length; ++i) {
                    if (e.results[i].isFinal) {
                        value += e.results[i][0].transcript;
                    }
                }
                if ( value != "") {
                    document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
                }
            }
            recognition.start();
            """))

        result = streamlit_bokeh_events(
            stt_button,
            events="GET_TEXT",
            key="listen",
            refresh_on_update=False,
            override_height=75,
            debounce_time=0)

        if result:
            if "GET_TEXT" in result:
                aud=result.get("GET_TEXT")
                st.write(aud)
            # st.text('Speak now!')
                with st.spinner('Recognizing...'):
                    # command=listener.recognize_google(aud)
                    # output=command
                    with open("./text.txt", "a+") as file_object:
                        file_object.seek(0)
                        data = file_object.read(100)
                        if len(data) > 0 :
                            file_object.write("\n")
                        file_object.write(aud)
                    x.append(aud.replace(' ',''))
                    st.write(x)

                xls = pd.read_excel("./words list - Copy.xlsx",index_col=0).to_dict()
                df=pd.read_excel("./Book2 - Copy.xlsx")
                # print(xls)


                xx=[]
                xxx=[]
                for i in xls:
                    xls=xls[i]
                    for ii in xls:
                        for jj in x:
                            if ii==jj:
                                xx.append(ii+":"+xls.get(jj))
                                for aq in xx:
                                    az=aq.split(":")
                                    for t in az:
                                        if az[1]==xls.get(jj):
                                            xxx.append(az[1])
                st.write(xxx)

                try:
                    result='This Product is:  '+xxx[0]+"     "+'😎'
                    font_color= f'<p style="font-family: American Typewriter ; background-color:red; color:white; font-size: 42px;">{result}</p>'
                    st.markdown(font_color, unsafe_allow_html=True)
                    df1=pd.DataFrame([df[df['sku code']==str(xxx[0])].iloc[0]['Product Name'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['Color/Group'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['Rating'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['MRP'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['Net.wet'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['Actual Description on products'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['Status of pics'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['Checked by Renuka'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['Product Dimensions'].replace('\n',', '),
                    df[df['sku code']==str(xxx[0])].iloc[0]['Buy LInk'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['HSN'].astype(int),
                    df[df['sku code']==str(xxx[0])].iloc[0]['How to use'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['Key Benefit'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['Difference from other'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['Hero Ingredients'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['Category'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['ARTIST TIP'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['Before / After'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['ARTIST TIP'],
                    df[df['sku code']==str(xxx[0])].iloc[0]['Name of Wev']],columns=['Product Details'],index=[
                    'Product Name','Color/Group','Rating','MRP','Net.wet','Actual Description on products','Status of pics','Checked by Renuka',
                    'Product Dimensions','Buy LInk','HSN','How to use','Key Benefit','Difference from other','Hero Ingredients','Category',
                    'ARTIST TIP','Before / After','ARTIST TIP-1','Name of Wev'])
                    html = """\
                        <html>  
                        <head></head>
                        <table border="0" 
                        align="center">
                        <body> {0}
                            <br> </br>
                            <br> </br>
                            <br> </br>
                            <br> </br>
                        </table>
                        </body>
                        </html>
                    """.format(df1.to_html(index=True,header=False))
                    st.markdown(html,unsafe_allow_html=True)
                except:
                    st.markdown('Error... Please speak Again. 😔 ')


    except:
        pass
