from allauth.account.adapter import DefaultAccountAdapter
class accountAdapter(DefaultAccountAdapter):

  def get_login_redirect_url(self, request):
      return '/'