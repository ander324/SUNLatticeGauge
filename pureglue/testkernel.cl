#include "clcomplex.h"

__kernel void squarer(__global clcomplex* in, __global clcomplex* out)
{
	int idx = get_global_id(0);
	out[idx] = Cmul(in[idx],in[idx]);
}