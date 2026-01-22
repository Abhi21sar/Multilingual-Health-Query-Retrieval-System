import os

import pandas as pd

from app.core.config import settings
from app.core.logging import logger


def convert_excel_to_parquet():
    """Converts the main Excel dataset to Parquet for industry-standard performance."""
    excel_path = settings.DATA_FILE
    parquet_path = excel_path.replace(".xlsx", ".parquet")

    if not os.path.exists(excel_path):
        logger.error(f"Excel file not found at {excel_path}")
        return

    logger.info(f"Converting {excel_path} to {parquet_path}...")
    try:
        df = pd.read_excel(excel_path)
        df.to_parquet(parquet_path, engine='pyarrow', compression='snappy')
        logger.info("Conversion successful.")
    except Exception as e:
        logger.error(f"Failed to convert: {e}")

if __name__ == "__main__":
    convert_excel_to_parquet()
