class StoreRouter(object):
    """
      A router to control all database operations on models in
      the store application
      """

def db_for_read(self, model, **hints):
        if model._meta.app_label == 'store':
            return 'store'
        return None


def db_for_write(self, model, **hints):
    if model._meta.app_label == 'store':
        return 'store'
    return None


def allow_syncdb(self, db, model):
    if db == 'store':
        return model._meta.app_label == 'store'
    elif model._meta.app_label == 'store':
        return False
    return None
