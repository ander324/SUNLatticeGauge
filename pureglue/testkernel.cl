#include "openclcomplex.h"

__kernel void squarer(__global cdouble_t* in, __global cdouble_t* out)
{
	int idx = get_global_id(0);
	out[idx] = cdouble_mul(in[idx],in[idx]);
}