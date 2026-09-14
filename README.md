🛍️ Customer Purchase Behavior & Retail Sales Analytics Dashboard
An end-to-end data analytics and business intelligence solution evaluating retail transactions, calculating **RFM (Recency, Frequency, Monetary) Customer Segmentation**, and visualizing customer lifetime value trends through an interactive Streamlit web dashboard.
🔗 **Live Interactive Dashboard: https://customer-behavior-analytics-dashboard-3kccrlwtshsytk9mbbovz9.streamlit.app/ 
📁 **Exploratory Data Analysis Notebook:`Customer_Purchase_Analysis.ipynb`

📌 Project Overview & Objectives
Data Cleansing & Preprocessing: Cleaned 500k+ transaction records by handling null CustomerIDs, eliminating negative quantities/unit prices, and deduplicating records.
RFM Customer Segmentation: Classified 4,300+ unique customers into 5 business segments (Champions, Loyal, Potential, At Risk, One-Time).
Exploratory & Cohort Analysis: Uncovered sales seasonality, top revenue-generating SKUs, and international market opportunities outside the UK.
Interactive Web Application: Built and deployed a Streamlit dashboard with real-time sidebar filters, dynamic KPI metrics, and Plotly visual distributions.

💡 Key Business Insights
 The Pareto Principle (80/20 Rule):
 **Top 30.36% (Champions)** drive **73.01% of total revenue** (~₹6.48M) with an average of 9+ orders per customer.
 **18.05% of customers (At Risk)** have high historical value but haven't repurchased recently, locking up ₹576K+ in potential lost revenue.
 **Holiday Seasonality Spike:** Sales volume surged significantly starting September, reaching a record peak in **November 2011 (~₹1.5M revenue)** driven by festive retail preparation.
 **Product Discrepancy (Volume vs Value):**  Certain SKUs (like `PAPER CRAFT, LITTLE BIRDIE`) generated massive volume and revenue, while items like `DOTCOM POSTAGE` represented high monetary fees with low order unit volume.
 **Global Footprint:** Netherlands, EIRE (Ireland), and Germany emerged as top international revenue markets outside the United Kingdom.

🛠️ Tech Stack & Tools
Programming & Analytics:Python, Pandas, NumPy
Data Visualization:Plotly Express, Matplotlib
Dashboard & Deployment: Streamlit Community Cloud
Environment: Jupyter Notebook, Git, GitHub

🚀 How to Run Locally
1. Clone this repository:
   ```bash
   git clone [https://github.com/Sathana0511/customer-behavior-analytics-dashboard.git](https://github.com/Sathana0511/customer-behavior-analytics-dashboard.git)
