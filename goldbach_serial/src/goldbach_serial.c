#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "dynamic_array.h"

#define STARTVALUE 2

/**
 * @brief Generic function to report an error
 */
void report_and_exit(bool error_condition, char* report_name);

/**
* @return True if n is prime
*/
bool is_prime(int64_t n);

/**
*@brief print the sums of the strong goldbach conjecture 
*@details works with 64-bit positive integers > 5
*@param number to verify
*@return ptr to array made up of the addends found
*/
dynamic_array_t* strongConjecture(int64_t number);

/**
*@brief print the sums of the weak goldbach conjecture 
*@details works with 64-bit positive integers > 5
*@param number to verify
*@return ptr to array made up of the addends found
*/
dynamic_array_t* weakConjecture(int64_t number);

/**
*@brief show all addings stored in array
*@param array to print
*@param num_addings : number of addings
*@param sums : amount of sums 
*/
void show_addings(int64_t* array, int num_addings, int sums);

/**
*@brief gives the format to the output for the user
*@param array to print
*@param sums : amount of sums
*@param number being broken down
*@param list : true = list false = don't list
*@param num_addings : number of addings 
*/
void show_goldbach_results(dynamic_array_t* array, int sums, int64_t number, bool list, int num_addings);

/**
*@brief validate user input
*@param value input
*/
bool analize_arguments(int64_t value);

/**
*@brief append a message or a number in Output.txt file
*@param mesage message to be writen
*@param number number to be writen
*@param number_flag true append the number, false append the message
*/
int write_output(char* mesage, size_t number, bool number_flag);

/**
*@brief get goldbach sums of a value
*@param value number 
*/
void calculate_number(int64_t value);

/**
*@brief get goldbach sums of a array
*@param input_numbers number 
*/
void calculate_array(dynamic_array_t* input_numbers);

void report_and_exit(bool error_condition, char* report_name) {
  if (error_condition == true) {
    printf("An error occurred with ");
    printf("%s", report_name);
    assert(error_condition != false);
    exit(EXIT_FAILURE);
  }
}

bool is_prime(int64_t n) {
  bool signal = true;
  const int64_t max = sqrt(n);
  int64_t iter = 2;
  while (iter <= max) {
    if (n%iter == 0) {
      signal = false;
      break;
    }
  iter += 1;
  }
  return signal;
}

dynamic_array_t* strong_conjecture(int64_t number) {
  dynamic_array_t* addings = (dynamic_array_t*)
      calloc(1, sizeof(dynamic_array_t));
  array_init(addings);
  report_and_exit (addings == NULL, "strong_conjecture\n");
  
  for (int64_t first_adding = STARTVALUE; first_adding <=  number; first_adding++) {
    if (is_prime(first_adding)) {
      int64_t second_adding = number - first_adding;
      bool valid_goldbach_sum = (is_prime(second_adding) && first_adding <= second_adding);
      if (valid_goldbach_sum) {
        array_append(addings, first_adding);
        array_append(addings, second_adding);
      }
    }
  }
  return addings;
}

dynamic_array_t* weak_conjecture(int64_t number) {
  dynamic_array_t* addings = (dynamic_array_t*)
      calloc(1, sizeof(dynamic_array_t));
  array_init(addings);
  report_and_exit (addings == NULL, "weak_conjecture\n");

  for (int64_t first_adding = STARTVALUE; first_adding <=  number; first_adding++) {
    if (is_prime(first_adding)) {
      for (int64_t second_adding = first_adding; second_adding <=  number; second_adding++) {
        if (is_prime(second_adding)) {
          int64_t third_adding = number - first_adding - second_adding;
          bool valid_goldbach_sum = (is_prime(third_adding) && second_adding <= third_adding);
          if (valid_goldbach_sum) {
            array_append(addings, first_adding);
            array_append(addings, second_adding);
            array_append(addings, third_adding);
          }
        }
      }
    }
  }
  return addings;
}

int count(dynamic_array_t* array, int num_addings) {
  int sums = 0;
  size_t iterAddings = 0;
    while (iterAddings < array->count) {
      sums +=1;
      iterAddings += num_addings;
    }
  return sums;
}

void show_addings(int64_t* array, int num_addings, int sums){
  int64_t iterAddings = 0;
  while (iterAddings <= num_addings*sums-num_addings) {
    if (iterAddings != 0) {
      write_output(", ", 0, false);
    }
    write_output("", array[iterAddings],true);
    write_output(" + ", 0, false);
    if (num_addings == 3) {
      write_output("", array[iterAddings+1],true);
      write_output(" + ", 0, false);
      write_output("", array[iterAddings+2],true);
    } else {
        write_output("", array[iterAddings+1],true);
      }
    iterAddings+=num_addings;
  }
}

void show_goldbach_results(dynamic_array_t* array, int sums, int64_t num, bool list, int num_addings) {
  if (list == true) {
    write_output("-", 0, false);
    write_output("",num, true);
    write_output(": ", 0, false);
    write_output("", sums, true);
    write_output(" sums", 0, false);
    write_output(": ", 0, false);
    show_addings(array->elements, num_addings, sums);
  } else {
    write_output("",num, true);
    write_output(": ", 0, false);
    write_output("", sums, true);
    write_output(" sums", 0, false);
  }
}

bool analize_arguments(int64_t value) {
  bool valid_number = (value > 5 || value < -5);
  if (!valid_number) {
    write_output("", value, true);
    write_output(": NA\n", 0, false);
  }
  return valid_number;
}

int write_output(char* mesage, size_t number, bool number_flag) {
  FILE *file = fopen("Output.txt", "a+");
  report_and_exit (file == NULL, "output\n");
  if(number_flag == false){
    fprintf(file, "%s", mesage);
  }else{
    char str_number[100];
    sprintf(str_number, "%li", number);
    fprintf(file, "%s", str_number);
  }
  fclose(file);
  return EXIT_SUCCESS;
}

void calculate_number(int64_t value) {
  bool valid_input = analize_arguments(value);
  if (valid_input) {
    bool list = false;
    if (value < 0) {
      list = true;
      value *= -1;
    }

    dynamic_array_t* results = (dynamic_array_t*)
        calloc(1, sizeof(dynamic_array_t));
    report_and_exit (results == NULL, "calculate_number\n");
    array_init(results);

    int num_addings = 0;
    if (value % 2 == 0) {
      num_addings = 2;
      results = strong_conjecture(value);
    } else {
      num_addings = 3;
      results = weak_conjecture(value);
    }

    int sums = count(results, num_addings);
    show_goldbach_results(results, sums, value, list, num_addings);
    write_output("\n",0, false);
    array_destroy(results);
  }
}

void calculate_array(dynamic_array_t* input_numbers) {
  for (size_t number = 0; number < input_numbers->count; number++) {
    int64_t goldbach_number = input_numbers->elements[number];
    bool valid_input = analize_arguments(goldbach_number);
    if (valid_input) {
      calculate_number(goldbach_number);
    }
  }
}

int main() {
  return EXIT_SUCCESS;
}
