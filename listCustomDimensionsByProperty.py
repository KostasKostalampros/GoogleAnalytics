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


def get_custom_dimensions_list(service):
    """Get all custom dimensions set in every Web Property the user has access to.

    Args:
        service: The service that is connected to the specified API.

    Returns:
        A list of lists [[accountId], [account], [webPropertyId], [internalWebPropertyId], [webProperty],
         [customDimensionName], [customDimensionIndex] ,[customDimensionScope], [customDimensionActive],
         [customDimensionCreated], [customDimensionUpdated]] .
    """

    list_accountId = ['accountId']
    list_account = ['account']
    list_webPropertyId = ['webPropertyId']
    list_internalWebPropertyId = ['internalWebPropertyId']
    list_webProperty = ['webProperty']
    list_customDimensionName = ['customDimensionName']
    list_customDimensionIndex = ['customDimensionIndex']
    list_customDimensionScope = ['customDimensionScope']
    list_customDimensionActive = ['customDimensionActive']
    list_customDimensionCreated = ['customDimensionCreated']
    list_customDimensionUpdated = ['customDimensionUpdated']

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    # Check if there is any account with access for the selected user
    if accounts.get('items'):
        # Search all accounts the user_account has access to
        for account in accounts.get('items'):
            # Get account name
            accountName = account.get('name')
            # Get a list of all the properties for the first account.
            accountId = account.get('id')
            properties = service.management().webproperties().list(
                accountId=accountId).execute()

            # Check if there are any Web Properties with access for the selected Account
            if properties.get('items'):
                # Search all Web Properties the user_account has access to
                for property in properties.get('items'):
                    # Get Web Property name and id
                    propertyName = property.get('name')
                    propertyId = property.get('id')
                    internalWebPropertyId = property.get('internalWebPropertyId')
                    custom_dimensions = service.management().customDimensions().list(
                        accountId=accountId,
                        webPropertyId=propertyId).execute()

                    # Retrieve all custom dimensions for the selected Web Property
                    for custom_dimension in custom_dimensions.get('items'):
                        # Get custom dimension data, first store them in a temporary variable and then
                        # append it in a list

                        customDimensionName = custom_dimension.get('name')
                        customDimensionIndex = custom_dimension.get('index')
                        customDimensionScope = custom_dimension.get('scope')
                        customDimensionActive = custom_dimension.get('active')
                        customDimensionCreated = custom_dimension.get('created')
                        customDimensionUpdated = custom_dimension.get('updated')

                        # Append collected data into python lists
                        list_accountId.append(accountId)
                        list_account.append(accountName)
                        list_webPropertyId.append(propertyId)
                        list_internalWebPropertyId.append(internalWebPropertyId)
                        list_webProperty.append(propertyName)
                        list_customDimensionName.append(customDimensionName)
                        list_customDimensionIndex.append(customDimensionIndex)
                        list_customDimensionScope.append(customDimensionScope)
                        list_customDimensionActive.append(customDimensionActive)
                        list_customDimensionCreated.append(customDimensionCreated)
                        list_customDimensionUpdated.append(customDimensionUpdated)

    # Final python list which includes all retrieved custom dimensions data from Google Analytics
    final_custom_dimensions_data_list = [list_accountId, list_account, list_webPropertyId, list_internalWebPropertyId, list_webProperty, 
                            list_customDimensionName, list_customDimensionIndex, list_customDimensionScope, list_customDimensionActive,
                            list_customDimensionCreated, list_customDimensionUpdated]

    return final_custom_dimensions_data_list


def print_table_to_csv(data_list, filename):
    """Print input list of lists in a csv format in the same folder as this scripts.

    Args:
        data_list: A list of lists populated with data.
        filename: A file name in string format used for the output file.

    Returns:
        None
    """
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        for iter in range(len(data_list[0])):
            writer.writerow([x[iter] for x in data_list])


def main():
    # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/analytics.readonly']
    key_file_location = 'KEY_JSON_FILEPATH'

    output_csv_filename = "GoogleAnalyticsCustomDimensionsList.csv"

    # Authenticate and construct service.
    service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=scope,
            key_file_location=key_file_location)

    final_custom_dimensions_data_list = get_custom_dimensions_list(service)
    print_table_to_csv(final_custom_dimensions_data_list, output_csv_filename)


if __name__ == '__main__':
    main()