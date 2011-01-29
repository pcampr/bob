/**
 * @author <a href="mailto:andre.anjos@idiap.ch">Andre Anjos</a> 
 * @brief blitz::Array<uint64_t,4> to and from python converters
 */
#include "core/python/array.h"
declare_unsigned_array(uint64_t, 4, uint64, bind_core_array_uint64_4)