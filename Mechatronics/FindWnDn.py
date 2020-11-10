import numpy as np
import math

# * Find dn, wn
print(-np.log(0.050872)/np.pi)


def calculatedwcl(Max, TS, revol=5):
    percent_OS = (Max - revol)/revol
    tantheta = -np.log(percent_OS)/np.pi
    theta = np.arctan(tantheta)
    dcl = np.sin(theta)
    Wcl = 4/(dcl*TS)

    return dcl, Wcl


d1, w1 = calculatedwcl(5.2546, 0.934)  # * 100
d2, w2 = calculatedwcl(5.194445, 0.872)  # * 200
d3, w3 = calculatedwcl(5.18055, 0.842)  # *300


def calculatewndn(dcl, wcl, K):
    wn = wcl/np.sqrt(1+K)
    dn = dcl*np.sqrt(1+K)
    return dn, wn


a = 10000
for _ in range(3):
    x = np.random.randint(-50, 100000000)
    Matrix = np.zeros((3, 2))
    Matrix[0] = calculatewndn(d1, w1, 100+x)
    Matrix[1] = calculatewndn(d2, w2, 200+x)
    Matrix[2] = calculatewndn(d3, w3, 300+x)
# * 코드 수정!!!
    loss = np.sum(np.std(Matrix, axis=0))
    print(np.std(Matrix), loss)
    if loss < a:
        a = loss
        k = x
print(k)
