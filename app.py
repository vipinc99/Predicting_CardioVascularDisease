import streamlit as st
import pandas as pd
from joblib import load
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from plotly.express import histogram,box,sunburst,scatter_mapbox
import json
from sklearn.preprocessing import OrdinalEncoder
from datetime import datetime
from fpdf import FPDF
from streamlit_gsheets import GSheetsConnection

#Layout
st.set_page_config(
    page_title="Silent Heart",
    layout="wide",
    page_icon="logo.jpg",
    initial_sidebar_state="auto")


@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath,"r") as f:
        return json.load(f)

@st.cache_resource
def model(model):
    final_model = load(model)
    return final_model

@st.cache_data(show_spinner="Loading visuals...")
def load_data(url):
    df = pd.read_csv(url)
    return df


final_model = model('model.joblib')
odf = load_data("CVD_cleaned.csv")

#Gsheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="Record",usecols=list(range(20)),ttl="5m")
existing_data=existing_data.dropna(how="all")
existing_data_validation=conn.read(worksheet="Validation",usecols=list(range(5)),ttl="5m")
existing_data_validation=existing_data_validation.dropna(how="all")

# # Hide the github icon on the right side in the deployed app
# hide_github_icon = """
#     <style>
#     .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
#     </style>
# """
# st.markdown(hide_github_icon, unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu('Silent Heart', ["Home", 'Prediction','Find a Doctor','About'], 
        icons=['house','activity','geo-alt','info-circle'],menu_icon='heart-pulse', default_index=0)
    lottie = load_lottiefile("heartanimation.json")
    st_lottie(lottie,key='loc')

# # To remove the hamburger menu (this is in the right part of the site)
# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style>"""
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)


