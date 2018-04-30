'''launchdiva4D is a python interface to call the execution of DIVA4D (Climatology)
'''

import os
import subprocess
from subprocess import check_output, Popen

LIST_PARAMS = ['data', 'years', 'months', 'qfs', 'vars', 'depths']

def launchdiva4D(**kwargs):
    # concatenate list

    for k in LIST_PARAMS:
        if k in kwargs:
            kwargs[k] = ','.join([str(_) for _ in kwargs[k]])

    args = ['./launchdiva4D']
    # args = ['echo']
    args.extend(['--{}={}'.format(k.replace('_','-'),v) for k,v in kwargs.items() ])

    wdir = '/home/abarth/Test/DIVATest/diva-4.7.1/JRA4/Climatology/'
    wdir = '/home/abarth/src/diva/JRA4/Climatology'
    wdir = '/home/ctroupin/Software/DIVA/diva-4.7.1/JRA4/Climatology'

# Revision: 7491
# Node Kind: directory
# Schedule: normal
# Last Changed Author: swat
# Last Changed Rev: 7321
# Last Changed Date: 2016-06-13 15:33:53 +0200 (Mon, 13 Jun 2016)

    #out = check_output(args)

    env = os.environ.copy()
    env["PATH"] = ".:" + env["PATH"]

    p = Popen(args, stdout=subprocess.PIPE, cwd=wdir,env=env)
    # p.wait()
    out = p.stdout.read()

    print(out)

#kwargs = {'data': ['ll'], 'vars': ['a','b']}
#launchdiva4D(**kwargs)


def test_launchdiva4D():
    launchdiva4D(
        data=['./blacksea_data_CTD.txt'],
        years=['19002009'],
        months=['0101','0202'],
        qfs=[0,1],
        vars=['Temperature'],
        depths=[30,0],
        signal_to_noise_ratio=0.5,
        correlation_length=1.5,
        xori=27,yori=40,dx=0.1,dy=0.1,nx=151,ny=76,
        institution='University of Liege, GeoHydrodynamics and Environment Research',
        group='Diva group. E-mails : a.barth@ulg.ac.be ; swatelet@ulg.ac.be ; ctroupin@ulg.ac.be',
        comment='No comment',
        email='swatelet@ulg.ac.be',
        acknowledgements='No acknowledgement',
        datasource=' data_from various sources for diva software testing work',
        title='Diva 3D analysis ',
        bathymetry='/home/abarth/workspace/DIVA4DWeb/diva_bath.nc',
        outdir = '/tmp'
    )

if __name__ == "__main__":
    test_launchdiva4D()
