import csv
row = ['2', ' Marie', ' California']
# with open('people.csv', 'r') as readFile:
#     reader = csv.reader(readFile)
#     lines = list(reader)
# lines[2] = row
# with open('people.csv', 'w') as writeFile:
#     writer = csv.writer(writeFile)
#     writer.writerows(lines)
# readFile.close()
# writeFile.close()
with open('people.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(row)
f.close()

with open('people.csv','r')  as file:
    reader = csv.reader(file)
    lines = list(reader)
    print(lines[0][0])
file.close()