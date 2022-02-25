CC=cc
CXX=g++
DEFS=
FLAGS=-g -Wall -Wextra $(DEFS) -fopenmp -shared -fPIC
CFLAGS=$(FLAGS) -std=gnu11
CXXFLAGS=$(FLAGS) -std=gnu++11
LIBS=-pthread -lm

SRC := /src
APPNAME=goldbach_omp
SRC_DIR := $(APPNAME)$(SRC)

DIRS=$(shell find $(SRC_DIR) -type d)
HEADERS:=$(wildcard $(DIRS:%=%/*.h))
SOURCES:=$(wildcard $(DIRS:%=%/*.c))
OBJECTS=$(SOURCES:src/%.c=build/%.o)
INCLUDES=$(DIRS:%=-I%)

.SECONDEXPANSION:

bin/$(APPNAME): $(OBJECTS) | $$(@D)/.
	$(CC) $(CFLAGS) $(INCLUDES) $^ -o bin/lib_$(APPNAME).so $(LIBS)

build/%.o: src/%.c $(HEADERS) | $$(@D)/.
	$(CC) -c $(CFLAGS) $(INCLUDES) $< -o $@ $(LIBS)

.PRECIOUS: %/.
%/.:
	mkdir -p $(dir $@)

all: bin/$(APPNAME)
