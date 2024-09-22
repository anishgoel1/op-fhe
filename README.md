# Optimism Encryption/Decryption Simulation

## Features

- **State Transition Simulation**: Simulates blockchain state transitions for different parties.
- **Noise Growth Analysis**: Tracks and analyzes the growth of noise in encrypted states.
- **Gas Cost Analysis**: Computes and analyzes gas costs of blockchain transactions.
- **Performance Benchmarking**: Logs performance metrics such as encryption, decryption, state transition, and memory usage.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/op-fhe.git
   cd op-fhe
2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   pip install --no-deps crypten

3. **Configure the API Key:**
   Create a file named `config.json` in `/src` and add your API key as follows:

   ```json
   {
     "api_key": "your-optimism-api-key"
   }
   ```
4. **Run the Simulation:**

   ```bash
   python src/main.py
   ```
