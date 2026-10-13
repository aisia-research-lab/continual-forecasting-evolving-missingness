"""Reproduce finite-N signed-observation minimax calculation."""
import argparse,math

def exact(N,a,alpha,horizons,weights=None):
    if not 0<a<1 or not 0<alpha<1 or N<0: raise ValueError('invalid parameters')
    hs=list(horizons); ws=list(weights or [1.]*len(hs))
    if len(hs)!=len(ws): raise ValueError('horizon/weight mismatch')
    q=a*a*sum(w*(1-alpha)**(2*h) for w,h in zip(ws,hs))
    eta=math.log((1+a)/(1-a))
    risk=0.0
    for k in range(N+1):
        comb=math.comb(N,k)
        pp=comb*((1+a)/2)**k*((1-a)/2)**(N-k)
        pm=comb*((1-a)/2)**k*((1+a)/2)**(N-k)
        sech2=1/math.cosh(eta*(2*k-N)/2)**2
        risk+=0.5*(pp+pm)*sech2
    return q*risk

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--N',nargs='+',type=int,required=True)
    ap.add_argument('--a',type=float,default=.28);ap.add_argument('--alpha',type=float,default=.2)
    ap.add_argument('--horizons',type=int,nargs='+',default=[1,3,6])
    args=ap.parse_args()
    for n in args.N:print(f'N={n:3d} exact_risk={exact(n,args.a,args.alpha,args.horizons):.9f}')
if __name__=='__main__':main()
