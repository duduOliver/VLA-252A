import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from scipy.io import wavfile
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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

def new_plot_freqz(self, yLim_min = -100, yLim_max = 100, xLim_min = 20, xLim_max = 20000, outpath: str = None, fft_size: int = None, scale_type: str = 'log'):
    """Plot the circuit's frequency response

    Args:
        outpath (str, optional): filepath to save figure. Defaults to None.
        fft_size (int, optional): FFT size. Defaults to None.
        scale_type (str, optional): Scale type ('log' or 'linear'). Defaults to 'log'.
    """
    if fft_size is None:
        fft_size = int(2 ** 15)

    H = self.compute_spectrum(fft_size)
    nyquist = self.fs / 2
    magnitude = 20 * np.log10(np.abs(H) + np.finfo(float).eps)
    phase = np.angle(H)
    magnitude_peak = np.max(magnitude)
    top_offset = 10
    bottom_offset = 70
    N2 = int(fft_size / 2 - 1)
    frequencies = np.linspace(0, nyquist, N2)

    # Create subplots with shared x-axis
    fig, (ax_magnitude, ax_phase) = plt.subplots(2, 1, figsize=(10, 8), sharex=False)

    # Plot magnitude response
    if scale_type == 'log':
        ax_magnitude.semilogx(frequencies, magnitude, label="WDF", color="blue")
        ax_magnitude.set_xscale('log')
    else:
        ax_magnitude.plot(frequencies, magnitude, label="WDF", color="blue")

    plt.xticks(rotation=45)
    ax_magnitude.set_xlim([xLim_min, xLim_max])
    ax_magnitude.set_ylim([yLim_min, yLim_max])
    ax_magnitude.xaxis.set_major_formatter(ScalarFormatter())
    ax_magnitude.set_xticks([20, 50, 100, 200, 500, 1000, 2000, 4000, 10000, 15000])
    ax_magnitude.set_xticklabels([20, 50, 100, 200, 500, 1000, 2000, 4000, 10000, 15000], rotation = 45)
    ax_magnitude.set_xlabel("Frequency [Hz]", fontsize=12)
    ax_magnitude.set_ylabel("Magnitude [dBFs]", fontsize=12)
    ax_magnitude.grid(True, which='both', color='0.65', linestyle='-')
    #ax_magnitude.set_title(self._class.name_ + " Magnitude Response")
    ax_magnitude.tick_params(labelsize=10)

    # Plot phase response
    phase_degrees = np.rad2deg(phase)
    if scale_type == 'log':
        ax_phase.semilogx(frequencies, phase_degrees, color="tab:orange")
        ax_phase.set_xscale('log')
    else:
        ax_phase.plot(frequencies, phase_degrees, color="tab:orange")

    ax_phase.set_xlim([xLim_min, xLim_max])
    ax_phase.set_ylim([-180, 180])
    ax_phase.xaxis.set_major_formatter(ScalarFormatter())
    ax_phase.set_xticks([20, 50, 100, 200, 500, 1000, 2000, 4000, 10000, 15000])
    ax_phase.set_xlabel("Frequency [Hz]", fontsize=12)
    ax_phase.set_ylabel("Phase [degrees]", fontsize=12)
    ax_phase.grid(True, which='both', color='0.65', linestyle='-')
    #ax_phase.set_title(self._class.name_ + " Phase Response")
    ax_phase.tick_params(labelsize=10)

    fig.tight_layout(pad=2.0)

    if outpath:
        plt.savefig(outpath)
    plt.show()

def sci2sufix(number):
    units = {0:' ', 1:'k',  2:'M', -1:'m', -2:'u', -3:'n', -4:'p'}
    mantissa,exponent = f"{number:e}".split("e")
    unitRange = int(exponent)//3
    unit = units.get(unitRange,None)
    unitValue = float(mantissa)*10**(int(exponent)%3)
    return f"{unitValue:.2f} {unit}" if unit else f"{number:.5e}"