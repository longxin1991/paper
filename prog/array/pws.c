#include <ipps.h>
#include <ippvm.h>
#include "numc.h"
#include "utils.h"

int main(int argc,char *argv[])
{
	int n,m,i=0,j,k,id;
	SacTrace *st;
	int p=0,np=100,cn,shift;
	float *u,cd,delta,delay,*ut,*at,u_add,tmp,b,e,*ph;
	Ipp32fc *ht,*pt,p_add;
	Ipp32f v = 2.0;
	char *path,*output,*cst,wf[128];
	FILE *fp;
	/*variables related with intel ipp */
	IppStatus status;
	IppsHilbertSpec_32f32fc* spec;

	if (argc !=4 ){
		printf("usage:pws path cstation output.\n");
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

	/*allocate memory */
	u=(float *)malloc(np*sizeof(float));

	ut=(float *)malloc(np*m*sizeof(float));
	at=(float *)malloc(m*sizeof(float));
	pt=(Ipp32fc *)malloc(np*m*sizeof(Ipp32fc *));
	ph=(Ipp32f *)malloc(np*m*sizeof(Ipp32f *));
	ht=(Ipp32fc *)malloc(m*sizeof(Ipp32fc *));
	memset(ut,0,np*m*sizeof(float));
	memset(pt,0,np*m*sizeof(float));

	linspace(p-2.0,p+2.0,np,u);
	delta=st[cn].hd.delta;
	cd=st[cn].hd.gcarc;
	b=st[cn].hd.b;
	e=st[cn].hd.e;

	status = ippsHilbertInitAlloc_32f32fc(&spec,m,ippAlgHintNone);
	/*perform the shift and stack */
	for (k=0;k<np;k++)
	{
		for (i=0;i<n;i++)
		{
			delay=(cd-st[i].hd.gcarc)*u[k];
			tmp=(delay/delta);
			shift=(int)tmp;

			/*perform hilbert tranform */
			status = ippsHilbert_32f32fc(st[i].data,ht,spec);
			ippsMagnitude_32fc((Ipp32fc*)ht,at,m);
			for (j=0;j<m;j++)
			{
				ht[j].im=ht[j].im/at[j];
				ht[j].re=ht[j].re/at[j];
			}
			for (j=0;j<m;j++)
			{
				if (j>=shift && (j-shift)<m)
				{
					u_add=st[i].data[j-shift];
					p_add=ht[j-shift];
				}
				else
				{
					u_add=0;
					p_add.im=0;
					p_add.re=0;
				}
				ut[k*m+j]+=u_add;
				pt[k*m+j].im+=p_add.im;
				pt[k*m+j].re+=p_add.re;
			}
		}
	}

	ippsMagnitude_32fc((Ipp32fc*)pt,ph,np*m);
	for (k=0;k<np*m;k++)
		ph[k]=ph[k]/n;
	
	status = ippsPowx_32f_A21(ph,v,ph,np*m);

	for (k=0;k<np*m;k++)
			ut[k]=ut[k]*ph[k]/n;

	strcpy(wf,output);
	strcat(wf,"_wf");

	fp=fopen(wf,"w");
	fwrite(ut,sizeof(float),np*m,fp);
	fclose(fp);

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
	free(at);
	free(ht);
	free(pt);
	free(ph);
	return 0;
}
