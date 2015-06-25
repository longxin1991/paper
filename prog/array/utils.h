#include "dtype.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <dirent.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

int linenum(const char *f);

void ftype(const char *path, int *id);

SacTrace *readsacdir(const char *path,int *n,int *m);

SacTrace *readflist(const char *flist,int *n,int *m);

