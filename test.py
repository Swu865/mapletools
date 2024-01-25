import re
import ast
from utils import DataPreprocessing

Data_process = DataPreprocessing("resources/item_category.txt")

print(Data_process.get_item_name_list())

