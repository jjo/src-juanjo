# $Header: /home/jjo/cvs.juanjo/jjotip/jjotip-sharedobjs.d/Makefile,v 1.3 2004/10/26 14:06:03 jjo Exp $
#
#1. Compilar lib:
#    make lib
#2. Compilar aplicacion:
#    make all
#3. Prueba fallida:
#    make badtest
#4. Prueba ok:
#    make test
CFLAGS=-g -Wall -fPIC   ## importante: -fPIC
LIBS=libjjo.so		## nombre de la lib
LIBOBJS=jjoprint.o	## objs de la lib.
TARGET=jjomain		## nombre del ejecutable
OBJS=jjomain.o		## objs del ejecutable

LDFLAGS=-L.		## buscar en . la lib en tiempo de enlace
LDLIBS=-ljjo		## enlazar con  lib<jjo>.so

all : $(TARGET)

lib: $(LIBS)

$(TARGET): $(OBJS) $(LIBS)
	$(CC) -o $(@) $(LDFLAGS) $(LDLIBS) $(OBJS)

$(LIBS): $(LIBOBJS)
	$(LD) -soname libjjo.so.0.1 -shared -o $(@) $^
	ldconfig -l $(@)
	ls -al $(@)*

badtest: $(TARGET)
	./$(TARGET)
test: $(TARGET)
	@echo "** IMPORTANTISIMO: LD_LIBRARY_PATH apuntando a dir. donde"
	@echo "** esta' el .so (si NO voy a instalar el .so en /lib o /usr/lib)"
	export LD_LIBRARY_PATH=.; ./$(TARGET)
clean: 	
	rm -f $(TARGET) $(OBJS) $(LIBOBJS) *.o *.so *.so.*
