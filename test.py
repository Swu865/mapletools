


import re
import ast

pattern = r"(\w+):(\{'.+?\})"
parsed_data = []
a = []
with open('gui/resources/item_category.txt','r') as file:
    for line in file:

        match = re.match(pattern, line.strip())
        if match:

            category = match.group(1)
            dict_str = match.group(2)
            dict_obj = ast.literal_eval(dict_str)
            parsed_data.append([category, dict_obj])


for i in range(len(parsed_data)):
    a.append(parsed_data[i][1])
print(a)

