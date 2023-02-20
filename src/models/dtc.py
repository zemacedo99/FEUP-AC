from models.common import train_model


def create(data):
    """Creates the model and trains it

    :param data: data to feed the model
    """
    model = train_model(data, 'dtc')
    return model


