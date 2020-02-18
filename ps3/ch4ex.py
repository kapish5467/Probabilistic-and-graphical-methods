from factor import *

# to use factor:
#  construct the discrete variables using "discretevariable" (see below)
#  calling discretevariable multiple times (even with the same arguments)
#   will produce different variables (just with the same name)
#  note that all variables have values of 0, 1, 2, ... (instead of 
#           special symbols like c^2 in the book)
#  
#  a *scope* is 
#   a set of variables (eg {x,y} if x and y are results of discretevariable)
#  an *assignment* is
#   a dictionary mapping variables to integers (eg {x:0, y:3})
#
#
# create a factor using discretefactor (passing in a scope)
#
# assign values using f[a] = val where
#   f is a discretefactor
#   a is an assignment (see above)
#   v is a value (real value, double/float)
#
# + , -, *, / all exist for factors, as defined in the book
#
# f.scope evaluates to the scope of the factor f
#
# to reduce use g = f.reduce(a) where
#   g is now the reduced version of f based on assignment a
#
# to marginalize, use g = f.marginalize(s) where
#   g is now the marginalized version of f with varibles in scope s
#       have been marginalized (summed) out

# below are examples to reproduce those in the book:

def fig41(printit=True):
    a = discretevariable("a",2)
    b = discretevariable("b",2)
    c = discretevariable("c",2)
    d = discretevariable("d",2)

    phi1 = discretefactor({a,b})
    phi1[{a:0,b:0}] = 30
    phi1[{a:0,b:1}] = 5
    phi1[{a:1,b:0}] = 1
    phi1[{a:1,b:1}] = 10

    phi2 = discretefactor({b,c})
    phi2[{b:0,c:0}] = 100
    phi2[{b:0,c:1}] = 1
    phi2[{b:1,c:0}] = 1
    phi2[{b:1,c:1}] = 100

    phi3 = discretefactor({c,d})
    phi3[{c:0,d:0}] = 1
    phi3[{c:0,d:1}] = 100
    phi3[{c:1,d:0}] = 100
    phi3[{c:1,d:1}] = 1

    phi4 = discretefactor({a,d})
    phi4[{d:0,a:0}] = 100
    phi4[{d:0,a:1}] = 1
    phi4[{d:1,a:0}] = 1
    phi4[{d:1,a:1}] = 100

    if printit:
        print("Figure 4.1:")
        print(phi1)
        print(phi2)
        print(phi3)
        print(phi4)

    return (a,b,c,d,phi1,phi2,phi3,phi4)

def fig42(printit=True):
    (a,b,c,d,phi1,phi2,phi3,phi4) = fig41(False)

    unnorm = phi1*phi2*phi3*phi4
    z = unnorm.marginalize({a,b,c,d})
    norm = unnorm / z

    if printit:
        print("Figure 4.2:")
        print(unnorm)
        print(norm)
        print("normalization constant is %g" % z[{}])
        print("")

    return (a,b,c,d,norm)

def ex42(printit=True):

    (a,b,c,d,joint) = fig42(False)

    abmarg = joint.marginalize({c,d})

    if printit:
        print("Example 4.2:")
        print(abmarg)

    return (a,b,abmarg)

def fig43(printit=True):
    a = discretevariable("a",3)
    b = discretevariable("b",2)
    c = discretevariable("c",2)

    phi1 = discretefactor({a,b})
    phi1[{a:0,b:0}] = 0.5
    phi1[{a:0,b:1}] = 0.8
    phi1[{a:1,b:0}] = 0.1
    phi1[{a:1,b:1}] = 0.0
    phi1[{a:2,b:0}] = 0.3
    phi1[{a:2,b:1}] = 0.9

    phi2 = discretefactor({b,c})
    phi2[{b:0,c:0}] = 0.5
    phi2[{b:0,c:1}] = 0.7
    phi2[{b:1,c:0}] = 0.1
    phi2[{b:1,c:1}] = 0.2

    phi12 = phi1*phi2

    if printit:
        print("Figure 4.3:")
        print(phi1)
        print(phi2)
        print(phi12)

    return (a,b,c,phi12)


def fig45(printit=True):
    (a,b,c,phi12) = fig43(False)

    phinew = phi12.reduce({c:0})

    if printit:
        print("Figure 4.5:")
        print(phinew)

fig41()
fig42()

ex42()

fig43()
fig45()
