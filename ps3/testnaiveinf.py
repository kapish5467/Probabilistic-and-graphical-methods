from factor import *
from factorset import *
from naiveinf import *

def buildrobotex(commandfailrate,stickprob,fpr,fnr):

    c = discretevariable("c",2)
    x0 = discretevariable("x0",3)
    x1 = discretevariable("x1",3)
    r0 = discretevariable("r0",2)
    l0 = discretevariable("l0",2)
    r1 = discretevariable("r1",2)
    l1 = discretevariable("l1",2)

    px0 = discretefactor({x0})
    px0[{x0:0}] = 1.0/3.0
    px0[{x0:1}] = 1.0/3.0
    px0[{x0:2}] = 1.0/3.0

    pc = discretefactor({c})
    pc[{c:0}] = 0.5
    pc[{c:1}] = 0.5

    px1x0c = discretefactor({x1,x0,c})
    px1x0c[{}] = 0.0 # initialize to all zeros
    for oldx in range(0,3):
        for cval in range(0,2):
            newx = oldx-1 if cval else oldx+1
            newx = min(max(newx,0),2)
            px1x0c[{x0:oldx,x1:newx,c:cval}] += 1.0-commandfailrate
            px1x0c[{x0:oldx,x1:oldx,c:cval}] += commandfailrate
 

    def initsensorcpd(pos,sen,walls):
        f = discretefactor({pos,sen})
        for posval in range(0,3):
            w = walls[posval]
            notw = 1-w
            errrate = fnr if w else fpr
            f[{pos:posval,sen:w}] = 1.0-errrate
            f[{pos:posval,sen:notw}] = errrate
        return f


    pr0x0 = initsensorcpd(x0,r0,[0,1,0])
    pl0x0 = initsensorcpd(x0,l0,[1,0,0])

    def nextsensorcpd(pos,oldsen,sen,walls):
        f = discretefactor({pos,oldsen,sen})
        f[{}] = 0.0
        for posval in range(0,3):
            for oldsenval in range(0,2):
                f[{pos:posval,oldsen:oldsenval,sen:oldsenval}] += stickprob
                w = walls[posval]
                notw = 1-w
                errrate = fnr if w else fpr
                f[{pos:posval,oldsen:oldsenval,sen:w}] += (1.0-stickprob)*(1.0-errrate)
                f[{pos:posval,oldsen:oldsenval,sen:notw}] += (1.0-stickprob)*errrate

        return f

    pr1r0x1 = nextsensorcpd(x1,r0,r1,[0,1,0])
    pl1l0x1 = nextsensorcpd(x1,l0,l1,[1,0,0])
                
    robotbn = factorset()
    robotbn.addfactor(pc)
    robotbn.addfactor(px0)
    robotbn.addfactor(px1x0c)
    robotbn.addfactor(pr0x0)
    robotbn.addfactor(pl0x0)
    robotbn.addfactor(pr1r0x1)
    robotbn.addfactor(pl1l0x1)
    
    unnorm = pc*pr0x0*pr1r0x1*pl0x0*pl1l0x1
    z = unnorm.marginalize({c,r0,r1,l0,l1})
    norm = unnorm / z
    phinew = unnorm.reduce({r0:1,l0:1,r1:1,l1:1})

    return robotbn,(c,x0,x1,r0,r1,l0,l1)

def buildstudentex():
    # note you will need to have g have values of 0,1,2
    # (not 1,2,3 as in the text)

    # remove line below when you write your code
    # it is okay just to "hard code" all of the values in here
   
    # will need to return your factorset (studentbn below) as the 
    # variables in the order d,i,g,s,l (as below)
   
    d= discretevariable("d",2)
   
    i = discretevariable("i",2)
    
    g = discretevariable("g",3)
     
    s = discretevariable("s",2)
    
    l = discretevariable("l",2)


    pd = discretefactor({d})
    pd[{d:0}] = 0.6
    pd[{d:1}] = 0.4

    pi = discretefactor({i})
    pi[{i:0}] = 0.7
    pi[{i:1}] = 0.3
    
    pgid=discretefactor({g,i,d})
    pgid[{g:0,i:0,d:0}]=0.3
    pgid[{g:0,i:0,d:1}]=0.005
    pgid[{g:0,i:1,d:0}]=0.9
    pgid[{g:0,i:1,d:1}]=0.5
    pgid[{g:1,i:0,d:0}]=0.4
    pgid[{g:1,i:0,d:1}]=0.25
    pgid[{g:1,i:1,d:0}]=0.08
    pgid[{g:1,i:1,d:1}]=0.3
    pgid[{g:2,i:0,d:0}]=0.3
    pgid[{g:2,i:0,d:1}]=0.7
    pgid[{g:2,i:1,d:0}]=0.002
    pgid[{g:2,i:1,d:1}]=0.2


    psi=discretefactor({s,i})
    psi[{s:0,i:0}]=0.95
    psi[{s:0,i:1}]=0.2
    psi[{s:1,i:0}]=0.05
    psi[{s:1,i:1}]=0.8

    plg=discretefactor({l,g})
    plg[{l:0,g:0}]=0.1
    plg[{l:0,g:1}]=0.4
    plg[{l:0,g:2}]=0.99
    plg[{l:1,g:0}]=0.9
    plg[{l:1,g:1}]=0.6
    plg[{l:1,g:2}]=0.01
  
    
    
    studentbn = factorset()
    studentbn.addfactor(pd)
    studentbn.addfactor(pi)
    studentbn.addfactor(pgid)
    studentbn.addfactor(psi)
    studentbn.addfactor(plg)
    
    
    return studentbn,(d,i,g,s,l)


#### below is the testing code

def runrobot():
    robotex,(c,x0,x1,r0,r1,l0,l1) = buildrobotex(0.1,0.2,0.05,0.1)
    robotquery = naiveinfval(robotex,{c},{r0:1,l0:1,r1:1,l1:1})
    return (robotquery,c)

def runstudent():
    studentex,(d,i,g,s,l) = buildstudentex()
    studentquery1 = naiveinf(studentex,{i},{l,s})
    studentquery2 = naiveinfval(studentex,{s},{d:0,l:1})
    return (studentquery1,studentquery2,(d,i,g,s,l))

if __name__ == '__main__':
    # note that rounding used in PS1 solutions will cause the answer to differ
    # from this one (computed without as much rounding) by a bit
    robotquery,_ = runrobot()
    print(robotquery)
    ## should return a factor where c=0 => 0.39676 and c=1 -> 0.603239


    ## it is up to you to figure out if these examples return the right values
    studentquery1,studentquery2,_ = runstudent()
    print(studentquery1)
    print(studentquery2)

## you should probably write your own tests, as we will be testing your
## code on different factorsets as well!
## but don't put them in here, or they will mess up the automatic
## testing -- write them on your own, but don't submit them!
