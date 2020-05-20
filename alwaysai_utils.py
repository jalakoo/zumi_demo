import edgeiq


def engine():
    """Switch Engine modes if an Intel accelerator is available"""
    if is_accelerator_available() == True:
        return edgeiq.Engine.DNN_OPENVINO
    return edgeiq.Engine.DNN


def is_accelerator_available():
    """Detect if an Intel Neural Compute Stick accelerator is attached"""
    if edgeiq.find_ncs1():
        return True
    if edgeiq.find_ncs2():
        return True
    return False


def object_detector(model, should_log=True):
    """Return an object detector for a given model"""
    if model is None:
        raise Exception(
            "alwaysai.py: object_detector: model name parameter not found")
    od = edgeiq.ObjectDetection(model)
    e = engine()
    od.load(e)
    if should_log == True:
        print("alwaysai.py: object_detector: Engine: {}".format(od.engine))
        print("alwaysai.py: object_detector: Accelerator: {}\n".format(
            od.accelerator))
        print("alwaysai.py: object_detector: Model:\n{}\n".format(od.model_id))
    return od
