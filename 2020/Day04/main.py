import re
fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
eye_colors = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

def read_data(file_name):
    data = open(file_name + ".txt", "r", newline=None)
    data = data.read().splitlines()
    data = " ".join(data).replace("  ", "|").split("|")
    return data

def is_valid_numbers(data):
    data = {key_value.split(":")[0]: key_value.split(":")[1] for key_value in data.split(" ")}
    try:
        if not ((len(data["byr"]) == 4) and 0 <= int(data["byr"])-1920 <= 82) : return False
        if not ((len(data["iyr"]) == 4) and 0 <= int(data["iyr"])-2010 <= 10) : return False
        if not ((len(data["eyr"]) == 4) and 0 <= int(data["eyr"])-2020 <= 10) : return False
        if not (("in" in data["hgt"] and 0 <= int(data["hgt"][:-2])-59  <= 17) or
            ("cm" in data["hgt"] and 0 <= int(data["hgt"][:-2])-150 <= 43)): return False
        if not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', data["hcl"]): return False
        if not ((len(data["pid"]) == 9) and int(data["pid"])): return False
        if not data["ecl"] in eye_colors: return False
        return True       
    except: 
        return False

def is_valid(data, valid_parameters):
    return all(word in data for word in valid_parameters)

def part_test():
    data = read_data("test")
    assert part_1(data) == 2
    data = read_data("test_2")
    assert part_2(data) == 4

def part_1(data):
    index  = 0
    for i in data:
        if 7 <= i.count(":") <= 8:                
            if is_valid(i, fields[:i.count(":")]): 
                index += 1
    return index

def part_2(data):
    index  = 0
    for i in data:
        if 7 <= i.count(":") <= 8:                
            if is_valid(i, fields[:i.count(":")]): 
                if is_valid_numbers(i):
                    index += 1
    return index

if __name__ == "__main__":
    part_test()
    data = read_data("input")
    print(part_1(data))
    print(part_2(data))