from typing import List, Tuple
from logger import Logger

class GasCostAnalysis:
    def __init__(self):
        self.logger = Logger()

    def analyze_gas_costs(self, encrypted_transactions: List[str], total_gas_cost: float) -> Tuple[float, float]:
        """
        Analyze the gas costs of transactions.

        Args:
            encrypted_transactions (List[str]): A list of encrypted transaction strings.
            total_gas_cost (float): The total gas cost for all transactions.

        Returns:
            Tuple[float, float]: A tuple containing the total gas cost and the average gas cost per transaction.
        """
        transaction_count = len(encrypted_transactions)
        if transaction_count > 0:
            average_gas_per_tx = total_gas_cost / transaction_count
        else:
            average_gas_per_tx = 0
        self.logger.log("Total Gas Cost: {}, Average Gas per Transaction: {}".format(total_gas_cost, average_gas_per_tx))
        return total_gas_cost, average_gas_per_tx