import inspect
import random
import string

from django_apps.utils.views.constants import SWAGGER_METHODS_TO_FIND


# TODO: remove this method to generate unique
#  name to serializers of other way.
def random_name(amount: int = 1):
    return "".join(random.choice(string.ascii_letters) for x in range(amount))


class GenerateSwagger(object):
    """
    Class decorator to generate dynamically
    swagger documentation to class's serializer
    """

    def __init__(self, f):
        self.f = f

    def __call__(self, cls):
        all_serializers = dict(
            inputget=dict(),
            outputget=dict(),
            inputpost=dict(),
            outputpost=dict(),
            inputpatch=dict(),
            outputpatch=dict(),
            inputput=dict(),
            outputput=dict(),
        )

        for name, m in inspect.getmembers(cls, inspect.isclass):
            serializer_class = getattr(cls, name)
            for serializer_key in all_serializers.keys():
                is_serializer = False
                lower_name = name.lower()
                if lower_name.startswith(serializer_key) and lower_name.startswith(
                    "output"
                ):
                    all_serializers[serializer_key].update(responses={200: m})
                    is_serializer = True

                if lower_name.startswith(serializer_key) and lower_name.startswith(
                    "input"
                ):
                    all_serializers[serializer_key].update(request_body=m)
                    is_serializer = True

                if is_serializer:
                    setattr(cls, "serializer_class", m)

                    class Meta:
                        ref_name = f"{name}{cls.__name__}{random_name(4)}"

                    setattr(serializer_class, "Meta", Meta)

        for method in SWAGGER_METHODS_TO_FIND:
            method_serializers = dict(
                **all_serializers[f"output{method}"],
            )
            if method != "get":
                method_serializers.update(
                    **all_serializers[f"input{method}"],
                )
            if method == "post" and "responses" in method_serializers:
                # change default status
                method_serializers.update(
                    responses={201: method_serializers["responses"][200]}
                )
            if hasattr(cls, method):
                try:
                    setattr(
                        cls,
                        method,
                        self.f(**method_serializers)(getattr(cls, method)),
                    )
                except AssertionError:
                    pass
        return cls
