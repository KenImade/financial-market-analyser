import os
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib import styles
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors

class ReportGenerator:
    """
    Generates plots and reports for stock data
    """

    def __init__(self, company_info: dict, monthly_data: pd.DataFrame, weekly_data: pd.DataFrame, daily_data: pd.DataFrame):
        self.company_info = company_info
        self.monthly_data = monthly_data.iloc[:11, :].copy()
        self.weekly_data = weekly_data.iloc[:7, :].copy()
        self.daily_data = daily_data.iloc[:11, :].copy()

        self._preprocessing()

    def _preprocessing(self):
        """
        Sorts data by date
        """
        self.monthly_data.sort_values(by='date', inplace=True)
        self.weekly_data.sort_values(by='date', inplace=True)
        self.daily_data.sort_values(by='date', inplace=True)

    def plot_line(self, symbol: str, time_period: str = "D") -> None:
        """
        Generates line plot for stock data

        Args:
            symbol: Stock ticker symbol
            time_period: Interval of stock data. 'W' denotes weekly, 'M' denotes monthly
                defaults to daily if not specified.
        
        Returns:
            None
        """
        if time_period == 'W':
            period = "Weekly"
            data = self.weekly_data
        elif time_period == 'M':
            period = "Monthly"
            data = self.monthly_data
        else:
            period = "Daily (Hrs)"
            data = self.daily_data


        margin = 0.09  # margin in inches
        a4_width = 8.27  # A4 width in inches
        plot_width = a4_width - (2 * margin)  # width of the plot
        plot_height = plot_width / 3  # maintain a 1:3 aspect ratio (height:width)

        fig = plt.figure(figsize=(plot_width, plot_height))
        plt.plot(data['date'], data['stock_price'], marker='o')
        plt.title(f"{period} trend of '{symbol}' stock", loc='left', fontweight='bold', fontsize=10)
        plt.ylabel("Stock Price (USD)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        self.save_plot(fig, f"{period}_plot.png")

    def save_plot(self, figure: plt.Figure, filename="plot.png") -> None:
        """
        Saves plot as png file to the output directory

        Args:
            figure: figure object to be saved
            filename: name of the plot
        
        Retuns:
            None
        """
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
        figure.savefig(output_path, dpi=300) # save with high dpi for better resolution

    def generate_pdf_report(self, output_path="output/report.pdf"):
        data = self.company_info

        width, height = A4

        # Define left and right margins
        left_margin = 1 * inch
        right_margin = 1 * inch

        doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=left_margin, rightMargin=right_margin)
        story = []

        # Title style
        title_style = styles.getSampleStyleSheet()['Title']

        # Add Title
        title = Paragraph(f"Stock Analysis Report for {data['Name']}", title_style)
        story.append(title)
        story.append(Spacer(1, 12))  # Add a little space

        # Company Overview Heading
        heading_style = styles.getSampleStyleSheet()['Heading2']
        overview_title = Paragraph("Company Overview", heading_style)
        story.append(overview_title)
        story.append(Spacer(1, 12))

        # Company Overview Style - Increase font size here
        overview_style = styles.getSampleStyleSheet()['Normal']
        overview_style.fontSize = 12  # Increase font size as needed
        overview_style.leading = 14  # Adjust leading (space between lines) to match font size

        # Company Overview Paragraph - Adjust width if necessary
        overview_text = data['Description']
        overview_paragraph = Paragraph(overview_text, overview_style)
        story.append(overview_paragraph)
        story.append(Spacer(1, 12))

        # Metrics
        metrics_title = Paragraph("Metrics", heading_style)
        story.append(metrics_title)
        story.append(Spacer(1, 12))

        # Prepare data for the table
        metrics_data = [
            ["MarketCap", data['MarketCapitalization'], "EPS", data['EPS'], "P/E Ratio", data['PERatio']],
            ["Revenue", data['RevenueTTM'], "Gross Profit", data['GrossProfitTTM'], "Operating Margin", data['OperatingMarginTTM']],
            ["Return on Equity", data['ReturnOnEquityTTM'], "Rev. per Share", data['RevenuePerShareTTM'], "Profit Margin", data['ProfitMargin']],
            ["Book Value", data['BookValue'], "Dividend Yield", data['DividendYield']]
        ]

        # Create the table with the data
        metrics_table = Table(metrics_data, colWidths=[1.25*inch]*3)

        # Add style to the table
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.beige),
            ('TEXTCOLOR',(0,0),(-1,0),colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND',(0,1),(-1,-1),colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ])
        metrics_table.setStyle(table_style)

        # Add table to story
        story.append(metrics_table)

        story.append(Spacer(1, 12))

        # Plots
        # You can convert other metrics to Paragraphs as well and append to story

        # Add plots
        # Check if the image file exists before adding
        daily_plot_path = "output/Daily (Hrs)_plot.png"
        weekly_plot_path = "output/Weekly_plot.png"
        monthly_plot_path = "output/Monthly_plot.png"
        
        if os.path.exists(daily_plot_path):
            img = Image(daily_plot_path, 8*inch, 3*inch)  # Example size
            story.append(img)
        
        if os.path.exists(weekly_plot_path):
            img = Image(weekly_plot_path, 8*inch, 3*inch)
            story.append(img)

        if os.path.exists(monthly_plot_path):
            img = Image(monthly_plot_path, 8*inch, 3*inch)
            story.append(img)
        
        story.append(Spacer(1, 12))
        
        # Add credits text with URL at the end
        normal_style = styles.getSampleStyleSheet()['Normal']
        report_credits = "Report generated by Financial Market Analyzer (https://github.com/KenImade/financial-market-analyser) by Kenneth Imade"
        credits_paragraph = Paragraph(report_credits, normal_style)
        story.append(credits_paragraph)
        
        # Build the document with the story
        doc.build(story)

        # If you need to add elements with exact positioning using Canvas, do it after building the document.
        # But be cautious, as it can overlap with existing content if not carefully positioned.