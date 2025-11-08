from typed import typed, Json, Any, Str, List, Table
from utils.err import TableErr

class table:
    @typed
    def get_row(table: Table=[], row_name: Str='' ) -> List(Any):
        if row_name not in table.keys():
            return []
        row_entries = []
        for entry in table:
            row_entries.append(entry.get(row_name))
        return row_entries

    @typed
    def get_column(table: Table=[], col_index: int=0) -> Json:
        if not isinstance(col_index, int):
            raise TypeError("Column index must be an integer.")
        if 0 <= col_index < len(table):
            return table[col_index]
        else:
            return None

    @typed
    def get_cell(table: Table=[], col_index: int=0, row_name: str='') -> Any:
        column = table.get_column(col_index)
        if column is not None and row_name in column:
            return column[row_name]
        else:
            return None

    @typed
    def normalize(table: Table) -> List(Any):
        if isinstance(table, list):
            normalized_list = []
            for item in table:
                if isinstance(item, (dict, list)):
                    cleaned_item = table.normalize(item)
                    normalized_list.append(cleaned_item)
                elif not(item == "" or item is None):
                    normalized_list.append(item)
            return normalized_list

        if isinstance(table, dict):
            return table.normalize(list(json.flat(table)))
