# import src.data_store as data_store
# import pandas as pd
# from pathlib import Path


# def test_get_excel_sheets(overview_df: pd.DataFrame, device_df: pd.DataFrame) -> None:
#     """Test that we can read all sheets from an Excel file."""
#     # ARRANGE
#     excel_content = {
#         "overview": overview_df,
#         "AM123": device_df,
#     }
#     excel_path = "mock_audiomoth.xlsx"
#     with pd.ExcelWriter(excel_path) as writer:
#         for sheet_name, df in excel_content.items():
#             df.to_excel(writer, sheet_name=sheet_name, index=False)
#     # ACT
#     sheets = data_store.get_excel_sheets(Path(excel_path))
#     # ASSERT
#     assert set(sheets.keys()) == set(excel_content.keys())
#     for sheet_name, df in sheets.items():
#         pd.testing.assert_frame_equal(
#             df.reset_index(drop=True), excel_content[sheet_name]
#         )
