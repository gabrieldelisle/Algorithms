from random import random
from numpy import exp, pi

class Polynomial(object) :
    def __init__(self, s) :
        if type(s) ==list :
            self.coeffs = s
            self.simplify()
        elif type(s) == Polynomial :
            self.coeffs = []
            for i in range(len(s.coeffs)) :
                self.coeffs.append(s.coeffs[i])
        elif type(s) == int or type(s) == float or type(s) == complex:
            if s==0 :
                self.coeffs=[]
            else :
                self.coeffs = [s]
         
    
    def __repr__(self) :
        s=""
        if self.degree()<0 :
            s='0'
        else :
            for i in range (len(self.coeffs)-1,-1,-1) :
                if self.coeffs[i]!=0 :
                    if self.coeffs[i]>0 and i<len(self.coeffs):
                        s+='+'
                    elif self.coeffs[i]<0 :
                        s+='-'
                    if i==0 or abs(self.coeffs[i]) !=1 :
                        s+=str(abs(self.coeffs[i]))
                    if i>0 :
                        s+='X'
                    if i>1 :
                        s+="^"
                        s+=str(i)
            if s[0]=='+' :
                s=s[1:]
        return s

    def __getitem__(self, index):
        return self.coeffs[index]

    def __setitem__(self, index, valeur):
        self.coeffs[index] = valeur

    def copy(self) :
        return Polynomial(self)

    def simplify(self) :
        while self.coeffs!=[] and self[len(self.coeffs)-1]==0 :
            del(self.coeffs[len(self.coeffs)-1])
        return self

    def degree(self) :
        return len(self.coeffs)-1

    def __add__(self,b) :
        if type(b) == int or type(b) == float or type(b) == complex:
            return self+Polynomial(b)
        else :
            la=len(self.coeffs)
            lb=len(b.coeffs)
            poly=Polynomial(0)
            for i in range(min(la,lb)) :
                poly.coeffs.append(self[i])
                poly.coeffs[i] += b.coeffs[i]
            if lb>la :
                for i in range(la,lb) :
                    poly.coeffs.append(b[i])
            else :
                for i in range(lb,la) :
                    poly.coeffs.append(self[i])
            return poly.simplify()

    def __sub__(self,b) :
        if type(b) == int or type(b) == float or type(b) == complex:
            return self-Polynomial(b)
        else :
            la=len(self.coeffs)
            lb=len(b.coeffs)
            poly=Polynomial(0)
            for i in range(min(la,lb)) :
                poly.coeffs.append(self[i])
                poly[i] -= b[i]
            if lb>la :
                for i in range(la,lb) :
                    poly.coeffs.append(-b[i])
            else :
                for i in range(lb,la) :
                    poly.coeffs.append(self[i])
            return poly.simplify()

    def __eq__(self, b) :
        if b==0 :
            return self.degree()==-1
        else :
            return self-b==0

    def __mul__(self, b) :
        if type(b) == int or type(b) == float or type(b) == complex:
            poly = self.copy()
            for i in range(len(self.coeffs)) :
                poly[i] = poly[i]*b
            return poly
        else :
            poly = Polynomial(0)
            for i in range(len(self.coeffs)) :
                p=Polynomial(0)
                p.coeffs = i*[0]+(self[i]*b).coeffs
                poly = poly+p
            return poly.simplify()
        
    def __rmul__(self,b) :
        return(self*b)

    def __truediv__(self,b) :
        return 1/b*self
    
    def __floordiv__(self,b) :
        q=Polynomial(0)
        r=self.copy()
        while r.degree() >= b.degree() :
            q = q + r[r.degree()]/b[b.degree()]*X**(r.degree()-b.degree())
            r = self - b*q
        return q.simplify()

    def __mod__(self,b) :
        q=Polynomial(0)
        r=self.copy()
        while r.degree() >= b.degree() :
            q = q + r[r.degree()]/b[b.degree()]*X**(r.degree()-b.degree())
            r = self - b*q
        return r.simplify()

    def __pow__(self, n) :
        if n == 1 :
            return self
        elif n==0 :
            return Polynomial(1)
        elif self==X :
            return Polynomial(n*[0]+[1])
        else :
            return (self**(n//2))*(self**(n-n//2))
                                  
    def value(self,t) :
        s=0
        for i in range(len(self.coeffs)) :
            s=t*s+self.coeffs[len(self.coeffs)-1-i]
        return s

    def derivative(self, n=1) :
        if n==0 :
            return self
        else :
            coeffs = [0]* (len(self.coeffs)-1)
            for i in range(len(self.coeffs)-1) :
                coeffs[i] = self.coeffs[i+1]*(i+1)
            return Polynomial(coeffs).derivative(n-1)

    def integral(self, n=1) :
        if n==0 :
            return self
        else :
            coeffs = [0]* (len(self.coeffs)+1)
            for i in range(1, len(self.coeffs)+1) :
                coeffs[i] = self.coeffs[i-1]/i
            return Polynomial(coeffs).integral(n-1)

    def gcd(a,b) :
        if a.degree()>b.degree():
            p=a.copy()
            q=b.copy()
        else :
            q=a.copy()
            p=b.copy()
        while q!=0:
            p,q = q,p%q
        p.simplify()
        return 1/p[p.degree()]*p



def lagrange(x,y) :
    # Lagrange Polynomial goes through each point (x,y) 
    s=Polynomial(0)
    for j in range(len(x)) :
        t=Polynomial(1)
        for k in range(len(x)) :
            if k!=j :
                t*=(X-x[k])/(x[j]-x[k])
        s+=y[j]*t
    return s

# care: X is a reserved name for polynomial X
X = Polynomial([0,1])

if __name__ == '__main__':
    print((X**2-1).integral())
    print((3*X**2+1).derivative())

    p1 = (4*X+1)**2
    p2 = X**2+1
    p3 = X**2-4
    p4 = p1*p2
    p5 = p1*p3
    print("gcd of", p4, "and", p5, "is", Polynomial.gcd(p4, p5), "\n")

    x,y = [1,2,3],[1,4,9]
    
    for i in range(3) :
        print(x[i],"->",y[i])

    p6 = lagrange(x,y)
    print("next ones are :")
    for i in range(4,6) :
        print(i,"->",p6.value(i))
