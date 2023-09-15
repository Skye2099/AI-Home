from torch import nn

class Trainer:
    def __init__(self, model, val_dataloader, n_epoch=100, optimizer=torch.optim.Adam, lr=1e-3, loss_fn=nn.MSELoss()):
        self.model = model
        self.val_dataloader = val_dataloader
        self.n_epoch = n_epoch
        self.loss_fn = loss_fn
        self.optimizer = optimizer(model.parameters(), lr=lr)
        self.scheduler = ReduceLROnPlateau(self.optimizer, mode='min', factor=0.1, patience=1000,verbose = True)


    def train_loop(self, train_dataloader, metric=0, verbose=True):
        self.model.train()

        total_loss = 0.

        for i,(X,y) in enumerate(train_dataloader):
            if torch.cuda.is_available():
                X = X.cuda()
                y = y.cuda()
            y_pred = self.model(X)
            self.optimizer.zero_grad()
            loss = self.loss_fn(y_pred, y)

            loss.backward() # loss 是个grad的tensor,获取数值需要loss.item()
            self.optimizer.step()

            total_loss += loss.item()
            self.scheduler.step(loss) # 每个epoch/batch 更新一次lr
        
        epoch_loss = total_loss/(i+1)

        return epoch_loss


    def val_loop(self, val_dataloader):
        self.model.eval()

        epoch_loss = 0.
        with torch.no_grad():
            for i,(X,y) in enumerate(val_dataloader):
                if torch.cuda.is_available():
                    X = X.cuda()
                    y = y.cuda()

                pred = self.model(X)
                loss = self.loss_fn(pred, y)
                epoch_loss += loss.item()

            return epoch_loss/(i+1)

    # test_dataloader should be wiht no y label             
    def test_loop(self, test_dataloader):
        self.model.eval()

        y_pred = []
        for i,batch_data in enumerate(test_dataloader):
            # TODO
            X = batch_data # or batch_data[0]

        
    def fit(self, train_dataloader, verbose=True):
        for epoch in range(self.n_epoch):
            train_loss = self.train_loop(train_dataloader)
            val_loss = self.val_loop(self.val_dataloader)
            print(f'epoch_{epoch} train_loss: {train_loss},val_loss:{val_loss}')     
            
            if verbose:
                current_lr = self.optimizer.param_groups[0]['lr']
                print(f'Epoch {epoch}: Learning Rate = {current_lr}')
        
