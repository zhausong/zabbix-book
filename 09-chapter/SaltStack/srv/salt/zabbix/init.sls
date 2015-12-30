zabbix-agent:
    service:
        - running
        - watch:
            - file: zabbix_agentd.conf
            - file: zabbix_agentd.conf.d
            - pkg: zabbix-agentd
    require:
        - pkg: zabbix-agent

zabbix-agentd:
    pkg.installed:
        - name: zabbix-agent
        - version: '2.2.2-0.el6.zbx'
        - skip_verify: True
        - skip_suggestions: True
        - fromrepo: zabbix
        - refresh: True

zabbix_agentd.conf:
    file.managed:
        - name: /etc/zabbix/zabbix_agentd.conf
        - source: salt://zabbix/conf/zabbix_agentd.conf
        - mode: 644
        - user: zabbix
        - group: zabbix
        - template: jinja

zabbix_agentd.conf.d:
    file.recurse:
        - name: /etc/zabbix/zabbix_agentd.conf.d
        - source: salt://zabbix/conf/zabbix_agentd.conf.d
        - include_empty: True
        - user: zabbix
        - group: zabbix
        - dir_mode: 755
        - file_mode: 644
        - template: jinja

scripts:
    file.recurse:
        - name: /etc/zabbix/scripts
        - source: salt://zabbix/scripts
        - include_empty: True
        - user: zabbix
        - group: zabbix
        - dir_mode: 755
        - file_mode: 700
