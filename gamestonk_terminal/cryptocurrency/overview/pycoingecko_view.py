"""CoinGecko view"""
__docformat__ = "numpy"

import os
import textwrap
from pandas.plotting import register_matplotlib_converters
from tabulate import tabulate
from gamestonk_terminal.helper_funcs import export_data
import gamestonk_terminal.cryptocurrency.overview.pycoingecko_model as gecko
from gamestonk_terminal import feature_flags as gtff

register_matplotlib_converters()

# pylint: disable=inconsistent-return-statements
# pylint: disable=R0904, C0302


def display_holdings_overview(coin: str, export: str) -> None:
    """Shows overview of public companies that holds ethereum or bitcoin. [Source: CoinGecko]

    Parameters
    ----------
    coin: str
        Cryptocurrency: ethereum or bitcoin
    export: str
        Export dataframe data to csv,json,xlsx
    """

    df = gecko.get_holdings_overview(endpoint=coin)

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df,
                headers=df.columns,
                floatfmt=".2f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "hold",
        df,
    )


def display_holdings_companies_list(coin: str, links: bool, export: str) -> None:
    """Shows Ethereum/Bitcoin Holdings by Public Companies [Source: CoinGecko]

    Track publicly traded companies around the world that are buying ethereum as part of corporate treasury

    Parameters
    ----------
    coin: str
        Cryptocurrency: ethereum or bitcoin
    links: bool
        Display urls
    export: str
        Export dataframe data to csv,json,xlsx
    """

    df = gecko.get_companies_assets(endpoint=coin)

    if links is True:
        df = df[["Rank", "Company", "Url"]]
    else:
        df.drop("Url", axis=1, inplace=True)

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df,
                headers=df.columns,
                floatfmt=".2f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "companies",
        df,
    )


def display_nft_of_the_day(export: str) -> None:
    """Shows NFT of the day "https://www.coingecko.com/en/nft" [Source: CoinGecko]

    NFT (Non-fungible Token) refers to digital assets with unique characteristics.
    Examples of NFT include crypto artwork, collectibles, game items, financial products, and more.

    Parameters
    ----------
    export: str
        Export dataframe data to csv,json,xlsx
    """

    df = gecko.get_nft_of_the_day()

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df,
                headers=df.columns,
                floatfmt=".2f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "nftday",
        df,
    )


def display_nft_market_status(export: str) -> None:
    """Shows overview data of nft markets "https://www.coingecko.com/en/nft" [Source: CoinGecko]

    NFT (Non-fungible Token) refers to digital assets with unique characteristics.
    Examples of NFT include crypto artwork, collectibles, game items, financial products, and more.

    Parameters
    ----------
    export: str
        Export dataframe data to csv,json,xlsx
    """

    df = gecko.get_nft_market_status()

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df,
                headers=df.columns,
                floatfmt=".2f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "nft",
        df,
    )


def display_exchange_rates(sortby: str, descend: bool, top: int, export: str) -> None:
    """Shows  list of crypto, fiats, commodity exchange rates. [Source: CoinGecko]

    Parameters
    ----------
    top: int
        Number of records to display
    sortby: str
        Key by which to sort data
    descend: bool
        Flag to sort data descending
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = gecko.get_exchange_rates().sort_values(by=sortby, ascending=descend)

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df.head(top),
                headers=df.columns,
                floatfmt=".2f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "exrates",
        df,
    )


def display_global_market_info(export: str) -> None:
    """Shows global statistics about crypto. [Source: CoinGecko]
        - market cap change
        - number of markets
        - icos
        - number of active crypto
        - market_cap_pct

    Parameters
    ----------
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = gecko.get_global_info()

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df,
                headers=df.columns,
                floatfmt=".2f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "global",
        df,
    )


def display_global_defi_info(export: str) -> None:
    """Shows global statistics about Decentralized Finances. [Source: CoinGecko]

    Parameters
    ----------
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = gecko.get_global_defi_info()

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df,
                headers=df.columns,
                floatfmt=".1f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "defi",
        df,
    )


def display_stablecoins(
    sortby: str, descend: bool, top: int, links: bool, export: str
) -> None:
    """Shows stablecoins data from "https://www.coingecko.com/en/stablecoins". [Source: CoinGecko]

    Parameters
    ----------
    top: int
        Number of records to display
    sortby: str
        Key by which to sort data
    descend: bool
        Flag to sort data descending
    links: bool
        Flag to display urls
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = gecko.get_stable_coins().sort_values(by=sortby, ascending=descend)

    df_data = df.copy()

    if links is True:
        df = df[["Rank", "Name", "Symbol", "Url"]]
    else:
        df.drop("Url", axis=1, inplace=True)

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df.head(top),
                headers=df.columns,
                floatfmt=".0f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "stables",
        df_data,
    )


