

def has_expected_potential_lines(OCR_result, potential, lines: int, True3: bool, above_160: bool):
    count = 0
    temp_sum = 0
    leng_sum = 0
    for potential_line in OCR_result:
        if True3 :
            value = int(''.join(filter(str.isdigit, potential_line)))
            if potential in ["STR", "DEX", "INT", "LUK"] and (potential in potential_line or "All Stats" in potential_line):   
                temp_sum += value

            elif potential == "ATT" and (potential in potential_line or "Boss" in potential_line) and (not potential_line.startswith("Magic ATT:")) and (not potential_line.startswith("ATT: +32")):
                temp_sum += value
        
            elif potential == "Magic ATT:" and (potential in potential_line or "Boss" in potential_line) and not potential_line.startswith("Magic ATT: +32"):
                temp_sum += value

        #for meso, drop rate etc...
            elif potential not in ["STR", "DEX", "INT", "LUK", "ATT", "Magic ATT:"] and potential in potential_line:
                temp_sum += value
    
        else:
            if potential in potential_line or "All Stats" in potential_line:   
                count +=1
            
    if True3:
        print('Stats sum:',temp_sum,OCR_result)
        return temp_sum >= (33 if above_160 else 30)
    else:
        print('count',count,OCR_result)
        return count >= lines