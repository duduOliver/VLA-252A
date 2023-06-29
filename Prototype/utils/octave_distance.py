import numpy as np

def octave_distance(central_freq: float) -> float: #Calculates the octave distance based on the given central frequency.
    """
    Args:
        central_freq (float): The central frequency in Hz.
    Returns:
        float: The octave distance.
    """
    cf = [50, 130, 320, 800, 2000, 5000, 12500]
    closest_index = min(range(len(cf)), key=lambda i: abs(cf[i] - central_freq))
    cf1 = cf[closest_index]
    if closest_index == len(cf) - 1:
        cf2 = cf1
    else:
        cf2 = cf[closest_index + 1]
    return np.log2(cf2 / cf1)

    x = wdf.get_impulse_response()
    nyquist = sample_rate / 2
    N2 = int(fft_size / 2 - 1)
    Hw = np.fft.fft(x, fft_size)[:N2]
    return Hw