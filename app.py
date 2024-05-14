import streamlit as st
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

def main():
    st.sidebar.markdown("<h1 style='backgrouond-color: #000000; color: #ffffff; font-size: 30px;'>FinovoTech</h1>", unsafe_allow_html = True)
    menu_options = ["Dashboard", "Purchase Order", "Sales", "Invoices", "Taxes", "Expenses"]

    option = st.sidebar.radio("Menu ", menu_options)
    handle_menu_selection(option)


def handle_menu_selection(option):
    if option == "Dashboard":
        show_dashboard()
    elif option == "Purchase Order":
        show_purchase_order()
    elif option == "Sales":
        show_sales()
    elif option == "Invoices":
        show_invoices()
    elif option == "Taxes":
        show_taxes()
    elif option == "Expenses":
        show_expenses()

def total_amount(data):

    amount = 0
    delivered = 0

    for index,row in data.iterrows():
        if row['status'].lower() == 'closed':
            delivered += 1
            amount += row['amount']

    return (amount, delivered)

def total_sales(data):

    sales = 0

    for index,row in data.iterrows():
        sales += int(row['total sales'])

    return sales

def show_purchasing_category(data):

    vendor_group = data.groupby('Vendor')['amount'].sum().reset_index()

    total_purchases = vendor_group['amount'].sum()
    vendor_group['percentage'] = (vendor_group['amount'] / total_purchases) * 100
    vendor_group = vendor_group.sort_values(by='percentage', ascending=False)


    st.markdown("<h6 style='font-size: 20px'>Top Purchases</h6>", unsafe_allow_html=True)
    show_all = st.checkbox('Show All Categories')

    if not show_all:
        top_three = vendor_group.head(3)
        for index, row in top_three.iterrows():
            st.write(row['Vendor'], f"{row['percentage']:.2f}%")
            progress_bar = st.progress(int(row['percentage']))
    else:
        for index, row in vendor_group.iterrows():
            st.write(row['Vendor'], f"{row['percentage']:.2f}%")
            progress_bar = st.progress(int(row['percentage']))

def show_recent_orders(data):
    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')

    data = data.sort_values(by='Date', ascending=False)


    st.markdown("<h6 style='font-size: 20px'>Recent Orders</h6>", unsafe_allow_html=True)
    show_all = st.checkbox('Show All Orders')

    if not show_all:
        top_three = data.head(3)
        for index, row in top_three.iterrows():
            st.markdown(f"<div style='display: flex; flex-direction: row; justify-content: between;'><div style='display: flex; flex-direction: column; justify-content: start;'><div style='font-size: 17px'>{row['purchase order']}</div><h6 style='font-size: 14px'>{row['Date'].strftime('%Y-%m-%d')}</h6></div><div>${row['amount']}</div></div>", unsafe_allow_html = True)
    else:
        for index, row in data.iterrows():
            st.markdown(f"<div style='display: flex; flex-direction: row; justify-content: between;'><div style='display: flex; flex-direction: column; justify-content: start;'><div style='font-size: 17px'>{row['purchase order']}</div><h6 style='font-size: 14px'>{row['Date'].strftime('%Y-%m-%d')}</h6></div><div>${row['amount']}</div></div>", unsafe_allow_html = True)

def show_product_selling(data):

    st.markdown("<h6 style='font-size: 20px'>Product Selling</h6>", unsafe_allow_html=True)

    show_all = st.checkbox('Show All')

    if not show_all:
        top_three = data.head(3)
        st.table(top_three)
    else:
        st.table(data)

def show_selling_category(data):
    product_group = data.groupby('product name')['total sales'].sum().reset_index()

    total_sales_all_products = product_group['total sales'].sum()
    product_group['percentage'] = (product_group['total sales'] / total_sales_all_products) * 100
    product_group = product_group.sort_values(by='percentage', ascending=False)

    st.markdown("<h6 style='font-size: 20px'>Top Selling Products</h6>", unsafe_allow_html=True)

    show_all = st.checkbox('Show All Products')

    if not show_all:
        top_three = product_group.head(3)
        for index, row in top_three.iterrows():
            st.write(row['product name'], f"{row['percentage']:.2f}%")
            progress_bar = st.progress(int(row['percentage']))
    else:
        for index, row in product_group.iterrows():
            st.write(row['product name'], f"{row['percentage']:.2f}%")
            progress_bar = st.progress(int(row['percentage']))

