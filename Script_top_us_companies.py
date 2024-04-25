{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests\n",
    "from bs4 import BeautifulSoup\n",
    "import pandas as pd\n",
    "import yfinance as yf"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Este script primero obtiene la lista de empresas del NASDAQ-100 utilizando requests y BeautifulSoup, y luego utiliza yfinance para obtener información financiera de estas empresas. Finalmente, imprime los datos financieros en forma de DataFrame de pandas."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "def obtener_empresas_nasdaq100():\n",
    "    url = 'https://en.wikipedia.org/wiki/NASDAQ-100'\n",
    "    respuesta = requests.get(url) \n",
    "    soup = BeautifulSoup(respuesta.text, 'html.parser')\n",
    "    tabla = soup.find('table', {'id': 'constituents'})\n",
    "    df = pd.read_html(str(tabla))[0]\n",
    "    return df['Ticker'].tolist()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Usuario\\AppData\\Local\\Temp\\ipykernel_10828\\3301309116.py:6: FutureWarning: Passing literal html to 'read_html' is deprecated and will be removed in a future version. To read from a literal string, wrap it in a 'StringIO' object.\n",
      "  df = pd.read_html(str(tabla))[0]\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "                               Empresa  Último Precio  \\\n",
      "ADBE                        Adobe Inc.     473.440002   \n",
      "ADP    Automatic Data Processing, Inc.     246.339996   \n",
      "ABNB                      Airbnb, Inc.     163.009995   \n",
      "GOOGL                    Alphabet Inc.     156.000000   \n",
      "GOOG                     Alphabet Inc.     157.949997   \n",
      "...                                ...            ...   \n",
      "WBA     Walgreens Boots Alliance, Inc.      17.600000   \n",
      "WBD    Warner Bros. Discovery, Inc. -        8.290000   \n",
      "WDAY                     Workday, Inc.     254.059998   \n",
      "XEL                   Xcel Energy Inc.      55.009998   \n",
      "ZS                       Zscaler, Inc.     174.809998   \n",
      "\n",
      "       Capitalización de Mercado  Ingresos Totales        EBITDA  \\\n",
      "ADBE                212101120000       19936000000    7589000192   \n",
      "ADP                 101194252288       18585899008    5305200128   \n",
      "ABNB                103565459456        9916999680    1548999936   \n",
      "GOOGL              1950499209216      307393986560  100171997184   \n",
      "GOOG               1950729895936      307393986560  100171997184   \n",
      "...                          ...               ...           ...   \n",
      "WBA                  15183749120      144596992000    3711000064   \n",
      "WBD                  20311576576       41321000960    7408999936   \n",
      "WDAY                 67119603712        7258999808     465000000   \n",
      "XEL                  30556403712       14206000128    5180000256   \n",
      "ZS                   26196676608        1895507968    -153450000   \n",
      "\n",
      "       Flujo de Caja Libre   Deuda Total  \n",
      "ADBE          6.730375e+09  4.086000e+09  \n",
      "ADP           3.193913e+09  3.436200e+09  \n",
      "ABNB          2.831875e+09  2.304000e+09  \n",
      "GOOGL         5.865775e+10  2.986700e+10  \n",
      "GOOG          5.865775e+10  2.986700e+10  \n",
      "...                    ...           ...  \n",
      "WBA           3.348750e+08  3.462700e+10  \n",
      "WBD           2.003575e+10  4.729000e+10  \n",
      "WDAY          2.006125e+09  3.296000e+09  \n",
      "XEL          -1.055250e+09  2.757800e+10  \n",
      "ZS            6.087174e+08  1.238553e+09  \n",
      "\n",
      "[101 rows x 7 columns]\n"
     ]
    }
   ],
   "source": [
    "def obtener_datos_financieros(tickers):\n",
    "    datos = {}\n",
    "    for ticker in tickers:\n",
    "        empresa = yf.Ticker(ticker)\n",
    "        hist = empresa.history(period=\"1d\")\n",
    "        info = empresa.info\n",
    "        \n",
    "        datos[ticker] = { \n",
    "            'Empresa': info.get('shortName'),\n",
    "            'Último Precio': hist['Close'].iloc[-1] if not hist.empty else None,\n",
    "            'Capitalización de Mercado': info.get('marketCap'),\n",
    "            'Ingresos Totales': info.get('totalRevenue'),\n",
    "            'EBITDA': info.get('ebitda'),\n",
    "            'Flujo de Caja Libre': info.get('freeCashflow'),\n",
    "            'Deuda Total': info.get('totalDebt')\n",
    "        }\n",
    "    return pd.DataFrame.from_dict(datos, orient='index')\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    empresas_nasdaq100 = obtener_empresas_nasdaq100()\n",
    "    datos_financieros = obtener_datos_financieros(empresas_nasdaq100)\n",
    "    print(datos_financieros)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Usuario\\AppData\\Local\\Temp\\ipykernel_10828\\3301309116.py:6: FutureWarning: Passing literal html to 'read_html' is deprecated and will be removed in a future version. To read from a literal string, wrap it in a 'StringIO' object.\n",
      "  df = pd.read_html(str(tabla))[0]\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "                               Empresa  Último Precio  \\\n",
      "ADBE                        Adobe Inc.     473.440002   \n",
      "ADP    Automatic Data Processing, Inc.     246.339996   \n",
      "ABNB                      Airbnb, Inc.     163.009995   \n",
      "GOOGL                    Alphabet Inc.     156.000000   \n",
      "GOOG                     Alphabet Inc.     157.949997   \n",
      "AMZN                  Amazon.com, Inc.     173.669998   \n",
      "AMD       Advanced Micro Devices, Inc.     153.759995   \n",
      "AEP    American Electric Power Company      86.860001   \n",
      "AMGN                        Amgen Inc.     269.380005   \n",
      "ADI               Analog Devices, Inc.     197.940002   \n",
      "\n",
      "       Capitalización de Mercado  Ingresos Totales        EBITDA  \\\n",
      "ADBE                212101120000       19936000000    7589000192   \n",
      "ADP                 101194252288       18585899008    5305200128   \n",
      "ABNB                103565459456        9916999680    1548999936   \n",
      "GOOGL              1950499209216      307393986560  100171997184   \n",
      "GOOG               1950729895936      307393986560  100171997184   \n",
      "AMZN               1806636941312      574784995328   85515001856   \n",
      "AMD                 248497684480       22680000512    3854000128   \n",
      "AEP                  45739610112       18982299648    6979700224   \n",
      "AMGN                144488972288       28189999104   12234999808   \n",
      "ADI                  98160033792       11568613376    5681083904   \n",
      "\n",
      "       Flujo de Caja Libre   Deuda Total  \n",
      "ADBE          6.730375e+09  4.086000e+09  \n",
      "ADP           3.193913e+09  3.436200e+09  \n",
      "ABNB          2.831875e+09  2.304000e+09  \n",
      "GOOGL         5.865775e+10  2.986700e+10  \n",
      "GOOG          5.865775e+10  2.986700e+10  \n",
      "AMZN          4.547575e+10  1.615740e+11  \n",
      "AMD           2.205375e+09  3.109000e+09  \n",
      "AEP          -3.056362e+09  4.392150e+10  \n",
      "AMGN          3.120625e+09  6.542300e+10  \n",
      "ADI           2.990380e+09  7.027513e+09  \n"
     ]
    }
   ],
   "source": [
    "if __name__ == \"__main__\":\n",
    "    empresas_nasdaq100 = obtener_empresas_nasdaq100()\n",
    "    datos_financieros = obtener_datos_financieros(empresas_nasdaq100)\n",
    "    \n",
    "    # Mostrar las primeras 10 empresas\n",
    "    print(datos_financieros.head(10))\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.11"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
