/**
 * @author Andre Anjos <andre.anjos@idiap.ch>
 * @date Thu 28 Jul 18:00:42 2011 
 *
 * @brief Constructs to allow the concatenation of blitz::Arrays along
 * configurable dimensions in a generic way and optimally avoiding excessive
 * copying.
 */

#ifndef TORCH_CORE_ARRAY_CAT_H 
#define TORCH_CORE_ARRAY_CAT_H

#include <vector>
#include <blitz/array.h>
#include <core/array_assert.h>

namespace Torch { namespace core { namespace array {

  /**
   * Copies the data of one array into the other, specifying a precise position
   * and a dimension along which the copy will take place. No checks are done,
   * just trust the user.
   *
   * Requires: Arrays have the same shape, except for the dimension in which
   * the copy will occur.
   *
   * Requires: The destination array should have enough space allocated.
   *
   * @return An array of the same type, but with the two input arrays
   * concatenated along the given dimension.
   */
  template <typename T, int N>
    void dcopy_(const blitz::Array<T,N>& source, blitz::Array<T,N>& dest, 
        int D, int pos) {
      blitz::RectDomain<N> domain = dest.domain();
      domain.lbound(D) = pos;
      domain.ubound(D) = pos + source.extent(D) - 1;
      dest(domain) = source; //copy
    }

  /**
   * Copies the data of one array into the other, specifying a precise position
   * and a dimension along which the copy will take place.
   *
   * Requires: Arrays have the same shape, except for the concatenation
   * dimension. 
   *
   * Requires: The destination array should have enough space allocated.
   *
   * @return An array of the same type, but with the two input arrays
   * concatenated along the given dimension.
   */
  template <typename T, int N>
    void dcopy(const blitz::Array<T,N>& source, blitz::Array<T,N>& dest,
        int D, int pos) {

      if ( D > (N-1) ) throw UnexpectedShapeError();

      //checks arrays are compatible
      blitz::TinyVector<int,N> v1 = source.shape();
      blitz::TinyVector<int,N> v2 = dest.shape();
      v1(D) = v2(D) = 0;
      if ( blitz::all(v1 != v2) ) throw UnexpectedShapeError();

      //checks destination has enough room
      if ( (source.extent(D) + pos) > dest.extent(D) )
        throw UnexpectedShapeError();

      dcopy_(source, dest, D, pos);
    }

  /**
   * Copies the data of array a into the destination array d without checking
   * the shape. "a" has N-1 dimensions and is copied along dimension "D" in "d"
   * at position "pos".
   */
  template <typename T, int N> struct copy__ {

      static void f(const blitz::Array<T,N-1>& a,
          blitz::Array<T,N>& d, int D, int pos) {
        //generic implementation: will not compile!
        blitz::TinyVector<int,N> lowerBounds = 0;
        blitz::TinyVector<int,N> upperBounds = d.shape();
        upperBounds -= 1;
        lowerBounds(D) = upperBounds(D) = pos;
        blitz::RectDomain<N> domain(lowerBounds, upperBounds);
        d(domain) = a;
      }

    };

  /**
   * Here are the specializations that do compile.
   */
  template <typename T> struct copy__<T,2> {

      static void f(const blitz::Array<T,1>& a,
          blitz::Array<T,2>& d, int D, int pos) {
        blitz::Range all = blitz::Range::all();
        switch (D) {
          case 0:
            d(pos, all) = a;
            break;
          case 1:
            d(all, pos) = a;
            break;
        }
      }

  };

  template <typename T> struct copy__<T,3> {

      static void f(const blitz::Array<T,2>& a,
          blitz::Array<T,3>& d, int D, int pos) {
        blitz::Range all = blitz::Range::all();
        switch (D) {
          case 0:
            d(pos, all, all) = a;
            break;
          case 1:
            d(all, pos, all) = a;
            break;
          case 2:
            d(all, all, pos) = a;
            break;
        }
      }

  };

  template <typename T> struct copy__<T,4> {

      static void f(const blitz::Array<T,3>& a,
          blitz::Array<T,4>& d, int D, int pos) {
        blitz::Range all = blitz::Range::all();
        switch (D) {
          case 0:
            d(pos, all, all, all) = a;
            break;
          case 1:
            d(all, pos, all, all) = a;
            break;
          case 2:
            d(all, all, pos, all) = a;
            break;
          case 3:
            d(all, all, all, pos) = a;
            break;
        }
      }

  };

