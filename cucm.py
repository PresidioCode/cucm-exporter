import time
import json


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
            }
        )
        all_users = []

        for user in user_list:
            # print(user)
            user_details = {}
            user_details['userid'] = user.userid
            user_details['firstName'] = user.firstName
            user_details['lastName'] = user.lastName
            user_details['telephoneNumber'] = user.telephoneNumber
            user_details['primaryExtension'] = user.primaryExtension.pattern
            user_details['directoryUri'] = user.directoryUri
            user_details['mailid'] = user.mailid

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
        print(e)
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
            line_details = ucm_axl.get_phone(name=phone.name)
            # print(line_details.lines.line)
            try:
                for line in line_details.lines.line:
                    # print(line)
                    phone_details[f"line_{line.index}_dirn"] = line.dirn.pattern
                    phone_details[f"line_{line.index}_routePartitionName"] = line.dirn.routePartitionName._value_1
                    phone_details[f"line_{line.index}_display"] = line.display
                    phone_details[f"line_{line.index}_e164Mask"] = line.e164Mask
            except Exception as e:
                print(e)
            all_phones.append(phone_details)

            print(
                f"exporting: {phone.name}: {phone.model} - {phone.description}")

        print("-" * 35)
        print(f"number of phones: {len(all_phones)}")
        return all_phones
    except Exception as e:
        print(e)
        return []


def export_siptrunks(ucm_axl):
    try:
        all_sip_trunks = []
        sip_trunks = ucm_axl.get_sip_trunks(
            tagfilter={
                "name": "",
                "description": "",
                "devicePoolName": "",
                "callingSearchSpaceName": "",
                "sipProfileName": "",
                "mtpRequired": "",
                "sigDigits": "",
                "destAddrIsSrv": "",
            }
        )
        for siptrunk in sip_trunks:
            trunk = {}
            trunk["name"] = siptrunk.name
            trunk["description"] = siptrunk.description
            trunk["devicePoolName"] = siptrunk.devicePoolName._value_1
            trunk["sipProfileName"] = siptrunk.sipProfileName._value_1
            trunk["callingSearchSpace"] = siptrunk.callingSearchSpaceName._value_1
            trunk["mtpRequired"] = siptrunk.mtpRequired
            trunk["sigDigits"] = siptrunk.sigDigits._value_1
            # TODO: get_siptrunk details for destinations
            trunk_details = ucm_axl.get_sip_trunk(name=siptrunk.name)
            destinations = trunk_details['return']['sipTrunk']['destinations']['destination']
            # print(destinations)
            for count, destination in enumerate(destinations):
                trunk[f'addressIpv4_{count}'] = destination.addressIpv4
                trunk[f'port_{count}'] = destination.port
                trunk[f'sortOrder_{count}'] = destination.sortOrder

            all_sip_trunks.append(trunk)
            # print(siptrunk)
            print(f"exporting: {siptrunk.name}: {siptrunk.description}")

        print("-" * 35)
        print(f"number of siptrunks: {len(all_sip_trunks)}")
        return all_sip_trunks
    except Exception as e:
        print(e)
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

    def limit(all_phones, n=1000): return [
        all_phones[i: i + n] for i in range(0, len(all_phones), n)
    ]
    groups = limit(all_phones)
    for group in groups:
        registered = ucm_ris.checkRegistration(group, subs)
        if registered["TotalDevicesFound"] < 1:
            print("no devices found!")
        else:
            reg["user"] = registered["LoginUserId"]
            reg["regtime"] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(registered["TimeStamp"]))
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
            # print(translation)
            xlate = {}
            xlate["pattern"] = translation.pattern
            xlate["routePartition"] = translation.routePartitionName._value_1
            xlate["description"] = translation.description
            xlate["callingSearchSpace"] = translation.callingSearchSpaceName._value_1
            xlate["calledPartyTransformationMask"] = translation.calledPartyTransformationMask
            xlate["callingPartyTransformationMask"] = translation.callingPartyTransformationMask
            xlate["digitDiscardInstructionName"] = translation.digitDiscardInstructionName._value_1
            xlate["prefixDigitsOut"] = translation.prefixDigitsOut
            all_translations.append(xlate)
            print(
                f"exporting: {xlate['pattern']}: {xlate['routePartition']} - {xlate['description']} --> {xlate['calledPartyTransformationMask']}")
        print("-" * 35)
        print(f"number of translations: {len(all_translations)}")
        return all_translations
    except Exception as e:
        return []
