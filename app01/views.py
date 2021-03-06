from django.shortcuts import render, HttpResponse
from django_redis import get_redis_connection
import random
from utils.tencent.sms import send_sms_single
from django.conf import settings

# Create your views here.
def send_sms(request):
	"""send sms
		?tpl=login -> 642365
		?tpl=register -> 642323
	"""
	tpl = request.GET.get('tpl')
	template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
	if not template_id:
		return HttpResponse("no template available")
	code = random.randrange(1000, 9999)
	# res = send_sms_single("15827384645", template_id, [code, ])
	res = send_sms_single(phone, template_id, [code, ])
	# print(res)
	if res["result"] == 0:
		# redis 设置
		conn = get_redis_connection("default")
		conn.set(phone, code, ex=60)
		return HttpResponse("短信发送成功")
	else:
		return HttpResponse(res["errmsg"])


from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class RegisterModelFrom(forms.ModelForm):
	phone = forms.CharField(label="phone", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])    # validators正则
	password = forms.CharField(label="password", widget=forms.PasswordInput())    # 隐藏显示密码      attrs={"class": "form-control", "placeholder": "confirm password"}
	confirm_password = forms.CharField(label="confirm_password", widget=forms.PasswordInput())    # attrs={"class": "form-control", "placeholder": "confirm password"}
	code = forms.CharField(label="验证码", widget=forms.TextInput())    # attrs={"class": "form-control", "placeholder": "请输入验证码"}
	class Meta:
		model = models.Login_info
		# fields = "__all__"    # 默认顺序展示
		fields = ["username", "email", "phone", "code", "password", "confirm_password"]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for name, field in self.fields.items():
			field.widget.attrs["class"] = "form-control"
			field.widget.attrs["placeholder"] = "plz input " + name    # '请输入%s' % (field.label,)


def register(request):
	form = RegisterModelFrom()
	return render(request, "app01/register.html", {"form": form})