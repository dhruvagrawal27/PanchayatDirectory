import pandas as pd
import random

def reduce_panchayat_members(input_file, output_file, reduction_percentage=0.25):
    """
    Reduce the number of Panchayat/Ward members for each GramPanchayatName by a specified percentage.
    
    Parameters:
    input_file (str): Path to input CSV file
    output_file (str): Path to output CSV file
    reduction_percentage (float): Percentage of members to remove (default 25%)
    
    Returns:
    tuple: (original_count, new_count) - Number of records before and after reduction
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Store original count
    original_count = len(df)
    
    # Group by GramPanchayatName
    grouped = df.groupby('GramPanchayatName')
    
    # Initialize list to store reduced dataframes
    reduced_dfs = []
    
    for gp_name, group in grouped:
        # Only reduce if there are multiple members
        if len(group) > 1:
            # Calculate number of records to keep
            records_to_remove = int(len(group) * reduction_percentage)
            # Ensure at least one record is kept
            records_to_keep = max(len(group) - records_to_remove, 1)
            
            # Randomly select records to keep
            reduced_group = group.sample(n=records_to_keep, random_state=42)
            reduced_dfs.append(reduced_group)
        else:
            # If only one record, keep it
            reduced_dfs.append(group)
    
    # Combine all reduced groups
    result_df = pd.concat(reduced_dfs)
    
    # Save to new CSV file
    result_df.to_csv(output_file, index=False)
    
    return original_count, len(result_df)

def print_reduction_stats(input_file, output_file):
    """
    Print statistics about the data reduction
    """
    original_df = pd.read_csv(input_file)
    reduced_df = pd.read_csv(output_file)
    
    print("\nReduction Statistics:")
    print(f"Original records: {len(original_df)}")
    print(f"Reduced records: {len(reduced_df)}")
    print(f"Reduction percentage: {((len(original_df) - len(reduced_df)) / len(original_df) * 100):.2f}%")
    
    # Print stats per Gram Panchayat
    original_grouped = original_df.groupby('GramPanchayatName').size()
    reduced_grouped = reduced_df.groupby('GramPanchayatName').size()
    
    print("\nPer Gram Panchayat Statistics:")
    for gp in original_grouped.index:
        orig = original_grouped[gp]
        red = reduced_grouped[gp]
        print(f"\n{gp}:")
        print(f"  Original members: {orig}")
        print(f"  Reduced members: {red}")
        print(f"  Reduction: {((orig - red) / orig * 100):.2f}%")

# Example usage
if __name__ == "__main__":
    input_file = r"F:\India_Info\panchayat_data_with_members.csv"
    output_file = "panchayat_data_with_members1.csv"
    
    try:
        orig_count, new_count = reduce_panchayat_members(
            input_file=input_file,
            output_file=output_file,
            reduction_percentage=0.25  # 25% reduction
        )
        
        print_reduction_stats(input_file, output_file)
        
    except Exception as e:
        print(f"Error: {str(e)}")