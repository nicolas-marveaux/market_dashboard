import plotly.express as px
import plotly.graph_objects as go


def price_chart(price_series, ticker):
    fig = px.line(x=price_series.index,y=price_series.values,title=f"{ticker} Historical Price")
    fig.update_layout(xaxis_title="Date",yaxis_title="Price")
    return fig


def returns_chart(return_series, ticker):
    fig = px.bar(x=return_series.index,y=return_series.values,title=f"{ticker} Monthly Returns")
    fig.update_layout(xaxis_title="Date",yaxis_title="Return")
    return fig


def strategy_vs_benchmark_chart(backtest_summary):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=backtest_summary.index,y=backtest_summary["Strategy Equity"],mode="lines",name="Momentum Strategy"))
    fig.add_trace(go.Scatter(x=backtest_summary.index,y=backtest_summary["FEZ Equity"],mode="lines",name="FEZ Benchmark"))
    fig.update_layout(title="Momentum Strategy vs FEZ Benchmark",xaxis_title="Date",yaxis_title="Portfolio Value (Base = 100)")
    return fig


def drawdown_chart(backtest_summary):
    strategy_equity = backtest_summary["Strategy Equity"]
    fez_equity = backtest_summary["FEZ Equity"] 
    strategy_drawdown = (strategy_equity / strategy_equity.cummax()) - 1
    fez_drawdown = (fez_equity / fez_equity.cummax()) - 1
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=strategy_drawdown.index,y=strategy_drawdown,mode="lines",name="Momentum Strategy"))
    fig.add_trace(go.Scatter(x=fez_drawdown.index,y=fez_drawdown,mode="lines",name="FEZ Benchmark"))
    fig.update_layout(title="Drawdown: Momentum Strategy vs FEZ Benchmark",xaxis_title="Date",yaxis_title="Drawdown")
    return fig


def rolling_volatility_chart(backtest_summary, window=12):
    strategy_rolling_vol = (backtest_summary["Strategy Return"].rolling(window).std()*(12 ** 0.5))
    fez_rolling_vol = (backtest_summary["FEZ Return"].rolling(window).std()*(12 ** 0.5))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=strategy_rolling_vol.index,y=strategy_rolling_vol,mode="lines",name="Momentum Strategy"))
    fig.add_trace(go.Scatter(x=fez_rolling_vol.index,y=fez_rolling_vol,mode="lines",name="FEZ Benchmark"))
    fig.update_layout(title="12-Month Rolling Volatility",xaxis_title="Date",yaxis_title="Annualized Volatility")
    return fig


def turnover_chart(transaction_costs_summary):
    fig = px.line(x=transaction_costs_summary.index,y=transaction_costs_summary["Turnover"],title="Monthly Portfolio Turnover")
    fig.update_layout(xaxis_title="Date",yaxis_title="Turnover")
    return fig


def gross_vs_net_chart(transaction_costs_summary):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=transaction_costs_summary.index,y=transaction_costs_summary["Gross Equity"],mode="lines",name="Gross Momentum Strategy"))
    fig.add_trace(go.Scatter(x=transaction_costs_summary.index,y=transaction_costs_summary["Net Equity"],mode="lines",name="Net Momentum Strategy"))
    fig.update_layout(title="Gross vs Net Momentum Strategy",xaxis_title="Date",yaxis_title="Portfolio Value (Base = 100)")
    return fig


def robustness_heatmap(robustness_grid):
    sharpe_matrix = robustness_grid.pivot(index="Momentum Window",columns="Top Quantile",values="Sharpe Ratio")
    sharpe_matrix = sharpe_matrix.reindex(index=["6-1", "9-1", "12-1"],columns=["Top 20%", "Top 30%", "Top 40%"])

    fig = px.imshow(sharpe_matrix,text_auto=".2f",aspect="auto",color_continuous_scale="Blues",title="Robustness Heatmap: Sharpe Ratio")
    fig.update_layout(xaxis_title="Selection Threshold",yaxis_title="Momentum Window",xaxis=dict(type="category"),yaxis=dict(type="category"))
    return fig

def best_base_worst_chart(robustness_grid):
    robustness_grid = robustness_grid.copy()
    best_row = robustness_grid.loc[robustness_grid["Sharpe Ratio"].idxmax()]
    worst_row = robustness_grid.loc[robustness_grid["Sharpe Ratio"].idxmin()]

    categories = ["Base: 12-1 | Top 30%",
        f"Best: {best_row['Momentum Window']} | {best_row['Top Quantile']}",
        f"Worst: {worst_row['Momentum Window']} | {worst_row['Top Quantile']}"]

    values = [robustness_grid[(robustness_grid["Momentum Window"] == "12-1") & (robustness_grid["Top Quantile"] == "Top 30%")]["Sharpe Ratio"].iloc[0],best_row["Sharpe Ratio"],worst_row["Sharpe Ratio"]]

    fig = px.bar(x=categories,y=values,title="Best / Base / Worst Parameter Combinations")
    fig.update_layout(xaxis_title="Parameter Combination",yaxis_title="Sharpe Ratio")
    return fig