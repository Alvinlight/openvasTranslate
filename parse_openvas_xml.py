import xmltodict
import os


def restore_xml_escape_char(xml_string):
    """还原xml字符串中的转义字符"""
    all_escape_char = {
        '&lt;': '<', '&gt;': '>', '&amp;': '&',
        '&quot;': '"', '&apos;': '\'', '&#39;': '\'',
    }
    for k, v in all_escape_char.items():
        if k in xml_string:
            xml_string = xml_string.replace(k, v)
    return xml_string


def get_risk(cvss):
    if cvss is None or cvss == '':
        return '信息'
    cvss = float(cvss)
    if cvss >= 9:
        return '严重'
    if cvss >= 7:
        return '高危'
    if cvss >= 4:
        return '中危'
    if cvss > 0:
        return '低危'
    return '信息'


def parse_openvas_xml_report(xml_path):
    with open(xml_path, 'r') as f:
        response = xmltodict.parse(f.read())

    all_info = []
    os = response['report']['report']['os']
    if os['count']:
        computer = os['count']

    host = response['report']['report']['host']
    if host.get('ip'):
        ip = host.get('ip')

    if host.get('result_count'):
        hole = {}
        host_dic = host.get('result_count')
        hole['high'] = host_dic['hole']['page']
        hole['medium'] = host_dic['warning']['page']
        hole['low'] = host_dic['info']['page']
        hole['sum'] = int(hole['high']) + int(hole['medium']) + int(hole['low'])
    if int(hole['high']):
        risk_level = '高危'
    elif (hole['medium']):
        risk_level = '中危'
    elif (hole['low']):
        risk_level = '低危'
    else:
        risk_level = '良好'
    

    if host.get('detail'):
        os_list = host.get('detail')
        # print(type(os_name))
        if not isinstance(os_list, list):
            os_list = [os_list]
        for data_os in os_list:
            if 'name' in data_os:
                if data_os['name'] == 'OS':
                    os = data_os['value']
                    break
    total = {'ip':ip, 'hole':hole, 'risk_level':risk_level, 'computer':computer, 'os':os}
    all_info.append(total)

    results = response['report']['report']['results']
    if results.get('result'):
        result_list = results.get('result')
        if not isinstance(result_list, list):
            result_list = [result_list]
        for result in result_list:
            # print('=============================================================================================')
            severity = result['severity']
            if float(severity) > 0:
                name = result['name']  # certainly exist
                name = ' '.join(name.split())
                name = restore_xml_escape_char(name)
                host = result['host']['#text']
                port = result['port']
                qod = result['qod']['value'] + '%'
                nvt = result['nvt']
                tags = nvt['tags']
                summary = ''
                for tag in tags.split('|'):
                    if tag[:8] == 'summary=':  # certainly exist
                        summary = ' '.join(tag[8:].split())
                        summary = restore_xml_escape_char(summary)
                    if tag[:8] == 'insight=':  # certainly exist
                        evidence_back = ' '.join(tag[8:].split())
                        evidence_back = restore_xml_escape_char(evidence_back)
                        break
                solution = nvt['solution']['#text']  # may be ''
                solution = ' '.join(solution.split())
                solution = restore_xml_escape_char(solution)
                if result['description']:
                    evidence = result['description']
                else:
                    evidence = evidence_back
                cves = []
                if nvt.get('refs'):
                    refs = nvt['refs']['ref']
                    if isinstance(refs, list):
                        for ref in refs:
                            if ref['@type'] == 'cve' or 1==1:
                                cves.append(ref['@id'])
                    else:
                        if refs['@type'] == 'cve' or 1==1:
                            cves.append(refs['@id'])
                cves = ', '.join(cves)
                risk = get_risk(severity)
                result = {'name': name, 'host': host, 'port': port, 'severity': severity, 'qod': qod,
                          'risk': risk, 'summary': summary, 'solution': solution, 'evidence':evidence, 'cve': cves}
                all_info.append(result)

    return all_info


# if __name__ == "__main__":
#     xml_path = os.getcwd() + '/report-123.xml'
#     report = parse_openvas_xml_report(xml_path)
#     print(report)