#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import pickle
from pathlib import Path
import glob
import os
import sys
from storages import log_store
from storages.log_store import LogStore
from log_model import logModel
from log_model.logModel import LogModel

if __name__ == '__main__':

    #コマンドライン引数
    parser = argparse.ArgumentParser(description='Train a model')
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help='GPU ID (negative value indicates CPU)')
    parser.add_argument('--n_units', '-n', type=int, default=2000,
                        help='Number of n_units')
    parser.add_argument('--iter', '-i', type=int, default=10,
                    help='Number of epochs')
    parser.add_argument('--cont', '-c', default=False,
                help='Continue to learn')
    parser.add_argument('logfile', metavar='F', help='Normal log file')

    args = parser.parse_args()


    if not Path('output').exists():
        os.mkdir('output')
    else:
        if not Path('output').is_dir():
            sys.exit('output is not a directory.')


    logname = Path(args.logfile).stem
    logstore = (Path('output') / logname).with_suffix('.pickle')

    print("loading log file...")
    if args.cont and logstre.exists():
        with logstore.open(mode='rb') as logstorefile:
            log_store = pickle.load(logstorefile)
    else:
        log_store = LogStore(args.logfile)

    with logstore.open(mode='wb') as f:
        pickle.dump(log_store, f)
    #print("start learning...")
    #
    # if args.cont:
    #     for epoch in range(args.iter, 0, -1):
    #         log_model_name = logname + "-model-{}-{}-{}".format(args.chunk, args.n_units, epoch)
    #         model_path = (Path('output') / log_model_name).with_suffix('.pickle')
    #         if path.exists():
    #             break
    #
    #     if model_path.exists(log_model_name):
    #         with open(model_path, 'rb') as modelfile:
    #             log_model = pickle.load(modelfile)
    #     else:
    #         log_model = LogModel(log_store, args.chunk, args.n_units, gpu=args.gpu, directory=Path('output'))
    # else:
    #     log_model = LogModel(log_store, args.chunk, args.n_units, gpu=args.gpu, directory=Path('output'))
    #
    # if log_model.current_epoch == args.iter:
    #     pass
    # else:
    #     log_model.train(args.iter)
