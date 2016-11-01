""" Checks cartridge usage
"""
import pandas as pd
import re

ON = re.compile(r'On:\s(\d+)')
OFF = re.compile(r'Off:\s(\d+)')

""" Don't use your cartridge more than 1000 h!"""
MAX_USE = 1000 * 60 * 60 

def usage_list(logfile):
    """ Creates a list of usage from log file

    Note:
        Log file must have the following format where the integers
        are unix time stamps.
    
          On: 1474557504
          Off: 1474557535
          On: 1474557504
          Off: 1474557535
          On: 1474558817
          Off: 1474559945
          On: 1474612596
          Off: 1474623146
          On: 1474643767
          Off: 1474644763
          On: 1474644785
          Off: 1474644787
          On: 1474701427
          Off: 1474703953
          On: 1474710909

    Args:
        logfile (basestring): filename of log file

    Returns:
        (list) list of cartridge uses in seconds
    """
    usage = []

    with open(logfile, 'r') as log:
        is_on = False
    
        for line in log:
            m_on = ON.match(line)
            m_off = OFF.match(line)
            f_on = bool(m_on)
            f_off = bool(m_off)
        
            is_valid = (is_on and f_off) or ((not is_on) and f_on)
            if is_valid:
                is_on = f_on
            
                if is_on:
                    t_on = int(m_on.group(1))
                else:
                    t_off = int(m_off.group(1))
                    usage.append(t_off - t_on)
            elif is_on:
                # Turend on but not correctly off
                usage.append(None)
            else:
                """If it was correctly turned off,
                we are skipping that line
                """
                pass
        return usage

def usetime(usage):
    """ Finds total usage
    
    Faulty entries will be substituted for 75 %-quantil
    
    Returns:
         (int) total use time
    """
    df = pd.DataFrame(usage)
    cut = int(df.quantile(0.75))
    df.fillna(cut, inplace=True)
    return int(df.sum())

if __name__ == '__main__':
    usage = usage_list('cartridge.log')
    
    use = usetime(usage)
    
    print use / 60. / 60.
    if use < MAX_USE:
        print 'cartridge okay'
    else:
        print 'change cartridge'