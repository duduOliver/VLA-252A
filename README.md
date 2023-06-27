  <h1>VLA-252A: Analog Modeling of the Langevin 252A Utilizing Wave Digital Filters</h1>

  <h2>Introduction</h2>
  <p>Our goal for this project is to create a revolutionary Passive Graphic Equalizer (GEQ) prototype replicating the iconic Langevin EQ252A, one of the earliest and most sought-after analog EQs in history. However, instead of relying on costly physical analogs that can set you back around 1400 GBP (around 1600 EUR or 1750 USD), we are taking a modern approach by utilizing Wave Digital Filters to create a digital model that is both affordable and highly efficient. With this innovative solution, we aim to bring the timeless sound of the Langevin EQ252A to a wider audience, while also revolutionizing the way we approach equalization in the digital age.</p>

  <h2>Background</h2>
  <h3>Langevin 252A Equalizer</h3>
  <p>The Langevin 252A Equalizer is an iconic analog equalizer known for its exceptional sound quality and versatility. It features seven bands, each with a fixed frequency center and a variable gain control, allowing for precise equalization across the audio spectrum.</p>
  <p>The EQ 252A's analog circuitry provides warmth, color, and depth to audio signals, contributing to its unique sonic characteristics.</p>

  <h3>Wave Digital Filters</h3>
  <p>Wave Digital Filters (WDFs) are a digital signal processing technique used to model and emulate analog audio circuits. They accurately simulate the behavior of analog components in the digital domain by using wave variables to represent voltages and currents in the circuit.</p>
  <p>WDFs are employed in this software project to faithfully reproduce the sonic qualities and tonal characteristics of the Langevin 252A equalizer, providing users with a highly realistic and versatile equalization tool.</p>
  
  <h2>Dependencies</h2>
   <li>Python v3.11</li>
   <li>Supercollider v3.13</li>

  <h2>Structure</h2>
  <pre>
  <code>
  ./VLA-252A/
  ├── LC_BPF.py
  ├── LCSecOrd_BPF.py
  ├── LCThirdOrd_BPF.py
  ├── main.py
  ├── RC_hpf.py
  ├── RC_lpf.py
  ├── test
  │   ├── test_LC_BPF.py
  │   ├── test_LCSecOrd_BPF.py
  │   ├── test_LCThirdOrd_BPF.py
  │   └── test_VLA251.py
  ├── utils
  │   ├── new_plot_freqz.py
  │   └── octave_distance.py
  ├── VLA251_GUI.py
  └── VLA251.py
  </code>
  </pre>

  <h2>Results</h2>
  <p></p>

  <h2>Improvements</h2>
  <p></p>

  <h2>Contributing</h2>
  <p>We welcome contributions to enhance the VLA-252A! If you'd like to contribute, please follow these steps:</p>
  <ol>
    <li>Fork the repository on GitHub.</li>
    <li>Create a new branch for your feature or bug fix: <code>git checkout -b feature/your-feature</code>.</li>
    <li>Make the necessary changes and commit them.</li>
    <li>Push your changes to your forked repository.</li>
    <li>Create a pull request on the main repository.</li>
  </ol>

  <h2>License</h2>
  <p>
    This project is licensed under the <a href="https://www.gnu.org/licenses/agpl-3.0.html">Affero General Public License (AGPL)</a>. The AGPL is a copyleft license that requires any modified or extended versions of the software to be distributed under the same license terms.
  </p>
  <p>
    Feel free to use, modify, and distribute the code according to the terms of the AGPL.
  </p>
<h2>Acknowledgments</h2>
  <p>
    This project was done as part of the Sound communication class for the Sound and Music Computing master's degree at Universitat Pompeu Fabra.
  </p>
  <p>
    It was made possible by the following libraries and resources:
  </p>
  <ul>
  <li><a href="https://github.com/gusanthon/pywdf">PYWDF</a> - Python framework designed for modeling and simulating wave digital filter circuits.</li>
