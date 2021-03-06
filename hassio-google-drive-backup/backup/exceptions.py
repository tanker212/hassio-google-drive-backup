from abc import ABC, abstractmethod
from .const import ERROR_MULTIPLE_DELETES, ERROR_HA_DELETE_ERROR, ERROR_GOOGLE_SESSION, ERROR_GOOGLE_TIMEOUT, ERROR_GOOGLE_INTERNAL, ERROR_GOOGLE_CONNECT, ERROR_GOOGLE_DNS, ERROR_DRIVE_FULL, ERROR_BAD_PASSWORD_KEY, ERROR_INVALID_CONFIG, ERROR_LOGIC, ERROR_CREDS_EXPIRED, ERROR_NO_SNAPSHOT, ERROR_NOT_UPLOADABLE, ERROR_PLEASE_WAIT, ERROR_PROTOCOL, ERROR_SNAPSHOT_IN_PROGRESS, ERROR_UPLOAD_FAILED, ERROR_EXISTING_FOLDER, ERROR_MULTIPLE_FOLDERS, ERROR_BACKUP_FOLDER_MISSING


def ensureKey(key, target, name):
    if key not in target:
        raise ProtocolError(key, name, target)
    return target[key]


class KnownError(Exception, ABC):
    @abstractmethod
    def message(self) -> str:
        pass

    @abstractmethod
    def code(self) -> str:
        pass

    def httpStatus(self) -> int:
        return 500

    def data(self):
        return {}


class SimulatedError(KnownError):
    def __init__(self, code):
        self._code = code

    def code(self):
        return self._code

    def message(self):
        return "Gave code " + str(self._code)


class LogicError(KnownError):
    def __init__(self, message):
        self._message = message

    def message(self):
        return self._message

    def code(self):
        return ERROR_LOGIC


class ProtocolError(KnownError):
    def __init__(self, parameter, object_name=None, debug_object=None):
        self._parameter = parameter
        self._object_name = object_name
        self._debug_object = debug_object

    def message(self):
        if self._object_name:
            return "Required key '{0}' was missing from {1}".format(self._parameter, self._object_name)
        else:
            return self._parameter

    def code(self):
        return ERROR_PROTOCOL


class SnapshotInProgress(KnownError):
    def message(self):
        return "A snapshot is already in progress"

    def code(self):
        return ERROR_SNAPSHOT_IN_PROGRESS


class SnapshotPasswordKeyInvalid(KnownError):
    def message(self):
        return "Couldn't find your snapshot password in your secrets file.  Please check your settings."

    def code(self):
        return ERROR_BAD_PASSWORD_KEY


class UploadFailed(KnownError):
    def message(self):
        return "Snapshot upload failed.  Please check the supervisor logs for details."

    def code(self):
        return ERROR_UPLOAD_FAILED


class GoogleCredentialsExpired(KnownError):
    def message(self):
        return "Your Google Drive credentials have expired.  Please reauthorize with Google Drive through the Web UI."

    def code(self):
        return ERROR_CREDS_EXPIRED


class NoSnapshot(KnownError):
    def message(self):
        return "The snapshot doesn't exist anymore"

    def code(self):
        return ERROR_NO_SNAPSHOT


class NotUploadable(KnownError):
    def message(self):
        return "This snapshot can't be uploaded to Home Assistant yet"

    def code(self):
        return ERROR_NOT_UPLOADABLE


class PleaseWait(KnownError):
    def message(self):
        return "Please wait until the sync is finished."

    def code(self):
        return ERROR_PLEASE_WAIT


class InvalidConfigurationValue(KnownError):
    def __init__(self, key, current):
        self.key = key
        self.current = current

    def message(self):
        return "'{0}' isn't a valid value for {1}".format(str(self.current), str(self.key))

    def code(self):
        return ERROR_INVALID_CONFIG


# UI Handler Done and updated

class DeleteMutlipleSnapshotsError(KnownError):
    def __init__(self, delete_sources):
        self.delete_sources = delete_sources

    def message(self):
        return "The add-on has been configured to delete more than one older snapshots.  Please confirm this by visiting the add-on's web UI or by setting the config option 'confirm_multiple_deletes'=false in your add-on configuration."

    def code(self):
        return ERROR_MULTIPLE_DELETES

    def data(self):
        return self.delete_sources


class DriveQuotaExceeded(KnownError):
    def message(self):
        return "Google Drive is out of space"

    def code(self):
        return ERROR_DRIVE_FULL


class GoogleDnsFailure(KnownError):
    def message(self):
        return "Unable to resolve host www.googleapis.com"

    def code(self):
        return ERROR_GOOGLE_DNS


class GoogleCantConnect(KnownError):
    def message(self):
        return "Unable to connect to www.googleapis.com"

    def code(self):
        return ERROR_GOOGLE_CONNECT


class GoogleInternalError(KnownError):
    def message(self):
        return "Google Drive returned an internal error (HTTP: 5XX)"

    def code(self):
        return ERROR_GOOGLE_INTERNAL


class GoogleTimeoutError(KnownError):
    def message(self):
        return "Timed out while trying to reach Google Drive"

    def code(self):
        return ERROR_GOOGLE_TIMEOUT


class GoogleSessionError(KnownError):
    def message(self):
        return "Upload session with Google Drive expired.  The upload could not complete."

    def code(self):
        return ERROR_GOOGLE_SESSION


class HomeAssistantDeleteError(KnownError):
    def message(self):
        return "Home Assistant refused to delete the snapshot."

    def code(self):
        return ERROR_HA_DELETE_ERROR


class ExistingBackupFolderError(KnownError):
    def __init__(self, existing_id: str):
        self.existing_id = existing_id
    
    def message(self):
        return "A backup folder already exists.  Please visit the add-on Web UI to select where to backup."

    def code(self):
        return ERROR_EXISTING_FOLDER

    def data(self):
        return {"existing_id": self.existing_id}


class MultipleBackupFoldersError(KnownError):
    def __init__(self, count: int):
        self.count = count

    def message(self):
        return "Multiple backup folders were found.  Please visit the add-on Web UI to select where to backup."

    def code(self):
        return ERROR_MULTIPLE_FOLDERS

    def data(self):
        return {"count": self.count}


class BackupFolderMissingError(KnownError):
    def message(self):
        return "The backup folder is missing.  Please visit the add-on Web UI to select where to backup."

    def code(self):
        return ERROR_BACKUP_FOLDER_MISSING
