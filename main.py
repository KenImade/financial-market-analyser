import argparse
# import matplotlib.pyplot as plt
# import pandas as pd

from src.api.alpha_vantage import AlphaVantageAPI
from src.core.data_processing import DataTransformer
from src.core.report_generator import ReportGenerator

def parse_arguments():
    parser = argparse.ArgumentParser(description='Financial Market Analysis Tool')
    parser.add_argument('--api-key', help='Your Alpha Vantage API Key', required=True)
    parser.add_argument('--symbol', help='Stock symbol to analyze', required=True)
    # Add more arguments as needed
    return parser.parse_args()


def main():
    
    args = parse_arguments()

    api = AlphaVantageAPI(args.api_key)

    # data retrieval
    daily_stock_data = api.get_daily_stock_data(args.symbol)
    weekly_stock_data = api.get_weekly_stock_data(args.symbol)
    monthly_stock_data = api.get_monthly_stock_data(args.symbol)
    company_info = api.get_company_overview_data(args.symbol)

    print("Data retrieved successfully.")
    
    # data processing
    daily_stock_data_cleaned = DataTransformer(daily_stock_data).clean_data()
    weekly_stock_data_cleaned = DataTransformer(weekly_stock_data).clean_data()
    monthly_stock_data_cleaned = DataTransformer(monthly_stock_data).clean_data()

    print("Data processed successfully.")

    # Generate report
    report_generator = ReportGenerator(company_info, monthly_stock_data_cleaned, weekly_stock_data_cleaned, daily_stock_data_cleaned)
    report_generator.plot_line(args.symbol)
    report_generator.plot_line(args.symbol, "W")
    report_generator.plot_line(args.symbol, "M")

    # dummy_df = pd.DataFrame({'date':[2, 4, 5, 7], 'stock_price':[1000, 2000, 20000, 4000]})
    # report_generator = ReportGenerator({}, dummy_df, dummy_df, dummy_df)
    
    report_generator.generate_pdf_report()

    print("PDF report generated successfully.")

if __name__ == "__main__":
    main()