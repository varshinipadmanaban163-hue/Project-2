#SQLAlchemy
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, URL

df = pd.read_csv("project2_fd_clean.csv")

connection_url = URL.create(
    "mysql+pymysql",
    username="root",
    password={password},
    host="localhost",
    database="food_delivery_db"
)

engine = create_engine(  "mysql+pymysql://root:{Password}@localhost:3306/food_delivery_db")

print("MySQL connection created")

df.to_sql(
    name="fooddelivery",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data inserted successfully") ;

### SQL Queries
queries= {
    '1. Identify top-spending Customer':"""
    select Customer_ID , sum(Final_Amount) as top_spending from fooddelivery
    group by Customer_ID 
    order by sum(Final_Amount) desc limit 10;""",

    '2.Analyze age group vs order group':"""
     select Customer_Age_Group, SUM(Order_Value) from fooddelivery 
     group by Customer_Age_Group  order by SUM(Order_Value) desc ;
     """,


    '3.Weekend vs Weekday order pattern':"""
    select  count(*), Order_Day from fooddelivery group by Order_Day;
    """,
    
    '4 . Monthly of revenge trend':"""
    select sum(Order_Value) as total_revenue , month from fooddelivery 
    group by month order by total_revenue desc;""",

    '5 . Impact of discount on profit':"""
    select Discount_Applied , count(*) as total_orders ,round(avg(Profit_Margin),2) as ave_profit_margin from fooddelivery 
    group by Discount_Applied order by Discount_Applied desc;  
    """,
    '6 . High-revenue cities and cuisines':"""
    select City , Cuisine_Type , sum(Order_Value) as total_revenue from fooddelivery
    group by city , Cuisine_Type order by total_revenue desc;
    """,
    '7 . Average delivery time by  city ':"""
    select round(avg(Delivery_Time_Min),2) as avg_Delivery_time  , city from fooddelivery 
    group by city  order by  avg_Delivery_time desc;""",

    '8. Distance vs delivery delay analysis':"""
    select case when Distance_km < 5 then "0-5" WHEN Distance_km < 10 then "5-10" 
    when Distance_km < 15 then "10- 15" else "15+" end as distance_range,
    round(avg(Delivery_Time_Min),2) as avg_delivery_time from fooddelivery group by distance_range
    order by avg_delivery_time  desc ;""",
    
    '9.Delivery rating vs delivery time':"""
    select Delivery_Rating ,round(avg(Delivery_Time_Min),2) as avg_delivery_time from fooddelivery group by Delivery_Rating
    order by avg_delivery_time desc;""",
    
    '10.Top-Rated Restaurants':"""
    select Restaurant_Name , round(avg(Restaurant_Rating),2) as avg_restaurant_rating from fooddelivery
    group by Restaurant_Name order by avg_restaurant_rating desc;""",

    '11.Cancellation rate by restaurant':"""
    select Restaurant_Name , avg( case  when Order_Status= "Cancelled" then 1 else 0 end ) *100 AS cancellation_rate  from fooddelivery 
    group by Restaurant_Name order by  cancellation_rate  desc limit 10;""",

    '12 . Cuisine-wise Performance':"""
    select Cuisine_Type , sum (Final_Amount) as revenue from fooddelivery
    group by Cuisine_Type  order  by  sum(Final_Amount) desc;""",

    '13 .Peak hour demand analysis':"""
    select case when Peak_Hour = 1 then "Peak_hour" else "Non-peak_hour " end as  peak_hour_status,
    count(*) as total_orders from fooddelivery 
    group by peak_hour_status order by total_orders;""",

    '14 .Payment mode preference':"""
    select Payment_Mode, count(*) as total_orders from fooddelivery
    group by  Payment_mode order by  total_orders desc;""",

    '15. Cancellation reason analysis':"""
    select cancellation_reason , count(*) as total_orders from fooddelivery
    group by  cancellation_reason;""",

    '16. Total orders':"""
    select count(*) as total_orders from fooddelivery;
    """,
    '17. Total_revenue':"""
    select sum(Final_Amount) as Total_revenue from fooddelivery;
    """,

    '18. Average Order Value':"""
    select avg(Order_Value) as  average_order_value from fooddelivery;""",

   '19. Average Delivery time':"""
   select avg(Delivery_Time_Min) as avg_delivery_time from fooddelivery;""",

   '20. Cancellation rate':"""
   select avg( case  when Order_Status= "Cancelled" then 1 else 0 end ) *100 AS cancellation_rate  from fooddelivery ;
   """,

   '21. Average Delivery Rating':"""
   select avg(Delivery_Rating)  as average_delivery_rating from fooddelivery;""",

   '22. Profit Margin %':"""
   select avg(Profit_Margin_Percentage) as profit_margin from fooddelivery;"""
}

#streamlit


st.title("Online Food Delivery Analysis Dashboard")
st.write("Select any problem to run")

task = st.selectbox("Choose task number", list(queries.keys()))

if st.button("Run Query"):
    query = queries[task]
    df = pd.read_sql(query, engine)
    st.subheader(f"Results for: {task}")
    st.dataframe(df,width= 'stretch')