#Home page
if selected=="Home":
    st.title(":red[Silent Heart]")
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📑 Blogs","📹 Videos"])
    with tab1:
        #Dashboard section
        st.header("Dashboard")
        col1, col2, col3 = st.columns(3)
        col1.metric("People affected by CVD", "620 M", "8 %",delta_color='inverse')
        col2.metric("Deaths", "20.5 M", "1.2 %",delta_color='inverse')
        col3.metric("Waiting time for surgery", "7 days", "- 8 days",delta_color='inverse')
        #Viz1
        @st.cache_data(show_spinner="Loading visuals...")
        def viz1():
            viz1 = histogram(odf, x="Smoking_History", color='Heart_Disease', barmode='group',
                            title="Smoking history vs Heart Disease",
                            labels={
                     "Smoking_History": "Smoking History",
                     "Heart_Disease": "Heart Disease"
                                    },
                            category_orders={"Smoking_History": ["Yes", "No"]}) 
            st.plotly_chart(viz1,theme="streamlit",use_column_width=True)
        
        viz1()

        #Viz2
        @st.cache_data(show_spinner="Loading visuals...")
        def viz2():
            viz2 = box(odf,
                    x="Alcohol_Consumption",
                    y="BMI",
                    color="Heart_Disease",
                     labels={
                     "Alcohol_Consumption": "Alcohol Consumption",
                     "Heart_Disease": "Heart Disease",
                     "BMI":"BMI"
                                    },
                    title="BMI Distribution across Alcohol Consumption on Heart Disease Status",
                    category_orders={"Alcohol_Consumption": ["Yes", "No"]})
            st.plotly_chart(viz2,theme="streamlit",use_column_width=True)

        viz2()


        #Viz3
        @st.cache_data(show_spinner="Loading visuals...")
        def viz3():
            viz3 = sunburst(odf, path=['Sex','Heart_Disease' ,'Age_Category'],values='Alcohol_Consumption', color='Alcohol_Consumption',labels={
                     "Alcohol_Consumption": "Alcohol Consumption"
                                    },title='Analysis of Sex, Age category and the presence of Heart disease')
            st.plotly_chart(viz3,theme="streamlit",use_column_width=True)
        
        viz3()

        #Viz4
        @st.cache_data(show_spinner="Loading visuals...")
        def viz4():
            viz4 = histogram(odf, x="BMI", color="Heart_Disease",
                            labels={"Heart_Disease":"Heart Disease"},title="BMI vs Heart Disease",nbins=30)
            st.plotly_chart(viz4,theme="streamlit",use_column_width=True)
        
        viz4()


    with tab2:
        #Blogs section
        st.header("Blogs")
        col1,col2=st.columns(2,gap="medium")
        with col1:
            with st.expander("**How to improve heart health at any age?**",expanded=True):
                st.image("blog1.jpg",use_column_width=True)
                st.markdown("<div style='text-align: justify;'>Dr. Leana Wen advocates early health habits: prioritize exercise, nutrition, and substance awareness from teens. Aim for 150 weekly minutes of enjoyable exercise, embrace whole foods, and avoid smoking for heart health.</div>", unsafe_allow_html=True)
                st.markdown( """<a style='display: block; text-align: center;' href="https://edition.cnn.com/2024/02/02/health/improve-heart-health-wellness/index.html">Read the full blog</a>""",unsafe_allow_html=True)
        with col2:
            with st.expander("**How can heart disease be prevented?**",expanded=True):
                st.image("blog2.jpg",use_column_width=True)
                st.markdown("<div style='text-align: justify;'>Prevent heart disease by avoiding tobacco, limiting alcohol, eating heart-healthy foods, and managing cholesterol levels. Lifestyle changes and medications can significantly reduce risks and promote heart health.</div>", unsafe_allow_html=True)
                st.markdown( """<a style='display: block; text-align: center;' href="https://my.clevelandclinic.org/health/articles/17385-heart-disease-prevention-and-reversal">Read the full blog</a>""",unsafe_allow_html=True)
            
        col1,col2=st.columns(2,gap="medium")
        with col1:
            with st.expander("**How does smoking and drinking harm your health?**",expanded=True):
                st.image("blog3.jpg",use_column_width=True)
                st.markdown("<div style='text-align: justify;'>The coexistence of smoking and drinking poses significant health risks, often intertwined as a lifestyle choice. Their combined impact can be severe and potentially fatal if frequent. It's crucial to understand and address the associated health hazards.</div>", unsafe_allow_html=True)
                st.markdown( """<a style='display: block; text-align: center;' href="https://shorturl.at/ginH5">Read the full blog</a>""",unsafe_allow_html=True)
        with col2:
            with st.expander("**6 Exercises to improve heart health**",expanded=True):
                st.image("blog4.jpg",use_column_width=True)
                st.markdown("<div style='text-align: justify;'>Various exercises, including brisk walking, running, cycling, strength training, yoga, and high-intensity interval training (HIIT), are scientifically proven to enhance heart health. Incorporate a mix of these activities into your routine for optimal cardiovascular benefits.</div>", unsafe_allow_html=True)
                st.markdown( """<a style='display: block; text-align: center;' href="https://www.goodrx.com/well-being/movement-exercise/exercises-to-improve-heart-health">Read the full blog</a>""",unsafe_allow_html=True)
    
    with tab3:
        #Video section
        st.header("Videos")
        col1,col2=st.columns(2,gap="medium")
        with col1:
            with st.container(border=True):
                st.video("https://youtu.be/h413NHcx7eo?si=k7GYfGGm7nCQn3lu")
        with col2:
            with st.container(border=True):
                st.video("https://youtu.be/g131j2lb3xw?si=TmTONNrRnYOkKfP7")
        
        col1,col2=st.columns(2,gap="medium")
        with col1:
            with st.container(border=True):
                st.video("https://youtu.be/_ePLBIDlChA?si=E_27Mo-D2lT9Aogm")
        with col2:
            with st.container(border=True):
                st.video("https://youtu.be/J1DUQFL-VHw?si=BLIl07CZXet14zvW")


