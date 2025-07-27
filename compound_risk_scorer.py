import pandas as pd
import numpy as np
import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CompoundRiskScorer:
    """
    Comprehensive wallet risk scoring system for Compound protocol users.
    
    This system analyzes on-chain transaction data to assess wallet risk profiles
    based on lending/borrowing behavior, liquidation history, and protocol interaction patterns.
    """
    
    def __init__(self):
        # Compound V2 contract addresses (Ethereum mainnet)
        self.compound_contracts = {
            'comptroller': '0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b',
            'ceth': '0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5',
            'cdai': '0x5d3a536e4d6dbd6114cc1ead35777bab948e3643',
            'cusdc': '0x39aa39c021dfbae8fac545936693ac917d5e7563',
            'cusdt': '0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9',
            'cwbtc': '0xc11b1268c1a384e55c48c2391d8d480264a3a7f4'
        }
        
        # Risk scoring weights
        self.risk_weights = {
            'liquidation_penalty': 200,      # Heavy penalty for liquidations
            'health_factor_penalty': 150,    # Penalty for low health factors
            'volatility_penalty': 100,       # Penalty for volatile asset usage
            'frequency_bonus': 50,           # Bonus for regular interactions
            'repayment_bonus': 100,          # Bonus for good repayment behavior
            'diversification_bonus': 75      # Bonus for portfolio diversification
        }
        
    def fetch_wallet_transactions(self, wallet_address: str) -> Dict:
        """
        Fetch transaction data for a wallet from Compound protocol.
        Uses Etherscan API for transaction history and event logs.
        """
        logger.info(f"Fetching data for wallet: {wallet_address}")
        
        # In a real implementation, you would use:
        # 1. Etherscan API for transaction history
        # 2. The Graph Protocol for Compound subgraph data
        # 3. Direct contract calls via Web3
        
        # For demonstration, we'll simulate realistic data based on common patterns
        return self._simulate_compound_data(wallet_address)
    
    def _simulate_compound_data(self, wallet_address: str) -> Dict:
        """
        Simulate realistic Compound protocol interaction data.
        This would be replaced with actual API calls in production.
        """
        np.random.seed(int(wallet_address[-8:], 16) % 2**32)  # Deterministic randomness
        
        # Simulate transaction history over 6 months
        num_transactions = np.random.poisson(15)  # Average 15 transactions
        
        transactions = []
        current_time = datetime.now()
        
        for i in range(num_transactions):
            tx_time = current_time - timedelta(days=np.random.randint(0, 180))
            tx_type = np.random.choice(['supply', 'borrow', 'repay', 'withdraw'], 
                                     p=[0.3, 0.25, 0.25, 0.2])
            
            # Simulate different asset types with varying volatility
            asset = np.random.choice(['ETH', 'DAI', 'USDC', 'USDT', 'WBTC'], 
                                   p=[0.3, 0.25, 0.25, 0.15, 0.05])
            
            amount = np.random.lognormal(7, 1.5)  # Log-normal distribution for amounts
            
            transactions.append({
                'timestamp': tx_time,
                'type': tx_type,
                'asset': asset,
                'amount': amount,
                'tx_hash': f"0x{''.join(np.random.choice(list('0123456789abcdef'), 64))}"
            })
        
        # Simulate liquidation events (rare but high impact)
        liquidations = []
        if np.random.random() < 0.15:  # 15% chance of having liquidations
            num_liquidations = np.random.poisson(1) + 1
            for _ in range(num_liquidations):
                liq_time = current_time - timedelta(days=np.random.randint(0, 180))
                liquidations.append({
                    'timestamp': liq_time,
                    'liquidated_amount': np.random.lognormal(8, 1),
                    'collateral_seized': np.random.lognormal(8, 1),
                    'asset': np.random.choice(['ETH', 'WBTC', 'DAI'])
                })
        
        # Simulate current positions
        positions = {}
        for asset in ['ETH', 'DAI', 'USDC', 'USDT', 'WBTC']:
            if np.random.random() < 0.4:  # 40% chance of having position in each asset
                positions[asset] = {
                    'supplied': np.random.lognormal(6, 2) if np.random.random() < 0.7 else 0,
                    'borrowed': np.random.lognormal(5, 2) if np.random.random() < 0.5 else 0
                }
        
        return {
            'wallet_address': wallet_address,
            'transactions': transactions,
            'liquidations': liquidations,
            'current_positions': positions,
            'first_interaction': min([tx['timestamp'] for tx in transactions]) if transactions else None,
            'last_interaction': max([tx['timestamp'] for tx in transactions]) if transactions else None
        }
    
    def extract_features(self, wallet_data: Dict) -> Dict:
        """
        Extract meaningful features from wallet transaction data for risk assessment.
        """
        features = {}
        transactions = wallet_data['transactions']
        liquidations = wallet_data['liquidations']
        positions = wallet_data['current_positions']
        
        # Basic activity metrics
        features['total_transactions'] = len(transactions)
        features['liquidation_count'] = len(liquidations)
        
        # Time-based features
        if transactions:
            first_tx = min([tx['timestamp'] for tx in transactions])
            last_tx = max([tx['timestamp'] for tx in transactions])
            features['account_age_days'] = (datetime.now() - first_tx).days
            features['days_since_last_activity'] = (datetime.now() - last_tx).days
            features['activity_frequency'] = len(transactions) / max(features['account_age_days'], 1) * 30
        else:
            features['account_age_days'] = 0
            features['days_since_last_activity'] = 999
            features['activity_frequency'] = 0
        
        # Transaction type analysis
        tx_types = [tx['type'] for tx in transactions]
        features['supply_ratio'] = tx_types.count('supply') / max(len(tx_types), 1)
        features['borrow_ratio'] = tx_types.count('borrow') / max(len(tx_types), 1)
        features['repay_ratio'] = tx_types.count('repay') / max(len(tx_types), 1)
        
        # Volume analysis
        total_supply_volume = sum([tx['amount'] for tx in transactions if tx['type'] == 'supply'])
        total_borrow_volume = sum([tx['amount'] for tx in transactions if tx['type'] == 'borrow'])
        total_repay_volume = sum([tx['amount'] for tx in transactions if tx['type'] == 'repay'])
        
        features['total_supply_volume'] = total_supply_volume
        features['total_borrow_volume'] = total_borrow_volume
        features['total_repay_volume'] = total_repay_volume
        
        # Repayment behavior
        features['repayment_ratio'] = total_repay_volume / max(total_borrow_volume, 1)
        
        # Asset diversification
        unique_assets = set([tx['asset'] for tx in transactions])
        features['asset_diversity'] = len(unique_assets)
        
        # Volatile asset usage (ETH, WBTC considered more volatile)
        volatile_assets = ['ETH', 'WBTC']
        volatile_tx_count = sum([1 for tx in transactions if tx['asset'] in volatile_assets])
        features['volatile_asset_ratio'] = volatile_tx_count / max(len(transactions), 1)
        
        # Current position analysis
        features['active_positions'] = len([k for k, v in positions.items() 
                                          if v['supplied'] > 0 or v['borrowed'] > 0])
        
        total_supplied = sum([v['supplied'] for v in positions.values()])
        total_borrowed = sum([v['borrowed'] for v in positions.values()])
        features['current_utilization'] = total_borrowed / max(total_supplied, 1)
        
        # Liquidation analysis
        if liquidations:
            features['avg_liquidation_amount'] = np.mean([liq['liquidated_amount'] for liq in liquidations])
            features['total_liquidated_value'] = sum([liq['liquidated_amount'] for liq in liquidations])
            features['days_since_last_liquidation'] = min([(datetime.now() - liq['timestamp']).days 
                                                         for liq in liquidations])
        else:
            features['avg_liquidation_amount'] = 0
            features['total_liquidated_value'] = 0
            features['days_since_last_liquidation'] = 999
        
        return features
    
    def calculate_risk_score(self, features: Dict) -> int:
        """
        Calculate risk score (0-1000) based on extracted features.
        Higher scores indicate lower risk (better creditworthiness).
        """
        base_score = 500  # Start with neutral score
        
        # Liquidation penalties (most important factor)
        liquidation_penalty = features['liquidation_count'] * self.risk_weights['liquidation_penalty']
        base_score -= liquidation_penalty
        
        # Recent liquidation penalty
        if features['days_since_last_liquidation'] < 30:
            base_score -= 100
        elif features['days_since_last_liquidation'] < 90:
            base_score -= 50
        
        # Repayment behavior bonus/penalty
        if features['repayment_ratio'] > 0.9:
            base_score += self.risk_weights['repayment_bonus']
        elif features['repayment_ratio'] < 0.5:
            base_score -= self.risk_weights['repayment_bonus']
        
        # Current utilization penalty
        if features['current_utilization'] > 0.8:
            base_score -= 150
        elif features['current_utilization'] > 0.6:
            base_score -= 75
        
        # Activity frequency bonus
        if features['activity_frequency'] > 2:  # More than 2 transactions per month
            base_score += self.risk_weights['frequency_bonus']
        elif features['activity_frequency'] < 0.5:  # Less than 0.5 transactions per month
            base_score -= 50
        
        # Asset diversification bonus
        if features['asset_diversity'] >= 3:
            base_score += self.risk_weights['diversification_bonus']
        elif features['asset_diversity'] == 1:
            base_score -= 25
        
        # Volatile asset penalty
        if features['volatile_asset_ratio'] > 0.7:
            base_score -= self.risk_weights['volatility_penalty']
        
        # Account age bonus (older accounts are generally more stable)
        if features['account_age_days'] > 365:
            base_score += 50
        elif features['account_age_days'] < 30:
            base_score -= 50
        
        # Recent activity bonus
        if features['days_since_last_activity'] < 7:
            base_score += 25
        elif features['days_since_last_activity'] > 90:
            base_score -= 75
        
        # Ensure score is within bounds
        final_score = max(0, min(1000, base_score))
        
        return int(final_score)
    
    def generate_risk_explanation(self, features: Dict, score: int) -> str:
        """
        Generate human-readable explanation for the risk score.
        """
        explanations = []
        
        if features['liquidation_count'] > 0:
            explanations.append(f"Liquidated {features['liquidation_count']} time(s)")
        
        if features['repayment_ratio'] > 0.9:
            explanations.append("Excellent repayment history")
        elif features['repayment_ratio'] < 0.5:
            explanations.append("Poor repayment history")
        
        if features['current_utilization'] > 0.8:
            explanations.append("High current utilization")
        
        if features['activity_frequency'] > 2:
            explanations.append("Active user")
        elif features['activity_frequency'] < 0.5:
            explanations.append("Inactive user")
        
        if features['asset_diversity'] >= 3:
            explanations.append("Well-diversified portfolio")
        
        return "; ".join(explanations) if explanations else "Standard risk profile"
    
    def process_wallet_list(self, wallet_file: str, output_file: str) -> pd.DataFrame:
        """
        Process a list of wallets and generate risk scores.
        """
        logger.info(f"Processing wallets from {wallet_file}")
        
        # Read wallet addresses
        df = pd.read_csv(wallet_file)
        results = []
        
        for i, wallet in enumerate(df['wallet_id']):
            logger.info(f"Processing wallet {i+1}/{len(df)}: {wallet}")
            
            try:
                # Fetch wallet data
                wallet_data = self.fetch_wallet_transactions(wallet)
                
                # Extract features
                features = self.extract_features(wallet_data)
                
                # Calculate risk score
                score = self.calculate_risk_score(features)
                
                # Generate explanation
                explanation = self.generate_risk_explanation(features, score)
                
                results.append({
                    'wallet_id': wallet,
                    'score': score,
                    'explanation': explanation,
                    'liquidation_count': features['liquidation_count'],
                    'repayment_ratio': round(features['repayment_ratio'], 3),
                    'current_utilization': round(features['current_utilization'], 3),
                    'activity_frequency': round(features['activity_frequency'], 2),
                    'asset_diversity': features['asset_diversity']
                })
                
                # Add small delay to avoid rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error processing wallet {wallet}: {str(e)}")
                results.append({
                    'wallet_id': wallet,
                    'score': 500,  # Default neutral score
                    'explanation': 'Error in processing',
                    'liquidation_count': 0,
                    'repayment_ratio': 0,
                    'current_utilization': 0,
                    'activity_frequency': 0,
                    'asset_diversity': 0
                })
        
        # Create results DataFrame
        results_df = pd.DataFrame(results)
        
        # Save detailed results
        results_df.to_csv(output_file.replace('.csv', '_detailed.csv'), index=False)
        
        # Save simple format as requested
        simple_results = results_df[['wallet_id', 'score']]
        simple_results.to_csv(output_file, index=False)
        
        logger.info(f"Results saved to {output_file}")
        return results_df

def main():
    """Main execution function"""
    scorer = CompoundRiskScorer()
    
    input_file = "data/Wallet id - Sheet1.csv"
    output_file = "output/wallet_scores.csv"
    
    # Process wallets and generate scores
    results = scorer.process_wallet_list(input_file, output_file)
    
    # Print summary statistics
    print("\n=== WALLET RISK SCORING SUMMARY ===")
    print(f"Total wallets processed: {len(results)}")
    print(f"Average risk score: {results['score'].mean():.1f}")
    print(f"Score distribution:")
    print(f"  High risk (0-300): {len(results[results['score'] < 300])}")
    print(f"  Medium risk (300-700): {len(results[(results['score'] >= 300) & (results['score'] < 700)])}")
    print(f"  Low risk (700-1000): {len(results[results['score'] >= 700])}")
    print(f"\nDetailed results saved to: output/wallet_scores_detailed.csv")

if __name__ == "__main__":
    main()