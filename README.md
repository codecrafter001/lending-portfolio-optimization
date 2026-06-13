# Digital Lending: Portfolio Optimization

## Project Overview
This project analyzes a digital lending portfolio to identify customer risk segments, early warning signals, and strategic recommendations for sustainable, risk-adjusted growth.

## Deliverables
1. **Synthetic Lending Dataset** - 10,000+ realistic customer records
2. **Data Analysis & Segmentation** - Risk-based customer clustering
3. **Policy Recommendation Report** - 4-6 pages addressed to CRO
4. **Presentation Deck** - Strategic insights with visualizations
5. **Code & Notebooks** - Reproducible analysis pipeline

## Project Structure
```
lending-portfolio-optimization/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   │   └── synthetic_lending_data.csv
│   └── processed/
│       ├── customer_segments.csv
│       ├── early_warnings.csv
│       └── portfolio_metrics.csv
├── notebooks/
│   ├── 01_data_generation.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   ├── 03_risk_segmentation.ipynb
│   ├── 04_early_warning_signals.ipynb
│   └── 05_strategy_recommendations.ipynb
├── src/
│   ├── __init__.py
│   ├── data_generator.py
│   ├── analysis.py
│   ├── segmentation.py
│   └── utils.py
├── reports/
│   ├── CRO_Policy_Recommendation.md
│   └── Executive_Summary.md
├── presentations/
│   └── Portfolio_Optimization_Deck.pptx
└── outputs/
    ├── visualizations/
    └── metrics/
```

## Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Run data generation: `python src/data_generator.py`
3. Run analysis: `jupyter notebook notebooks/01_data_generation.ipynb`
4. View reports in `reports/` folder

## Key Questions Addressed
1. Which customer segments exhibit materially different risk and repayment behaviors?
2. How do acquisition channels impact portfolio quality and customer lifetime value?
3. Which loan products and tenures deliver strongest risk-adjusted returns?
4. How can pricing strategies be tailored across segments?
5. What metrics should leadership monitor for proactive risk management?

## Author
CodeCrafter001 | June 2026