#Prediction Page
predict = st.container()
results = st.container()
if selected=="Prediction":
    with predict:
        st.title(":red[Cardiovascular Disease Prediction]")
        st.subheader('Fill out the following:')
        name = st.text_input('Enter your Name')
        st.write('**Demographic and Screening Questions**')
        Age_Category = st.selectbox('In what Age category do you belong?',('Select One','18-24',
                                                                            '25-29',
                                                                            '30-34',
                                                                            '35-39',
                                                                            '40-44',
                                                                            '45-49',
                                                                            '50-54',
                                                                            '55-59',
                                                                            '60-64',
                                                                            '65-69',
                                                                            '70-74',
                                                                            '75-79',
                                                                            '80+'))
                                                    
        Sex = st.selectbox('Sex',('Select One','Male','Female'))

        Height = st.selectbox('How tall are you?',('Feet and Inches','Centimeters'))

        if Height == 'Feet and Inches':
            Feet = st.selectbox('Feet',('Feet',3,4,5,6,7),label_visibility="collapsed")
            Inches = st.selectbox('Inches',('Inches',0,1,2,3,4,5,6,7,8,9,10,11),label_visibility="collapsed")
            if Feet != 'Feet' and Inches != 'Inches':
                Height_cm = ((Feet * 12) + Inches) * 2.54         
        else:
            Height_cm = st.number_input('How tall are you in cm?',min_value=25,max_value=300,step=10)
    
        Weight_kg = st.number_input('Weight (kg)',min_value=25.00,max_value=300.00,step=10.00)
                      
        Smoking_History = st.radio('Have you smoked at least 100 cigarettes in your entire life?',
                                    ('No','Yes'),horizontal=True)

        st.write('**Health Status**')
        General_Health = st.selectbox('Would you say that in general, your health is',('Select One',
                                                                            'Poor',
                                                                            'Fair',
                                                                            'Good',
                                                                            'Very Good',
                                                                            'Excellent'
                                                                                    ))
        st.write('**Health Care Access**')
        Checkup = st.selectbox('About how long has it been since you \
                                    last visited a doctor for a routine checkup?',('Select One',
                                                                            'Within the past year',
                                                                            'Within the past 2 years',
                                                                            'Within the past 5 years',
                                                                            '5 or more years ago',
                                                                            'Never'
                                                                                    ))

        st.write('**Exercise**')
        Exercise = st.radio('During the past month, other than your regular job, did you participate in any physical activities or exercises such as running, calisthenics, golf, gardening, or walking for exercise?',
                                    ('Yes','No'),horizontal=True)

        st.write('**Health Conditions**')
        st.write('Have you ever been diagnosed with any of the following?')
        Depression = st.radio('Have you been diagnosed with a depressive disorder such as depression, major depression, dysthymia, or minor depression?',
                                    ('No','Yes'),horizontal=True)
        Diabetes = st.radio('Have you been diagnosed with diabetes?',
                                    ('No','Yes'),horizontal=True)
        Arthritis = st.radio('Have you been diagnosed with some form of arthritis, rheumatoid arthritis, gout, lupus, or fibromyalgia?',
                                    ('No','Yes'),horizontal=True)
        Skin_Cancer = st.radio('Have you been diagnosed with skin cancer?',
                                    ('No','Yes'),horizontal=True)
        Other_Cancer = st.radio('Have you been diagnosed with any other types of cancer?',
                                    ('No','Yes'),horizontal=True)
        
        st.write('**Food and Drink Consumption**')

        Alcohol_Consumption = st.slider(
                                'During the past 30 days, how many days \
                                did you have at least one drink of any alcoholic beverage such \
                                as beer, wine, a malt beverage or liquor?',
                                0, 30,step=1)
        
        st.write('Think about the food you ate during the past 30 days, including meals and snacks.')

        fruit = st.selectbox('Not including juices, how often do you eat a fruit?',('Select One','Per Day',
                                                                                'Per Week',
                                                                                'Per Month'))

        if fruit == 'Per Day':
            fruit_day = st.selectbox('Day',('How many times do you eat fruit per day?',0,1,2,3,4,5),label_visibility="collapsed")

            if fruit_day != 'How many times do you eat fruit per day?':
                Fruit_Consumption = fruit_day*30
        
        elif fruit == 'Per Week':
            fruit_week = st.selectbox('Day',('How many times do you eat fruit per week?',0,1,2,3,4,5),label_visibility="collapsed")
            if fruit_week != 'How many times do you eat fruit per week?':
                Fruit_Consumption = fruit_week *4
        elif fruit == 'Per Month':
            fruit_month = st.selectbox('Day',('How many times do you eat fruit per month?',0,1,2,3,4,5),label_visibility="collapsed")
            if fruit_month != 'How many times do you eat fruit per month?':
                Fruit_Consumption = fruit_month

        green_veg = st.selectbox('How often do you eat a green leafy or lettuce salad, with or without other vegetables?',('Select One','Per Day',
                                                                                'Per Week',
                                                                                'Per Month'))

        if green_veg == 'Per Day':
            green_veg_day = st.selectbox('Day',('How many times do you eat Green Vegetables per day?',0,1,2,3,4,5),label_visibility="collapsed")

            if green_veg_day != 'How many times do you eat Green Vegetables per day?':
                Green_Vegetables_Consumption = green_veg_day*30
        
        elif green_veg == 'Per Week':
            green_veg_week = st.selectbox('Day',('How many times do you eat Green Vegetables per week?',0,1,2,3,4,5),label_visibility="collapsed")
            if green_veg_week != 'How many times do you eat Green Vegetables per week?':
                Green_Vegetables_Consumption = green_veg_week *4
        elif green_veg == 'Per Month':
            green_veg_month = st.selectbox('Day',('How many times do you eat Green Vegetables per month?',0,1,2,3,4,5),label_visibility="collapsed")
            if green_veg_month != 'How many times do you eat Green Vegetables per month?':
                Green_Vegetables_Consumption = green_veg_month

        fried = st.selectbox('How often do you eat any kind of fried potatoes, including French fries, home fries, or hash browns?',('Select One','Per Day',
                                                                                'Per Week',
                                                                                'Per Month'))

        if fried == 'Per Day':
            fried_day = st.selectbox('Day',('How many times do you eat Fried Potatoes per day?',0,1,2,3,4,5),label_visibility="collapsed")

            if fried_day != 'How many times do you eat Fried Potatoes per day?':
                FriedPotato_Consumption = fried_day*30
        
        elif fried == 'Per Week':
            fried_week = st.selectbox('Day',('How many times do you eat Fried Potatoes per week?',0,1,2,3,4,5),label_visibility="collapsed")
            if fried_week != 'How many times do you eat Fried Potatoes week?':
                FriedPotato_Consumption = fried_week *4
        elif fried == 'Per Month':
            fried_month = st.selectbox('Day',('How many times do you eat Fried Potatoes per month?',0,1,2,3,4,5),label_visibility="collapsed")
            if fried_month != 'How many times do you eat Fried Potatoes per month?':
                FriedPotato_Consumption = fried_month
        
        col1, col2, col3 , col4, col5 = st.columns(5)
        with col1:
            pass
        with col2:
            pass
        with col4:
            pass
        with col5:
            pass
        with col3 :
            submit = st.button('Predict',type="primary")
        
        st.warning('Disclaimer: **Your data is being collected to enhance our model. We prioritize your privacy and employ strict security measures.The results from this test are not intended to diagnose or treat any disease.**')
    
    

    with results:
        if "load_state" not in st.session_state:
            st.session_state.load_state=False
        
        if submit or st.session_state.load_state:
            st.session_state.load_state=True
            try:
                bmi = round(Weight_kg / (Height_cm/100)**2,2)
                new_input = [General_Health,Checkup,Exercise,Skin_Cancer,
                            Other_Cancer,Depression,Diabetes,Arthritis,
                            Sex,Age_Category,Height_cm,Weight_kg,bmi,
                            Smoking_History,Alcohol_Consumption,Fruit_Consumption,
                            Green_Vegetables_Consumption,FriedPotato_Consumption
                ]
                df = pd.DataFrame([new_input])
                df.columns = ['General_Health',
                'Checkup',
                'Exercise',
                'Skin_Cancer',
                'Other_Cancer',
                'Depression',
                'Diabetes',
                'Arthritis',
                'Sex',
                'Age_Category',
                'Height_(cm)',
                'Weight_(kg)',
                'BMI',
                'Smoking_History',
                'Alcohol_Consumption',
                'Fruit_Consumption',
                'Green_Vegetables_Consumption',
                'FriedPotato_Consumption']
                copy_df=df.copy()
                copy_df.insert(0, 'Name', [name])
                test_dict={'General_Health': ['Poor', 'Very Good', 'Good', 'Fair', 'Excellent'], 'Checkup': ['Within the past 2 years', 'Within the past year', '5 or more years ago', 'Within the past 5 years', 'Never'], 'Exercise': ['No', 'Yes'], 'Skin_Cancer': ['No', 'Yes'], 'Other_Cancer': ['No', 'Yes'], 'Depression': ['No', 'Yes'], 'Diabetes': ['No', 'Yes', 'No, pre-diabetes or borderline diabetes', 'Yes, but female told only during pregnancy'], 'Arthritis': ['Yes', 'No'], 'Sex': ['Female', 'Male'], 'Age_Category': ['70-74', '60-64', '75-79', '80+', '65-69', '50-54', '45-49', '18-24', '30-34', '55-59', '35-39', '40-44', '25-29'], 'Smoking_History': ['Yes', 'No']}
                categorical = df.select_dtypes(include=['object']).columns
                l=[]
                for i in test_dict.values():
                    l.append(i)

                ordinal_encoder = OrdinalEncoder(categories=l)
                df[categorical]=ordinal_encoder.fit_transform(df[categorical])
                pred = final_model.predict(df)
                st.subheader("Result")
                st.write(f'Hello, {name}!')
                st.write('Based from the Machine Learning model, your risk of developing Cardiovascular Disease (CVD) is:')

                if pred[0] == 0: 
                    #st.balloons()    
                    risk = 'LOW'
                    copy_df['Heart_Disease']="No"
                    st.success(f'**{risk}**')
                else:
                    risk = 'HIGH'
                    copy_df['Heart_Disease']="Yes"
                    st.error(f'**{risk}**')
                
                updated_df=pd.concat([existing_data,copy_df],ignore_index=True)
                conn.update(worksheet="Record",data=updated_df)

                cnum=['Alcohol_Consumption','Fruit_Consumption','Green_Vegetables_Consumption','FriedPotato_Consumption']
                mean_values =odf[cnum].mean()
                with st.expander("**Detailed information**"):
                    for col in cnum:
                        mean_value = mean_values[col]
                        input_value = df.loc[0, col]
                        col = col.replace('_', ' ')
                        percentage_difference = abs(((input_value - mean_value) / mean_value) * 100)
                        if input_value > mean_value:
                            st.write(f"Your {col} ({input_value}) is greater than the mean ({mean_value:.2f}) by {percentage_difference:.2f}%")
                        elif input_value < mean_value:
                            st.write(f"Your {col} ({input_value}) is less than the mean ({mean_value:.2f}) by {percentage_difference:.2f}%")
                        else:
                            st.write(f"Your {col} ({input_value}) is equal to the mean ({mean_value:.2f})")

                with st.expander("**Recommendation**"):
                    if pred[0]==0:
                        st.markdown("<ul style='list-style-type:disc;'><li>Maintain a heart-healthy diet rich in fruits(pomegranate,avacado,berries), vegetables(tomatoes,onions,dioscorea), whole grains, and lean proteins.</li><li>Engage in regular physical activity such as meditation/yoga or exercise for at least 30 minutes most days of the week.</li><li>Keep up-to-date with current health guidelines to ensure ongoing adherence to heart-healthy habits.</li><li>Regular check-ups can help monitor overall health and detect any potential issues early on.</li></ul>",unsafe_allow_html=True)
                    else:
                        st.markdown("<ul style='list-style-type:disc;'><li>Adhere to prescribed medications and regular medical check-ups.</li><li>Seek professional guidance and support from healthcare providers or nutritionists for personalized preventive strategies.</li><li>⁠Incorporate stress-reducing activities such as meditation into daily routine and ensure adequate sleep duration</li><li>Avoid smoking and alcohol consumption with immediate effect</li><li>⁠Adopt dietary modifications to reduce salt and sugar intake.</li></ul>",unsafe_allow_html=True)
                

                #CSV download        
                @st.cache_data
                def convert_df(df):
                    return df.to_csv(index=False).encode("utf-8")

                csv = convert_df(copy_df)
                current_date = datetime.now().strftime("%d-%b-%y")
                #current_date = datetime.now()
               
                #PDF download
                content_str = f"""
                            Name:{name}\n
                            Sex:{Sex}\n
                            Age Category:{Age_Category}\n
                            Height(cm):{Height_cm}\n
                            Weight(kg):{Weight_kg}\n
                            BMI:{bmi}\n
                            General Health:{General_Health}\n
                            Checkup:{Checkup}\n
                            Smoking history:{Smoking_History}\n
                            Skin Cancer:{Skin_Cancer}\n
                            Other Cancer:{Other_Cancer}\n
                            Depression:{Depression}\n
                            Diabetes:{Diabetes}\n
                            Arthritis:{Arthritis}\n
                            Data in the past one month(30 days):\n
                            Exercise:{Exercise}\n
                            Alcohol Consumption:{Alcohol_Consumption}\n
                            Fruit Consumption:{Fruit_Consumption}\n
                            Green Vegetables Consumption:{Green_Vegetables_Consumption}\n
                            Fried Potato Consumption:{FriedPotato_Consumption}\n\n
                            The risk of developing Cardiovascular Disease (CVD) is:{risk}
                            """

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial",size=18,style="B")
                pdf.cell(0, 10, txt="Health Record", ln=1,align="C")
                pdf.set_font("Arial", size=15)
                pdf.multi_cell(0, 5, txt=content_str,align="L")
                pdf_file = pdf.output(dest="S").encode("latin-1")
                
                st.subheader("User Record")
                st.download_button(
                        label="Download PDF",
                        data=pdf_file,
                        file_name=f"{name} details:{current_date}.pdf",
                        mime="application/pdf",
                        type="primary"
                    )
                st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"{name} details:{current_date}.csv",
                        mime="text/csv",
                        type="primary"
                        )
                

                with st.expander("**Doctor's Validation (To be filled by a medical practitioner only)**"):
                    doctorname=st.text_input("Enter Doctor's Name")
                    doctoropinion = st.radio('What is the risk of patient developing Cardiovascular Disease (CVD)?',
                                    ('LOW','HIGH'),horizontal=True,index=None)
                    if doctoropinion!=None and doctorname!=None:
                        if risk==doctoropinion:
                            validation="Correct"
                        else:
                            validation="Wrong"

                        validationdata = {'Patient Name': [name],
                                'Model output': [risk],
                                'Doctor output': [doctoropinion],
                                'Validation':[validation],
                                'Doctor Name':[doctorname]
                                }
                        validationdf=pd.DataFrame(validationdata)
                        updated_validation_df=pd.concat([existing_data_validation,validationdf],ignore_index=True)
                        conn.update(worksheet="Validation",data=updated_validation_df)
                        st.success(f"Thank you Dr.{doctorname} for validating our model!")      
                         
            except:
                st.error("Please enter valid values")


