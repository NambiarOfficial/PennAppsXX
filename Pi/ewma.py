import numpy as np
def ewma(data, alpha, offset=None, dtype=None, order='C', out=None):
	"""
	Calculates the exponential moving average over a vector.
	Will fail for large inputs.
	:param data: Input data
	:param alpha: scalar float in range (0,1)
		The alpha parameter for the moving average.
	:param offset: optional
		The offset for the moving average, scalar. Defaults to data[0].
	:param dtype: optional
		Data type used for calculations. Defaults to float64 unless
		data.dtype is float32, then it will use float32.
	:param order: {'C', 'F', 'A'}, optional
		Order to use when flattening the data. Defaults to 'C'.
	:param out: ndarray, or None, optional
		A location into which the result is stored. If provided, it must have
		the same shape as the input. If not provided or `None`,
		a freshly-allocated array is returned.
	"""
	data = np.array(data, copy=False)

	if dtype is None:
		if data.dtype == np.float32:
			dtype = np.float32
		else:
			dtype = np.float64
	else:
		dtype = np.dtype(dtype)

	if data.ndim > 1:
		# flatten input
		data = data.reshape(-1, order)

	if out is None:
		out = np.empty_like(data, dtype=dtype)
	else:
		assert out.shape == data.shape
		assert out.dtype == dtype

	if data.size < 1:
		# empty input, return empty array
		return out

	if offset is None:
		offset = data[0]

	alpha = np.array(alpha, copy=False).astype(dtype, copy=False)

	# scaling_factors -> 0 as len(data) gets large
	# this leads to divide-by-zeros below
	scaling_factors = np.power(1. - alpha, np.arange(data.size + 1, dtype=dtype),
							   dtype=dtype)
	# create cumulative sum array
	np.multiply(data, (alpha * scaling_factors[-2]) / scaling_factors[:-1],
				dtype=dtype, out=out)
	np.cumsum(out, dtype=dtype, out=out)

	# cumsums / scaling
	out /= scaling_factors[-2::-1]

	if offset != 0:
		offset = np.array(offset, copy=False).astype(dtype, copy=False)
		# add offsets
		out += offset * scaling_factors[1:]

	return out

def wma(data):
	s = data[0]*0.05 + data[1]*0.1 + data[2]*0.15 + data[3]*0.25 + data[4]*0.45
	return s