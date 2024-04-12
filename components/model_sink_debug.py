class ModelSinkNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
            },
        }

    RETURN_TYPES = tuple()
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "test"

    OUTPUT_NODE = True

    CATEGORY = "Example"

    def test(self, *args, **kwargs):
        print('args')
        for arg in args:
            print(type(arg))
        print('kwargs')
        for key, value in kwargs.items():
            print(key, type(value))
        return (0, )


class PipeSinkNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipe": ("pipe",),
            },
        }

    RETURN_TYPES = tuple()
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "test"

    OUTPUT_NODE = True

    CATEGORY = "Example"

    def test(self, *args, **kwargs):
        print('args')
        for arg in args:
            print(type(arg))
        print('kwargs')
        for key, value in kwargs.items():
            print(key, type(value))
        return (0, )
