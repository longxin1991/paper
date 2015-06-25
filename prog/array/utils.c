#include "dtype.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <dirent.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

int linenum(const char *f)
{
	int i=0;
	FILE *fp;
	char line[128];

	if((fp=fopen(f,"r"))==NULL)
	{
		printf("linenum: open %s failed.\n",f);
		exit(-1);
	}
	
	while((fgets(line,128,fp)) != NULL )
		i++;

	fclose(fp);
	return i;
}

SacTrace *readsacdir(const char *path,int *n,int *m)
{
	DIR *d;
	SACHEAD hd;
	struct dirent *file;
	int i=0;
	char *fname,cmd[128],line[10];
	SacTrace *st;
	FILE *fp;
	
	strcpy(cmd,"ls ");
	strcat(cmd,path);
	strcat(cmd,"|wc -l");
	fp=popen(cmd,"r");

	if (fgets(line,5,fp) == NULL)
		exit(-1);
	fclose(fp);

	*n=atoi(line);
	st=(SacTrace *)malloc((*n)*sizeof(SacTrace));
	if (!(d = opendir(path)))
	{
		printf("Error to open dir %s!\n",path);
		exit(0);
	}
	else
		chdir(path);

	while((file=readdir(d)) != NULL)
	{
		if (strncmp(file->d_name,".",1) == 0)
			continue;
		fname=file->d_name;
		st[i].data=read_sac(fname,&st[i].hd);
		i++;
	}
	*m=st[0].hd.npts;
	chdir("..");
	closedir(d);
	return st;
}

SacTrace *readflist(const char *flist,int *n,int *m)
{
	int i=0,fn,len;
	FILE *fp;
	char fname[128];
	SACHEAD hd;
	SacTrace *st;
	fn=linenum(flist);
	*n=fn;

	st=(SacTrace *)malloc(fn*sizeof(SacTrace));

	if((fp=fopen(flist,"r"))==NULL)
	{
		printf("linenum: open %s failed.\n",flist);
		exit(-1);
	}

	while((fgets(fname,128,fp)) != NULL )
	{	
		len=strlen(fname);
		fname[len-1]='\0';
		st[i].data=read_sac(fname,&st[i].hd);
		i++;
	}
	*m=st[0].hd.npts;
	fclose(fp);
	
	return st; 
}

void ftype(const char *path, int *id)
{
    struct stat buf;
    if( stat(path,&buf)==-1)
    {   
        perror("stat");
        exit(EXIT_FAILURE);
    }   

    switch(buf.st_mode & S_IFMT){
        case S_IFDIR : *id=0; break;
        case S_IFREG : *id=1; break;
        default : *id=-1; break;
    }   
}
