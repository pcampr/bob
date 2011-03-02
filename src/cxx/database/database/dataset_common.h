/**
 * @file src/cxx/database/database/dataset_common.h
 * @author <a href="mailto:Laurent.El-Shafey@idiap.ch">Laurent El Shafey</a> 
 *
 * @brief This file contains standard definitions for the Dataset 
 * implementation
 *
 */

#ifndef TORCH_DATABASE_DATASET_COMMON_H
#define TORCH_DATABASE_DATASET_COMMON_H

#include "core/array_common.h"

namespace Torch {
/**
 * \ingroup libdatabase_api
 * @{
 *
 */
  namespace database {

    /**
     * string for the XML attributes
     */
    extern const char *dataset;
    extern const char *arrayset;
    extern const char *external_arrayset;
    extern const char *relationset;
    extern const char *pathlist;
    extern const char *version;
    extern const char *id;
    extern const char *role;
    extern const char *elementtype;
    extern const char *shape;
    extern const char *codec;
    extern const char *file;
    extern const char *array;
    extern const char *external_array;
    extern const char *name;
    extern const char *author;
    extern const char *datetime;
    extern const char *rule;
    extern const char *relation;
    extern const char *member;
    extern const char *arrayset_member;
    extern const char *arrayset_role;
    extern const char *min;
    extern const char *max;
    extern const char *array_id;
    extern const char *arrayset_id;
    extern const char *entry;
    extern const char *path;

    // elementtype
    extern const char *t_bool;
    extern const char *t_int8;
    extern const char *t_int16;
    extern const char *t_int32;
    extern const char *t_int64;
    extern const char *t_uint8;
    extern const char *t_uint16;
    extern const char *t_uint32;
    extern const char *t_uint64;
    extern const char *t_float32;
    extern const char *t_float64;
    extern const char *t_float128;
    extern const char *t_complex64;
    extern const char *t_complex128;
    extern const char *t_complex256;

    /**
     * This structure holds information about array typing in a single bound
     * place.
     */
    class ArrayTypeInfo {

      public:
        //what defines an array in terms of its typing...
        Torch::core::array::ElementType eltype;
        size_t ndim;
        size_t shape[Torch::core::array::N_MAX_DIMENSIONS_ARRAY];

        /**
         * Compares two ArrayTypeInfo objects for equality
         */
        bool operator== (const ArrayTypeInfo& other) const;

        /**
         * Compares two ArrayTypeInfo objects for inequality
         */
        inline bool operator!= (const ArrayTypeInfo& other) const {
          return ! (*this == other);
        }

    };

/**
 * @}
 */
  }
}

#endif /* TORCH_DATABASE_DATASET_COMMON_H */