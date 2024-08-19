# Optimism FHE Simulation

## Overview

This project simulates the effects of Fully Homomorphic Encryption (FHE) on the Optimism blockchain. The simulation processes real blockchain data, performing encrypted state transitions and analyzing noise growth, gas costs, and other performance metrics related to FHE.

## Features

- **State Transition Simulation**: Simulates blockchain state transitions using FHE for different parties.
- **Noise Growth Analysis**: Tracks and analyzes the growth of noise in encrypted states.
- **Gas Cost Analysis**: Computes and analyzes gas costs of blockchain transactions.
- **Performance Benchmarking**: Logs FHE performance metrics such as encryption, decryption, state transition, and memory usage.

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