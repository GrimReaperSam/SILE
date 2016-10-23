
def get_prefix(image_id):
    if image_id > 9:
        return str(image_id)[-2:]
    else:
        return "0%s" % str(image_id)[-1]
