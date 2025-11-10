"""
Demo: Basic DataComPy Usage
Learn how datacompy works with simple examples
"""
import pandas as pd
import datacompy


def demo_1_perfect_match():
    """Demo 1: Two identical DataFrames"""
    print("\n" + "="*80)
    print("DEMO 1: Perfect Match - Identical DataFrames")
    print("="*80 + "\n")
    
    # Create two identical DataFrames
    df1 = pd.DataFrame({
        'ID': [1, 2, 3],
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Amount': [100.50, 200.75, 150.25]
    })
    
    df2 = df1.copy()  # Exact copy
    
    print("DataFrame 1 (Excel):")
    print(df1)
    print("\nDataFrame 2 (CSV):")
    print(df2)
    
    # Compare using datacompy
    compare = datacompy.Compare(
        df1=df1,
        df2=df2,
        join_columns=['ID'],
        df1_name='Excel',
        df2_name='CSV'
    )
    
    print("\n" + "-"*80)
    print("DataComPy Report:")
    print("-"*80)
    print(compare.report())
    
    if compare.matches():
        print("✅ Result: DataFrames are IDENTICAL!")


def demo_2_value_differences():
    """Demo 2: Same structure, different values"""
    print("\n" + "="*80)
    print("DEMO 2: Value Differences - Same rows, different amounts")
    print("="*80 + "\n")
    
    df1 = pd.DataFrame({
        'ID': [1, 2, 3],
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Amount': [100.50, 200.75, 150.25]
    })
    
    df2 = pd.DataFrame({
        'ID': [1, 2, 3],
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Amount': [100.55, 200.75, 150.30]  # Different amounts for ID 1 and 3
    })
    
    print("Excel Data:")
    print(df1)
    print("\nCSV Data:")
    print(df2)
    
    compare = datacompy.Compare(
        df1=df1,
        df2=df2,
        join_columns=['ID'],
        abs_tol=0.01,  # Tolerance of 0.01 (1 cent)
        df1_name='Excel',
        df2_name='CSV'
    )
    
    print("\n" + "-"*80)
    print("DataComPy Report:")
    print("-"*80)
    print(compare.report())
    
    print("\n" + "-"*80)
    print("Detailed Mismatches:")
    print("-"*80)
    print(compare.all_mismatch())


def demo_3_missing_rows():
    """Demo 3: Different rows in each DataFrame"""
    print("\n" + "="*80)
    print("DEMO 3: Missing Rows - Different data in each file")
    print("="*80 + "\n")
    
    df1 = pd.DataFrame({
        'ID': [1, 2, 3, 4],
        'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor'],
        'Price': [999.99, 25.50, 75.00, 299.99]
    })
    
    df2 = pd.DataFrame({
        'ID': [1, 2, 3, 5],  # Has ID 5 instead of ID 4
        'Product': ['Laptop', 'Mouse', 'Keyboard', 'Headphones'],
        'Price': [999.99, 25.50, 75.00, 89.99]
    })
    
    print("Excel Data:")
    print(df1)
    print("\nCSV Data:")
    print(df2)
    
    compare = datacompy.Compare(
        df1=df1,
        df2=df2,
        join_columns=['ID'],
        df1_name='Excel',
        df2_name='CSV'
    )
    
    print("\n" + "-"*80)
    print("DataComPy Report:")
    print("-"*80)
    print(compare.report())
    
    print("\n" + "-"*80)
    print("Rows only in Excel:")
    print("-"*80)
    print(compare.df1_unq_rows)
    
    print("\n" + "-"*80)
    print("Rows only in CSV:")
    print("-"*80)
    print(compare.df2_unq_rows)


def demo_4_column_differences():
    """Demo 4: Different columns"""
    print("\n" + "="*80)
    print("DEMO 4: Column Differences - Extra columns in one file")
    print("="*80 + "\n")
    
    df1 = pd.DataFrame({
        'ID': [1, 2, 3],
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Amount': [100, 200, 150],
        'ExtraColumnInExcel': ['A', 'B', 'C']
    })
    
    df2 = pd.DataFrame({
        'ID': [1, 2, 3],
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Amount': [100, 200, 150],
        'ExtraColumnInCSV': ['X', 'Y', 'Z']
    })
    
    print("Excel Data:")
    print(df1)
    print("\nCSV Data:")
    print(df2)
    
    compare = datacompy.Compare(
        df1=df1,
        df2=df2,
        join_columns=['ID'],
        df1_name='Excel',
        df2_name='CSV'
    )
    
    print("\n" + "-"*80)
    print("DataComPy Report:")
    print("-"*80)
    print(compare.report())


