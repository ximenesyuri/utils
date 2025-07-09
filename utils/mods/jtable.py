from typed import typed, Json, Any, Str, List, JsonTable
from utils.mods.json_ import json
from utils.err import JTableErr

class jtable:
    @typed
    def get_row(json_table: JsonTable=[], row_name: Str='' ) -> List(Any):
        if row_name not in json_table.keys():
            return []
        row_entries = []
        for entry in json_table:
            row_entries.append(entry.get(row_name))
        return row_entries

    @typed
    def get_column(json_table: JsonTable=[], col_index: int=0) -> Json:
        if not isinstance(col_index, int):
            raise TypeError("Column index must be an integer.")
        if 0 <= col_index < len(json_table):
            return json_table[col_index]
        else:
            return None

    @typed
    def get_cell(json_table: JsonTable=[], col_index: int=0, row_name: str='') -> Any:
        column = jtable.get_column(col_index)
        if column is not None and row_name in column:
            return column[row_name]
        else:
            return None

    @typed
    def normalize(json_table: JsonTable) -> List(Any):
        if isinstance(json_table, list):
            normalized_list = []
            for item in json_table:
                if isinstance(item, (dict, list)):
                    cleaned_item = jtable.normalize(item)
                    normalized_list.append(cleaned_item)
                elif not(item == "" or item is None):
                    normalized_list.append(item)
            return normalized_list

        if isinstance(json_table, dict):
            return jtable.normalize(list(json.flat(json_table)))
