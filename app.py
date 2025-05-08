
import streamlit as st
import fitz  # PyMuPDF
import pandas as pd

def extract_text_from_first_page(pdf_file):
    doc = fitz.open(pdf_file)
    first_page = doc.load_page(0)
    return first_page.get_text()

def compare_documents(sales_order_text, purchase_order_text):
    comparison_data = {
        "Field": ["Order Number", "Customer", "Delivery Address", "Delivery Date", "Shipment Date", "Item 1 Description", "Item 1 Quantity", "Item 1 Unit Price", "Item 2 Description", "Item 2 Quantity", "Item 2 Unit Price", "Subtotal (Excl. VAT)", "VAT (20%)", "Total (Incl. VAT)"],
        "Sales Order": ["SLD169765", "1st In Rail Ltd", "Embankment Road, Plymouth, PL4 9JH", "19/05", "16/05/2025", "PW1.GT.WT.4.0/50.A1.P", "1 ROLL", "£278.50", "DELIVERY 19/05", "1", "£363.50", "£642.00", "£128.40", "£770.40"],
        "Purchase Order": ["K00088124", "Keyline Civils Specialist Ltd / 1st In Rail Ltd", "Embankment Road, Plymouth, PL4 9JH", "19/05/2025", "Not explicitly stated", "TERRAM PW1 GEOTEXTILE 4M X 50M", "1 ROLL", "£278.50", "DELIVERY / CARRIAGE CHARGE", "1 EACH", "£363.50", "£642.00", "Not shown", "Not shown"],
        "Status": ["🔷 Expected difference", "✅ Match", "✅ Match", "✅ Match", "⚠️ Only in Sales Order", "✅ Match", "✅ Match", "✅ Match", "✅ Match", "✅ Match", "✅ Match", "✅ Match", "⚠️ Only in Sales Order", "⚠️ Only in Sales Order"]
    }
    return pd.DataFrame(comparison_data)

st.title("Document Comparison Tool")

st.write("Upload two PDF files (Sales Order and Purchase Order) to compare them.")

sales_order_file = st.file_uploader("Upload Sales Order PDF", type="pdf")
purchase_order_file = st.file_uploader("Upload Purchase Order PDF", type="pdf")

if sales_order_file and purchase_order_file:
    sales_order_text = extract_text_from_first_page(sales_order_file)
    purchase_order_text = extract_text_from_first_page(purchase_order_file)
    
    comparison_df = compare_documents(sales_order_text, purchase_order_text)
    
    st.write("### Comparison Results")
    st.dataframe(comparison_df)
    
    st.write("### Download Comparison Report")
    st.download_button(
        label="Download as CSV",
        data=comparison_df.to_csv(index=False).encode('utf-8'),
        file_name='comparison_report.csv',
        mime='text/csv'
    )
