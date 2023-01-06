from logging import PlaceHolder
import time
import plotly.express as px
import csv 
import numpy as np
import pandas as pd
import pickle
import streamlit as st
import sqlite3 as sq

conn = sq.connect("Login.db")
c = conn.cursor()


def create_usertable():
    c.execute("CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)")


def add_userdata(username, password):
    c.execute("INSERT INTO userstable(username,password) VALUES (?,?)", (username, password))
    conn.commit()


def login_user(username, password):
    c.execute("SELECT * FROM userstable WHERE username=? AND password= ?", (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute("SELECT * FROM userstable")
    data = c.fetchall()
    return data


def main():
    st.caption("Made with Afya Bora Foundation.")
    st.title("Welcome to the Afya Bora Medical Analysis System.")

    Menu = ['Login', 'SignUp', 'AboutUs']
    Selection = st.sidebar.selectbox("Menu", Menu)

    if Selection == "Login":
        st.sidebar.subheader("Login with correct credentials.")

        username = st.sidebar.text_input("User name:")
        password = st.sidebar.text_input("Password:", type='password')

        if st.sidebar.checkbox("Login"):
            create_usertable()
            result = login_user(username, password)
            if result:
                st.success("Logged in as {}".format(username))
                st.warning("To be used by a fully trained medical officer.")
                st.write(""" ## Analyzation and Presentation of Data.""")

                categories = ['Data Analysation', 'Visual Display', 'Dashboard']
                categories = st.selectbox("Select category:", categories)

                if categories == 'Data Analysation':
                    st.subheader("Analyze data effectively.")

                    data = st.file_uploader("Upload dataset:", type=['csv'])
                    st.success("Data successfully loaded.")
                    if data is not None:
                        df = pd.read_csv(data)
                        st.dataframe(df.head(10))

                        if st.checkbox("Columns count"):
                            st.write(df.columns)
                        if st.checkbox("Number of rows and Cols"):
                            st.write(df.shape)
                        if st.checkbox("Checking empty(null) columns"):
                            st.write(df.isnull().sum())
                        if st.checkbox("Multiple columns Selection"):
                            selected_columns = st.multiselect(
                                "Select columns of choice for analysis, N/B Let target be  the last column of selection:",
                                df.columns)
                            df1 = df[selected_columns]
                            st.dataframe(df1)

                        if st.checkbox("Summarized Display"):
                            st.write(df1.describe().T)


                elif categories == 'Visual Display':
                    st.subheader("Visually analyze the data")

                    data = st.file_uploader("Upload dataset:", type=['csv'])
                    st.success("Data successfully loaded")
                    if data is not None:
                        df = pd.read_csv(data)
                        st.dataframe(df.head(10))

                    if st.checkbox("Multiple Columns Selection for Plot"):
                        selected_columns = st.multiselect(
                            "Select columns of choice for plotting, N/B Let target be  the last column of selection:",
                            df.columns)
                        df1 = df[selected_columns]
                        st.dataframe(df1)

                    if st.checkbox("Bar Display"):
                        st.area_chart(df1)

                    if st.checkbox("Pie Display"):
                        all_columns = df.columns.to_list()
                        pie_columns = st.selectbox("Select Column for Display:", all_columns)
                        pieChart = df[pie_columns].value_counts().plot.pie(autopct="%1.1f%%")
                        st.write(pieChart)
                        st.pyplot()
                        
                        
                        
                        
                elif categories == 'Dashboard':
                    st.subheader("Dashboard analysis of the data")
                    #Creating filters
                    df = pd.read_csv("C:/Users/BREEZIE/Desktop/diabetes.csv")
                    Outcome_filter = st.selectbox("Choose medical condition for analysis:",pd.unique(df['Outcome']))
                    st.write("###### 0: Represents Non Diabetic")
                    st.write("###### 1: Represents Diabetic")
                    st.write("###### Condition Selected:",Outcome_filter)

                    PlaceHolder = st.empty()

                    #Filtering job data to a unique selection
                    df = df[df['Outcome']==Outcome_filter]

                    for seconds in range(800):
                        
                        df['Insulin_new'] = df['Insulin'] * np.random.choice(range(1,6))
                        df['BloodPressure_new'] = df['BloodPressure'] * np.random.choice(range(1,6))
                        df['Glucose_new'] = df['Glucose'] * np.random.choice(range(1,6))
                        df['SkinThickness_new'] = df['SkinThickness'] * np.random.choice(range(1,6))
                        
                        #KPI intergrations
                        Insulin = np.mean(df['Insulin_new'])
                        BloodPressure = np.mean(df['BloodPressure_new'])
                        Glucose = np.mean(df['Glucose_new'])
                        SkinThickness = np.mean(df['SkinThickness_new'])
                        
                        with PlaceHolder.container():
                            KPIA,KPIB,KPIC,KPID = st.columns(4)
                            KPIA.metric(label="Insulin🧪:", value=round(Insulin), delta=round(Insulin) -10)
                            KPIB.metric(label="BloodPressure🩸:", value=round(BloodPressure), delta=round(BloodPressure) -10)
                            KPIC.metric(label="Glucose💊:", value=round(Glucose), delta=round(Glucose) -10)
                            KPID.metric(label="SkinThickness🧬:", value=round(SkinThickness), delta=round(SkinThickness) -10)
                            
                            #Creating charts and graphical displays
                            graph1,graph2 = st.columns(2)
                            with graph1:
                                st.markdown(" ###### Heatmap:")
                                graph1 = px.density_heatmap(data_frame=df, y='Age', x='Pregnancies')
                                st.write(graph1)
                                
                            with graph2:
                                st.markdown(" ###### Area Map:")
                                graph2 = px.area(data_frame=df, y='Age', x='DiabetesPedigreeFunction')
                                st.write(graph2)
                                
                            st.markdown("Tabular Display:")
                            st.dataframe(df)
                            time.sleep(1)
                                                            

            else:
                st.warning("Incorrect username or password.")

    elif Selection == "SignUp":
                st.subheader("Create New Account.")
                new_user = st.text_input("username:")
                new_password = st.text_input("password:", type='password')

                if st.button("SignUp"):
                    create_usertable()
                    add_userdata(new_user, new_password)
                    st.success("Account created successfully.")
                    st.info("👈Now go to the login page.")


    elif Selection == "AboutUs":
            st.subheader("Afya Bora Medical Data Analysis System.")
            st.markdown(
                "This system has been extensively been designed to help medics in the presentation and analysation of both diabetic and non-diabetic patients enabling them make the correct judgments. It has been built with a nicely designed user interface that is easily interactable with. Feel free to use the app accordingly.")
            st.write("Komesha! Ugonjwa wa Sukari.")

            st.write("You can reach as via:")
            st.write("Contact: 0700 495 575.")
            st.write("Email: afyabora@gmail.com")

if __name__ == '__main__':
            main()


