"""Tests for import_to_seekdb module."""
import pandas as pd


from import_to_seekdb import read_file, import_to_seekdb,client


def test_read_csv_file(tmp_path):
    """Test reading a valid CSV file."""
    # Create a temporary CSV file
    csv_file = tmp_path / "test_data.csv"
    csv_content = "Name,Age,City\nAlice,30,Beijing\nBob,25,Shanghai\n"
    csv_file.write_text(csv_content)

    # Read the file
    df = read_file(str(csv_file))

    # Verify
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["Name", "Age", "City"]
    assert df.iloc[0]["Name"] == "Alice"
    assert df.iloc[0]["Age"] == 30
    assert df.iloc[1]["City"] == "Shanghai"


def test_read_xlsx_file(tmp_path):
    """Test reading a valid Excel (.xlsx) file."""
    # Create a temporary Excel file
    xlsx_file = tmp_path / "test_data.xlsx"
    df_original = pd.DataFrame({
        "Product": ["Laptop", "Phone", "Tablet"],
        "Price": [1000, 800, 500],
        "Stock": [10, 25, 15]
    })
    df_original.to_excel(str(xlsx_file), index=False)

    # Read the file
    df = read_file(str(xlsx_file))

    # Verify
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == ["Product", "Price", "Stock"]
    assert df.iloc[0]["Product"] == "Laptop"
    assert df.iloc[1]["Price"] == 800


def test_import_to_seekdb(tmp_path):
    # Create a temporary CSV file
    csv_file = tmp_path / "mobiles.csv"
    column_name = "Name,Brand,Selling Price,MRP,Discount,Ratings,No_of_ratings,Details\n"
    # Each row must be on a single line - no embedded newlines in CSV data
    rowOne = "SAMSUNG Galaxy F13 (Waterfall Blue 64 GB),SAMSUNG,11999,14999,20% off,4.4,101958 Ratings & 5654 Reviews,\"['4 GB RAM | 64 GB ROM | Expandable Upto 1 TB' '16.76 cm (6.6 inch) Full HD+ Display' '50MP + 5MP + 2MP | 8MP Front Camera' '6000 mAh Lithium Ion Battery' 'Exynos 850 Processor' '1 Year Warranty Provided By the Manufacturer from Date of Purchase']\"\n"
    rowTwo = "REDMI 9i Sport (Coral Green 64 GB),REDMI,7099,9999,29% off,4.3,195377 Ratings & 11204 Reviews,\"['4 GB RAM | 64 GB ROM | Expandable Upto 512 GB' '16.59 cm (6.53 inch) HD+ Display' '13MP Rear Camera | 5MP Front Camera' '5000 mAh Li-Polymer Battery' 'MediaTek Helio G25 Processor' 'Brand Warranty of 1 Year Available for Mobile and 6 Months for Accessories']\"\n"
    csv_file.write_text(column_name + rowOne + rowTwo)
    file_path = str(csv_file)
    vectorize_column = "Details"
    collection_name = "mobiles"
    if(client.has_collection(collection_name)):
        client.delete_collection(collection_name)
    inserted_collection_name, count = import_to_seekdb(
        file_path, vectorize_column, collection_name)
    assert inserted_collection_name == collection_name
    assert count == 2
