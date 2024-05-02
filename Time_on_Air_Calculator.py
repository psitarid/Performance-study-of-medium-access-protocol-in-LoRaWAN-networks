import numpy as np
import math
import matplotlib.pyplot as plt
#Time on Air Calculation in msec


def find_payload(BW, SF, payload, header, CRC, DE, CR):
    T_symbol = 2**SF/BW *1000
    payload_symbols = 8 + np.max(np.ceil((8*payload-4*SF + 28 + 16*CRC - 20*header)/(4*(SF - 2*DE)))*(CR + 4),0)
    T_payload = payload_symbols * T_symbol

    return T_payload

def Time_on_Air(BW, SF, preamble, payload, header, CRC, DE, CR):
    T_symbol = 2**SF/BW *1000
    T_preamble = (preamble + 4.25)* T_symbol
    payload_symbols = 8 + np.max(np.ceil((8*payload-4*SF + 28 + 16*CRC - 20*header)/(4*(SF - 2*DE)))*(CR + 4),0)
    T_payload = payload_symbols * T_symbol
    ToA = T_preamble + T_payload

    print(f'ToA = {ToA} ms')
    print(f'Tsymbol = {T_symbol} ms ')
    print(f'Tpreamble = {T_preamble} ms')
    print(f'Payload Symbols = {payload_symbols} symbols')
    print(f'Tpayload = {T_payload} ms')

    return ToA