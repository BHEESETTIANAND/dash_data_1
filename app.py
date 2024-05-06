import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import plotly.figure_factory as ff
from streamlit_option_menu import option_menu

st.set_page_config("wide")
st.title("Exploratory Data Analysis ")

selected=option_menu("Main menu",["📊Data Visualization📈","Insights🔍","👀 Actions"],orientation="horizontal")

if selected=="📊Data Visualization📈":
    
    col1, col2 = st.columns(2,gap="large")

    categoricals = ['ReserveStatus','Gender','From','To','Domestic','TripReason','Vehicle','Cancel']
    numericals = ['Price','CouponDiscount']



    null_data=pd.read_csv("null_data.csv")
    cancel=pd.read_csv("cancel_count.csv")
    df=pd.read_csv("eda.csv")
    top10dep=pd.read_csv("top10dep.csv")
    top10des=pd.read_csv("top10to.csv")
    moninc=pd.read_csv("monthincome.csv")
    incdis=pd.read_csv("incwithoutdis.csv")
    daysdiff=pd.read_csv("daysdiff.csv")
    top10can=pd.read_csv("top10can.csv")
    canmon=pd.read_csv("cancelpermon.csv")

    with col1:
        fig = px.pie(null_data, values='missing_value', names='feature', title='Percentage of Null Values in Each Column',hole=0.6)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)




    with col2:
        fig = px.pie(cancel, values='Count', names='Cancel', title='Cancellation percentage of customers',
                hole=0.6)  # Set hole parameter to 0.4 for a donut chart
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)


    with col1:
        fig = px.box(y=numericals[0], data_frame=df,title="boxplot of Price")
        plt.tight_layout()
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig = px.box(y=numericals[1], data_frame=df,title="boxplot of Coupon discount")
        plt.tight_layout()
        st.plotly_chart(fig,use_container_width=True)


    features = ['ReserveStatus', 'Gender', 'Price', 'CouponDiscount', 'Domestic', 'TripReason', 'Cancel', 'From_encoded', 'To_encoded']

    # with col1:
    #     sns.kdeplot(data=df['ReserveStatus'], color='red')
    #     plt.title('ReserveStatus KDE Plot')
    #     plt.xlabel('Value')
    #     plt.ylabel('Density')

    # # Display the Seaborn plot in Streamlit
    #     st.pyplot(plt)

    with col1:
        fig=px.bar(top10dep,x='From',y="count",title="top 10 depatured cities")
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig=px.bar(top10des,x='To',y="size",title="top 10 destination cities")
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        fig=px.line(moninc,x="Created",y="Income",title="monthly income ")
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig=px.line(incdis,x="Created",y="Income",title="monthly income without cancellation ")
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        st.markdown("comparison of monthly incomes")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=moninc["Created"], y=moninc["Income"], mode='lines', name='monthly income'))
        fig.add_trace(go.Scatter(x=incdis["Created"], y=incdis["Income"], mode='lines', name="moninc without canc"))
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig=px.bar(data_frame=daysdiff,x="Days_Difference",y="count",title="gap between booking and depature")
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        #sns.countplot(data=df,x='TripReason',hue='Cancel')
        #st.pyplot(plt)
        fig = px.histogram(df, x='TripReason', color='Cancel',marginal="box", barmode='group',title="relation b/w cancellation and tripreason")
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig = px.histogram(df, x='Vehicle', color='Cancel',marginal="box", barmode='group',title="relation b/w vehicle and cancellation")
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        fig = px.histogram(df, x='Gender', color='Cancel',marginal="box", barmode='group',title="relation b/w gender and cancellation")
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        df['DepartureTime'] = pd.to_datetime(df['DepartureTime'])

    # Extract month from 'DepartureTime'
        df['DepartureMonth'] = df['DepartureTime'].dt.month
        fig = px.histogram(df, x='DepartureMonth', color='Cancel',marginal="box", barmode='group',title="relation b/w Depature month and cancellation")
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        fig=px.bar(top10can,x='To',y="cancel_count",title="top 10 cancelled cities")
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig=px.scatter(df,x="Price",y="Cancel",title="relation b/w cancel and price")
        st.plotly_chart(fig,use_container_width=True)


    with col1:
        fig=px.scatter(df,x="CouponDiscount",y="Cancel",title="relation b/w cancel and price")
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        st.write("Price CouponDisc")
        fig = go.Figure(go.Scattergl(
        x = df['Price'],
        y = df['CouponDiscount'],
        mode = 'markers',
        marker=dict(color='rgba(0, 0, 0, 0.3)'),
        text=df['Cancel'],
        hoverinfo='text',
        ))
        fig.update_traces(marker=dict(size=5, line=dict(width=0.5, color='white')), selector=dict(mode='markers'))
        plt.xlabel("Price")
        plt.ylabel("CouponDiscount")
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        grouped_data = df.groupby(['Gender', 'Vehicle']).size().reset_index(name='Count')

    # Create a stacked bar plot with Plotly Express
        fig = px.bar(grouped_data, x='Gender', y='Count', color='Vehicle',
                title='Stacked Bar Plot of Gender vs Vehicle', barmode='stack')
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        grouped_data = df.groupby(['Cancel', 'Vehicle']).size().reset_index(name='Count')

    # Create a stacked bar plot with Plotly Express
        fig = px.bar(grouped_data, x='Cancel', y='Count', color='Vehicle',
                title='Stacked Bar Plot of Cancel vs Vehicle', barmode='stack')
        st.plotly_chart(fig,use_container_width=True)

    with col1:
        grouped_data = df.groupby(['Cancel', 'TripReason']).size().reset_index(name='Count')

    # Create a stacked bar plot with Plotly Express
        fig = px.bar(grouped_data, x='Cancel', y='Count', color='TripReason',
                title='Stacked Bar Plot of Cancel vs Tripreason', barmode='stack')
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        grouped_data = df.groupby(['Cancel', 'Domestic']).size().reset_index(name='Count')

    # Create a stacked bar plot with Plotly Express
        fig = px.bar(grouped_data, x='Cancel', y='Count', color='Domestic',
                title='Stacked Bar Plot of Cancel vs Domestic', barmode='stack')
        st.plotly_chart(fig,use_container_width=True)


    st.header("Distribution of each features")



    features = ['ReserveStatus','Gender','Price','CouponDiscount','Domestic','TripReason','Cancel','From_encoded','To_encoded']
    plt.figure(figsize=(10,50))
    for i in range (0,len(features)):
        plt.subplot(20,2,i+1)
        sns.histplot(data=df,x=df[features[i]],kde=True)
    plt.tight_layout()
    st.pyplot(plt)

