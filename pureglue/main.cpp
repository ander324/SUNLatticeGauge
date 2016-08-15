#include <sstream>
#include <fstream>
#include <algorithm>
#include <memory>
#include <iostream>
#include <array>
#include <complex>
#include <CL/cl.h>
#include "clRNG/clRNG.h"
#include "clRNG/mrg31k3p.h"

int main()
{
	cl_platform_id platform = NULL;
	auto status = clGetPlatformIDs(1, &platform, NULL);

	cl_device_id device = NULL;
	status = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, NULL);

	cl_context_properties cps[] = { CL_CONTEXT_PLATFORM, (cl_context_properties)platform, 0 };
	cl_command_queue_properties cqps = 0 ;
	auto context = clCreateContext(cps, 1, &device, 0, 0, &status);

	auto queue = clCreateCommandQueue(context, device, cqps, &status);




	std::ifstream file("testrngkernel.cl");
	std::string source( std::istreambuf_iterator<char>(file), (std::istreambuf_iterator<char>()));
	size_t      sourceSize = source.size();
	const char* sourcePtr  = source.c_str();
	auto program = clCreateProgramWithSource(context, 1, &sourcePtr, &sourceSize, &status);
	
	status = clBuildProgram(program, 1, &device, "-I. -I/home/ander324/clRNG.build/package/include", nullptr, nullptr);
	if (status != CL_SUCCESS)
	{
		size_t len = 0;
		status = clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, 0, nullptr, &len);
		//std::unique_ptr<char[]> log = std::make_unique<char[]>(len);
		char* log = new char[len];
		status = clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, len, log, nullptr);
		printf("%s\n", log);
		system("PAUSE");
		delete[] log;
	}

	auto kernel = clCreateKernel(program, "testrng", &status);

	std::array<std::complex<double>, 8> B;

	cl_int err;
	size_t streamBufferSize;
	clrngMrg31k3pStream* streams = clrngMrg31k3pCreateStreams(NULL, B.size(),
								  &streamBufferSize, (clrngStatus *)&err);
	//check_error(err, "cannot create random stream array");
	


	// Create buffer to transfer streams to the device.
	cl_mem buffer_in = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR,
				       streamBufferSize, streams, &err);
	
	auto buffer_out = clCreateBuffer(context, CL_MEM_WRITE_ONLY | CL_MEM_COPY_HOST_PTR, B.size() * sizeof(std::complex<double>), B.data(), &status);

	status = clSetKernelArg(kernel, 0, sizeof(buffer_in), &buffer_in);
	status = clSetKernelArg(kernel, 1, sizeof(buffer_out), &buffer_out);

	size_t thread_count = B.size();
	status = clEnqueueNDRangeKernel( queue, kernel, 1, nullptr, &thread_count, nullptr, 0, nullptr, nullptr);
	status = clEnqueueReadBuffer(queue, buffer_out, false, 0, B.size() * sizeof(std::complex<double>), B.data(), 0, nullptr, nullptr);
	status = clFinish(queue);
	std::for_each(B.begin(), B.end(), [](std::complex<double> x) { std::cout << x.real() <<'\t' << x.imag() << "\n"; });

	
	return 0;

}
