#ifndef input_handler_H
#define input_handler_H
#include <inttypes.h>
#include <stddef.h>
#include <assert.h>
#include "dynamic_array.h"

dynamic_array_t* read_input();

/**
*@brief validate user input to handle errors and N/A exceptions
*@param value input value
*@return error code
*/
int verify_input(int64_t value);

/**
*@brief analize given arguments : number of threads
*@details assert for invalid thread count
*@param argc number of args
*@param argv char of args
*@return valid thread count 
*/
int64_t analyze_arguments(int argc, char* argv[]);

#endif  // input_handler_H
