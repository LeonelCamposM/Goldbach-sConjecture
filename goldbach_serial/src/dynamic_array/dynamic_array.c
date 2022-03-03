// Copyright 2021 Jeisson Hidalgo-Cespedes <jeisson.hidalgo@ucr.ac.cr> CC-BY-4

#include <assert.h>
#include <stdlib.h>
#include <inttypes.h>
#include <math.h>
#include <stdio.h>

#include "dynamic_array.h"

dynamic_array_t* array_create(){
  dynamic_array_t* array = (dynamic_array_t*)
      calloc(1, sizeof(dynamic_array_t));
  array_init(array);
  return array;
}

int array_init(dynamic_array_t* array) {
  assert(array);
  array->capacity = 0;
  array->count = 0;
  array->elements = NULL;
  return EXIT_SUCCESS;
}

void array_destroy(dynamic_array_t* array) {
    assert(array);
    array->capacity = 0;
    array->count = 0;
    free(array->elements);
}

int array_increase_capacity(dynamic_array_t* array) {
  size_t new_capacity = 10 *(array->capacity ? array->capacity : 1);
  int64_t* new_elements = (int64_t*)
  realloc(array->elements, new_capacity * sizeof(int64_t));
  if (new_elements) {
    array->capacity = new_capacity;
    array->elements = new_elements;
    return EXIT_SUCCESS;
  } else {
    return EXIT_FAILURE;
  }
}

int array_append(dynamic_array_t* array, int64_t element) {
  assert(array);
  if (array->count == array->capacity) {
    if (array_increase_capacity(array) != EXIT_SUCCESS) {
      return EXIT_FAILURE;
    }
  }
  array->elements[array->count++] = element;
  return EXIT_SUCCESS;
}

void array_print(dynamic_array_t* array){
  for (size_t i = 0; i < array->count; i++)
  {
    printf("%" PRIi64 " + ", array->elements[i]);
  }
}