def demo_5_numeric_tolerance():
    """Demo 5: Numeric tolerance handling"""
    print("\n" + "="*80)
    print("DEMO 5: Numeric Tolerance - Small differences ignored")
    print("="*80 + "\n")
    
    df1 = pd.DataFrame({
        'ID': [1, 2, 3],
        'Amount': [100.001, 200.002, 150.003]
    })
    
    df2 = pd.DataFrame({
        'ID': [1, 2, 3],
        'Amount': [100.002, 200.003, 150.004]  # Very small differences
    })
    
    print("Excel Data:")
    print(df1)
    print("\nCSV Data:")
    print(df2)
    
    # Without tolerance
    print("\n" + "-"*80)
    print("WITHOUT Tolerance (abs_tol=0):")
    print("-"*80)
    compare_strict = datacompy.Compare(
        df1=df1,
        df2=df2,
        join_columns=['ID'],
        abs_tol=0,  # No tolerance
        df1_name='Excel',
        df2_name='CSV'
    )
    print(f"Matches: {compare_strict.matches()}")
    
    # With tolerance
    print("\n" + "-"*80)
    print("WITH Tolerance (abs_tol=0.01):")
    print("-"*80)
    compare_tolerant = datacompy.Compare(
        df1=df1,
        df2=df2,
        join_columns=['ID'],
        abs_tol=0.01,  # Tolerance of 0.01
        df1_name='Excel',
        df2_name='CSV'
    )
    print(f"Matches: {compare_tolerant.matches()}")
    print("\n✅ Small differences ignored with tolerance!")


def demo_6_column_statistics():
    """Demo 6: Get detailed column statistics"""
    print("\n" + "="*80)
    print("DEMO 6: Column Statistics - Detailed match rates per column")
    print("="*80 + "\n")
    
    df1 = pd.DataFrame({
        'ID': [1, 2, 3, 4, 5],
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Score': [95, 87, 92, 78, 88],
        'Grade': ['A', 'B', 'A', 'C', 'B']
    })
    
    df2 = pd.DataFrame({
        'ID': [1, 2, 3, 4, 5],
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Score': [95, 90, 92, 78, 85],  # 2 differences in Score
        'Grade': ['A', 'B', 'A', 'B', 'B']  # 1 difference in Grade
    })
    
    print("Excel Data:")
    print(df1)
    print("\nCSV Data:")
    print(df2)
    
    compare = datacompy.Compare(
        df1=df1,
        df2=df2,
        join_columns=['ID'],
        df1_name='Excel',
        df2_name='CSV'
    )
    
    print("\n" + "-"*80)
    print("Column Statistics:")
    print("-"*80)
    stats_df = pd.DataFrame(compare.column_stats)
    print(stats_df)
    
    print("\n" + "-"*80)
    print("Summary:")
    print("-"*80)
    for stat in compare.column_stats:
        col = stat['column']
        unequal = stat.get('unequal_cnt', 0)
        total = stat.get('all_cnt', 0)
        if total > 0:
            match_rate = ((total - unequal) / total * 100)
            print(f"  {col}: {match_rate:.1f}% match ({unequal} mismatches out of {total})")


if __name__ == "__main__":
    print("\n" + "="*100)
    print(" DATACOMPY BASIC USAGE DEMOS")
    print("="*100)
    print("\nThese examples show how datacompy compares DataFrames")
    print("(Works the same for Excel vs CSV comparison)")
    
    demo_1_perfect_match()
    demo_2_value_differences()
    demo_3_missing_rows()
    demo_4_column_differences()
    demo_5_numeric_tolerance()
    demo_6_column_statistics()
    
    print("\n" + "="*100)
    print(" DEMOS COMPLETE!")
    print("="*100)
    print("\nNext steps:")
    print("  1. Run demo_excel_csv.py to see Excel vs CSV comparison")
    print("  2. Run run_comparison.py to validate your actual data")
