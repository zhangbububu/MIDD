import os
import time
import wandb
import argparse
import random

from torch.backends import cudnn
from utils.utils import *
from functools import partial
from solver import Solver
from torch.utils.tensorboard import SummaryWriter

def str2bool(v):
    return v.lower() in ('true')

def main(config):
    cudnn.benchmark = True
    print(config)
    if (not os.path.exists(config.model_save_path)):
        mkdir(config.model_save_path)

    solver = Solver(vars(config))

    if config.mode == 'train':
        solver.train()

        print('============================  TRING END  ================================')

        load_path = os.path.join('checkpoints',config.dataset, config.model_save_path+'checkpoint.pt')
        print("Loading :", load_path)
        solver.model.load_state_dict(torch.load(load_path))

        with torch.no_grad():
            pr, re, f1score = solver.test()

        wandb.log({'f1score':f1score,
                   'precision': pr,
                   'recall': re})



    elif config.mode == 'test':

        solver.model.load_state_dict(torch.load('20230930143432checkpoints/checkpoint.pt'), strict=True)

        with torch.no_grad():
            solver.test()

    return solver



if __name__ == '__main__':

    wandb.login()
    parser = argparse.ArgumentParser()
    parser.add_argument('--lr', type=float, default=0.00005)

    parser.add_argument('--num_epochs', type=int, default=20)
    parser.add_argument('--win_size', type=int, default=100)
    parser.add_argument('--batch_size', type=int, default=256)
    parser.add_argument('--pretrained_model', type=str, default=None)
    parser.add_argument('--tem', type=float, default=2)

    # parser.add_argument('--input_c', type=int, default=55)
    # parser.add_argument('--output_c', type=int, default=55)
    # parser.add_argument('--dataset', type=str, default='MSL')
    # parser.add_argument('--data_path', type=str, default='./dataset/MSL')

    # parser.add_argument('--input_c', type=int, default=25)
    # parser.add_argument('--output_c', type=int, default=25)
    # parser.add_argument('--dataset', type=str, default='PSM')
    # parser.add_argument('--data_path', type=str, default='./dataset/PSM')

    parser.add_argument('--input_c', type=int, default=51)
    parser.add_argument('--output_c', type=int, default=51)
    parser.add_argument('--dataset', type=str, default='SWAT')
    # parser.add_argument('--data_path', type=str, default='./dataset/swat')
    parser.add_argument('--data_path', type=str, default='./dataset/kdd/dataset/SWAT')

    # parser.add_argument('--input_c', type=int, default=38)
    # parser.add_argument('--output_c', typ/public_data/zba/MIformer/datasete=int, default=38)
    # parser.add_argument('--dataset', type=str, default='SMD')
    # parser.add_argument('--data_path', type=str, default='./dataset/mySMD')


    parser.add_argument('--mode', type=str, default='train', choices=['train', 'test'])
    parser.add_argument('--model_save_path', type=str, default='checkpoints')
    parser.add_argument('--anomaly_ratio', type=float, default=0.5)
    parser.add_argument('--wandb', type=bool, default=True)
    parser.add_argument('--l_rec', type=float, default=0.)
    parser.add_argument('--l_intra_s', type=float, default=1.)
    parser.add_argument('--l_intra_r', type=float, default=1.)
    parser.add_argument('--l_mi', type=float, default=1.)
    parser.add_argument('--l_cons', type=float, default=1.)

    config = parser.parse_args()
    config.model_save_path =time.strftime("%Y%m%d%H%M%S")  + config.model_save_path

    args = vars(config)

    # wandb.init(config=args)
    # wandb_config = wandb.config
    # args = wandb_config



    print('------------ Options -------------')
    for k, v in sorted(args.items()):
        print('%s: %s' % (str(k), str(v)))
    print('-------------- End ----------------')

    seed = np.random.randint(0,10000000)
    print("seed = ", seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True

    # main(args)
    main(config)

 