  /**
   * Copies the data of "source" along the given dimension of "dest".  Special
   * case: source has dimension N-1. Does not check any of the requirements
   * (trust the user).
   *
   * Requires: Arrays have the same shape, except for the copy dimension.
   *
   * Requires: The destination array should have enough space allocated.
   *
   * @return An array of the same type, but with the two input arrays
   * concatenated along the given dimension.
   */
  template <typename T, int N> void dcopy_(const blitz::Array<T,N-1>& source,
      blitz::Array<T,N>& dest, int D, int pos) {
      copy__<T,N>::f(source, dest, D, pos);
    }

  /**
   * Copies the data of "source" along the given dimension of "dest".  Special
   * case: source has dimension N-1.
   *
   * Requires: Arrays have the same shape, except for the copy dimension.
   *
   * Requires: The destination array should have enough space allocated.
   *
   * @return An array of the same type, but with the two input arrays
   * concatenated along the given dimension.
   */
  template <typename T, int N>
    void dcopy(const blitz::Array<T,N-1>& source, blitz::Array<T,N>& dest, 
        int D, int pos) {

      if ( D > (N-1) ) throw UnexpectedShapeError();

      //checks arrays are compatible
      blitz::TinyVector<int,N> v1 = dest.shape();
      blitz::TinyVector<int,N> v2;
      for (int k=0, l=0; k<N; ++k) {
        if (k == D) v2(k) = 0;
        else v2(l++) = source.shape()(k);
      }
      v1(D) = 0;
      if ( blitz::all(v1 != v2) ) throw UnexpectedShapeError();

      //checks destination has enough room
      if ( pos >= dest.extent(D) ) throw UnexpectedShapeError();

      copy__<T,N>::f(source, dest, D, pos);
    }

  /**
   * Concatenates a bunch of arrays with the same shape together, along
   * dimension D. Does not check the user input.
   *
   * Requires: The source and destination shapes are identical except along
   * dimension D.
   *
   * Requires: The destination array has enough space.
   */
  template <typename T, int N>
    void cat_(const std::vector<blitz::Array<T,N> >& source,
        blitz::Array<T,N>& dest, int D) {
      int pos = 0;
      for (size_t i=0; i<source.size(); ++i) {
        dcopy_(source[i], dest, D, pos);
        pos += source[i].extent(D);
      }
    }

  /**
   * Concatenates a bunch of arrays with the same shape together, along
   * dimension D.
   *
   * Requires: The source and destination shapes are identical except along
   * dimension D.
   *
   * Requires: The destination array has enough space.
   */
  template <typename T, int N>
    void cat(const std::vector<blitz::Array<T,N> >& source,
        blitz::Array<T,N>& dest, int D) {
      int pos = 0;
      for (size_t i=0; i<source.size(); ++i) {
        dcopy(source[i], dest, D, pos);
        pos += source[i].extent(D);
      }
    }

  /**
   * Concatenates a bunch of arrays with N-1 dimensions together, along
   * dimension D of the destination array. Does not check the user input.
   *
   * Requires: The source and destination shapes are identical except along
   * dimension D.
   *
   * Requires: The destination array has enough space.
   */
  template <typename T, int N>
    void cat_(const std::vector<blitz::Array<T,N-1> >& source,
        blitz::Array<T,N>& dest, int D) {
      int pos = 0;
      for (size_t i=0; i<source.size(); ++i) {
        dcopy_(source[i], dest, D, pos++);
      }
    }

  /**
   * Concatenates a bunch of arrays with N-1 dimensions together, along
   * dimension D of the destination array.
   *
   * Requires: The source and destination shapes are identical except along
   * dimension D.
   *
   * Requires: The destination array has enough space.
   */
  template <typename T, int N>
    void cat(const std::vector<blitz::Array<T,N-1> >& source,
        blitz::Array<T,N>& dest, int D) {
      int pos = 0;
      for (size_t i=0; i<source.size(); ++i) {
        dcopy(source[i], dest, D, pos++);
      }
    }

}}}

#endif /* TORCH_CORE_ARRAY_CAT_H */