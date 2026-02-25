from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from src.auth_backends import _is_locked


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Tên đăng nhập hoặc mật khẩu không đúng.",
        "inactive": "Tài khoản này đã bị vô hiệu hóa.",
        "locked": "Tài khoản tạm thời bị khóa do đăng nhập sai quá nhiều lần. Vui lòng thử lại sau vài phút hoặc liên hệ quản trị viên nếu bạn cần hỗ trợ.",  # noqa: E501
    }

    def clean(self):
        username = self.cleaned_data.get("username")
        if username and _is_locked(username):
            raise ValidationError(
                self.error_messages["locked"],
                code="locked",
            )
        return super().clean()
