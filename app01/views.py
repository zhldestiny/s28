from django.shortcuts import render, HttpResponse
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
	res = send_sms_single("15827384645", template_id, [code, ])
	# print(res)
	if res["result"] == 0:
		return HttpResponse("短信发送成功")
	else:
		return HttpResponse(res["errmsg"])