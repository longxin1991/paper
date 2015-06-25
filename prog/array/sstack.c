#include "utils.h"
#include "numc.h"

int main(int argc,char *argv[])
{
	int n,m,i=0,j,k,id;
	SacTrace *st;
	int p=0,cn,shift;
	float cd,delta,delay,*ut,add,tmp,b,e;
	char *cst;
	char *path,*output,wf[128];
	/*variables related with intel ipp */
	
	if (argc !=5 ){
		printf("usage: slant path cstation slowness output.\n");
		exit(0);
	}
	else{
		path=argv[1];
		cst=argv[2];
		p=atof(argv[3]);
		output=argv[4];

	}

	/*decide method of read data*/
	ftype(path,&id);
	switch(id){
		case 0: st=readsacdir(path,&n,&m); break;
		case 1: st=readflist(path,&n,&m); break;
		default : printf("Fail to read data.") ; exit(EXIT_FAILURE);break; 
	}
	/*obtain the staking centeral station */
	while(strcmp(cst,st[i].hd.kstnm))
		i++;
	cn=i;

	ut=(float *)malloc(m*sizeof(float));
	memset(ut,0,m);

	delta=st[cn].hd.delta;
	cd=st[cn].hd.gcarc;
	b=st[cn].hd.b;
	e=st[cn].hd.e;

	/*perform the shift and stack */
		for (i=0;i<n;i++)
		{
			delay=(cd-st[i].hd.gcarc)*p;
			tmp=(delay/delta);
			shift=(int)tmp;
			for (j=0;j<m;j++)
			{
				if (j>=shift && (j-shift)<m)
					add=st[i].data[j-shift];
				else
					add=0;
				ut[j]+=add;
			}
		}

	for (k=0;k<m;k++)
		ut[k]=ut[k]/n;

	write_sac(output,st[cn].hd,ut);	
	/*output maxtrix dimension */
	printf("%d %d\n",n,m);
	free(st);
	free(ut);
	return 0;
}
