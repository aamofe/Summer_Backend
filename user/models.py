from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class User(models.Model):
    username=models.CharField(verbose_name="真实姓名",max_length=20)
    nickname=models.CharField(verbose_name="昵称",max_length=20)#默认
    email=models.EmailField(verbose_name="邮箱")
    #密码要求是 数字+字母 8-16位
    password=models.CharField(verbose_name="账户密码",max_length=16)
    avatar_url = models.URLField(verbose_name="头像路径",default="https://summer-1315620690.cos.ap-beijing.myqcloud.com/user_avatar/default.png")
    created_at=models.DateTimeField(verbose_name='注册时间',auto_now_add=True)
    is_active=models.BooleanField(verbose_name='是否有效账户',max_length=20,default=False)
    current_team_id=models.IntegerField(verbose_name="当前团队id")
    is_new=models.BooleanField(verbose_name='是否为新用户',default=True)
    def to_dict(self):
        return {
            'id':self.id,
            'username':self.username,
            'nickname':self.nickname,
            'avatar_url':self.avatar_url,
            'email':self.email,

        }

