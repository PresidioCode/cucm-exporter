# functions for cucm export
def export_users(ucm_axl):
    """
    retrieve users from ucm
    """
    try:
        user_list = ucm_axl.get_users(
            tagfilter={
                "userid": "",
                "firstName": "",
                "lastName": "",
                "directoryUri": "",
                "telephoneNumber": "",
                "enableCti": "",
                "mailid": "",
                "primaryExtension": {"pattern": "", "routePartitionName": ""},
                "enableMobility": "",
                "homeCluster": "",
                "associatedPc": "",
                "enableEmcc": "",
                "imAndPresenceEnable": "",
                "serviceProfile": {"_value_1": ""},
                "status": "",
                "userLocale": "",
                "title": "",
                "subscribeCallingSearchSpaceName": "",
                "ldapDirectoryName": "",
                "accountType": "",
                "authenticationType": "",
                "enableUserToHostConferenceNow": "",
                "attendeesAccessCode": "",
            }
        )
        all_users = []

        for user in user_list:
            # print(user)
            user_details = {
                "userid": user.userid,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "telephoneNumber": user.telephoneNumber,
                "primaryExtension": user.primaryExtension.pattern,
                "directoryUri": user.directoryUri,
                "mailid": user.mailid,
            }

            all_users.append(user_details)
            print(
                f"{user_details.get('userid')} -- {user_details.get('firstName')} {user_details.get('lastName')}:  {user_details.get('primaryExtension')}"
            )

        print("-" * 35)
        print(f"number of users: {len(all_users)}")
        # print(user_list)
        # print(json.dumps(all_users, indent=2))
        return all_users
    except Exception as e:
        return []


def export_phones(ucm_axl):
    """
    Export Phones
    """
    try:
        phone_list = ucm_axl.get_phones(
            tagfilter={
                "name": "",
                "description": "",
                "product": "",
                "model": "",
                "class": "",
                "protocol": "",
                "protocolSide": "",
                "callingSearchSpaceName": "",
                "devicePoolName": "",
                "commonDeviceConfigName": "",
                "commonPhoneConfigName": "",
                "networkLocation": "",
                "locationName": "",
                "mediaResourceListName": "",
                "networkHoldMohAudioSourceId": "",
                "userHoldMohAudioSourceId": "",
                "loadInformation": "",
                "securityProfileName": "",
                "sipProfileName": "",
                "cgpnTransformationCssName": "",
                "useDevicePoolCgpnTransformCss": "",
                "numberOfButtons": "",
                "phoneTemplateName": "",
                "primaryPhoneName": "",
                "loginUserId": "",
                "defaultProfileName": "",
                "enableExtensionMobility": "",
                "currentProfileName": "",
                "loginTime": "",
                "loginDuration": "",
                # "currentConfig": "",
                "ownerUserName": "",
                "subscribeCallingSearchSpaceName": "",
                "rerouteCallingSearchSpaceName": "",
                "allowCtiControlFlag": "",
                "alwaysUsePrimeLine": "",
                "alwaysUsePrimeLineForVoiceMessage": "",
            }
        )

        all_phones = []

        for phone in phone_list:
            # print(phone)
            phone_details = {
                "name": phone.name,
                "description": phone.description,
                "product": phone.product,
                "model": phone.model,
                "protocol": phone.protocol,
                "protocolSide": phone.protocolSide,
                "callingSearchSpaceName": phone.callingSearchSpaceName._value_1,
                "devicePoolName": phone.defaultProfileName._value_1,
                "commonDeviceConfigName": phone.commonDeviceConfigName._value_1,
                "commonPhoneConfigName": phone.commonPhoneConfigName._value_1,
                "networkLocation": phone.networkLocation,
                "locationName": phone.locationName._value_1,
                "mediaResourceListName": phone.mediaResourceListName._value_1,
                "networkHoldMohAudioSourceId": phone.networkHoldMohAudioSourceId,
                "userHoldMohAudioSourceId": phone.userHoldMohAudioSourceId,
                "loadInformation": phone.loadInformation,
                "securityProfileName": phone.securityProfileName._value_1,
                "sipProfileName": phone.sipProfileName._value_1,
                "cgpnTransformationCssName": phone.cgpnTransformationCssName._value_1,
                "useDevicePoolCgpnTransformCss": phone.useDevicePoolCgpnTransformCss,
                "numberOfButtons": phone.numberOfButtons,
                "phoneTemplateName": phone.phoneTemplateName._value_1,
                "primaryPhoneName": phone.primaryPhoneName._value_1,
                "loginUserId": phone.loginUserId,
                "defaultProfileName": phone.defaultProfileName._value_1,
                "enableExtensionMobility": phone.enableExtensionMobility,
                "currentProfileName": phone.currentProfileName._value_1,
                "loginTime": phone.loginTime,
                "loginDuration": phone.loginDuration,
                # "currentConfig": phone.currentConfig,
                "ownerUserName": phone.ownerUserName._value_1,
                "subscribeCallingSearchSpaceName": phone.subscribeCallingSearchSpaceName._value_1,
                "rerouteCallingSearchSpaceName": phone.rerouteCallingSearchSpaceName._value_1,
                "allowCtiControlFlag": phone.allowCtiControlFlag,
                "alwaysUsePrimeLine": phone.alwaysUsePrimeLine,
                "alwaysUsePrimeLineForVoiceMessage": phone.alwaysUsePrimeLineForVoiceMessage,
            }
            all_phones.append(phone_details)

            print(f"exporting: {phone.name}: {phone.model} - {phone.description}")

        print("-" * 35)
        print(f"number of phones: {len(all_phones)}")
        return all_phones
    except Exception as e:
        return []


