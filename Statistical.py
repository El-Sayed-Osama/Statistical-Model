import numpy as np
import random,re
from flask import Flask,render_template,request
app = Flask(__name__)
###################################################
#Extract the query array weights
def query(x):
    #Check Query Syntax before calculations
    pattern = r'^<([A-E]:((0.[0-9]+)|1))(;[A-E]:((0.[0-9]+)|1))*>$'
    result = re.match(pattern,x)
    if not result:
        return 2
    if x=='':
        return 1

    #End of check and start of calculations
    # x=x[1:len(x)-1]
    x = x.strip('<>')
    x=x.split(";")
    y=[0]*len(x)
    c=[0,0,0,0,0]
    for i in range (len(x)):
        y[i]=x[i].split(":")

    for i in range (len(y)):
        y[i][1]=float(y[i][1])

    for i in range (len(y)):
        if(y[i][0]=='A'):
            c[0]=y[i][1]
        elif(y[i][0]=='B'):
            c[1]=y[i][1]
        elif(y[i][0]=='C'):
            c[2]=y[i][1]
        elif(y[i][0]=='D'):
            c[3]=y[i][1]
        else:
            c[4]=y[i][1]
    return c
#Calculate the simillarty
def Cal(s,q):
    c=[0,0,0,0,0]
    c[0]=s.count('A')
    c[1]=s.count('B')
    c[2]=s.count('C')
    c[3]=s.count('D')
    c[4]=s.count('E')
    d1=[c[0]/len(s),c[1]/len(s),c[2]/len(s),c[3]/len(s),c[4]/len(s)]
    d1sum=np.sum(np.multiply(d1,q))
    return round(d1sum,3)
#read file and extarct wanted array
def read(p):
    f = open(p, "r+")
    line = f.readline()
    s=line.split()
    return s
#Display Result
def show(d1sum,d2sum,d3sum):
    if (d1sum>=d2sum and d1sum>=d3sum):
        if (d2sum>=d3sum):
            res = 'Sim to Query is : \n(1) D1 with ratio = '+str(d1sum)+'\n(2) D2 with ratio = '+str(d2sum)+'\n(3) D3 with ratio = '+str(d3sum)+'\n'
            return res
        else:
            res = 'Sim to Query is : \n(1) D1 with ratio = '+str(d1sum)+'\n(2) D3 with ratio = '+str(d3sum)+'\n(3) D2 with ratio = '+str(d2sum)+'\n'
            return res
    elif (d2sum>=d1sum and d2sum>=d3sum):
        if (d1sum>=d3sum):
            res = 'Sim to Query is : \n(1) D2 with ratio = '+str(d2sum)+'\n(2) D1 with ratio = '+str(d1sum)+'\n(3) D3 with ratio = '+str(d3sum)+'\n'
            return res
        else:
            res = 'Sim to Query is : \n(1) D2 with ratio = '+str(d2sum)+'\n(2) D3 with ratio = '+str(d3sum)+'\n(3) D1 with ratio = '+str(d1sum)+'\n'
            return res
    else:
        if (d3sum>=d1sum and d3sum>=d2sum):
            if (d1sum>=d2sum):
                res = 'Sim to Query is : \n(1) D3 with ratio = '+str(d3sum)+'\n(2) D1 with ratio = '+str(d1sum)+'\n(3) D2 with ratio = '+str(d2sum)+'\n'
                return res
            else:
                res = 'Sim to Query is : \n(1) D3 with ratio = '+str(d3sum)+'\n(2) D2 with ratio = '+str(d2sum)+'\n(3) D1 with ratio = '+str(d1sum)+'\n'
                return res
#Random String
def randString(length=6):
    letters='ABCDE'
    return ''.join((random.choice(letters) for i in range(length)))
#Write Generated Strings in files
def wrrd(p):
    s=randString()
    s=s[0]+" "+s[1]+" "+s[2]+" "+s[3]+" "+s[4]+" "+s[5]
    f = open(p,"w")
    f.write(s)
    f.close()
###################################################
@app.route('/')
def index():
	return render_template('home.html')
###################################################
@app.route('/form', methods=['GET','POST'])
def form():
    #If ShowSim button clicked
    if 's' in request.form:
        s1=read("D:\My Projects\IR\Project\D1.txt")
        s2=read("D:\My Projects\IR\Project\D2.txt")
        s3=read("D:\My Projects\IR\Project\D3.txt")
        if request.method=='POST':
            x=request.form['x']
            y=query(x)
            if y==1:
                return 'Please, Insert Query!'
            if y==2:
                return 'Please, Insert a Valid Query!'
            res1=Cal(s1,y)
            res2=Cal(s2,y)
            res3=Cal(s3,y)
            fres=show(res1,res2,res3)
            fres=fres.split("\n")
            return render_template('home.html',x=fres[0],y=fres[1],z=fres[2],c=fres[3])
        else:
            return render_template('home.html')
    #If Random Generate button clicked
    else:
        wrrd("D:\My Projects\IR\Project\D1.txt")
        wrrd("D:\My Projects\IR\Project\D2.txt")
        wrrd("D:\My Projects\IR\Project\D3.txt")
        s1=read("D:\My Projects\IR\Project\D1.txt")
        s2=read("D:\My Projects\IR\Project\D2.txt")
        s3=read("D:\My Projects\IR\Project\D3.txt")
        if request.method=='POST':
            x=request.form['x']
            y=query(x)
            if y==1:
                return 'Please, Insert Query!'
            if y==2:
                return 'Please, Insert a Valid Query!'
            res1=Cal(s1,y)
            res2=Cal(s2,y)
            res3=Cal(s3,y)
            fres=show(res1,res2,res3)
            fres=fres.split("\n")
            return render_template('home.html',x=fres[0],y=fres[1],z=fres[2],c=fres[3])
        else:
            return render_template('home.html')
##################################################
if __name__ == '__main__':
	app.run(debug = True)
