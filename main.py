import csv
import re


with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

contacts_list_new = []
for element in contacts_list:
    new_element = []
    new_element.extend(" ".join(element[:3]).strip().split(" "))
    if len(new_element) > 3:
        new_element.remove('')
    elif len(new_element) < 3:
        new_element.append('')
    new_element.extend(element[3:5])
    pattern = r"(\+7|8)[\s]?\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})[\s]?\(?(доб\.)?[\s]?(\d+)?\)?"
    sub_pattern = r"+7(\2)\3-\4-\5 \6\7"
    result = re.sub(pattern, sub_pattern, element[5])
    new_element.append(result)
    new_element.append(element[6])
    contacts_list_new.append(new_element)

pairs = []
index_delete = []
for i1 in range(len(contacts_list_new)):
    if i1 ==0:
        continue
    for i2 in range(len(contacts_list_new)):
        if i2 == 0 or i1 == i2 or {i1, i2} in pairs:
            continue
        pair = {i1, i2}
        if contacts_list_new[i1][0] == contacts_list_new[i2][0] and contacts_list_new[i1][1] == contacts_list_new[i2][1]:
            index_delete.append(i2)
            for i3 in range(len(contacts_list_new[i1])):
                if i3 < 2:
                    continue
                if contacts_list_new[i1][i3] == '' and not contacts_list_new[i2][i3] == '':
                    contacts_list_new[i1].pop(i3)
                    contacts_list_new[i1].insert(i3, contacts_list_new[i2][i3])

        pairs.append(pair)
index_delete.reverse()

for index in index_delete:
    contacts_list_new.pop(index)

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list_new)
