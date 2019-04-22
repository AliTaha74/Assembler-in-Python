import re
DataSegment = "#Translation of Data Segment\n"
CodeSegment = "#Translation of Code Segment\n"
lbl_data_count = 0       #count labels of data
lbl_dic= dict()         #key and value of the variables
lbl_dic2= dict()           #key and value of labels in code
f = open("pro.txt", "r")
data = f.read()
file =  re.split(r" +.text",data)
line_data = file[0].splitlines() # the part of data in separated string
line_data.pop(0) #pop to ".data" line
for i in range(len(line_data)):
    line_data[i] = re.sub(r"[#].*","", line_data[i]) #remove comments
    if line_data[i].isspace():
        line_data[i] = re.sub(r" *", "", line_data[i])      #after removing comments, remove spaces
line_data  = list(filter(None, line_data))      #remove empty lines
for i in range(len(line_data)):
    s = re.findall(r"\w+(?= *[:])", line_data[i])   # finding labels
    line_data[i] = re.split(" +",line_data[i])      #split lines by spaces
    lbl_dic[s[0]] = lbl_data_count                  #indexing labels
    if line_data[i][1] == ".space":                 #check data type
        for j in range(int(line_data[i][2])):   #reserve 32-bits lines for the count of space variable
            print("MEMORY("+str(lbl_data_count)+")",'<= "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" ;\n')
            DataSegment += "MEMORY("+str(lbl_data_count)+")" +" "+'<= "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" ;\n'
            lbl_data_count+=1
    elif line_data[i][1] == ".word":
        print("MEMORY(" + str(lbl_data_count) + ")",'<=', '"'+"{:032b}".format(int(line_data[i][2])) +'" ;\n')
        DataSegment += "MEMORY(" + str(lbl_data_count) + ")"+" "+'<='+" "+'"'+"{:032b}".format(int(line_data[i][2])) +'" ;\n'       #store the variable in 32 bit format
        lbl_data_count += 1
#####################################################
line_txt = file[1].splitlines()
line_txt.pop(0)         #pop empty line
for i in range(len(line_txt)):
    line_txt[i] = re.sub(r"[#].*","", line_txt[i])
    if line_txt[i].isspace():
        line_txt[i] = re.sub(r" *","",line_txt[i])
line_txt = list(filter(None, line_txt))
for i in range(len(line_txt)):
    if ":" in line_txt[i]:
        tmpl = re.findall(r"\w+(?= *[:])",line_txt[i]) # dah pattern bygeb label f line
        lbl_dic2[tmpl[0]] = i
        instruction = re.split(r":| +:|: +| +: +",line_txt[i])  #get insturction without label
        line_txt[i] = instruction[1] #get insturction without label
###############################
dictinary_of_inst = dict()
dictinary_of_inst ={"j":["J","000010"],"add":["R","000000","100000"],"and":["R","000000","100100"],"sub":["R","000000","100010"],"nor":["R","000000","100111"],"or":["R","000000","100101"],"slt":["R","000000","101010"],
                    "addi":["I","001000"],"lw":["I","100011"],"sw":["I","101011"],"beq":["I","000100"],"bne":["I","000101"]}
dictinary_of_regs = {"$zero":"00000","$at":"00001","$v0":"00010","$v1":"00011",
                     "$a0":"00100","$a1":"00101","$a2":"00110","$a3":"00111",
                     "$t0":"01000","$t1":"01001","$t2":"01010","$t3":"01011","$t4":"01100","$t5":"01101","$t6":"01110","$t7":"01111",
                     "$s0":"10000","$s1":"10001","$s2":"10010","$s3":"10011","$s4":"10100","$s5":"10101","$s6":"10110","$s7":"10111",
                     "$t8":"11000","$t9":"11001","$k0":"11010","$k1":"11011","$gp":"11100","$sp":"11101","$fp":"11110","ra":"11111"}
