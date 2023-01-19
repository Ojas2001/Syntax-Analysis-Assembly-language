LC=0 
mnemonics={'STOP':('00','IS',0),
           'ADD':('01','IS',2),
           'SUB':('02','IS',2),
           'MULT':('03','IS',2),
           'MOVER':('04','IS',2),
           'MOVEM':('05','IS',2),
           'COMP':('06','IS',2),
           'BC':('07','IS',2),
           'DIV':('08','IS',2),
           'READ':('09','IS',1),
           'PRINT':('10','IS',1),
           'LOAD':('11','IS',1),
           'STORE':('12','IS',1),
           'LTORG':('05','AD',0),
           'ORIGIN':('03','AD',1),
           'START':('01','AD',1),
           'EQU':('04','AD',2),
           'DS':('01','DL',1),
           'DC':('02','DL',1),
           'END':('AD',0)
           }
           
REG={'AREG':1,'BREG':2,'CREG':3,'DREG':4} 

fname = input("Enter file name: ")
input_file = open(fname,"r")
inter_file = open("intermediate.txt","a+")
inter_file.truncate(0)
literal_file = open("literal.txt","a+")
literal_file.truncate(0)
temp = open("temp.txt","a+")
temp.truncate(0)
error = open("error.txt","a+")
error.truncate(0)
symtab={}   
pooltab=[]	
word=[]

def errors(arg,p):
    global LC
    global mnemonics
    global symtab
    if arg in symtab.keys():
    	if p != "-":
        	error.write(str(arg)+" not declared OR is declared twice!! \n")
    elif arg not in mnemonics.keys():
        error.write(str(arg)+" not a valid mnemonic!! -> "+str(LC)+"\n")
        inter_file.write(str(LC)+"\t error\n")

def littab():
    print("literal table:")
    literal_file.seek(0,0)
    for x in literal_file:
        print(x)

def pooltab2():
    global pooltab
    print("Pool Table:")
    print(pooltab)

def symbol():
    global symtab
    print("Symbol Table:")
    print(symtab)
      
def END():
    global LC
    pool=0
    z=0
    inter_file.write("\t(AD,02)\n")
    literal_file.seek(0,0)
    for x in literal_file:
        if "**" in x:
            pool+=1
            if pool==1:
                pooltab.append(z)
            y=x.split()
            temp.write(y[0]+"\t"+str(LC)+"\n")
            LC+=1
        else:
            temp.write(x)
        z+=1
    literal_file.truncate(0)
    temp.seek(0,0)
    for x in temp:
        literal_file.write(x)
    temp.truncate(0)

def DS(size):
    global LC
    inter_file.write(str(LC)+"\t(DL,01)\t(C,"+size+")\n")
    LC=LC+int(size)

def DC(value):
    global LC
    inter_file.write(str(LC)+"\t(DL,02)\t(C,"+value+")\n")
    LC+=1
    
def EQU(word):
    global symindex,LC
    global symtab
    if len(word) < 3:
        errors(word[0])
    else:
        if word[2] in symtab.keys():
            obj_1 = symtab.get(word[0])
            obj_2 = symtab.get(word[2])
            symtab[word[0]] = (obj_2[0],obj_1[1])
            inter_file.write("\t(AD,04)\t(S,"+str(obj_2[1])+")\n")
        else:
            sp = word[2].strip()
            if str(sp[1]) == '+' and sp[2].isnumeric():
                obj_1 = symtab.get(word[0])
                obj_2 = symtab.get(sp[0])
                lc = int(obj_2[0])+int(sp[2])
                symtab[word[0]] = (lc,obj_1[1])
                inter_file.write("\t(AD,04)\n")
            elif str(sp[1]) == '-' and sp[2].isnumeric():
                obj_1 = symtab.get(word[0])
                obj_2 = symtab.get(sp[0])
                lc = int(obj_2[0]) - int(sp[2])
                symtab[word[0]] = (lc,obj_1[1])
                inter_file.write("\t(AD,04)\n")
            else:
                errors(word[2],"-")
            
    
def LTORG():
    global LC
    pool=0
    z=0
    literal_file.seek(0,0)
    x=literal_file.readlines()
    i=0
    while(i<len(x)):
        f=[]
        if("**" in x[i]):
            j=0
            pool+=1
            if pool==1:
                pooltab.append(z)
            while(x[i][j]!="'"):
                j+=1
            j+=1
            while(x[i][j]!="'"):
                f.append(x[i][j])
                j+=1
            if(i!=len(x)-1):
                inter_file.write(str(LC)+"\t(AD,05)\t(DL,02)(C,"+str(f[0])+")\n")
                y=x[i].split()
                temp.write(y[0]+"\t"+str(LC)+"\n")
                LC+=1
            else:
                inter_file.write(str(LC)+"\t(AD,05)\t(DL,02)(C,"+str(f[0])+")\n")
                y=x[i].split()
                temp.write(y[0]+"\t"+str(LC)+"\n")
                LC+=1
        else:
            temp.write(x[i])
        z+=1
        i+=1
    literal_file.truncate(0)
    temp.seek(0,0)
    for x in temp:
        literal_file.write(x)
    temp.truncate(0)
    
