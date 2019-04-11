import json, os, pandas as pd
from ftplib import FTP

# Get any CSV file from the state leg FTP server
def get_csv(path, filename, outfile=None,outdir="output"):
    if (outfile==None):
        outfile=filename
    host = "ftp.cga.ct.gov"
    ftp = FTP(host)
    ftp.connect()
    ftp.login()
    # print ftp.getwelcome()
    ftp.cwd(path)
    
    def make_dir(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    make_dir(outdir)
    
    outfh = open(os.path.join(outdir,outfile) ,"wb")

    def write_block(b):
        outfh.write(b)
    
    csv = ftp.retrbinary("RETR " + filename,
                         write_block)

    outfh.close()
    ftp.quit()

    return pd.read_csv("output/LegislatorDatabase.csv")

    
def get_legislators():
    path = "/pub/data/"
    filename = "LegislatorDatabase.csv"
    return get_csv(path, filename, filename)

def get_committees():
    return get_csv("pub/data/","committee.csv")

def get_subjects():
    return get_csv("pub/data/","subject.csv")

def get_billhistory():
    return get_csv("pub/data/","bill_history.csv")

print get_legislators().head()
print get_committees().head()
print get_subjects().head()
print get_billhistory().head()
