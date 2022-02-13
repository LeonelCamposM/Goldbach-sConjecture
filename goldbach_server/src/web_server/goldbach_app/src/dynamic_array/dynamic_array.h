// Copyright 2021 Jeisson Hidalgo-Cespedes <jeisson.hidalgo@ucr.ac.cr> CC-BY-4

#ifndef DYNAMIC_ARRAY_H
#define DYNAMIC_ARRAY_H

#include <inttypes.h>
#include <math.h>
#include <stddef.h>

/**
 * @brief create empty dinamyc_array
 */
typedef struct dynamic_array {
  size_t capacity;
  size_t count;
  int64_t* elements;
}dynamic_array_t;

/**
 * @brief Initializes an empty dynamic array
 * @param array A pointer to the array
 * @return An integer, indicating if there was an error
 */
int array_init(dynamic_array_t* array);

/**
 * @brief Destroys a dynamic array
 * @param array A pointer to the array
 * @return NA
 */
void array_destroy(dynamic_array_t* array);

/**
 * @brief Adds an element to the dynamic array
 * @param array A pointer to the array
 * @param element The new element
 * @return An integer, indicating if there was an error
 */
int array_append(dynamic_array_t* array, int64_t element);

/**
 * @brief print stored elements in array
 * @param array A pointer to the array
 */
void array_print(dynamic_array_t* array);

#endif  //  DYNAMIC_ARRAY_H