#Find a doctor page
if selected=="Find a Doctor":
    st.title(":red[Find a Doctor]")
    mapdata=pd.read_excel("Cardiologist_List.xlsx")
    state=st.selectbox("Choose your State",mapdata['State'].unique(),index=None,placeholder="State")
    if state!=None:
        mapdata['Check']=False
        filtered_df = mapdata[mapdata['State'] == state]
        t=st.data_editor(filtered_df,column_order=['Check','Doctor Name','Address','Phone','Email','URL','City']
        ,column_config={"URL":st.column_config.LinkColumn(),
        "Check":st.column_config.CheckboxColumn(width='small',help="Select the checkbox to see the location on map")},
        hide_index=True,disabled=['Doctor Name','Address','Phone','Email','URL','City'])
        check=t[t['Check']==True]
        contains_true = check['Check'].any()
        if contains_true:
            fig =scatter_mapbox(check, lat="lat", lon="lng", hover_name="City", hover_data=["Address"],
                                    color_discrete_sequence=["red"], zoom=12)
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        else:
            fig =scatter_mapbox(t, lat="lat", lon="lng", hover_name="City", hover_data=["Address"],
                                    color_discrete_sequence=["red"], zoom=6)
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig,use_column_width=True)
        with st.expander("**Doctors across India**"):
            st.cache_data(show_spinner="Loading map...")
            def loadmap():
                fig2 =scatter_mapbox(mapdata, lat="lat", lon="lng", hover_name="City", hover_data=["State","Address"],
                                        color_discrete_sequence=["red"], zoom=4)
                fig2.update_layout(mapbox_style="open-street-map")
                fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig2,use_column_width=True)

            loadmap()