def display_news(
    sortby: str, descend: bool, top: int, links: bool, export: str
) -> None:
    """Shows latest crypto news. [Source: CoinGecko]

    Parameters
    ----------
    top: int
        Number of records to display
    sortby: str
        Key by which to sort data
    descend: bool
        Flag to sort data descending
    links: bool
        Flag to display urls
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = gecko.get_news(n=top).sort_values(by=sortby, ascending=descend)

    df_data = df.copy()

    df["Title"] = df["Title"].apply(
        lambda x: "\n".join(textwrap.wrap(x, width=65)) if isinstance(x, str) else x
    )

    if not links:
        df.drop("Url", axis=1, inplace=True)
    else:
        df = df[["Index", "Url"]]

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df,
                headers=df.columns,
                floatfmt=".0f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "news",
        df_data,
    )


def display_categories(
    sortby: str, descend: bool, top: int, links: bool, export: str
) -> None:
    """Shows top cryptocurrency categories by market capitalization from https://www.coingecko.com/en/categories

    The cryptocurrency category ranking is based on market capitalization. [Source: CoinGecko]

    Parameters
    ----------
    top: int
        Number of records to display
    sortby: str
        Key by which to sort data
    descend: bool
        Flag to sort data descending
    links: bool
        Flag to display urls
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = gecko.get_top_crypto_categories().sort_values(by=sortby, ascending=descend)

    df_data = df.copy()

    if not links:
        df.drop("Url", axis=1, inplace=True)
    else:
        df = df[["Rank", "Name", "Url"]]

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df.head(top),
                headers=df.columns,
                floatfmt=".0f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "categories",
        df_data,
    )


def display_exchanges(
    sortby: str, descend: bool, top: int, links: bool, export: str
) -> None:
    """Shows list of top exchanges from CoinGecko. [Source: CoinGecko]

    Parameters
    ----------
    top: int
        Number of records to display
    sortby: str
        Key by which to sort data
    descend: bool
        Flag to sort data descending
    links: bool
        Flag to display urls
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = gecko.get_exchanges().sort_values(by=sortby, ascending=descend)

    if links is True:
        df = df[["Rank", "Name", "Url"]]
    else:
        df.drop("Url", axis=1, inplace=True)

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df.head(top),
                headers=df.columns,
                floatfmt=".1f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "exchanges",
        df,
    )


def display_platforms(sortby: str, descend: bool, top: int, export: str) -> None:
    """Shows list of financial platforms. [Source: CoinGecko]

    Parameters
    ----------
    top: int
        Number of records to display
    sortby: str
        Key by which to sort data
    descend: bool
        Flag to sort data descending
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = gecko.get_financial_platforms().sort_values(by=sortby, ascending=descend)

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df.head(top),
                headers=df.columns,
                floatfmt=".2f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "platforms",
        df,
    )


def display_products(sortby: str, descend: bool, top: int, export: str) -> None:
    """Shows list of financial products. [Source: CoinGecko]

    Parameters
    ----------
    top: int
        Number of records to display
    sortby: str
        Key by which to sort data
    descend: bool
        Flag to sort data descending
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = gecko.get_finance_products().sort_values(by=sortby, ascending=descend)

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df.head(top),
                headers=df.columns,
                floatfmt=".2f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "products",
        df,
    )


def display_indexes(sortby: str, descend: bool, top: int, export: str) -> None:
    """Shows list of crypto indexes. [Source: CoinGecko]

    Parameters
    ----------
    top: int
        Number of records to display
    sortby: str
        Key by which to sort data
    descend: bool
        Flag to sort data descending
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = gecko.get_indexes().sort_values(by=sortby, ascending=descend)

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df.head(top),
                headers=df.columns,
                floatfmt=".2f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "indexes",
        df,
    )


def display_derivatives(sortby: str, descend: bool, top: int, export: str) -> None:
    """Shows  list of crypto derivatives. [Source: CoinGecko]

    Parameters
    ----------
    top: int
        Number of records to display
    sortby: str
        Key by which to sort data
    descend: bool
        Flag to sort data descending
    export : str
        Export dataframe data to csv,json,xlsx file
    """

    df = gecko.get_derivatives().sort_values(by=sortby, ascending=descend)

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df.head(top),
                headers=df.columns,
                floatfmt=".4f",
                showindex=False,
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(df.to_string, "\n")

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "derivatives",
        df,
    )
