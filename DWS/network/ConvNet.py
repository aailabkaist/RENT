import torch
import torch.nn as nn
import torch.nn.functional as F


class LeNet(nn.Module):
    def __init__(self, args):
        super(LeNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5, stride=1, padding=2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(400, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, args.n_class)

    def forward(self, x, feature=False):
        out = F.relu(self.conv1(x))
        out = F.max_pool2d(out, 2)
        out = F.relu(self.conv2(out))
        out = F.max_pool2d(out, 2)
        out = out.view(out.size(0), -1)
        out = F.relu(self.fc1(out))
        feat = F.relu(self.fc2(out))
        out = self.fc3(feat)

        if feature:
            return feat, out
        else:
            return out

class LeNet_BLTM(LeNet):
    def __init__(self, args):
        super().__init__(args)
        self.fc3_bltm = nn.Linear(84, args.n_class*args.n_class)
        self.n_class = args.n_class

    def forward(self, x):
        out = F.relu(self.conv1(x))
        out = F.max_pool2d(out, 2)
        out = F.relu(self.conv2(out))
        out = F.max_pool2d(out, 2)
        out = out.view(out.size(0), -1)
        out = F.relu(self.fc1(out))
        out = F.relu(self.fc2(out))
        out = self.fc3_bltm(out)
        out = out.reshape(out.size(0), self.n_class, self.n_class)
        out = torch.transpose(F.softmax(out, dim=2), 2, 1)

        return out


# def call_bn(bn, x):
#     return bn(x)
#
# class CNN(nn.Module):
#     def __init__(self, args, dropout_rate=0.25, top_bn=False):
#         self.dropout_rate = dropout_rate
#         self.top_bn = top_bn
#         super(CNN, self).__init__()
#         self.c1=nn.Conv2d(args.n_channel,128,kernel_size=3,stride=1, padding=1)
#         self.c2=nn.Conv2d(128,128,kernel_size=3,stride=1, padding=1)
#         self.c3=nn.Conv2d(128,128,kernel_size=3,stride=1, padding=1)
#         self.c4=nn.Conv2d(128,256,kernel_size=3,stride=1, padding=1)
#         self.c5=nn.Conv2d(256,256,kernel_size=3,stride=1, padding=1)
#         self.c6=nn.Conv2d(256,256,kernel_size=3,stride=1, padding=1)
#         self.c7=nn.Conv2d(256,512,kernel_size=3,stride=1, padding=0)
#         self.c8=nn.Conv2d(512,256,kernel_size=3,stride=1, padding=0)
#         self.c9=nn.Conv2d(256,128,kernel_size=3,stride=1, padding=0)
#         self.l_c1=nn.Linear(128, args.n_class)
#         self.bn1=nn.BatchNorm2d(128)
#         self.bn2=nn.BatchNorm2d(128)
#         self.bn3=nn.BatchNorm2d(128)
#         self.bn4=nn.BatchNorm2d(256)
#         self.bn5=nn.BatchNorm2d(256)
#         self.bn6=nn.BatchNorm2d(256)
#         self.bn7=nn.BatchNorm2d(512)
#         self.bn8=nn.BatchNorm2d(256)
#         self.bn9=nn.BatchNorm2d(128)
#
#     def forward(self, x,):
#         h=x
#         h=self.c1(h)
#         h=F.leaky_relu(call_bn(self.bn1, h), negative_slope=0.01)
#         h=self.c2(h)
#         h=F.leaky_relu(call_bn(self.bn2, h), negative_slope=0.01)
#         h=self.c3(h)
#         h=F.leaky_relu(call_bn(self.bn3, h), negative_slope=0.01)
#         h=F.max_pool2d(h, kernel_size=2, stride=2)
#         h=F.dropout2d(h, p=self.dropout_rate)
#
#         h=self.c4(h)
#         h=F.leaky_relu(call_bn(self.bn4, h), negative_slope=0.01)
#         h=self.c5(h)
#         h=F.leaky_relu(call_bn(self.bn5, h), negative_slope=0.01)
#         h=self.c6(h)
#         h=F.leaky_relu(call_bn(self.bn6, h), negative_slope=0.01)
#         h=F.max_pool2d(h, kernel_size=2, stride=2)
#         h=F.dropout2d(h, p=self.dropout_rate)
#
#         h=self.c7(h)
#         h=F.leaky_relu(call_bn(self.bn7, h), negative_slope=0.01)
#         h=self.c8(h)
#         h=F.leaky_relu(call_bn(self.bn8, h), negative_slope=0.01)
#         h=self.c9(h)
#         h=F.leaky_relu(call_bn(self.bn9, h), negative_slope=0.01)
#         h=F.avg_pool2d(h, kernel_size=h.data.shape[2])
#
#         h = h.view(h.size(0), h.size(1))
#         logit=self.l_c1(h)
#         if self.top_bn:
#             logit=call_bn(self.bn_c1, logit)
#         return logit
