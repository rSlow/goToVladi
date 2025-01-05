from goToVladi.flaskadmin.views.mixins.secure import SecureModelView


class AppModelView(SecureModelView):
    page_size = 10
