import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Buka dan baca dataset yang digunakan
orders_df = pd.read_csv('olist_orders_dataset.csv')
order_items_df = pd.read_csv('olist_order_items_dataset.csv')
customers_df = pd.read_csv('olist_customers_dataset.csv')

# Merge data
merged_df = order_items_df.merge(orders_df, on='order_id').merge(customers_df, on='customer_id')

# Apa saja produk terlaris yang dijual ?
def plot_top_selling_products():
    top_categories = merged_df['product_id'].value_counts().head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_categories.values, y=top_categories.index, palette='viridis')
    plt.title('10 Produk Terlaris')
    plt.xlabel('Jumlah Penjualan')
    plt.ylabel('Product ID')
    st.pyplot(plt)

# Bagaimana tren pengembalian produk dalam dataset ini?
def plot_return_trends():
    returns_summary = merged_df[merged_df['order_status'].isin(['canceled', 'unavailable'])].groupby('product_category_name')['order_id'].count().reset_index()
    returns_summary.columns = ['product_category_name', 'returned_count']
    
    total_sales = merged_df['product_category_name'].value_counts().reset_index()
    total_sales.columns = ['product_category_name', 'total_sales']
    
    returns_summary = returns_summary.merge(total_sales, on='product_category_name')
    returns_summary['return_percentage'] = (returns_summary['returned_count'] / returns_summary['total_sales']) * 100

    plt.figure(figsize=(12, 6))
    sns.barplot(x='return_percentage', y='product_category_name', data=returns_summary, palette='viridis')
    plt.title('Persentase Pengembalian Produk per Kategori')
    plt.xlabel('Persentase Pengembalian (%)')
    plt.ylabel('Kategori Produk')
    st.pyplot(plt)

# Bagaimana distribusi order status untuk setiap states pelanggan ?
def plot_order_status_distribution():
    order_status_count = merged_df['order_status'].value_counts()
    plt.figure(figsize=(12, 6))
    sns.barplot(x=order_status_count.index, y=order_status_count.values, palette='viridis')
    plt.title('Distribusi Status Pesanan')
    plt.xlabel('Status Pesanan')
    plt.ylabel('Jumlah Pesanan')
    st.pyplot(plt)

# Tampilan dashboard
st.title('Dashboard Analisis Data')
st.sidebar.header('Pilih Grafik untuk Ditampilkan')
option = st.sidebar.selectbox('Pilih Analisis', ['Produk Terlaris', 'Tren Pengembalian Produk', 'Distribusi Order Status'])

if option == 'Produk Terlaris':
    plot_top_selling_products()
elif option == 'Tren Pengembalian Produk':
    plot_return_trends()
elif option == 'Distribusi Order Status':
    plot_order_status_distribution()
