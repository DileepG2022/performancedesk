import pandas as pd
from io import BytesIO
from openpyxl.styles import numbers
from datetime import timedelta

def export_dataframe_with_text_format(df, filename, sheet_name="Sheet1"):
    """
    Export DataFrame to Excel with phone number columns as text.
    Returns an HttpResponse with the file attached.
    """
    from django.http import HttpResponse

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)

        # Apply text format to phone number columns
        ws = writer.sheets[sheet_name]
        for col in ["mobile_no", "whatsapp_no"]:
            if col in df.columns:
                col_idx = df.columns.get_loc(col) + 1  # Excel is 1-based
                for row_idx in range(2, len(df) + 20):  # Add buffer rows
                    cell = ws.cell(row=row_idx, column=col_idx)
                    cell.number_format = "@"

    buffer.seek(0)
    response = HttpResponse(
        buffer,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response

def calculate_working_day(start_date, day_count):
    """
    Returns the date that is `day_count` working days after `start_date`,
    skipping Saturdays and Sundays.
    """
    current_date = start_date
    added_days = 0

    while added_days < day_count:
        if current_date.weekday() < 5:  # Monday=0, ..., Friday=4
            added_days += 1
        if added_days < day_count:
            current_date += timedelta(days=1)

    return current_date