def show_purchase_order():
    
    columns = st.columns([6,1])
    
    columns[0].markdown("<h1 style='color: #ffffff; font-size: 30px; margin-top: -20px'>Purchase Order</h1>", unsafe_allow_html = True)

    st.write("")
    st.write("")

    if 'fl' not in st.session_state:
        st.session_state.fl = True

    if columns[1].button("Add New"):
        st.session_state.fl = not st.session_state.fl

    if not st.session_state.fl:
        
        row_1 = st.columns(2)

        with row_1[0]:
            date = st.date_input("Date")
        with row_1[1]:
            po_number = st.text_input("Purchase Order Number")

        row_2 = st.columns(2)

        with row_2[0]:
            vendor = st.text_input("Vendor")
        with row_2[1]:
            delivery_date = st.date_input("Delivery Date")
    
        row_3 = st.columns(2)

        with row_3[0]:
            status = st.selectbox("Status", ["Draft", "Closed" , "In Progress", "On Hold"], None)
        with row_3[1]:
            amount = st.number_input("Amount")
    
        st.write("")

        year, month, day = str(date).split('-')
        date = f"{day}/{month}/{year}"

        year, month, day = str(delivery_date).split('-')
        delivery_date = f"{day}/{month}/{year}"

        new_data = {}
        with st.columns(5)[2]:
            if st.button("Submit", use_container_width = True):
                new_data = {
                    "Date": date,
                    "purchase order": po_number,
                    "Vendor": vendor,
                    "delivery date": delivery_date,
                    "status": status,
                    "amount": amount
                }

                with open("PurchaseOrder.csv", "a", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=new_data.keys())
                    writer.writerow(new_data)

    else:
        data = pd.read_csv('./PurchaseOrder.csv')
        st.write(data)

def show_purchase_status(data):

    st.subheader('Status Distribution')
    status_counts = data['status'].value_counts()

    fig_status, ax_status = plt.subplots(figsize=(5, 5))
    ax_status.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', startangle=140)
    ax_status.axis('equal')
    st.pyplot(fig_status)
    plt.close(fig_status)

def show_stock_status(data):

    status_counts = data['status'].value_counts()

    st.subheader('Status Distribution')

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(status_counts.index, status_counts.values, color='skyblue')
    ax.set_xlabel('Status')
    ax.set_ylabel('Count')
    ax.set_title('Status Distribution')
    ax.tick_params(axis='x', rotation=45) 
    plt.tight_layout() 
    st.pyplot(fig)
    plt.close(fig)

def show_dashboard():
    st.markdown("<h1 style='color: #ffffff; font-size: 30px;'>DashBoard</h1>", unsafe_allow_html = True)

    warnings.filterwarnings("ignore", category=UserWarning)

    data = pd.read_csv('./PurchaseOrder.csv')
    sales = pd.read_csv('./Sales.csv')

    sales_amount = total_sales(sales)
    amount,delivered = total_amount(data)

    row_1 = st.columns(3)

    with row_1[0]:
        st.error(f"Total Sales \n\n {sales_amount}")

    with row_1[1]:
        st.info(f"Total Purchase Amount \n\n {amount}")

    with row_1[2]:
        st.success(f"Total Delivered \n\n {delivered}")

    with st.columns([1,5,1])[1]:
        show_purchase_status(data)

    with st.columns([1,5,1])[1]:
        show_stock_status(sales)

def show_sales():
    st.markdown("<h1 style='color: #ffffff; font-size: 40px;'>Sales</h1>", unsafe_allow_html = True)
    
    purchases = pd.read_csv('./PurchaseOrder.csv')
    sales = pd.read_csv('./Sales.csv')

    sales_count = total_sales(sales)

    with st.columns(3)[0]:
        st.warning(f"Total Sales \n\n {sales_count}")

    st.write("")
    st.write("")

    with st.columns([2,1])[0]:
        show_purchasing_category(purchases)

    st.write("")
    st.write("")
    
    show_product_selling(sales)

    row = st.columns([1,2])

    with row[0]:
        show_recent_orders(purchases)
    
    with row[1]:
        show_selling_category(sales)

def show_invoices():
    st.markdown("<h1 style='color: #ffffff; font-size: 40px;'>Invoices</h1>", unsafe_allow_html = True)
    
    invoices = pd.read_csv('./Invoices.csv')

    st.table(invoices)

def show_taxes():
    st.markdown("<h1 style='color: #ffffff; font-size: 40px;'>Taxes</h1>", unsafe_allow_html = True)
    st.write("This is the taxes section.")

def show_expenses():
    st.markdown("<h1 style='color: #ffffff; font-size: 40px;'>Expenses</h1>", unsafe_allow_html = True)
    st.write("This is the expenses section.")

if __name__ == "__main__":
    main()
