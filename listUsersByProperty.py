import csv
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service


def get_user_data_list(service):
    """Get all user emails address and permission for all Google Analytics account and Properties.

    Args:
        service: The service that is connected to the specified API.

    Returns:
        A list of lists [[account], [WebProperty], [EmailAddress], [UserPermissions]] .
    """

    list_account = ['Account']
    list_property = ['WebProperty']
    list_email = ['EmailAddress']
    list_permissions = ['UserPermissions']

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    # Check if there is any account with access for the selected user
    if accounts.get('items'):
        # Search all accounts the user_account has access to
        for account in accounts.get('items'):
            # Get account name
            account_name = account.get('name')
            # Get a list of all the properties for the first account.
            account_id = account.get('id')
            properties = service.management().webproperties().list(
                accountId=account_id).execute()

            # Check if there are any Web Properties with access for the selected Account
            if properties.get('items'):
                # Search all Web Properties the user_account has access to
                for property in properties.get('items'):
                    # Get Web Property name and id
                    property_name = property.get('name')
                    property_id = property.get('id')
                    property_links = service.management().webpropertyUserLinks().list(
                        accountId=account_id,
                        webPropertyId=property_id).execute()

                    # Retrieve all user with access level for the selected Web Property
                    for property_user in property_links.get('items'):
                        # Get the email address and the access permissions for each user
                        email_adress = property_user.get('userRef').get('email')
                        permissions_list = property_user.get('permissions').get('effective')

                        # Append account name, property name, email address and permission list to python lists
                        list_account.append(account_name)
                        list_property.append(property_name)
                        list_email.append(email_adress)
                        list_permissions.append(permissions_list)

    # Final python list which includes all retrieved user data from Google Analytics
    final_user_data_list = [list_account, list_property, list_email, list_permissions]

    return final_user_data_list


def print_table_to_csv(data_list, filename):
    """Print input list of lists in a csv format in the same folder as this scripts.

    Args:
        data_list: A list of lists populated with data.

    Returns:
        None
    """
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        for iter in range(len(data_list[0])):
            writer.writerow([x[iter] for x in data_list])


def main():
    # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/analytics.manage.users', 'https://www.googleapis.com/auth/analytics.readonly']
    key_file_location = 'P:\\service_acccount_keys\\my_project-c1c9c02d2c87.json'

    output_csv_filename = "GoogleAnalyticsUserDataList.csv"

    # Authenticate and construct service.
    service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=scope,
            key_file_location=key_file_location)

    final_user_data_list = get_user_data_list(service)
    print_table_to_csv(final_user_data_list, output_csv_filename)


if __name__ == '__main__':
    main()