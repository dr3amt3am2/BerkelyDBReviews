''' 
formats .txt files to key on one line data on next
'''

# open files and create intermediate files (m)
rw = open("reviews.txt", "r")
pt = open("pterms.txt", "r")
rt = open("rterms.txt", "r")
sc = open("scores.txt", "r")
rwm = open("rwm.txt", "w")
ptm = open("ptm.txt", "w")
rtm = open("rtm.txt", "w")
scm = open("scm.txt", "w")

# separate key and data with newline
for line in rw:
    line = line.replace(",", "\n", 1)
    rwm.write(line)

for line in pt:
    line = line.replace(",", "\n", 1)
    ptm.write(line)

for line in rt:
    line = line.replace(",", "\n", 1)
    rtm.write(line)

for line in sc:
    line = line.replace(",", "\n", 1)
    scm.write(line)

# close files
rw.close()
pt.close()
rt.close()
sc.close()
rwm.close()
ptm.close()
rtm.close()
scm.close()

print("Formatting Completed.")