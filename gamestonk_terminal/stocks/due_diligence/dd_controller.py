""" Due Diligence Controller """
__docformat__ = "numpy"

import argparse
import os
from typing import List
from pandas.core.frame import DataFrame
from prompt_toolkit.completion import NestedCompleter

from gamestonk_terminal.stocks.due_diligence import (
    fmp_view,
    business_insider_view,
    finviz_view,
    marketwatch_view,
    finnhub_view,
    csimarket_view,
    ark_view,
)
from gamestonk_terminal import feature_flags as gtff
from gamestonk_terminal.helper_funcs import (
    get_flair,
    parse_known_args_and_warn,
    check_positive,
    EXPORT_ONLY_RAW_DATA_ALLOWED,
)
from gamestonk_terminal.menu import session
from gamestonk_terminal.stocks.stocks_helper import load


class DueDiligenceController:
    """Due Diligence Controller"""

    # Command choices
    CHOICES = ["?", "cls", "help", "q", "quit", "load"]

    CHOICES_COMMANDS = [
        "sec",
        "rating",
        "pt",
        "rot",
        "est",
        "analyst",
        "supplier",
        "customer",
        "arktrades",
    ]

    CHOICES += CHOICES_COMMANDS

    def __init__(self, ticker: str, start: str, interval: str, stock: DataFrame):
        """Constructor

        Parameters
        ----------
        ticker : str
            Due diligence ticker symbol
        start : str
            Start date of the stock data
        interval : str
            Stock data interval
        stock : DataFrame
            Due diligence stock dataframe
        """
        self.ticker = ticker
        self.start = start
        self.interval = interval
        self.stock = stock

        self.dd_parser = argparse.ArgumentParser(add_help=False, prog="dd")
        self.dd_parser.add_argument(
            "cmd",
            choices=self.CHOICES,
        )

    def print_help(self):
        """Print help"""

        s_intraday = (f"Intraday {self.interval}", "Daily")[self.interval == "1440min"]
        if self.ticker and self.start:
            stock_text = f"{s_intraday} Stock: {self.ticker} (from {self.start.strftime('%Y-%m-%d')})"
        else:
            stock_text = f"{s_intraday} Stock: {self.ticker}"

        help_text = f"""
Due Diligence:
    cls           clear screen
    ?/help        show this menu again
    q             quit this menu, and shows back to main menu
    quit          quit to abandon program
    load          load new ticker

{stock_text}

Finviz:
    analyst       analyst prices and ratings of the company
FMP:
    rating        rating over time (daily)
Finnhub:
    rot           number of analysts ratings over time (monthly)
Business Insider:
    pt            price targets over time
    est           quarter and year analysts earnings estimates
Market Watch:
    sec           SEC filings
csimarket:
    supplier      list of suppliers
    customer      list of customers
cathiesark.com
    arktrades     get ARK trades for ticker
        """

        print(help_text)

    def switch(self, an_input: str):
        """Process and dispatch input

        Returns
        -------
        True, False or None
            False - quit the menu
            True - quit the program
            None - continue in the menu
        """

        # Empty command
        if not an_input:
            print("")
            return None

        (known_args, other_args) = self.dd_parser.parse_known_args(an_input.split())

        # Help menu again
        if known_args.cmd == "?":
            self.print_help()
            return None

        # Clear screen
        if known_args.cmd == "cls":
            os.system("cls||clear")
            return None

        return getattr(
            self, "call_" + known_args.cmd, lambda: "Command not recognized!"
        )(other_args)

    def call_help(self, _):
        """Process Help command"""
        self.print_help()

    def call_q(self, _):
        """Process Q command - quit the menu"""
        return False

    def call_quit(self, _):
        """Process Quit command - quit the program"""
        return True

    def call_load(self, other_args: List[str]):
        """Process load command"""
        self.ticker, self.start, self.interval, self.stock = load(
            other_args, self.ticker, self.start, "1440min", self.stock
        )

    def call_analyst(self, other_args: List[str]):
        """Process analyst command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="analyst",
            description="""
                Print analyst prices and ratings of the company. The following fields are expected:
                date, analyst, category, price from, price to, and rating. [Source: Finviz]
            """,
        )
        parser.add_argument(
            "--export",
            choices=["csv", "json", "xlsx"],
            default="",
            type=str,
            dest="export",
            help="Export dataframe data to csv,json,xlsx file",
        )
        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            finviz_view.analyst(ticker=self.ticker, export=ns_parser.export)

        except Exception as e:
            print(e, "\n")

    def call_pt(self, other_args: List[str]):
        """Process pt command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="pt",
            description="""Prints price target from analysts. [Source: Business Insider]""",
        )
        parser.add_argument(
            "--raw",
            action="store_true",
            dest="raw",
            help="Only output raw data",
        )
        parser.add_argument(
            "-n",
            "--num",
            action="store",
            dest="n_num",
            type=check_positive,
            default=10,
            help="Number of latest price targets from analysts to print.",
        )
        parser.add_argument(
            "--export",
            choices=["csv", "json", "xlsx"],
            default="",
            type=str,
            dest="export",
            help="Export dataframe data to csv,json,xlsx file",
        )

        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            business_insider_view.price_target_from_analysts(
                ticker=self.ticker,
                start=self.start,
                interval=self.interval,
                stock=self.stock,
                num=ns_parser.n_num,
                raw=ns_parser.raw,
                export=ns_parser.export,
            )

        except Exception as e:
            print(e, "\n")

    def call_est(self, other_args: List[str]):
        """Process est command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="est",
            description="""Yearly estimates and quarter earnings/revenues. [Source: Business Insider]""",
        )
        parser.add_argument(
            "--export",
            choices=["csv", "json", "xlsx"],
            default="",
            type=str,
            dest="export",
            help="Export dataframe data to csv,json,xlsx file",
        )
        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            business_insider_view.estimates(
                ticker=self.ticker,
                export=ns_parser.export,
            )

        except Exception as e:
            print(e, "\n")

    def call_rot(self, other_args: List[str]):
        """Process rot command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="rot",
            description="""
                Rating over time (monthly). [Source: Finnhub]
            """,
        )
        parser.add_argument(
            "-n",
            "--num",
            action="store",
            dest="n_num",
            type=check_positive,
            default=10,
            help="number of last months",
        )
        parser.add_argument(
            "--raw",
            action="store_true",
            dest="raw",
            help="Only output raw data",
        )
        parser.add_argument(
            "--export",
            choices=["csv", "json", "xlsx"],
            default="",
            type=str,
            dest="export",
            help="Export dataframe data to csv,json,xlsx file",
        )
        try:
            if other_args:
                if "-" not in other_args[0]:
                    other_args.insert(0, "-n")

            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            finnhub_view.rating_over_time(
                ticker=self.ticker,
                num=ns_parser.n_num,
                raw=ns_parser.raw,
                export=ns_parser.export,
            )

        except Exception as e:
            print(e, "\n")

    def call_rating(self, other_args: List[str]):
        """Process rating command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="rating",
            description="""
                Based on specific ratios, prints information whether the company
                is a (strong) buy, neutral or a (strong) sell. The following fields are expected:
                P/B, ROA, DCF, P/E, ROE, and D/E. [Source: Financial Modeling Prep]
            """,
        )
        parser.add_argument(
            "-n",
            "--num",
            action="store",
            dest="n_num",
            type=check_positive,
            default=10,
            help="number of last days to display ratings",
        )
        parser.add_argument(
            "--export",
            choices=["csv", "json", "xlsx"],
            default="",
            type=str,
            dest="export",
            help="Export dataframe data to csv,json,xlsx file",
        )

        try:
            if other_args:
                if "-" not in other_args[0]:
                    other_args.insert(0, "-n")

            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            fmp_view.rating(
                ticker=self.ticker,
                num=ns_parser.n_num,
                export=ns_parser.export,
            )

        except Exception as e:
            print(e, "\n")

    def call_sec(self, other_args: List[str]):
        """Process sec command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="sec",
            description="""
                Prints SEC filings of the company. The following fields are expected: Filing Date,
                Document Date, Type, Category, Amended, and Link. [Source: Market Watch]
            """,
        )
        parser.add_argument(
            "-n",
            "--num",
            action="store",
            dest="n_num",
            type=check_positive,
            default=5,
            help="number of latest SEC filings.",
        )
        parser.add_argument(
            "--export",
            choices=["csv", "json", "xlsx"],
            default="",
            type=str,
            dest="export",
            help="Export dataframe data to csv,json,xlsx file",
        )

        try:
            if other_args:
                if "-" not in other_args[0]:
                    other_args.insert(0, "-n")

            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            marketwatch_view.sec_filings(
                ticker=self.ticker,
                num=ns_parser.n_num,
                export=ns_parser.export,
            )

        except Exception as e:
            print(e, "\n")

    def call_supplier(self, other_args: List[str]):
        """Process supplier command"""
        parser = argparse.ArgumentParser(
            prog="supplier",
            add_help=False,
            description="List of suppliers from ticker provided. [Source: CSIMarket]",
        )
        parser.add_argument(
            "--export",
            choices=["csv", "json", "xlsx"],
            default="",
            type=str,
            dest="export",
            help="Export dataframe data to csv,json,xlsx file",
        )
        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            csimarket_view.suppliers(
                ticker=self.ticker,
                export=ns_parser.export,
            )

        except Exception as e:
            print(e, "\n")

    def call_customer(self, other_args: List[str]):
        """Process customer command"""
        parser = argparse.ArgumentParser(
            prog="customer",
            add_help=False,
            description="List of customers from ticker provided. [Source: CSIMarket]",
        )
        parser.add_argument(
            "--export",
            choices=["csv", "json", "xlsx"],
            default="",
            type=str,
            dest="export",
            help="Export dataframe data to csv,json,xlsx file",
        )
        try:
            ns_parser = parse_known_args_and_warn(parser, other_args)
            if not ns_parser:
                return

            csimarket_view.customers(
                ticker=self.ticker,
                export=ns_parser.export,
            )

        except Exception as e:
            print(e, "\n")

    def call_arktrades(self, other_args):
        """Process arktrades command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            prog="arktrades",
            description="""
                Get trades for ticker across all ARK funds.
            """,
        )
        parser.add_argument(
            "-n",
            "--num",
            help="Number of rows to show",
            dest="num",
            default=20,
            type=int,
        )
        parser.add_argument(
            "-s",
            "--show_ticker",
            action="store_true",
            default=False,
            help="Flag to show ticker in table",
            dest="show_ticker",
        )
        try:
            ns_parser = parse_known_args_and_warn(
                parser, other_args, export_allowed=EXPORT_ONLY_RAW_DATA_ALLOWED
            )
            if not ns_parser:
                return
            ark_view.display_ark_trades(
                ticker=self.ticker,
                num=ns_parser.num,
                export=ns_parser.export,
                show_ticker=ns_parser.show_ticker,
            )
        except Exception as e:
            print(e, "\n")


def menu(ticker: str, start: str, interval: str, stock: DataFrame):
    """Due Diligence Menu

    Parameters
    ----------
    ticker : str
        Due diligence ticker symbol
    start : str
        Start date of the stock data
    interval : str
        Stock data interval
    stock : DataFrame
        Due diligence stock dataframe
    """

    dd_controller = DueDiligenceController(ticker, start, interval, stock)
    dd_controller.call_help(None)

    while True:
        # Get input command from user
        if session and gtff.USE_PROMPT_TOOLKIT:
            completer = NestedCompleter.from_nested_dict(
                {c: None for c in dd_controller.CHOICES}
            )

            an_input = session.prompt(
                f"{get_flair()} (stocks)>(dd)> ",
                completer=completer,
            )
        else:
            an_input = input(f"{get_flair()} (stocks)>(dd)> ")

        try:
            process_input = dd_controller.switch(an_input)

            if process_input is not None:
                return process_input

        except SystemExit:
            print("The command selected doesn't exist\n")
            continue
