###
Mounted filesystem discovery: Free disk space on /var/named/chroot/etc/rndc.key	 	vfs.fs.size[/var/named/chroot/etc/rndc.key,free]
###

![图1](img/001.png)


![图2](img/002.png)


![图3](img/003.png)

int     VFS_FS_DISCOVERY(AGENT_REQUEST *request, AGENT_RESULT *result)
{       
        int             ret = SYSINFO_RET_FAIL;
        char            line[MAX_STRING_LEN], *p, *mpoint, *mtype;
        FILE            *f;
        struct zbx_json j;
        
        zbx_json_init(&j, ZBX_JSON_STAT_BUF_LEN);
        
        zbx_json_addarray(&j, ZBX_PROTO_TAG_DATA);
        
        if (NULL != (f = fopen("/proc/mounts", "r")))
        {      
                while (NULL != fgets(line, sizeof(line), f))
                {
                        if (NULL == (p = strchr(line, ' ')))
                                continue;
        
                        mpoint = ++p;
        
                        if (NULL == (p = strchr(mpoint, ' ')))
                                continue;
        
                        *p = '\0';
        
                        mtype = ++p;
        
                        if (NULL == (p = strchr(mtype, ' ')))
                                continue;
        
                        *p = '\0';
        
                        zbx_json_addobject(&j, NULL);
                        zbx_json_addstring(&j, "{#FSNAME}", mpoint, ZBX_JSON_TYPE_STRING);
                        zbx_json_addstring(&j, "{#FSTYPE}", mtype, ZBX_JSON_TYPE_STRING);
                        zbx_json_close(&j);
                }
        
                zbx_fclose(f);
        
                ret = SYSINFO_RET_OK;
        }

![图4](img/004.png)
