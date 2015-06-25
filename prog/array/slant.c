#include <ipps.h>
#include "utils.h"
#include "numc.h"

int main(int argc,char *argv[])
{
	int n,m,i=0,j,k,id;
	SacTrace *st;
	int p=0,np=100,cn,shift;
	float *u,cd,delta,delay,*ut,add,tmp,b,e;
	Ipp32fc *ht;
	char *cst;
	FILE *fp;
	char *path,*output,wf[128];
	/*variables related with intel ipp */
	IppStatus status;
	IppsHilbertSpec_32f32fc* spec;
	
	if (argc !=4 ){
		printf("usage: slant path cstation output.\n");
		exit(0);
	}
	else{
		path=argv[1];
		cst=argv[2];
		output=argv[3];

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
	
	u=(float *)malloc(np*sizeof(float));

	ut=(float *)malloc(np*m*sizeof(float));
	ht=(Ipp32fc *)malloc(m*sizeof(Ipp32fc *));
	memset(ut,0,np*m);

	linspace(p-2.0,p+2.0,np,u);
	delta=st[cn].hd.delta;
	cd=st[cn].hd.gcarc;
	b=st[cn].hd.b;
	e=st[cn].hd.e;

	/*perform the shift and stack */
	for (k=0;k<np;k++)
	{
		for (i=0;i<n;i++)
		{
			delay=(cd-st[i].hd.gcarc)*u[k];
			tmp=(delay/delta);
			shift=(int)tmp;
			for (j=0;j<m;j++)
			{
				if (j>=shift && (j-shift)<m)
					add=st[i].data[j-shift];
				else
					add=0;
				ut[k*m+j]+=add;
			}
		}
	}

	for (k=0;k<np*m;k++)
		ut[k]=ut[k]/n;

	strcpy(wf,output);
	strcat(wf,"_wf");

	fp=fopen(wf,"w");
	fwrite(ut,sizeof(float),np*m,fp);
	fclose(fp);
	
	ippStaticInit();

	status = ippsHilbertInitAlloc_32f32fc(&spec,m,ippAlgHintNone);

	for (i=0;i<np;i++)
	{
		status = ippsHilbert_32f32fc(&ut[i*m],ht,spec);
		ippsMagnitude_32fc((Ipp32fc*)ht,&ut[i*m],m);
	}
	ippsHilbertFree_32f32fc(spec);

	
	fp=fopen(output,"w");
	fwrite(ut,sizeof(float),np*m,fp);
	fclose(fp);
	/*output time and slowness extent */
	printf("%.2f %.2f -2 2\n",b,e);
	/*output maxtrix dimension */
	printf("%d %d\n",n,m);
	free(u);
	free(st);
	free(ut);
	return 0;
}
