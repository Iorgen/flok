

class ValidatorWrappers:

    @staticmethod
    def responseValidator(func, MAX_TRIES_REQUEST=5):
        def wrapper(*args, **kwargs):
            for x in range(MAX_TRIES_REQUEST):
                try:
                    resp = func(*args, **kwargs)
                except Exception as e:
                    # TODO Define with logger
                    print('Something goes wrong')
                    # getLogger().error("{}".format(e))
                    continue
            return resp
        return wrapper