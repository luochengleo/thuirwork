CC   =gcc  -g -O -c -o $@ -DOUTERR
LC   =gcc -o $@

ntcir_eval: ntcir_eval.o
	$(LC) ntcir_eval.o -lm

ntcir_eval.o: ntcir_eval.c ntcir_eval.h
	$(CC) ntcir_eval.c
