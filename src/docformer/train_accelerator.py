## Dependencies

from accelerate import Accelerator
import accelerate
import pytesseract
import torchmetrics
import math
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from PIL import Image
import json
import numpy as np
from tqdm.auto import tqdm
from torchvision.transforms import ToTensor
import torch.nn.functional as F
import torch.nn as nn
import torchvision.models as models
from einops import rearrange
from einops import rearrange as rearr
from sklearn.model_selection import train_test_split as tts
from torch.autograd import Variable
from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import ToTensor
from modeling import DocFormer

batch_size = 9

class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n

    @property
    def avg(self):
        return (self.sum / self.count) if self.count>0 else 0

## Loggers
class Logger:
    def __init__(self, filename, format='csv'):
        self.filename = filename + '.' + format
        self._log = []
        self.format = format

    def save(self, log, epoch=None):
        log['epoch'] = epoch + 1
        self._log.append(log)
        if self.format == 'json':
            with open(self.filename, 'w') as f:
                json.dump(self._log, f)
        else:
            pd.DataFrame(self._log).to_csv(self.filename, index=False)



def train_fn(data_loader, model, criterion, optimizer, epoch, device, scheduler=None):
    model.train()
    accelerator = Accelerator()
    model, optimizer, data_loader = accelerator.prepare(model, optimizer, data_loader)
    loop = tqdm(data_loader, leave=True)
    log = None
    train_acc = torchmetrics.Accuracy()
    loop = tqdm(data_loader)

    for batch in loop:

        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["mlm_labels"].to(device)

        # process
        outputs = model(batch)
        ce_loss = criterion(outputs.transpose(1,2), labels)

        if log is None:
            log = {}
            log["ce_loss"] = AverageMeter()
            log['accuracy'] = AverageMeter()

        optimizer.zero_grad()
        accelerator.backward(ce_loss)
        optimizer.step()

        if scheduler is not None:
            scheduler.step()

        log['accuracy'].update(train_acc(labels.cpu(),torch.argmax(outputs,-1).cpu()).item(),batch_size)
        log['ce_loss'].update(ce_loss.item())
        loop.set_postfix({k: v.avg for k, v in log.items()})

    return log


# Function for the validation data loader
def eval_fn(data_loader, model, criterion, device):
    model.eval()
    log = None
    val_acc = torchmetrics.Accuracy()       


    with torch.no_grad():
        loop = tqdm(data_loader, total=len(data_loader), leave=True)
        for batch in loop:

            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["mlm_labels"].to(device)
            output = model(batch)
            ce_loss = criterion(output.transpose(1,2), labels)

            if log is None:
                log = {}
                log["ce_loss"] = AverageMeter()
                log['accuracy'] = AverageMeter()

            log['accuracy'].update(val_acc(labels.cpu(),torch.argmax(output,-1).cpu()).item(),batch_size)
            log['ce_loss'].update(ce_loss.item())
            loop.set_postfix({k: v.avg for k, v in log.items()})
    return log  # ['total_loss']

date = '20Oct'


def run(config,train_dataloader,val_dataloader,device,epochs,path,classes,lr = 5e-5):
    logger = Logger(f"{path}/logs")
    model = DocFormerForClassification(config,classes).to(device)
    criterion = nn.CrossEntropyLoss()
    criterion = criterion.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    best_val_loss = 1e9
    header_printed = False
    batch_size = config['batch_size']
    for epoch in range(epochs):
        print("Training the model.....")
        train_log = train_fn(
            train_dataloader, model, criterion, optimizer, epoch, device, scheduler=None
        )

        print("Validating the model.....")
        valid_log = eval_fn(val_dataloader, model, criterion, device)
        log = {k: v.avg for k, v in train_log.items()}
        log.update({"V/" + k: v.avg for k, v in valid_log.items()})
        logger.save(log, epoch)
        keys = sorted(log.keys())
        if not header_printed:
            print(" ".join(map(lambda k: f"{k[:8]:8}", keys)))
            header_printed = True
        print(" ".join(map(lambda k: f"{log[k]:8.3f}"[:8], keys)))
        if log["V/ce_loss"] < best_val_loss:
            best_val_loss = log["V/ce_loss"]
            print("Best model found at epoch {}".format(epoch + 1))
            torch.save(model.state_dict(), f"{path}/docformer_best_{epoch}_{date}.pth")
