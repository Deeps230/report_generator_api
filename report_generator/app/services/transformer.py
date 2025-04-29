import pandas as pd

def transform_data(input_df: pd.DataFrame, ref_df: pd.DataFrame, rules: dict) -> pd.DataFrame:
    merged = pd.merge(input_df, ref_df, on=["refkey1", "refkey2"], how="left")
    
    merged["outfield1"] = merged["field1"] + merged["field2"]
    merged["outfield2"] = merged["refdata1"]
    merged["outfield3"] = merged["refdata2"] + merged["refdata3"]
    merged["outfield4"] = merged["field3"].astype(float) * merged[["field5", "refdata4"]].max(axis=1)
    merged["outfield5"] = merged[["field5", "refdata4"]].max(axis=1)
    
    return merged[["outfield1", "outfield2", "outfield3", "outfield4", "outfield5"]]
