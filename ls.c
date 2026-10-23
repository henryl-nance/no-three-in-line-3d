// Local search for large no-three-in-line sets in the n x n x n grid.
// usage: ./ls n k_start seconds seed outprefix
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int n,N,NL; static int *lp,*lstart,*llen; static int *pl,*pstart,*pdeg;
static int *cnt,*c2,*c3,*in,*tabu; static long long it;
static unsigned long long rs; static unsigned rnd(){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (unsigned)(rs>>11);}
static int g(int a,int b){a=abs(a);b=abs(b);while(b){int t=a%b;a=b;b=t;}return a;}
static int id(int x,int y,int z){return (x*n+y)*n+z;}
static int ins(int x,int y,int z){return x>=0&&x<n&&y>=0&&y<n&&z>=0&&z<n;}
static void build(){int m=(n-1)/2,cap=1<<22; lp=malloc(sizeof(int)*cap*8); lstart=malloc(sizeof(int)*cap); llen=malloc(sizeof(int)*cap); int tot=0; NL=0;
 for(int a=-m;a<=m;a++)for(int b=-m;b<=m;b++)for(int c=-m;c<=m;c++){ if(!a&&!b&&!c)continue; if(g(g(a,b),c)!=1)continue;
  int f=a?a:(b?b:c); if(f<0)continue;
  for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){ if(ins(x-a,y-b,z-c))continue; int L=0,X=x,Y=y,Z=z; while(ins(X,Y,Z)){L++;X+=a;Y+=b;Z+=c;}
   if(L<3)continue; lstart[NL]=tot; llen[NL]=L; X=x;Y=y;Z=z; while(ins(X,Y,Z)){lp[tot++]=id(X,Y,Z);X+=a;Y+=b;Z+=c;} NL++; }}
 pdeg=calloc(N,sizeof(int)); for(int i=0;i<tot;i++)pdeg[lp[i]]++; pstart=malloc(sizeof(int)*(N+1)); pstart[0]=0; for(int p=0;p<N;p++)pstart[p+1]=pstart[p]+pdeg[p];
 pl=malloc(sizeof(int)*tot); int *fill=calloc(N,sizeof(int)); for(int l=0;l<NL;l++)for(int j=0;j<llen[l];j++){int p=lp[lstart[l]+j]; pl[pstart[p]+fill[p]++]=l;} free(fill);}
static int V; // total excess = sum max(0,cnt-2)
static void inc(int l){int a=++cnt[l]; int *q=lp+lstart[l],L=llen[l]; if(a==2)for(int j=0;j<L;j++)c2[q[j]]++; else if(a==3)for(int j=0;j<L;j++)c3[q[j]]++; if(a>=3)V++;}
static void dec(int l){int a=cnt[l]--; int *q=lp+lstart[l],L=llen[l]; if(a==2)for(int j=0;j<L;j++)c2[q[j]]--; else if(a==3)for(int j=0;j<L;j++)c3[q[j]]--; if(a>=3)V--;}
static void add(int p){in[p]=1; for(int i=pstart[p];i<pstart[p+1];i++)inc(pl[i]);}
static void rem(int p){in[p]=0; for(int i=pstart[p];i<pstart[p+1];i++)dec(pl[i]);}
int main(int argc,char**argv){ n=atoi(argv[1]); int k=atoi(argv[2]); double secs=atof(argv[3]); rs=0x9E3779B97F4A7C15ULL^(unsigned long long)atoll(argv[4])*2654435761ULL; char*pre=argv[5];
 N=n*n*n; build(); fprintf(stderr,"n=%d points=%d lines=%d\n",n,N,NL);
 cnt=calloc(NL,sizeof(int)); c2=calloc(N,sizeof(int)); c3=calloc(N,sizeof(int)); in=calloc(N,sizeof(int)); tabu=calloc(N,sizeof(int));
 int *mem=malloc(sizeof(int)*N); V=0;
 // greedy random start
 int *perm=malloc(sizeof(int)*N); for(int i=0;i<N;i++)perm[i]=i; for(int i=N-1;i>0;i--){int j=rnd()%(i+1);int t=perm[i];perm[i]=perm[j];perm[j]=t;}
 int sz=0; for(int i=0;i<N&&sz<k;i++){int p=perm[i]; if(c2[p]==0){add(p);sz++;}} for(int i=0;i<N&&sz<k;i++){int p=perm[i]; if(!in[p]){add(p);sz++;}}
 int best=0; clock_t t0=clock(); long long lastimp=0;
 for(it=1;;it++){
  if(V==0){ if(sz>best){best=sz; char fn[256]; sprintf(fn,"%s_n%d_%d.txt",pre,n,best); FILE*f=fopen(fn,"w"); for(int p=0;p<N;p++)if(in[p])fprintf(f,"%d %d %d\n",p/(n*n),(p/n)%n,p%n); fclose(f);
      fprintf(stderr,"[%.1fs it=%lld] found %d\n",(double)(clock()-t0)/CLOCKS_PER_SEC,it,best); lastimp=it;}
    // grow: add least-conflicting outside point
    int bq=-1,bs=1<<30,ties=0; for(int q=0;q<N;q++)if(!in[q]){int s=c2[q]; if(s<bs){bs=s;bq=q;ties=1;}else if(s==bs&&rnd()%(++ties)==0)bq=q;}
    add(bq); sz++; continue; }
  if((it&1023)==0 && (double)(clock()-t0)/CLOCKS_PER_SEC>secs)break;
  // pick conflicted member with max c3 (not tabu), random walk 3%
  int m=0; for(int p=0;p<N;p++)if(in[p]&&c3[p]>0)mem[m++]=p;
  int bp; if(rnd()%100<3) bp=mem[rnd()%m]; else { int bv=-1,ties=0; bp=mem[0]; for(int i=0;i<m;i++){int p=mem[i]; if(tabu[p]>it)continue; int v=c3[p]; if(v>bv){bv=v;bp=p;ties=1;}else if(v==bv&&rnd()%(++ties)==0)bp=p;} }
  rem(bp); tabu[bp]=it+7+rnd()%10;
  int bq=-1,bs=1<<30,ties=0; for(int q=0;q<N;q++)if(!in[q]&&q!=bp&&tabu[q]<=it){int s=c2[q]; if(s<bs){bs=s;bq=q;ties=1;}else if(s==bs&&rnd()%(++ties)==0)bq=q;}
  if(bq<0)bq=bp; add(bq); tabu[bq]=it+3+rnd()%5;
 }
 printf("n=%d best=%d iters=%lld\n",n,best,it); return 0;}
