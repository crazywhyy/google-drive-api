from __future__ import print_function
import pickle
import os
import io
import magic
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import tkinter.messagebox


# If modifying these scopes, delete the file token.pickle.


def getToken():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service


def listfile():
    a = getToken()
    results = a.files().list(
        pageSize=40, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        return items

def getID(indexItem):
    items = listfile()
    IDitem = items[int(indexItem)].get('id')
    return IDitem


def Downloadfile(index, filename):
    try:
        file_id = getID(index)
        request = getToken().files().get_media(fileId=file_id)
        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            tkinter.messagebox.showinfo("Notification!!","Download %d%%." % int(status.progress() * 100))
    except:
        tkinter.messagebox.showwarning('Download failed!!')


def Uploadfile(filename):
    try:
        getToken()
        Namee = filename.split("/")
        file_metadata = {'name': Namee[(len(Namee) - 1)]}
        m1 = magic.Magic(mime=True)
        mime = str(m1.from_file(filename))

        mediaUP = MediaFileUpload(filename, mimetype=mime, resumable=True)
        fileUP = getToken().files().create(body=file_metadata, media_body=mediaUP, fields='id').execute()
        tkinter.messagebox.showinfo('Notification', 'Upload success: ' + Namee[(len(Namee) - 1)])
        print('File ID: %s' % fileUP.get('id'))
    except(AttributeError):
        print("Upload failed!")
