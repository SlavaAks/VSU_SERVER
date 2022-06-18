from datetime import datetime, timedelta

from storages.backends.dropbox import *

print(setting('DROPBOX_OAUTH2_TOKEN'))
@deconstructible
class DropBoxStorageCustom(DropBoxStorage):
    """DropBox Storage class for Django pluggable storage system."""

    # location = setting('DROPBOX_ROOT_PATH', '/')
    app_key = setting('DROPBOX_APP_KEY')
    app_secret = setting("DROPBOX_APP_SECRET")
    oauth2_access_token_expiration = setting("DROPBOX_API_EXPIRATION")
    oauth2_access_token = setting('DROPBOX_OAUTH2_TOKEN')
    oauth2_refresh_token = setting('DROPBOX_OAUTH2_REFRESH_TOKEN')
    # timeout = setting('DROPBOX_TIMEOUT', _DEFAULT_TIMEOUT)
    # write_mode = setting('DROPBOX_WRITE_MODE', _DEFAULT_MODE)

    CHUNK_SIZE = 4 * 1024 * 1024

    def __init__(self, oauth2_access_token=oauth2_access_token,
                 oauth2_access_token_expiration=oauth2_access_token_expiration,
                 oauth2_refresh_token=oauth2_refresh_token,
                 app_key=app_key,
                 app_secret=app_secret):
        # if oauth2_access_token is None:
        #     raise ImproperlyConfigured("You must configure an auth token at"
        #                                "'settings.DROPBOX_OAUTH2_TOKEN'.")

        self.root_path = '/'
        self.write_mode = 'add'
        self.client = Dropbox(oauth2_access_token=oauth2_access_token,
                              oauth2_access_token_expiration=oauth2_access_token_expiration,
                              oauth2_refresh_token=oauth2_refresh_token,
                              app_key=app_key,
                              app_secret=app_secret)