out = ""
for i in range(len(line_txt)):
    tmpins = re.findall(r"\$\w+(?= *[\(\)])",line_txt[i]) #get reg between barkets
    line_txt[i] =re.sub(r",",r" ",line_txt[i])
    line_txt[i] = re.sub(r"\(|\)", r" ", line_txt[i]) #delete barkets
    ins = line_txt[i].split()
    print(ins)
    if dictinary_of_inst[ins[0]][0] == "R":
        out = dictinary_of_inst[ins[0]][1]
        out += dictinary_of_regs[ins[2]]
        out += dictinary_of_regs[ins[3]]
        out += dictinary_of_regs[ins[1]]
        out += "00000"
        out += dictinary_of_inst[ins[0]][2]
        print("MEMORY("+str(i)+")",':=',"\"" +out+ "\" ;\n")
        CodeSegment += "MEMORY("+str(i)+")"+" "+':='+" "+"\"" +out+ "\" ;\n"
    elif dictinary_of_inst[ins[0]][0] == "I":
        if len(ins) == 3 and ins[0] != "beq" and ins[0] != "bne":
            out = dictinary_of_inst[ins[0]][1]
            out += dictinary_of_regs[tmpins[0]]
            out += dictinary_of_regs[ins[1]]
            bi = "{:016b}".format(int(ins[2][0]))
            out += bi
            print("MEMORY(" + str(i) + ")", ':=', "\"" + out + "\" ;\n")
            CodeSegment += "MEMORY(" + str(i) + ")" + " " + ':=' + " " + "\"" + out + "\" ;\n"
        elif len(ins) == 4 and ins[0] != "beq" and ins[0] != "bne" != ins[0] != "addi":
            out = dictinary_of_inst[ins[0]][1]
            out += dictinary_of_regs[tmpins[0]]
            out += dictinary_of_regs[ins[1]]
            if ins[2].isdigit():                   # bashof hl hwa rqm wla la 3shan lw d5l msafa
                num = "{:016b}".format(int(ins[2]))
            else:
                num = "{:016b}".format(lbl_dic[ins[2]] * 4)
            out += num
            print("MEMORY(" + str(i) + ")", ':=', "\"" + out + "\" ;\n")
            CodeSegment += "MEMORY(" + str(i) + ")" + " " + ':=' + " " + "\"" + out + "\" ;\n"
        elif ins[0] == "beq" or ins[0] == "bne":
            out = dictinary_of_inst[ins[0]][1]
            out += dictinary_of_regs[ins[1]]
            out += dictinary_of_regs[ins[2]]
            v = lbl_dic2[ins[3]]
            r = (int(v) - i - 1)
            num = int((bin(r & 0b1111111111111111)), 2)  # bn3ml 2s comp, covert binary str to int
            out += "{:016b}".format(num)  # covert to binary with format 16 bit
            print("MEMORY(" + str(i) + ")", ':=', "\"" + out + "\" ;\n")
            CodeSegment += "MEMORY(" + str(i) + ")" + " " + ':=' + " " + "\"" + out + "\" ;\n"
        elif ins[0] == "addi":
            out = dictinary_of_inst[ins[0]][1]
            out += dictinary_of_regs[ins[2]]
            out += dictinary_of_regs[ins[1]]
            out += "{:016b}".format(int(ins[3]))
            print("MEMORY(" + str(i) + ")", ':=', "\"" + out + "\" ;\n")
            CodeSegment += "MEMORY(" + str(i) + ")" + " " + ':=' + " " + "\"" + out + "\" ;\n"
        elif ins[0] == "addi":
            out = dictinary_of_inst[ins[0]][1]
            out += dictinary_of_regs[ins[2]]
            out += dictinary_of_regs[ins[1]]
            out += "{:016b}".format(int(ins[3]))
            print("MEMORY(" + str(i) + ")", ':=', "\"" + out + "\" ;\n")
            CodeSegment += "MEMORY(" + str(i) + ")" + " " + ':=' + " " + "\"" + out + "\" ;\n"

    elif dictinary_of_inst[ins[0]][0] == 'J':
        out = dictinary_of_inst[ins[0]][1]
        v = lbl_dic2[ins[1]]
        r = (int(v))
        num = "{:026b}".format(r)
        out += str(num)
        print("MEMORY(" + str(i) + ")", ':=', "\"" + out + "\" ;\n")
        CodeSegment += "MEMORY(" + str(i) + ")" + " " + ':=' + " " + "\"" + out + "\" ;\n"

################ fileSave ###########3
f = open("CodeSegment.txt", "a")
f.truncate(0)
f.write(CodeSegment)
f.close()
####################
f = open("DataSegment.txt", "a")
f.truncate(0)
f.write(DataSegment)
f.close()