def export_siptrunks(ucm_axl):
    try:
        all_sip_trunks = []
        sip_trunks = ucm_axl.get_sip_trunks(
            tagFilter={
                "name": "",
                "description": "",
                "callingSearchSpaceName": "",
                "sipProfileName": "",
                "mtpRequired": "",
                "sigDigits": "",
            }
        )
        for siptrunk in sip_trunks:
            trunk = {}
            trunk["name"] = siptrunk.name
            trunk["sipProfileName"] = siptrunk.sipProfileName
            trunk["callingSearchSpace"] = siptrunk.callingSearchSpaceName
            trunk["mtpRequired"] = siptrunk.mtpRequired
            trunk["sigDigits"] = siptrunk.sigDigits
            all_sip_trunks.append(trunk)
        return all_sip_trunks
    except Exception as e:
        return []


def export_phone_registrations(ucm_axl, ucm_ris):
    """
    Export Phone Registrations
    """
    nodes = ucm_axl.list_process_nodes()
    del nodes[0]  # remove EnterpriseWideData node
    subs = []
    for node in nodes:
        subs.append(node.name)
    phones = ucm_axl.get_phones(tagfilter={"name": ""})
    all_phones = []
    phone_reg = []
    reg = {}
    for phone in phones:
        all_phones.append(phone.name)
    limit = lambda all_phones, n=1000: [
        all_phones[i : i + n] for i in range(0, len(all_phones), n)
    ]
    groups = limit(all_phones)
    for group in groups:
        registered = ucm_ris.checkRegistration(group, subs)
        if registered["TotalDevicesFound"] < 1:
            print("no devices found!")
        else:
            reg["user"] = registered["LoginUserId"]
            reg["regtime"] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(registered["TimeStamp"])
            )
            for item in registered["IPAddress"]:
                reg["ip"] = item[1][0]["IP"]
            for item in registered["LinesStatus"]:
                reg["primeline"] = item[1][0]["DirectoryNumber"]
            reg["name"] = registered["Name"]
            print(f"exporting: {reg['name']}: {reg['ip']} - {reg['regtime']}")
            phone_reg.append(reg)

    print("-" * 35)
    print(f"number of registered phones: {len(phone_reg)}")
    return phone_reg


def export_translations(ucm_axl):
    try:
        all_translations = []
        translations = ucm_axl.get_translations()
        for translation in translations:
            xlate = {}
            xlate["pattern"] = translation.pattern
            xlate["description"] = translation.description
            xlate["routePartition"] = translation.routePartitionName._value_1
            xlate["callingSearchSpace"] = translation.callingSearchSpaceName._value_1
            xlate[
                "calledPartyTransformationMask"
            ] = translation.calledPartyTransformationMask
            xlate[
                "callingPartyTransformationMask"
            ] = translation.callingPartyTransformationMask
            all_translations.append(xlate)
        return all_translations
    except Exception as e:
        return []
