CC=gcc
CFLAGS=-D TEST

test_ll_equal: test_ll_equal.c
	$(CC) $(CFLAGS) -o $@ $?

test_ll_cycle: test_ll_cycle.c
	$(CC) $(CFLAGS) -o $@ $?

.PHONY: clean

clean:
	$(RM) test_ll_equal test_ll_cycle
	
autograder-clean:
	rm -rf test_ll_equal.c test_ll_cycle.c grading/__pycache__

