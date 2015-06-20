from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pprint import pprint as pp


def recursiveCopyInto(gauth, fID_from, fID_to, maxdepth=float('infinity'), __currentDepth=0):

    if __currentDepth > maxdepth:
        return

    result = gauth.service.files().get(fileId=fID_from).execute()
    print '  ' * __currentDepth + 'Recursively copying "%s" (id: %s)' % (result['title'], result['id'])
    print '  ' * __currentDepth + 'into id: %s' % fID_to


    # Go through children with pagination
    while True:
        result = gauth.service.files().list(q='"%s" in parents and trashed = false' % fID_from).execute()
        # Alternative way to get children:
        #   (returns `drive#childReference` instead of `drive#file`)
        # result = gauth.service.children().list(folderId=fID_from).execute()
        for child in result['items']:
            if child['kind'] != 'drive#file':
                print 'Unknown object type (not file or folder): "%s"' % child['kind']
                pp(child)

            if child['mimeType'] == 'application/vnd.google-apps.folder':
                data_new_folder = {
                  'title': child['title'],
                  'parents': [{ 'id': fID_to }],
                  'mimeType': 'application/vnd.google-apps.folder',
                }

                exists_check = gauth.service.files().list(q='title = "%s" and "%s" in parents and trashed = false' % (child['title'].replace('"', '\\"'), fID_to)).execute()
                pp(exists_check)

                if exists_check['items'] == []:
                    print '  ' * (__currentDepth+1) + 'Trying to create folder "%s"' % child['title']
                    new_folder = gauth.service.files().insert(body=data_new_folder).execute()
                    print '  ' * (__currentDepth+1) + 'Created folder "%s" (id: %s) in "%s" (id: %s)' % (new_folder['title'], new_folder['id'], child['title'], child['id'])
                else:
                    new_folder = exists_check['items'][0]
                recursiveCopyInto(gauth, child['id'], new_folder['id'], maxdepth=maxdepth, __currentDepth=__currentDepth+1)

            else:
                copied_file = {
                  'parents': [{ 'id': fID_to }], # Place copy in "to" folder
                  'title': child['title'], # If `title` is not specified the new file will be named
                                           # "Copy of ..."
                }

                exists_check = gauth.service.files().list(q='title = "%s" and "%s" in parents and trashed = false' % (child['title'].replace('"', '\\"'), fID_to)).execute()

                if exists_check['items'] == []:
                    print '  ' * (__currentDepth+1) + 'Trying to copy "%s"' % child['title']
                    try:
                        new_file = gauth.service.files().copy(fileId=child['id'], body=copied_file).execute()
                        print '  ' * (__currentDepth+1) + 'Copied file "%s"' % new_file['title']
                    except googleapiclient.errors.HttpError as e:
                        print 'Failed: %s\n trying again' % e
                        new_file = gauth.service.files().copy(fileId=child['id'], body=copied_file).execute()
                else:
                    print 'file "%s" already exists in destination folder "%s"' % (child['title'], fID_to)


        # Get page
        page_token = result.get('nextPageToken')
        if not page_token:
            break

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Recursively copies the contents of a Google Drive folder to another Google Drive folder')
    parser.add_argument('to_folder_id', metavar='FROM_FOLDER_ID', help='an integer for the accumulator')
    parser.add_argument('from_folder_id', metavar='TO_FOLDER_ID', help='an integer for the accumulator')

    args = parser.parse_args()

    # Authenticate
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)
    gauth.Authorize()

    # Copy folder
    recursiveCopyInto(gauth, args.to_folder_id, args.from_folder_id) #, maxdepth=0)


# permission_list = gauth.service.permissions().list(fileId=file1['id']).execute()
# print 'Changing permission for file "%s" (id: %s)' % (file1['title'], file1['id'])

# new_permission = {
#   'role': 'owner',
#   'type': 'user',
#   'value': 'malthe@socialsquare.dk',
# }

# # print gauth.service.permissions().update(fileId=file1['id']).execute()

# # Try to change permission
# # * Ownership can only be transferred to another user in the same domain # as the current owner.  # (https://support.google.com/drive/answer/2494892?hl=en)
# # * You cannot change permission between personal and Google Apps account (https://productforums.google.com/d/msg/docs/5liCUAfvKUs/y9h7GYQT_z0J)
# #
# ### gauth.service.permissions().insert(fileId=file1['id'], body=new_permission).execute()

# copied_file = {
#   'parents': [{ 'id': '0B-WpRvMKai6WfkxCcXh2UUhVUktjT0dnUEZkdEtaY2E1UUo2dUctTnhIMmxUelVQN3FzZ3M' }], # "Copied from BIT BLUEPRINT" folder
#   # 'title': file1.metadata['title'] + ' copy',
# }

# new_file = gauth.service.files().copy(fileId=file1['id'], body=copied_file).execute()
# pp(new_file)

# # permission_list = gauth.service.permissions().list(fileId=file1['id']).execute()
# # pp(permissions['items'])