if selected=="Insights🔍":
    st.header("🔍Insights gained from the above plots📊📈")
    st.write("1. Most of the customers approx(85%) are not cancelling their tickets")
    st.write("2. The top 10 cities from which more customers are departuring from")
    st.markdown("""
                -> i. Tehran,
                -> ii. Mashhad,
                -> iii. Isfahan,
                -> iv. Shiraz,
                -> v. Yazd,
                -> vi. Mashhad (Greater Khorasan),
                -> vii. Ahvaz,
                -> viii. Kerman,
                ->ix. Qom,
                ->x. Bandar Abbas""" )
    st.write("3. The top 10 destination cities to which more customers are travelling are")
    st.markdown("""
                -> i. Tehran,
                -> ii. Mashhad,
                -> iii. Isfahan,
                -> iv. Shiraz,
                -> v. Yazd,
                -> vi. Qom,
                -> vii. Mashhad (Greater Khorasan),
                -> viii. Ahvaz,
                ->ix. Kerman,
                ->x. Tabriz""")
    st.write("4. We are having less income during the months february to July")
    st.write("5. we rea high income during the months August to November")
    st.write("6. The trend of income is increasing with months from february to November")
    st.write("7. The trend of income is decreasing from the month December to January")
    st.write("8. Most of the customers are booking the tickets and departuring on the same day")
    st.write("9. Most of the customers are travelling for there work purposes")
    st.write("10. Most of the customers prefer to travel on Bus and Train")
    st.write("11. Most of the customers who are travelling are Males")
    st.write("12. Most of the customers depature in months of August,September and November")
    st.write("13. Most of the customers who booked there tickets to Tehran are cancelling their tickets")


if selected=="👀 Actions":
    st.header("👀 Actions that can be taken to reduce the risk of ticket Cancellation and to increase Sales from the above Insights🖊️🔄")
    st.write("**1. Optimize Pricing Strategies**: Offer promotions or discounts during periods of low income(in the months of December,january) to stimulate demand and increase sales")
    st.write("""**2. Provide Incentives for Non-Cancellation:** Offering incentives or rewards for customers who do not cancel their tickets, such as loyalty points, discounts on future bookings, or exclusive offers.
            Rewarding loyal customers can help incentivize them to honor their bookings and reduce the *risk of cancellations*.""")
    st.write("""**3. Target female customers with special offers:** As the Female customers are travelling less we can offer the female customers some special offers so that they will get
            attracted and book tickets, so that our sales may increase""")
    st.write("""**4. Increase Offered Services in High-Departure Cities:** We have increase the number of offered services from the places where there are more customer depatures""")
    st.write("""**5. Reduce Services in Cities with High Cancellation Rates:** Identify the cities to which most of the customers are cancelling their tickets and reduce the number of services
             offered to that cities, so that ticket cancellation risk can be reduced""")
    







    

