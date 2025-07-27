# API Configuration
ETHERSCAN_API_KEY = "YOUR_ETHERSCAN_API_KEY" 
INFURA_PROJECT_ID = "YOUR_INFURA_PROJECT_ID" 

# Compound Protocol Contract Addresses (Ethereum Mainnet)
COMPOUND_CONTRACTS = {
    'comptroller': '0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b',
    'ceth': '0x4ddc2d193948926d02f9b1fe9e1daa0718270ed5',
    'cdai': '0x5d3a536e4d6dbd6114cc1ead35777bab948e3643',
    'cusdc': '0x39aa39c021dfbae8fac545936693ac917d5e7563',
    'cusdt': '0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9',
    'cwbtc': '0xc11b1268c1a384e55c48c2391d8d480264a3a7f4',
    'ccomp': '0x70e36f6bf80a52b3b46b3af8e106cc0ed743e8e4',
    'cuni': '0x35a18000230da775cac24873d00ff85bccded550'
}

# Risk Scoring Weights (adjustable parameters)
RISK_WEIGHTS = {
    'liquidation_penalty': 200,      # Penalty per liquidation event
    'health_factor_penalty': 150,    # Penalty for low health factors
    'volatility_penalty': 100,       # Penalty for volatile asset usage
    'frequency_bonus': 50,           # Bonus for regular interactions
    'repayment_bonus': 100,          # Bonus for good repayment behavior
    'diversification_bonus': 75,     # Bonus for portfolio diversification
    'account_age_bonus': 50,         # Bonus for account maturity
    'recent_activity_bonus': 25      # Bonus for recent activity
}

# Asset Classifications
VOLATILE_ASSETS = ['ETH', 'WBTC', 'COMP', 'UNI']
STABLE_ASSETS = ['DAI', 'USDC', 'USDT']

# Risk Thresholds
RISK_THRESHOLDS = {
    'high_utilization': 0.8,         # Above this is high risk
    'medium_utilization': 0.6,       # Above this is medium risk
    'good_repayment_ratio': 0.9,     # Above this gets bonus
    'poor_repayment_ratio': 0.5,     # Below this gets penalty
    'high_activity_frequency': 2.0,  # Transactions per month
    'low_activity_frequency': 0.5,   # Transactions per month
    'min_diversification': 3,        # Assets for diversification bonus
    'mature_account_days': 365,      # Days for account age bonus
    'recent_activity_days': 7,       # Days for recent activity bonus
    'recent_liquidation_days': 30,   # Days for recent liquidation penalty
    'medium_liquidation_days': 90    # Days for medium liquidation penalty
}

# Scoring Bounds
MIN_SCORE = 0
MAX_SCORE = 1000
BASE_SCORE = 500

# Processing Configuration
BATCH_SIZE = 10                      # Wallets to process in parallel
API_RATE_LIMIT_DELAY = 0.1          # Seconds between API calls
MAX_RETRIES = 3                      # Maximum API retry attempts
TIMEOUT_SECONDS = 30                 # API request timeout

# Output Configuration
OUTPUT_PRECISION = {
    'score': 0,                      # Integer scores
    'ratios': 3,                     # 3 decimal places for ratios
    'frequencies': 2                 # 2 decimal places for frequencies
}

# Logging Configuration
LOG_LEVEL = 'INFO'                   # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# File Paths
DEFAULT_INPUT_FILE = "data/Wallet id - Sheet1.csv"
DEFAULT_OUTPUT_FILE = "output/wallet_scores.csv"
DETAILED_OUTPUT_SUFFIX = "_detailed"
METHODOLOGY_FILE = "METHODOLOGY.md"