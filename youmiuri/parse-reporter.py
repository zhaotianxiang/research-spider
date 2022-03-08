import csv
import re

csv_reader = csv.reader(open("./data/csv/youmiuri.csv"))
csv_writer = csv.writer(open("./data/csv/youmiuri.csv"))
csv_list = []

new_line_list = []
for line in csv_reader:
    content = line[3]
    content_reverse = content[::-1]
    author_list = re.findall(r'^）.*?（', content_reverse)
    author_list_2 = re.findall(r'(?<=【).*?(?=】)', content)

    if author_list and len(author_list):
        author_str = author_list[0]
        author_str = author_str[::-1]
        authors_str = author_str.lstrip("（").rstrip("）").replace("\u3000", "----")

        authors_str_splits = authors_str.split("、")
        for author in authors_str_splits:
            new_line = line.copy()
            author_name = None
            author_department = None
            is_contain_ch = "----" in author
            if is_contain_ch:
                author_name = author.split("----")[0]
                author_department = author.split("----")[1]
                pass
            else:
                is_contain_dot = "・" in author
                if is_contain_dot:
                    new_line.append(author.split("・")[0])
                    author_name = author.split("・")[1]
                else:
                    author_name = author
            new_line[1] = author_name
            new_line[2] = author_department
            new_line_list.append(new_line)
    elif author_list_2 and len(author_list_2) > 0:
        for author_str in author_list_2:
            author_area_list = author_str.split("、")
            for author_area_str in author_area_list:
                author_area_splits = author_area_str.split("＝", 1)
                if author_area_splits and len(author_area_splits) == 2:
                    new_line = line.copy()
                    new_line[1] = author_area_str.split("＝", 1)[1]
                    new_line[2] = author_area_str.split("＝", 1)[0]
                    new_line_list.append(new_line)
    else:
        new_line_list.append(line)

print("new line len: ", len(new_line_list))

with open('./data/csv/youmiuri-parse-reporter.csv', 'w', newline='') as student_file:
    writer = csv.writer(student_file)
    for row in new_line_list:
        writer.writerow(row)