#About page
if selected=="About":
    st.title(":red[Information]")
    st.markdown("<div style='text-align: justify; padding:30px;'><p>The term <span style='color:#ff4b4b;'>heart disease</span> refers to a broad range of disorders that impair arteries, blood vessels, and other organs and cause abnormal heart function. In the modern world, heart disease is the primary cause of death. The World Health Organization estimates that cardiac conditions will kill 12 million people globally year. Irrespective of the type of heart disease afflicting an individual, the benefit of early detection is undeniable. Similar to other medical conditions, early detection of heart disease simplifies treatment and significantly raises a patient's chances of survival.</p><p>The purpose of this Heart Disease Prediction App is to assist users in evaluating their cardiovascular health.It is crucial to examine the interdependence of the risk factors in patients' medical histories and comprehend their respective contributions to the prognosis of heart disease. This algorithm predicts whether or not a user has heart disease based on a variety of characteristics, including age, gender, the user's history of depression or diabetes, and numerous other lifestyle factors like alcohol usage or smoking.In addition, this program allows users to evaluate their cardiovascular health and provides contact information for many physicians.</p></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-top: 25px;'><p style='color:#ff4b4b;font-weight: bold;'>Contact us</p><a href='mailto:silentheart.care@gmail.com'> silentheart.care@gmail.com</a></div>", unsafe_allow_html=True)