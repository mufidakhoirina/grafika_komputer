x1,y1 = (0,0)
x2,y2 = (5,3)

kx = []
ky = []

lkh = max(x1,x2,y1,y2)
dx = x2 / lkh
dy = y2 / lkh

x=x1; y=y1
for l in range (lkh+1):
    kx.append(round(x))
    x=x+dx
    ky.append(round(y))
    y=y+dy
    
koor = set(zip(kx,ky))

for a in range (10):
    for b in range(10):
        if (b,a) in koor: print("#",end=" ")
        else: print(" ",end=" ")
    print("")