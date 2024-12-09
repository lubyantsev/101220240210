import yfinance as yf


def fetch_stock_data(ticker, period='1mo'):
    """
    Получает исторические данные акций по заданному тикеру и периоду.

    :param ticker: Тикер акций (например, 'AAPL' для Apple).
    :param period: Период исторических данных (например, '1mo', '1y').
    :return: DataFrame с историческими данными акций.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    """
    Добавляет скользящую среднюю к DataFrame.

    :param data: DataFrame с историческими данными акций.
    :param window_size: Размер окна для скользящей средней.
    :return: DataFrame с добавленной скользящей средней.
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_rsi(data, window=14):
    """
    Рассчитывает индекс относительной силы (RSI).

    :param data: DataFrame с историческими данными акций.
    :param window: Период для расчета RSI.
    :return: DataFrame с добавленным столбцом RSI.
    """
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Рассчитывает MACD и сигнальную линию.

    :param data: DataFrame с историческими данными акций.
    :param short_window: Период для короткой EMA.
    :param long_window: Период для длинной EMA.
    :param signal_window: Период для сигнальной линии.
    :return: DataFrame с добавленными столбцами MACD и сигнальной линии.
    """
    data['EMA_12'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_26'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA_12'] - data['EMA_26']
    data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data
