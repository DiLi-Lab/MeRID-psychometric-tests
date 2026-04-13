import os
import re
import tempfile
import zipfile
from pathlib import Path

import pandas as pd


def resolve_table_file(base_path_without_ext, file_label='input file'):
    """
    Resolve a table file path, preferring xlsx but allowing csv.
    """
    candidate_extensions = ('.xlsx', '.csv')
    base_path = Path(base_path_without_ext)
    for extension in candidate_extensions:
        candidate_path = base_path.with_suffix(extension)
        if candidate_path.exists():
            return str(candidate_path)

    tried_paths = ", ".join(str(base_path.with_suffix(ext)) for ext in candidate_extensions)
    raise FileNotFoundError(f"Could not find {file_label}. Tried: {tried_paths}")


def load_table_file(table_path, **kwargs):
    """
    Load a tabular file from csv/xlsx based on file extension.
    """
    table_path = Path(table_path)
    if table_path.suffix.lower() == '.csv':
        return pd.read_csv(table_path, **kwargs)

    # pandas/openpyxl can fail on malformed xlsx merge metadata in some files.
    excel_kwargs = dict(kwargs)
    excel_kwargs.pop('encoding', None)  # not used by read_excel
    try:
        return pd.read_excel(table_path, **excel_kwargs)
    except Exception as excel_error:
        fallback_csv_path = table_path.with_suffix('.csv')
        if fallback_csv_path.exists():
            return pd.read_csv(fallback_csv_path, **kwargs)

        # Final fallback: strip malformed merge metadata from workbook XML
        # and retry with pandas/openpyxl.
        try:
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
                sanitized_path = temp_file.name

            with zipfile.ZipFile(table_path, 'r') as source_zip, zipfile.ZipFile(sanitized_path, 'w') as target_zip:
                for item in source_zip.infolist():
                    data = source_zip.read(item.filename)
                    if item.filename.startswith('xl/worksheets/sheet') and item.filename.endswith('.xml'):
                        # Remove mergeCells block; merge metadata is optional for data reads
                        # and malformed merge refs can crash openpyxl parsing.
                        try:
                            xml_text = data.decode('utf-8')
                            xml_text = re.sub(r'<mergeCells[^>]*>.*?</mergeCells>', '', xml_text, flags=re.DOTALL)
                            data = xml_text.encode('utf-8')
                        except UnicodeDecodeError:
                            pass
                    target_zip.writestr(item, data)

            try:
                return pd.read_excel(sanitized_path, **excel_kwargs)
            finally:
                if Path(sanitized_path).exists():
                    os.remove(sanitized_path)
        except Exception:
            raise excel_error