def ORIGIN(word):
    global LC
    global symtab
    if word[1].isnumeric():
        LC = int(word[1])
        inter_file.write("\t(AD,03)\n")
    elif word[1] in symtab.keys():
            obj = symtab.get(word[1])
            LC = obj[0]
            inter_file.write("\t(AD,03)\t(S,"+str(obj[1])+")\n")
    else:
            sp = word[1].strip()
            if str(sp[1]) == '+' and sp[2].isnumeric():
                obj = symtab.get(sp[0])
                LC = int(obj[0])+int(sp[2])
                inter_file.write("\t(AD,03)\n")
            elif str(sp[1]) == '-' and sp[2].isnumeric():
                obj = symtab.get(sp[0])
                LC = int(obj[0])-int(sp[2])
                inter_file.write("\t(AD,03)\n")
            else:
                errors(word[1])
    
def OTHERS(mnemonic,k):
    global mnemonics 
    global symtab, pooltab
    global symindex, LC
    z=mnemonics[mnemonic]
    inter_file.write(str(LC)+"\t("+z[1]+","+z[0]+")\t")
    i=0
    for i in range(1,3):
        word[k+i-1]=word[k+i-1].replace(",","")
        if(word[k+i-1] in REG.keys()):
            inter_file.write("(RG,"+str(REG[word[k+i-1]])+")\n")
        elif("=" in word[k+i-1]):
            literal_file.seek(0,2)
            literal_file.write(word[k+i-1]+"\t**\n")
            literal_file.seek(0,0)
            x=literal_file.readlines()
            inter_file.write("(L,"+str(len(x))+")")
        else:
            if(word[k+i-1] not in mnemonics.keys()):
                if(word[k+i-1] not in symtab.keys()):
                    symindex+=1
                    inter_file.write("(S,"+str(symindex)+")")
                else:
                    w=symtab[word[k+i-1]]
                    inter_file.write("(S,"+str(w[-1])+")")
    inter_file.write("\n")
    LC+=1

def detect_mn(word,k):
    global LC
    global mnemonics
    if(word[k]=="START"):
        LC=int(word[k+1])
        inter_file.write("\t(AD,01)\t(C,"+str(LC)+')\n')
    elif(word[k]=='END'):
        END()
    elif(word[k]=="LTORG"):
       LTORG()
    elif(word[k]=="ORIGIN"):
       ORIGIN(word)
    elif(word[k]=="DS"):
        DS(word[k+1])
    elif(word[k]=="DC"):
        DC(word[k+1])
    elif(word[k]=="EQU"):
        EQU(word)
    elif(word[k]=='STOP'):
        inter_file.write("\t(IS,00)\n")
    else:
        OTHERS(word[k],k)
    littab()
    pooltab2()
    symbol()

symindex = 0
for line in input_file:
    word = line.split()
    print("LC=",LC)
    print(line)
    print(word)
    if len(word) == 3:
        if word[0] not in mnemonics.keys():
            if word[0]  not in symtab.keys():
                symtab[word[0]] = (LC,symindex)
                symindex += 1
            #elif word[0]  in symtab.keys():
            	#errors(word[0],"-")
            if word[1] not in mnemonics.keys():
                errors(word[1],"-")
            else:
               detect_mn(word,1)
    elif len(word) == 2:
        if word[0] not in mnemonics.keys(): 
            errors(word[0],"-")
            if word[1] not in symtab.keys():
                symtab[word[1]] = ("**",symindex)
                symindex += 1
        else:
            detect_mn(word, 0)
    elif len(word) == 1:
        if word[0] in mnemonics.keys():
             detect_mn(word, 0)
    else:
        errors(word[0],"-")
        


sym=open("SymTab.txt","a+")
sym.truncate(0)
for x in symtab:
    if str(symtab[x][0]) == "**":
        errors(x,"**")
    sym.write(x+"\t"+str(symtab[x][0])+"\n")
sym.close()
pool=open("PoolTab.txt","a+")
pool.truncate(0)
for x in pooltab:
    pool.write(str(x+1)+"\n")
pool.close()  
input_file.close()
error.close()   
inter_file.close()
literal_file.close()
temp.close()   
                
