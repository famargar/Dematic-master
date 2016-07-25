import time
import argparse
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

from gen_data_simple import makedata

#global settings
plt.interactive(False)


def check_data(period, DIR):
    """
        This function fills dataframes with the data incoming from the monitor (or the synthetic data generator, in this
        prototype) with frequency 1Hz (variable). It fills three tables - "data", "cal_x", "cal_y" - in a SQLite
        database with that data (MultiShuttle.db). It calls perf_checks that produce monitoring plots at 0.2Hz and
        checks that there is no trend or outliers in "data" data, and that data does not exceed boundaries in
        type "cal_x", "caly" data.
        Args
            period: how long acquiring data
            DIR:    directory where to store generated plot
        Returns:
            df, dfx , dfy are three pandas dataframe with the three fictitious quantities monitored
    """

    disk_engine = create_engine('sqlite:///MultiShuttle.db')

    start = time.time()

    df = pd.DataFrame(columns=('key', 'data'))
    dfx = pd.DataFrame(columns=('key', 'xaxis', 'up', 'down'))
    dfy = pd.DataFrame(columns=('key', 'yaxis', 'up', 'down'))
    dfDB = pd.DataFrame(columns=('key', 'data'))
    dfxDB = pd.DataFrame(columns=('key', 'xaxis', 'up', 'down'))
    dfyDB = pd.DataFrame(columns=('key', 'yaxis', 'up', 'down'))

    i, random_number, index = 0, 0, 0

    # devo fare un dataframe di una riga da aggiungere al database
    # poi mi serve un secondo dataframe con tutte le linee per generare i plots

    while time.time() - start < period:
        n1, n2, n3, t = makedata()

        df.loc[i] = [t, n1];          dfDB.loc[0] = [t, n1];
        dfx.loc[i] = [t, n2, -50, 50];   dfxDB.loc[0] = [t, n2, -50, 50]
        dfy.loc[i] = [t, n3, -50, 50];   dfyDB.loc[0] = [t, n3, -50, 50]

        # save to SQLite database
        dfDB.to_sql('data', disk_engine, if_exists='append', index=False)
        dfxDB.to_sql('cal_x', disk_engine, if_exists='append', index=False)
        dfyDB.to_sql('cal_y', disk_engine, if_exists='append', index=False)

        time.sleep(0.5)
        i += 1

        if i % 5 == 0:
            perf_checks(df, dfx, dfy, DIR)

    return df, dfx, dfy


def perf_checks(dfc, dfxc, dfyc, DIR):
    """
        This function produces monitoring plots at 0.2Hz and checks that there is
        no trend or outliers in type I data, and that data does not exceed boundaries in type II data.
        Args:
            dfc, dfxc, dfyc: datframes with the data from the three quantities to be monitored
            DIR: directory where to store the plots
        Return:
            none
    """

    calx = pd.DataFrame(columns=('key', 'xaxis', 'up', 'down', 'roll'))
    caly = pd.DataFrame(columns=('key', 'yaxis', 'up', 'down', 'roll'))

    calx['key'] = dfxc['key']
    calx['xaxis'] = dfxc['xaxis']
    calx['xaxis'] = calx['xaxis'].cumsum()
    calx['up'] = 50
    calx['down'] = -50
    calx['roll'] = pd.rolling_mean(calx['xaxis'], 60)

    caly['key'] = dfyc['key']
    caly['yaxis'] = dfyc['yaxis']
    caly['yaxis'] = caly['yaxis'].cumsum()
    caly['up'] = 50
    caly['down'] = -50
    caly['roll'] = pd.rolling_mean(caly['yaxis'], 60)

    # quantity exceeding five sigma from expectation
    t1 = abs(10-dfc.data.any()) > 5
    # quantities exceeding the (arbitrary) threshold
    t2 = abs(calx.xaxis.any()) > 50 or abs(caly.yaxis.any()) > 50

    # in the title we append the control check value
    typ1, typ2 = send_notif(t1, t2)

    myDpi = 96

    # creating figures, saving them to disk
    plt.figure()
    dfc.plot(ylim=[0, 20], title="MultiShuttle Z Monitor : %s" % typ1)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Z quantity (Z units)')
    leg = plt.legend()
    leg.get_texts()[0].set_text('Data')
    plt.savefig('%s/df.png' % DIR, dpi=myDpi, bbox_inches='tight')
    calx.plot(ylim=[-70, 70], title="MultiShuttle x axis position:  %s" % typ2)
    plt.xlabel('Time (seconds)')
    plt.ylabel('X quantity (X units)')
    leg = plt.legend()
    leg.get_texts()[0].set_text('X quantity')
    leg.get_texts()[1].set_text('Max value')
    leg.get_texts()[2].set_text('Min value')
    leg.get_texts()[3].set_text('Rolling mean')
    plt.savefig('%s/calx.png' % DIR, dpi=myDpi, bbox_inches='tight')
    caly.plot(ylim=[-70, 70], title="MultiShuttle y axis position:  %s" % typ2)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Y quantity (Y units)')
    leg = plt.legend()
    leg.get_texts()[0].set_text('Y quantity')
    leg.get_texts()[1].set_text('Max value')
    leg.get_texts()[2].set_text('Min value')
    leg.get_texts()[3].set_text('Rolling mean')
    plt.savefig('%s/caly.png' % DIR, dpi=myDpi, bbox_inches='tight')

    plt.close('all')

    del calx, caly,dfc

def send_notif(t1, t2):
    """
        This function receives the warning flags from perf_checks, and sends textual warnings to the web server
        Args:
            t1, t2: are the two types of flags that can arise due to bad data
        Returns:
            type1: the string containing the message in case of outliers
            type2: the string containing the error message in case of data exceeding safety thresholds
    """

    type1 = ""
    type2 = ""

    if t1: type1 = "Outliers!"
    else: type1 = "OK"
    if t2: type2 = "Miscalibration!"
    else: type2 = "OK",

    return type1, type2


if __name__ == '__main__':
    # The main function tells what to do in case of running in standalone mode

    parser = argparse.ArgumentParser(description='check_data DB')
    parser.add_argument('-d', '--dir', help='dir where to create pdf files', required=True)
    args = vars(parser.parse_args())
    DOC_ROOT = args['dir']

    check_data(1000, DOC_ROOT)


