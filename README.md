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
  ├── Demos
  │   ├── Prototype Demo
  │   ├──RealTimee Demo
  ├── Documentation
  │   ├── User Manual
  │   ├── VLA252A
  ├── Langevin251
  │   ├── LTSpice
      │   ├── HiCutLoBoost.asc
      │   ├── HiLoBoost.asc
      │   ├── HiLoCut.asc
      │   ├── LoCutHiBoost.asc
      │   ├── Simplifiedcircuit.asc
  │   ├── Netlist
      │   ├── HiCutLoBoost.txt
      │   ├── HiLoBoost.txt
      │   ├── HiLoCut.txt
      │   ├── LoCutHiBoost.txt
      │   ├── Simplifiedcircuit.txt
  │   ├── Scattering Matrix
      │   ├── HiCutLoBoost.txt
      │   ├── HiLoBoost.txt
      │   ├── HiLoCut.txt
      │   ├── LoCutHiBoost.txt
      │   ├── Simplifiedcircuit.txt
  │   ├─ Separated Ports
      │   ├── HiCutLoBoost.py
      │   ├── HiLoBoost.py
      │   ├── HiLoCut.py
      │   ├── LoCutHiBoost.py
  │   ├──Sounds / Input
      │   ├── piano.wav
  │   ├── Langevin.py
  │   ├── utils.py
  ├── sc
      │   ├── Prototype
          │   ├── utils.py
          │   ├── LC_SecondOrd_BPF.py
          │   ├── LC_ThirdOrd_BPF.py
          │   ├── LC_BPF.py
          │   ├── RC_hpf.py
          │   ├── RC_lpf.py
          │   ├── VLA252.py
          │   ├── VLA252_GUI.py
          │   ├── environment.yml
          │   ├── main.py
      │   ├── Supercollider
          │   ├── Langevin252A.sc
          │   ├── langevinTest.scd
          │   ├── somiomio.wav

  </code>
  </pre>
  
  <h2>Installation and Usage</h2>

  <p>For more information about the usage of the plugin you can check the  <a href="Documentation/UserManual.docx.pdf/">User Manual</a></p>
  
  <h3>Python prototype</h3>
  <p>To set up and install the Python prototype, please follow the instructions provided below:</p>
  <ol>
  <li>Begin by downloading the source code from the designated GitHub repository.</li>
  <li>Install all the necessary libraries by executing the following command in your terminal:</li>
</ol>

<pre><code>pip install -r requirements.txt</code></pre>

<p>This command will utilize the <code>requirements.txt</code> file to automatically install all the required libraries.</p>

<ol start="3">
  <li>Once the installation process is complete, you are ready to run the code and start utilizing the prototype.</li>
</ol>


  <h3> Supercollider</h3>
<ol>
  <li>Copy the folder named "Langevin252A" located in <a href="sc/Supercollider/">Supercollider</a>, and paste it into the extensions folder of your SuperCollider installation on your computer.</li>
  <li>To find the location of the extension folder, open SuperCollider and evaluate the following line of code: <code>Platform.userExtensionDir</code>.</li>
  <li>Inside the extension folder, you will find the plugin file, an audio file for the tutorial, and a tutorial named "langevinTest".</li>
  <li>For the final part of the tutorial (VarGui), you need to install the "MiSCellaneous" library from the Quarks system.</li>
</ol>

  <h2>Results</h2>
  <h3>Python Prototype</h3>
  <p>The evaluation results of the python prototype showcased exceptional accuracy and fidelity in terms of sonic reproduction. We were able to achieve a remarkably close sound to our desired outcome, highlighting the prototype's potential in delivering high-quality audio. 
However, one significant drawback surfaced during the evaluation process - the computational efficiency of the prototype was insufficient for real-time performance. This limitation impacted the overall feature set and functionality of the prototype, falling short of our initial expectations. While the prototype could potentially serve as a standalone version of the plugin, it remains less convenient due to its inability to operate in real time.
</p>
  <h3>Supercollider</h3>
  <p>The evaluation results showed that it may not be able to perfectly reproduce the distinctive sound of the Langevin 252A due to the unavailability of its schematics. However, it does possess a commendable ability to accurately reproduce the sonic characteristics of a bandpass filter. While it may not replicate the exact sound signature of the Langevin 252A, it still offers a satisfying audio experience.</p>

  <p>Moreover, this plugin has the potential to deliver high-quality audio output. It is designed to ensure that the audio signals passing through it are faithfully reproduced, maintaining their clarity, dynamics, and fidelity. In addition, it offers sufficient computational efficiency to enable real-time performance. It can handle audio processing tasks without significant latency or lag. This capability is especially important for applications where immediate audio feedback or live performances are involved.</p>


  <h2>Improvements</h2>
  <p>Looking ahead, we recognize the scope for future improvements in the circuit used. Given more time, we could have sought out a circuit that closely matched our requirements, ultimately yielding better results. Continual refinement and fine-tuning of the circuit will contribute to the overall enhancement of the project.
</p>

  <h2>Contributing</h2>
  <p>We welcome contributions to enhance the VLA-252A! If you'd like to contribute, please follow these steps:</p>
  <ol>
    <li>Fork the repository on GitHub.</li>
    <li>Create a new branch for your feature or bug fix: <code>git checkout -b feature/your-feature</code>.</li>
    <li>Make the necessary changes and commit them.</li>
    <li>Push your changes to your forked repository.</li>
    <li>Create a pull request on the main repository.</li>
  </ol>

  <h2>Demos</h2>
    
  <p>For a demonstration of the Python prototype, you can watch the video <a href="https://www.youtube.com/watch?v=jWJqOlhxAtM">here</a>.</p>
  
  <p>Additionally, we have a video showcasing the real-time part in SuperCollider, which can be found <a href="https://www.youtube.com/watch?v=xoGPNt4fo-o">here</a>.</p>


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
    
  <h3>Contact</h3>
  <p>If you have any questions, or feedback, or need assistance with our plugin, we encourage you to get in touch with us. We are here to help and provide you with the support you need. You can contact us through the following emails:</p>
  <ul>
    <li>
      Andrea Sofia Vallejo Budziszewski: <a href="mailto:sofiavallejo98@hotmail.com">sofiavallejo98@hotmail.com</a>
    </li>
    <li>
      Chris Morse: <a href="mailto:cemorse100@gmail.com">cemorse100@gmail.com</a>
    </li>
    <li>
      Du Huang: <a href="mailto:du.huang01@estudiant.upf.edu">du.huang01@estudiant.upf.edu</a>
    </li>
    <li>
      Pablo Rodríguez Solans: <a href="mailto:pablo.rodriguez04@estudiant.upf.edu">pablo.rodriguez04@estudiant.upf.edu</a>
    </li>
    <li>
      Tommaso Settimi: <a href="mailto:tommssett@gmail.com">tommssett@gmail.com</a>
    </li>
  </ul>
  
  <p>Please provide as much detail as possible when contacting us, including the version of the plugin you are using, any error messages you encountered, and steps to reproduce the issue. This information will assist us in diagnosing and resolving your problem quickly.</p>
  
  <p>We value your feedback and strive to continuously improve our plugin based on your suggestions and needs. Don't hesitate to reach out to us. Your input is invaluable in making our plugin even better.</p>
  
  <p>Thank you for using our plugin!</p>
