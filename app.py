import os
import sys
from compound_risk_scorer import CompoundRiskScorer

def main():
    """
    Main application entry point.
    Processes wallet addresses and generates comprehensive risk scores.
    """
    print("=== Compound Wallet Risk Scoring System ===")
    print("Initializing enhanced risk assessment engine...\n")
    
    # Initialize the risk scorer
    scorer = CompoundRiskScorer()
    
    # File paths
    input_file = "data/Wallet id - Sheet1.csv"
    output_file = "output/wallet_scores.csv"
    
    # Verify input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        print("Please ensure the wallet CSV file is in the correct location.")
        return 1
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    try:
        # Process wallets and generate comprehensive risk scores
        print("Processing wallets with enhanced risk assessment...")
        results = scorer.process_wallet_list(input_file, output_file)
        
        # Display summary
        print("\n" + "="*50)
        print("RISK SCORING COMPLETED SUCCESSFULLY")
        print("="*50)
        print(f"Total wallets processed: {len(results)}")
        print(f"Average risk score: {results['score'].mean():.1f}")
        print(f"Standard deviation: {results['score'].std():.1f}")
        
        # Risk distribution
        high_risk = len(results[results['score'] < 300])
        medium_risk = len(results[(results['score'] >= 300) & (results['score'] < 700)])
        low_risk = len(results[results['score'] >= 700])
        
        print(f"\nRisk Distribution:")
        print(f"  🔴 High Risk (0-299):    {high_risk:3d} wallets ({high_risk/len(results)*100:.1f}%)")
        print(f"  🟡 Medium Risk (300-699): {medium_risk:3d} wallets ({medium_risk/len(results)*100:.1f}%)")
        print(f"  🟢 Low Risk (700-1000):   {low_risk:3d} wallets ({low_risk/len(results)*100:.1f}%)")
        
        # Top risk factors
        print(f"\nKey Risk Indicators:")
        print(f"  Wallets with liquidations: {len(results[results['liquidation_count'] > 0])}")
        print(f"  Average repayment ratio: {results['repayment_ratio'].mean():.3f}")
        print(f"  Average utilization: {results['current_utilization'].mean():.3f}")
        print(f"  Average asset diversity: {results['asset_diversity'].mean():.1f}")
        
        print(f"\nOutput Files:")
        print(f"  📄 Simple scores: {output_file}")
        print(f"  📊 Detailed analysis: {output_file.replace('.csv', '_detailed.csv')}")
        print(f"  📖 Methodology: METHODOLOGY.md")
        
        return 0
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        print("Please check the input file format and try again.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)