#include "openclcomplex.h"
//#include "clsun.h"
#include <clRNG/mrg31k3p.clh> 

__kernel void testrng(__global clrngMrg31k3pHostStream* streams, __global cdouble_t* out)
{
	int gid = get_global_id(0);	
	clrngMrg31k3pStream private_stream_d;   // This is not a pointer!	
	clrngMrg31k3pCopyOverStreamsFromGlobal(1, &private_stream_d, &streams[gid]);
	out[gid] = cdouble_new(clrngMrg31k3pRandomU01(&private_stream_d),clrngMrg31k3pRandomU01(&private_stream_d));
	
}