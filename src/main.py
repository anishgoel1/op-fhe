from config_loader import ConfigLoader
from fhe_encryption import OptimismFHEEncryption
from state_simulation import FHEStateSimulator
from gas_cost_analysis import GasCostAnalysis
from logger import Logger
from typing import Any, Dict, Optional

def main() -> None:
    """
    Main function to load configuration, initialize components, simulate state transitions,
    and log the results including gas cost analysis and FHE performance metrics.
    """
    logger = Logger()

    # Load configuration
    config_loader = ConfigLoader()
    config: Dict[str, Any] = config_loader.load_config("config.json")
    api_key: str = config.get("api_key")
    
    # Initialize components
    state_simulator = FHEStateSimulator(api_key)
    gas_analyzer = GasCostAnalysis()

    # Simulate state transitions with real Optimism data using advanced FHE and MPC operations
    simulation_results: Optional[Dict[str, Any]] = state_simulator.simulate_state_with_real_data(num_blocks=20)

    if simulation_results is not None:
        # Unpack the simulation results
        decrypted_final_state_party1: Any = simulation_results["decrypted_final_state_party1"]
        decrypted_final_state_party2: Any = simulation_results["decrypted_final_state_party2"]
        decrypted_final_state_party3: Any = simulation_results["decrypted_final_state_party3"]
        decrypted_final_aggregate_state: Any = simulation_results["decrypted_final_aggregate_state"]
        total_gas_cost: float = simulation_results["total_gas_cost"]
        transaction_count: int = simulation_results["transaction_count"]
        transaction_stats: Any = simulation_results["transaction_stats"]
        block_analysis: Any = simulation_results["block_analysis"]
        fhe_performance: Dict[str, Any] = simulation_results["fhe_performance"]

        # Log decrypted final states for each party and aggregate state
        logger.log("Final decrypted state (Party 1): {}".format(decrypted_final_state_party1))
        logger.log("Final decrypted state (Party 2): {}".format(decrypted_final_state_party2))
        logger.log("Final decrypted state (Party 3): {}".format(decrypted_final_state_party3))
        logger.log("Final decrypted aggregate state: {}".format(decrypted_final_aggregate_state))
        logger.log("Total transactions: {}, Total Gas Cost: {}".format(transaction_count, total_gas_cost))

        # Analyze gas costs
        gas_analysis: Any = gas_analyzer.analyze_gas_costs([1, 2, 3, 4, 5], total_gas_cost)
        logger.log("Gas cost analysis: {}".format(gas_analysis))

        # Log transaction statistics
        logger.log("Transaction Stats: {}".format(transaction_stats))
        logger.log("Block Analysis: {}".format(block_analysis))

        # Log FHE performance metrics including multiplication times
        logger.log("FHE Performance - Avg Encryption Time: {:.6f}s".format(fhe_performance['avg_enc_time']))
        logger.log("Avg Decryption Time: {:.6f}s".format(fhe_performance['avg_dec_time']))
        logger.log("Avg State Transition Time (Encrypted): {:.6f}s".format(fhe_performance['avg_state_transition_time']))
        logger.log("Avg Multiplication Time (Encrypted): {:.6f}s".format(fhe_performance['avg_mul_time']))
        logger.log("Avg Aggregation Time (Encrypted): {:.6f}s".format(fhe_performance['avg_agg_time']))
        logger.log("Memory Usage - Current: {:.2f} KB, Peak: {:.2f} KB".format(fhe_performance['memory_usage'][0] / 1024, fhe_performance['memory_usage'][1] / 1024))

        # Check for noise levels before logging
        if "noise_levels_party1" in simulation_results and "noise_levels_party2" in simulation_results and "noise_levels_party3" in simulation_results:
            noise_levels_party1: Optional[list[float]] = simulation_results["noise_levels_party1"]
            noise_levels_party2: Optional[list[float]] = simulation_results["noise_levels_party2"]
            noise_levels_party3: Optional[list[float]] = simulation_results["noise_levels_party3"]

            if noise_levels_party1 and noise_levels_party2 and noise_levels_party3:
                # Perform Noise Growth Analysis
                logger.log("Noise Growth (Party 1): Avg Noise: {:.6f}, Max: {:.6f}, Min: {:.6f}".format(
                    sum(noise_levels_party1) / len(noise_levels_party1),
                    max(noise_levels_party1),
                    min(noise_levels_party1)
                ))
                logger.log("Noise Growth (Party 2): Avg Noise: {:.6f}, Max: {:.6f}, Min: {:.6f}".format(
                    sum(noise_levels_party2) / len(noise_levels_party2),
                    max(noise_levels_party2),
                    min(noise_levels_party2)
                ))
                logger.log("Noise Growth (Party 3): Avg Noise: {:.6f}, Max: {:.6f}, Min: {:.6f}".format(
                    sum(noise_levels_party3) / len(noise_levels_party3),
                    max(noise_levels_party3),
                    min(noise_levels_party3)
                ))
            else:
                logger.log("Noise data is missing or incomplete for one or more parties.")
        else:
            logger.log("Noise data is missing for one or more parties.")
    else:
        logger.log("Simulation did not return any valid results.")


if __name__ == "__main__":
    main()