import crypten
import torch
import numpy as np
import time
import tracemalloc
from typing import List, Dict, Any, Optional, Tuple, Union
from scipy.stats import skew, kurtosis

from logger import Logger
from optimism_api import OptimismAPI
from fhe_encryption import OptimismFHEEncryption

class FHEStateSimulator:
    def __init__(self, api_key: str):
        """
        Initialize the FHEStateSimulator with the given API key.

        Args:
            api_key (str): API key for accessing the Optimism API.
        """
        crypten.init()
        self.logger = Logger()
        self.api = OptimismAPI(api_key)
        self.max_retries = 3

        # Initialize FHE encryption handler
        self.fhe_encryption = OptimismFHEEncryption(precision=1e-6)

        # Noise growth parameters from academic literature (simplified)
        self.noise_addition_constant = 1.0   # Fixed noise increase per addition
        self.noise_multiplication_factor = 1.05  # Noise growth factor for multiplications

    def simulate_state_with_real_data(self, num_blocks: int = 20) -> Optional[Dict[str, Any]]:
        """
        Simulate the state with real data using advanced FHE and MPC operations.

        Args:
            num_blocks (int): Number of recent blocks to simulate. Default is 20.

        Returns:
            Optional[Dict[str, Any]]: Simulation results including decrypted states, transaction stats, and performance metrics.
        """
        self.logger.log("Simulating state with {} recent blocks using advanced FHE and MPC operations...".format(num_blocks))

        # Start tracking memory usage for FHE
        tracemalloc.start()

        block_data = self.fetch_recent_blocks(num_blocks)  # Fetch the most recent blocks
        if block_data is None:
            self.logger.log("No block data available. Exiting simulation.")
            return None

        # Initialize multiple encrypted states for different parties using OptimismFHEEncryption
        encrypted_state_party1 = self.fhe_encryption.encrypt_data(1000.0)  # Initial state for party 1
        encrypted_state_party2 = self.fhe_encryption.encrypt_data(500.0)   # Initial state for party 2
        encrypted_state_party3 = self.fhe_encryption.encrypt_data(750.0)   # Additional party in the simulation

        encrypted_state_aggregate = self.fhe_encryption.encrypt_data(0.0)  # Aggregate state for MPC

        total_gas_cost = 0
        transaction_count = 0
        block_sizes: List[int] = []
        block_times: List[int] = []
        gas_prices: List[int] = []  # To analyze gas price volatility
        transaction_values: List[float] = []

        encryption_times: List[float] = []
        decryption_times: List[float] = []
        state_transition_times: List[float] = []
        multiplication_times: List[float] = []  # Track multiplication operations
        aggregation_times: List[float] = []     # Track aggregation times

        noise_levels_party1: List[float] = []   # Track noise levels for party 1
        noise_levels_party2: List[float] = []   # Track noise levels for party 2
        noise_levels_party3: List[float] = []   # Track noise levels for party 3

        # Initial noise levels
        noise_party1 = 0.01
        noise_party2 = 0.01
        noise_party3 = 0.01

        for block in block_data:
            if isinstance(block, dict):
                try:
                    # Block data extraction
                    block_size = int(block.get('size', '0x0'), 16)
                    block_time = int(block.get('timestamp', '0x0'), 16)
                    gas_price = int(block.get('baseFeePerGas', '0x0'), 16)  # Gas price data
                    block_sizes.append(block_size)
                    block_times.append(block_time)
                    gas_prices.append(gas_price)

                    block_transactions = block.get('transactions', [])
                    if isinstance(block_transactions, list):
                        for tx in block_transactions:
                            if isinstance(tx, dict):
                                transaction_value = int(tx.get('value', '0x0'), 16) / (10**18)
                                gas_used = int(tx.get('gas', '0x0'), 16)

                                if transaction_value == 0:
                                    continue  # Skip zero-value transactions

                                # Track FHE encryption time
                                start_enc = time.time()
                                encrypted_tx_value_party1 = self.fhe_encryption.encrypt_data(transaction_value)  # Encrypt for party 1
                                encrypted_tx_value_party2 = self.fhe_encryption.encrypt_data(transaction_value * 1.5)  # Encrypt for party 2
                                encrypted_tx_value_party3 = self.fhe_encryption.encrypt_data(transaction_value * 1.2)  # Encrypt for party 3
                                encryption_times.append(time.time() - start_enc)

                                # Perform MPC-FHE operations (addition, scaling, multiplication, and aggregation)
                                start_state_transition = time.time()

                                # FHE addition and multiplication with noise growth
                                start_mul = time.time()

                                # Add noise for addition
                                noise_party1 += self.noise_addition_constant
                                noise_party2 += self.noise_addition_constant
                                noise_party3 += self.noise_addition_constant

                                # Homomorphic addition
                                encrypted_state_party1 += encrypted_tx_value_party1
                                encrypted_state_party2 += encrypted_tx_value_party2
                                encrypted_state_party3 += encrypted_tx_value_party3

                                # Noise growth from multiplication
                                encrypted_state_party1 *= self.fhe_encryption.encrypt_data(1.05)
                                noise_party1 *= self.noise_multiplication_factor
                                encrypted_state_party2 *= self.fhe_encryption.encrypt_data(1.10)
                                noise_party2 *= self.noise_multiplication_factor
                                encrypted_state_party3 *= self.fhe_encryption.encrypt_data(1.03)
                                noise_party3 *= self.noise_multiplication_factor

                                multiplication_times.append(time.time() - start_mul)  # Track multiplication time

                                # Track noise levels
                                noise_levels_party1.append(noise_party1)
                                noise_levels_party2.append(noise_party2)
                                noise_levels_party3.append(noise_party3)

                                state_transition_times.append(time.time() - start_state_transition)

                                # Homomorphic aggregation across parties
                                start_agg = time.time()
                                encrypted_state_aggregate += encrypted_tx_value_party1 + encrypted_tx_value_party2 + encrypted_tx_value_party3
                                aggregation_times.append(time.time() - start_agg)

                                total_gas_cost += gas_used
                                transaction_count += 1
                                transaction_values.append(transaction_value)
                    else:
                        # Log missing noise levels if no transactions are processed in the block
                        noise_levels_party1.append(noise_party1)
                        noise_levels_party2.append(noise_party2)
                        noise_levels_party3.append(noise_party3)

                except (AttributeError, ValueError, TypeError) as e:
                    self.logger.log_error("Error processing block transactions: {}".format(e))
            else:
                self.logger.log_error("Invalid block data received.")
                # Log missing noise levels if invalid block data is processed
                noise_levels_party1.append(noise_party1)
                noise_levels_party2.append(noise_party2)
                noise_levels_party3.append(noise_party3)

        # Decrypt the final states and track time
        start_dec = time.time()
        decrypted_final_state_party1 = self.fhe_encryption.decrypt_data(encrypted_state_party1)
        decrypted_final_state_party2 = self.fhe_encryption.decrypt_data(encrypted_state_party2)
        decrypted_final_state_party3 = self.fhe_encryption.decrypt_data(encrypted_state_party3)
        decrypted_final_aggregate_state = self.fhe_encryption.decrypt_data(encrypted_state_aggregate)
        decryption_times.append(time.time() - start_dec)

        # Memory usage for FHE
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Log results
        self.logger.log("Final decrypted state (Party 1): {}".format(decrypted_final_state_party1))
        self.logger.log("Final decrypted state (Party 2): {}".format(decrypted_final_state_party2))
        self.logger.log("Final decrypted state (Party 3): {}".format(decrypted_final_state_party3))
        self.logger.log("Final decrypted aggregate state: {}".format(decrypted_final_aggregate_state))
        self.logger.log("Total transactions: {}, Total Gas Cost: {}".format(transaction_count, total_gas_cost))

        # Perform advanced statistical analysis
        transaction_stats = self.analyze_transactions(transaction_values)
        block_analysis = self.analyze_block_data(block_sizes, block_times, gas_prices)

        # Log FHE performance metrics
        avg_enc_time = np.mean(encryption_times)
        avg_dec_time = np.mean(decryption_times)
        avg_state_transition_time = np.mean(state_transition_times)
        avg_mul_time = np.mean(multiplication_times)  # Track average multiplication time
        avg_agg_time = np.mean(aggregation_times)

        self.logger.log("FHE Performance - Avg Encryption Time: {:.6f}s, Avg Decryption Time: {:.6f}s".format(avg_enc_time, avg_dec_time))
        self.logger.log("Avg State Transition Time (Encrypted): {:.6f}s".format(avg_state_transition_time))
        self.logger.log("Avg Multiplication Time (Encrypted): {:.6f}s".format(avg_mul_time))
        self.logger.log("Avg Aggregation Time (Encrypted): {:.6f}s".format(avg_agg_time))
        self.logger.log("Memory Usage: Current={:.2f}KB, Peak={:.2f}KB".format(current_memory / 1024, peak_memory / 1024))

        # Perform Noise Growth Analysis
        self.analyze_noise_growth(noise_levels_party1, noise_levels_party2, noise_levels_party3)

        return {
            "decrypted_final_state_party1": decrypted_final_state_party1,
            "decrypted_final_state_party2": decrypted_final_state_party2,
            "decrypted_final_state_party3": decrypted_final_state_party3,
            "decrypted_final_aggregate_state": decrypted_final_aggregate_state,
            "total_gas_cost": total_gas_cost,
            "transaction_count": transaction_count,
            "transaction_stats": transaction_stats,
            "block_analysis": block_analysis,
            "noise_levels_party1": noise_levels_party1,  # Return noise levels
            "noise_levels_party2": noise_levels_party2,  # Return noise levels
            "noise_levels_party3": noise_levels_party3,  # Return noise levels
            "fhe_performance": {
                "encryption_times": encryption_times,
                "decryption_times": decryption_times,
                "state_transition_times": state_transition_times,
                "multiplication_times": multiplication_times,  # Include multiplication times in performance data
                "aggregation_times": aggregation_times,
                "avg_enc_time": avg_enc_time,
                "avg_dec_time": avg_dec_time,
                "avg_state_transition_time": avg_state_transition_time,
                "avg_mul_time": avg_mul_time,  # Include average multiplication time
                "avg_agg_time": avg_agg_time,
                "memory_usage": (current_memory, peak_memory)
            }
        }

    def fetch_recent_blocks(self, num_blocks: int) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch the most recent blocks from the blockchain.

        Args:
            num_blocks (int): Number of recent blocks to fetch.

        Returns:
            Optional[List[Dict[str, Any]]]: List of block data dictionaries or None if no blocks are fetched.
        """
        latest_block_response = self.api.get_block_by_number('latest')
        if latest_block_response and 'result' in latest_block_response:
            latest_block = int(latest_block_response['result'], 16)
            blocks = []
            for i in range(latest_block, latest_block - num_blocks, -1):
                block_data, retries = self.fetch_block_with_retries(i)
                if block_data and 'result' in block_data and isinstance(block_data['result'], dict):
                    blocks.append(block_data['result'])
                else:
                    self.logger.log_error("Failed to retrieve valid block data for block {} after {} retries.".format(i, retries))
            return blocks if blocks else None
        return None

    def fetch_block_with_retries(self, block_number: int, delay: int = 2) -> Tuple[Optional[Dict[str, Any]], int]:
        """
        Fetch a block with retries in case of failure.

        Args:
            block_number (int): Block number to fetch.
            delay (int): Delay between retries in seconds. Default is 2.

        Returns:
            Tuple[Optional[Dict[str, Any]], int]: Block data dictionary and number of retries.
        """
        retries = 0
        block_data = None
        while retries < self.max_retries:
            block_data = self.api.get_block_by_number(block_number)
            if block_data and 'result' in block_data and isinstance(block_data['result'], dict):
                return block_data, retries  # Valid block data found
            retries += 1
            self.logger.log("Retrying block {}... attempt {}".format(block_number, retries))
            time.sleep(delay)  # Wait before retrying

        return block_data, retries

    def decrypt_state(self, encrypted_state: Any) -> float:
        """
        Decrypt the final state.

        Args:
            encrypted_state (Any): Encrypted state to decrypt.

        Returns:
            float: Decrypted state value.
        """
        self.logger.log("Decrypting final state...")
        decrypted_state = encrypted_state.get_plain_text()
        return decrypted_state.item()

    def analyze_noise_growth(self, noise_levels_party1: List[float], noise_levels_party2: List[float], noise_levels_party3: List[float]) -> None:
        """
        Analyze how noise accumulates in the encrypted states for each party.

        Args:
            noise_levels_party1 (List[float]): Noise levels for party 1.
            noise_levels_party2 (List[float]): Noise levels for party 2.
            noise_levels_party3 (List[float]): Noise levels for party 3.
        """
        avg_noise_party1 = np.mean(noise_levels_party1)
        avg_noise_party2 = np.mean(noise_levels_party2)
        avg_noise_party3 = np.mean(noise_levels_party3)

        self.logger.log("Noise Growth Analysis (Party 1) - Avg Noise Level: {:.6f}, Max Noise: {:.6f}, Min Noise: {:.6f}".format(avg_noise_party1, np.max(noise_levels_party1), np.min(noise_levels_party1)))
        self.logger.log("Noise Growth Analysis (Party 2) - Avg Noise Level: {:.6f}, Max Noise: {:.6f}, Min Noise: {:.6f}".format(avg_noise_party2, np.max(noise_levels_party2), np.min(noise_levels_party2)))
        self.logger.log("Noise Growth Analysis (Party 3) - Avg Noise Level: {:.6f}, Max Noise: {:.6f}, Min Noise: {:.6f}".format(avg_noise_party3, np.max(noise_levels_party3), np.min(noise_levels_party3)))

    def analyze_transactions(self, transaction_values: List[float]) -> Dict[str, Union[float, int]]:
        """
        Perform advanced statistical analysis on the transaction values.

        Args:
            transaction_values (List[float]): List of transaction values.

        Returns:
            Dict[str, Union[float, int]]: Statistical analysis results including mean, variance, min, max, median, skewness, and kurtosis.
        """
        if not transaction_values:
            return {"mean": 0, "variance": 0, "min": 0, "max": 0, "median": 0, "skewness": 0, "kurtosis": 0}

        mean_val = np.mean(transaction_values)
        variance_val = np.var(transaction_values)
        min_val = np.min(transaction_values)
        max_val = np.max(transaction_values)
        median_val = np.median(transaction_values)
        skewness_val = skew(transaction_values)
        kurtosis_val = kurtosis(transaction_values)

        self.logger.log("Transaction Value Stats - Mean: {}, Variance: {}, Min: {}, Max: {}".format(mean_val, variance_val, min_val, max_val))
        self.logger.log("Median: {}, Skewness: {}, Kurtosis: {}".format(median_val, skewness_val, kurtosis_val))
        return {
            "mean": mean_val,
            "variance": variance_val,
            "min": min_val,
            "max": max_val,
            "median": median_val,
            "skewness": skewness_val,
            "kurtosis": kurtosis_val
        }

    def analyze_block_data(self, block_sizes: List[int], block_times: List[int], gas_prices: List[int]) -> Dict[str, Union[float, List[int]]]:
        """
        Perform advanced statistical analysis on block sizes, block times, and gas prices.

        Args:
            block_sizes (List[int]): List of block sizes.
            block_times (List[int]): List of block times.
            gas_prices (List[int]): List of gas prices.

        Returns:
            Dict[str, Union[float, List[int]]]: Statistical analysis results including average block size, average block time, average gas price, and gas price volatility.
        """
        if not block_sizes or not block_times or not gas_prices:
            self.logger.log("Insufficient data for block analysis.")
            return {
                "avg_block_size": 0,
                "avg_block_time": 0,
                "avg_gas_price": 0,
                "gas_price_volatility": 0,
                "block_times": [],
                "gas_prices": []
            }

        avg_block_size = np.mean(block_sizes)
        avg_block_time = np.mean(block_times)
        avg_gas_price = np.mean(gas_prices)
        gas_price_volatility = np.std(gas_prices)  # Standard deviation as a measure of volatility

        self.logger.log("Block Stats - Avg Block Size: {}, Avg Block Time: {}, Avg Gas Price: {}, Gas Price Volatility: {}".format(avg_block_size, avg_block_time, avg_gas_price, gas_price_volatility))
        
        return {
            "avg_block_size": avg_block_size,
            "avg_block_time": avg_block_time,
            "avg_gas_price": avg_gas_price,
            "gas_price_volatility": gas_price_volatility,
            "block_times": block_times,  # Ensure these are returned
            "gas_prices": gas_prices      # Ensure these are returned
        }