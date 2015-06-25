ifndef CC
	CC: gcc
endif

IPPLIB := -static -lipps -lippvm -lippcore -lm
CFLAGS := -w
OBJ := sacio.o numc.o utils.o 

all:pws slant spws sstack


slant:%:%.o $(OBJ) 
	$(CC) $^ $(CFLAGS) $(IPPLIB) -o $@

pws:%:%.o $(OBJ)
	$(CC) $^ $(CFLAGS) $(IPPLIB) -o $@

sstack:%:%.o $(OBJ)
	$(CC) $^ $(CFLAGS) -lm -o $@

spws:%:%.o $(OBJ)
	$(CC) $^ $(CFLAGS) $(IPPLIB) -o $@

%o.:%.c

clean:
	rm pws slant sslant *.o
