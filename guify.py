from tkinter import *
from tkinter import messagebox
import sys
import argparse
import subprocess

def defparse(line: str):
    phase_0=line.strip("{").strip("}")
    phase_1=phase_0.split(":-")
    print(phase_1)
    return phase_1

def progparser(prog: str):
    argdict = {}
    with open(prog) as file:
        lines = file.readlines()
        if "#!/bin/bash" not in lines[0]:
            print("Not a bash script (first line must contain \"#!/bin/bash\")",file=sys.stderr)
            exit(1)
        for i in lines:
            if "=$" in i:
                phase_0 = i.strip('\n')
                phase_0 = phase_0.split("=$") #Splits into LHS (variable), RHS (value)
                if ":" in phase_0[1]: #Check for defaults
                    phase_1 = defparse(phase_0[1])
                    # phase_0
                    # phase_0 += phase_1
                    argdict.update({phase_1[0]: {"var": phase_0[0], "default": phase_1[-1].strip("\"")}})
                    # print(phase_0)
                else:
                    argdict.update({phase_0[1]: phase_0[0]})
                print(phase_0)
        print(argdict)
    return argdict

def Launch(arglist: list):
   argliststr = [i.get() for i in arglist]
   argstring = " ".join([i.get() for i in arglist])
   command = "."+prog+" "+argstring
   msg=messagebox.showinfo("Launching Program", "Command: "+command)
   print([prog]+argliststr)
   subprocess.run([prog]+argliststr)


parser = argparse.ArgumentParser(
    prog='GUIfy',
    description='Adds a GUI form for any bash script',
    epilog='Version 0.1'
)

parser.add_argument('filepath',help='path to program to GUIfy')
pras = parser.parse_args()

prog = pras.filepath

print(prog)

argdict = progparser(prog)

progname = prog.split("/")[-1].split(".")[0]

root = Tk()
root.title(progname)
w = Label(root, text='GUIfy v0.1').grid(row=0,column=1)
arglist = []
for num,i in enumerate(argdict):
    # print(type(argdict[i]))
    print(num)
    if type(argdict[i]) is dict: #Default is dict
        # for j in argdict[i]:
            # print(argdict[i][j])
        arglist.append(StringVar(root))
        x = Label(root, text=argdict[i]['var']).grid(row=num+1)
        e1 = Entry(root, textvariable=arglist[-1]).grid(row=num+1, column=1)
        x = Label(root, text="Default: "+argdict[i]['default']).grid(row=num+1,column=2)
    else:
        # print(argdict[i])
        arglist.append(StringVar(root))
        x = Label(root, text=argdict[i]).grid(row=num+1)
        e1 = Entry(root, textvariable=arglist[-1]).grid(row=num+1, column=1)

# x = Label(root, text='First Name').grid(row=1)
# e1 = Entry(root).grid(row=1, column=1)
# l = Label(root, text='Last Name').grid(row=2)
# e2 = Entry(root).grid(row=2, column=1)
y = Button(root,text='Launch', command=lambda: Launch(arglist)).grid(row=3,column=1)
# var1 = IntVar()
# Checkbutton(root, text='male', variable=var1).grid(row=4, sticky=W)
# var2 = IntVar()
# Checkbutton(root, text='female', variable=var2).grid(row=5, sticky=W)


# w.pack()
# y.pack()

'''
widgets are added here
'''

root.mainloop()
