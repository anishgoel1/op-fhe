from logger import Logger

class GasCostAnalysis:
    def __init__(self):
        self.logger = Logger()

    def analyze_gas_costs(self, encrypted_transactions, total_gas_cost):
        transaction_count = len(encrypted_transactions)
        if transaction_count > 0:
            average_gas_per_tx = total_gas_cost / transaction_count
        else:
            average_gas_per_tx = 0
        self.logger.log("Total Gas Cost: {}, Average Gas per Transaction: {}".format(total_gas_cost, average_gas_per_tx))
        return total_gas_cost, average_gas_per_tx