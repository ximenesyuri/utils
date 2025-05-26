from utils.mods.types import Json, Any
from utils.mods.json_ import json
from utils.err import JTableErr

class JTable(Json):
    def __init__(self, data):
        if not isinstance(data, list):
            raise TypeError("Input data must be a list.")
        if not all(isinstance(item, dict) for item in data):
            raise TypeError("All items in the list must be dictionaries.")
        if data:
            first_keys = set(data[0].keys())
            if not all(set(item.keys()) == first_keys for item in data):
                raise ValueError("All dictionaries in the list must have the same keys.")

        self.data = data
        self.keys = list(data[0].keys()) if data else []

    def get_row(self, row_name) -> list:
        if row_name not in self.keys:
            return []

        row_entries = []
        for entry in self.data:
            row_entries.append(entry.get(row_name))

        return row_entries

    def get_column(self, col_index: int) -> Json:
        if not isinstance(col_index, int):
            raise TypeError("Column index must be an integer.")
        if 0 <= col_index < len(self.data):
            return self.data[col_index]
        else:
            return None

    def get_cell(self, col_index: int, row_name: str) -> Any:
        column = self.get_column(col_index)
        if column is not None and row_name in column:
            return column[row_name]
        else:
            return None

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"JsonTable(data={self.data})"

class jtable:
    def get_row(json_table: JTable, row_name: str='') -> list:
        try:
            return JTable(json_table).get_row(row_name=row_name)
        except Exception as e:
            raise JTableErr(e)

    def get_column(json_table: JTable, col_index: int=0) -> dict:
        try:
            return JTable(json_table).get_column(col_index=col_index)
        except Exception as e:
            raise JTableErr(e)

    def get_cell(json_table: JTable, col_index: int=0, row_name: str='') -> Any:
        try:
            return JTable(json_table).get_cell(col_index=col_index,  row_name=row_name)
        except Exception as e:
            raise JTableErr(e)

    def normalize(json_data: Json) -> list:
        if isinstance(json_data, list):
            normalized_list = []
            for item in json_data:
                if isinstance(item, (dict, list)):
                    cleaned_item = jtable.normalize(item)
                    normalized_list.append(cleaned_item)
                elif not(item == "" or item is None):
                    normalized_list.append(item)
            return normalized_list

        if isinstance(json_data, dict):
            return jtable.normalize(list(json.flat(json_data)))
